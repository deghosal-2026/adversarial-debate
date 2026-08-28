# M4 — Test Corrections & Audits

> Goal: fix tautological tests that cannot catch regressions, add isolation audit test, and add ground-truth false-positive/false-negative rate and blinded human scoring. This milestone ensures the test suite actually validates what it claims to and adds critical integrity guarantees. Part of [index](index.md).

## PRD coupling

- [06-security-baseline §6.3 isolation](../../design/prd/06-security-baseline.md): adversarial isolation audit test
- [07-success-metrics §7.6 methodology](../../design/prd/07-success-metrics.md): ground-truth FP/FN rates, blinded scoring

## Dependencies

Upstream: M1, M2, M3. Downstream: M5, M6, M7, M8.

## Workstreams & tasks

### WS 4.a — Fix tautological tests

- [x] T4.1 (#93) `test_transcript_export_jsonl`: replace `assert out_path.is_file() or not out_path.is_file()` with concrete assertions on path, existence, and parseable JSONL
- [x] T4.2 (#94) `test_unaddressed_objection_emits_event`: assert event has `kind == "system"` and `degraded=True` instead of just `len(state.events) >= 1`
- [x] T4.3 (#96) `test_init_missing_path_is_handled`: assert exact exit code and file existence instead of accepting both OK and USAGE
- [x] T4.4 (#97) `test_concessions_are_recorded`: assert concrete expected concession count (`>= 1`) instead of `assert len(state.concessions) >= 0`

### WS 4.b — Add isolation audit

- [x] T4.5 (#76) Add adversarial isolation audit test: inject known secret string into A's output, verify B's transcript does not contain it
- [ ] T4.6 (#73) Canary token test for runtime isolation verification (feature request — deferred to M5 scope)

### WS 4.c — Ground-truth methodology

- [ ] T4.7 (#75) Add false-positive rate, false-negative rate, and blinded human scoring to ground-truth verification (deferred to M5 scope)

## Documents, plans & tests to update

- `tests/test_cli.py` — fix `test_transcript_export_jsonl`, `test_init_missing_path_is_handled`
- `tests/test_debate_controller.py` — fix `test_unaddressed_objection_emits_event`, `test_concessions_are_recorded`
- `tests/test_isolation.py` — new file: adversarial isolation audit test + canary token test
- `src/adversarial_debate/engine/evidence.py` — add `_detect_leak` for canary isolation check
- `src/adversarial_debate/engine/debate_controller.py` — inject canary after A's review
- `docs/field-test/v0.1.0/FIELD_TEST_REPORT_full_corpus.md` — add FP/FN rates, blinded scoring section
- `scripts/06_ground_truth.py` — add FP/FN rate computation, blinded scoring export
- `SECURITY.md` — add isolation audit procedure

## Acceptance criteria / exit gate

- [x] All 5 of 7 issues closed with passing tests (T4.6 deferred to M5, T4.7 deferred to M5)
- [x] Ruff clean, mypy strict clean (pre-existing errors only in providers)
- [x] 436 tests passing (all tests except pre-existing network-dependent provider tests)
- [x] Isolation audit test runs in CI on every PR
- [x] Code review completed on all changes
- [x] Committed and pushed to `rel-0.2.0` (8946fad)

## Explicitly out of scope

Engine bugs (M1), transport/script fixes (M2), CLI fixes (M3), field test data integrity (M5), documentation (M6).