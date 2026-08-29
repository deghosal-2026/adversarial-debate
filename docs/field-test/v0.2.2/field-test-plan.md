# Field Test Plan — v0.2.2 "Measurement Infrastructure"

> **Status:** ✅ Complete · **Version:** 0.2.2 · **Window:** Aug 29-Sep 5, 2026
> **Owner:** Deb Ghosal
>
> This plan does NOT run a new debate sweep. It adds measurement infrastructure on top of existing v0.2.1 results — three measurement gaps identified by community readers after the v0.2.1 release. All analysis is post-hoc on stored data; zero new LLM calls.

## 1. Objective

| # | Question | How answered |
|---|----------|-------------|
| Q1 | **Is the LLM judge's near-100% match rate measuring discrimination or vocabulary overlap?** | Shuffle claim-to-ground-truth pairings N>=500 times. Measure null distribution of match rate using deterministic text similarity. Report z-score of real rate above null. |
| Q2 | **What is the statistical noise floor of each core metric?** | Bootstrap-resample stored debate results (10,000 resamples per pair). Report mean, std, 95% CI for convergence score, verdict rate, capitulation rate, theater rate, avg concessions. |
| Q3 | **Is the Mistral effect driven by Mistral's positive traits or by non-Mistral rubber-stamping?** | Document competing causal mechanisms. Recommend RLHF-distance experiment for next release. |

## 2. What Changed From v0.2.1

| Dimension | v0.2.1 | v0.2.2 | Why |
|-----------|--------|--------|-----|
| **New LLM calls** | 480 debates across 5 pairs | **Zero** | All analysis is post-hoc on stored data |
| **Field test sweep** | Full sweep (download, review, debate, analyze) | **No sweep** | Measurement infrastructure only |
| **Model pairs** | 5 pairs | **Unchanged** (same stored results) | No new pairs this release |
| **Evaluation** | Precision + recall (binary match + missed-issue) | + Noise-floor CIs + permutation null | Statistical rigor for published metrics |
| **Corpus** | 150 artifacts, 4 domains | **Unchanged** | No new domains |
| **Cost** | ~$0.56 | **$0.00** | Zero new LLM calls |

## 3. LLM-as-Judge Permutation Control

### 3.1 The Problem

Across v0.1.0 (7,612 claims) and v0.2.1 (3,440 claims), the LLM-as-judge returned **0 NO_MATCH**. A matcher that never fires its negative verdict on a corpus that size may be measuring its own leniency rather than the debates' accuracy.

Source: Vinh Nguyen — "The permuted rate will not go to zero, because claims and outcomes from the same repo share file paths, identifiers and issue idiom."

### 3.2 Methodology

- Use deterministic text similarity (token Jaccard) as a proxy for the LLM judge
- Shuffle claim-to-ground-truth pairings: for each claim, assign a known_reason from a different PR
- Run N >= 500 shuffles to build a stable null distribution
- Report null mean, std, 95% CI as the corpus-specific vocabulary floor
- Report the real match rate as a z-score above that floor

### 3.3 Falsifiable Pass/Fail Criteria

| Outcome | Interpretation |
|---------|---------------|
| Real match rate > 6 standard deviations above null mean | The LLM judge is discriminating well — vocabulary overlap alone does not explain the match rate |
| Real match rate < 3 standard deviations above null mean | The LLM judge may be lenient — the corpus floor accounts for a significant share of matches |
| Null mean match rate > 40% | The corpus has high vocabulary overlap — 0 NO_MATCH is partially explained by shared file paths and issue idioms |

### 3.4 Comparison Table Template

| Metric | Real (LLM) | Real (deterministic) | Null mean | Null std | 95% CI | Z-score |
|--------|-----------|---------------------|-----------|----------|--------|---------|
| Match rate | 0.874 | TBD | TBD | TBD | TBD | TBD |
| Partial rate | 0.126 | TBD | TBD | TBD | TBD | TBD |
| No_match rate | 0.000 | TBD | TBD | TBD | TBD | TBD |

## 4. Noise-Floor Baseline

### 4.1 The Problem

No core metric has ever been measured for baseline variance under identical conditions. A shift from 0.536 to 0.572 could be signal or instrument noise.

Source: Bert Shim — "I read the same value four times in four seconds: 124, 121, 119, 123."

### 4.2 Methodology

- Load all stored debate report.json files from v0.2.1
- For each pair, bootstrap-resample with 10,000 resamples
- Report per metric: mean, standard deviation, 95% CI
- Metrics measured: convergence score, verdict rate, theater rate, capitulation rate, avg concessions

### 4.3 Pass/Fail Criteria

| Finding | Interpretation |
|---------|---------------|
| Convergence std < 0.03 for pairs with n >= 50 | The metric is stable enough for pair comparisons at scale |
| Convergence std > 0.05 for any pair | That pair needs more debates before its score can be interpreted |
| Any metric has a CI width > 0.2 for a pair used in published comparisons | That comparison should have been reported with a confidence interval |

### 4.4 Noise-Floor Table Template

| Pair | N | Convergence (mean +/- std) | 95% CI | Verdict rate | Capitulation |
|------|---|------------------------|--------|-------------|-------------|
| homogeneous_gpt | 7 | TBD | TBD | TBD | TBD |
| pair1_gpt_gemini | 24 | TBD | TBD | TBD | TBD |
| pair3_gpt_mistral | 150 | TBD | TBD | TBD | TBD |
| pair5_deepseek_mistral | 36 | TBD | TBD | TBD | TBD |
| pair8_deepseek_gpt_mini | 150 | TBD | TBD | TBD | TBD |

## 5. Shared RLHF Priors Design Note

### 5.1 Why This Is a Field Test Activity

The v0.2.1 separating experiment (DeepSeek+GPT) confirmed the Mistral effect exists — but it did not explain *why*. Two causal mechanisms predict the same data:

- **Positive mechanism**: Mistral is a uniquely good debating partner
- **Negative mechanism**: Non-Mistral models share RLHF priors and rubber-stamp each other; Mistral just happens to break the symmetry

This matters because the two mechanisms lead to different next experiments. If the positive mechanism is correct, the next experiment is "find another model like Mistral." If the negative mechanism is correct, the next experiment is "test models with explicitly diverged RLHF." The v0.2.2 field test is the place to formalize this distinction so v0.3.0 can run the right experiment.

### 5.2 What's New in v0.2.2

Nothing changes in the codebase or results. The new thing is a **documented hypothesis** that changes the interpretation of existing data:

| Before v0.2.2 | After v0.2.2 |
|---------------|--------------|
| "Mistral is the only model that won't fold" (positive story only) | Two competing mechanisms documented: positive (Mistral-specific) and negative (shared priors) |
| Next experiment assumed: test more model pairs from different labs | Next experiment corrected: test RLHF-distance directly (e.g. uncensored vs safety-aligned) |
| Causal gap was implicit — readers could infer it but had to read between the lines | Causal gap is explicit — the learnings log names what is not yet known |

### 5.3 Deliverable

- Design note in `docs/field-test/v0.2.2/learnings.md`
- Distinguishes positive from negative causal stories
- Recommends next experiment: RLHF-distance vs convergence correlation

### 5.3 Pass/Fail Criteria

| Outcome | Interpretation |
|---------|---------------|
| Design note written with both mechanisms and experiment suggestion | Complete |
| Note cross-referenced from v0.2.1 learnings | Recommended but optional |

## 6. Pass/Fail Philosophy

Same as v0.2.0/v0.2.1: **invariant-based assertions**, not golden-plan matching.

**What is tested:**
- Permutation control null distribution with >= 500 shuffles
- Noise-floor bootstrap with 10,000 resamples per pair
- Design note with both causal mechanisms documented

**What is NOT tested:**
- New debates or LLM calls (zero added)
- New model pairs
- New artifacts or domains
- Changes to the debate protocol or reviewer prompts
- UI/CLI surfaces (deferred to v1.0.0)

## 7. Execution Order

1. Run `scripts/noise_floor.py --trials 10000 --seed 42` — bootstrap all pairs
2. Run `scripts/permutation_control.py --shuffles 500 --seed 42` — null distribution
3. Write `docs/field-test/v0.2.2/learnings.md` — shared RLHF priors + findings
4. Write `docs/field-test/v0.2.2/FIELD_TEST_REPORT.md` — full results

## 8. Deliverables

- `docs/field-test/v0.2.2/FIELD_TEST_REPORT.md` — full results with noise-floor table, permutation control, and design notes
- `docs/field-test/v0.2.2/field-test-plan.md` — this document
- `docs/field-test/v0.2.2/learnings.md` — lessons learned
- `results/field-test/v0.2.2/noise-floor-report.json` — full bootstrap results
- `results/field-test/v0.2.2/noise-floor-report.md` — summary table
- `results/field-test/v0.2.2/permutation-control-report.json` — null distribution
- `results/field-test/v0.2.2/permutation-control-report.md` — summary