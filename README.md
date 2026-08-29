<div align="center">

# AdversarialDebate

[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-v0.2.1-brightgreen)]()
[![PyPI](https://img.shields.io/pypi/v/adversarial-debate)](https://pypi.org/project/adversarial-debate/)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/14254/badge)](https://www.bestpractices.dev/en/projects/14254/passing)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000)](https://github.com/astral-sh/ruff)

**A multi-agent adversarial review engine. Two independent LLMs analyze the same artifact without seeing each other's answers, debate their conclusions point by point, and produce either a converged decision — or a structured disagreement report that preserves the dissent.**

</div>

> [!NOTE]
> **Status:** v0.2.1 shipped Aug 2026. Field-tested on 150 artifacts across 4 domains — 367 debates, $0.57 total cost.
> **Key finding:** The Mistral effect is confirmed — Mistral is the unique variable driving productive debate, not lab diversity.
> **Core improvement:** Row-count invariants at all pipeline seams prevent silent data loss. False-negative measurement (1.7–3.4% miss rate) provides recall data for the first time.
> The core isolation rule is mechanically enforced: **reviewer B cannot see reviewer A's answer until it has fully committed its own.**

---

## Why

Most AI "second opinions" are fake. The usual pattern is one model proposes an answer and a second model is asked to double-check — *after* being shown the first model's framing, assumptions, and conclusion. That setup almost guarantees convergence, even when convergence should not happen. It looks careful. It is actually agreement with extra steps.

The most expensive agent failures are rarely about missing information. They are about prematurely accepted reasoning: a pull request that feels "probably safe," an architecture change that seems "good enough," an incident hypothesis that sounds plausible in the first ten minutes. These are exactly the decisions where human teams rely on *independent* review and constructive conflict.

AdversarialDebate productizes that discipline for LLM systems:

- **Independent passes** — agents analyze the same input in strict isolation.
- **Delayed revelation** — conclusions are revealed only after both sides commit.
- **Structured challenge** — each agent must respond point by point: assumptions, evidence quality, edge cases, risk exposure.
- **Dissent preservation** — if disagreement survives the debate, the system ships a structured disagreement report instead of pretending consensus exists.

The outcome is not always consensus. Sometimes the most valuable result is a sharply defined disagreement showing exactly where uncertainty lives.

## Quickstart

```bash
pip install adversarial-debate

# Scaffold config
advdeb init

# Edit in your API keys
# $EDITOR advdeb.toml

# Review a PR
advdeb review --pr https://github.com/kubernetes/kubernetes/pull/140860 --domain pr_review

# View the report
advdeb report <run_id>

# Export the transcript
advdeb transcript <run_id> --export jsonl
```

See [docs/reference/quickstart.md](docs/reference/quickstart.md) for the full walkthrough.

## What It Is

### The Independent Pass → Debate → Decide Loop

```
                    ┌────────────────────────────┐
        input ────► │  Input Normalizer          │  PR diff / ADR / incident / plan
                    └──────────┬─────────────────┘
                               │  same artifact, isolated contexts
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
           ┌──────────┐                ┌──────────┐
           │ Agent A  │   no peeking   │ Agent B  │
           └────┬─────┘                └────┬─────┘
                │ commit review             │ commit review
                └────────────┬──────────────┘
                             ▼  revelation gate opens
                    ┌─────────────────┐
                    │ Debate Controller│  bounded rounds, point-by-point
                    └────────┬─────────┘
                             ▼
              converged? ─── yes ──► Joint Verdict (strongest surviving arguments)
                  │
                  no
                  ▼
       Disagreement Report (unresolved points + what would resolve them)
```

### Key Properties

| Property | Description |
|----------|-------------|
| **Independence before interaction** | Reviewers never see each other's output before committing |
| **Disagreement is a feature** | Forced synthetic consensus hides exactly what you need to see |
| **Evidence over rhetoric** | Confidence tied to cited evidence and failure modes, not tone |
| **Auditability** | Full transcript lineage: every claim, objection, concession, verdict |

## Architecture (v0.2.0)

| Component | Responsibility |
|-----------|----------------|
| **Input Normalizer** | Converts PRs, docs, incidents, plans into a common review schema |
| **Independent Reviewer Engine** | Isolated review passes with strict context separation |
| **Debate Controller** | Bounded rebuttal rounds; tracks argument state |
| **Evidence Tracker** | Claims, supporting evidence, unresolved points, concessions |
| **Synthesis Layer** | Joint decision or structured disagreement report |
| **Audit Log** | Persists full review lineage (SQLite) |

**Current stack:** Python · Pydantic schemas · SQLite · PydanticAI / LangGraph / raw-API adapters · CLI and field-test scripts.

**Planned additions:** FastAPI service · React side-by-side review UI · broader adapter coverage.

## Example Output

```yaml
verdict: DISPUTED            # 6 of 9 points converged
resolved:
  - claim: "Rate-limit bump is safe under current traffic"
    status: agreed_by_both
unresolved:
  - claim: "Expand/contract migration is safe for pr-482"
    agent_a: sufficient as written
    agent_b: needs lock-timeout analysis on orders table (~40GB)
    would_resolve_if: load test at production row count
audit: transcripts/2026-08-pr482.jsonl
```

## Use Cases

- Code review — two reviewers, one risky diff, zero shared bias
- Architecture tradeoff evaluation under uncertainty
- Change risk assessment before rollout
- Incident hypothesis review — competing root causes, argued out
- Migration plan audit

## Roadmap

| Version | Scope |
|---------|-------|
| v0.1.0 | Independent dual-review pass, bounded debate, claims/objections/concessions schema, consensus + disagreement reports, PR-review domain adapter, transcripts, field test on real public-repo PRs |
| **v0.2.0** | Corrected field-test pipeline, mixed-domain corpus (PR review, incident response, change management, security incidents), subset-based model validation, stronger report integrity |
| v0.3.0 | N-agent mode, side-by-side debate visualization, diversity/convergence-quality metrics |
| v0.4.0 | Eval benchmark scenarios, approval-workflow integration, learning from past unresolved disagreements |

## Field Test Reports

- [v0.2.0 Full Corpus Report](docs/field-test/v0.2.0/FIELD_TEST_REPORT_full_corpus.md) — 150 artifacts, 4 domains, 217 debates, $0.42
- [v0.2.0 Field Test Plan](docs/field-test/v0.2.0/field-test-plan.md) — corpus design, model strategy, success criteria
- [v0.1.0 Full Corpus Report](docs/field-test/v0.1.0/FIELD_TEST_REPORT_full_corpus.md) — 70 PRs, 6 pairs, 411 debates, $0.53
- [v0.1.0 Field Test Plan](docs/field-test/v0.1.0/field-test-plan.md) — original PR-only field test plan
- [Field Testing Strategy](docs/field-test/field-testing-strategy.md) — 4-tier cross-domain plan

### v0.2.0 Key Results

| Metric | v0.1.0 | v0.2.0 |
|--------|--------|--------|
| Artifacts | 70 PRs | 150 across 4 domains |
| Debates | 411 | 217 |
| Theater | 0.2% | 0% |
| Binary bar (MATCH) | 81% | 88.7% |
| Verdict stability | 96% | 100% (sampled) |
| Total cost | $0.53 | $0.42 |
| Primary pair | pair5 (DeepSeek+Mistral) | pair3 (GPT+Mistral) |

### v0.2.0 Artifacts

- Corpus: `results/field-test/v0.2.0/corpus.csv`
- Candidate lists: `docs/field-test/v0.2.0/{incident_response,change_management,security_incidents}_corpus_candidates.csv`
- PR reuse list: `docs/field-test/v0.2.0/pr_reuse_80.csv`
- Validation subset: `results/field-test/v0.2.0/validation_subset.csv`
- Negative control subset: `results/field-test/v0.2.0/negative_control_subset.csv`
- Pair roles: `results/field-test/v0.2.0/SUBSETS.md`
- Analysis CSVs: `results/field-test/v0.2.0/analysis/`
- Ground truth: `results/field-test/v0.2.0/analysis/ground-truth-judged.csv`
- Flakiness: `results/field-test/v0.2.0/analysis/flakiness-summary.csv`
- Field test scripts: `scripts/README.md`

## Non-Goals

- Replacing human reviewers for irreversible high-risk decisions
- Forcing consensus when disagreement is more informative
- Optimizing speed over reasoning quality
- Being a generic chat wrapper around multiple models

## Honest Limitation

Debate does not guarantee truth. Two strong debaters can still miss the same blind spot, and poorly designed personas can turn useful disagreement into performance theater. The design answer: measure whether debate *changed* anything, and preserve dissent rather than flattening it.

## License

[MIT](LICENSE) © 2026 Debashish Ghosal
