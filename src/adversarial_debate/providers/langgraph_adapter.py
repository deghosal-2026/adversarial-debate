"""LangGraph adapter: wraps a LangGraph chat model node as a reviewer backend (WBS T2.4 #11).

Honours the same ReviewRequest / ReviewResult contract as OpenAITransport.
LangGraph is an optional dependency — install with ``uv add adversarial-debate[langgraph]``.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from adversarial_debate.providers.contract import (
    ReviewRequest,
    ReviewResult,
    ReviewResultMetadata,
    ReviewUsage,
)
from adversarial_debate.schemas.debate import Claim
from adversarial_debate.schemas.review import Risk

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel


class LangGraphAdapter:
    """Wrap a LangGraph-compatible chat model as a BYOM reviewer.

    Args:
        base_url: Base URL for the chat model endpoint.
        model: Model identifier (e.g. ``gpt-4o``).
        api_key: API key for the underlying provider.
    """

    def __init__(self, base_url: str, model: str, api_key: str) -> None:
        """Store config; chat model is lazily initialized."""
        self._model_id = model
        self._api_key = api_key
        self._base_url = base_url
        self._llm: BaseChatModel | None = None

    def _lazy_init(self) -> None:
        if self._llm is not None:
            return
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            msg = "langgraph is not installed. Install with: uv add adversarial-debate[langgraph]"
            raise ImportError(msg) from None
        self._llm = ChatOpenAI(model=self._model_id, api_key=self._api_key)

    def review(self, request: ReviewRequest) -> ReviewResult:
        """Run the review via LangGraph."""
        self._lazy_init()
        assert self._llm is not None

        messages = self._build_messages(request)
        result = self._llm.invoke(messages)
        raw_text: str = result.content if isinstance(result.content, str) else str(result.content)

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

    def _build_messages(self, request: ReviewRequest) -> list[Any]:
        """Build LangChain message list from the review request."""
        from langchain_core.messages import (
            HumanMessage,
            SystemMessage,
        )

        system = "You are a code reviewer. Respond with structured JSON."
        user_parts = [f"Source: {request.artifact.source_uri}"]
        for block in request.artifact.content_blocks:
            user_parts.append(f"--- {block.name} ({block.kind}) ---")
            user_parts.append(block.content)
        user_parts.append(
            'Respond with JSON: {"claims": [...], "risks": [...], "confidence": <0..1>}'
        )
        return [
            SystemMessage(content=system),
            HumanMessage(content="\n".join(user_parts)),
        ]


__all__ = ["LangGraphAdapter"]
