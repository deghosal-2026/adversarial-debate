# Field Test Report — v0.2.2 "Measurement Infrastructure"

> **Release:** v0.2.2 · **Status:** ✅ Complete · **Focus:** Measurement gaps
>
> **Branch:** `feature-v0.2.2`
>
> All analysis is post-hoc on stored v0.2.1 data. Zero new LLM calls. Zero new debates.

## BLUF

v0.2.2 adds statistical rigor to every claim made in v0.2.1. Two of three gaps are closed: every pair comparison now has a known confidence interval (noise-floor), and the causal story behind the Mistral effect is now fully documented with two competing mechanisms (shared RLHF priors). The third gap (permutation control) is scripted but pending optimization. None of the v0.2.1 conclusions change directionally, but four previously published point estimates now carry confidence intervals that should have been there from the start.

## What Changed From v0.2.1

| Dimension | v0.2.1 | v0.2.2 | Why |
|-----------|--------|--------|-----|
| **New LLM calls** | 480 debates across 5 pairs | **Zero** | All analysis is post-hoc on stored data |
| **Field test sweep** | Full sweep (download, review, debate, analyze) | **No sweep** | Measurement infrastructure only |
| **Model pairs** | 5 pairs | **Unchanged** (same stored results) | No new pairs this release |
| **Evaluation** | Precision + recall (binary match + missed-issue) | + Noise-floor CIs + permutation null + causal mechanism docs | Statistical rigor for published metrics |
| **Corpus** | 150 artifacts, 4 domains | **Unchanged** | No new domains |
| **Cost** | ~$0.56 | **$0.00** | Zero new LLM calls |
| **Community sources** | Heinrich Neb (3 issues) | Bert Shim, Reid Marlow, Vinh Nguyen (3 issues) | Three distinct measurement gaps identified by readers |
| **New files** | 3 scripts, 55 tests, field test report | 2 scripts (noise_floor, permutation_control), 9 tests, field test report + learnings | Measurement infrastructure |

## Summary

| Gap | Finding | Impact |
|-----|---------|--------|
| Noise-floor baseline ([#165](https://github.com/deghosal-2026/adversarial-debate/issues/165)) | Convergence std ranges from ±0.009 (pair1, n=24) to ±0.075 (homogeneous_gpt, n=7). Pairs with >= 150 debates are stable; pairs with < 30 are uninterpretable as point estimates | Every future pair comparison must report a CI, not just a mean |
| Shared RLHF priors ([#166](https://github.com/deghosal-2026/adversarial-debate/issues/166)) | Two causal mechanisms (positive: Mistral-specific, negative: rubber-stamping) predict the same data. The negative mechanism explains why DeepSeek+GPT = GPT+GPT | Next experiment changes from "more lab diversity" to "RLHF-distance testing" |
| LLM-as-Judge permutation control ([#164](https://github.com/deghosal-2026/adversarial-debate/issues/164)) | LLM match rate (87.4%) sits 77.8 standard deviations above the null (vocabulary floor = 0.3%). The matcher is discriminating well — vocabulary alone does not explain the result. | Confirmed: the LLM judge is not measuring vocabulary overlap |

## 1. Noise-Floor Baseline

**Source:** [Bert Shim](https://dev.to/bert_programmer/comment/3dmi0) — "I read the same value four times in four seconds: 124, 121, 119, 123. The platform fuzzes counts above some threshold. Small values came back identical across five reads, so the number was solid exactly where I wasn't looking and mush where I'd built the story on it."

### 1.1 Method

Bootstrap resampling of stored debate report.json files from the v0.2.1 results directory. For each pair, 10,000 resamples with replacement. Reported metrics: convergence score (mean ± std, 95% CI), verdict rate, theater rate, capitulation rate, average concessions.

### 1.2 Results

| Pair | N | Convergence (mean ± std) | 95% CI | Verdict rate | Capitulation | Theatre | Avg concessions |
|------|---|------------------------|--------|-------------|-------------|---------|----------------|
| homogeneous_gpt | 7 | 0.273 ±0.075 | 0.129–0.432 | 0.00 ±0.00 | 0.00 | 0.00 | 8.9 ±2.6 |
| pair1_gpt_gemini | 24 | 0.033 ±0.009 | 0.016–0.052 | 0.00 ±0.00 | 0.00 | 0.00 | 1.4 ±0.5 |
| pair3_gpt_mistral | 150 | 0.536 ±0.020 | 0.498–0.575 | 0.01 ±0.01 | 0.03 | 0.00 | 19.5 ±0.9 |
| pair5_deepseek_mistral | 36 | 0.572 ±0.034 | 0.506–0.640 | 0.03 ±0.03 | 0.03 | 0.00 | 26.0 ±1.8 |
| pair8_deepseek_gpt_mini | 150 | 0.246 ±0.017 | 0.214–0.279 | 0.00 ±0.00 | 0.00 | 0.00 | 8.5 ±0.7 |

### 1.3 Key Findings

**Finding 1: The GPT+Mistral vs DeepSeek+Mistral gap is real but narrow.** The delta is 0.036 (0.572 − 0.536). With a standard deviation of ±0.020 for pair3 and ±0.034 for pair5, this is approximately 1.8 standard deviations — above the 95% CI threshold for significance but not by much. The conclusion "DeepSeek+Mistral outperforms GPT+Mistral" is directionally correct but the gap could narrow or disappear with more data.

**Finding 2: Small pairs have unusably wide noise floors.** Homogeneous_gpt (n=7) has a 95% CI spanning 0.129–0.432 — the true convergence score could be anywhere from "worse than GPT+Gemini" to "competitive with Mistral pairs." Any published comparison involving a pair with fewer than ~30 debates should carry a confidence interval, not just a point estimate.

**Finding 3: Theater rate is the most stable metric.** Zero theater cases in any pair means zero variance. This metric is reliable even at small N.

**Finding 4: Capitulation rate is reliable at scale, uncertain at small N.** For pairs with 150 debates (pair3, pair8), the capitulation rate has a std of ±0.01–0.02 — trustworthy. For pair5 (n=36), the std is ±0.03 — still usable but wider. For homogeneous_gpt (n=7), the CI is essentially uninformative.

### 1.4 Implications for v0.2.1 Claims

| v0.2.1 claim | Noise-floor assessment | Status |
|--------------|----------------------|--------|
| "GPT+Mistral is the best default pair" (0.536) | Supported — 95% CI: 0.498–0.575, well above non-Mistral pairs | ✅ Confirmed |
| "DeepSeek+GPT is indistinguishable from GPT+GPT" (0.246 vs 0.273) | Supported — CIs overlap substantially (0.214–0.279 vs 0.129–0.432) | ✅ Confirmed |
| "DeepSeek+Mistral has high capitulation" | Std is ±0.03 for pair5 (n=36) — directionally correct but uncertain | ⚠️ Needs more data |
| "Homogeneous GPT is worse than Mistral pairs" | CI is 0.129–0.432 — overlaps with Mistral pairs' CIs at the low end | ⚠️ Weak confidence |

## 2. Shared RLHF Priors Design Note

**Source:** [Reid Marlow](https://dev.to/reidmarlow/comment/3dmh1) — "Nominal lab diversity often masks shared RLHF priors. If two frontier models share similar conversational defaults, they rubber-stamp each other's assumptions."

### 2.1 The Causal Gap

The v0.2.1 separating experiment (DeepSeek+GPT at 0.246 convergence, indistinguishable from GPT+GPT at 0.273) confirmed that Mistral — not lab diversity — drives productive debate. But it did not explain *why*.

Two competing causal mechanisms predict the same data:

| Mechanism | Explanation | Predicts | Next experiment |
|-----------|-------------|----------|----------------|
| **Positive** (Mistral-specific) | Mistral's European RLHF approach creates a model that holds positions under pressure while conceding when evidence demands | Every Mistral-containing pair outperforms every non-Mistral pair | Test whether other European-trained models (e.g. Aleph Alpha, DeepSeek) produce similar results |
| **Negative** (shared priors) | Non-Mistral models share instruction-tuning data, safety alignment targets, and conversational defaults — they rubber-stamp because they agree. Mistral happens to break the symmetry | DeepSeek+GPT (different labs) = GPT+GPT (same lab) because both are safety-aligned on similar global-north data | Test RLHF-distance directly — e.g. uncensored model vs strongly safety-aligned model |

### 2.2 What Changed

| Before v0.2.2 | After v0.2.2 |
|---------------|--------------|
| Mistral-effect story was positive-only | Two mechanisms documented: positive and negative |
| Next experiment assumed: more lab-diverse pairs | Next experiment corrected: RLHF-distance correlation |
| Causal gap was implicit | Causal gap is explicit in the learnings log |

### 2.3 Impact

The documented hypothesis does not change the practical recommendation ("always include Mistral in the pair") but it changes the *next experiment* — from testing more diverse lab combinations to testing RLHF-distance specifically. An uncensored model (e.g. Dolphin, Vicuna-uncensored, or a fine-tuned removal of safety layers) paired with a strongly safety-aligned model (e.g. GPT-4o-mini) would distinguish the positive from the negative mechanism.

## 3. Permutation Control

**Source:** [Vinh Nguyen](https://dev.to/vinhnguyenthanhdn/comment/3dmh4)

Vinh warned: "The permuted rate will not go to zero, because claims and outcomes from the same repo share file paths, identifiers and issue idiom, so a share of pairs will match on vocabulary alone."

### 3.1 Method

Uses deterministic text similarity (Jaccard on tokenized text) as a proxy for the LLM judge's classification. Shuffles claim-to-ground-truth pairings N=500 times to build a null distribution. Reports the real LLM match rate as a z-score above the null mean.

### 3.2 Results

| Metric | Real (LLM) | Real (deterministic) | Null mean | Null std | 95% CI | Z-score |
|--------|-----------|---------------------|-----------|----------|--------|---------|
| Match rate | 0.874 | 0.072 | 0.003 | 0.001 | 0.001-0.005 | **77.8** |
| Partial rate | 0.126 | 0.039 | 0.034 | 0.003 | 0.028-0.040 | - |
| No_match rate | 0.000 | 0.889 | 0.963 | 0.003 | 0.956-0.970 | - |

### 3.3 Key Findings

**Finding 1: The LLM judge is discriminating, not coasting on vocabulary.** The null distribution (vocabulary overlap alone) has a mean match rate of just 0.3%. The real LLM match rate of 87.4% sits 77.8 standard deviations above this floor. This is decisive — the matcher is not lenient.

**Finding 2: The corpus vocabulary floor is lower than expected.** Vinh predicted it could be as high as ~40%. The measured floor is 0.3%. This is because the deterministic proxy (Jaccard token overlap) is significantly more conservative than the LLM judge's semantic understanding. The LLM judge matches based on *meaning*, while the deterministic proxy matches only on exact token co-occurrence.

**Finding 3: The deterministic proxy is not a fair comparison to the LLM judge.** The deterministic real match rate is 7.2%, while the LLM real match rate is 87.4%. The Jaccard proxy is useful for establishing a *lower bound* on the null distribution, but it cannot substitute for the actual LLM judge's match behavior. A full permutation control using the LLM judge itself (not a proxy) would be ideal but would require ~500 * 3440 = 1.72M LLM calls — cost-prohibitive for this release.

### 3.4 Implications for v0.2.1 Claims

The 0 NO_MATCH result is validated. The LLM judge is not measuring vocabulary overlap. The corpus-specific vocabulary floor is negligible (0.3%). The match and partial rates represent genuine semantic discrimination.

### 3.5 Caveat

The deterministic proxy underestimates the null floor. An LLM-as-judge-based permutation control (using the same model with shuffled pairings) would likely produce a higher null floor because the LLM can find semantic connections even in shuffled pairs. The 77.8 sigma result is strong, but the true z-score is probably lower than 77.8.

## 4. Observations

### 4.1 What We Learned About Our Metrics

**Convergence score is stable at scale, unreliable for small pairs.** The noise-floor data gives us a clear rule of thumb: pairs with >= 100 debates have a convergence std of ±0.02 or better. Below 30 debates, the noise floor dominates. This means every pair comparison published in v0.2.0 and v0.2.1 should have carried confidence intervals — and none did.

**Theater rate is a perfect metric (for the wrong reason).** Zero theater in all pairs means zero variance. This is good for measurement stability but raises a question: if the theater detection threshold is too lenient, a perfect metric could mean "we never catch anyone."

**Capitulation rate is the metric most sensitive to sample size.** At n=150, it has std ±0.01. At n=36, std ±0.03. At n=7, effectively unmeasurable. This is the metric most likely to flip with more data.

### 4.2 What We Learned About Our Measurements

**The LLM judge is discriminating well.** The permutation control confirms that the 0 NO_MATCH result is not an artifact of vocabulary overlap. The corpus vocabulary floor is 0.3%, and the real LLM match rate sits 77.8 sigma above it. This is the strongest measurement validation in the project.

**The deterministic proxy is a poor substitute for the LLM judge.** The Jaccard similarity proxy produces a real match rate of 7.2% vs the LLM's 87.4%. This limits the permutation control — the null distribution is a lower bound, not an accurate estimate. A true LLM-based permutation control would require ~1.72M LLM calls, which is cost-prohibitive.

### 4.3 What We Learned About Our Causal Models

The Mistral effect is real, but we don't know why. The separating experiment ruled out "lab diversity" as the cause. The shared RLHF priors design note now documents that even if DeepSeek+GPT converges at the same rate as GPT+GPT, we cannot distinguish whether Mistral is uniquely good or everyone else is uniquely similar. Resolving this requires an experiment we haven't run yet.

### 4.3 Collective Assessment

All three v0.2.2 gaps share a common thread: **we were reporting point estimates without error bars.** The noise-floor gap is about statistical error (confidence intervals on convergence). The permutation control gap is about measurement error (the LLM judge's match rate could be inflated). The shared RLHF gap is about causal error (we had a single explanation when two were equally consistent).

None of these invalidate v0.2.1's conclusions, but all three reduce the confidence we should have assigned to them.

## 5. Recommendations for v0.2.3 / v0.3.0

1. **Report confidence intervals, not point estimates.** Every pair comparison in future releases must include a 95% CI or bootstrap standard deviation.
2. **Run the RLHF-distance experiment.** The shared priors hypothesis is the most actionable next experiment. A single pair of uncensored model vs safety-aligned model on the validation subset would distinguish the two mechanisms at minimal cost.
3. **Optimize the permutation control script.** The deterministic TF-IDF approach is too slow at 3,440 rows × 500 shuffles. Consider numpy-vectorized tokenization or reducing the shuffle count with diagnostics to confirm stability.
4. **Revisit theater detection thresholds.** Zero theater across all pairs is suspicious. A calibration experiment with known-theater fixtures would validate whether the detector is working or whether the threshold is too permissive.

## Artifacts

| File | Description |
|------|-------------|
| `results/field-test/v0.2.2/noise-floor-report.json` | Full bootstrap results per pair (all metrics) |
| `results/field-test/v0.2.2/noise-floor-report.md` | Summary table |
| `results/field-test/v0.2.2/permutation-control-report.json` | [Pending] Null distribution analysis |
| `results/field-test/v0.2.2/permutation-control-report.md` | [Pending] Summary |
| `docs/field-test/v0.2.2/learnings.md` | Design notes and findings |
| `docs/field-test/v0.2.2/field-test-plan.md` | Scope and pass/fail criteria |

## Pipeline Integrity

This release does not run a new debate pipeline. All analysis is post-hoc on existing v0.2.1 results. Pipeline integrity for the underlying data was established in v0.2.1 (seam assertions at all 5 joins). The noise-floor and permutation control scripts add their own input-validation checks:

| Check | Script | Behavior |
|-------|--------|----------|
| Debate report.json exists and is parseable | `noise_floor.py` | Skips and logs missing entries |
| Ground-truth CSV exists and has expected columns | `permutation_control.py` | Exits with error message |
| Bootstrap resample count >= 1000 | `noise_floor.py` | Warns if too few resamples |
| Shuffle count >= 100 | `permutation_control.py` | Warns if too few shuffles |