"""Review schemas contract (WBS T1.4, PRD §2.4 rows 2-3 + WBS status enum)."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from adversarial_debate.schemas import Claim, Review, ReviewerSession

NOW = datetime(2026, 8, 24, 12, 0, tzinfo=UTC)


def make_claim() -> Claim:
    return Claim(id="cl_1", review_id="rev_1", text="SQL injection in handler", severity="high")


def make_session(**overrides: object) -> ReviewerSession:
    fields: dict[str, object] = {
        "id": "sess_a",
        "artifact_id": "art_test",
        "side": "A",
        "provider": "openai-compat",
        "model": "gpt-x",
        "created_at": NOW,
    }
    fields.update(overrides)
    return ReviewerSession.model_validate(fields)


def make_review(**overrides: object) -> Review:
    fields: dict[str, object] = {
        "id": "rev_1",
        "session_id": "sess_a",
        "claims": [make_claim()],
        "risks": [],
        "confidence": 0.8,
        "committed_at": None,
    }
    fields.update(overrides)
    return Review.model_validate(fields)


def test_session_defaults_to_isolated() -> None:
    assert make_session().status == "isolated"


def test_session_status_enum_covers_gate_transitions() -> None:
    for status in ("isolated", "revealed", "debating", "done"):
        assert make_session(status=status).status == status
    assert make_session(status="error", error="timeout").status == "error"


def test_session_rejects_unknown_status_and_side() -> None:
    with pytest.raises(ValidationError):
        make_session(status="committed")
    with pytest.raises(ValidationError):
        make_session(side="C")


def test_session_error_detail_only_when_errored() -> None:
    errored = make_session(status="error", error="provider timeout")
    assert errored.error == "provider timeout"
    with pytest.raises(ValidationError, match="stray detail"):
        make_session(status="done", error="stray detail")


def test_error_status_requires_detail() -> None:
    with pytest.raises(ValidationError, match="error detail required"):
        make_session(status="error")


def test_review_round_trip_and_commit_flag() -> None:
    draft = make_review()
    assert Review.model_validate_json(draft.model_dump_json()) == draft
    assert draft.is_committed is False
    committed = make_review(committed_at=NOW)
    assert committed.is_committed is True


def test_confidence_bounded() -> None:
    with pytest.raises(ValidationError):
        make_review(confidence=1.2)
    with pytest.raises(ValidationError):
        make_review(confidence=-0.1)


def test_frozen_after_creation() -> None:
    review = make_review()
    with pytest.raises(ValidationError):
        review.confidence = 0.5


def test_nested_claim_validation_propagates() -> None:
    with pytest.raises(ValidationError):
        make_review(claims=[{"id": "cl_x", "review_id": "rev_1", "text": "", "severity": "high"}])
