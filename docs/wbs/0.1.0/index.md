# WBS — AdversarialDebate v0.1.0 (Index)

> Work breakdown structure for v0.1.0 "Prove the Loop". 11 milestones, ~55 tasks, each task wired to a live GitHub issue attached to milestone `[Release-Milestone] v0.1.0`. PRD coupling is explicit: every milestone cites the PRD sections it implements.

**Milestone:** `[Release-Milestone] v0.1.0` · **Window:** Aug 25-31, 2026 · **Exit bar:** one inspectable case where independent review surfaced what a single reviewer missed — or a disagreement report that improved a human call ([PRD §7.1](../../design/prd/07-success-metrics.md)).

## Milestones

| M | File | Focus | Issues | Depends on |
|---|------|-------|--------|-----------|
| M1 | [M1-foundation-core-schemas.md](M1-foundation-core-schemas.md) | Repo scaffold, core Pydantic schemas, config, CI gates | #1-#7 | — |
| M2 | [M2-provider-layer-byom.md](M2-provider-layer-byom.md) | Provider registry, OpenAI-compatible transport, PydanticAI/LangGraph adapters, seeds, scripted reviewers | #8-#13 | M1 |
| M3 | [M3-isolation-engine.md](M3-isolation-engine.md) | Reviewer sessions, revelation gate, commit immutability, leakage test suite | #14-#17 | M1 |
| M4 | [M4-normalizer-pr-adapter.md](M4-normalizer-pr-adapter.md) | Normalizer framework, git diff parser, chunking, fixture corpus | #18-#22 | M1 |
| M5 | [M5-debate-controller.md](M5-debate-controller.md) | Bounded rounds, point-by-point enforcement, caps, degradation detection | #23-#26 | M2, M3 |
| M6 | [M6-evidence-convergence.md](M6-evidence-convergence.md) | Claim lifecycle, convergence score, theater detector, evidence validation | #27-#30 | M5 |
| M7 | [M7-synthesis-reports.md](M7-synthesis-reports.md) | Joint verdict, disagreement report, fail-closed synthesis, JSONL export | #31-#34 | M6 |
| M8 | [M8-persistence-resilience.md](M8-persistence-resilience.md) | SQLite store, schema versioning, resume, budget/backoff, crash safety | #35-#39 | M7 |
| M9 | [M9-cli-surface.md](M9-cli-surface.md) | init / review / report / resume / transcript commands; terminal rendering | #40-#45 | M8 |
| M10 | [M10-field-test-tier0.md](M10-field-test-tier0.md) | Public-PR corpus, flakiness sweep, baseline comparison, field-test report | #46-#50 | M9 |
| M11 | [M11-release.md](M11-release.md) | Security sweep, docs, OSS files, OpenSSF, packaging, PyPI, public flip, articles | #51-#57 | M10 |

**Total: 57 issues · milestone `[Release-Milestone] v0.1.0`**

```
M1 ──┬──► M2 ──┐
     ├──► M3 ──┼──► M5 ──► M6 ──► M7 ──► M8 ──► M9 ──► M10 ──► M11
     └──► M4 ──┘
(M3 ∥ M4 after M1; M5 needs M2 providers + M3 isolation + M4 artifacts)
```

## Global exit gates (every milestone)

- Ruff clean, mypy strict clean, ≥95% coverage on touched code
- Zero paid-LLM calls in CI (scripted reviewers only)
- Isolation invariant tests green after every merge into M3+ surfaces

## Traceability

| PRD source | Implemented by |
|-----------|----------------|
| [05-features F1-F10](../../design/prd/05-features.md) | M2-M9 tasks (F# cited per task) |
| [02-architecture §2.3 invariant](../../design/prd/02-architecture.md) | M3 (mechanically enforced + tested) |
| [02 §2.7 convergence](../../design/prd/02-architecture.md), [§2.8 chunking](../../design/prd/02-architecture.md) | M6, M4 |
| [06 §6.4 reproducibility](../../design/prd/06-security-baseline.md), [§6.5 ops failures](../../design/prd/06-security-baseline.md) | M2 (seeds/prompt versions), M8 (resume/budget/backoff) |
| [07 §7.6 methodology](../../design/prd/07-success-metrics.md) | M6 (theater rate), M10 (flakiness, baseline, report) |
| [field-testing-strategy Tier 0](../../field-test/field-testing-strategy.md) | M10 |
| [13-failure-modes](../../design/prd/13-failure-modes.md) | M5 (FM-9 degradation), M6 (FM-2/FM-7), M4 (FM-10) |

## Conventions

- Every task id `T<m>.<k>` maps to exactly one GitHub issue (`T2.3 (#10)` → issue #N, label `milestone-M2`).
- Issue bodies carry: what/why, PRD references, acceptance criteria checklist.
- A task is done when its issue closes AND the global exit gates pass.
