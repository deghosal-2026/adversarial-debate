# 25 — Data Retention & Deletion Policy

> Sub-document of the [Design overview](../README.md). Artifact and transcript lifecycle aligned with GDPR, CCPA, and enterprise data-governance requirements.

## 25.1 Data lifecycle

```
Artifact submitted
  │
  ├──► Normalized → ReviewArtifact (in memory + SQLite)
  │
  ├──► Debate runs → Transcript rows (SQLite, append-only)
  │
  ├──► Report generated → Verdict/Disagreement (SQLite + optional export)
  │
  ├──► Retention period (configurable, default: 90 days)
  │
  └──► Deletion (soft → hard)
```

## 25.2 Retention configuration

```toml
# advdeb.toml
[retention]
default_days = 90              # transcripts kept for 90 days after debate completes
artifact_content = true        # keep original artifact text in transcript (default)
auto_delete = false            # auto-delete expired transcripts (default: manual)
delete_action = "soft"         # soft (mark deleted) or hard (remove rows)

[retention.overrides]
domain.pr_review = 30          # code diffs: shorter retention
domain.legal_contracts = 365   # contracts: longer retention for audit
domain.healthcare = 2555       # 7 years (HIPAA-aligned, if partner deploys)
```

## 25.3 Deletion mechanics

| Mode | What happens | Recoverable |
|------|-------------|-------------|
| **Soft delete** (`advdeb delete <id>`) | Sets `deleted_at` timestamp; artifact excluded from reports and UI | Yes — `advdeb restore <id>` |
| **Hard delete** (`advdeb purge <id>`) | Removes all rows for that artifact from SQLite | No |
| **Bulk purge** (`advdeb purge --expired`) | Hard-deletes all artifacts past retention period | No |
| **Redact content** (`advdeb redact <id>`) | Replaces artifact content with `[REDACTED]`; keeps claim/concession structure | No (content gone, structure remains) |

**Rule:** hard delete and purge require `--confirm` flag. No accidental data loss.

## 25.4 GDPR / CCPA alignment

| Requirement | How we meet it |
|------------|----------------|
| **Right to erasure** | `advdeb purge <id>` removes all data for a specific artifact |
| **Data minimization** | Engine stores only what's needed: artifact content, reviews, debate transcript, report. No user PII unless artifact contains it. |
| **Purpose limitation** | Data is used only for debate and reporting. No secondary use (training, analytics) — ever. |
| **Data portability** | `advdeb export <id> --format jsonl` produces a complete, portable record |
| **Breach notification** | If transcript database is compromised, the Security Disclosure Policy (§17) applies — 48h acknowledgment, 30-day fix |
| **No cross-border transfer** | BYOM means artifacts go only to user-configured endpoints. The engine itself has no server — data stays where the user runs it. |

## 25.5 What the engine does NOT store

- **Model responses beyond the transcript** — no secondary logs, no training caches
- **User identity** — the engine doesn't authenticate users in v0.1; v0.5+ HTTP service logs API key hashes only
- **Telemetry** — none by default; opt-in only (see [06-security-baseline.md](06-security-baseline.md) §6.2)
- **Artifact metadata beyond what's in the diff/document** — no scraping of repo info, no author profiles

## 25.6 Partner-deployment data boundary (Tier 3)

For regulated verticals where a partner runs the engine on their infrastructure:

- The project never receives artifact content, transcripts, or reports
- The partner configures retention per their regulatory requirements
- Anonymized disagreement reports (structure only, no artifact content) may be contributed back to the fixture library — only if the partner explicitly redacts and submits
- The project's contribution is the engine + adapter skeleton, not data
