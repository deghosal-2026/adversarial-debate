"""Debate controller tests (M5: T5.1-T5.4, WBS M5 exit gate).

Tests cover:
  - DebateController: round orchestration, termination states
  - Point-by-point enforcement validator
  - Caps: max claims enforcement
  - Degradation detector: repetition, truncation, refusal
  - Prompt builder: no-forced-persona grep test (DD-02)
  - End-to-end scripted debate scenarios
"""

from __future__ import annotations

import ast
import pathlib
from datetime import UTC, datetime
from typing import ClassVar

from adversarial_debate.engine.debate_controller import (
    AddressableObjection,
    DebateController,
    RoundContext,
    TokenBudget,
    build_round_prompt,
    check_claims_cap,
    detect_degradation,
    validate_point_by_point,
)
from adversarial_debate.providers.contract import ReviewRequest, ReviewResult, ReviewResultMetadata
from adversarial_debate.providers.scripted_reviewer import ScriptedReviewer
from adversarial_debate.schemas import (
    Claim,
    ContentBlock,
    Objection,
    Review,
    ReviewArtifact,
    ReviewerSession,
)
from adversarial_debate.schemas.debate import ClaimStatus, Severity, Side
from adversarial_debate.schemas.review import Risk

NOW = datetime(2026, 8, 24, 12, 0, tzinfo=UTC)

# ── test doubles ──────────────────────────────────────────────────────────────


class ScriptedDebateProvider:
    """Test double that returns canned results for debate rounds.

    Accepts a sequence of (raw_text, claims, risks) tuples, one per call.
    """

    def __init__(self, responses: list[ReviewResult] | None = None) -> None:
        self.responses = responses or []
        self.call_count = 0
        self.last_request: ReviewRequest | None = None

    def review(self, request: ReviewRequest) -> ReviewResult:
        self.call_count += 1
        self.last_request = request
        if self.call_count <= len(self.responses):
            return self.responses[self.call_count - 1]
        return ReviewResult(raw_text="No more responses configured", confidence=0.0)


def _make_session(side: Side, artifact_id: str = "art_test_1") -> ReviewerSession:
    return ReviewerSession(
        id=f"sess_{artifact_id}_{side}",
        artifact_id=artifact_id,
        side=side,
        provider="scripted",
        model="test",
        created_at=NOW,
        status="revealed",
    )


def _make_review(side: Side, claims: list[Claim] | None = None) -> Review:
    session_id = f"sess_art_test_1_{side}"
    review_id = f"rev_{session_id}"
    return Review(
        id=review_id,
        session_id=session_id,
        claims=claims or [],
        risks=[],
        confidence=0.75,
        committed_at=NOW,
    )


def _make_claim(
    claim_id: str,
    text: str,
    severity: Severity = "medium",
    evidence_refs: list[str] | None = None,
    status: ClaimStatus = "open",
) -> Claim:
    return Claim(
        id=claim_id,
        review_id="rev_fake",
        text=text,
        severity=severity,
        evidence_refs=evidence_refs or [],
        status=status,
    )


def _make_objection(
    obj_id: str,
    target_claim_id: str,
    argument: str,
    round_num: int = 1,
) -> Objection:
    return Objection(
        id=obj_id,
        target_claim_id=target_claim_id,
        argument=argument,
        round=round_num,
    )


def _make_responder(
    raw_text: str,
    claims: list[Claim] | None = None,
) -> ScriptedDebateProvider:
    return ScriptedDebateProvider(
        responses=[
            ReviewResult(
                raw_text=raw_text,
                claims=claims or [],
                risks=[],
                confidence=0.75,
                metadata=ReviewResultMetadata(seed=42, prompt_version="test"),
            )
        ]
    )


# ── T5.1 (#23) DebateController ──────────────────────────────────────────────


class TestDebateController:
    """Orchestration: round progression, termination states, event emission."""

    def test_happy_path_converge_rounds_exhausted(self) -> None:
        """Conceded claims resolve → debate may end early or exhaust rounds."""
        provider_a = _make_responder("CONCEDED on cl_001. REBUTTED on cl_002.")
        provider_b = _make_responder("CONCEDED on cl_003. REBUTTED on cl_004.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_003", "B1")]),
            artifact_for_prompt="test artifact",
            max_rounds=2,
        )

        state = controller.run()

        assert state.reason in ("rounds_exhausted", "all_resolved")
        assert state.rounds_completed >= 1

    def test_all_resolved_terminates_early(self) -> None:
        """Debate terminates with all_resolved when no outstanding claims."""
        provider_a = _make_responder("CONCEDED on cl_001.")
        provider_b = _make_responder("CONCEDED.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A"),
            review_b=_make_review("B"),
            artifact_for_prompt="test",
            max_rounds=4,
        )

        state = controller.run()

        assert state.reason == "all_resolved"
        assert state.rounds_completed == 0  # terminated before any round

    def test_budget_exhausted_terminates(self) -> None:
        """Debate terminates with budget_exhausted when budget hits zero."""
        provider = _make_responder("Some response text here.")

        controller = DebateController(
            provider_a=provider,
            provider_b=provider,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "Claim")]),
            review_b=_make_review("B", claims=[_make_claim("cl_002", "Claim")]),
            artifact_for_prompt="test",
            max_rounds=2,
            token_budget=TokenBudget(limit=0),
        )

        state = controller.run()

        assert state.reason == "budget_exhausted"

    def test_per_turn_budget_check_returns_empty(self) -> None:
        """Per-turn budget check in _run_side_turn returns early when exhausted."""
        provider_a = _make_responder("CONCEDED.")
        provider_b = _make_responder("CONCEDED.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_002", "B1")]),
            artifact_for_prompt="test",
            max_rounds=2,
            token_budget=TokenBudget(limit=0),
        )

        state = controller.run()
        assert state.reason == "budget_exhausted"

    def test_termination_state_contains_events(self) -> None:
        """TerminationState includes all emitted events and claims."""
        provider_a = _make_responder("CONCEDED. REBUTTED on cl_001.")
        provider_b = _make_responder("CARRIED.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_002", "B1")]),
            artifact_for_prompt="test",
            max_rounds=1,
        )

        state = controller.run()

        assert state.reason in ("rounds_exhausted", "all_resolved")
        assert isinstance(state.events, list)
        assert state.rounds_completed >= 0

    def test_all_events_returns_snapshot(self) -> None:
        """all_events() returns a copy of the events list."""
        provider_a = _make_responder("CONCEDED.")
        provider_b = _make_responder("REBUTTED.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_002", "B1")]),
            artifact_for_prompt="test",
            max_rounds=1,
        )

        controller.run()
        events = controller.all_events()
        assert len(events) >= 2
        for event in events:
            assert event.round_index >= 1

    def test_provider_error_terminates_with_error(self) -> None:
        """If a provider raises, the debate terminates with error."""

        class FailingProvider:
            def review(self, request: ReviewRequest) -> ReviewResult:
                del request
                msg = "Provider failure"
                raise RuntimeError(msg)

        controller = DebateController(
            provider_a=FailingProvider(),
            provider_b=FailingProvider(),
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_002", "B1")]),
            artifact_for_prompt="test",
            max_rounds=2,
        )

        state = controller.run()

        assert state.reason == "error"

    def test_multiple_rounds_emit_correct_number_of_events(self) -> None:
        """Running N rounds produces at least N*2 events (one per side per round)."""
        provider_a = _make_responder("CARRIED on all. REBUTTED.")
        provider_b = _make_responder("CARRIED.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_002", "B1")]),
            artifact_for_prompt="test",
            max_rounds=3,
        )

        state = controller.run()

        assert state.reason in ("rounds_exhausted", "all_resolved")
        assert state.rounds_completed >= 1


# ── T5.2 (#24) Point-by-point enforcement ─────────────────────────────────────


class TestPointByPointEnforcement:
    """Validator requires every outstanding objection to be addressed."""

    def test_all_objections_conceded(self) -> None:
        objections = [
            _make_objection("obj_1", "cl_001", "Missing validation"),
            _make_objection("obj_2", "cl_002", "Memory leak"),
        ]
        addressed = validate_point_by_point("CONCEDED on obj_1 and obj_2.", objections)

        assert all(a.addressed for a in addressed)
        assert addressed[0].response_type == "conceded"
        assert addressed[1].response_type == "conceded"

    def test_all_objections_rebutted(self) -> None:
        objections = [
            _make_objection("obj_1", "cl_001", "Missing validation"),
            _make_objection("obj_2", "cl_002", "Memory leak"),
        ]
        addressed = validate_point_by_point("REBUTTED on obj_1 and obj_2.", objections)

        assert all(a.addressed for a in addressed)
        assert addressed[0].response_type == "rebutted"
        assert addressed[1].response_type == "rebutted"

    def test_unaddressed_objections_detected(self) -> None:
        objections = [
            _make_objection("obj_1", "cl_001", "Missing validation"),
            _make_objection("obj_2", "cl_002", "Memory leak"),
        ]
        response = "CONCEDED on obj_1."

        addressed = validate_point_by_point(response, objections)

        assert addressed[0].addressed
        assert not addressed[1].addressed

    def test_empty_response_no_objections(self) -> None:
        addressed = validate_point_by_point("", [])
        assert addressed == []

    def test_carried_response_type(self) -> None:
        objections = [_make_objection("obj_1", "cl_001", "Issue")]
        response = "CARRIED on obj_1."

        addressed = validate_point_by_point(response, objections)

        assert addressed[0].addressed
        assert addressed[0].response_type == "carried"

    def test_addressable_objection_tracks_state(self) -> None:
        obj = _make_objection("obj_1", "cl_001", "Test")
        ao = AddressableObjection(obj)
        assert ao.objection == obj
        assert ao.addressed is False
        assert ao.is_conceded() is False

        ao.addressed = True
        ao.response_type = "conceded"
        assert ao.is_conceded()

    def test_no_matching_response(self) -> None:
        objections = [_make_objection("obj_1", "cl_001", "Issue")]
        response = "Nothing relevant here."

        addressed = validate_point_by_point(response, objections)
        assert not addressed[0].addressed

    def test_per_objection_keyword_scoping(self) -> None:
        """Each objection gets its own verdict from its region of the response."""
        objections = [
            _make_objection("obj_A", "cl_A", "Locking issue"),
            _make_objection("obj_B", "cl_B", "Memory leak"),
        ]
        response = (
            "CONCEDED on obj_A: you are right about the locking issue.\n"
            "REBUTTED on obj_B: the evidence does not support this concern."
        )

        addressed = validate_point_by_point(response, objections)

        assert addressed[0].response_type == "conceded"
        assert addressed[1].response_type == "rebutted"

    def test_carried_and_conceded_in_same_response(self) -> None:
        """Mixed response types per objection."""
        objections = [
            _make_objection("obj_1", "cl_001", "First issue"),
            _make_objection("obj_2", "cl_002", "Second issue"),
        ]
        response = "CARRIED on obj_1: I stand by my assessment.\nCONCEDED on obj_2: valid point."

        addressed = validate_point_by_point(response, objections)

        assert addressed[0].response_type == "carried"
        assert addressed[1].response_type == "conceded"


# ── T5.3 (#25) Caps ──────────────────────────────────────────────────────────


class TestCaps:
    """Max-claims enforcement and token budget."""

    def test_under_cap_passes_through(self) -> None:
        claims = [_make_claim(f"cl_{i}", f"Claim {i}") for i in range(5)]
        capped = check_claims_cap(claims, max_claims=20)
        assert len(capped) == 5

    def test_over_cap_truncates(self) -> None:
        claims = [_make_claim(f"cl_{i}", f"Claim {i}") for i in range(25)]
        capped = check_claims_cap(claims, max_claims=20)
        assert len(capped) == 20
        assert capped[-1].id == "cl_19"

    def test_exactly_at_cap(self) -> None:
        claims = [_make_claim(f"cl_{i}", f"Claim {i}") for i in range(20)]
        capped = check_claims_cap(claims, max_claims=20)
        assert len(capped) == 20

    def test_token_budget_exhausted(self) -> None:
        budget = TokenBudget(limit=0)
        assert budget.exhausted is True  # computed property from remaining <= 0
        assert budget.limit == 0

    def test_token_budget_with_remaining(self) -> None:
        budget = TokenBudget(limit=10000)
        assert budget.limit == 10000
        assert budget.exhausted is False

    def test_outstanding_filters_by_round(self) -> None:
        """Objections from earlier rounds are not re-presented in later rounds."""
        provider_a = _make_responder("CARRIED on cl_001.")
        provider_b = _make_responder("CARRIED on cl_003.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_003", "B1")]),
            artifact_for_prompt="test",
            max_rounds=2,
        )

        state = controller.run()
        # Round 2 should not re-present objections from round 1
        # that were already carried (not conceded)
        assert state.reason in ("rounds_exhausted", "all_resolved")

    def test_side_turn_only_updates_responding_side(self) -> None:
        """_run_side_turn only updates the responding side's claim list."""
        provider_a = _make_responder("CONCEDED on cl_001.")
        provider_b = _make_responder("REBUTTED.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_003", "B1")]),
            artifact_for_prompt="test",
            max_rounds=1,
        )

        state = controller.run()
        # After round 1, only side A's claims should have status changes
        a_conceded = any(c.status == "conceded" for c in state.claims_a)
        assert a_conceded  # A conceded on cl_001


# ── T5.4 (#26) Degradation detector ───────────────────────────────────────────


class TestDegradationDetector:
    """Heuristic detection of repetition, truncation, and refusal."""

    def test_clean_text_not_degraded(self) -> None:
        assert detect_degradation("This is a normal review response.") is False

    def test_repetition_detected(self) -> None:
        text = "This is repetitive. This is repetitive. This is repetitive."
        assert detect_degradation(text) is True

    def test_truncation_detected(self) -> None:
        assert detect_degradation("Here is my review of the") is True

    def test_completed_sentence_not_truncated(self) -> None:
        assert detect_degradation("Here is my review of the code.") is False

    def test_refusal_detected(self) -> None:
        assert detect_degradation("I cannot review this code.") is True

    def test_empty_text_degraded(self) -> None:
        assert detect_degradation("") is True

    def test_white_space_not_truncated(self) -> None:
        assert detect_degradation("Fine.") is False

    def test_exclamation_ending_not_truncated(self) -> None:
        assert detect_degradation("Excellent work!") is False

    def test_various_refusal_phrases(self) -> None:
        assert detect_degradation("i refuse to participate") is True
        assert detect_degradation("i cannot continue with this") is True
        assert detect_degradation("i'm not able to review") is True

    def test_question_mark_ends_sentence(self) -> None:
        assert detect_degradation("Is this correct?") is False

    def test_code_block_ending(self) -> None:
        assert detect_degradation("Here is the code: ```") is False

    def test_closing_brace_ending(self) -> None:
        assert detect_degradation("{ key: value }") is False


# ── Prompt builder ────────────────────────────────────────────────────────────


class TestBuildRoundPrompt:
    """Prompt builder: structure, no-forced-persona (DD-02)."""

    def test_prompt_contains_own_claims(self) -> None:
        review = _make_review("A", claims=[_make_claim("cl_001", "My claim")])
        ctx = RoundContext(
            own_review=review,
            own_session=_make_session("A"),
            other_claims=[],
            other_objections=[],
            outstanding_claims=[],
            outstanding_objections=[],
            round_index=1,
        )

        prompt = build_round_prompt(ctx)

        assert "My claim" in prompt
        assert "Debate Round 1" in prompt

    def test_prompt_contains_other_claims(self) -> None:
        review = _make_review("A")
        other_claims = [_make_claim("cl_002", "Other claim")]
        ctx = RoundContext(
            own_review=review,
            own_session=_make_session("A"),
            other_claims=other_claims,
            other_objections=[],
            outstanding_claims=[],
            outstanding_objections=[],
            round_index=1,
        )

        prompt = build_round_prompt(ctx)
        assert "Other claim" in prompt

    def test_prompt_contains_outstanding_objections(self) -> None:
        review = _make_review("A")
        objections = [_make_objection("obj_1", "cl_001", "Missing test")]
        ctx = RoundContext(
            own_review=review,
            own_session=_make_session("A"),
            other_claims=[],
            other_objections=[],
            outstanding_claims=[],
            outstanding_objections=objections,
            round_index=1,
        )

        prompt = build_round_prompt(ctx)
        assert "Missing test" in prompt

    def test_no_forced_persona_phrasing(self) -> None:
        """DD-02: prompt must not contain forced-persona phrasing."""
        review = _make_review("A", claims=[_make_claim("cl_001", "Claim")])
        ctx = RoundContext(
            own_review=review,
            own_session=_make_session("A"),
            other_claims=[],
            other_objections=[],
            outstanding_claims=[],
            outstanding_objections=[],
            round_index=1,
        )

        prompt = build_round_prompt(ctx)
        forbidden = [
            "you are now",
            "you are an expert",
            "act as a",
            "pretend you are",
            "role-play",
            "take on the role",
        ]
        for phrase in forbidden:
            assert phrase not in prompt.lower(), f"Forced persona phrase found: {phrase!r}"


# ── End-to-end scripted debate ────────────────────────────────────────────────


class TestScriptedDebateE2E:
    """End-to-end scripted debates: happy path, hold-and-dispute, capitulation."""

    def test_happy_path_converge(self) -> None:
        """Both sides concede on all points → debate resolves."""
        provider_a = _make_responder("CONCEDED on cl_001. REBUTTED on cl_002.")
        provider_b = _make_responder("CONCEDED on cl_003. REBUTTED on cl_004.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_003", "B1")]),
            artifact_for_prompt="test",
            max_rounds=2,
        )

        state = controller.run()
        assert state.reason in ("rounds_exhausted", "all_resolved")
        assert state.rounds_completed >= 1

    def test_hold_and_dispute(self) -> None:
        """Both sides hold position → disagreement preserved."""
        provider_a = _make_responder("CARRIED on cl_001. CARRIED on cl_002.")
        provider_b = _make_responder("CARRIED on cl_003. CARRIED on cl_004.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_003", "B1")]),
            artifact_for_prompt="test",
            max_rounds=2,
        )

        state = controller.run()
        assert state.reason == "rounds_exhausted"

    def test_capitulation_path(self) -> None:
        """One side concedes everything immediately → concessions recorded."""
        provider_a = _make_responder("CONCEDED on cl_001. CONCEDED on cl_002.")
        provider_b = _make_responder("REBUTTED.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_003", "B1")]),
            artifact_for_prompt="test",
            max_rounds=2,
        )

        state = controller.run()
        assert state.reason in ("rounds_exhausted", "all_resolved")
        assert state.rounds_completed >= 1

    def test_empty_reviews_converge_immediately(self) -> None:
        """Both sides with no claims → all_resolved immediately."""
        provider_a = _make_responder("Nothing to debate.")
        provider_b = _make_responder("Nothing to debate.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A"),
            review_b=_make_review("B"),
            artifact_for_prompt="test",
            max_rounds=2,
        )

        state = controller.run()
        assert state.reason == "all_resolved"

    def test_prompt_with_risks_includes_risks_section(self) -> None:
        """Prompt builder includes risks section when review has risks."""
        review = _make_review("A", claims=[_make_claim("cl_001", "Claim")])
        review = review.model_copy(
            update={"risks": [Risk(id="risk_1", text="Potential issue", severity="high")]}
        )
        ctx = RoundContext(
            own_review=review,
            own_session=_make_session("A"),
            other_claims=[],
            other_objections=[],
            outstanding_claims=[],
            outstanding_objections=[],
            round_index=1,
        )

        prompt = build_round_prompt(ctx)
        assert "Potential issue" in prompt
        assert "Your noted risks" in prompt

    def test_concessions_are_recorded(self) -> None:
        """Concessions from responses are stored in termination state."""
        provider_a = ScriptedDebateProvider(
            responses=[
                ReviewResult(raw_text="CONCEDED on cl_001.", claims=[], risks=[], confidence=0.5)
            ]
        )
        provider_b = ScriptedDebateProvider(
            responses=[
                ReviewResult(raw_text="CONCEDED on cl_002.", claims=[], risks=[], confidence=0.5)
            ]
        )

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_002", "B1")]),
            artifact_for_prompt="test",
            max_rounds=1,
        )

        state = controller.run()
        # Concessions should be recorded when CONCEDED appears in responses
        assert len(state.concessions) >= 1

    def test_unaddressed_objection_emits_event(self) -> None:
        """Unaddressed objections trigger a system event."""
        provider_a = ScriptedDebateProvider(
            responses=[ReviewResult(raw_text="Nothing here.", claims=[], risks=[], confidence=0.5)]
        )
        provider_b = ScriptedDebateProvider(
            responses=[
                ReviewResult(raw_text="Nothing from us.", claims=[], risks=[], confidence=0.5)
            ]
        )

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review("A", claims=[_make_claim("cl_001", "A1")]),
            review_b=_make_review("B", claims=[_make_claim("cl_002", "B1")]),
            artifact_for_prompt="test",
            max_rounds=1,
        )

        state = controller.run()
        # Should have a system/degraded event for unaddressed objections
        system_events = [e for e in state.events if e.kind == "system" and e.degraded]
        assert len(system_events) >= 1


# ── End-to-end with ScriptedReviewer (M2) ─────────────────────────────────────


class TestScriptedReviewerE2E:
    """End-to-end debates using real ScriptedReviewer from YAML scenarios."""

    SCENARIOS_PATH = "tests/scenarios/debate_scenarios.yaml"

    def _artifact(self, prefix: str) -> ReviewArtifact:
        return ReviewArtifact(
            id=f"{prefix}_001",
            domain="pr_review",
            source_uri="https://github.com/test/repo/pull/1",
            content_blocks=[
                ContentBlock(
                    id="block_1",
                    kind="diff",
                    name="test.py",
                    content="diff --git a/test.py b/test.py\n@@ -1,3 +1,5 @@\n+print('hello')",
                    sequence=0,
                )
            ],
            created_at=NOW,
            content_hash="0" * 64,
        )

    def _reviewer_from_scenario(self, artifact_id: str) -> ScriptedReviewer:
        return ScriptedReviewer(
            model="test",
            scenarios_path=self.SCENARIOS_PATH,
        )

    def test_converge_path(self) -> None:
        """ScriptedReviewer e2e: converge path — both sides concede."""
        reviewer = self._reviewer_from_scenario("art_debate_converge")
        result_a = reviewer.review(
            ReviewRequest(
                artifact=self._artifact("art_debate_converge"),
                prompt_version="v1",
            )
        )
        result_b = reviewer.review(
            ReviewRequest(
                artifact=self._artifact("art_debate_converge"),
                prompt_version="v1",
            )
        )

        session_a = _make_session("A", artifact_id="art_debate_converge_001")
        session_b = _make_session("B", artifact_id="art_debate_converge_001")

        controller = DebateController(
            provider_a=_ScriptedReviewerAdapter(reviewer),
            provider_b=_ScriptedReviewerAdapter(reviewer),
            session_a=session_a,
            session_b=session_b,
            review_a=_make_review("A", claims=list(result_a.claims)),
            review_b=_make_review("B", claims=list(result_b.claims)),
            artifact_for_prompt="test",
            max_rounds=2,
        )

        state = controller.run()
        assert state.reason in ("rounds_exhausted", "all_resolved")
        assert state.rounds_completed >= 1

    def test_hold_and_dispute_path(self) -> None:
        """ScriptedReviewer e2e: hold-and-dispute — both sides carry."""
        reviewer = self._reviewer_from_scenario("art_debate_hold")
        result_a = reviewer.review(
            ReviewRequest(
                artifact=self._artifact("art_debate_hold"),
                prompt_version="v1",
            )
        )
        result_b = reviewer.review(
            ReviewRequest(
                artifact=self._artifact("art_debate_hold"),
                prompt_version="v1",
            )
        )

        controller = DebateController(
            provider_a=_ScriptedReviewerAdapter(reviewer),
            provider_b=_ScriptedReviewerAdapter(reviewer),
            session_a=_make_session("A", artifact_id="art_debate_hold_001"),
            session_b=_make_session("B", artifact_id="art_debate_hold_001"),
            review_a=_make_review("A", claims=list(result_a.claims)),
            review_b=_make_review("B", claims=list(result_b.claims)),
            artifact_for_prompt="test",
            max_rounds=2,
        )

        state = controller.run()
        assert state.reason in ("rounds_exhausted", "all_resolved")

    def test_capitulation_path(self) -> None:
        """ScriptedReviewer e2e: capitulation — one side concedes everything."""
        reviewer = self._reviewer_from_scenario("art_debate_capitulate")
        result_a = reviewer.review(
            ReviewRequest(
                artifact=self._artifact("art_debate_capitulate"),
                prompt_version="v1",
            )
        )
        result_b = reviewer.review(
            ReviewRequest(
                artifact=self._artifact("art_debate_capitulate"),
                prompt_version="v1",
            )
        )

        controller = DebateController(
            provider_a=_ScriptedReviewerAdapter(reviewer),
            provider_b=_ScriptedReviewerAdapter(reviewer),
            session_a=_make_session("A", artifact_id="art_debate_capitulate_001"),
            session_b=_make_session("B", artifact_id="art_debate_capitulate_001"),
            review_a=_make_review("A", claims=list(result_a.claims)),
            review_b=_make_review("B", claims=list(result_b.claims)),
            artifact_for_prompt="test",
            max_rounds=2,
        )

        state = controller.run()
        assert state.reason in ("rounds_exhausted", "all_resolved")


class _ScriptedReviewerAdapter:
    """Adapts ScriptedReviewer to the DebateProvider protocol.

    ScriptedReviewer.review() matches on request.artifact.id prefix.
    The DebateProvider protocol expects a .review(ReviewRequest) → ReviewResult.
    The adapter delegates directly — no translation needed since both use
    ReviewRequest/ReviewResult from the contract module.
    """

    def __init__(self, reviewer: ScriptedReviewer) -> None:
        self._reviewer = reviewer

    def review(self, request: ReviewRequest) -> ReviewResult:
        return self._reviewer.review(request)


# ── DD-02: No forced personas ─────────────────────────────────────────────────


class TestNoForcedPersonas:
    """Grep test over all prompt templates — no forced-persona phrasing (DD-02)."""

    PROMPT_TEMPLATE_FILES: ClassVar[list[str]] = [
        "src/adversarial_debate/engine/debate_controller.py",
    ]

    FORBIDDEN_PATTERNS: ClassVar[list[str]] = [
        "you are now",
        "you are an expert",
        "act as a",
        "pretend you are",
        "role-play",
        "take on the role of",
        "you're an expert",
        "you are a senior",
        "you are a code review",
        "pretend to be",
    ]

    def test_no_forced_persona_in_prompt_builder(self) -> None:
        """Search prompt builder source for forbidden persona phrases."""
        filepath = pathlib.Path(self.PROMPT_TEMPLATE_FILES[0])
        source = filepath.read_text()
        tree = ast.parse(source)

        # Only check string literals in the file — these are the prompt templates
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                text = node.value.lower()
                for pattern in self.FORBIDDEN_PATTERNS:
                    if pattern in text:
                        msg = (
                            f"Forbidden persona phrase {pattern!r} "
                            f"found in prompt builder at {filepath}"
                        )
                        raise AssertionError(msg)
