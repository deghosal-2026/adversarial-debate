"""PydanticAI adapter tests (WBS T2.3 #10).

PydanticAI is an optional dependency — tests use stub objects via monkeypatch
to verify wrapper logic without installing the heavy lib.
"""

import json
import sys
import types
from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from adversarial_debate.providers.contract import ReviewRequest
from adversarial_debate.providers.pydanticai_adapter import PydanticAIAdapter
from adversarial_debate.schemas.artifact import ContentBlock, ReviewArtifact


class TestPydanticAIAdapter:
    """Verify adapter wraps a stub pydantic_ai Agent correctly."""

    def _stub_pydantic_ai(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Inject a minimal stub pydantic_ai module into sys.modules."""
        stub = types.ModuleType("pydantic_ai")
        stub.Agent = _StubAgent  # type: ignore[attr-defined]
        monkeypatch.setitem(sys.modules, "pydantic_ai", stub)

    def test_returns_review_result(self, monkeypatch: pytest.MonkeyPatch) -> None:
        self._stub_pydantic_ai(monkeypatch)
        adapter = PydanticAIAdapter(base_url="", model="openai:gpt-4o", api_key="sk-test")
        art = _make_artifact("art_001")
        req = ReviewRequest(artifact=art, prompt_version="v1", seed=5)
        result = adapter.review(req)
        assert result.claims[0].text == "stub claim"
        assert result.metadata.seed == 5
        assert result.metadata.prompt_version == "v1"

    def test_missing_extra_raises_import_error(self) -> None:
        if "pydantic_ai" in sys.modules:
            pytest.skip("pydantic_ai is actually installed; run in a clean env")

        adapter = PydanticAIAdapter(base_url="", model="openai:gpt-4o", api_key="sk-test")
        with pytest.raises(ImportError, match="pydantic_ai"):
            adapter.review(ReviewRequest(artifact=_make_artifact("art_002"), prompt_version="v1"))

    def test_non_json_response(self, monkeypatch: pytest.MonkeyPatch) -> None:
        class NonJsonAgent:
            def __init__(self, model: str, **_kwargs: object) -> None:
                pass

            def run_sync(self, _prompt: str) -> object:
                result = MagicMock()
                result.data = "not json at all"
                return result

        stub = types.ModuleType("pydantic_ai")
        stub.Agent = NonJsonAgent  # type: ignore[attr-defined]
        monkeypatch.setitem(sys.modules, "pydantic_ai", stub)

        adapter = PydanticAIAdapter(base_url="", model="openai:gpt-4o", api_key="sk-test")
        art = _make_artifact("art_003")
        req = ReviewRequest(artifact=art, prompt_version="v1")
        result = adapter.review(req)
        assert result.raw_text == "not json at all"
        assert result.claims == []


class _StubAgent:
    """Minimal pydantic_ai.Agent stand-in for testing."""

    def __init__(self, model: str, **_kwargs: object) -> None:
        self._model = model

    def run_sync(self, _prompt: str) -> object:
        result = MagicMock()
        result.data = json.dumps(
            {
                "claims": [
                    {
                        "id": "cl_stub",
                        "review_id": "rv_stub",
                        "text": "stub claim",
                        "severity": "low",
                        "status": "open",
                    }
                ],
                "risks": [],
                "confidence": 0.75,
            }
        )
        return result


def _make_artifact(artifact_id: str = "art_default") -> ReviewArtifact:
    return ReviewArtifact(
        id=artifact_id,
        domain="test",
        source_uri="test://example",
        content_blocks=[ContentBlock(id="blk_1", kind="text", name="test.txt", content="test")],
        created_at=datetime.now(UTC),
        content_hash="d" * 64,
    )
