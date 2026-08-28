# M5 — Field Test Data Integrity

> Goal: correct all field-test report inaccuracies identified in the v0.1.0 postmortem. Fix etcd corpus claim, no-op verdict inflation, MATCH rate fragment contamination, zero-overlap contradiction, capitulation rate presentation, and homogeneous control falsifiability. Part of [index](index.md).

## PRD coupling

- [07-success-metrics §7.6 methodology](../../design/prd/07-success-metrics.md): field-test reporting standards, binary bar, overlap analysis
- [field-testing-strategy](../../field-test/field-testing-strategy.md): corpus composition, control methodology

## Dependencies

Upstream: M1, M2, M3, M4. Downstream: M6, M7, M8.

## Workstreams & tasks

### WS 5.a — Report corrections

- [ ] T5.1 (#102) Full-corpus report: correct etcd coverage claim — only 3 repos exist in frozen corpus, not 4
- [ ] T5.2 (#103) Full-corpus report: exclude zero-claim zero-event no-op rows from verdict totals and success metrics
- [ ] T5.3 (#104) MATCH rate: restrict ground-truth scoring to substantive issue claims only — exclude severity labels, evidence headings, file paths, generic remediation text
- [ ] T5.4 (#111) Small-corpus report: correct universal zero-overlap claim — overlap CSV contains non-zero values

### WS 5.b — Methodology improvements

- [ ] T5.5 (#72) Pair ranking table: add capitulation rate column or annotate verdict rate with capitulation caveat
- [ ] T5.6 (#74) Homogeneous control pair (GPT+GPT): define falsifiable failure thresholds so control can actually detect leakage
- [ ] T5.7 (#73) Implement canary token test for runtime isolation verification as a built-in feature

## Documents, plans & tests to update

- `docs/field-test/v0.1.0/FIELD_TEST_REPORT_full_corpus.md` — correct etcd claim, no-op verdicts, MATCH rate, add capitulation column, add control thresholds
- `docs/field-test/v0.1.0/FIELD_TEST_REPORT_small_corpus.md` — correct zero-overlap claim
- `docs/field-test/v0.1.0/field-testing-strategy.md` — add homogeneous control falsifiable thresholds
- `scripts/06_ground_truth.py` — substantive claim filtering, FP/FN rate computation
- `results/field-test/v0.1.0/analysis/` — regenerate CSVs if corrections change derived data
- `src/adversarial_debate/engine/evidence.py` — add canary leak detection (`_detect_leak`)
- `src/adversarial_debate/engine/debate_controller.py` — inject canary after A's review

## Acceptance criteria / exit gate

- All 7 issues closed with passing tests
- Corrected reports are internally consistent (prose matches CSVs)
- Ruff clean, mypy strict clean, full test suite green
- Code review completed on all changes
- Committed and pushed to `rel-0.2.0`

## Explicitly out of scope

Documentation/PRD corrections (M6), field-test re-run (M7), release (M8).