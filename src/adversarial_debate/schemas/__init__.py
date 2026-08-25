"""Core Pydantic schemas implementing the PRD [§2.4 data model](docs/design/prd/02-architecture.md).

Canonical entity list — field-for-field. Naming source of truth:
[11-glossary](docs/design/prd/11-glossary.md).
"""

from adversarial_debate.schemas.artifact import (
    ContentBlock,
    DetectedLanguage,
    ReviewArtifact,
    RubricHint,
)
from adversarial_debate.schemas.base import SchemaBase
from adversarial_debate.schemas.debate import (
    Claim,
    ClaimStatus,
    Concession,
    DebateMessage,
    DebateRound,
    Objection,
    Outcome,
    Severity,
    Side,
    UnresolvedPoint,
)
from adversarial_debate.schemas.review import (
    Review,
    ReviewerSession,
    Risk,
    SessionStatus,
)

__all__ = [
    "Claim",
    "ClaimStatus",
    "Concession",
    "ContentBlock",
    "DebateMessage",
    "DebateRound",
    "DetectedLanguage",
    "Objection",
    "Outcome",
    "Review",
    "ReviewArtifact",
    "ReviewerSession",
    "Risk",
    "RubricHint",
    "SchemaBase",
    "SessionStatus",
    "Severity",
    "Side",
    "UnresolvedPoint",
]
