# 05 — Features (What v0.1.0 Ships)

> Sub-document of the [Design overview](../README.md). Feature list for v0.1.0 — a lean MVP that proves the loop. Everything else is explicitly versioned.

## 5.1 Must-have (v0.1.0 — lean MVP)

The MVP proves one thing: two isolated reviewers produce materially different conclusions than a single reviewer, on real code, with full transcripts.

| # | Feature | Notes |
|---|---------|-------|
| F1 | **Independent dual-review pass** | Two isolated reviewer sessions per artifact; engine-enforced context separation |
| F2 | **Delayed answer revelation** | Explicit state transition `isolated → revealed`; provable from audit log |
| F3 | **Structured debate schema** | First-class `Claim`, `Objection`, `Concession`, `UnresolvedPoint` objects |
| F4 | **Bounded debate rounds** | Default 2 rounds; mandatory point-by-point response; configurable cap |
| F5 | **Converged-verdict output** | Joint decision + strongest surviving arguments from each side |
| F6 | **Disagreement-report output** | `resolved[]`, `unresolved[].position_a/position_b/would_resolve_if` |
| F7 | **PR-review domain adapter** | Git diff + metadata → `ReviewArtifact`; the only shipping domain |
| F8 | **Bring-your-own-model registry** | Config-driven; any OpenAI-compatible endpoint; PydanticAI + LangGraph adapters; heterogeneous pairs supported |
| F9 | **Transcript storage** | SQLite persistence of full lineage; JSONL export |
| F10 | **CLI** | `advdeb init`, `advdeb review --pr`, `advdeb report` |

**That's it.** No UI, no multi-language, no GitHub Action, no cost tiering. The MVP is terminal-only, English-only, PR-only. It proves the loop or it doesn't.

## 5.2 Deferred to v0.2.0 (explicitly)

| Feature | Why deferred |
|---------|-------------|
| F11 — Basic review UI | Terminal output proves the loop in 0.1; UI is adoption accelerator, not proof |
| F13 — Multi-language artifacts | English PRs are sufficient to prove independence; i18n is reach, not validation |
| GitHub Action wrapper | CLI is sufficient for 0.1; CI integration is 0.2 adoption work |
| Cost tiering | MVP uses one pair per run; tiering is optimization, not proof |
| Redaction hooks | No sensitive artifacts in 0.1 (public repos only) |
| Debate-usefulness score | Metric needs corpus to calibrate; ships with field-test data in 0.2 |
| Heterogeneous pairing presets | Config supports it; UX presets are 0.2 polish |

## 5.3 Adapter contribution protocol (design direction, spec in v0.1, code in v0.2)

Each domain adapter is a spec and an implementation — no engine changes required to add a new domain:

1. **Artifact normalizer** — converts domain-specific input → `ReviewArtifact` schema
2. **Claim extraction rubric** — what constitutes a relevant claim in this domain
3. **Evidence expectations** — what counts as evidence (diff lines, clause cross-refs, timeline entries)
4. **No engine changes required** — adapters sit in `adversarial_debate/adapters/<domain>/`

The protocol spec ships as a design document in v0.1; the first external adapter (change management) validates it in v0.2.

## 5.4 Mid-debate human injection (scoped to v0.3.0)

- **v0.1 stance:** human reads the final report only. Reports include `would_resolve_if`.
- **v0.3.0 commitment:** optional human-injection turn at any debate round; question + identity logged in audit trail.

## 5.5 API surface sketch (v0.1.0)

### CLI

```
advdeb init                                    # scaffold config
advdeb review --pr <url|path>                  # run a debate on a PR diff
advdeb report <artifact-id>                    # render the report
advdeb resume <artifact-id>                    # resume interrupted debate
advdeb transcript <artifact-id> --export jsonl # export full lineage
```

### Python API

```python
from adversarial_debate import Engine, ReviewConfig

engine = Engine(config="advdeb.toml")
result = engine.review(
    artifact="pr-482.diff",
    domain="pr_review",
    config=ReviewConfig(rounds=2, pair="diverse")
)

if result.verdict == "disputed":
    for point in result.unresolved:
        print(f"{point.position_a} vs {point.position_b}")
        print(f"  Resolve if: {point.would_resolve_if}")
```

### HTTP service (v0.5.0+ — not in MVP)

## 5.6 Explicitly out of scope for v0.1.0

- N-agent jury orchestration (→ AgentJury, v0.6.0)
- Fully automated production action (output is advisory to humans)
- Additional domain adapters beyond PR review (change-management is v0.2.0)
- Fine-tuning or training of any model
- Hosted multi-tenant service
- UI (terminal only in 0.1.0)
- Multi-language (English only in 0.1.0)
