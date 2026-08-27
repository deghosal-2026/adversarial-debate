"""SQLite store tests (M8: T8.1-T8.5, WBS M8 exit gate).

Tests cover:
  - SQLiteStore: create tables, run management, event storage, schema versioning
  - Concurrent-run lock: second run rejected
  - Resume: load last completed round, continue
  - Budget-exhaustion partial report
  - Crash safety: sequence integrity, reopen+resume
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from adversarial_debate.engine.debate_controller import DebateEvent
from adversarial_debate.engine.synthesis import (
    HeaderBlock,
    ReportFlags,
    SynthesisReport,
    UnresolvedEntry,
)
from adversarial_debate.schemas.debate import DebateMessage
from adversarial_debate.store.store import SQLiteStore, StoreError

NOW = datetime(2026, 8, 25, 12, 0, tzinfo=UTC)


@pytest.fixture
def store() -> SQLiteStore:
    s = SQLiteStore(":memory:")
    s.initialize()
    return s


def _make_event(
    round_index: int = 1, side: str = "A", kind: str = "defense", content: str = ""
) -> DebateEvent:
    msg: DebateMessage | None = None
    if content:
        msg = DebateMessage(
            id=f"msg_{side}_r{round_index}",
            side=side,  # type: ignore[arg-type]
            kind="defense",
            content=content,
        )
    return DebateEvent(
        round_index=round_index,
        side=side,  # type: ignore[arg-type]
        kind=kind,  # type: ignore[arg-type]
        message=msg,
        timestamp=NOW,
    )


def _make_report(artifact_id: str = "art_001", kind: str = "verdict") -> SynthesisReport:
    return SynthesisReport(
        kind=kind,  # type: ignore[arg-type]
        artifact_id=artifact_id,
        header=HeaderBlock(),
        verdict="Verdict reached.",
        strongest_a=["[high] Issue A"],
        strongest_b=["[medium] Issue B"],
        resolved=[],
        unresolved=[
            UnresolvedEntry(
                claim_ids=["cl_001"],
                position_a="Side A position",
                position_b="Side B position",
                severity="high",
                would_resolve_if="Need more evidence",
            )
        ],
        flags=ReportFlags(),
        convergence_score=0.5,
        total_claims=2,
        resolved_count=1,
    )


# ── T8.1 (#35) SQLiteStore ───────────────────────────────────────────────────


class TestSQLiteStore:
    def test_initialize_creates_tables(self, store: SQLiteStore) -> None:
        store.initialize()
        assert store.schema_version == 1

    def test_create_run_returns_id(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        assert run_id
        assert run_id.startswith("run_")

    def test_create_run_accepts_custom_id(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001", run_id="custom_run")
        assert run_id == "custom_run"

    def test_create_run_raises_on_duplicate_active(self, store: SQLiteStore) -> None:
        store.create_run("art_001")
        with pytest.raises(StoreError, match="already has an active run"):
            store.create_run("art_001")

    def test_create_run_allows_after_complete(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        store.mark_complete(run_id)
        run_id2 = store.create_run("art_001")
        assert run_id2 != run_id

    def test_get_active_run_returns_none_when_empty(self, store: SQLiteStore) -> None:
        assert store.get_active_run("art_001") is None

    def test_get_active_run_returns_id(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        assert store.get_active_run("art_001") == run_id

    def test_get_active_run_returns_none_after_complete(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        store.mark_complete(run_id)
        assert store.get_active_run("art_001") is None

    def test_get_run_status_returns_none_for_unknown(self, store: SQLiteStore) -> None:
        assert store.get_run_status("nonexistent") is None

    def test_get_run_status_returns_info(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        status = store.get_run_status(run_id)
        assert status is not None
        assert status["status"] == "active"
        assert status["artifact_id"] == "art_001"


# ── T8.2 (#36) Schema versioning ─────────────────────────────────────────────


class TestSchemaVersioning:
    def test_schema_version_is_one(self, store: SQLiteStore) -> None:
        assert store.schema_version == 1

    def test_initialize_is_idempotent(self, store: SQLiteStore) -> None:
        store.initialize()
        store.initialize()
        assert store.schema_version == 1

    def test_refuses_newer_schema(self) -> None:
        s = SQLiteStore(":memory:")
        s.initialize()
        with s._connect() as conn:
            conn.execute("UPDATE schema_version SET version = 99")
        with pytest.raises(StoreError, match="newer than"):
            s.initialize()


# ── T8.3 (#37) Resume ────────────────────────────────────────────────────────


class TestResume:
    def test_resume_from_returns_none_for_empty_run(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        assert store.resume_from(run_id) is None

    def test_resume_from_returns_next_round(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        event = _make_event(round_index=1, content="Round 1")
        store.append_event(run_id, event)
        next_round = store.resume_from(run_id)
        assert next_round == 2  # resume from round 2

    def test_resume_from_after_multiple_events(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        for i in range(1, 4):
            store.append_event(run_id, _make_event(round_index=i, content=f"Round {i}"))
        next_round = store.resume_from(run_id)
        assert next_round == 4

    def test_create_run_with_resumed_from(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001", resumed_from=2)
        status = store.get_run_status(run_id)
        assert status is not None
        assert status["resumed_from"] == 2


# ── T8.4 (#38) Budget & backoff ──────────────────────────────────────────────


class TestBudgetExhaustion:
    def test_mark_complete_with_partial_report(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        report = _make_report()
        store.mark_complete(run_id, report=report, partial=True, partial_reason="budget_exhausted")
        stored = store.get_report(run_id)
        assert stored is not None
        assert stored["partial"] is True
        assert stored["partial_reason"] == "budget_exhausted"

    def test_complete_run_without_report(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        store.mark_complete(run_id)
        assert store.get_report(run_id) is None

    def test_complete_run_with_report(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        report = _make_report(kind="disputed")
        store.mark_complete(run_id, report=report)
        stored = store.get_report(run_id)
        assert stored is not None
        assert stored["kind"] == "disputed"
        assert stored["convergence_score"] == 0.5


# ── Event storage ─────────────────────────────────────────────────────────────


class TestEventStorage:
    def test_append_event_returns_sequence(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        seq = store.append_event(run_id, _make_event(content="test"))
        assert seq == 1

    def test_append_events_sequential(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        seqs = store.append_events(
            run_id,
            [
                _make_event(content="First"),
                _make_event(content="Second"),
            ],
        )
        assert seqs == [1, 2]

    def test_get_events_returns_in_order(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        store.append_events(
            run_id,
            [
                _make_event(round_index=1, content="First"),
                _make_event(round_index=2, content="Second"),
            ],
        )
        events = store.get_events(run_id)
        assert len(events) == 2
        assert events[0]["content"] == "First"
        assert events[1]["content"] == "Second"
        assert events[0]["sequence"] == 1
        assert events[1]["sequence"] == 2

    def test_get_events_empty_run(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        assert store.get_events(run_id) == []

    def test_get_last_sequence_zero_for_empty(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        assert store.get_last_sequence(run_id) == 0

    def test_get_last_sequence_after_events(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        store.append_events(
            run_id,
            [
                _make_event(content="A"),
                _make_event(content="B"),
                _make_event(content="C"),
            ],
        )
        assert store.get_last_sequence(run_id) == 3

    def test_degraded_event_stored(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        event = DebateEvent(round_index=1, side="A", kind="defense", degraded=True)
        store.append_event(run_id, event)
        events = store.get_events(run_id)
        assert events[0]["degraded"] is True

    def test_error_event_stored(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        event = DebateEvent(round_index=1, side="A", kind="system", error="timeout")
        store.append_event(run_id, event)
        events = store.get_events(run_id)
        assert events[0]["error"] == "timeout"


# ── T8.5 (#39) Crash safety ──────────────────────────────────────────────────


class TestCrashSafety:
    def test_sequence_integrity_no_gaps(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        store.append_events(
            run_id,
            [
                _make_event(content="A"),
                _make_event(content="B"),
                _make_event(content="C"),
            ],
        )
        assert store.check_sequence_integrity(run_id) == []

    def test_sequence_integrity_empty_run(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        assert store.check_sequence_integrity(run_id) == []

    def test_reopen_and_resume_produces_same_state(self, tmp_path: Path) -> None:
        """Property test: reopen+resume produces same data as uninterrupted run."""
        db_path = str(tmp_path / "test.db")
        s1 = SQLiteStore(db_path)
        s1.initialize()
        run_id = s1.create_run("art_001")
        s1.append_events(
            run_id,
            [
                _make_event(round_index=1, content="Round 1"),
                _make_event(round_index=2, content="Round 2"),
            ],
        )
        state1 = s1.get_events(run_id)
        s1.close()

        s2 = SQLiteStore(db_path)
        s2.initialize()
        state2 = s2.get_events(run_id)
        s2.close()

        assert state1 == state2

    def test_concurrent_run_lock_second_rejected(self, store: SQLiteStore) -> None:
        store.create_run("art_001")
        with pytest.raises(StoreError, match="already has an active run"):
            store.create_run("art_001")

    def test_report_json_stored_properly(self, store: SQLiteStore) -> None:
        run_id = store.create_run("art_001")
        report = _make_report()
        store.mark_complete(run_id, report=report)
        stored = store.get_report(run_id)
        assert stored is not None
        parsed = json.loads(stored["report_json"])
        assert parsed["kind"] == "verdict"
        assert parsed["convergence_score"] == 0.5

    def test_budget_exhaustion_labeled_partial(self, store: SQLiteStore) -> None:
        """Budget-exhaustion scenario yields labeled partial report."""
        run_id = store.create_run("art_001")
        report = _make_report()

        store.append_events(
            run_id,
            [
                _make_event(round_index=1, content="Round 1"),
            ],
        )
        store.mark_complete(run_id, report=report, partial=True, partial_reason="budget_exhausted")

        stored = store.get_report(run_id)
        assert stored is not None
        assert stored["partial"] is True
        assert stored["partial_reason"] == "budget_exhausted"
        report_data = json.loads(stored["report_json"])
        assert report_data["convergence_score"] == 0.5
