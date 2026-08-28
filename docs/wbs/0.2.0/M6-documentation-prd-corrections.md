# M6 — Documentation & PRD Corrections

> Goal: fix all documentation references to missing files and unimplemented features across PRDs, deployment guides, READMEs, and design docs. These are documentation bugs that mislead readers about the current state of the product. Part of [index](index.md).

## PRD coupling

- [02-architecture](../../design/prd/02-architecture.md): architecture document references
- [15-performance](../../design/prd/15-performance.md): performance claims vs shipped CLI
- [22-internationalization](../../design/prd/22-internationalization.md): i18n feature claims vs shipped behavior
- [23-enterprise-deployment](../../design/prd/23-enterprise-deployment.md): provider type examples
- [26-brand-guide](../../design/prd/26-brand-guide.md): design README delivery surfaces

## Dependencies

Upstream: M5. Downstream: M7, M8.

## Workstreams & tasks

### WS 6.a — Missing file references

- [x] T6.1 (#105) Architecture doc: add `docs/architecture/architecture-v0.1.0.md` or retarget all references to existing doc
- [x] T6.2 (#110) API reference: add `docs/reference/api.md` or remove from key-document lists

### WS 6.b — Unimplemented feature claims

- [x] T6.3 (#106) Performance PRD: move non-existent CLI flags (`--no-budget-limit`, `--batch`) and HTTP service claims to roadmap/future sections
- [x] T6.4 (#107) Enterprise deployment guide: rewrite provider config examples to use supported types (`openai_compatible` for Ollama/Azure)
- [x] T6.5 (#108) Internationalization PRD: mark i18n features as future work instead of v0.1.0 shipped
- [x] T6.6 (#109) Design README: mark FastAPI/React delivery surfaces as roadmap items, consistent with CLI/library-only implementation

## Documents, plans & tests to update

- `docs/architecture/architecture-v0.1.0.md` — create or retarget references
- `docs/architecture/README.md` — fix references to architecture doc
- `docs/design/prd/02-architecture.md` — fix reference to architecture doc
- `docs/design/prd/15-performance.md` — move non-existent CLI flags and HTTP service claims to roadmap
- `docs/design/prd/22-internationalization.md` — mark i18n as future work
- `docs/design/prd/23-enterprise-deployment.md` — fix provider config examples
- `docs/design/README.md` — mark FastAPI/React as roadmap items
- `docs/README.md` — fix reference to `api.md`
- `docs/reference/README.md` — fix reference to `api.md`
- `docs/reference/quickstart.md` — fix reference to architecture doc
- `README.md` — fix reference to architecture doc
- `SUPPORT.md` — fix reference to architecture doc
- `tests/test_docs.py` — new file: link-checker that verifies every referenced markdown target exists
- `tests/test_cli.py` — add parser-based test that every documented CLI flag exists in `build_parser()`

## Acceptance criteria / exit gate

- [x] All 6 issues closed with passing tests
- [x] Every referenced markdown target exists in-tree
- [x] Every documented CLI flag exists in `build_parser()`
- [x] Ruff clean, mypy strict clean, full test suite green
- [x] Code review completed on all changes
- [x] Committed and pushed to `rel-0.2.0` (b775cd3)

## Explicitly out of scope

Field-test re-run (M7), release readiness (M8).