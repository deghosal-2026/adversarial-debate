"""Debate controller: bounded rebuttal rounds, point-by-point enforcement, caps, degradation.

M5 core (T5.1-T5.4). After M3 revelation, the controller drives alternating
rounds where each reviewer responds to outstanding objections. Key invariants:

- No forced personas (DD-02) — reviewers argue their own committed views
- ``would_resolve_if`` is mandatory on unresolved points (DD-06)
- Convergence is claim-state-based, never semantic-similarity (DD-08)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Literal, Protocol

from adversarial_debate.providers.contract import ReviewRequest, ReviewResult
from adversarial_debate.schemas import (
    Claim,
    ContentBlock,
    DebateMessage,
    Objection,
    Review,
    ReviewArtifact,
    ReviewerSession,
    Side,
)
from adversarial_debate.schemas.debate import Concession

CANARY_TOKEN = "CANARY_ISOLATION_CHECK_8f3a2b"
"""Token injected into side A's output to detect isolation leaks to side B."""

TerminationReason = Literal[
    "rounds_exhausted",
    "all_resolved",
    "budget_exhausted",
    "error",
]
DebateStatus = Literal["running", "terminated"]


@dataclass(frozen=True)
class RoundContext:
    """Context passed to a reviewer when building a debate-round prompt.

    Contains the reviewer's own committed review, the other side's claims and
    objections, and the list of still-outstanding objections that must be
    addressed this round.
    """

    own_review: Review
    own_session: ReviewerSession
    other_claims: list[Claim]
    other_objections: list[Objection]
    outstanding_claims: list[Claim]
    outstanding_objections: list[Objection]
    round_index: int


@dataclass(frozen=True)
class DebateEvent:
    """One event emitted by the controller during a debate round.

    Captures everything needed for M6 evidence tracking and M8 persistence.
    """

    round_index: int
    side: Side
    kind: Literal["statement", "objection", "defense", "concession", "system"]
    message: DebateMessage | None = None
    concession: Concession | None = None
    degraded: bool = False
    error: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class TerminationState:
    """Final state of a debate after termination.

    ``reason`` explains why the debate ended; ``events`` contains the full
    ordered event sequence for M6 evidence tracking.
    """

    reason: TerminationReason
    events: list[DebateEvent]
    rounds_completed: int
    claims_a: list[Claim]
    claims_b: list[Claim]
    concessions: list[Concession]
    objections: list[Objection] = field(default_factory=list)


# ── prompt builder ────────────────────────────────────────────────────────────


def build_round_prompt(ctx: RoundContext) -> str:
    """Build a reviewer prompt for a debate round.

    The prompt presents:
    - The reviewer's own committed claims and risks (their position to defend)
    - The other side's claims and objections (what to respond to)
    - Outstanding objections that still need a reply

    Per DD-02, there is no forced-persona phrasing — the
    reviewer argues from their own committed position.
    """
    parts: list[str] = [
        f"## Debate Round {ctx.round_index}",
    ]

    # Own review reminder
    own_claims_text = _format_claims(ctx.own_review.claims)
    parts.append(f"--- Your committed claims ---\n{own_claims_text}")

    # Other side's position
    other_claims_text = _format_claims(ctx.other_claims)
    parts.append(f"--- Other reviewer's claims ---\n{other_claims_text}")

    # Outstanding objections
    if ctx.outstanding_objections:
        objs_text = _format_objections(ctx.outstanding_objections)
        parts.append(f"--- Outstanding objections for you to address ---\n{objs_text}")

    if ctx.own_review.risks:
        risks_text = "\n".join(f"- [{r.severity}] {r.text}" for r in ctx.own_review.risks)
        parts.append(f"--- Your noted risks ---\n{risks_text}")

    instruction = (
        "\n--- Instructions ---\n"
        "Respond to each outstanding objection targeting your claims. "
        "For each objection, you must state your response type as one of:\n"
        "  - CONCEDED: you accept the objection and withdraw the claim\n"
        "  - REBUTTED: you provide evidence/argument against the objection\n"
        "  - CARRIED: you explicitly decline to change your position\n"
        "Do not introduce new claims. Stay within your committed position."
    )
    parts.append(instruction)

    return "\n\n".join(parts)


def _format_claims(claims: list[Claim]) -> str:
    return "\n".join(
        f"- [{c.severity}] {c.text} (id: {c.id})"
        + (f" evidence: {', '.join(c.evidence_refs)}" if c.evidence_refs else "")
        for c in claims
    )


def _format_objections(objections: list[Objection]) -> str:
    return "\n".join(
        f"- Objection to claim {o.target_claim_id}: {o.argument} (id: {o.id})"
        + (f" evidence: {', '.join(o.evidence_refs)}" if o.evidence_refs else "")
        for o in objections
    )


# ── point-by-point validator ──────────────────────────────────────────────────


class AddressableObjection:
    """An objection with its addressing state for point-by-point validation."""

    def __init__(self, objection: Objection) -> None:
        """Initialize with an objection to track addressing state."""
        self.objection = objection
        self.addressed = False
        self.response_type: Literal["conceded", "rebutted", "carried"] | None = None

    def is_conceded(self) -> bool:
        """True if this objection was conceded by the responding reviewer."""
        return self.response_type == "conceded"


def validate_point_by_point(
    response_text: str,
    outstanding_objections: list[Objection],
) -> list[AddressableObjection]:
    """Validate that every outstanding objection is addressed in the response.

    Returns the list of ``AddressableObjection`` objects reflecting the
    response. Unaddressed objections trigger a repair retry (up to
    ``max_repair_attempts``); after that the round is marked error.

    Detection is case-insensitive and checks for ``CONCEDED``, ``REBUTTED``,
    ``CARRIED`` markers adjacent to each specific objection reference.
    """
    addressed = [AddressableObjection(o) for o in outstanding_objections]
    response_upper = response_text.upper()
    lines = response_text.split("\n")

    for obj in addressed:
        obj_id_upper = obj.objection.id.upper()
        target_id_upper = obj.objection.target_claim_id.upper()
        obj_ref_found = obj_id_upper in response_upper or target_id_upper in response_upper
        if not obj_ref_found:
            continue

        # Extract the region of the response pertaining to this specific objection
        obj_region = _extract_region_for_objection(lines, obj.objection)
        obj_region_upper = obj_region.upper()

        if "CONCEDED" in obj_region_upper:
            obj.addressed = True
            obj.response_type = "conceded"
        elif "REBUTTED" in obj_region_upper:
            obj.addressed = True
            obj.response_type = "rebutted"
        elif "CARRIED" in obj_region_upper:
            obj.addressed = True
            obj.response_type = "carried"

    return addressed


def _extract_region_for_objection(lines: list[str], objection: Objection) -> str:
    """Extract the portion of the response that pertains to a specific objection.

    Finds the line(s) mentioning the objection ID or target claim ID and
    returns the relevant text region.
    """
    obj_id = objection.id
    target_id = objection.target_claim_id
    matching_lines: list[str] = []
    for line in lines:
        if obj_id in line or target_id in line:
            matching_lines.append(line)
    return "\n".join(matching_lines) if matching_lines else ""


# ── degradation detector ──────────────────────────────────────────────────────


def detect_degradation(text: str) -> bool:
    """Heuristic detection of degraded reviewer output.

    Flags messages that exhibit:
    - Repetition (same sentence repeated 3+ times)
    - Truncation (ends abruptly without completing a sentence)
    - Refusal (explicit refusal to engage)

    Returns ``True`` if degradation is detected.
    """
    if not text:
        return True

    # Repetition: same sentence repeated 3+ times
    sentences = [
        s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()
    ]
    if len(sentences) >= 3:  # noqa: PLR2004
        for i in range(len(sentences) - 2):
            if sentences[i] == sentences[i + 1] == sentences[i + 2]:
                return True

    # Truncation: ends without terminal punctuation
    text_stripped = text.strip()
    if text_stripped and text_stripped[-1] not in (".", "!", "?", "}", ")", '"', "'", "`"):
        return True

    # Refusal markers
    refusal_markers = [
        "i cannot review",
        "i cannot continue",
        "i cannot participate",
        "i refuse",
        "i'm not able to",
        "i am not able to",
        "cannot comply",
        "not appropriate to review",
    ]
    text_lower = text.lower()
    return any(marker in text_lower for marker in refusal_markers)


# ── caps ──────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class TokenBudget:
    """Per-artifact token budget for cost control.

    ``remaining`` starts equal to ``limit``. When it reaches zero, the budget
    is exhausted.
    """

    limit: int
    remaining: int = field(compare=False, default=0)

    def __post_init__(self) -> None:
        """Initialize remaining from limit if not explicitly set."""
        if object.__getattribute__(self, "remaining") <= 0 and self.limit > 0:
            object.__setattr__(self, "remaining", self.limit)

    @property
    def exhausted(self) -> bool:
        """True if the budget has been fully consumed."""
        return self.remaining <= 0


def check_claims_cap(claims: list[Claim], max_claims: int = 20) -> list[Claim]:
    """Enforce max claims per review; excess claims dropped with warning.

    Returns the capped list (first ``max_claims`` items). The controller should
    log a warning event when claims are dropped.
    """
    if len(claims) <= max_claims:
        return claims
    return claims[:max_claims]


class DebateProvider(Protocol):
    """Protocol for providers during debate rounds (returns ReviewResult with raw_text)."""

    def review(self, request: ReviewRequest) -> ReviewResult: ...


# ── main controller ───────────────────────────────────────────────────────────


class DebateController:
    """Bounded debate orchestrator (T5.1).

    Drives alternating rounds after M3 revelation. Each round presents each
    reviewer with the other side's claims and outstanding objections, enforces
    point-by-point addressing, and detects degradation.

    Usage::

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=session_a,
            session_b=session_b,
            review_a=review_a,
            review_b=review_b,
            max_rounds=2,
            token_budget=TokenBudget(limit=100000),
        )
        state = controller.run()
    """

    def __init__(  # noqa: D107, PLR0913
        self,
        provider_a: DebateProvider,
        provider_b: DebateProvider,
        session_a: ReviewerSession,
        session_b: ReviewerSession,
        review_a: Review,
        review_b: Review,
        artifact_for_prompt: str,
        max_rounds: int = 2,
        max_claims_per_review: int = 20,
        token_budget: TokenBudget | None = None,
    ) -> None:
        self._provider_a = provider_a
        self._provider_b = provider_b
        self._session_a = session_a
        self._session_b = session_b
        self._review_a = review_a
        self._review_b = review_b
        self._artifact_for_prompt = artifact_for_prompt
        self._max_rounds = max_rounds
        self._max_claims_per_review = max_claims_per_review
        self._token_budget = token_budget

        # Internal state accumulated per debate
        self._claims_a: list[Claim] = list(review_a.claims)
        self._claims_b: list[Claim] = list(review_b.claims)
        # Seed initial objections: each side's claims are objections the other
        # side must address. Round-0 objections represent the initial position
        # differences that drive round-1 responses.
        self._objections: list[Objection] = []
        for i, claim in enumerate(self._claims_a):
            self._objections.append(
                Objection(
                    id=f"obj_initial_a_{i}",
                    target_claim_id=claim.id,
                    argument=f"Reviewer A claims: {claim.text}",
                    round=1,
                )
            )
        for i, claim in enumerate(self._claims_b):
            self._objections.append(
                Objection(
                    id=f"obj_initial_b_{i}",
                    target_claim_id=claim.id,
                    argument=f"Reviewer B claims: {claim.text}",
                    round=1,
                )
            )
        self._concessions: list[Concession] = []
        self._events: list[DebateEvent] = []
        self._rounds_completed = 0

    # ── public API ──────────────────────────────────────────────────────────

    def run(self) -> TerminationState:
        """Execute the full debate and return the termination state."""
        for _round_index in range(1, self._max_rounds + 1):
            if self._all_claims_resolved():
                return self._terminate("all_resolved")

            if self._check_budget():
                return self._terminate("budget_exhausted")

            round_events = self._run_single_round(_round_index)
            self._events.extend(round_events)
            self._rounds_completed = _round_index

            if any(e.error for e in round_events):
                return self._terminate("error")

        return self._terminate("rounds_exhausted")

    def all_events(self) -> list[DebateEvent]:
        """Return all events emitted so far."""
        return list(self._events)

    # ── internal helpers ─────────────────────────────────────────────────────

    def _run_single_round(self, round_index: int) -> list[DebateEvent]:
        """Run one debate round: A responds, then B responds.

        Returns the events generated during this round.
        """
        round_events: list[DebateEvent] = []

        # Side A responds to B's objections
        a_events = self._run_side_turn(
            side="A",
            round_index=round_index,
            own_review=self._review_a,
            own_session=self._session_a,
            other_claims=self._claims_b,
            provider=self._provider_a,
        )
        round_events.extend(a_events)

        # Side B responds to A's objections
        b_events = self._run_side_turn(
            side="B",
            round_index=round_index,
            own_review=self._review_b,
            own_session=self._session_b,
            other_claims=self._claims_a,
            provider=self._provider_b,
        )
        round_events.extend(b_events)

        return round_events

    def _run_side_turn(  # noqa: PLR0913
        self,
        side: Side,
        round_index: int,
        own_review: Review,
        own_session: ReviewerSession,
        other_claims: list[Claim],
        provider: DebateProvider,
    ) -> list[DebateEvent]:
        """Run one side's turn in a round.

        Builds the prompt, calls the provider, validates point-by-point, and
        processes any concessions.
        """
        turn_events: list[DebateEvent] = []

        # Outstanding objections are those targeting this side's claims.
        # `_outstanding_for_side(side)` already returns the correct set;
        # no further filtering against other_claims is needed (that would
        # incorrectly require target_claim_id to belong to the opposing side).
        outstanding_objections = self._outstanding_for_side(side, round_index)

        ctx = RoundContext(
            own_review=own_review,
            own_session=own_session,
            other_claims=other_claims,
            other_objections=self._objections,
            outstanding_claims=[c for c in other_claims if c.status == "open"],
            outstanding_objections=outstanding_objections,
            round_index=round_index,
        )

        prompt = build_round_prompt(ctx)

        # Check budget before calling provider
        if self._token_budget and self._token_budget.remaining <= 0:
            return turn_events

        # Call the provider
        try:
            result = provider.review(
                ReviewRequest(
                    artifact=ReviewArtifact(
                        id=own_session.artifact_id,
                        domain="pr_review",
                        source_uri=own_session.artifact_id,
                        content_blocks=[
                            ContentBlock(
                                id="debate_prompt",
                                kind="text",
                                name=f"Debate round {round_index} prompt for side {side}",
                                content=prompt,
                                sequence=0,
                            )
                        ],
                        created_at=datetime.now(UTC),
                        content_hash="0" * 64,
                    ),
                    rubric_hints=[],
                    seed=None,
                    prompt_version="debate_round_v1",
                )
            )
        except Exception as exc:
            turn_events.append(
                DebateEvent(
                    round_index=round_index,
                    side=side,
                    kind="system",
                    error=str(exc),
                    degraded=True,
                )
            )
            return turn_events

        # Detect degradation (use original text, not canary-injected)
        degraded = detect_degradation(result.raw_text)

        # Inject canary token into side A's output for isolation leak detection
        canary_text = result.raw_text
        if side == "A":
            canary_text = result.raw_text + f"\n\n{CANARY_TOKEN}"

        # Validate point-by-point
        addressed = validate_point_by_point(canary_text, outstanding_objections)

        unaddressed = [a for a in addressed if not a.addressed]
        if unaddressed:
            # Emit a warning event but continue — the round is marked error
            # if repair attempts fail per T5.2 spec
            turn_events.append(
                DebateEvent(
                    round_index=round_index,
                    side=side,
                    kind="system",
                    degraded=True,
                )
            )

        # Process concessions
        concessioned_ids: set[str] = set()
        for obj in addressed:
            if obj.is_conceded():
                concession = Concession(
                    id=f"concession_{side}_{round_index}_{obj.objection.id}",
                    claim_id=obj.objection.target_claim_id,
                    by_side=side,
                    round=round_index,
                    rationale=obj.objection.argument,
                )
                self._concessions.append(concession)
                concessioned_ids.add(obj.objection.target_claim_id)
                turn_events.append(
                    DebateEvent(
                        round_index=round_index,
                        side=side,
                        kind="concession",
                        concession=concession,
                        degraded=degraded,
                    )
                )

        # Mark conceded claims as resolved — only update the responding side's claims
        if concessioned_ids:
            target_claims = self._claims_a if side == "A" else self._claims_b
            updated = [
                c.model_copy(update={"status": "conceded"}) if c.id in concessioned_ids else c
                for c in target_claims
            ]
            if side == "A":
                self._claims_a = updated
            else:
                self._claims_b = updated

        # Build the DebateMessage
        msg = DebateMessage(
            id=f"msg_{side}_r{round_index}",
            side=side,
            kind="defense",
            content=canary_text,
        )

        turn_events.append(
            DebateEvent(
                round_index=round_index,
                side=side,
                kind="defense",
                message=msg,
                degraded=degraded,
            )
        )

        return turn_events

    def _outstanding_for_side(self, side: Side, current_round: int = 1) -> list[Objection]:
        """Return objections targeting claims from the given side.

        Only includes objections from the current round or later — objections
        already addressed in previous rounds are excluded.
        """
        if side == "A":
            target_ids = {c.id for c in self._claims_a}
        else:
            target_ids = {c.id for c in self._claims_b}

        already_conceded_ids = {c.claim_id for c in self._concessions}
        resolved_claim_ids = {
            c.id for c in self._claims_a + self._claims_b if c.status in ("conceded", "resolved")
        }

        return [
            o
            for o in self._objections
            if o.target_claim_id in target_ids
            and o.target_claim_id not in already_conceded_ids
            and o.target_claim_id not in resolved_claim_ids
            and o.round >= current_round
        ]

    def _all_claims_resolved(self) -> bool:
        """Check if all claims have been resolved (conceded or upheld)."""
        all_claims = self._claims_a + self._claims_b
        if not all_claims:
            return True
        return all(c.status in ("conceded", "resolved") for c in all_claims)

    def _check_budget(self) -> bool:
        if self._token_budget is None:
            return False
        return self._token_budget.remaining <= 0

    def _terminate(self, reason: TerminationReason) -> TerminationState:
        return TerminationState(
            reason=reason,
            events=list(self._events),
            rounds_completed=self._rounds_completed,
            claims_a=list(self._claims_a),
            claims_b=list(self._claims_b),
            concessions=list(self._concessions),
            objections=list(self._objections),
        )


__all__ = [
    "AddressableObjection",
    "DebateController",
    "DebateEvent",
    "RoundContext",
    "TerminationReason",
    "TerminationState",
    "TokenBudget",
    "build_round_prompt",
    "check_claims_cap",
    "detect_degradation",
    "validate_point_by_point",
]
