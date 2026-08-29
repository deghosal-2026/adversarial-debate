# WBS — AdversarialDebate v0.2.2-M2: Release Readiness ⬜ Pending

> Part of the v0.2.2 release. See [index](index.md) for milestone overview.
>
> **Branch:** `feature-v0.2.2` · **Milestone:** [v0.2.2-M2](https://github.com/deghosal-2026/adversarial-debate/milestone/16)
>
> **Status:** ⬜ Pending — blocked until M1 is merged
>
> **Scope:** Standard release readiness activities. No field test sweep needed — all M1 changes are measurement infrastructure on existing data.

## #167 — All Tests Passing

**Acceptance criteria:**
- [ ] Full deterministic test suite green
- [ ] No regression from v0.2.1 baseline
- [ ] Ruff clean, mypy strict clean

## #168 — Docs Sweep

**Acceptance criteria:**
- [ ] CHANGELOG updated with v0.2.2 entries
- [ ] Release notes v0.2.2 written
- [ ] README updated if needed
- [ ] API reference updated if needed
- [ ] WBS status updated to reflect completion

## #169 — Security Scan

**Acceptance criteria:**
- [ ] truffleHog scan clean
- [ ] pip-audit clean
- [ ] Dependency versions current

## #170 — Packaging & PyPI Release

**Acceptance criteria:**
- [ ] `python -m build` succeeds
- [ ] Dockerfile pinned to v0.2.2
- [ ] `twine upload` to PyPI
- [ ] `pip install adversarial-debate==0.2.2` verified

## #171 — Release Tags and Milestone Closure

**Acceptance criteria:**
- [ ] Git tag v0.2.2 created and pushed
- [ ] GitHub release published with release notes
- [ ] All v0.2.2 milestones closed (M1, M2, M3)

## #172 — Final Quality Gate

**Acceptance criteria:**
- [ ] Code review completed
- [ ] Ruff clean, mypy strict clean
- [ ] Full test suite green
- [ ] Merged to `main`
- [ ] `feature-v0.2.2` branch deleted after merge

## Issue Summary

| Issue | Title | Predecessor | Status |
|-------|-------|-------------|--------|
| #167 | All tests passing — full suite confirmed green | M1 | ⬜ Open |
| #168 | Docs sweep — README, CHANGELOG, release notes, API reference | #167 | ⬜ Open |
| #169 | Security scan — truffleHog, dependency audit, secret detection | #167 | ⬜ Open |
| #170 | Packaging & PyPI release — build, dist, upload | #168, #169 | ⬜ Open |
| #171 | Release tags and milestone closure | #170 | ⬜ Open |
| #172 | Closure — final quality gate: lint strict, merge to main, tag | #170 | ⬜ Open |

## Exit gate

- [ ] All 6 issues closed
- [ ] Full test suite green
- [ ] PyPI published: `pip install adversarial-debate==0.2.2`
- [ ] Git tag v0.2.2 created and pushed
- [ ] GitHub release published
- [ ] All v0.2.2 milestones closed
- [ ] `feature-v0.2.2` merged to `main`
- [ ] Ruff clean, mypy strict clean
- [ ] Code review completed