"""Artifact schemas: the normalized thing under review (PRD §2.2 component 1, §2.4).

Naming source of truth: [11-glossary](docs/design/prd/11-glossary.md) ("Artifact").
``detected_language`` per [i18n §22.2](docs/design/prd/22-internationalization.md)
— auto-detected, overridable, never a translation trigger.
"""

from typing import Literal

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
    PositiveFloat,
)


class SchemaBase(BaseModel):
    """Shared config: frozen instances (audit safety), no unknown fields, strict types."""

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)


class ContentBlock(SchemaBase):
    """One reviewable chunk of artifact content (per-file blocks for PRs, PRD §2.8)."""

    id: str = Field(min_length=1)
    kind: Literal["diff", "text", "clause", "log"] = "text"
    name: str = Field(min_length=1)
    content: str
    sequence: NonNegativeInt = 0


class RubricHint(SchemaBase):
    """Claim-extraction rubric hint steering both reviewers equally (PRD §5.3)."""

    id: str = Field(min_length=1)
    dimension: str = Field(min_length=1)
    guidance: str
    weight: PositiveFloat = 1.0


class DetectedLanguage(SchemaBase):
    """Artifact natural language (i18n §22.2): auto-detected by default, overridable."""

    code: str = Field(min_length=2)
    source: Literal["auto_detected", "overridden"] = "auto_detected"
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class ReviewArtifact(SchemaBase):
    """The normalized thing under review — PRD §2.4 row 1, field-for-field.

    ``content_hash`` is the SHA-256 of canonical artifact content (T1.7 utility);
    adapters compute it at normalization time so transcripts can prove integrity.
    """

    id: str = Field(min_length=1)
    domain: str = Field(min_length=1)
    source_uri: str = Field(min_length=1)
    content_blocks: list[ContentBlock] = Field(min_length=1)
    rubric_hints: list[RubricHint] = Field(default_factory=list)
    created_at: AwareDatetime
    content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    detected_language: DetectedLanguage | None = None
    classification_tag: str | None = Field(default=None, min_length=1)
    metadata: dict[str, str] = {}
