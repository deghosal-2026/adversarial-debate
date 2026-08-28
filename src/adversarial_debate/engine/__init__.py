"""Isolation engine: ReviewerSessionManager, RevelationGate, AuditEvent, IsolationViolation.

Mechanically enforces the revelation gate ``isolated → revealed`` (PRD §2.3)
and provides the reviewer-backend Protocol for M3 → M2 wiring.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable

from adversarial_debate.schemas import Review, ReviewerSession, Side

# ── public exception ──────────────────────────────────────────────────────────


class IsolationViolation(Exception):  # noqa: N818  # spec requires this exact name
    """Raised when cross-context leakage is detected or the revelation gate is violated.

    This is the single, loud failure mode for M3 isolation invariants (WBS T3.4, §6.1).
    """


# ── audit event ───────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class AuditEvent:
    """One state-transition record emitted by the RevelationGate (in-memory, M3 scope)."""

    actor: str
    action: str
    from_state: str
    to_state: str
    timestamp: datetime


# ── backend Protocol ──────────────────────────────────────────────────────────


@runtime_checkable
class ReviewerBackend(Protocol):
    """Abstract contract for M2 providers consumed by M3.

    A ReviewerBackend takes a ``ReviewRequest`` and returns a ``Review``.
    The engine never shares a backend instance between sides, nor does it
    peek at one side's review before handing to the other.
    """

    def run(self, request: ReviewRequest) -> Review:
        """Execute a single review pass and return a structured Review."""
        ...


@dataclass(frozen=True)
class ReviewRequest:
    """Input to a ReviewerBackend — the artifact content plus hints."""

    artifact_id: str
    side: Side
    artifact_content: str
    rubric_hints: list[str]  # serialised rubric hint texts


# ── session manager ───────────────────────────────────────────────────────────


# The lifecycle is: isolated → revealed → debating → done | error
# (WBS M3 status lifecycle). Error is always reachable.
_SESSION_STATUS_TRANSITIONS: dict[str, set[str]] = {
    "isolated": {"revealed", "error"},
    "revealed": {"debating", "error"},
    "debating": {"done", "error"},
    "done": set(),
    "error": set(),
}


class ReviewerSessionManager:
    """Creates and tracks exactly two reviewer sessions per artifact (T3.1/#14).

    Sessions are distinct objects with no shared mutable references. The manager
    owns the authoritative session registry; downstream code reads from it.
    """

    def __init__(self) -> None:
        """Initialize an empty session registry."""
        self._sessions: dict[str, ReviewerSession] = {}
        self._initialized = False

    def create_sessions(  # noqa: PLR0913
        self,
        artifact_id: str,
        provider_a: str,
        model_a: str,
        provider_b: str,
        model_b: str,
        created_at: datetime,
    ) -> list[ReviewerSession]:
        """Create exactly two sessions — one per side. Raises if already initialized."""
        if self._initialized:
            msg = "session manager already initialized for an artifact"
            raise RuntimeError(msg)
        self._initialized = True

        session_a = ReviewerSession(
            id=f"sess_{artifact_id}_A",
            artifact_id=artifact_id,
            side="A",
            provider=provider_a,
            model=model_a,
            created_at=created_at,
            status="isolated",
        )
        session_b = ReviewerSession(
            id=f"sess_{artifact_id}_B",
            artifact_id=artifact_id,
            side="B",
            provider=provider_b,
            model=model_b,
            created_at=created_at,
            status="isolated",
        )
        self._sessions[session_a.id] = session_a
        self._sessions[session_b.id] = session_b
        return [session_a, session_b]

    def get_session(self, session_id: str) -> ReviewerSession | None:
        """Look up a session by id."""
        return self._sessions.get(session_id)

    def update_status(
        self, session_id: str, status: str, error: str | None = None
    ) -> ReviewerSession:
        """Update session status with transition validation."""
        session = self._sessions.get(session_id)
        if session is None:
            msg = f"unknown session: {session_id}"
            raise ValueError(msg)

        allowed = _SESSION_STATUS_TRANSITIONS.get(session.status, set())
        if status not in allowed:
            msg = f"invalid status transition: {session.status} -> {status}"
            raise ValueError(msg)

        update_kwargs: dict[str, object] = {"status": status}
        if status == "error":
            update_kwargs["error"] = error
        elif error is not None:
            msg = "error detail only allowed when status is 'error'"
            raise ValueError(msg)

        updated = session.model_copy(update=update_kwargs)
        self._sessions[session_id] = updated
        return updated

    @property
    def all_sessions(self) -> list[ReviewerSession]:
        """Return all tracked sessions."""
        return list(self._sessions.values())

    @property
    def sessions_a(self) -> ReviewerSession | None:
        """Session for side A, if created."""
        for s in self._sessions.values():
            if s.side == "A":
                return s
        return None

    @property
    def sessions_b(self) -> ReviewerSession | None:
        """Session for side B, if created."""
        for s in self._sessions.values():
            if s.side == "B":
                return s
        return None


# ── revelation gate ───────────────────────────────────────────────────────────


class RevelationGate:
    """Explicit state machine enforcing the revelation invariant (T3.2/#15).

    ``reveal()`` is only callable when both sessions hold committed reviews
    (status == done). Every transition emits an ``AuditEvent``.
    """

    def __init__(self) -> None:
        """Initialize an empty gate with no sessions or reviews."""
        self._sessions: dict[str, ReviewerSession] = {}
        self._reviews: dict[str, Review] = {}
        self._revealed = False
        self._audit_log: list[AuditEvent] = []

    def register_session(self, session: ReviewerSession) -> None:
        """Register a session for gate tracking."""
        self._sessions[session.id] = session

    def register_review(self, session_id: str, review: Review) -> None:
        """Register a committed review for a session."""
        self._reviews[session_id] = review

    def reveal(self) -> list[ReviewerSession]:
        """Transition both sessions to revealed — or raise IsolationViolation."""
        if self._revealed:
            msg = "revelation gate already revealed"
            raise IsolationViolation(msg)

        if len(self._sessions) < 2:  # noqa: PLR2004  # exactly two sessions required
            msg = "no sessions registered — cannot reveal"
            raise IsolationViolation(msg)

        for session in self._sessions.values():
            if session.status != "done":
                msg = (
                    f"session {session.id} is not ready (status={session.status}, expected 'done')"
                )
                raise IsolationViolation(msg)

            review = self._reviews.get(session.id)
            if review is None or not review.is_committed:
                msg = f"session {session.id} review is not committed (committed_at is None)"
                raise IsolationViolation(msg)

        self._revealed = True
        now = datetime.now()

        results: list[ReviewerSession] = []
        for session in self._sessions.values():
            updated = session.model_copy(update={"status": "revealed"})
            self._sessions[session.id] = updated
            results.append(updated)

            self._audit_log.append(
                AuditEvent(
                    actor="engine",
                    action="reveal",
                    from_state="isolated",
                    to_state="revealed",
                    timestamp=now,
                )
            )

        return results

    @property
    def audit_log(self) -> list[AuditEvent]:
        """Immutable snapshot of all emitted audit events."""
        return list(self._audit_log)


__all__ = [
    "AuditEvent",
    "IsolationViolation",
    "RevelationGate",
    "ReviewRequest",
    "ReviewerBackend",
    "ReviewerSessionManager",
]
