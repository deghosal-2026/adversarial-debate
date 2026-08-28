# M3 — CLI & Adapter Integrations

> Goal: fix CLI output paths, adapter registration, metadata extraction guard, and diff parser binary-line handling. These are user-facing fixes that affect the correctness of CLI output and adapter behavior. Part of [index](index.md).

## PRD coupling

- [02-architecture §2.4](../../design/prd/02-architecture.md): adapter framework, normalizer registry
- [05-features F4](../../design/prd/05-features.md): CLI commands and output paths

## Dependencies

Upstream: M1, M2. Downstream: M4, M5, M6, M7, M8.

## Workstreams & tasks

### WS 3.a — CLI fixes

- [ ] T3.1 (#82) `cmd_report`: merge partial metadata into stored flags instead of overwriting — preserves theater/capitulation/degraded-round warnings
- [ ] T3.2 (#83) `cmd_transcript`: default output path relative to selected store database instead of CWD

### WS 3.b — Adapter integration fixes

- [ ] T3.3 (#84) `PrMetadataExtractor.extract`: add `gh` availability guard for PR metadata fetch — consistent with `_gh_diff()` behavior
- [ ] T3.4 (#85) Built-in `pr_review` adapter: ensure auto-registration on first registry access per lazy-load contract
- [ ] T3.5 (#86) Diff parser: handle whitespace-prefixed `Binary files ... differ` metadata lines — normalize leading whitespace before binary-note check

## Documents, plans & tests to update

- `src/adversarial_debate/cli/cli.py` — `cmd_report` flags merge, `cmd_transcript` output path
- `src/adversarial_debate/adapters/pr_review/metadata.py` — `_extract_github` availability guard
- `src/adversarial_debate/adapters/__init__.py` — lazy-load import for `pr_review` adapter
- `src/adversarial_debate/adapters/pr_review/diff_parser.py` — whitespace-prefixed binary note handling
- `tests/test_cli.py` — add tests for flag merge, transcript output path, report flag preservation
- `tests/test_metadata.py` — add test for `gh` unavailable PR metadata extraction
- `tests/test_adapters.py` — add test for auto-registration of `pr_review` adapter
- `tests/test_diff_parser.py` — add test for indented binary notice lines

## Acceptance criteria / exit gate

- All 5 issues closed with passing tests
- Ruff clean, mypy strict clean, full test suite green
- Code review completed on all changes
- Committed and pushed to `rel-0.2.0`

## Explicitly out of scope

Engine bugs (M1), transport/script fixes (M2), test corrections (M4), field test data integrity (M5), documentation (M6).