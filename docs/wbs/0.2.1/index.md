# WBS — AdversarialDebate v0.2.1 (Index)

> Work breakdown structure for v0.2.1 "Separate the Signal". 3 milestones, 26+ tasks, each task wired to a live GitHub issue attached to milestone `v0.2.1-M1` through `v0.2.1-M3`. This cycle focuses on the three community-raised issues from the v0.2.0 release: the model pairing confound (Heinrich Neb), the row-count invariant gap (Heinrich Neb), and the false-negative blind spot (Heinrich Neb).

**Milestone:** M1-M3 · **Window:** Sep 1-30, 2026 · **Status:** ✅ COMPLETE — v0.2.1 shipped Aug 28, 2026.

| M | File | Focus | Issues | Status |
|---|------|-------|--------|--------|
| M1 | [M1-core-fixes.md](M1-core-fixes.md) | DeepSeek+GPT pairing experiment, row-count invariants, false-negative measurement, unit tests | #127-#129, #153-#155 | ✅ Complete |
| M2 | [M2-field-test.md](M2-field-test.md) | Field test plan, scripts, execution, conclusions, report | #130-#152 | ✅ Complete |
| M3 | [M3-release-readiness.md](M3-release-readiness.md) | Security scan, tests, docs, PyPI, tag, merge to main | #138-#143 | ✅ Complete |

**Total: 26+ issues · 3 milestones (M1-M3)**

```
M1 ──► M2 ──► M3
```

## Global exit gates (every milestone)

- Ruff clean, mypy strict clean, full test suite green
- Zero paid-LLM calls in CI (scripted reviewers only)
- Code review required before merge to `rel-v0.2.1`
- All new code has tests covering the regression case

## Conventions

- Every milestone end must involve: code review, run all tests, lint strict clean, commit, push to `rel-v0.2.1`
- Issue bodies carry: what/why, reproduction steps, fix description, acceptance criteria
- A task is done when its issue closes AND the global exit gates pass