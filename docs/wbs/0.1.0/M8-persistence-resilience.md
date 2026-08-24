# M8 — Persistence & Resilience

> Goal: SQLite storage with append-only transcripts and schema versioning; resume interrupted debates; budget ceilings with honest partial reports; crash-safe by construction. Part of [index](index.md).

## PRD coupling

- [05-features](../../design/prd/05-features.md): F9 (SQLite persistence of full lineage)
- [06-security §6.5 operational failure modes](../../design/prd/06-security-baseline.md): provider outage → pause + resume; partial transcript integrity; rate-limit backoff + `incomplete: budget_exhausted` partial reports; per-artifact lock rejecting concurrent runs
- [14-schema-migration](../../design/prd/14-schema-migration.md): `schema_version` table, forward-only migrations, no destructive ops
- [02-architecture §2.2 Audit Log](../../design/prd/02-architecture.md): tamper-evident ordering

## Dependencies

Upstream: M7 (outputs to persist). Downstream: M9 (CLI drives store), M10 (sweeps rely on resume/budget).

## Workstreams & tasks

### WS 8.a — Store

- [ ] T8.1 SQLiteStore: tables per [PRD §2.4 data model](../../design/prd/02-architecture.md); WAL mode; append-only transcript rows with per-artifact monotonic sequence; unique per-artifact active-run lock (second run rejected with clear message)
- [ ] T8.2 Schema versioning: `schema_version` singleton table (value 1); migration runner skeleton (`advdeb migrate`) — forward-only, transactional, idempotent; refuses newer-than-supported DB ([14 §14.2](../../design/prd/14-schema-migration.md))

### WS 8.b — Resilience

- [ ] T8.3 Resume: on restart, load last completed round state; continue debate from there; resumed runs marked `resumed_from_round=k` in report header; resume of completed artifact is a no-op with message
- [ ] T8.4 Budget & backoff integration: wire M2 retries to a per-artifact token/cost budget; exhaustion at round k → stop + synthesize **partial** report labeled `incomplete: budget_exhausted` with rounds completed so far ([06 §6.5](../../design/prd/06-security-baseline.md))
- [ ] T8.5 Crash safety: kill -9 / SIGTERM mid-round leaves valid partial transcript (sequence-integrity test); reopen+resume produces identical continuation as uninterrupted run (property test); corruption attempts detected via sequence gaps

## Acceptance criteria / exit gate

- Crash/resume property tests pass across randomized kill points (≥20 seeds)
- Concurrent-run lock test: second process rejected with actionable message
- Budget-exhaustion scenario yields labeled partial report, not silence
- Coverage ≥95% on `store/`

## Explicitly out of scope

Postgres ([DD-03](../../design/prd/12-design-decisions.md) — v0.8); hash-chain tamper evidence (v0.2); remote storage.
