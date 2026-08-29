# Field Test Plan — v0.2.1 "Separate the Signal"

> **Status:** Planned · **Version:** 0.2.1 · **Window:** Sep 1-30, 2026
> **Owner:** Deb Ghosal
>
> This plan builds on v0.2.0's mixed-domain foundation and adds three structural improvements driven by community feedback: a model pairing separating experiment, row-count pipeline invariants, and false-negative measurement.

## 1. Objective

| # | Question | How answered |
|---|----------|-------------|
| Q1 | **Is debate quality driven by diversity of training objective or by the Mistral model specifically?** | Run DeepSeek+GPT-4o-mini on full corpus — two labs, no Mistral. Compare against existing pairs. |
| Q2 | **Can silent data loss at pipeline seams be prevented?** | Row-count invariant assertions at all 5 pipeline seams. Pipeline fails fast on unexpected row loss. |
| Q3 | **What is the missed-issue rate (recall) for each pair?** | Feed pre-fix artifacts from 70 known-bad PRs through both reviewers. Measure single vs dual miss rates. |
| Q4 | **Do no regressions appear against the v0.2.0 baseline?** | Compare all metrics against published v0.2.0 results. |

## 2. What Changed From v0.2.0

| Dimension | v0.2.0 | v0.2.1 | Why |
|-----------|--------|--------|-----|
| **Model pairs** | 3 pairs (GPT+Mistral, DeepSeek+Mistral, GPT+Gemini) | 5 pairs (+ DeepSeek+GPT, optional Llama+GPT) | Separating experiment for diversity hypothesis (#127) |
| **Pipeline integrity** | Silent row loss at joins (2,333→359 collapse) | 5 seam assertions with fail-fast | Prevent hidden data loss (#128) |
| **Evaluation** | Binary match rate only (precision) | + Missed-issue rate (recall) | Measure what the system misses (#129) |
| **Corpus** | 150 artifacts, 4 domains | 150 artifacts, 4 domains (unchanged) | Regression-only — no new domains |
| **Cost** | $0.42 for 360 runs | ~$0.56 for 480 runs (+1 pair) | One extra LLM pair |

## 3. Pass/Fail Philosophy

Same as v0.2.0: **invariant-based assertions**, not golden-plan matching. LLM output is non-deterministic.

**What is tested:**
- All 5 seam assertions pass (pipeline integrity)
- DeepSeek+GPT convergence score reported (falsifiable hypothesis test)
- Missed-issue rate measured with survivorship boundary
- No regressions against v0.2.0 baseline metrics

**What is NOT tested:**
- Exact claim text matching (LLM variance)
- New domains (deferred to v0.3.0)
- UI/CLI surfaces (deferred to v1.0.0)

## 4. Measurements

### 4.1 Pipeline Integrity

| Seam | Scripts | Invariant | Expected |
|------|--------|-----------|----------|
| Corpus → model review | `02_run_reviewer.py` | `count_post <= count_pre` | Equal for full corpus |
| Model review → pair combine | `03_combine_results.py` | `count_post <= count_pre` | Equal per pair |
| Pair combine → debate | `04_run_debate.py` | `count_post <= count_pre` | Equal |
| Debate → analysis | `05_analyze.py` | `count_post <= count_pre` | Zero-claim exclusions logged |
| Analysis → ground truth | `06_ground_truth.py` | `count_post <= count_pre` | Non-substantive filters logged |

### 4.2 Model Pair Comparison

| Metric | GPT+Mistral | DeepSeek+Mistral | DeepSeek+GPT | GPT+Gemini | GPT+GPT |
|--------|------------|-----------------|-------------|-----------|---------|
| Convergence score | | | | | |
| Verdict rate | | | | | |
| Theater rate | | | | | |
| Capitulation rate | | | | | |
| Binary match rate | | | | | |
| Missed-issue rate | | | | | |
| Improvement ratio | | | | | |

### 4.3 False-Negative Measurement

- **Source:** 70 PRs with documented revert reasons
- **Method:** Feed pre-fix artifacts through both reviewers
- **Metrics:** Single-reviewer miss rate (A), single-reviewer miss rate (B), dual-reviewer miss rate, improvement ratio
- **Boundary:** "lower bound — 70 documented failures measured. Undocumented failures are not measurable."

## 5. Execution Order

1. Run `02_run_reviewer.py` for DeepSeek on full corpus (if not already cached)
2. Run `03_combine_results.py` — includes pair8_deepseek_gpt_mini
3. Run `04_run_debate.py` — debates for new pair
4. Run `05_analyze.py` — includes all 5 pairs, seam assertions
5. Run `06_ground_truth.py` — includes seam assertions
6. Run `07_llm_judge.py` — ground-truth judging
7. Run `09_missed_issues.py` — false-negative measurement
8. Run `08_flakiness.py` — flakiness sweep on representative artifacts

## 6. Deliverables

- `docs/field-test/v0.2.1/FIELD_TEST_REPORT.md` — full results
- `docs/field-test/v0.2.1/learnings.md` — lessons learned
- Updated article vault files with new conclusions
- All results in `results/field-test/v0.2.1/`