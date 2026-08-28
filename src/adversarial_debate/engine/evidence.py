"""Evidence tracker, convergence scoring, theater detection, evidence-ref validation.

M6 core (T6.1-T6.4). Consumes M5 DebateEvent/TerminationState and produces
the claim-state finalization that M7 synthesis reads. Key invariants:

- Claim transitions are append-only records (DD-04: concessions are events, not edits)
- Convergence is claim-state-based (DD-08: never semantic-similarity)
- Theater and capitulation-cascade are computed flags, not judgments
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal, cast

from adversarial_debate.engine.debate_controller import (
    DebateEvent,
)
from adversarial_debate.schemas import Claim, ContentBlock
from adversarial_debate.schemas.debate import ClaimStatus, Concession, Objection, Severity

CANARY_TOKEN = "CANARY_ISOLATION_CHECK_8f3a2b"
"""Token injected into side A's output to detect isolation leaks to side B."""


@dataclass(frozen=True)
class ResolutionEvent:
    """Append-only record of a claim state transition (T6.1).

    Each transition is a separate event — claims are never mutated in place.
    The ``round`` field links back to the debate round that triggered it.
    """

    claim_id: str
    from_status: str
    to_status: str
    round: int
    rationale: str = ""
    by_side: str | None = None


@dataclass(frozen=True)
class ClaimSnapshot:
    """Immutable snapshot of a claim at debate end.

    ``final_status`` is the terminal state after all transitions have been
    applied. ``transition_count`` is the number of transitions this claim
    underwent.
    """

    id: str
    text: str
    severity: Severity
    final_status: str
    transition_count: int
    evidence_refs: list[str]


@dataclass(frozen=True)
class EvidenceContext:
    """Full evidence tracking output consumed by M7 synthesis.

    ``convergence_score`` is resolved / total (T6.2).
    ``theater`` is true when no state changes occurred (T6.3).
    ``capitulation_cascade`` is true when >=80% of round-1 concessions with no rebuttals.
    ``canary_leak`` is true if a canary token from side A was detected in side B's output.
    """

    convergence_score: float
    resolved_count: int
    total_claims: int
    verdict_kind: Literal["verdict", "disputed"]
    theater: bool
    capitulation_cascade: bool
    claims: list[ClaimSnapshot]
    transitions: list[ResolutionEvent]
    unverified_claims: list[str]
    canary_leak: bool = False


# ── T6.1 (#27) EvidenceTracker ───────────────────────────────────────────────


class EvidenceTracker:
    """Applies debate events to claim lifecycle and produces a final context.

    Usage::

        tracker = EvidenceTracker(all_claims, all_concessions, all_events)
        context = tracker.compute()
    """

    def __init__(
        self,
        claims: list[Claim],
        concessions: list[Concession],
        events: list[DebateEvent],
        objections: list[Objection] | None = None,
    ) -> None:
        """Initialize tracker with initial claims, concessions, events, and objections."""
        self._initial_claims = {c.id: c for c in claims}
        self._concessions = list(concessions)
        self._events = list(events)
        self._objections = list(objections) if objections else []

        # Internal accumulators
        self._transitions: list[ResolutionEvent] = []
        self._resolved_ids: set[str] = set()

    def compute(self) -> EvidenceContext:
        """Apply all events and return the final evidence context.

        Steps:
        1. Apply concessions as claim transitions
        2. Apply debate events for status changes based on content
        3. Compute convergence score and detect anomalies
        """
        self._apply_concessions()
        self._apply_debate_events()

        total = len(self._initial_claims)
        resolved = len(self._resolved_ids)
        score = resolved / total if total > 0 else 1.0
        verdict: Literal["verdict", "disputed"] = "verdict" if resolved == total else "disputed"

        snapshots = self._build_snapshots()
        theater = self._detect_theater()
        cascade = self._detect_capitulation_cascade()
        unverified = self._find_unverified_claims()
        leak = self._detect_leak()

        return EvidenceContext(
            convergence_score=score,
            resolved_count=resolved,
            total_claims=total,
            verdict_kind=verdict,
            theater=theater,
            capitulation_cascade=cascade,
            claims=snapshots,
            transitions=list(self._transitions),
            unverified_claims=unverified,
            canary_leak=leak,
        )

    def _apply_concessions(self) -> None:
        """Apply each concession as a claim transition."""
        for concession in self._concessions:
            claim = self._initial_claims.get(concession.claim_id)
            if claim is None:
                continue

            self._transitions.append(
                ResolutionEvent(
                    claim_id=concession.claim_id,
                    from_status=claim.status,
                    to_status="conceded",
                    round=concession.round,
                    rationale=concession.rationale,
                    by_side=concession.by_side,
                )
            )
            self._resolved_ids.add(concession.claim_id)

    def _apply_debate_events(self) -> None:
        """Apply debate events to update claim statuses.

        Events with kind "concession" that carry a concession object have
        already been processed by _apply_concessions. Here we look for
        events that signal a claim was upheld (e.g., a rebuttal with
        evidence that the other side accepted).
        """
        for event in self._events:
            if event.kind != "defense":
                continue
            if event.message is None:
                continue
            # Scan defense text for evidence that a claim was upheld
            # Heuristic: patterns like "UPHELD", "ACCEPTED", "AGREED"
            text = event.message.content.upper()
            if "UPHELD" in text or "AGREED" in text or "ACCEPTED" in text:
                # Find claim ids referenced in this defense
                content = event.message.content
                for claim_id in self._initial_claims:
                    if claim_id in content and claim_id not in self._resolved_ids:
                        self._transitions.append(
                            ResolutionEvent(
                                claim_id=claim_id,
                                from_status=self._initial_claims[claim_id].status,
                                to_status="upheld",
                                round=event.round_index,
                                rationale="Accepted during debate",
                                by_side=event.side,
                            )
                        )
                        self._resolved_ids.add(claim_id)

    def _build_snapshots(self) -> list[ClaimSnapshot]:
        """Build final snapshots for all claims."""
        snapshots: list[ClaimSnapshot] = []
        for claim in self._initial_claims.values():
            final_status: ClaimStatus = claim.status
            t_count = sum(1 for t in self._transitions if t.claim_id == claim.id)
            if claim.id in self._resolved_ids and claim.status == "open":
                # Use the last transition for the final status
                for t in self._transitions:
                    if t.claim_id == claim.id:
                        final_status = cast("ClaimStatus", t.to_status)

            snapshots.append(
                ClaimSnapshot(
                    id=claim.id,
                    text=claim.text,
                    severity=claim.severity,
                    final_status=final_status,
                    transition_count=t_count,
                    evidence_refs=list(claim.evidence_refs),
                )
            )
        return snapshots

    # ── T6.3 (#29) — Theater & capitulation ─────────────────────────────

    def _detect_theater(self) -> bool:
        """True if no state changes occurred during the debate.

        No concessions AND no defense responses = the debate was theater.
        If sides at least addressed objections (even with CARRIED), that's a
        real (if stubborn) debate, not theater.
        """
        if not self._concessions and not self._transitions:
            # Check if any defense events happened — if sides responded to
            # objections (even with CARRIED), the debate was real
            has_defense = any(e.kind == "defense" for e in self._events)
            if has_defense:
                return False
            # No defense, no concessions, no transitions = theater
            return all(claim.status == "open" for claim in self._initial_claims.values())

        # If we have only seeding transitions (concessions we applied)
        # and no actual debate-driven changes, it's still theater
        debate_transitions = self._count_debate_transitions()
        return debate_transitions == 0

    def _detect_capitulation_cascade(self) -> bool:
        """True when >=80% of round-1 concessions with zero rebuttals (FM-2)."""
        if not self._concessions:
            return False

        round_1_concessions = [c for c in self._concessions if c.round == 1]
        if not round_1_concessions:
            return False

        total_round_1 = len(round_1_concessions)
        if total_round_1 < 1:
            return False

        round_1_objections = [o for o in self._objections if o.round == 1]
        denominator = max(len(round_1_objections), 1)
        cap_ratio = total_round_1 / denominator
        has_rebuttals = any(
            e.kind == "defense"
            and e.message is not None
            and "REBUTTED" in e.message.content.upper()
            for e in self._events
        )

        capitulation_threshold = 0.8
        return cap_ratio >= capitulation_threshold and not has_rebuttals

    def _count_debate_transitions(self) -> int:
        """Count transitions that were driven by debate events, not initial setup."""
        return len(self._transitions)

    # ── T6.4 (#30) — Evidence reference validation ──────────────────────

    def _find_unverified_claims(self) -> list[str]:
        """Find claims where evidence_refs cannot be resolved.

        For v0.1, we check that:
        - Non-empty refs are present for high-severity claims (FM-7 guard)
        - Refs follow the pattern expected by the artifact store
        """
        unverified: list[str] = []
        for claim in self._initial_claims.values():
            refs = claim.evidence_refs
            if claim.severity == "high" and not refs:
                unverified.append(claim.id)
            elif not refs:
                continue
            else:
                # Basic format validation: each ref should match
                # expected patterns like file:line or content-block-id
                for ref in refs:
                    if not self._ref_looks_valid(ref):
                        unverified.append(claim.id)
                        break
        return unverified

    def _ref_looks_valid(self, ref: str) -> bool:
        """Check a single ref looks like a valid evidence reference.

        Acceptable patterns:
        - ``path/file.py:NN-NN`` (file + line range)
        - ``path/file.py:NN`` (file + single line)
        - bare content block id
        """
        if not ref:
            return False
        # file:line pattern
        if re.match(r"^[\w./-]+:\d+(-\d+)?$", ref):
            return True
        # plain block id (alphanumeric plus _ and -)
        return bool(re.match(r"^[a-zA-Z0-9_-]+$", ref))

    def validate_evidence(
        self,
        content_blocks: list[ContentBlock],
    ) -> list[str]:
        """Cross-check evidence_refs against actual artifact content blocks.

        Returns a list of claim ids whose refs could not be resolved
        to any content block. This is the full validation for M6 exit gate.
        """
        block_ids = {b.id for b in content_blocks}
        unresolved: list[str] = []

        for claim in self._initial_claims.values():
            for ref in claim.evidence_refs:
                # Extract block id from ref (before the colon if present)
                # Preserve the exact block ID — do not strip leading ./ or /
                block_candidate = ref.split(":")[0]
                if block_candidate not in block_ids:
                    unresolved.append(claim.id)
                    break

        return unresolved

    def _detect_leak(self) -> bool:
        """Detect whether side B's output contains side A's canary token.

        If the canary injected into A's debate response appears in any of B's
        defense messages, isolation has been violated. Returns True on leak.
        """
        for event in self._events:
            if event.side != "B":
                continue
            if event.message is not None and CANARY_TOKEN in event.message.content:
                return True
        return False


__all__ = [
    "ClaimSnapshot",
    "EvidenceContext",
    "EvidenceTracker",
    "ResolutionEvent",
]
