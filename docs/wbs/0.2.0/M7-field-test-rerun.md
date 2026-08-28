# M7 — Field Test Rerun

> Goal: after all M1-M6 fixes are applied, re-run the full-corpus and small-corpus field tests, run flakiness sweep, produce corrected field-test reports, and publish article updates. This milestone validates that the fixes actually produce correct results. Part of [index](index.md).

## PRD coupling

- [07-success-metrics §7.6 methodology](../../design/prd/07-success-metrics.md): field-test reporting standards
- [field-testing-strategy Tier 0](../../field-test/field-testing-strategy.md): corpus execution, flakiness analysis
- [18-article-plan §18.2](../../design/prd/18-article-plan.md): article updates with corrected results

## Dependencies

Upstream: M1, M2, M3, M4, M5, M6. Downstream: M8.

## Workstreams & tasks

### WS 7.a — Full-corpus field test

- [ ] T7.1 (#112) Re-run full-corpus field test (70 PRs, 4 model pairs) with corrected engine and scripts
  - Verify no zero-claim no-op artifacts remain (fix for #103)
  - Verify repo coverage matches actual corpus (fix for #102)
  - Verify MATCH rates use substantive claims only (fix for #104)
  - Verify overlap calculations are consistent (fix for #111)

### WS 7.b — Small-corpus field test

- [ ] T7.2 (#113) Re-run small-corpus field test (5 PRs, 4 model pairs) with corrected engine and scripts
  - Verify overlap values match published CSV
  - Verify no zero-claim artifacts
  - Cross-check against full-corpus results

### WS 7.c — Flakiness sweep

- [ ] T7.3 (#122) Run flakiness sweep (N=5 seeds) with corrected engine
  - Verify stability calculation accounts for missing runs (fix for #99)
  - Compare flakiness rates against v0.1.0 baseline

### WS 7.d — Reports and articles

- [ ] T7.4 (#114) Produce updated FIELD_TEST_REPORT_full_corpus.md and FIELD_TEST_REPORT_small_corpus.md
  - Correct repo coverage, exclude no-op verdicts, restrict MATCH rate to substantive claims
  - Fix overlap statements, add capitulation rate to pair ranking table
  - Add FP/FN rates to ground-truth section, add methodology section with homogeneous control thresholds
  - Add doc-generation checks that derive summary stats from CSVs

## Documents, plans & tests to update

- `docs/field-test/v0.2.0/FIELD_TEST_REPORT_full_corpus.md` — new file with corrected results
- `docs/field-test/v0.2.0/FIELD_TEST_REPORT_small_corpus.md` — new file with corrected results
- `results/field-test/v0.2.0/` — new directory with corrected corpus, debates, analysis CSVs
- `scripts/` — add doc-generation checks that derive summary stats from CSVs
- `docs/design/prd/07-success-metrics.md` — update binary bar results to v0.2.0
- `docs/design/prd/18-article-plan.md` — update with corrected metrics for article updates
- dev.to articles — publish updated field-test results and methodology improvements

## Acceptance criteria / exit gate

- All field test runs complete without errors
- Zero invalid (no-op) verdicts counted in results
- Ground-truth MATCH rate reflects only substantive claims
- Overlap statistics are self-consistent
- Reports are internally consistent (prose matches CSVs)
- Ruff clean, mypy strict clean, full test suite green
- Code review completed on all changes
- Committed and pushed to `rel-0.2.0`

## Explicitly out of scope

Release readiness (M8) — that's the next and final milestone.