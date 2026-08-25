"""Debate schemas: first-class evidence objects (PRD §2.4 rows 4-9, §2.7, F3).

Lifecycle semantics per [11-glossary](docs/design/prd/11-glossary.md): a concession
is a new event, never an edit; convergence is claim-state-based (DD-08), and
``would_resolve_if`` is mandatory on every unresolved point (DD-06).
"""

from typing import Literal

from pydantic import (
    AwareDatetime,
    Field,
    NonNegativeInt,
    PositiveInt,
    computed_field,
    model_validator,
)

from adversarial_debate.schemas.base import SchemaBase

Side = Literal["A", "B"]
Severity = Literal["low", "medium", "high"]
ClaimStatus = Literal["open", "conceded", "upheld", "resolved"]


class Claim(SchemaBase):
    """Structured reviewer assertion with status lifecycle ``open → conceded|upheld|resolved``.

    PRD §2.4 row 4. Concessions never mutate a claim — they are separate
    [Concession][adversarial_debate.schemas.debate.Concession] events.
    """

    id: str = Field(min_length=1)
    review_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    severity: Severity
    evidence_refs: list[str] = Field(default_factory=list)
    status: ClaimStatus = "open"


class Objection(SchemaBase):
    """Structured challenge from one reviewer targeting the other's claim (glossary)."""

    id: str = Field(min_length=1)
    target_claim_id: str = Field(min_length=1)
    argument: str = Field(min_length=1)
    round: PositiveInt  # debate rounds are 1-based; round 0 is the isolated review pass
    evidence_refs: list[str] = Field(default_factory=list)


class Concession(SchemaBase):
    """Formal withdrawal/modification of a claim in response to an objection (glossary)."""

    id: str = Field(min_length=1)
    claim_id: str = Field(min_length=1)
    by_side: Side
    round: PositiveInt
    rationale: str = Field(min_length=1)


class UnresolvedPoint(SchemaBase):
    """Disagreement surviving all rounds. ``would_resolve_if`` is mandatory (DD-06)."""

    id: str = Field(min_length=1)
    claim_ids: list[str] = Field(min_length=1)
    position_a: str = Field(min_length=1)
    position_b: str = Field(min_length=1)
    would_resolve_if: str = Field(min_length=1)


class DebateMessage(SchemaBase):
    """One turn inside a debate round; full LLM lineage lives in the transcript."""

    id: str = Field(min_length=1)
    side: Side
    kind: Literal["statement", "objection", "defense", "concession"]
    content: str = Field(min_length=1)


class DebateRound(SchemaBase):
    """Bounded debate round container — PRD §2.4 row 8. Rounds are 1-based."""

    id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    index: PositiveInt
    messages: list[DebateMessage] = Field(default_factory=list)
    started_at: AwareDatetime
    ended_at: AwareDatetime | None = None


class Outcome(SchemaBase):
    """Terminal result — verdict when converged, disputed otherwise (PRD §2.7, F5/F6).

    ``convergence_score`` = resolved_claims / total_claims, computed from the
    stored counts so reports can never hide the denominator (§2.7).
    """

    id: str = Field(min_length=1)
    artifact_id: str = Field(min_length=1)
    kind: Literal["verdict", "disputed"]
    converged_count: NonNegativeInt
    total_claims: PositiveInt
    report_ref: str = Field(min_length=1)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def convergence_score(self) -> float:
        """Fraction of claims converged: ``resolved_claims / total_claims`` (PRD §2.7)."""
        return self.converged_count / self.total_claims

    @model_validator(mode="after")
    def _counts_consistent(self) -> "Outcome":
        if self.converged_count > self.total_claims:
            msg = "converged_count cannot exceed total_claims"
            raise ValueError(msg)
        return self


__all__ = [
    "Claim",
    "ClaimStatus",
    "Concession",
    "DebateMessage",
    "DebateRound",
    "Objection",
    "Outcome",
    "Severity",
    "Side",
    "UnresolvedPoint",
]
