# 14 — Schema Migration & Transcript Continuity

> Sub-document of the [Design overview](../README.md). How SQLite transcripts survive schema changes across versions. Audit-trail continuity is a trust requirement — legal and compliance buyers need to know v0.3 can read v0.1 transcripts.

## 14.1 The problem

Every version adds fields: v0.2 adds `argument_type` to `Objection`; v0.3 adds `agent_count` to `Outcome`. Without a migration strategy, old transcripts become unreadable — and an audit trail that can't be read is no audit trail at all.

## 14.2 Strategy

| Layer | Mechanism |
|-------|-----------|
| **Schema versioning** | Every SQLite database has a `schema_version` table with a single row. The engine checks this on startup and refuses to run if the version is newer than it supports (fail-closed, never silent corruption). |
| **Migrations** | Forward-only migration scripts in `adversarial_debate/migrations/`. `advdeb migrate` runs all pending migrations. Each migration is idempotent and transactional. |
| **Transcript compatibility** | Old transcripts remain readable after migration — new fields are nullable with sensible defaults. A v0.3 engine reading a v0.1 transcript shows `argument_type: null` (unknown) rather than failing. |
| **Export stability** | JSONL export format is versioned (`export_format: "v1"`). Breaking changes to export format increment the version; old formats remain readable for 2 major releases. |

## 14.3 Migration lifecycle

```
v0.1.0 → schema_version 1
v0.2.0 → migration_001_to_002.sql  (adds argument_type, kill_criterion fields)
v0.3.0 → migration_002_to_003.sql  (adds agent_count, diversity_score)
```

**Rule:** no migration may destroy or alter existing data. Migrations add columns or tables only. Column removal requires a major version bump and explicit user opt-in (`advdeb migrate --major --accept-data-loss`).

## 14.4 What buyers need to hear

- "Your v0.1 transcripts are readable in v0.3 — new fields show as unknown, not as errors."
- "Migrations are forward-only and transactional. A failed migration rolls back; your data is never half-migrated."
- "Export format is versioned. Your JSONL exports from v0.1 are importable in v0.3 tooling."
