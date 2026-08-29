# WBS — AdversarialDebate v0.2.2 (Index)

> Work breakdown structure for v0.2.2 "Measurement Infrastructure". 3 milestones, 10+ tasks, each task wired to a live GitHub issue attached to milestone `v0.2.2-M1` through `v0.2.2-M3`. This cycle focuses on three community-raised gaps from the v0.2.1 release: the permutation control for LLM-as-judge (Vinh Nguyen), the noise-floor baseline (Bert Shim), and the shared RLHF design note (Reid Marlow).

**Milestone:** M1-M3 · **Window:** Aug 29-Sep 5, 2026 · **Status:** 🔄 In progress

| M | File | Focus | Issues | Status |
|---|------|-------|--------|--------|
| M1 | [M1-measurement-gaps.md](M1-measurement-gaps.md) | Permutation control, noise-floor baseline, shared RLHF design note | #164-#166 | 🔄 In progress |
| M2 | [M2-release-readiness.md](M2-release-readiness.md) | Tests, docs, security, PyPI, tag, merge | #167-#172 | ⬜ Pending |
| M3 | [M3-vault-update.md](M3-vault-update.md) | Update unpublished articles with v0.2.2 findings | #173 | ⬜ Pending |

**Total: 10 issues · 3 milestones (M1-M3)**

```
M1 ──► M2 ──► M3
```

## Global exit gates (every milestone)

- Ruff clean, mypy strict clean, full test suite green
- Zero paid-LLM calls in CI (scripted reviewers only)
- Code review required before merge to `feature-v0.2.2`
- All new code has tests covering the regression case

## Conventions

- Every milestone end must involve: code review, run all tests, lint strict clean, commit, push to `feature-v0.2.2`
- Issue bodies carry: what/why, reproduction steps, fix description, acceptance criteria
- A task is done when its issue closes AND the global exit gates pass
- No field test sweep required for this release — all changes are measurement infrastructure on existing data