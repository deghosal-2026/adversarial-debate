# 02 — Architecture (What We're Building)

> Sub-document of the [Design overview](../README.md). Component overview, pipeline stages, and data model for v0.1.0. The canonical deep spec lives in `docs/architecture/architecture-v0.1.0.md`.

## 2.1 The loop

```
                     ┌──────────────────────────────┐
   artifact ───────► │  Input Normalizer            │  PR diff / contract / memo /
                     └──────────┬───────────────────┘  incident / change request
                                │  common ReviewArtifact schema
                  ┌─────────────┴─────────────┐
                  ▼                           ▼
            ┌──────────┐                ┌──────────┐
            │ Reviewer A│   no peeking  │ Reviewer B│   isolated contexts,
            └────┬─────┘                └────┬─────┘   independent evidence gathering
                 │ structured review         │ structured review
                 │  (committed, immutable)   │  (committed, immutable)
                 └────────────┬──────────────┘
                              ▼  revelation gate opens
                   ┌─────────────────────┐
                   │  Debate Controller  │   bounded rounds; mandatory
                   └─────────┬───────────┘   point-by-point response
                             ▼
                   ┌─────────────────────┐
                   │  Evidence Tracker   │   claims · objections · concessions
                   └─────────┬───────────┘   unresolved points · evidence shifts
                             ▼
                    convergence detected?
                    │                 │
                   yes                no
                    ▼                 ▼
            Joint Verdict      Disagreement Report
        (+ surviving args       (+ would_resolve_if
          from both sides)        per unresolved point)
                    └────────┬────────┘
                             ▼
                    Audit Log (SQLite)
              full lineage: every message, claim, concession
```

## 2.2 Components

| # | Component | Responsibility | v0.1.0 notes |
|---|-----------|----------------|--------------|
| 1 | **Input Normalizer** | Converts domain artifacts into a `ReviewArtifact`: metadata, content blocks, claims-to-review, rubric hints | One domain adapter ships: PR review |
| 2 | **Independent Reviewer Engine** | Runs two isolated passes; enforces context separation; collects committed structured reviews | Isolation is engine-enforced, not prompt-enforced |
| 3 | **Debate Controller** | Bounded rebuttal rounds; each round requires direct response to outstanding objections; tracks round state | Default 2 rounds, configurable |
| 4 | **Evidence Tracker** | First-class objects: `Claim`, `Objection`, `Concession`, `UnresolvedPoint`, evidence references | Powers both outputs |
| 5 | **Synthesis Layer** | Convergence scoring → Joint Verdict or Disagreement Report | Report includes `would_resolve_if` |
| 6 | **Audit Log** | Persists full transcript lineage to SQLite | Tamper-evident ordering; exportable JSONL |

## 2.3 The one non-negotiable invariant

> **Reviewer B cannot see reviewer A's output until B has fully committed its own review — and vice versa.**

This is enforced mechanically: separate conversation contexts, no shared memory, revelation handled by the engine as an explicit state transition (`isolated → revealed`). Every audit log proves it happened that way. Everything else in the architecture is secondary to this rule.

## 2.4 Data model (draft)

```
ReviewArtifact   id, domain, source_uri, content_blocks[], rubric_hints, created_at
ReviewerSession  id, artifact_id, side(A|B), provider, model, status(committed|revealed|debating)
Review           id, session_id, claims[], risks[], confidence, committed_at
Claim            id, review_id, text, severity, evidence_refs[], status(open|conceded|upheld|resolved)
Objection        id, target_claim_id, argument, round, evidence_refs[]
Concession       id, claim_id, by_side, round, rationale
UnresolvedPoint  id, claim_ids[], position_a, position_b, would_resolve_if
DebateRound      id, artifact_id, index, messages[], started_at, ended_at
Outcome          id, artifact_id, kind(verdict|disputed), converged_count, total_claims, report_ref
Transcript       jsonl blob per artifact: every LLM call, in order
```

## 2.5 Provider layer

- Model-agnostic registry (config-driven): any OpenAI-compatible endpoint; PydanticAI and LangGraph adapters.
- **Heterogeneous pairs encouraged** (different model families) — diversity of thought measurably beats homogeneous debate ([Mila 2025](https://www.alphaxiv.org/overview/2410.12853v2)).
- Same-model-twice mode supported when isolation is strict enough; surfaced honestly in reports.
- Zero paid LLM calls in CI; hermetic tests with scripted reviewers.

## 2.6 Design principles

1. Independence before interaction.
2. Disagreement is a feature, not a bug.
3. Preserve minority arguments when they matter.
4. Optimize for auditability, not theatrical conversation.
5. Forced personas are banned — agents argue their own committed positions (research shows assigned stances produce rhetorical rigidity, not truth).

## 2.7 Convergence detection (the hardest design problem)

The engine must decide when two reviews have "converged" — but semantic equivalence of claims is not trivially computable. Our approach for v0.1.0:

- **Claim-level state tracking** — each `Claim` has a status lifecycle (`open → conceded | upheld | resolved`). Convergence means no `open` claims remain at debate end.
- **Objection-driven convergence** — an objection is resolved when the objecting party either concedes (accepts the counter-argument) or the target claim is modified in revision; unresolved objections become `UnresolvedPoint` entries.
- A **convergence score** is computed as `resolved_claims / total_claims`. Reports display this score alongside the verdict, never hiding the denominator.

Known limitation: a claim can be *technically* conceded while the underlying disagreement persists (concession-theater). Mitigations: `would_resolve_if` on every unresolved point (what concrete evidence/action would close this?) and the theater-rate metric (zero state-change debates flagged explicitly).

## 2.8 Long-artifact / context-window strategy

Contracts, large PRs, and incident timeliness can exceed single-reviewer context windows. v0.1.0 scope:

- **Chunking** — artifacts exceeding the active model's context receive a deterministic first pass: split into content blocks (by file for PRs, by clause group for contracts), each reviewed independently by the same agent, then merged via structured merge prompts.
- **Claim deduplication** — overlapping claims across chunks merged in the evidence tracker; cross-chunk contradictions surfaced as `UnresolvedPoint` entries.
- **Context budget reporting** — every report states the model context window, artifact size, chunk count, and whether any chunk exceeded 80% of the budget. This is an honest signal for downstream reliability.
- **v0.2.0 improvement:** hierarchical summarization per chunk to reduce budget pressure without losing claim granularity.

Long-term: this is a provider-layer concern. Different models have different windows; the engine adapts its chunking strategy to the user-chosen model, not the other way around.
