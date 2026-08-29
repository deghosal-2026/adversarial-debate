# Release Notes — v0.2.2

**Date:** 2026-08-29

**What's new in AdversarialDebate v0.2.2,** a measurement infrastructure release that adds statistical rigor to every published metric. Three community-raised gaps are closed — no new LLM calls, no new debates.

---

## Quick Summary

| Metric | v0.2.2 | vs v0.2.1 |
|--------|--------|-----------|
| New LLM calls | **0** | 480 debates |
| Noise-floor CIs | **5 pairs measured** | None |
| Permutation control | **77.8 sigma above null** | Not measured |
| Shared RLHF priors | **Documented** | Implicit |
| New unit tests | **+21** (all deterministic) | +55 |
| Total cost | **$0.00** | $0.57 |

## What Changed

### Noise-Floor Baseline (M1)
- `scripts/noise_floor.py` — bootstrap resampling (10,000 resamples) of stored debate results
- Measures: convergence score, verdict rate, theater rate, capitulation rate, avg concessions
- Key findings: GPT+Mistral vs DeepSeek+Mistral gap = 1.8 sigma (real but narrow); pairs with < 30 debates have unusably wide noise floors
- Every future pair comparison must report a CI, not just a point estimate

### Permutation Control (M1)
- `scripts/permutation_control.py` — shuffles claim-to-ground-truth pairings N=500 times
- Uses deterministic Jaccard similarity (0.87s runtime, zero LLM calls)
- Result: LLM match rate (87.4%) sits 77.8 sigma above null mean (0.3%)
- The 0 NO_MATCH result is validated — vocabulary overlap does not explain it

### Shared RLHF Priors (M1)
- Design note documenting two competing causal mechanisms for the Mistral effect
- Positive: Mistral-specific training makes it a better debating partner
- Negative: non-Mistral models share RLHF priors and rubber-stamp each other
- Next experiment: RLHF-distance vs convergence correlation

### Field Test (M2)
- No new sweep — all analysis is post-hoc on existing v0.2.1 data
- All results in `results/field-test/v0.2.2/`

## Model Selection Guidance

*Unchanged from v0.2.1.* All published pair recommendations remain valid. The noise-floor baseline adds confidence intervals to the existing comparisons.

| Pair | Convergence (95% CI) | Best For | Verdict |
|------|--------------------|----------|--------|
| GPT+Mistral | 0.536 (0.498–0.575) | Production default | ✅ Recommended |
| DeepSeek+Mistral | 0.572 (0.506–0.640) | Validation | ✅ Recommended |
| DeepSeek+GPT | 0.246 (0.214–0.279) | Hypothesis testing | ❌ Not recommended |
| GPT+Gemini | 0.033 (0.016–0.052) | Negative control | ❌ Not recommended |
| GPT+GPT | 0.273 (0.129–0.432) | Homogeneous control | ❌ Not recommended |

## Documentation
- `docs/field-test/v0.2.2/FIELD_TEST_REPORT.md` — full field test results with noise-floor table, permutation control, and RLHF design note
- `docs/field-test/v0.2.2/learnings.md` — findings and causal mechanism documentation
- `docs/field-test/v0.2.2/field-test-plan.md` — experimental methodology
- `scripts/README.md` — updated with new step 8 (noise floor) and step 9 (permutation control)

## Upgrade Notes
- The noise-floor and permutation control scripts are standalone — add them to any post-debate pipeline
- No changes to existing configuration or debate results
- All existing v0.2.1 artifacts remain valid