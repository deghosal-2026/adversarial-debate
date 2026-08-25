"""Review schemas: isolated reviewer sessions and their committed reviews (PRD §2.3, §2.4).

Session status enum per WBS T1.4: ``isolated|revealed|debating|done|error`` — the
revelation gate transition ``isolated → revealed`` (§2.3) is mechanically enforced
by the engine in M3; this schema carries the state.
"""

from typing import Literal

from pydantic import AwareDatetime, Field, model_validator

from adversarial_debate.schemas.base import SchemaBase
from adversarial_debate.schemas.debate import Claim, Severity, Side

SessionStatus = Literal["isolated", "revealed", "debating", "done", "error"]


class ReviewerSession(SchemaBase):
    """One reviewer's isolated pass over one artifact — PRD §2.4 row 2."""

    id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    side: Side
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    created_at: AwareDatetime
    status: SessionStatus = "isolated"
    error: str | None = None

    @model_validator(mode="after")
    def _error_detail_matches_status(self) -> "ReviewerSession":
        if self.status == "error" and not self.error:
            msg = "error detail required when status is 'error'"
            raise ValueError(msg)
        if self.status != "error" and self.error is not None:
            msg = "error detail only allowed when status is 'error'"
            raise ValueError(msg)
        return self


class Risk(SchemaBase):
    """Hazard note from a review that is not a falsifiable claim (PRD §2.4 row 3)."""

    id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    severity: Severity | None = None


class Review(SchemaBase):
    """A reviewer's committed structured review — PRD §2.4 row 3.

    Immutable after commit: instances are frozen at construction and
    ``committed_at`` marks the commit event the engine persists (M3).
    """

    id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    claims: list[Claim] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    committed_at: AwareDatetime | None = None

    @property
    def is_committed(self) -> bool:
        """True once the engine has stamped ``committed_at`` (§2.3 commit-then-reveal)."""
        return self.committed_at is not None
