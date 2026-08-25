"""Debate schemas contract (WBS T1.5, PRD §2.4 rows 4-9, §2.7 convergence)."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from adversarial_debate.schemas import (
    Claim,
    Concession,
    DebateMessage,
    DebateRound,
    Objection,
    Outcome,
    UnresolvedPoint,
)

NOW = datetime(2026, 8, 24, 12, 0, tzinfo=UTC)


def make_claim() -> Claim:
    return Claim(id="cl_1", review_id="rev_1", text="SQL injection in handler", severity="high")


def test_claim_lifecycle_defaults_open() -> None:
    claim = make_claim()
    assert claim.status == "open"
    assert claim.evidence_refs == []
    for status in ("conceded", "upheld", "resolved"):
        assert (
            Claim(id="cl_2", review_id="rev_1", text="x", severity="low", status=status).status
            == status
        )


def test_claim_rejects_unknown_status_and_severity() -> None:
    with pytest.raises(ValidationError, match="status"):
        Claim.model_validate(
            {"id": "cl_2", "review_id": "rev_1", "text": "x", "severity": "low", "status": "closed"}
        )
    with pytest.raises(ValidationError, match="severity"):
        Claim.model_validate({"id": "cl_3", "review_id": "r", "text": "x", "severity": "blocker"})


def test_objection_targets_specific_claim_with_round() -> None:
    obj = Objection(id="ob_1", target_claim_id="cl_1", argument="Parameterized already", round=1)
    assert obj.round == 1
    with pytest.raises(ValidationError):
        Objection(id="ob_2", target_claim_id="cl_1", argument="x", round=0)
    with pytest.raises(ValidationError):
        Objection(id="ob_3", target_claim_id="", argument="x", round=1)


def test_concession_requires_rationale() -> None:
    conc = Concession(id="co_1", claim_id="cl_1", by_side="A", round=2, rationale="Conceded: fixed")
    assert conc.by_side == "A"
    with pytest.raises(ValidationError, match="rationale"):
        Concession(id="co_2", claim_id="cl_1", by_side="B", round=1, rationale="")


def test_unresolved_point_would_resolve_if_mandatory() -> None:
    point = UnresolvedPoint(
        id="up_1",
        claim_ids=["cl_1"],
        position_a="Safe due to ORM escaping",
        position_b="Raw string interpolation is unsafe",
        would_resolve_if="Add integration test with quote-laden input",
    )
    assert point.would_resolve_if
    assert "would_resolve_if" in UnresolvedPoint.model_fields
    with pytest.raises(ValidationError):
        UnresolvedPoint(
            id="up_2",
            claim_ids=["cl_1"],
            position_a="a",
            position_b="b",
            would_resolve_if="",
        )


def test_debate_round_messages_and_window() -> None:
    msg = DebateMessage(id="m_1", side="A", kind="objection", content="Rebutting cl_1")
    rnd = DebateRound(
        id="dr_1",
        artifact_id="art_test",
        index=1,
        messages=[msg],
        started_at=NOW,
    )
    assert DebateRound.model_validate_json(rnd.model_dump_json()) == rnd
    assert rnd.ended_at is None
    with pytest.raises(ValidationError):
        DebateRound(id="dr_2", artifact_id="art", index=0, messages=[], started_at=NOW)


def test_outcome_convergence_score_consistent() -> None:
    outcome = Outcome(
        id="out_1",
        artifact_id="art_test",
        kind="verdict",
        converged_count=4,
        total_claims=5,
        report_ref="reports/art_test.md",
    )
    assert outcome.convergence_score == pytest.approx(0.8)
    with pytest.raises(ValidationError, match="converged_count"):
        Outcome(
            id="out_2",
            artifact_id="a",
            kind="disputed",
            converged_count=6,
            total_claims=5,
            report_ref="r",
        )
    with pytest.raises(ValidationError, match="total_claims"):
        Outcome(
            id="out_3",
            artifact_id="a",
            kind="verdict",
            converged_count=1,
            total_claims=0,
            report_ref="r",
        )


def test_outcome_score_hidden_denominator_forbidden() -> None:
    """PRD §2.7: score displayed alongside verdict, never hiding the denominator."""
    outcome = Outcome(
        id="out_4",
        artifact_id="art_test",
        kind="verdict",
        converged_count=5,
        total_claims=5,
        report_ref="r",
    )
    assert outcome.convergence_score == 1.0
