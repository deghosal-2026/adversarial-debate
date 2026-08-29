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

## 3. DeepSeek+GPT Separating Experiment

### 3.1 Hypothesis

The v0.2.0 data shows every productive pair contains Mistral. This is equally consistent with two explanations:

- **Diversity hypothesis**: debate quality is driven by diversity of training objective — models from labs with different RLHF philosophies disagree more productively
- **Mistral effect**: Mistral is the unique variable — it won't fold under pressure, and no other model shares this property

### 3.2 Separating Experiment

**Pair under test:** DeepSeek-V3 (deepseek_deepseek-chat) + GPT-4o-mini (openai_gpt-4o-mini)

**Corpus:** Full 150-artifact, 4-domain corpus (same as v0.2.0)

**Pipeline:** Same as all other pairs — 02_run_reviewer → 03_combine_results → 04_run_debate → 05_analyze

### 3.3 Falsifiable Pass/Fail Criteria

| Outcome | Interpretation | Action |
|---------|---------------|--------|
| Convergence > 0.4, theater < 5%, capitulation < 10% | Diversity hypothesis supported — different labs produce productive debate without Mistral | Publish as evidence for the theory; update model selection guidance |
| Convergence < 0.2, high theater or capitulation | Mistral effect confirmed — Mistral is the unique variable, not diversity | Revise model selection guidance to "always include Mistral" |
| Productive but with high capitulation (> 30%) | Mixed — diversity helps but one side still folds | Investigate which side folds; may need prompt-level fix |

### 3.4 Shared-Corpus Confound — Llama Control Pair (Optional)

GPT+Gemini share both training objective AND training data. A Llama+GPT pair separates them.

**Pair under test:** Llama 3 + GPT-4o-mini
**Scope:** Validation subset only (secondary experiment)
**Pass/fail:** Same criteria as above

### 3.5 Comparison Table Template

| Metric | GPT+Mistral | DeepSeek+Mistral | DeepSeek+GPT | GPT+Gemini | GPT+GPT |
|--------|------------|-----------------|-------------|-----------|---------|
| Convergence score | 0.536 | 0.572 | TBD | TBD | 0.688 |
| Verdict rate | 48% | 97% | TBD | 4% | 57% |
| Theater rate | 0% | 0% | TBD | ~0% | 0% |
| Capitulation rate | low | 65% | TBD | low | low |
| Concession rate | 1,728 | 2,352 | TBD | 727 | 1,444 |
| Binary match rate | 88.7% | 85.2% | TBD | 35.7% | 68.8% |
| Missed-issue rate | TBD | TBD | TBD | TBD | TBD |

## 4. Pipeline Integrity — Row-Count Invariants

### 4.1 The Problem

In v0.2.0, a join logic error silently collapsed the ground-truth dataset from 2,333 rows to 359. Published numbers were reported against 15% of the real corpus. The specific bug was fixed, but the underlying failure mode — silent row loss at pipeline seams without any assertion — was not addressed.

### 4.2 The Fix

Every pipeline seam now asserts `count_post` against `count_pre` with the expected relation. If the assertion fails, the pipeline stops with a diagnostic message.

### 4.3 Seam Assertions

| Seam | Scripts | Invariant | Expected Relation | Failure Behavior |
|------|--------|-----------|-----------------|-----------------|
| Corpus → model review | `02_run_reviewer.py` | `count_post <= count_pre` | Equal for full corpus | Pipeline fails with artifact ID |
| Model review → pair combine | `03_combine_results.py` | `count_post <= count_pre` | Equal per pair | Pipeline fails with pair + artifact ID |
| Pair combine → debate | `04_run_debate.py` | `count_post <= count_pre` | Equal | Pipeline fails with pair + artifact ID |
| Debate → analysis | `05_analyze.py` | `count_post <= count_pre` | Zero-claim exclusions logged with count | Warning with `--strict` flag |
| Analysis → ground truth | `06_ground_truth.py` | `count_post <= count_pre` | Non-substantive filters logged with count | Warning with `--strict` flag |

### 4.4 Fail-Fast Behavior

- If any assertion fails (unexpected row loss), the pipeline stops with: `SEAM FAIL: {seam_name}: expected {N}, found {M} — MISSING: {artifact_id_list}`
- This is a hard error — no silent `continue`
- The field test runner must not proceed past a failed seam

### 4.5 Strict Mode

- `--strict` flag: any row count change, even expected (zero-claim exclusion, non-substantive filter), emits a structured warning
- Non-strict mode: expected exclusions are logged silently
- The field test report must include whether `--strict` was used

### 4.6 Pipeline Integrity Evidence Template

The field test report will include a new section:

```
## Pipeline Integrity

| Seam | Pre-count | Post-count | Expected | Status |
|------|----------|-----------|----------|--------|
| Corpus → model review | 150 | 150 | equal | PASS |
| Model review → pair combine | 150 | 150 | equal | PASS |
| Pair combine → debate | 150 | 150 | equal | PASS |
| Debate → analysis | 150 | 148 | <= (2 zero-claim excluded) | PASS |
| Analysis → ground truth | 148 | 148 | <= | PASS |
```

## 5. False-Negative Measurement

### 5.1 The Problem

v0.2.0 only measures binary match rate (precision): "does at least one debate claim match the documented PR outcome?" It has no recall measurement. The article explicitly states "false negatives are invisible" as a limitation.

### 5.2 Methodology

- **Source**: 70 PRs from the v0.1.0 corpus with documented revert reasons
- **Input**: Pre-fix artifact for each PR (the diff before the fix was applied — the original buggy state)
- **Process**: Run both independent reviewers on the pre-fix artifact, same as any other artifact
- **Measurement**: Do both reviewers converge on "looks fine" (no blocker-level claims about the issue that actually existed)?
- **Metric**: `missed_issues / total_known_issues = missed_issue_rate`

### 5.3 Comparison Dimensions

| Dimension | What it measures |
|-----------|-----------------|
| Reviewer A alone | What does GPT-4o-mini miss when reviewing alone? |
| Reviewer B alone | What does Mistral miss when reviewing alone? |
| Both reviewers (dual) | What do both miss together? The dual-reviewer blind spot |
| Improvement ratio | `max(A_missed, B_missed) / both_missed` — quantifies value of independent dual review |

### 5.4 Survivorship Boundary

The field test report will include this exact language:

> "The missed-issue rate is computed across N documented failures — failures that were eventually found and fixed, and whose PRs have a recorded revert reason. Failures that were never caught, never documented, or never reverted are invisible to any ground-truth study. The reported rate is therefore a **lower bound**: the true missed-issue rate is at least this value, and likely higher."

### 5.5 Pass/Fail Criteria

| Result | Interpretation |
|--------|---------------|
| Missed-issue rate < 5% | Dual-reviewer independence is effective |
| Missed-issue rate 5-15% | Dual-reviewer helps but has a measurable blind spot |
| Missed-issue rate > 15% | Dual-reviewer independence is not sufficient — additional safety layers needed |
| Single-reviewer == dual-reviewer | Independence adds zero value |

### 5.6 Expanded Comparison Table

| Pair | Binary Match Rate | Single-A Miss | Single-B Miss | Dual Miss | Improvement |
|------|------------------|--------------|--------------|----------|-------------|
| GPT+Mistral | 88.7% | TBD | TBD | TBD | TBD |
| DeepSeek+Mistral | 85.2% | TBD | TBD | TBD | TBD |
| DeepSeek+GPT | TBD | TBD | TBD | TBD | TBD |
| GPT+Gemini | 35.7% | TBD | TBD | TBD | TBD |
| GPT+GPT | 68.8% | TBD | TBD | TBD | TBD |

## 6. Pass/Fail Philosophy

Same as v0.2.0: **invariant-based assertions**, not golden-plan matching. LLM output is non-deterministic.

**What is tested:**
- DeepSeek+GPT separating experiment with falsifiable criteria
- All 5 seam assertions pass (pipeline integrity)
- Missed-issue rate measured with survivorship boundary
- No regressions against v0.2.0 baseline metrics

**What is NOT tested:**
- Exact claim text matching (LLM variance)
- New domains (deferred to v0.3.0)
- UI/CLI surfaces (deferred to v1.0.0)

## 7. Execution Order

1. Run `02_run_reviewer.py` for DeepSeek on full corpus (if not already cached)
2. Run `03_combine_results.py` — includes pair8_deepseek_gpt_mini, seam assertions
3. Run `04_run_debate.py` — debates for new pair, seam assertions
4. Run `05_analyze.py` — includes all 5 pairs, seam assertions
5. Run `06_ground_truth.py` — includes seam assertions
6. Run `07_llm_judge.py` — ground-truth judging
7. Run `09_missed_issues.py` — false-negative measurement
8. Run `08_flakiness.py` — flakiness sweep on representative artifacts

## 8. Deliverables

- `docs/field-test/v0.2.1/FIELD_TEST_REPORT.md` — full results with pipeline integrity evidence, model selection guidance, and missed-issue rate
- `docs/field-test/v0.2.1/learnings.md` — lessons learned
- Updated article vault files with new conclusions (diversity hypothesis result, pipeline integrity, recall measurement)
- All results in `results/field-test/v0.2.1/`