"""Synthesis layer tests (M7: T7.1-T7.4, WBS M7 exit gate)."""

from __future__ import annotations

import json
from datetime import UTC, datetime

import pytest

from adversarial_debate.engine.debate_controller import DebateEvent
from adversarial_debate.engine.evidence import ClaimSnapshot, EvidenceContext
from adversarial_debate.engine.synthesis import (
    HeaderBlock,
    SynthesisValidationError,
    UnresolvedEntry,
    export_jsonl,
    synthesize_verdict,
    validate_synthesis_inputs,
    verify_export,
)
from adversarial_debate.schemas import Claim
from adversarial_debate.schemas.debate import Concession, DebateMessage, Severity, Side

NOW = datetime(2026, 8, 25, 12, 0, tzinfo=UTC)


def _make_evidence(  # noqa: PLR0913, PLR0917
    verdict: str = "verdict",
    resolved: int = 2,
    total: int = 2,
    theater: bool = False,
    cascade: bool = False,
    claims: list[ClaimSnapshot] | None = None,
) -> EvidenceContext:
    return EvidenceContext(
        convergence_score=resolved / total if total > 0 else 1.0,
        resolved_count=resolved,
        total_claims=total,
        verdict_kind=verdict,  # type: ignore[arg-type]
        theater=theater,
        capitulation_cascade=cascade,
        claims=claims or [],
        transitions=[],
        unverified_claims=[],
    )


def _make_claim(claim_id: str, text: str = "", severity: Severity = "medium") -> Claim:
    return Claim(
        id=claim_id,
        review_id="rev_test",
        text=text or f"Claim {claim_id}",
        severity=severity,
        evidence_refs=[],
        status="open",
    )


def _make_snapshot(
    claim_id: str,
    text: str = "",
    severity: Severity = "medium",
    final_status: str = "open",
) -> ClaimSnapshot:
    return ClaimSnapshot(
        id=claim_id,
        text=text or f"Claim {claim_id}",
        severity=severity,
        final_status=final_status,
        transition_count=0,
        evidence_refs=[],
    )


def _make_concession(claim_id: str, by_side: Side = "A", round_num: int = 1) -> Concession:
    return Concession(
        id=f"concession_{claim_id}",
        claim_id=claim_id,
        by_side=by_side,
        round=round_num,
        rationale=f"Conceded {claim_id}",
    )


def _make_event(
    kind: str,
    side: Side = "A",
    round_index: int = 1,
    content: str = "",
) -> DebateEvent:
    msg: DebateMessage | None = None
    if content:
        msg = DebateMessage(
            id=f"msg_{side}_r{round_index}",
            side=side,
            kind="defense",
            content=content,
        )
    return DebateEvent(
        round_index=round_index,
        side=side,
        kind=kind,  # type: ignore[arg-type]
        message=msg,
        timestamp=NOW,
    )


# ── T7.1 (#31) JointVerdict ──────────────────────────────────────────────────


class TestJointVerdict:
    def test_verdict_when_converged(self) -> None:
        evidence = _make_evidence(verdict="verdict", resolved=3, total=3)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        assert report.kind == "verdict"
        assert "Verdict" in report.verdict

    def test_disputed_when_not_converged(self) -> None:
        evidence = _make_evidence(verdict="disputed", resolved=1, total=3)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        assert report.kind == "disputed"
        assert "Disagreement" in report.verdict

    def test_strongest_arguments_by_severity(self) -> None:
        claims_a = [_make_claim("cl_001", "Low issue", "low")]
        snapshots = [_make_snapshot("cl_001", "Low issue", "low", "upheld")]
        evidence = _make_evidence(verdict="verdict", resolved=1, total=1, claims=snapshots)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": claims_a},
            concessions=[],
        )
        assert len(report.strongest_a) == 1
        assert "low" in report.strongest_a[0].lower()

    def test_header_block_includes_version(self) -> None:
        evidence = _make_evidence(verdict="verdict", resolved=1, total=1)
        header = HeaderBlock(engine_version="0.1.0")
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": [], "B": []},
            concessions=[],
            header=header,
        )
        assert report.header.engine_version == "0.1.0"

    def test_synthesis_with_multiple_claims_on_each_side(self) -> None:
        claims_a = [
            _make_claim("cl_001", "High impact", "high"),
            _make_claim("cl_002", "Medium impact", "medium"),
        ]
        claims_b = [_make_claim("cl_003", "Low impact", "low")]
        snapshots = [
            _make_snapshot("cl_001", "High impact", "high", "upheld"),
            _make_snapshot("cl_002", "Medium impact", "medium", "upheld"),
            _make_snapshot("cl_003", "Low impact", "low", "upheld"),
        ]
        evidence = _make_evidence(verdict="verdict", resolved=3, total=3, claims=snapshots)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": claims_a, "B": claims_b},
            concessions=[],
        )
        assert len(report.strongest_a) == 2
        assert len(report.strongest_b) == 1


# ── T7.2 (#32) DisagreementReporter ──────────────────────────────────────────


class TestDisagreementReporter:
    def test_resolved_entries_from_concessions(self) -> None:
        claims = [_make_claim("cl_001", "Security issue", "high")]
        snapshots = [_make_snapshot("cl_001", "Security issue", "high", "conceded")]
        concessions = [_make_concession("cl_001", by_side="A")]
        evidence = _make_evidence(verdict="disputed", resolved=1, total=2, claims=snapshots)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": claims, "B": []},
            concessions=concessions,
        )
        assert len(report.resolved) == 1
        assert report.resolved[0].claim_id == "cl_001"
        assert report.resolved[0].conceded_by == "A"
        assert report.resolved[0].rationale == "Conceded cl_001"

    def test_unresolved_entries_with_mandatory_would_resolve_if(self) -> None:
        snapshots = [_make_snapshot("cl_001", "Unresolved issue", "high", "open")]
        evidence = _make_evidence(verdict="disputed", resolved=0, total=1, claims=snapshots)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": [_make_claim("cl_001", "Unresolved issue", "high")]},
            concessions=[],
        )
        assert len(report.unresolved) == 1
        assert report.unresolved[0].would_resolve_if
        assert len(report.unresolved[0].would_resolve_if) > 10
        assert report.unresolved[0].severity == "high"
        assert report.unresolved[0].claim_ids == ["cl_001"]

    def test_top_n_cap_on_unresolved_points(self) -> None:
        snapshots = [_make_snapshot(f"cl_{i:03d}", f"Issue {i}", "high", "open") for i in range(20)]
        evidence = _make_evidence(verdict="disputed", resolved=0, total=20, claims=snapshots)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={
                "A": [_make_claim(f"cl_{i:03d}", f"Issue {i}", "high") for i in range(20)]
            },
            concessions=[],
            max_unresolved=5,
        )
        assert len(report.unresolved) <= 5

    def test_would_resolve_if_not_empty(self) -> None:
        snapshots = [_make_snapshot("cl_001", "XSS in search", "high", "open")]
        evidence = _make_evidence(verdict="disputed", resolved=0, total=1, claims=snapshots)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": [_make_claim("cl_001", "XSS in search", "high")]},
            concessions=[],
        )
        for u in report.unresolved:
            assert u.would_resolve_if, "would_resolve_if must not be empty (DD-06)"

    def test_empty_resolved_when_no_concessions(self) -> None:
        evidence = _make_evidence(verdict="verdict", resolved=0, total=0)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        assert report.resolved == []

    def test_flags_from_evidence_context(self) -> None:
        evidence = _make_evidence(
            verdict="disputed", resolved=0, total=1, theater=True, cascade=True
        )
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        assert report.flags.theater is True
        assert report.flags.capitulation_cascade is True


# ── T7.3 (#33) Fail-closed synthesis ─────────────────────────────────────────


class TestFlags:
    """Report flags from evidence context and debate events."""

    def test_flags_from_evidence_context(self) -> None:
        evidence = _make_evidence(
            verdict="disputed", resolved=0, total=1, theater=True, cascade=True
        )
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        assert report.flags.theater is True
        assert report.flags.capitulation_cascade is True

    def test_degraded_rounds_from_events(self) -> None:
        """Degraded rounds are extracted from debate events."""
        events = [
            _make_event("defense", side="A", round_index=1, content="Normal response."),
            DebateEvent(
                round_index=2,
                side="B",
                kind="defense",
                degraded=True,
                message=DebateMessage(
                    id="msg_B_r2", side="B", kind="defense", content="Degraded output"
                ),
                timestamp=NOW,
            ),
        ]
        evidence = _make_evidence(verdict="disputed", resolved=0, total=1)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": [], "B": []},
            concessions=[],
            events=events,
        )
        assert report.flags.degraded_rounds == [2]


# ── T7.3 (#33) Fail-closed synthesis ─────────────────────────────────────────
    def test_valid_inputs_pass_validation(self) -> None:
        evidence = _make_evidence(verdict="verdict", resolved=2, total=2)
        v = validate_synthesis_inputs(
            evidence, {"A": [_make_claim("cl_001"), _make_claim("cl_002")]}
        )
        assert v == []

    def test_negative_count_raises(self) -> None:
        evidence = _make_evidence(verdict="verdict", resolved=-1, total=2)
        with pytest.raises(SynthesisValidationError, match="resolved_count"):
            validate_synthesis_inputs(evidence, {"A": []})

    def test_exceeded_count_raises(self) -> None:
        evidence = _make_evidence(verdict="verdict", resolved=5, total=3)
        with pytest.raises(SynthesisValidationError, match="exceeds"):
            validate_synthesis_inputs(evidence, {"A": []})

    def test_empty_claims_by_side_raises(self) -> None:
        evidence = _make_evidence(verdict="verdict", resolved=0, total=0)
        with pytest.raises(SynthesisValidationError, match="empty"):
            validate_synthesis_inputs(evidence, {})

    def test_mismatched_claim_count_raises(self) -> None:
        evidence = _make_evidence(verdict="verdict", resolved=1, total=1)
        with pytest.raises(SynthesisValidationError, match="does not match"):
            validate_synthesis_inputs(
                evidence, {"A": [_make_claim("cl_001"), _make_claim("cl_002")]}
            )

    def test_duplicate_claim_ids_across_sides_passes(self) -> None:
        """Same claim ID in both sides counts once toward total_claims."""
        evidence = _make_evidence(verdict="verdict", resolved=1, total=1)
        # Same claim ID appears in both sides — unique count is 1, matches total_claims
        v = validate_synthesis_inputs(
            evidence, {"A": [_make_claim("cl_001")], "B": [_make_claim("cl_001")]}
        )
        assert v == []


# ── T7.4 (#34) JSONL exporter ────────────────────────────────────────────────


class TestJsonlExporter:
    def test_export_has_header_line(self) -> None:
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=_make_evidence(verdict="verdict", resolved=1, total=1),
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        export = export_jsonl(report, events=[])
        first = json.loads(export.strip().split("\n")[0])
        assert first["type"] == "header"

    def test_export_has_completeness_line(self) -> None:
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=_make_evidence(verdict="verdict", resolved=1, total=1),
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        export = export_jsonl(report, events=[])
        last = json.loads(export.strip().split("\n")[-1])
        assert last["type"] == "__completeness__"

    def test_events_appear_in_order(self) -> None:
        events = [
            _make_event("defense", side="A", round_index=1, content="First"),
            _make_event("defense", side="B", round_index=1, content="Second"),
        ]
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=_make_evidence(verdict="verdict", resolved=1, total=1),
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        export = export_jsonl(report, events)
        lines = export.strip().split("\n")
        assert len(lines) == 5
        assert json.loads(lines[1])["type"] == "event"
        assert json.loads(lines[2])["type"] == "event"
        assert json.loads(lines[3])["type"] == "report"
        assert json.loads(lines[4])["type"] == "__completeness__"

    def test_report_line_contains_all_fields(self) -> None:
        evidence = _make_evidence(verdict="disputed", resolved=1, total=3)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        export = export_jsonl(report, events=[])
        report_line = json.loads(export.strip().split("\n")[-2])
        assert report_line["type"] == "report"
        assert report_line["kind"] == "disputed"
        assert report_line["convergence_score"] == pytest.approx(1 / 3)
        assert "unresolved" in report_line
        assert "resolved" in report_line

    def test_verify_complete_export_returns_true(self) -> None:
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=_make_evidence(verdict="verdict", resolved=1, total=1),
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        assert verify_export(export_jsonl(report, events=[])) is True

    def test_verify_truncated_export_returns_false(self) -> None:
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=_make_evidence(verdict="verdict", resolved=1, total=1),
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        export = export_jsonl(report, events=[])
        truncated = "\n".join(export.strip().split("\n")[:-1])
        assert verify_export(truncated) is False

    def test_verify_empty_export_returns_false(self) -> None:
        assert verify_export("") is False

    def test_content_hash_in_header(self) -> None:
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=_make_evidence(verdict="verdict", resolved=1, total=1),
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        export = export_jsonl(report, events=[], content_hash="abc123")
        header = json.loads(export.strip().split("\n")[0])
        assert header["content_hash"] == "abc123"

    def test_header_to_dict(self) -> None:
        header = HeaderBlock(engine_version="0.1.0", prompt_version="v1", seeds={"A": 42})
        d = header.to_dict()
        assert d["engine_version"] == "0.1.0"
        assert d["seeds"] == {"A": 42}

    def test_event_with_concession_in_export(self) -> None:
        concession = Concession(
            id="conc_001", claim_id="cl_001", by_side="A", round=1, rationale="Ok"
        )
        event = DebateEvent(
            round_index=1,
            side="A",
            kind="defense",
            message=_make_event("defense", content="conceded").message,
            concession=concession,
        )
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=_make_evidence(verdict="verdict", resolved=1, total=1),
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        export = export_jsonl(report, events=[event])
        event_line = json.loads(export.strip().split("\n")[1])
        assert "concession" in event_line
        assert event_line["concession"]["claim_id"] == "cl_001"

    def test_event_with_error_in_export(self) -> None:
        event = DebateEvent(
            round_index=1,
            side="A",
            kind="system",
            error="Provider failure",
        )
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=_make_evidence(verdict="verdict", resolved=1, total=1),
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        export = export_jsonl(report, events=[event])
        event_line = json.loads(export.strip().split("\n")[1])
        assert event_line["error"] == "Provider failure"

    def test_verify_export_nonsense_returns_false(self) -> None:
        assert verify_export("not json") is False
        assert verify_export('{"type": "wrong"}') is False
        assert verify_export("[1, 2, 3]") is False


# ── Determinism ───────────────────────────────────────────────────────────────


class TestDeterminism:
    def test_same_input_produces_same_output(self) -> None:
        claims_a = [_make_claim("cl_001", "High impact", "high")]
        claims_b = [_make_claim("cl_002", "Low impact", "low")]
        snapshots = [
            _make_snapshot("cl_001", "High impact", "high", "conceded"),
            _make_snapshot("cl_002", "Low impact", "low", "open"),
        ]
        concessions = [_make_concession("cl_001", by_side="A")]
        evidence = _make_evidence(verdict="disputed", resolved=1, total=2, claims=snapshots)
        header = HeaderBlock(engine_version="0.1.0", prompt_version="v1")

        r1 = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": claims_a, "B": claims_b},
            concessions=concessions,
            header=header,
            max_unresolved=10,
        )
        r2 = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": claims_a, "B": claims_b},
            concessions=concessions,
            header=header,
            max_unresolved=10,
        )
        assert r1 == r2
        assert r1.verdict == r2.verdict
        assert r1.convergence_score == r2.convergence_score

    def test_same_input_same_jsonl(self) -> None:
        evidence = _make_evidence(verdict="verdict", resolved=1, total=1)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": [], "B": []},
            concessions=[],
        )
        e1 = export_jsonl(report, events=[])
        e2 = export_jsonl(report, events=[])
        assert e1 == e2

    def test_would_resolve_if_present_on_all_unresolved(self) -> None:
        snapshots = [_make_snapshot("cl_001", "Issue", "high", "open")]
        evidence = _make_evidence(verdict="disputed", resolved=0, total=1, claims=snapshots)
        report = synthesize_verdict(
            artifact_id="art_001",
            evidence=evidence,
            claims_by_side={"A": [_make_claim("cl_001", "Issue", "high")]},
            concessions=[],
        )
        for u in report.unresolved:
            assert isinstance(u, UnresolvedEntry)
            assert len(u.would_resolve_if) > 0
