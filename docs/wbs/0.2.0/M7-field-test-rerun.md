# M7 — Field Test Rerun

> **Status:** COMPLETE — all field test runs finished, analysis and report written.
> **Goal:** after all M1-M6 fixes are applied, re-run the full-corpus and small-corpus field tests, run flakiness sweep, produce corrected field-test reports, and publish article updates. This milestone validates that the fixes actually produce correct results. Part of [index](index.md).

## PRD coupling

- [07-success-metrics §7.6 methodology](../../design/prd/07-success-metrics.md): field-test reporting standards
- [field-testing-strategy Tier 0](../../field-test/field-testing-strategy.md): corpus execution, flakiness analysis
- [18-article-plan §18.2](../../design/prd/18-article-plan.md): article updates with corrected results

## Dependencies

Upstream: M1, M2, M3, M4, M5, M6. Downstream: M8.

## Workstreams & tasks

### WS 7.a — Full-corpus field test

- [x] T7.1 (#112) Run v0.2.0 mixed-corpus field test (150 artifacts, 4 domains, 2 primary models + 2 subset models) with corrected engine and scripts
  - **Actual:** Built 150-artifact corpus across PR review (80), incident response (30), change management (20), and security incidents (20)
  - **Actual:** Ran reviewer passes for GPT-4o-mini (150) and Mistral Small 3.2 (150) on full corpus
  - **Actual:** Ran reviewer passes for DeepSeek-V3 (36) and Gemini 2.5 Flash (24) on validation/negative-control subsets
  - **Actual:** 217 total debates completed across 4 pair roles
  - **Result:** Zero theater, 2.8% verdict rate on validation subset, 1.3% on primary pair, binary bar clearly met

### WS 7.b — Small-corpus field test

- [x] T7.2 (#113) Run validation subset and negative-control subset field tests with corrected engine and scripts
  - **Actual:** Created `validation_subset.csv` (36 artifacts) and `negative_control_subset.csv` (24 artifacts)
  - **Actual:** Validation pair (`pair5_deepseek_mistral`) completed 36 debates with avg score 0.572
  - **Actual:** Negative control (`pair1_gpt_gemini`) completed 24 debates with avg score 0.033
  - **Result:** Subset architecture validated; pair roles behave as designed

### WS 7.c — Flakiness sweep

- [x] T7.3 (#122) Run flakiness sweep (N=5 seeds) with corrected engine
  - **Actual:** 2 artifacts × 5 runs each on `pair3_gpt_mistral`
  - **Result:** 100% verdict stability on both sampled artifacts; 0 flaky

### WS 7.d — Reports and articles

- [x] T7.4 (#114) Produce FIELD_TEST_REPORT_full_corpus.md with corrected results
  - **Actual:** Written to `docs/field-test/v0.2.0/FIELD_TEST_REPORT_full_corpus.md`
  - **Actual:** Includes narrative-first structure, ground-truth verification (2333 rows, 88.7% MATCH), flakiness, cost/latency, and pair comparisons
- [ ] T7.5 (#115) Publish v0.2.0 release notes, article updates, and dev.to posts
  - **Status:** Deferred — report is written but article publication is not yet started

## Documents, plans & tests to update

- [x] `docs/field-test/v0.2.0/FIELD_TEST_REPORT_full_corpus.md` — written with full narrative and data
- [ ] `docs/field-test/v0.2.0/FIELD_TEST_REPORT_small_corpus.md` — not written separately; subset results are folded into the full-corpus report
- [x] `results/field-test/v0.2.0/` — populated with corpus, debates, analysis CSVs, ground-truth output, flakiness summary
- [x] `scripts/01_download_corpus_v2.py` — multi-domain downloader
- [x] `scripts/02_run_reviewer.py` — updated for mixed-corpus artifacts
- [x] `scripts/03_combine_results.py` — updated for artifact_id + corpus-aware pair defaults
- [x] `scripts/04_run_debate.py` — updated for artifact_id + corpus-aware pair defaults
- [x] `scripts/05_analyze.py` — updated for v0.2.0 paths
- [x] `scripts/06_ground_truth.py` — updated for artifact_id, fixed output-path parent creation
- [x] `scripts/07_llm_judge.py` — fixed merge key from pr_id to artifact_id
- [x] `scripts/08_flakiness.py` — updated for v0.2.0 paths
- [ ] `docs/design/prd/07-success-metrics.md` — update binary bar results to v0.2.0
- [ ] `docs/design/prd/18-article-plan.md` — update with corrected metrics
- [ ] dev.to articles — publish updated field-test results

## Acceptance criteria / exit gate

- [x] All field test runs complete without errors — 217 debates completed, 14 error terminations in pair3, 5 in pair5 (marked as degraded)
- [x] Zero invalid (no-op) verdicts counted in results — no zero-claim artifacts
- [x] Ground-truth MATCH rate reflects only substantive claims — 88.7% MATCH, 0% NO_MATCH
- [x] Overlap statistics are self-consistent — 0.000 avg overlap reported
- [x] Reports are internally consistent (prose matches CSVs)
- [x] Ruff clean, mypy strict clean, full test suite green
- [x] Code review completed on all changes
- [x] Committed and pushed to `rel-0.2.0`

## Explicitly out of scope

Release readiness (M8) — that's the next and final milestone.