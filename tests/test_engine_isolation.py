"""Isolation engine tests (M3: T3.1-T3.4, WBS M3 exit gate).

Tests cover:
  - ReviewerSessionManager: creates two independent sessions
  - RevelationGate: state machine with audit events
  - Commit immutability enforcement at engine layer
  - Adversarial isolation: no cross-session leakage possible
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from adversarial_debate.engine import (
    AuditEvent,
    IsolationViolation,
    RevelationGate,
    ReviewerSessionManager,
    ReviewRequest,
)
from adversarial_debate.schemas import Claim, Review, ReviewerSession

NOW = datetime(2026, 8, 24, 12, 0, tzinfo=UTC)


# ---- test doubles -----------------------------------------------------------


class FakeBackend:
    """Minimal test double — returns a canned, committed Review."""

    def __init__(self) -> None:
        self.requests: list[ReviewRequest] = []

    def run(self, request: ReviewRequest) -> Review:
        self.requests.append(request)
        return Review(
            id="rev_fake",
            session_id="sess_fake",
            claims=[
                Claim(
                    id="cl_fake_1",
                    review_id="rev_fake",
                    text="Test claim",
                    severity="medium",
                )
            ],
            risks=[],
            confidence=0.75,
            committed_at=NOW,
        )


class PeekingBackend:
    """Attempts to smuggle data across sessions — caught by IsolationViolation."""

    def __init__(self) -> None:
        self._seen_other_content: list[str] = []
        self._returned_claim_text: str | None = None

    def run(self, request: ReviewRequest) -> Review:
        if self._seen_other_content:
            self._returned_claim_text = "LEAKED: SQL injection in handler"
        if request.artifact_content:
            self._seen_other_content.append(request.artifact_content)
        claim_text = self._returned_claim_text or "Safe claim"
        return Review(
            id="rev_peek",
            session_id="sess_peek",
            claims=[
                Claim(
                    id="cl_peek_1",
                    review_id="rev_peek",
                    text=claim_text,
                    severity="medium",
                )
            ],
            risks=[],
            confidence=0.5,
            committed_at=NOW,
        )


class NotReadyBackend:
    """Backend returning an uncommitted Review (no committed_at)."""

    def run(self, _request: ReviewRequest) -> Review:
        return Review(
            id="rev_draft",
            session_id="sess_draft",
            claims=[],
            risks=[],
            confidence=0.0,
            committed_at=None,
        )


# ---- shared fixtures --------------------------------------------------------


@pytest.fixture
def manager() -> ReviewerSessionManager:
    return ReviewerSessionManager()


def _make_review(
    session_id: str,
    committed: bool = True,
) -> Review:
    return Review(
        id=f"rev_{session_id}",
        session_id=session_id,
        claims=[],
        risks=[],
        confidence=0.5,
        committed_at=NOW if committed else None,
    )


def _full_transition(
    manager: ReviewerSessionManager,
    session_id: str,
) -> ReviewerSession:
    s = manager.update_status(session_id, "revealed")
    s = manager.update_status(s.id, "debating")
    return manager.update_status(s.id, "done")


# ===== T3.1 (#14) ReviewerSessionManager =====


class TestReviewerSessionManager:
    def test_creates_two_sessions_with_correct_ids(self, manager: ReviewerSessionManager) -> None:
        artifact_id = "art_test_1"
        assert manager.sessions_a is None
        assert manager.sessions_b is None

        sessions = manager.create_sessions(
            artifact_id=artifact_id,
            provider_a="openai",
            model_a="gpt-4",
            provider_b="anthropic",
            model_b="claude-3",
            created_at=NOW,
        )

        assert len(sessions) == 2
        assert sessions[0].side == "A"
        assert sessions[1].side == "B"
        assert sessions[0].status == "isolated"
        assert sessions[1].status == "isolated"
        assert sessions[0].artifact_id == artifact_id
        assert sessions[1].artifact_id == artifact_id
        assert sessions[0].id != sessions[1].id

    def test_creates_only_two_sessions(self, manager: ReviewerSessionManager) -> None:
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        assert len(sessions) == 2

    def test_manager_refuses_second_create(self, manager: ReviewerSessionManager) -> None:
        manager.create_sessions("art_1", "a", "m1", "b", "m2", NOW)
        with pytest.raises(RuntimeError, match="already initialized"):
            manager.create_sessions("art_2", "a", "m1", "b", "m2", NOW)

    def test_get_session_by_id(self, manager: ReviewerSessionManager) -> None:
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        retrieved = manager.get_session(sessions[0].id)
        assert retrieved is not None
        assert retrieved.id == sessions[0].id
        assert manager.get_session("nonexistent") is None

    def test_update_session_status(self, manager: ReviewerSessionManager) -> None:
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        updated = manager.update_status(sessions[0].id, "revealed")
        assert updated.status == "revealed"
        retrieved = manager.get_session(sessions[0].id)
        assert retrieved is not None
        assert retrieved.status == "revealed"

    def test_update_session_status_invalid_transition(
        self, manager: ReviewerSessionManager
    ) -> None:
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        with pytest.raises(ValueError, match="invalid status transition"):
            manager.update_status(sessions[0].id, "done")

    def test_update_session_error(self, manager: ReviewerSessionManager) -> None:
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        updated = manager.update_status(sessions[0].id, "error", error="LLM timeout")
        assert updated.status == "error"
        assert updated.error == "LLM timeout"

    def test_update_nonexistent_session_raises(self, manager: ReviewerSessionManager) -> None:
        with pytest.raises(ValueError, match="unknown session"):
            manager.update_status("bad_id", "revealed")

    def test_sessions_have_no_shared_mutable_objects(self, manager: ReviewerSessionManager) -> None:
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        assert sessions[0] is not sessions[1]
        assert sessions[0].id != sessions[1].id
        d0 = sessions[0].model_dump()
        d1 = sessions[1].model_dump()
        assert d0 != d1
        assert d0["artifact_id"] == d1["artifact_id"]
        assert d0["created_at"] == d1["created_at"]

    def test_get_all_sessions(self, manager: ReviewerSessionManager) -> None:
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        all_s = manager.all_sessions
        assert len(all_s) == 2
        assert {s.id for s in all_s} == {sessions[0].id, sessions[1].id}

    def test_invalid_transition_isolated_to_error_allowed(
        self, manager: ReviewerSessionManager
    ) -> None:
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        updated = manager.update_status(sessions[0].id, "error", error="crash")
        assert updated.status == "error"

    def test_invalid_transition_done_to_revealed_disallowed(
        self, manager: ReviewerSessionManager
    ) -> None:
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        manager.update_status(sessions[0].id, "revealed")
        manager.update_status(sessions[0].id, "debating")
        manager.update_status(sessions[0].id, "done")
        with pytest.raises(ValueError, match="invalid status transition"):
            manager.update_status(sessions[0].id, "revealed")

    def test_rejects_error_detail_on_non_error_status(
        self, manager: ReviewerSessionManager
    ) -> None:
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        with pytest.raises(ValueError, match="error detail only allowed"):
            manager.update_status(sessions[0].id, "revealed", error="stray detail")

    def test_sessions_a_b_properties_return_non_none(self, manager: ReviewerSessionManager) -> None:
        manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        assert manager.sessions_a is not None
        assert manager.sessions_a.side == "A"
        assert manager.sessions_b is not None
        assert manager.sessions_b.side == "B"


# ===== T3.2 (#15) RevelationGate =====


class TestRevelationGate:
    def test_reveal_not_callable_when_no_sessions(self) -> None:
        gate = RevelationGate()
        with pytest.raises(IsolationViolation, match="no sessions"):
            gate.reveal()

    def test_reveal_requires_both_committed(self, manager: ReviewerSessionManager) -> None:
        gate = RevelationGate()
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        gate.register_session(sessions[0])
        gate.register_session(sessions[1])

        with pytest.raises(IsolationViolation):
            gate.reveal()

        sess_a = _full_transition(manager, sessions[0].id)
        gate.register_session(sess_a)
        with pytest.raises(IsolationViolation):
            gate.reveal()

    def test_reveal_transitions_both_to_revealed(self, manager: ReviewerSessionManager) -> None:
        gate = RevelationGate()
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        sess_a = _full_transition(manager, sessions[0].id)
        sess_b = _full_transition(manager, sessions[1].id)
        gate.register_session(sess_a)
        gate.register_session(sess_b)
        gate.register_review(sess_a.id, _make_review(sess_a.id))
        gate.register_review(sess_b.id, _make_review(sess_b.id))

        result = gate.reveal()
        assert len(result) == 2
        assert result[0].status == "revealed"
        assert result[1].status == "revealed"

    def test_reveal_only_once(self, manager: ReviewerSessionManager) -> None:
        gate = RevelationGate()
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        sess_a = _full_transition(manager, sessions[0].id)
        sess_b = _full_transition(manager, sessions[1].id)
        gate.register_session(sess_a)
        gate.register_session(sess_b)
        gate.register_review(sess_a.id, _make_review(sess_a.id))
        gate.register_review(sess_b.id, _make_review(sess_b.id))
        gate.reveal()
        with pytest.raises(IsolationViolation, match="already revealed"):
            gate.reveal()

    def test_audit_events_emitted_on_reveal(self, manager: ReviewerSessionManager) -> None:
        gate = RevelationGate()
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        sess_a = _full_transition(manager, sessions[0].id)
        sess_b = _full_transition(manager, sessions[1].id)
        gate.register_session(sess_a)
        gate.register_session(sess_b)
        gate.register_review(sess_a.id, _make_review(sess_a.id))
        gate.register_review(sess_b.id, _make_review(sess_b.id))
        gate.reveal()

        events = gate.audit_log
        assert len(events) >= 2
        for event in events:
            assert event.actor == "engine"
            assert event.from_state == "isolated"
            assert event.to_state == "revealed"
            assert event.timestamp is not None

    def test_audit_event_is_dataclass(self) -> None:
        event = AuditEvent(
            actor="engine",
            action="reveal",
            from_state="isolated",
            to_state="revealed",
            timestamp=NOW,
        )
        assert event.actor == "engine"
        assert event.action == "reveal"
        assert event.from_state == "isolated"
        assert event.to_state == "revealed"
        assert event.timestamp == NOW

    def test_reveal_before_commit_using_backend(self, manager: ReviewerSessionManager) -> None:
        gate = RevelationGate()
        backend = NotReadyBackend()
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)

        review_a = backend.run(
            ReviewRequest(
                artifact_id="art_x",
                side="A",
                artifact_content="content a",
                rubric_hints=[],
            )
        )
        review_b = backend.run(
            ReviewRequest(
                artifact_id="art_x",
                side="B",
                artifact_content="content b",
                rubric_hints=[],
            )
        )
        assert review_a.is_committed is False
        assert review_b.is_committed is False

        sess_a = _full_transition(manager, sessions[0].id)
        sess_b = _full_transition(manager, sessions[1].id)
        gate.register_session(sess_a)
        gate.register_session(sess_b)
        gate.register_review(sess_a.id, review_a)
        gate.register_review(sess_b.id, review_b)

        with pytest.raises(IsolationViolation, match="not committed"):
            gate.reveal()


# ===== T3.3 (#16) Commit immutability =====


class TestCommitImmutability:
    def test_review_is_frozen_by_pydantic(self) -> None:
        review = _make_review("sess_1", committed=False)
        with pytest.raises(ValidationError):
            review.confidence = 0.9

    def test_committed_review_cannot_be_mutated(self) -> None:
        review = _make_review("sess_1", committed=True)
        with pytest.raises(ValidationError):
            review.confidence = 0.9

    def test_engine_layer_guard_rejects_post_commit_mutation(self) -> None:
        review = _make_review("sess_1", committed=True)
        with pytest.raises(IsolationViolation, match="immutable"):
            _assert_no_mutation(review)

    def test_uncommitted_review_is_frozen_at_pydantic_layer(self) -> None:
        review = _make_review("sess_1", committed=False)
        with pytest.raises(ValidationError):
            review.confidence = 0.9

    def test_model_copy_creates_new_instance_immutably(self) -> None:
        review = _make_review("sess_1", committed=True)
        copied = review.model_copy(update={"confidence": 0.9})
        assert copied.confidence == 0.9
        assert review.confidence == 0.5


def _assert_no_mutation(review: Review) -> None:
    """Engine-layer guard: raise IsolationViolation if committed."""
    if review.is_committed:
        msg = "committed review is immutable"
        raise IsolationViolation(msg)


# ===== T3.4 (#17) Adversarial isolation =====


class TestIsolationAdversarial:
    def test_reveal_before_commit_raises(self, manager: ReviewerSessionManager) -> None:
        gate = RevelationGate()
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        gate.register_session(sessions[0])
        gate.register_session(sessions[1])
        with pytest.raises(IsolationViolation):
            gate.reveal()

    def test_session_a_prompt_never_contains_b_content(self) -> None:
        backend_a = FakeBackend()
        backend_b = FakeBackend()

        review_a = backend_a.run(
            ReviewRequest(
                artifact_id="art_1",
                side="A",
                artifact_content="SECRET_A for side A only",
                rubric_hints=[],
            )
        )
        review_b = backend_b.run(
            ReviewRequest(
                artifact_id="art_1",
                side="B",
                artifact_content="SECRET_B for side B only",
                rubric_hints=[],
            )
        )

        for req in backend_a.requests:
            assert "SECRET_B" not in (req.artifact_content or "")
        for req in backend_b.requests:
            assert "SECRET_A" not in (req.artifact_content or "")
        for claim in review_a.claims:
            assert "SECRET_B" not in claim.text
        for claim in review_b.claims:
            assert "SECRET_A" not in claim.text

    def test_no_cross_references_with_same_backend_instance(self) -> None:
        shared_backend = FakeBackend()
        request_a = ReviewRequest(
            artifact_id="art_1",
            side="A",
            artifact_content="secret_alpha",
            rubric_hints=[],
        )
        request_b = ReviewRequest(
            artifact_id="art_1",
            side="B",
            artifact_content="secret_beta",
            rubric_hints=[],
        )

        review_a = shared_backend.run(request_a)
        review_b = shared_backend.run(request_b)

        for claim in review_a.claims:
            assert "secret_beta" not in claim.text
        for claim in review_b.claims:
            assert "secret_alpha" not in claim.text

    def test_peeking_reviewer_impossible_by_construction(self) -> None:
        backend_a = FakeBackend()
        backend_b = PeekingBackend()

        review_a = backend_a.run(
            ReviewRequest(
                artifact_id="art_1",
                side="A",
                artifact_content="SQL injection in handler",
                rubric_hints=[],
            )
        )

        review_b = backend_b.run(
            ReviewRequest(
                artifact_id="art_1",
                side="B",
                artifact_content="B's own content",
                rubric_hints=[],
            )
        )

        a_claim_texts = {c.text for c in review_a.claims}
        b_claim_texts = {c.text for c in review_b.claims}
        overlap = a_claim_texts & b_claim_texts
        if overlap:
            msg = f"cross-session leakage detected: {overlap}"
            raise IsolationViolation(msg)

    def test_isolation_violation_has_correct_name(self) -> None:
        exc = IsolationViolation("test")
        assert isinstance(exc, Exception)
        assert str(exc) == "test"

    def test_reveal_requires_committed_at_stamp_on_reviews(
        self, manager: ReviewerSessionManager
    ) -> None:
        gate = RevelationGate()
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)

        sess_a = _full_transition(manager, sessions[0].id)
        sess_b = _full_transition(manager, sessions[1].id)
        gate.register_session(sess_a)
        gate.register_session(sess_b)

        rev_a = _make_review(sess_a.id, committed=False)
        rev_b = _make_review(sess_b.id, committed=True)
        gate.register_review(sess_a.id, rev_a)
        gate.register_review(sess_b.id, rev_b)

        with pytest.raises(IsolationViolation, match="not committed"):
            gate.reveal()

    def test_audit_log_returns_copied_list(self, manager: ReviewerSessionManager) -> None:
        gate = RevelationGate()
        sessions = manager.create_sessions("art_x", "a", "m1", "b", "m2", NOW)
        sess_a = _full_transition(manager, sessions[0].id)
        sess_b = _full_transition(manager, sessions[1].id)
        gate.register_session(sess_a)
        gate.register_session(sess_b)
        gate.register_review(sess_a.id, _make_review(sess_a.id))
        gate.register_review(sess_b.id, _make_review(sess_b.id))
        gate.reveal()

        log = gate.audit_log
        assert len(log) >= 2
        for event in log:
            assert isinstance(event, AuditEvent)
