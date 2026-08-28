"""PydanticAI adapter: wraps a PydanticAI model as a reviewer backend (WBS T2.3 #10).

Honours the same ReviewRequest / ReviewResult contract as OpenAITransport.
PydanticAI is an optional dependency — install with ``uv add adversarial-debate[pydanticai]``.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from adversarial_debate.providers.contract import (
    ReviewRequest,
    ReviewResult,
    ReviewResultMetadata,
    ReviewUsage,
)
from adversarial_debate.schemas.debate import Claim
from adversarial_debate.schemas.review import Risk

if TYPE_CHECKING:
    from pydantic_ai import Agent


class PydanticAIAdapter:
    """Wrap a PydanticAI ``Agent`` as a BYOM reviewer.

    Args:
        base_url: Unused by the adapter itself; kept for config compatibility.
        model: PydanticAI model identifier (e.g. ``openai:gpt-4o``).
        api_key: API key for the underlying provider.
    """

    def __init__(self, base_url: str, model: str, api_key: str) -> None:
        """Store config; agent is lazily initialized."""
        self._model_id = model
        self._api_key = api_key
        self._base_url = base_url
        self._agent: Agent | None = None

    def _lazy_init(self) -> None:
        if self._agent is not None:
            return
        try:
            from pydantic_ai import Agent
        except ImportError:
            msg = (
                "pydantic_ai is not installed. Install with: uv add adversarial-debate[pydanticai]"
            )
            raise ImportError(msg) from None
        self._agent = Agent(self._model_id, api_key=self._api_key)

    def review(self, request: ReviewRequest) -> ReviewResult:
        """Run the review via PydanticAI."""
        self._lazy_init()
        assert self._agent is not None

        prompt = self._build_prompt(request)
        result = self._agent.run_sync(prompt)
        raw_text: str = result.data if isinstance(result.data, str) else str(result.data)

        metadata = ReviewResultMetadata(
            seed=request.seed,
            prompt_version=request.prompt_version,
            usage=ReviewUsage(),
            model=self._model_id,
        )

        try:
            parsed = json.loads(raw_text)
        except (json.JSONDecodeError, TypeError):
            return ReviewResult(raw_text=raw_text, confidence=0.0, metadata=metadata)

        claims = [Claim(**c) for c in parsed.get("claims", [])]
        risks = [Risk(**r) for r in parsed.get("risks", [])]
        confidence = float(parsed.get("confidence", 0.0))

        return ReviewResult(
            claims=claims,
            risks=risks,
            confidence=confidence,
            raw_text=raw_text,
            metadata=metadata,
        )

    def _build_prompt(self, request: ReviewRequest) -> str:
        parts = [
            "Review the following artifact and produce a structured JSON response.",
            f"Source: {request.artifact.source_uri}",
        ]
        for block in request.artifact.content_blocks:
            parts.append(f"--- {block.name} ({block.kind}) ---")
            parts.append(block.content)
        parts.append('Respond with JSON: {"claims": [...], "risks": [...], "confidence": <0..1>}')
        return "\n".join(parts)


__all__ = ["PydanticAIAdapter"]
