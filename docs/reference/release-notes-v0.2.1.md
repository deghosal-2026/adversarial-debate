# Release Notes — v0.2.1

**Date:** 2026-08-28

**What's new in AdversarialDebate v0.2.1,** a measurement methodology release that confirms the Mistral effect, adds pipeline integrity invariants, and introduces false-negative measurement.

---

## Quick Summary

| Metric | v0.2.1 | vs v0.2.0 |
|--------|--------|-----------|
| Field test artifacts | 150 (same corpus) | 150 |
| Model pairs | 5 (2 new) | 3 |
| Debates | 367 | 217 |
| Ground truth MATCH | 87.4% (3,008/3,440) | 88.7% |
| Theatre rate | 0% | 0% |
| Flaky artifacts | 0 | 0 |
| Pipeline integrity | 5 seam assertions | None |
| Missed-issue rate | 1.7–3.4% | Not measured |
| Unit tests | +55 (all deterministic) | — |
| Total cost | $0.57 | $0.42 |

## What Changed

### Model Pairing (M1)
- Added `pair8_deepseek_gpt_mini` — the separating experiment that tests whether debate quality is driven by lab diversity or by Mistral specifically
- Result: Mistral effect confirmed (0.246 convergence without Mistral vs 0.536 with Mistral)
- Model selection guidance updated: "always include Mistral"

### Pipeline Integrity (M1)
- `scripts/_seam_assert.py` — shared assertion utility with fail-fast behavior
- 5 seam assertions added to `02_run_reviewer`, `03_combine_results`, `04_run_debate`, `05_analyze`, `06_ground_truth`
- All 5 passed on the first field test run — the 2,333→359 collapse class of bug is eliminated

### False-Negative Measurement (M1)
- `scripts/missed_issues.py` — importable module for recall measurement
- `scripts/09_missed_issues.py` — CLI entry point
- `scripts/scripts_common.py` — shared pipeline utilities
- First missed-issue rates: 1.7–3.4% across all reviewers (lower bound from 59 known-bad PRs)

### Field Test (M2)
- Full sweep executed across 6 parallel terminals using corpus split files
- 150 artifacts, 4 domains, 5 pairs
- 367 debates, 3,440 ground-truth rows, 0 flaky
- Pipeline integrity verified at every seam

## Model Selection Guidance

| Pair | Convergence | Best For | Verdict |
|------|------------|----------|--------|
| GPT+Mistral | 0.536 | Production default (cost-effective, zero theatre) | ✅ Recommended |
| DeepSeek+Mistral | 0.572 | Validation (higher convergence, 2.8% capitulation) | ✅ Recommended |
| DeepSeek+GPT | 0.246 | Hypothesis testing only | ❌ Not recommended |
| GPT+Gemini | 0.033 | Negative control | ❌ Not recommended |
| GPT+GPT | 0.273 | Homogeneous control | ❌ Not recommended |

## Documentation
- `docs/field-test/v0.2.1/FIELD_TEST_REPORT.md` — full field test results
- `docs/field-test/v0.2.1/findings-learnings.md` — detailed learnings
- `docs/field-test/v0.2.1/field-test-plan.md` — experimental methodology
- `docs/wbs/0.2.1/` — work breakdown structure for all 3 milestones

## Upgrade Notes
- If you have custom pipeline scripts, add seam assertions at join boundaries to prevent silent data loss
- The `missed_issues` module provides a `detect_missed_issue()` function for measuring recall
- Existing v0.2.0 configuration files remain compatible