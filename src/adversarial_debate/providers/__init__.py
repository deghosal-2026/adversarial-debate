"""BYOM provider layer (F8): config-driven registry, OpenAI-compatible transport, adapters.

Zero paid LLM calls in CI — scripted reviewers for hermetic tests (PRD §2.5).
"""

from adversarial_debate.providers.contract import (
    ReviewRequest,
    ReviewResult,
    ReviewResultMetadata,
    ReviewUsage,
)
from adversarial_debate.providers.registry import ProviderRegistry

__all__ = [
    "ProviderRegistry",
    "ReviewRequest",
    "ReviewResult",
    "ReviewResultMetadata",
    "ReviewUsage",
]
