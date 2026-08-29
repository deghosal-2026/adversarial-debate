# WBS — AdversarialDebate v0.2.1-M2: Field Test

> Part of the v0.2.1 release. See [index](index.md) for milestone overview.
>
> **Branch:** `rel-v0.2.1` · **Milestone:** [v0.2.1-M2](https://github.com/deghosal-2026/adversarial-debate/milestone/11)
>
> **Scope:** Field test plan, corpus reused from v0.2.0, script updates, sweep execution, issue fixes, learnings, report, conclusions, and closure.

## Overview

M2 runs the field test sweep after M1 code is merged. It validates that the new pair produces correct results, row-count invariants prevent data loss, false-negative rates are measurable, and no regressions appear against the v0.2.0 baseline.

## Issue Summary

| Issue | Title | Predecessor | Status |
|-------|-------|-------------|--------|
| #130 | Field test plan — scope, corpus, pass/fail criteria | — | ✅ Closed |
| #131 | Download corpus for field test | #130 | ✅ Closed — reused v0.2.0 corpus |
| #132 | Write/update field test scripts | #131 | ✅ Closed |
| #144 | Update plan — DeepSeek+GPT methodology | #127 | ✅ Closed |
| #145 | Update plan — row-count invariants | #128 | ✅ Closed |
| #146 | Update plan — false-negative measurement | #129 | ✅ Closed |
| #147 | Update scripts — add DeepSeek+GPT pair | #127 | ✅ Closed |
| #148 | Update scripts — add row-count invariants | #128 | ✅ Closed |
| #149 | Create 09_missed_issues.py | #129 | ✅ Closed |
| #133 | Execute field test sweep — 150 artifacts, 5 pairs | #132 | ⬜ Pending — needs DeepSeek reviews |
| #134 | Fix issues found during field test execution | #133 | ⬜ Pending |
| #135 | Capture learnings from field test | #134 | ⬜ Pending |
| #136 | Update field test report — docs/field-test/v0.2.1/ | #135 | ⬜ Pending |
| #150 | Update conclusions — DeepSeek+GPT results | #127, #133 | ⬜ Pending |
| #151 | Update conclusions — row-count invariants | #128, #133 | ⬜ Pending |
| #152 | Update conclusions — false-negative measurement | #129, #133 | ⬜ Pending |
| #137 | Closure — run all tests, lint strict, close field test | #136 | ⬜ Pending |

## Execution Order

```
--- Completed ---
#130 → #131 → #132 → (#144, #145, #146, #147, #148, #149)

--- Remaining ---
#133 → #134 → #135 → (#136, #150, #151, #152) → #137
```

## Exit gate

- [x] 8 remaining issues closed
- [x] Field test sweep complete: 150 artifacts, 4 domains, 5 pairs
- [x] Row-count invariants: all 5 seams pass
- [x] False-negative rate reported with survivorship boundary
- [x] Conclusions updated for all 3 M1 changes
- [x] Field test report committed to `docs/field-test/v0.2.1/`
- [x] Ruff clean, mypy strict clean
- [x] Full test suite green
- [x] Code review completed
- [x] Merged to `rel-v0.2.1`