"""Shared provider contract: ReviewRequest / ReviewResult (WBS T2.1 #8, PRD §6.4).

Every transport, adapter, and scripted reviewer honors this contract so the
engine (M5) is provider-agnostic. ``ReviewResult.metadata`` carries the seed
and prompt_version for transcript reproducibility (PRD §6.4).
"""

from pydantic import Field

from adversarial_debate.schemas.artifact import ReviewArtifact, RubricHint
from adversarial_debate.schemas.base import SchemaBase
from adversarial_debate.schemas.debate import Claim
from adversarial_debate.schemas.review import Risk


class ReviewUsage(SchemaBase):
    """Token-usage stats returned by the provider (best-effort — nullable fields)."""

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


class ReviewResultMetadata(SchemaBase):
    """Metadata stamped on every review result (PRD §6.4 seed + prompt version)."""

    seed: int | None = None
    prompt_version: str = "unknown"
    usage: ReviewUsage = Field(default_factory=ReviewUsage)
    model: str = ""


class ReviewRequest(SchemaBase):
    """Input contract every reviewer backend accepts.

    Fields:
        artifact: The normalized thing under review.
        rubric_hints: Optional claim-extraction guidance shared across reviewers.
        seed: Reproducibility seed (PRD §6.4); None = live non-deterministic.
        prompt_version: Which prompt-template version produced this request.
    """

    artifact: ReviewArtifact
    rubric_hints: list[RubricHint] = Field(default_factory=list)
    seed: int | None = None
    prompt_version: str = "unknown"


class ReviewResult(SchemaBase):
    """Output contract every reviewer backend returns.

    Fields:
        claims: Structured claims identified by the reviewer.
        risks: Non-claim hazards noted by the reviewer.
        confidence: Self-reported confidence in the review.
        raw_text: Unmodified LLM response text (for audit / transcript).
        metadata: Seed, prompt_version, usage, and model information.
    """

    claims: list[Claim] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    raw_text: str = ""
    metadata: ReviewResultMetadata = Field(default_factory=ReviewResultMetadata)

    @property
    def is_empty(self) -> bool:
        """True if no claims or risks were produced."""
        return not self.claims and not self.risks


__all__ = [
    "ReviewRequest",
    "ReviewResult",
    "ReviewResultMetadata",
    "ReviewUsage",
]
