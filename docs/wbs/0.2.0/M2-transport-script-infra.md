# M2 — Transport & Script Infrastructure

> Goal: fix provider transport layer, script-level bugs, dependency hygiene, and pricing infrastructure. These fixes ensure reliable API communication, correct cost accounting, and maintainable scripts. Part of [index](index.md).

## PRD coupling

- [06-security-baseline §6.4 reproducibility](../../design/prd/06-security-baseline.md): seeds, pricing, dependency management
- [10-cost-model](../../design/prd/10-cost-model.md): accurate cost estimation and reporting

## Dependencies

Upstream: M1. Downstream: M3, M4, M5, M6, M7, M8.

## Workstreams & tasks

### WS 2.a — Transport layer fixes

- [ ] T2.1 (#77) API key leak: strip query parameters from URL before including in error messages
- [ ] T2.2 (#81) `OpenAITransport._parse`: normalize list-shaped `message.content` payloads before parsing

### WS 2.b — Script infrastructure fixes

- [ ] T2.3 (#78) `ScriptedReviewer._load`: add warning when scenarios file is missing or malformed instead of silent empty results
- [ ] T2.4 (#79) O(n²) merge loop in `07_llm_judge.py`: use dict keyed by compound key instead of rebuilding list from scratch
- [ ] T2.5 (#92) `05_analyze.py`: build PR IDs from union of all model directories instead of first model only
- [ ] T2.6 (#95) Baseline pair files crash `04_run_debate` because `side_b` is null — handle baseline pairs gracefully
- [ ] T2.7 (#98) `07_llm_judge` resume: use composite key `(pr_id, pair, claim_id, claim_source)` instead of `claim_id` alone
- [ ] T2.8 (#99) `08_flakiness`: require `len(verdicts) == args.runs` before declaring a PR stable
- [ ] T2.9 (#100) `06_ground_truth`: export `claim_text` instead of `rationale` as the judged text for resolved rows
- [ ] T2.10 (#101) `test_validate_evidence_cross_check_content_blocks`: assert semantic correctness, not just type

### WS 2.c — Pricing and dependency fixes

- [ ] T2.11 (#63) `compute_cost`: fail closed (raise or warn) for unknown models instead of returning $0.00
- [ ] T2.12 (#80) Cost estimate: use model-aware pricing from `PRICING` dict instead of hardcoded `$0.002/PR`
- [ ] T2.13 (#64) `pyyaml`: remove from dev dependency group (redundant with runtime deps)

### WS 2.d — Code quality fixes

- [ ] T2.14 (#68) Resource leak: use context manager for `open()` in `scripts/07_llm_judge.py`
- [ ] T2.15 (#69) Double import of `re` in `scripts/05_analyze.py`: remove local imports, use module-level `re`
- [ ] T2.16 (#70) `scripts/08_flakiness.py`: refactor module-level `sys.path` modification + dynamic import into proper shared module

## Documents, plans & tests to update

- `src/adversarial_debate/providers/openai_transport.py` — URL sanitization, list-content normalization
- `src/adversarial_debate/providers/scripted_reviewer.py` — warning on missing/malformed scenarios
- `scripts/02_run_reviewer.py` — `compute_cost` fail-closed, model-aware estimate
- `scripts/05_analyze.py` — PR ID union, remove double `re` import
- `scripts/06_ground_truth.py` — export `claim_text` instead of `rationale`
- `scripts/07_llm_judge.py` — O(n²) fix, context manager, composite key resume
- `scripts/08_flakiness.py` — stability completeness check, refactor sys.path hack
- `scripts/04_run_debate.py` — baseline pair null `side_b` handling
- `pyproject.toml` — remove `pyyaml` from dev deps
- `tests/test_evidence.py` — fix `test_validate_evidence_cross_check_content_blocks`
- `tests/test_providers.py` — add transport parse tests for list-shaped content
- `tests/test_scripted_reviewer.py` — add tests for missing/malformed scenarios

## Acceptance criteria / exit gate

- All 16 issues closed with passing tests
- Ruff clean, mypy strict clean, full test suite green
- Code review completed on all changes
- Committed and pushed to `rel-0.2.0`

## Explicitly out of scope

CLI fixes (M3), test corrections and audits (M4), field test data integrity (M5), documentation (M6).