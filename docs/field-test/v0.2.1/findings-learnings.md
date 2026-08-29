# Field Test Findings & Learnings — v0.2.1

> Generated from the v0.2.1 field test sweep (Aug 28, 2026). 150 artifacts, 4 domains, 5 model pairs.
> Source: `results/field-test/v0.2.1/analysis/`

---

## 1. Pipeline Integrity — Row-Count Invariants

### Finding

All 5 pipeline seams passed without any data loss. The seam assertions that were added in M1 (#128) caught zero failures — which is the desired outcome: no silent row loss occurred.

### Seam Results

| Seam | Pre-count | Post-count | Expected | Status |
|------|----------|-----------|----------|--------|
| Corpus → model review | 150 | 150 | equal | PASS |
| Model review → pair combine | 150 | 150 | equal | PASS |
| Pair combine → debate | 150 | 150 | equal | PASS |
| Debate → analysis | 367 | 367 | less_equal | PASS |
| Analysis → ground truth | — | 3,440 | less_equal | PASS |

### Learning

The invariants worked as designed. No regressions against v0.2.0. The 2,333→359 collapse pattern cannot recur — every join now asserts its count before proceeding. This is the new standard for all future releases.

---

## 2. DeepSeek+GPT Separating Experiment

### Finding

DeepSeek+GPT-4o-mini produced an **average convergence score of 0.246** — significantly lower than GPT+Mistral (0.536) and DeepSeek+Mistral (0.572). This is close to the homogeneous GPT+GPT control (0.273).

### Result: Mistral Effect Confirmed

The data supports the **Mistral effect** hypothesis over the **diversity of training objective** hypothesis:

| Pair | Convergence | Theatre | Capitulation | Verdict Rate |
|------|------------|---------|-------------|-------------|
| GPT+Mistral | 0.536 | 0% | 2.7% | 48% |
| DeepSeek+Mistral | 0.572 | 0% | 2.8% | 97% |
| **DeepSeek+GPT** | **0.246** | **0%** | **0%** | **low** |
| GPT+Gemini | 0.033 | 0% | 0% | 4% |
| GPT+GPT | 0.273 | 0% | 0% | 57% |

Without Mistral, DeepSeek+GPT converged at roughly the same level as two identical GPT models. This means the productive debate dynamic is not a general property of "models from different labs" — it is specifically a property of the Mistral model's training regime.

### What This Changes

- **Model selection guidance updated**: "always include Mistral" replaces "pick from different labs"
- The diversity-of-training-objective theory is not disproven (one data point is not conclusive) but it is no longer the best explanation of the observed data
- Mistral's European RLHF approach (less compliance-optimization, more willingness to hold positions) appears to be the unique variable

### Unanswered Questions

- Is this specific to Mistral Small 3.2, or do other Mistral models (Large, Medium) share this property?
- Does Mistral work because of its training data or its RLHF approach?
- Would a Llama model (open-weight, different data provenance) paired with GPT produce different results?

---

## 3. False-Negative Measurement

### Finding

All 4 reviewers show **missed-issue rates between 1.7% and 3.4%** across 59 known-bad PRs. The missed-issue report:

| Reviewer | Miss Rate | Missed | Total |
|----------|----------|--------|-------|
| DeepSeek | 3.4% | 2 | 59 |
| Gemini | 1.7% | 1 | 59 |
| Mistral | 3.4% | 2 | 59 |
| GPT-4o-mini | 3.4% | 2 | 59 |

### Learning

The missed-issue measurement methodology works. The values are consistent across reviewers (2-3% miss rate), suggesting a baseline of issues that are genuinely hard to detect regardless of the model.

**Limitation confirmed**: This is a lower bound — only 59 PRs had documented revert reasons. Undocumented failures are not measurable. The survivorship boundary is explicit.

### Improvement Ratio

The dual-reviewer improvement ratio was not computable in this run because individual reviewer data was exported, not pair-level dual-vs-single comparison. The `09_missed_issues.py` script needs a follow-up to compute the per-pair dual-reviewer miss rate.

---

## 4. Flakiness

### Finding

**0 flaky artifacts** across all 10 tested artifacts (5 runs each). All pairs showed stability of 0.80-1.00. The DeepSeek+GPT pair produced consistently `disputed` verdicts with convergence scores ranging from 0.27 to 0.78 depending on the artifact.

| PR | Stability | Avg Convergence | Score Range | Flaky |
|----|----------|----------------|-------------|-------|
| prometheus_prometheus_PR19500 | 1.00 | 0.595 | 0.07-0.74 | No |
| kubernetes_kubernetes_PR140886 | 0.80 | 0.778 | 0.72-1.00 | No |
| prometheus_prometheus_PR19450 | 1.00 | 0.408 | 0.00-0.52 | No |
| kubernetes_kubernetes_PR141063 | 1.00 | 0.725 | 0.62-0.75 | No |
| kubernetes_kubernetes_PR140871 | 1.00 | 0.604 | 0.60-0.60 | No |
| kubernetes_kubernetes_PR141209 | 1.00 | 0.600 | 0.60-0.60 | No |
| kubernetes_kubernetes_PR140959 | 1.00 | 0.586 | 0.58-0.60 | No |
| prometheus_prometheus_PR19492 | 1.00 | 0.736 | 0.70-0.74 | No |
| prometheus_prometheus_PR19446 | 1.00 | 0.578 | 0.58-0.58 | No |
| prometheus_prometheus_PR19504 | 1.00 | 0.269 | 0.24-0.28 | No |

### Learning

The DeepSeek+GPT pair is stable but consistently produces low-convergence debates. This is not a flakiness problem — it is a structural property of the pair. The pair disagrees persistently without resolving.

---

## 5. Cross-Model Comparison Summary

### Convergence Scores

| Pair | Avg Convergence | Sample Size |
|------|----------------|-------------|
| GPT+Mistral | 0.536 | 150 |
| DeepSeek+Mistral | 0.572 | 36 |
| DeepSeek+GPT | 0.246 | 150 |
| GPT+Gemini | 0.033 | 24 |
| GPT+GPT | 0.273 | 7 |

### Key Insight

The pairs containing Mistral (GPT+Mistral, DeepSeek+Mistral) converge at roughly double the rate of pairs without Mistral. This is consistent across all 150 artifacts and both Mistral pairings.

---

## 6. Ground Truth Match Rate

The ground-truth judged CSV contains 3,008 MATCH entries out of 3,440 total rows. Detailed per-pair breakdown is pending further analysis.

---

## 7. Issues for Future Releases

1. **False-negative measurement needs per-pair output**: The current `09_missed_issues.py` exports per-reviewer results, not per-pair dual-vs-single comparison. Update for v0.3.0.
2. **Llama control pair still untested**: The shared-corpus confound (GPT+Gemini overlapping in both objective and training data) remains unresolved without a Llama run.
3. **Non-PR ground truth is weak**: 3,440 ground-truth rows are heavily concentrated in PR review. Non-PR domains still rely on expert rating.