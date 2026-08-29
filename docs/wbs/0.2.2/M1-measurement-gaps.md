# WBS — AdversarialDebate v0.2.2-M1: Measurement Gaps ✅ COMPLETE

> Part of the v0.2.2 release. See [index](index.md) for milestone overview.
>
> **Branch:** `feature-v0.2.2` · **Milestone:** [v0.2.2-M1](https://github.com/deghosal-2026/adversarial-debate/milestone/15)
>
> **Status:** ✅ COMPLETE — all 3 issues closed, 21 tests passing, committed to `feature-v0.2.2`.
>
> **Scope:** Three community-raised measurement gaps. All changes are post-hoc analysis on existing artifacts — no new debates, no field test sweep.

## Overview

M1 addresses three gaps identified by readers after the v0.2.1 release. None require new LLM calls or new debate runs — each is a measurement or documentation change on existing data.

## #164 — LLM-as-Judge Permutation Control ✅

**Source:** Vinh Nguyen ([dev.to comment](https://dev.to/vinhnguyenthanhdn/comment/3dmh4))

**Problem:** 0 NO_MATCH across 7,612 claims in v0.1.0 and 3,440 claims in v0.2.1 is suspicious. A matcher that never fires its negative verdict may be measuring its own leniency rather than the debates' accuracy. The null is not zero — claims from the same repo share vocabulary (file paths, identifiers, issue idioms), so the permuted rate has a corpus-specific floor.

**Changes:**
- Created standalone `scripts/permutation_control.py` (not a flag on 07_llm_judge.py — separate script for clarity)
- Pre-computes token sets for performance: 0.87s for 500 shuffles
- Shuffles claim-to-ground-truth pairings: for each claim, assigns a known_reason from a different row
- Runs N=500 shuffles for stable null distribution
- Reports null mean ± std, 95% CI, z-score of real rate above null
- Result: LLM match rate (87.4%) sits 77.8 sigma above null floor (0.3%)
- 12 unit tests (tokenization, Jaccard, simulate_judge, script loads)
- Results in field test report and learnings

**Acceptance criteria:**
- [x] Permutation control script created (`scripts/permutation_control.py`)
- [x] N=500 shuffles for stable null distribution (0.87s runtime)
- [x] Null distribution (mean, std, CI) reported alongside real match rate
- [x] Real match rate reported as z-score (77.8 sigma above null)
- [x] Documentation: "null floor is 0.3%, not ~40% as hypothesized"
- [x] Existing ground-truth CSV format unchanged
- [x] 12 unit tests passing

## #165 — Metric Noise-Floor Baseline ✅

**Source:** Bert Shim ([dev.to comment](https://dev.to/bert_programmer/comment/3dmi0))

**Problem:** No core metric has ever been measured for baseline variance under identical conditions. A shift from 0.536 to 0.572 could be signal or instrument noise. Bert's story — "I read the same value four times in four seconds: 124, 121, 119, 123" — is the exact failure class.

**Changes:**
- Created `scripts/noise_floor.py` — bootstrap resampling of stored debate results
- Reports all 5 metrics: convergence score, verdict rate, theater rate, capitulation rate, avg concessions
- Mean, std, and 95% CI per metric per pair
- Output JSON + markdown summary
- 9 unit tests

**Results:**
- GPT+Mistral vs DeepSeek+Mistral gap = 1.8 sigma — real but narrow
- Pairs with < 30 debates have unusably wide noise floors
- Theater rate has zero variance (stable metric)
- Capitulation rate reliable at n=150, uncertain at n=36

**Acceptance criteria:**
- [x] Noise-floor measurement script created
- [x] All 5 pairs measured with 10,000 bootstrap resamples each
- [x] Per-metric table: mean, std, 95% CI under identical conditions
- [x] Baseline run artifacts committed to repo
- [x] Zero LLM calls (uses existing stored results)
- [x] 9 unit tests passing

## #166 — Shared RLHF Priors Design Note ✅

**Source:** Reid Marlow ([dev.to comment](https://dev.to/reidmarlow/comment/3dmh1))

**Problem:** The Mistral effect is confirmed empirically, but the causal mechanism is underspecified. Two competing stories: (a) Mistral is positively good at debate, or (b) non-Mistral models share RLHF priors and rubber-stamp each other. The negative mechanism — "nominal lab diversity can mask shared conversational defaults" — has never been formally captured.

**Changes:**
- Added design note to `docs/field-test/v0.2.2/learnings.md`
- Documents both positive (Mistral-specific) and negative (shared priors) mechanisms
- Recommends RLHF-distance experiment for next release
- Cross-references in FIELD_TEST_REPORT.md section 2

**Acceptance criteria:**
- [x] Design note added to learnings log
- [x] Causal mechanism explicitly distinguished from positive Mistral-effect story
- [x] Next experiment suggestion: RLHF-distance vs convergence

## Issue Summary

| Issue | Title | Type | Status |
|-------|-------|------|--------|
| #164 | [v0.2.2-M1] LLM-as-Judge Permutation Control | Code change + analysis | ✅ Closed |
| #165 | [v0.2.2-M1] Metric noise-floor baseline | Code change + analysis | ✅ Closed |
| #166 | [v0.2.2-M1] Design note: shared RLHF priors | Documentation | ✅ Closed |

## Exit gate

- [x] All 3 issues closed
- [x] All changes use existing stored data — zero new LLM calls
- [x] Ruff clean (pre-existing exceptions only), format clean
- [x] 21 new tests passing (12 permutation + 9 noise floor)
- [x] Full existing test suite green
- [x] Code review completed
- [x] Merged to `feature-v0.2.2`