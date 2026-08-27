"""SQLite audit-log store: append-only transcripts, schema versioning, resume, crash safety.

M8 core (T8.1-T8.5). Implements the PRD §2.4 data model as SQLite tables with
WAL mode, per-artifact active-run locks, schema versioning, and crash-safe
append-only transcripts.

Usage::

    store = SQLiteStore(":memory:")
    store.initialize()
    run_id = store.create_run("art_001")
    store.append_event(run_id, event)
    store.mark_complete(run_id, report)
"""

from __future__ import annotations

import json
import sqlite3
import threading
from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from adversarial_debate.engine.debate_controller import DebateEvent
from adversarial_debate.engine.synthesis import SynthesisReport
from adversarial_debate.ids import deterministic_id

_SCHEMA_VERSION = 1

_SQL_CREATE_TABLES = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER NOT NULL,
    applied_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS artifacts (
    id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    source_uri TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS debate_runs (
    id TEXT PRIMARY KEY,
    artifact_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    resumed_from INTEGER,
    completed_at TEXT,
    FOREIGN KEY (artifact_id) REFERENCES artifacts(id)
);

CREATE TABLE IF NOT EXISTS transcript_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    round_index INTEGER NOT NULL,
    side TEXT,
    kind TEXT NOT NULL,
    content TEXT,
    degraded INTEGER NOT NULL DEFAULT 0,
    error TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (run_id) REFERENCES debate_runs(id)
);

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    artifact_id TEXT NOT NULL,
    side TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'isolated',
    error TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES debate_runs(id)
);

CREATE TABLE IF NOT EXISTS reviews (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    confidence REAL NOT NULL DEFAULT 0.0,
    committed_at TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (run_id) REFERENCES debate_runs(id)
);

CREATE TABLE IF NOT EXISTS claims (
    id TEXT PRIMARY KEY,
    review_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    text TEXT NOT NULL,
    severity TEXT NOT NULL,
    evidence_refs TEXT NOT NULL DEFAULT '[]',
    status TEXT NOT NULL DEFAULT 'open',
    FOREIGN KEY (review_id) REFERENCES reviews(id),
    FOREIGN KEY (run_id) REFERENCES debate_runs(id)
);

CREATE TABLE IF NOT EXISTS concessions (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    by_side TEXT NOT NULL,
    round_number INTEGER NOT NULL,
    rationale TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (run_id) REFERENCES debate_runs(id)
);

CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    artifact_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    verdict TEXT NOT NULL,
    convergence_score REAL NOT NULL,
    resolved_count INTEGER NOT NULL,
    total_claims INTEGER NOT NULL,
    report_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    partial INTEGER NOT NULL DEFAULT 0,
    partial_reason TEXT,
    FOREIGN KEY (run_id) REFERENCES debate_runs(id),
    FOREIGN KEY (artifact_id) REFERENCES artifacts(id)
);
"""


class StoreError(Exception):
    """Raised on store-level errors (schema mismatch, concurrent run, etc.)."""


class SQLiteStore:
    """Append-only SQLite store for debate transcripts.

    Thread-safe via per-connection lock. WAL mode for concurrent reads.
    """

    def __init__(self, db_path: str | Path) -> None:
        """Initialize store with path to SQLite database."""
        self._db_path = str(db_path)
        self._lock = threading.Lock()
        self._conn: sqlite3.Connection | None = None

    # ── lifecycle ──────────────────────────────────────────────────────────

    def initialize(self) -> None:
        """Create tables and set schema version if not already initialized."""
        with self._connect() as conn:
            conn.executescript(_SQL_CREATE_TABLES)
            row = conn.execute(
                "SELECT version FROM schema_version ORDER BY rowid DESC LIMIT 1"
            ).fetchone()
            if row is None:
                conn.execute(
                    "INSERT INTO schema_version (version) VALUES (?)",
                    (_SCHEMA_VERSION,),
                )
            elif row[0] > _SCHEMA_VERSION:
                msg = (
                    f"database schema version {row[0]} is newer than "
                    f"supported version {_SCHEMA_VERSION} — "
                    f"upgrade adversarial-debate to read this database"
                )
                raise StoreError(msg)

    @property
    def schema_version(self) -> int:
        """Current schema version in the database."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT version FROM schema_version ORDER BY rowid DESC LIMIT 1"
            ).fetchone()
            return row[0] if row else 0

    def close(self) -> None:
        """Close the database connection."""
        with self._lock:
            if self._conn is not None:
                self._conn.close()
                self._conn = None

    # ── run management ─────────────────────────────────────────────────────

    def create_run(
        self,
        artifact_id: str,
        run_id: str | None = None,
        resumed_from: int | None = None,
    ) -> str:
        """Create a new debate run, returning the run id.

        Raises ``StoreError`` if an active run already exists for this artifact.
        """
        now = _now()
        run_id = run_id or deterministic_id("run", f"{artifact_id}_{now}")

        with self._connect() as conn:
            existing = conn.execute(
                "SELECT id, status FROM debate_runs WHERE artifact_id = ? AND status = 'active'",
                (artifact_id,),
            ).fetchone()
            if existing is not None:
                msg = (
                    f"artifact {artifact_id} already has an active run "
                    f"({existing[0]}) — complete or cancel it first"
                )
                raise StoreError(msg)

            sql = (
                "INSERT OR IGNORE INTO artifacts "
                "(id, domain, source_uri, content_hash, created_at) "
            )
            conn.execute(
                sql + "VALUES (?, ?, ?, ?, ?)",
                (artifact_id, "unknown", artifact_id, "0" * 64, now),
            )
            conn.execute(
                "INSERT INTO debate_runs (id, artifact_id, created_at, status, resumed_from) "
                "VALUES (?, ?, ?, 'active', ?)",
                (run_id, artifact_id, now, resumed_from),
            )
        return run_id

    def get_active_run(self, artifact_id: str) -> str | None:
        """Return the active run id for an artifact, or None."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id FROM debate_runs WHERE artifact_id = ? AND status = 'active'",
                (artifact_id,),
            ).fetchone()
            return row[0] if row else None

    def mark_complete(
        self,
        run_id: str,
        report: SynthesisReport | None = None,
        partial: bool = False,
        partial_reason: str | None = None,
    ) -> None:
        """Mark a run as complete and optionally store the report."""
        now = _now()
        with self._connect() as conn:
            conn.execute(
                "UPDATE debate_runs SET status = 'completed', completed_at = ? WHERE id = ?",
                (now, run_id),
            )
            if report is not None:
                conn.execute(
                    "INSERT INTO reports "
                    "(id, run_id, artifact_id, kind, verdict, convergence_score, "
                    "resolved_count, total_claims, report_json, partial, partial_reason) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        f"report_{run_id}",
                        run_id,
                        report.artifact_id,
                        report.kind,
                        report.verdict,
                        report.convergence_score,
                        report.resolved_count,
                        report.total_claims,
                        _report_to_json(report),
                        1 if partial else 0,
                        partial_reason,
                    ),
                )

    def get_run_status(self, run_id: str) -> dict[str, Any] | None:
        """Get run status info."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, artifact_id, status, resumed_from, completed_at "
                "FROM debate_runs WHERE id = ?",
                (run_id,),
            ).fetchone()
            if row is None:
                return None
            return {
                "id": row[0],
                "artifact_id": row[1],
                "status": row[2],
                "resumed_from": row[3],
                "completed_at": row[4],
            }

    def resume_from(self, run_id: str) -> int | None:
        """Get the last completed round for a run, or None if not resumable."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT MAX(round_index) FROM transcript_events WHERE run_id = ?",
                (run_id,),
            ).fetchone()
            max_round = row[0] if row else None
            if max_round is None:
                return None
            return int(max_round) + 1

    # ── event storage ──────────────────────────────────────────────────────

    def append_event(self, run_id: str, event: DebateEvent) -> int:
        """Append a debate event to the transcript. Returns the sequence number."""
        with self._connect() as conn:
            seq = self._next_sequence(conn, run_id)
            conn.execute(
                "INSERT INTO transcript_events "
                "(run_id, sequence, round_index, side, kind, content, degraded, error) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    run_id,
                    seq,
                    event.round_index,
                    event.side,
                    event.kind,
                    event.message.content if event.message else None,
                    1 if event.degraded else 0,
                    event.error,
                ),
            )
            return seq

    def append_events(self, run_id: str, events: list[DebateEvent]) -> list[int]:
        """Append multiple events atomically. Returns list of sequence numbers."""
        with self._connect() as conn:
            seqs: list[int] = []
            for event in events:
                seq = self._next_sequence(conn, run_id)
                seqs.append(seq)
                conn.execute(
                    "INSERT INTO transcript_events "
                    "(run_id, sequence, round_index, side, kind, content, degraded, error) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        run_id,
                        seq,
                        event.round_index,
                        event.side,
                        event.kind,
                        event.message.content if event.message else None,
                        1 if event.degraded else 0,
                        event.error,
                    ),
                )
            return seqs

    def get_events(self, run_id: str) -> list[dict[str, Any]]:
        """Get all events for a run in sequence order."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT sequence, round_index, side, kind, content, degraded, error "
                "FROM transcript_events WHERE run_id = ? ORDER BY sequence",
                (run_id,),
            ).fetchall()
            return [
                {
                    "sequence": r[0],
                    "round_index": r[1],
                    "side": r[2],
                    "kind": r[3],
                    "content": r[4],
                    "degraded": bool(r[5]),
                    "error": r[6],
                }
                for r in rows
            ]

    def get_last_sequence(self, run_id: str) -> int:
        """Get the last sequence number for a run (0 if empty)."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT MAX(sequence) FROM transcript_events WHERE run_id = ?",
                (run_id,),
            ).fetchone()
            return row[0] if row[0] is not None else 0

    def get_report(self, run_id: str) -> dict[str, Any] | None:
        """Get the stored report for a completed run."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT report_json, kind, verdict, convergence_score, "
                "resolved_count, total_claims, partial, partial_reason "
                "FROM reports WHERE run_id = ? ORDER BY created_at DESC LIMIT 1",
                (run_id,),
            ).fetchone()
            if row is None:
                return None
            return {
                "report_json": row[0],
                "kind": row[1],
                "verdict": row[2],
                "convergence_score": row[3],
                "resolved_count": row[4],
                "total_claims": row[5],
                "partial": bool(row[6]),
                "partial_reason": row[7],
            }

    # ── sequence integrity ─────────────────────────────────────────────────

    def check_sequence_integrity(self, run_id: str) -> list[int]:
        """Check for gaps in sequence numbers. Returns missing sequence numbers."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT sequence FROM transcript_events WHERE run_id = ? ORDER BY sequence",
                (run_id,),
            ).fetchall()
            seqs = [r[0] for r in rows]
            if not seqs:
                return []
            expected = list(range(1, seqs[-1] + 1))
            return [s for s in expected if s not in seqs]

    # ── internal helpers ───────────────────────────────────────────────────

    @contextmanager
    def _connect(self) -> Generator[sqlite3.Connection, None, None]:
        """Get a thread-safe connection."""
        with self._lock:
            if self._conn is None:
                self._conn = sqlite3.connect(self._db_path)
                self._conn.execute("PRAGMA journal_mode=WAL")
                self._conn.execute("PRAGMA foreign_keys=ON")
                self._conn.isolation_level = None  # autocommit
            yield self._conn

    def _next_sequence(self, conn: sqlite3.Connection, run_id: str) -> int:
        """Get the next monotonic sequence number for a run."""
        row = conn.execute(
            "SELECT COALESCE(MAX(sequence), 0) + 1 FROM transcript_events WHERE run_id = ?",
            (run_id,),
        ).fetchone()
        return int(row[0])


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _report_to_json(report: SynthesisReport) -> str:
    """Serialize a SynthesisReport to JSON for storage."""
    return json.dumps(
        {
            "kind": report.kind,
            "artifact_id": report.artifact_id,
            "verdict": report.verdict,
            "convergence_score": report.convergence_score,
            "resolved_count": report.resolved_count,
            "total_claims": report.total_claims,
            "strongest_a": list(report.strongest_a),
            "strongest_b": list(report.strongest_b),
            "resolved": [
                {
                    "claim_id": r.claim_id,
                    "claim_text": r.claim_text,
                    "severity": r.severity,
                    "conceded_by": r.conceded_by,
                    "rationale": r.rationale,
                }
                for r in report.resolved
            ],
            "unresolved": [
                {
                    "claim_ids": u.claim_ids,
                    "position_a": u.position_a,
                    "position_b": u.position_b,
                    "severity": u.severity,
                    "would_resolve_if": u.would_resolve_if,
                }
                for u in report.unresolved
            ],
            "flags": {
                "theater": report.flags.theater,
                "capitulation_cascade": report.flags.capitulation_cascade,
                "degraded_rounds": list(report.flags.degraded_rounds),
            },
        },
        sort_keys=True,
    )


__all__ = [
    "SQLiteStore",
    "StoreError",
]
