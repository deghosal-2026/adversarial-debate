# WBS — AdversarialDebate v0.2.0 (Index)

> Work breakdown structure for v0.2.0 "Fix the Data". 8 milestones, 58+ tasks, each task wired to a live GitHub issue attached to milestone `M1`-`M8`. This cycle focuses on correcting the 54 bugs identified in the v0.1.0 postmortem, re-running field tests, and shipping a hardened release.

**Milestone:** M1-M8 · **Window:** Aug 28-31, 2026 · **Exit bar:** all 54 v0.1.0 bugs fixed, field-test reports corrected, security scan clean, PyPI publish, GitHub release.

## Milestones

| M | File | Focus | Issues | Depends on |
|---|------|-------|--------|-----------|
| M1 | [M1-core-engine-bugfixes.md](M1-core-engine-bugfixes.md) | Debate controller & evidence engine bugs | #58-#62, #65-#67, #71, #87-#91 | — |
| M2 | [M2-transport-script-infra.md](M2-transport-script-infra.md) | Provider transport, scripts, pricing, deps | #63-#64, #68-#70, #77-#81, #92, #95, #98-#101 | M1 |
| M3 | [M3-cli-adapter-integrations.md](M3-cli-adapter-integrations.md) | CLI output paths, adapter registration, metadata extraction, diff parser | #82-#86 | M1, M2 |
| M4 | [M4-test-corrections-audits.md](M4-test-corrections-audits.md) | Fix tautological tests, add isolation audit, ground-truth FP/FN | #75-#76, #93-#94, #96-#97 | M1, M2, M3 |
| M5 | [M5-field-test-data-integrity.md](M5-field-test-data-integrity.md) | Correct field-test report inaccuracies | #72-#74, #102-#104, #111 | M1-M4 |
| M6 | [M6-documentation-prd-corrections.md](M6-documentation-prd-corrections.md) | Missing files, unimplemented features in PRDs/guides/READMEs | #105-#110 | M5 |
| M7 | [M7-field-test-rerun.md](M7-field-test-rerun.md) | ✅ COMPLETE — Re-run field tests, flakiness sweep, produce corrected reports, articles | #112-#114, #122 (closed); #115 (article updates deferred) | M1-M6 |
| M8 | [M8-release-readiness.md](M8-release-readiness.md) | Security scan, CI verify, docs, OSS files, PyPI, GitHub tag, merge to main | #115-#121, #123-#125 | M7 |

**Total: 58+ issues · 8 milestones (M1-M8)**

```
M1 ──► M2 ──► M3 ──► M4 ──► M5 ──► M6 ──► M7 ──► M8
```

## Global exit gates (every milestone)

- Ruff clean, mypy strict clean, full test suite green
- Zero paid-LLM calls in CI (scripted reviewers only)
- Code review required before merge to `rel-0.2.0`
- All new code has tests covering the regression case

## Conventions

- Every milestone end must involve: code review, run all tests, lint strict clean, commit, push to `rel-0.2.0`
- Issue bodies carry: what/why, reproduction steps, fix description, acceptance criteria
- A task is done when its issue closes AND the global exit gates pass