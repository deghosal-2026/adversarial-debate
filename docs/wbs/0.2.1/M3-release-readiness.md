# WBS — AdversarialDebate v0.2.1-M3: Release Readiness

> Part of the v0.2.1 release. See [index](index.md) for milestone overview.
>
> **Branch:** `rel-v0.2.1` · **Milestone:** [v0.2.1-M3](https://github.com/deghosal-2026/adversarial-debate/milestone/12)
>
> **Scope:** Final release readiness: security scan, all tests passing, docs updated, PyPI release, tags updated, close all v0.2.1 milestones.

## Overview

M3 is the final release readiness gate. All issues are strictly sequential — each depends on the previous one completing successfully.

## Issue Summary

| Issue | Title | Predecessor |
|-------|-------|-------------|
| #138 | Security scan — truffleHog, dependency audit, secret detection | — |
| #139 | All tests passing — full suite + field test confirmed green | #138 |
| #140 | Docs sweep — README, CHANGELOG, release notes, API reference | #139 |
| #141 | Packaging & PyPI release — build, dist, upload | #140 |
| #142 | Release tags and milestone closure — git tag, GitHub release, close milestones | #141 |
| #143 | Closure — final quality gate: lint strict, merge to main, tag | #142 |

## Execution Order

```
#138 → #139 → #140 → #141 → #142 → #143
```

## Exit gate

- [ ] All 6 issues closed
- [ ] Security scan clean (truffleHog, pip-audit)
- [ ] Full test suite green (existing + 55 new tests)
- [ ] Docs updated: README, CHANGELOG, release notes, API reference
- [ ] PyPI published: `pip install adversarial-debate==0.2.1`
- [ ] Git tag v0.2.1 created and pushed
- [ ] GitHub release published with release notes
- [ ] All v0.2.1 milestones closed (M1, M2, M3)
- [ ] `rel-v0.2.1` merged to `main`
- [ ] Ruff clean, mypy strict clean
- [ ] Code review completed