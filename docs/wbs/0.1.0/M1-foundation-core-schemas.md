# M1 — Foundation & Core Schemas

> Goal: repo scaffold, package layout, all v0.1.0 Pydantic schemas, TOML config model, and CI quality gates. Everything downstream imports from here. Part of [index](index.md).

## PRD coupling

- [05-features](../../design/prd/05-features.md): F3 (structured debate schema), F8 (config registry shape), F9 (transcript schema)
- [02-architecture §2.4 data model](../../design/prd/02-architecture.md): canonical entity list — this milestone implements it verbatim
- [11-glossary](../../design/prd/11-glossary.md): term definitions are the naming source of truth

## Dependencies

Upstream: none. Downstream: every milestone.

## Workstreams & tasks

### WS 1.a — Repo & tooling

- [x] T1.1 (#1) Repo + package scaffold: `src/adversarial_debate/{schemas,providers,engine,adapters,store,cli}` layout, pyproject (hatch), Makefile, uv lock, ruff+mypy strict config, pre-commit
- [x] T1.2 (#2) CI pipeline: lint + typecheck + pytest + coverage gate (≥95%, fail under) + hermetic-only guard (no network in tests)

### WS 1.b — Core schemas

- [x] T1.3 (#3) Artifact schemas: `ReviewArtifact`, `ContentBlock`, `RubricHint`, `DetectedLanguage` — field-for-field per PRD §2.4 incl. `content_hash`, `detected_language`, `classification_tag`
- [x] T1.4 (#4) Review schemas: `ReviewerSession` (side A|B, status enum `isolated|revealed|debating|done|error`), `Review` (claims[], risks[], confidence, committed_at, immutable-after-commit flag)
- [x] T1.5 (#5) Debate schemas: `Claim` (status lifecycle `open→conceded|upheld|resolved`), `Objection` (target_claim_id, round, evidence_refs[]), `Concession` (by_side, round, rationale), `UnresolvedPoint` (position_a/b, would_resolve_if), `DebateRound`, `Outcome` (kind verdict|disputed, convergence_score)
- [x] T1.6 (#6) Config model + loader: providers (slots A/B, provider type, base_url/model/key-env), rounds, budgets, retention stubs, seed; `advdeb.toml.example`; validation errors are human-readable

### WS 1.c — Utilities

- [x] T1.7 (#7) ID/hash utilities: artifact content hash (SHA-256), monotonic sequence numbers per artifact, deterministic IDs

## Acceptance criteria / exit gate

- All schemas round-trip JSON ↔ Pydantic with strict validation tests
- Malformed inputs produce readable validation errors (no raw tracebacks)
- CI green on GitHub Actions; coverage ≥95% on `schemas/` and `config/`
- Schema docstrings cite the PRD section each entity implements

## Explicitly out of scope

Provider transports (M2), SQLite persistence (M8), CLI (M9).
