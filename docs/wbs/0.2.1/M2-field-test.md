# WBS — AdversarialDebate v0.2.1-M2: Field Test

> Part of the v0.2.1 release. See [index](index.md) for milestone overview.
>
> **Branch:** `rel-v0.2.1` · **Milestone:** [v0.2.1-M2](https://github.com/deghosal-2026/adversarial-debate/milestone/11)
>
> **Scope:** Field test plan, corpus download, script updates, sweep execution, issue fixes, learnings, report, conclusions, and closure.

## Overview

M2 runs the full field test sweep after all M1 work is merged. It validates that the new pair produces correct results, row-count invariants prevent data loss, false-negative rates are measurable, and no regressions appear against the v0.2.0 baseline.

## Issue Summary

| Issue | Title | Predecessor |
|-------|-------|-------------|
| #130 | Field test plan — scope, corpus, pass/fail criteria | — |
| #131 | Download corpus for field test | #130 |
| #132 | Write/update field test scripts — new pair, row-count, missed-issue | #131 |
| #144 | Update plan — DeepSeek+GPT methodology and pass/fail criteria | #127 |
| #145 | Update plan — row-count invariants and pipeline integrity | #128 |
| #146 | Update plan — false-negative measurement and survivorship boundary | #129 |
| #147 | Update scripts — add DeepSeek+GPT pair | #127 |
| #148 | Update scripts — add row-count invariants | #128 |
| #149 | Create 09_missed_issues.py | #129 |
| #133 | Execute field test sweep — 150 artifacts, 4 domains, 3 pairs | #132 |
| #134 | Fix issues found during field test execution | #133 |
| #135 | Capture learnings from field test | #134 |
| #136 | Update field test report — docs/field-test/v0.2.1/ | #135 |
| #150 | Update conclusions — DeepSeek+GPT results change model selection | #127, #133 |
| #151 | Update conclusions — row-count invariants change credibility | #128, #133 |
| #152 | Update conclusions — false-negative measurement changes claims | #129, #133 |
| #137 | Closure — run all tests, lint strict, close field test | #136 |

## Execution Order

```
#130 → #131 → #132 → (#144, #145, #146, #147, #148, #149) → #133 → #134 → #135 → (#136, #150, #151, #152) → #137
```

## Exit gate

- [ ] All 17 issues closed
- [ ] Field test sweep complete: 150 artifacts, 4 domains, 5 pairs
- [ ] Row-count invariants: all 5 seams pass
- [ ] False-negative rate reported with survivorship boundary
- [ ] Conclusions updated for all 3 M1 changes
- [ ] Field test report committed to `docs/field-test/v0.2.1/`
- [ ] Ruff clean, mypy strict clean
- [ ] Full test suite green
- [ ] Code review completed
- [ ] Merged to `rel-v0.2.1`