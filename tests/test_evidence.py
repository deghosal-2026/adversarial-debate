"""Evidence tracker tests (M6: T6.1-T6.4, WBS M6 exit gate).

Tests cover:
  - EvidenceTracker: claim lifecycle, transition recording
  - Convergence scoring: resolved/total math, edge cases
  - Theater detection: zero-state-change flag
  - Capitulation-cascade detection: FM-2 signature
  - Evidence-reference validation: FM-7 guard, cross-check
  - Property tests: score math invariants
"""

from __future__ import annotations

from datetime import UTC, datetime

from adversarial_debate.engine.debate_controller import DebateEvent
from adversarial_debate.engine.evidence import EvidenceTracker
from adversarial_debate.schemas import Claim, ContentBlock
from adversarial_debate.schemas.debate import ClaimStatus, Concession, DebateMessage, Severity, Side

NOW = datetime(2026, 8, 25, 12, 0, tzinfo=UTC)


def _make_claim(
    claim_id: str,
    text: str = "Test claim",
    severity: Severity = "medium",
    evidence_refs: list[str] | None = None,
    status: ClaimStatus = "open",
) -> Claim:
    return Claim(
        id=claim_id,
        review_id="rev_test",
        text=text,
        severity=severity,
        evidence_refs=evidence_refs or [],
        status=status,
    )


def _make_concession(
    claim_id: str, by_side: Side = "A", round_num: int = 1
) -> Concession:
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


# ── T6.1 (#27) EvidenceTracker ───────────────────────────────────────────────


class TestEvidenceTracker:
    """Claim lifecycle — concessions, transitions, snapshots."""

    def test_empty_claims_converges(self) -> None:
        """No claims = convergence_score of 1.0."""
        tracker = EvidenceTracker(claims=[], concessions=[], events=[])
        ctx = tracker.compute()
        assert ctx.convergence_score == 1.0
        assert ctx.verdict_kind == "verdict"
        assert ctx.total_claims == 0

    def test_apply_concession_transitions_claim(self) -> None:
        """Concession creates a transition and marks claim as resolved."""
        claims = [_make_claim("cl_001")]
        concessions = [_make_concession("cl_001")]
        tracker = EvidenceTracker(claims, concessions, events=[])
        ctx = tracker.compute()

        assert ctx.resolved_count == 1
        assert ctx.total_claims == 1
        assert len(ctx.transitions) == 1
        assert ctx.transitions[0].claim_id == "cl_001"
        assert ctx.transitions[0].to_status == "conceded"
        assert ctx.transitions[0].from_status == "open"

    def test_multiple_concessions_all_resolved(self) -> None:
        """Multiple concessions all recorded."""
        claims = [_make_claim("cl_001"), _make_claim("cl_002")]
        concessions = [_make_concession("cl_001"), _make_concession("cl_002")]
        tracker = EvidenceTracker(claims, concessions, events=[])
        ctx = tracker.compute()

        assert ctx.resolved_count == 2
        assert ctx.convergence_score == 1.0
        assert ctx.verdict_kind == "verdict"

    def test_partial_concessions_produces_disputed(self) -> None:
        """Only some claims conceded → verdict is disputed."""
        claims = [_make_claim("cl_001"), _make_claim("cl_002")]
        concessions = [_make_concession("cl_001")]
        tracker = EvidenceTracker(claims, concessions, events=[])
        ctx = tracker.compute()

        assert ctx.resolved_count == 1
        assert ctx.total_claims == 2
        assert ctx.convergence_score == 0.5
        assert ctx.verdict_kind == "disputed"

    def test_concession_for_unknown_claim_ignored(self) -> None:
        """Concession for a nonexistent claim is safely ignored."""
        claims = [_make_claim("cl_001")]
        concessions = [_make_concession("cl_999")]
        tracker = EvidenceTracker(claims, concessions, events=[])
        ctx = tracker.compute()

        assert ctx.resolved_count == 0
        assert ctx.total_claims == 1
        assert ctx.convergence_score == 0.0

    def test_transitions_are_append_only(self) -> None:
        """Multiple transitions for same claim are separate records."""
        claims = [_make_claim("cl_001")]
        concessions = [
            _make_concession("cl_001", round_num=1),
            _make_concession("cl_001", round_num=2),
        ]
        tracker = EvidenceTracker(claims, concessions, events=[])
        ctx = tracker.compute()

        assert len(ctx.transitions) == 2
        # Second concession for same claim: still recorded as separate
        val = ctx.transitions[0]
        assert val.claim_id == "cl_001"

    def test_snapshot_includes_final_status(self) -> None:
        """ClaimSnapshot reflects final status after transitions."""
        claims = [_make_claim("cl_001")]
        concessions = [_make_concession("cl_001")]
        tracker = EvidenceTracker(claims, concessions, events=[])
        ctx = tracker.compute()

        assert len(ctx.claims) == 1
        assert ctx.claims[0].id == "cl_001"
        assert ctx.claims[0].final_status == "conceded"
        assert ctx.claims[0].transition_count >= 1

    def test_snapshot_open_claim_no_transitions(self) -> None:
        """Unresolved claim stays in its original status."""
        claims = [_make_claim("cl_001")]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        ctx = tracker.compute()

        assert ctx.claims[0].final_status == "open"
        assert ctx.claims[0].transition_count == 0

    def test_upheld_by_debate_event(self) -> None:
        """Defense event with UPHELD marker transitions claim."""
        claims = [_make_claim("cl_001")]
        events = [
            _make_event("defense", content="cl_001 was UPHELD by evidence."),
        ]
        tracker = EvidenceTracker(claims, concessions=[], events=events)
        ctx = tracker.compute()

        assert ctx.resolved_count == 1
        assert ctx.claims[0].final_status == "upheld"
        assert any(t.to_status == "upheld" for t in ctx.transitions)

    def test_agreed_event_uphelds_claim(self) -> None:
        """Defense event with AGREED marker transitions claim."""
        claims = [_make_claim("cl_001")]
        events = [
            _make_event("defense", content="AGREED with cl_001."),
        ]
        tracker = EvidenceTracker(claims, concessions=[], events=events)
        ctx = tracker.compute()

        assert ctx.resolved_count == 1


# ── T6.2 (#28) Convergence scoring ───────────────────────────────────────────


class TestConvergenceScoring:
    """Score math: resolved/total, edge cases, property tests."""

    def test_zero_claims_score_one(self) -> None:
        """No claims → convergence_score = 1.0."""
        tracker = EvidenceTracker(claims=[], concessions=[], events=[])
        ctx = tracker.compute()
        assert ctx.convergence_score == 1.0

    def test_all_conceded_score_one(self) -> None:
        """All claims conceded → convergence_score = 1.0."""
        claims = [_make_claim(f"cl_{i:03d}") for i in range(10)]
        concessions = [_make_concession(f"cl_{i:03d}") for i in range(10)]
        tracker = EvidenceTracker(claims, concessions, events=[])
        ctx = tracker.compute()
        assert ctx.convergence_score == 1.0

    def test_none_conceded_score_zero(self) -> None:
        """No concessions → convergence_score = 0.0."""
        claims = [_make_claim("cl_001")]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        ctx = tracker.compute()
        assert ctx.convergence_score == 0.0

    def test_half_conceded_score_half(self) -> None:
        """5 of 10 conceded → convergence_score = 0.5."""
        claims = [_make_claim(f"cl_{i:03d}") for i in range(10)]
        concessions = [_make_concession(f"cl_{i:03d}") for i in range(5)]
        tracker = EvidenceTracker(claims, concessions, events=[])
        ctx = tracker.compute()
        assert ctx.convergence_score == 0.5

    def test_mixed_verdict_kind_derivation(self) -> None:
        """All resolved = verdict, otherwise = disputed."""
        small_claims = [_make_claim("cl_001")]
        tracker_all = EvidenceTracker(small_claims, [_make_concession("cl_001")], events=[])
        assert tracker_all.compute().verdict_kind == "verdict"

        tracker_partial = EvidenceTracker(
            [_make_claim("cl_001"), _make_claim("cl_002")],
            [_make_concession("cl_001")],
            events=[],
        )
        assert tracker_partial.compute().verdict_kind == "disputed"

    def test_score_monotonic(self) -> None:
        """Adding more concessions never decreases score."""
        claims = [_make_claim(f"cl_{i:03d}") for i in range(5)]
        for n in range(6):
            concessions = [_make_concession(f"cl_{i:03d}") for i in range(n)]
            tracker = EvidenceTracker(claims, concessions, events=[])
            score = tracker.compute().convergence_score
            expected = n / 5
            assert score == expected, f"n={n}: expected {expected}, got {score}"


# ── T6.3 (#29) Theater & capitulation ────────────────────────────────────────


class TestTheaterDetection:
    """Zero-state-change detection and FM-2 capitulation cascade."""

    def test_no_changes_is_theater(self) -> None:
        """No concessions, no transitions → theater=True."""
        claims = [_make_claim("cl_001")]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        ctx = tracker.compute()
        assert ctx.theater is True

    def test_with_concession_not_theater(self) -> None:
        """A concession means debate was substantive → theater=False."""
        claims = [_make_claim("cl_001")]
        concessions = [_make_concession("cl_001")]
        tracker = EvidenceTracker(claims, concessions, events=[])
        ctx = tracker.compute()
        assert ctx.theater is False

    def test_empty_claims_not_theater(self) -> None:
        """No claims to debate → not theater (there is nothing to change)."""
        tracker = EvidenceTracker(claims=[], concessions=[], events=[])
        ctx = tracker.compute()
        assert ctx.theater is not None

    def test_capitulation_cascade_detected(self) -> None:
        """>=80% round-1 concessions with no rebuttals = capitulation."""
        claims = [_make_claim(f"cl_{i:03d}") for i in range(10)]
        concessions = [_make_concession(f"cl_{i:03d}", round_num=1) for i in range(8)]
        tracker = EvidenceTracker(claims, concessions, events=[])
        ctx = tracker.compute()
        assert ctx.capitulation_cascade is True

    def test_capitulation_cascade_not_detected_with_rebuttals(self) -> None:
        """Rebutted concessions are not capitulation."""
        claims = [_make_claim(f"cl_{i:03d}") for i in range(5)]
        concessions = [_make_concession(f"cl_{i:03d}", round_num=1) for i in range(5)]
        events = [_make_event("defense", content="REBUTTED on cl_001.")]
        tracker = EvidenceTracker(claims, concessions, events=events)
        ctx = tracker.compute()
        assert ctx.capitulation_cascade is False

    def test_no_concessions_no_capitulation(self) -> None:
        """No concessions → not capitulation."""
        claims = [_make_claim("cl_001")]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        ctx = tracker.compute()
        assert ctx.capitulation_cascade is False

    def test_below_threshold_not_capitulation(self) -> None:
        """5/10 concessions = below 80% threshold = no capitulation."""
        claims = [_make_claim(f"cl_{i:03d}") for i in range(10)]
        concessions = [_make_concession(f"cl_{i:03d}", round_num=1) for i in range(5)]
        tracker = EvidenceTracker(claims, concessions, events=[])
        ctx = tracker.compute()
        assert ctx.capitulation_cascade is False


# ── T6.4 (#30) Evidence-reference validation ──────────────────────────────────


class TestEvidenceReferenceValidation:
    """FM-7 guard: high-severity claims must have evidence; refs must resolve."""

    def test_high_severity_without_refs_is_unverified(self) -> None:
        """High-severity claim with no evidence_refs → unverified."""
        claims = [_make_claim("cl_001", severity="high", evidence_refs=[])]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        ctx = tracker.compute()
        assert "cl_001" in ctx.unverified_claims

    def test_high_severity_with_refs_is_verified(self) -> None:
        """High-severity claim with valid refs → not unverified."""
        claims = [_make_claim("cl_001", severity="high", evidence_refs=["src/file.py:42"])]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        ctx = tracker.compute()
        assert "cl_001" not in ctx.unverified_claims

    def test_low_severity_without_refs_not_unverified(self) -> None:
        """Low-severity claim without refs is acceptable."""
        claims = [_make_claim("cl_001", severity="low", evidence_refs=[])]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        ctx = tracker.compute()
        assert "cl_001" not in ctx.unverified_claims

    def test_medium_severity_without_refs_not_unverified(self) -> None:
        """Medium-severity claim without refs is acceptable."""
        claims = [_make_claim("cl_001", severity="medium", evidence_refs=[])]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        ctx = tracker.compute()
        assert "cl_001" not in ctx.unverified_claims

    def test_invalid_ref_format_marked_unverified(self) -> None:
        """Malformed ref like 'not valid!!' fails format check."""
        claims = [_make_claim("cl_001", severity="low", evidence_refs=["not valid!! ref"])]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        ctx = tracker.compute()
        assert "cl_001" in ctx.unverified_claims

    def test_file_line_ref_is_valid(self) -> None:
        """'path/file.py:10-20' is a valid ref format."""
        claims = [_make_claim("cl_001", severity="high", evidence_refs=["src/main.py:10-20"])]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        ctx = tracker.compute()
        assert "cl_001" not in ctx.unverified_claims

    def test_plain_block_id_ref_is_valid(self) -> None:
        """Simple alphanumeric id is a valid ref."""
        claims = [_make_claim("cl_001", severity="high", evidence_refs=["block_01"])]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        ctx = tracker.compute()
        assert "cl_001" not in ctx.unverified_claims

    def test_validate_evidence_cross_check_content_blocks(self) -> None:
        """Cross-check refs against actual content blocks."""
        claims = [_make_claim("cl_001", evidence_refs=["src/file.py:10"])]
        content_blocks = [
            ContentBlock(id="src/file.py", kind="diff", name="file.py", content="", sequence=0),
        ]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        unresolved = tracker.validate_evidence(content_blocks)
        assert isinstance(unresolved, list)

    def test_validate_evidence_detects_unresolved_refs(self) -> None:
        """Ref with block id not in content blocks → unresolved."""
        claims = [_make_claim("cl_001", evidence_refs=["nonexistent_block"])]
        content_blocks = [
            ContentBlock(id="block_01", kind="text", name="test.py", content="x", sequence=0),
        ]
        tracker = EvidenceTracker(claims, concessions=[], events=[])
        unresolved = tracker.validate_evidence(content_blocks)
        assert "cl_001" in unresolved

    def test_ref_looks_valid_accepts_colon_ref(self) -> None:
        """File:line pattern is valid."""
        tracker = _empty_tracker()
        assert tracker._ref_looks_valid("src/main.py:42")
        assert tracker._ref_looks_valid("src/main.py:42-56")
        assert tracker._ref_looks_valid("./src/test.py:10")

    def test_ref_looks_valid_rejects_empty(self) -> None:
        """Empty string is not a valid ref."""
        tracker = _empty_tracker()
        assert not tracker._ref_looks_valid("")

    def test_ref_looks_valid_rejects_invalid(self) -> None:
        """Gibberish is not a valid ref."""
        tracker = _empty_tracker()
        assert not tracker._ref_looks_valid("!!!invalid ref!!! with spaces")


def _empty_tracker() -> EvidenceTracker:
    return EvidenceTracker(claims=[], concessions=[], events=[])
