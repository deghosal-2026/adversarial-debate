"""LangGraph adapter tests (WBS T2.4 #11).

LangGraph is an optional dependency — tests use stub objects via monkeypatch
to verify wrapper logic without installing the heavy lib.
"""

import json
import sys
import types
from datetime import UTC, datetime

import pytest

from adversarial_debate.providers.contract import ReviewRequest
from adversarial_debate.providers.langgraph_adapter import LangGraphAdapter
from adversarial_debate.schemas.artifact import ContentBlock, ReviewArtifact


class TestLangGraphAdapter:
    """Verify adapter wraps a stub LangGraph chat model correctly."""

    def _stub_langgraph(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Inject stub langchain_openai module and langchain_core types."""
        stub_lc = types.ModuleType("langchain_openai")
        stub_lc.ChatOpenAI = _StubChatOpenAI  # type: ignore[attr-defined]
        monkeypatch.setitem(sys.modules, "langchain_openai", stub_lc)

        stub_core_messages = types.ModuleType("langchain_core.messages")
        stub_core = types.ModuleType("langchain_core")

        class StubSystemMessage:
            def __init__(self, content: str) -> None:
                self.content = content

        class StubHumanMessage:
            def __init__(self, content: str) -> None:
                self.content = content

        stub_core_messages.SystemMessage = StubSystemMessage  # type: ignore[attr-defined]
        stub_core_messages.HumanMessage = StubHumanMessage  # type: ignore[attr-defined]
        stub_core.messages = stub_core_messages  # type: ignore[attr-defined]
        monkeypatch.setitem(sys.modules, "langchain_core", stub_core)
        monkeypatch.setitem(sys.modules, "langchain_core.messages", stub_core_messages)

    def test_returns_review_result(self, monkeypatch: pytest.MonkeyPatch) -> None:
        self._stub_langgraph(monkeypatch)
        adapter = LangGraphAdapter(base_url="", model="gpt-4o", api_key="sk-test")
        art = _make_artifact("art_001")
        req = ReviewRequest(artifact=art, prompt_version="v1", seed=10)
        result = adapter.review(req)
        assert result.claims[0].text == "langgraph stub claim"
        assert result.metadata.seed == 10

    def test_missing_extra_raises_import_error(self) -> None:
        if "langchain_openai" in sys.modules:
            pytest.skip("langchain_openai is installed; run in a clean env")

        adapter = LangGraphAdapter(base_url="", model="gpt-4o", api_key="sk-test")
        with pytest.raises(ImportError, match="langgraph"):
            adapter.review(ReviewRequest(artifact=_make_artifact("art_002"), prompt_version="v1"))

    def test_non_json_response(self, monkeypatch: pytest.MonkeyPatch) -> None:
        self._stub_langgraph(monkeypatch)

        class StubNonJsonModel:
            def invoke(self, _messages: list[object]) -> object:
                return _StubAIMessage("raw non-json text")

        adapter = LangGraphAdapter(base_url="", model="gpt-4o", api_key="sk-test")
        adapter._llm = StubNonJsonModel()
        art = _make_artifact("art_003")
        req = ReviewRequest(artifact=art, prompt_version="v1")
        result = adapter.review(req)
        assert result.raw_text == "raw non-json text"
        assert result.claims == []


class _StubChatOpenAI:
    """Minimal langchain_openai.ChatOpenAI stand-in for testing."""

    def __init__(self, model: str, api_key: str = "", **_kwargs: object) -> None:
        self.model = model

    def invoke(self, _messages: list[object]) -> object:
        return _StubAIMessage(
            json.dumps(
                {
                    "claims": [
                        {
                            "id": "cl_lg",
                            "review_id": "rv_lg",
                            "text": "langgraph stub claim",
                            "severity": "medium",
                            "status": "open",
                        }
                    ],
                    "risks": [],
                    "confidence": 0.8,
                }
            )
        )


class _StubAIMessage:
    """Minimal langchain_core.messages.AIMessage stand-in."""

    def __init__(self, content: str) -> None:
        self.content = content


def _make_artifact(artifact_id: str = "art_default") -> ReviewArtifact:
    return ReviewArtifact(
        id=artifact_id,
        domain="test",
        source_uri="test://example",
        content_blocks=[ContentBlock(id="blk_1", kind="text", name="test.txt", content="test")],
        created_at=datetime.now(UTC),
        content_hash="e" * 64,
    )
