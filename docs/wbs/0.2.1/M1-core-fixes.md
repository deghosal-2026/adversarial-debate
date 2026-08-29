# WBS — AdversarialDebate v0.2.1-M1: Core Fixes ✅ COMPLETE

> Part of the v0.2.1 release. See [index](index.md) for milestone overview.
>
> **Branch:** `rel-v0.2.1` · **Milestone:** [v0.2.1-M1](https://github.com/deghosal-2026/adversarial-debate/milestone/10)
>
> **Status:** ✅ COMPLETE — all 6 issues closed, 55 tests passing, committed to `rel-v0.2.1`.
>
> **Scope:** DeepSeek+GPT pairing experiment, row-count invariant assertions, false-negative measurement, and all associated unit tests. No LLM calls in any test.

## Overview

M1 addresses the three community-raised issues from the v0.2.0 release. Each issue has a code change component and a unit test component. All tests are deterministic — zero LLM calls.

## #127 — Model Pairing Separating Experiment

**Problem:** Every productive pair in v0.2.0 contains Mistral. The data is equally consistent with "diversity of training objective" and "Mistral is the one that won't fold." The separating experiment is DeepSeek + GPT-4o-mini — two different labs, no Mistral.

**Changes:**
- Add `pair8_deepseek_gpt_mini` to `scripts/03_combine_results.py` PAIRS dict
- Optional: add `pair9_llama_gpt` for shared-corpus confound separation
- Ensure all 5 pipeline scripts handle the new pair
- Update provider config if needed

**Unit tests (#153):**
- `test_pairs.py` — 6 tests: pair configured, correct models, distinct, not Mistral, no duplicate, Llama optional
- `test_pair_model_slugs.py` — 4 tests: deepseek resolves, gpt resolves, llama resolves if configured, no duplicate slugs
- `test_pair_assignment.py` — 3 tests: full corpus uses pair8, validation uses pair9 or fallback, every corpus has a pair
- `test_analysis_pair_inclusion.py` — 2 tests: analyze includes all pairs, ground truth includes all pairs

## #128 — Row-Count Invariant Assertion

**Problem:** The 2,333→359 row collapse in v0.2.0 happened because joins silently dropped rows without any assertion. The fix generalizes to every seam.

**Changes:**
- Create `scripts/_seam_assert.py` with shared `assert_seam()` function
- Add seam assertions to `02_run_reviewer.py`, `03_combine_results.py`, `04_run_debate.py`, `05_analyze.py`, `06_ground_truth.py`
- Switch skip tracking from silent counts to explicit ID lists
- Add `--strict` flag for expected exclusion warnings

**Unit tests (#154):**
- `test_seam_assert.py` — 12 tests: equal pass/fail, less_equal pass/fail, skip IDs, strict mode, zero/negative counts, large counts
- `test_script_seam_integration.py` — 5 tests: one per script, verifying assert_seam is called correctly
- `test_skip_tracking.py` — 2 tests: skip IDs logged, skip count accurate

## #129 — False-Negative Measurement

**Problem:** v0.2.0 only measures binary match rate (precision). No recall measurement. False negatives were invisible.

**Changes:**
- Create `scripts/09_missed_issues.py` — full implementation
- Collect pre-fix artifacts for 70 known-bad PRs
- Output: missed-issue-report.csv and console summary

**Unit tests (#155):**
- `test_missed_issue_detection.py` — 8 tests: detected, missed, empty claims, multiple claims, case insensitive, partial match, stop words, short claims
- `test_missed_issue_rate_computation.py` — 7 tests: 100%, 0%, partial, dual vs single, improvement ratio, per-domain, empty results
- `test_survivorship_boundary.py` — 3 tests: includes "lower bound", includes failure count, does not overclaim
- `test_missed_issue_csv_output.py` — 3 tests: expected columns, one row per pair, percentage format

## Issue Summary

| Issue | Title | Type | Tests | Status |
|-------|-------|------|-------|--------|
| #127 | Model Pairing Separating Experiment | Code change | 15 | ✅ Closed |
| #128 | Row-Count Invariant Assertion | Code change | 19 | ✅ Closed |
| #129 | False-Negative Measurement | Code change | 21 | ✅ Closed |
| #153 | Unit tests — pair config | Test | — | ✅ Closed |
| #154 | Unit tests — seam assertion | Test | — | ✅ Closed |
| #155 | Unit tests — false-negative | Test | — | ✅ Closed |

## Exit gate

- [x] All 6 issues closed
- [x] 55 new tests pass with zero LLM calls
- [x] Ruff clean, mypy strict clean
- [x] Full existing test suite green
- [x] Code review completed
- [x] Merged to `rel-v0.2.1`