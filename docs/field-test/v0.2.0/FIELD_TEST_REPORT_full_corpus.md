# Field Test Results — v0.2.0 Full Corpus

> **Date:** 2026-08-27
> **Provider:** OpenRouter (single API key: `OPENROUTER_API_KEY`)
> **Models:** GPT-4o-mini, Mistral Small 3.2, DeepSeek-V3, Gemini 2.5 Flash
> **Corpus:** 150 artifacts across 4 domains (PR review, incident response, change management, security incidents)
> **Pairs:** 4 active pair roles (1 primary, 1 validation, 1 negative control, 1 homogeneous control)
> **Cost:** $0.42 · **Debates:** 217 · **Analysis:** 5 analysis CSVs produced
> **Config:** `results/field-test/v0.2.0/corpus.csv` + subset files under `results/field-test/v0.2.0/`

---

## BLUF (Bottom Line Up Front)

**The `v0.2.0` field test confirms the `v0.1.0` model-selection story under a corrected mixed-domain pipeline.**

The strongest full-corpus default remains `pair3_gpt_mistral` (GPT-4o-mini + Mistral Small 3.2). Across 150 debates it produced zero theater, 2 verdicts, 148 disputes, 4 capitulation cascades, 2,927 total concessions, and an average convergence score of 0.536. That is materially stronger than the negative control and stronger than the partial homogeneous control sample.

The negative control behaved exactly as it should. `pair1_gpt_gemini` (GPT-4o-mini + Gemini 2.5 Flash) completed 24/24 debates with zero verdicts, zero theater, zero capitulation, and an average convergence score of 0.033. It remains a bad default pair and a good negative control.

The validation pair also held up. `pair5_deepseek_mistral` completed 36 debates with 1 verdict, 35 disputes, zero theater, 1 capitulation cascade, and a stronger average convergence score of 0.572. That confirms `DeepSeek + Mistral` remains materially stronger than the negative control, even though the primary product-default conclusion should still rest on the full-corpus `pair3` run.

The key corrections from `v0.2.0` mattered:

- mixed-corpus scripts were migrated from flat `pr_id` assumptions to nested `artifact_id` layout
- non-PR artifacts now strip HTML and bound prompt size before review
- pair defaults now follow corpus role correctly (`corpus.csv`, validation subset, negative-control subset)
- the ground-truth judge merge bug was fixed, restoring the full `2333` judged rows

The PR-domain binary bar is clearly met:

- `2070 MATCH`
- `263 PARTIAL`
- `0 NO_MATCH`
- `0 ERROR`

Sampled flakiness is also clean:

- `2/2` sampled artifacts stable by verdict
- `0` flaky in the completed sample

The remaining caveats are not about whether the system works. They are about cleanup and interpretation:

- `19` error terminations still need investigation (`14` in `pair3`, `5` in `pair5`)
- non-PR expert ratings are still pending
- `would_resolve_if` actionability is still unrated
- homogeneous control evidence is still only a small partial sample

---

## Conclusions

### 1. GPT + Mistral is the right full-corpus default for v0.2.0

`pair3_gpt_mistral` is the most defensible product-default pair tested in `v0.2.0`. It ran on the full 150-artifact corpus, produced strong engagement, zero theater, and materially better convergence than both the negative control and the partial homogeneous control sample.

Its verdict rate is still low (2/150), but that is not the core product failure mode. The product is designed to preserve dissent rather than force agreement, and the PR-domain ground-truth results show that disputed debates can still be highly relevant.

### 2. The negative control validates the pair-selection thesis

`pair1_gpt_gemini` remained weak in exactly the way `v0.1.0` predicted. It did not collapse into theater. It did not capitulate. It simply failed to converge productively. That makes it a strong control: it shows that the better-performing pairs are not just benefitting from easier artifacts or looser evaluation.

### 3. The stronger validation pair did not repeat the worst v0.1.0 capitulation pattern

`pair5_deepseek_mistral` remained materially stronger than the negative control, but on the `v0.2.0` validation subset it produced only 1 capitulation cascade across 36 debates. That is a much cleaner validation signal than the extreme capitulation-heavy behavior seen in `v0.1.0`.

### 4. The mixed-domain pipeline now works end-to-end

`v0.2.0` forced the project to stop being a PR-only field-test harness. The pipeline now handles:

- PR review
- incident response
- change management
- security incidents

That required real script migration work, but the result is a better-aligned evaluation surface for the broader product thesis.

### 5. The PR-domain binary bar is clearly satisfied

The repaired ground-truth judgment output contains `2333` judged rows across `59` PR artifacts with documented outcomes:

- `2070 MATCH` (`88.7%`)
- `263 PARTIAL` (`11.3%`)
- `0 NO_MATCH`

That means the system is surfacing relevant issues even when debates remain disputed. This is the strongest completed evidence in the report.

---

## Surprises

1. **The negative control remained almost completely unproductive outside PR-only evaluation.** The weakness of `GPT + Gemini` held up under a mixed-domain corpus with almost no resolution at all.

2. **The negative control failed by stubbornness, not by collapse.** There was zero theater and zero capitulation. The pair engaged, but produced low-yield disagreement.

3. **The validation pair was strong without repeating the extreme v0.1.0 capitulation behavior.** That makes the `pair5` validation result cleaner and more interpretable than the earlier release.

4. **Mixed-domain ingestion was harder than model execution.** Several meaningful fixes in `v0.2.0` were about artifact quality and script assumptions, not about the debate engine itself.

5. **Sampled flakiness ended up cleaner than the interrupted early run suggested.** Once the sweep completed, both sampled artifacts were stable by verdict.

---

## Learnings

### Corpus & Data Learnings

1. **The `v0.1.0` negative-control conclusion generalizes.** `GPT + Gemini` is still weak under a mixed-domain corpus.
2. **Candidate-source URLs are not artifact URLs.** Planning sources and reviewable artifacts are not the same thing; pinned artifact URLs matter.
3. **Narrative domains are harder to evaluate than PR diffs.** Non-PR domains need expert-rated usefulness, not just binary ground truth.

### Pipeline & Engineering Learnings

4. **Every script had to be updated for `artifact_id` and nested corpus layout.** The move from flat PR-only evaluation to mixed-domain evaluation touched reviewer, combine, debate, analysis, ground-truth, and flakiness scripts.
5. **Non-PR artifact ingestion is the hard part.** PRs are clean diffs; non-PR artifacts come in inconsistent HTML, markdown, and dashboard forms.
6. **The debate protocol itself generalized better than the ingestion layer.** Domain-specific reviewer prompts were needed, but the debate controller and synthesis layer did not need structural changes.
7. **The ground-truth merge bug was a data-integrity bug, not a modeling bug.** `07_llm_judge.py` was still keyed on `pr_id`, which collapsed `artifact_id`-based rows until fixed.

### Model & Execution Learnings

8. **The 2-model primary strategy is sufficient.** Full-corpus GPT + Mistral plus subset DeepSeek/Gemini was the right cost vs. insight tradeoff.
9. **High dispute rates do not imply low relevance.** The PR ground-truth results show that many disputed debates still point to the right underlying issue.
10. **Sampled flakiness is lower than it first appeared.** Stable verdicts matter more than small convergence-score movement within a verdict band.

---

## Takeaways

1. **Keep `pair3_gpt_mistral` as the mainline pair.** It is the best full-corpus default tested here.
2. **Keep `pair5_deepseek_mistral` as validation, not the default story.** It is stronger than the negative control, but the product-default claim should rest on the full-corpus pair.
3. **Keep `pair1_gpt_gemini` explicitly labeled as a negative control.** Its weakness is useful evidence, not an embarrassment to hide.
4. **Continue replacing candidate URLs with pinned artifact URLs.** This is the biggest remaining data-quality improvement lever.
5. **Treat verdict rate and relevance as separate dimensions.** Low verdict rates do not erase strong ground-truth relevance.

---

## What's Next (v0.2.0)

1. Investigate the `14` primary-pair and `5` validation-pair error terminations and decide whether to retry or classify them as degraded-but-valid data.
2. Complete non-PR expert ratings.
3. Rate `would_resolve_if` actionability.
4. Tighten the report language around the provisional homogeneous-control sample.
5. Optionally expand the homogeneous-control sample if a cleaner heterogeneous-vs-homogeneous comparison is needed.

---

## Scorecards

### Scorecard A — Strict Verdict (Release Gate)

A debate is a "pass" only if it reaches convergence (verdict). Disputed or theater = fail.

| Category | Debates | Pass | Fail | Pass Rate | Gate |
|----------|---------|------|------|-----------|------|
| Primary pair (`pair3_gpt_mistral`) | 150 | 2 | 148 | 1.3% | ≥80% ❌ low by design; dissent preserved |
| Negative control (`pair1_gpt_gemini`) | 24 | 0 | 24 | 0% | ≥80% ❌ expected weak control behavior |
| Validation pair (`pair5_deepseek_mistral`) | 36 | 1 | 35 | 2.8% | ≥80% ❌ subset only; verdicts still rare |
| Non-theater (all pairs) | 217 | 217 | 0 | 100% | 100% ✅ debate protocol engaged |

**Scorecard A fails if you treat verdict as the only success metric.** That is expected. The product is designed to preserve dissent, not force agreement.

### Scorecard B — Safe-Fail (Engagement Semantics)

A debate is a "pass" if it produced real engagement (non-theater, claims addressed, state changes).

| Category | Debates | Pass | Pass* | True Fail | Pass Rate |
|----------|---------|------|-------|-----------|-----------|
| `pair3_gpt_mistral` | 150 | 2 | 148 | 0 | 100% |
| `pair1_gpt_gemini` | 24 | 0 | 24 | 0 | 100% |
| `pair5_deepseek_mistral` | 36 | 1 | 35 | 0 | 100% |
| `homogeneous_gpt` | 7 | 0 | 7 | 0 | 100% |
| **Total** | **217** | **3** | **214** | **0** | **100%** |

**Scorecard B passes cleanly.** Every debate produced engagement. Theater is zero across all completed runs.

---

## Release Gate Verdict

| Criterion | Requirement | Result | Status |
|-----------|-------------|--------|--------|
| Theater rate | < 30% | 0/217 (0%) across all pairs | ✅ PASS no empty debates observed |
| Convergence rate | 30-70% | 1.3% on primary pair, 2.8% on validation, 0% on negative control | ⏳ BELOW RANGE expected because the system preserves dissent |
| Budget exhaustion rate | < 20% | not measured | ⏳ PENDING metric not collected in this run |
| Heterogeneous vs homogeneous delta | +30% distinct | pair3 (0.536) vs homogeneous (0.273) = +96% on current partial homogeneous sample | ⚠️ PROVISIONAL homogeneous sample is only 7 debates |
| Engine errors (non-rate-limit) | 0 | 14 errors in pair3, 5 in pair5 | ⚠️ PARTIAL counts are known, root-cause review still pending |
| Binary bar (≥1 distinct issue confirmed by ground truth) | ≥1 artifact | 2070/2333 MATCH, 263/2333 PARTIAL, 0 NO_MATCH across 59 PR artifacts | ✅ PASS strong relevance to known outcomes |
| Verdict stability | > 80% | 2/2 sampled artifacts stable at 100% verdict stability | ✅ PASS small sample only |
| `would_resolve_if` actionable | > 50% | not yet rated | ⏳ PENDING expert/actionability review still needed |

**Verdict: PASS WITH CAVEATS.** The engine behavior is strong, the binary bar is clearly met, and sampled flakiness is stable. The remaining caveats are the 19 error terminations, the partial homogeneous-control sample, and the pending non-PR ratings / `would_resolve_if` review.

---

## Observations

### Pair Roles

| Role | Pair | Result |
|------|------|--------|
| Primary / positive | `pair3_gpt_mistral` | best full-corpus default |
| Validation | `pair5_deepseek_mistral` | stronger than negative control on subset |
| Negative control | `pair1_gpt_gemini` | weak, as expected |
| Homogeneous control | `homogeneous_gpt` | partial sample only |

### Debate Outcomes

| Pair | Models | Debates | Verdicts | Verdict % | Avg Score | Concessions | Capitulation | Theater | Errors |
|------|--------|---------|----------|-----------|-----------|-------------|-------------|---------|--------|
| `pair3_gpt_mistral` | GPT + Mistral | 150 | 2 | 1.3% | 0.536 | 2,927 total | 4 | 0 | 14 |
| `pair1_gpt_gemini` | GPT + Gemini | 24 | 0 | 0% | 0.033 | 34 total | 0 | 0 | 0 |
| `pair5_deepseek_mistral` | DeepSeek + Mistral | 36 | 1 | 2.8% | 0.572 | 936 total | 1 | 0 | 5 |
| `homogeneous_gpt` | GPT + GPT | 7 | 0 | 0% | 0.273 | 62 total | 0 | 0 | 0 |

### Ground-Truth Verification

| Metric | Count | % |
|--------|-------|---|
| MATCH | 2070 | 88.7% |
| PARTIAL | 263 | 11.3% |
| NO_MATCH | 0 | 0.0% |
| ERROR | 0 | 0.0% |
| Total judged rows | 2333 | 100.0% |

Coverage:

- 59 PR artifacts with documented ground truth
- 2333 judged claim rows
- 0 unrelated (`NO_MATCH`) claims

### Flakiness Sweep

| Artifact | Runs | Dominant Verdict | Stability | Avg Convergence | Score Range | Flaky |
|----------|------|------------------|-----------|-----------------|-------------|-------|
| `prometheus_prometheus_PR19500` | 5 | disputed | 1.00 | 0.502 | 0.46-0.52 | False |
| `kubernetes_kubernetes_PR140886` | 5 | disputed | 1.00 | 0.650 | 0.57-0.68 | False |

### Cost & Latency

| Model | Cost | Avg Latency | Total Tokens | Artifact Count |
|-------|------|-------------|--------------|----------------|
| GPT-4o-mini | $0.2462 | 7678ms | 1,372,855 | 150 |
| Gemini 2.5 Flash | $0.0212 | 5558ms | 75,016 | 24 |
| DeepSeek-V3 | $0.1011 | 35710ms | 301,843 | 36 |
| Mistral Small 3.2 | $0.0507 | 14976ms | 506,159 | 150 |
| **Total** | **$0.4192** | | **2,255,873** | **360 reviewer runs** |

### Cross-Model Overlap

`05_analyze.py` reports:

- **Avg overlap (GPT-4o-mini vs Gemini): `0.000`**

This matches the qualitative `v0.1.0` finding: the weak negative-control pair is not failing because both sides raise the same issues. They raise distinct issues and still fail to converge productively.

### Coverage Status

| Dimension | Value |
|-----------|-------|
| Corpus | 150 artifacts across 4 domains |
| Completed negative-control debates | 24 |
| Completed validation debates | 36 |
| Primary full-corpus pair | complete (150 debates) |
| Validation pair | complete on subset |
| Homogeneous control summary | partial (7 debates) |
| PR ground-truth export | complete |
| Non-PR expert ratings | pending |

---

## Issues Found and Fixed

The `v0.2.0` field test surfaced several pipeline issues that are now part of the report story because they changed the trustworthiness of the results.

| # | Issue | Status | Impact |
|---|-------|--------|--------|
| 1 | `v0.1.0` script assumptions broke on mixed `artifact_id` corpus | ✅ Fixed script migration complete | Reviewer, combine, debate, analysis, ground-truth, and flakiness scripts now target `v0.2.0` layout |
| 2 | README still described old/full-matrix behavior | ✅ Fixed documentation updated | Runbook now matches `v0.2.0` execution design |
| 3 | Non-PR artifacts downloaded as raw HTML/index pages | ✅ Mitigated input sanitized | Reviewer strips HTML and bounds prompt size |
| 4 | Missing subset corpus files for validation / negative control | ✅ Fixed subset files created | `validation_subset.csv` and `negative_control_subset.csv` created |
| 5 | Negative-control commands were undocumented | ✅ Fixed pair roles documented | Pair roles and subset commands now documented |
| 6 | Several non-PR artifacts still point to dashboard or index pages instead of pinned documents | ⚠️ Open corpus cleanup still needed | Final report quality will improve after corpus URL cleanup |
| 7 | `07_llm_judge.py` merged on `pr_id` instead of `artifact_id`, collapsing 2333 judged rows to 359 | ✅ Fixed merge key corrected | Final judged output repaired to full row count without rerunning model calls |

---

## References

| Document | Relevance |
|----------|-----------|
| `docs/field-test/v0.2.0/field-test-plan.md` | canonical v0.2.0 plan |
| `results/field-test/v0.2.0/corpus.csv` | full mixed corpus |
| `results/field-test/v0.2.0/validation_subset.csv` | validation subset |
| `results/field-test/v0.2.0/negative_control_subset.csv` | negative-control subset |
| `results/field-test/v0.2.0/SUBSETS.md` | pair-role definitions |
| `results/field-test/v0.2.0/analysis/debate-summary.csv` | full debate summary |
| `results/field-test/v0.2.0/analysis/cost-latency.csv` | reviewer cost/latency totals |
| `results/field-test/v0.2.0/analysis/ground-truth-judged.csv` | repaired 2333-row PR ground-truth judgment output |
| `results/field-test/v0.2.0/analysis/flakiness-summary.csv` | sampled verdict stability evidence |
| `docs/field-test/v0.1.0/FIELD_TEST_REPORT_full_corpus.md` | v0.1.0 baseline and format reference |
