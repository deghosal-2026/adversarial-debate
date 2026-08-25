"""OpenAI transport tests (WBS T2.2 #9): HTTP POST, retries, timeouts, structured output.

All network access is monkeypatched — real urllib calls never execute.
"""

import json
import urllib.error
import urllib.request
from datetime import UTC, datetime
from http.client import HTTPMessage
from typing import Any
from unittest.mock import MagicMock

import pytest

from adversarial_debate.providers.contract import ReviewRequest
from adversarial_debate.providers.openai_transport import OpenAITransport
from adversarial_debate.schemas.artifact import ContentBlock, ReviewArtifact, RubricHint


class TestBuildBody:
    """OpenAITransport builds correct request bodies."""

    def test_include_seed(self) -> None:
        transport = OpenAITransport(
            base_url="https://api.openai.com/v1", model="gpt-4o", api_key="sk-test"
        )
        art = _make_artifact("art_001")
        req = ReviewRequest(artifact=art, prompt_version="v1", seed=42)
        body = transport._build_body(req)
        assert body["seed"] == 42
        assert body["model"] == "gpt-4o"

    def test_no_seed_when_none(self) -> None:
        transport = OpenAITransport(
            base_url="https://api.openai.com/v1", model="gpt-4o", api_key="sk-test"
        )
        art = _make_artifact("art_001")
        req = ReviewRequest(artifact=art, prompt_version="v1")
        body = transport._build_body(req)
        assert "seed" not in body

    def test_includes_messages(self) -> None:
        transport = OpenAITransport(
            base_url="https://api.openai.com/v1", model="gpt-4o", api_key="sk-test"
        )
        art = _make_artifact("art_001", content="def foo(): pass")
        req = ReviewRequest(artifact=art, prompt_version="v1")
        body = transport._build_body(req)
        assert len(body["messages"]) == 2
        assert body["messages"][0]["role"] == "system"
        assert "def foo(): pass" in body["messages"][0]["content"]

    def test_includes_rubric_hints(self) -> None:
        transport = OpenAITransport(
            base_url="https://api.openai.com/v1", model="gpt-4o", api_key="sk-test"
        )

        art = _make_artifact("art_002")
        hints = [RubricHint(id="rh_1", dimension="security", guidance="Check for SQLi", weight=1.5)]
        req = ReviewRequest(artifact=art, prompt_version="v1", rubric_hints=hints)
        body = transport._build_body(req)
        system_content = body["messages"][0]["content"]
        assert "security" in system_content
        assert "Check for SQLi" in system_content


class TestPost:
    """HTTP POST with retry/backoff — all network calls are faked."""

    def _make_transport(self) -> OpenAITransport:
        return OpenAITransport(base_url="https://api.test/v1", model="gpt-4o", api_key="sk-test")

    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        transport = self._make_transport()

        def fake_urlopen(*_args: Any, **_kwargs: Any) -> MagicMock:
            mock = MagicMock()
            mock.read.return_value = b'{"id":"123","choices":[{"message":{"content":"ok"}}]}'
            return mock

        monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
        result = transport._post({"model": "gpt-4o"})
        assert result["id"] == "123"

    def test_retry_on_429(self, monkeypatch: pytest.MonkeyPatch) -> None:
        transport: OpenAITransport = self._make_transport()
        call_count = [0]

        def fake_urlopen(*_args: Any, **_kwargs: Any) -> MagicMock:
            call_count[0] += 1
            if call_count[0] < 3:
                raise urllib.error.HTTPError(
                    "http://test", 429, "Too Many Requests", HTTPMessage(), None
                )
            mock = MagicMock()
            mock.read.return_value = b'{"id":"123"}'
            return mock

        monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
        result = transport._post({"model": "gpt-4o"})
        assert result["id"] == "123"
        assert call_count[0] == 3

    def test_retry_on_5xx(self, monkeypatch: pytest.MonkeyPatch) -> None:
        transport: OpenAITransport = self._make_transport()
        call_count = [0]

        def fake_urlopen(*_args: Any, **_kwargs: Any) -> MagicMock:
            call_count[0] += 1
            if call_count[0] < 2:
                raise urllib.error.HTTPError("http://test", 502, "Bad Gateway", HTTPMessage(), None)
            mock = MagicMock()
            mock.read.return_value = b'{"id":"456"}'
            return mock

        monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
        result = transport._post({"model": "gpt-4o"})
        assert result["id"] == "456"
        assert call_count[0] == 2

    def test_gives_up_after_max_retries(self, monkeypatch: pytest.MonkeyPatch) -> None:
        transport: OpenAITransport = self._make_transport()

        def fake_urlopen(*_args: Any, **_kwargs: Any) -> MagicMock:
            raise urllib.error.HTTPError(
                "http://test", 503, "Service Unavailable", HTTPMessage(), None
            )

        monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
        with pytest.raises(RuntimeError, match="HTTP 503"):
            transport._post({"model": "gpt-4o"})

    def test_urlerror_retry(self, monkeypatch: pytest.MonkeyPatch) -> None:
        transport: OpenAITransport = self._make_transport()
        call_count = [0]

        def fake_urlopen(*_args: Any, **_kwargs: Any) -> MagicMock:
            call_count[0] += 1
            if call_count[0] < 2:
                raise urllib.error.URLError(reason="connection refused")
            mock = MagicMock()
            mock.read.return_value = b'{"id":"789"}'
            return mock

        monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
        result = transport._post({"model": "gpt-4o"})
        assert result["id"] == "789"

    def test_non_retryable_http_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        transport: OpenAITransport = self._make_transport()

        def fake_urlopen(*_args: Any, **_kwargs: Any) -> MagicMock:
            raise urllib.error.HTTPError("http://test", 400, "Bad Request", HTTPMessage(), None)

        monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
        with pytest.raises(RuntimeError, match="HTTP 400"):
            transport._post({"model": "gpt-4o"})

    def test_timeout_set_on_request(self, monkeypatch: pytest.MonkeyPatch) -> None:
        transport = OpenAITransport(
            base_url="https://api.test/v1", model="gpt-4o", api_key="sk-test", timeout=15.0
        )
        captured_timeout: list[float] = []

        def fake_urlopen(_req: Any, **kwargs: Any) -> MagicMock:
            captured_timeout.append(kwargs.get("timeout", -1))
            mock = MagicMock()
            mock.read.return_value = b"{}"
            return mock

        monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
        transport._post({"model": "gpt-4o"})
        assert captured_timeout[0] == 15.0

    def test_urlerror_gives_up(self, monkeypatch: pytest.MonkeyPatch) -> None:
        transport: OpenAITransport = self._make_transport()

        def fake_urlopen(*_args: Any, **_kwargs: Any) -> MagicMock:
            raise urllib.error.URLError(reason="connection timeout")

        monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
        with pytest.raises(RuntimeError, match="connection error after"):
            transport._post({"model": "gpt-4o"})

    def test_backoff_does_not_raise(self) -> None:
        transport: OpenAITransport = self._make_transport()
        transport._backoff(0)
        transport._backoff(1)
        transport._backoff(2)


class TestParse:
    """Response parsing to ReviewResult."""

    def test_parses_json_content(self) -> None:
        transport = OpenAITransport(
            base_url="https://api.test/v1", model="gpt-4o", api_key="sk-test"
        )
        art = _make_artifact("art_001")
        req = ReviewRequest(artifact=art, prompt_version="v1", seed=7)

        raw_response: dict[str, object] = {
            "id": "chatcmpl-123",
            "model": "gpt-4o-2024-08-06",
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "claims": [
                                    {
                                        "id": "cl_001",
                                        "review_id": "rv_001",
                                        "text": "SQL injection risk",
                                        "severity": "high",
                                        "evidence_refs": ["line:42"],
                                        "status": "open",
                                    }
                                ],
                                "risks": [
                                    {
                                        "id": "risk_001",
                                        "text": "Unvalidated input",
                                        "severity": "high",
                                    }
                                ],
                                "confidence": 0.85,
                            }
                        )
                    }
                }
            ],
        }
        result = transport._parse(raw_response, req)
        assert len(result.claims) == 1
        assert result.claims[0].text == "SQL injection risk"
        assert len(result.risks) == 1
        assert result.risks[0].text == "Unvalidated input"
        assert result.confidence == 0.85
        assert result.metadata.seed == 7
        assert result.metadata.prompt_version == "v1"
        assert result.metadata.usage.total_tokens == 15
        assert "gpt-4o" in result.metadata.model

    def test_graceful_fallback_on_non_json(self) -> None:
        transport = OpenAITransport(
            base_url="https://api.test/v1", model="gpt-4o", api_key="sk-test"
        )
        art = _make_artifact("art_001")
        req = ReviewRequest(artifact=art, prompt_version="v1")

        raw_response: dict[str, object] = {
            "choices": [{"message": {"content": "This is not JSON"}}],
        }
        result = transport._parse(raw_response, req)
        assert result.raw_text == "This is not JSON"
        assert result.claims == []
        assert result.confidence == 0.0

    def test_empty_choices(self) -> None:
        transport = OpenAITransport(
            base_url="https://api.test/v1", model="gpt-4o", api_key="sk-test"
        )
        art = _make_artifact("art_001")
        req = ReviewRequest(artifact=art, prompt_version="v1")

        raw_response: dict[str, object] = {"choices": []}
        result = transport._parse(raw_response, req)
        assert result.raw_text == ""

    def test_usage_none_when_missing(self) -> None:
        transport = OpenAITransport(
            base_url="https://api.test/v1", model="gpt-4o", api_key="sk-test"
        )
        art = _make_artifact("art_001")
        req = ReviewRequest(artifact=art, prompt_version="v1")

        raw_response: dict[str, object] = {"choices": [{"message": {"content": "{}"}}]}
        result = transport._parse(raw_response, req)
        assert result.metadata.usage.prompt_tokens is None


class TestIntegration:
    """Full review() flow with monkeypatched HTTP."""

    def test_review_happy_path(self, monkeypatch: pytest.MonkeyPatch) -> None:
        transport = OpenAITransport(
            base_url="https://api.test/v1", model="gpt-4o", api_key="sk-test"
        )

        def fake_urlopen(*_args: Any, **_kwargs: Any) -> MagicMock:
            mock = MagicMock()
            content = json.dumps(
                {
                    "claims": [
                        {
                            "id": "cl_001",
                            "review_id": "rv_001",
                            "text": "Hardcoded credential",
                            "severity": "high",
                            "status": "open",
                        }
                    ],
                    "risks": [],
                    "confidence": 0.9,
                }
            )
            mock.read.return_value = json.dumps(
                {
                    "id": "test-id",
                    "model": "gpt-4o",
                    "usage": {"prompt_tokens": 20, "completion_tokens": 10, "total_tokens": 30},
                    "choices": [{"message": {"content": content}}],
                }
            ).encode()
            return mock

        monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

        art = _make_artifact("art_001")
        req = ReviewRequest(artifact=art, prompt_version="v1", seed=99)
        result = transport.review(req)
        assert len(result.claims) == 1
        assert result.claims[0].text == "Hardcoded credential"
        assert result.confidence == 0.9
        assert result.metadata.seed == 99
        assert result.metadata.usage.total_tokens == 30


def _make_artifact(artifact_id: str = "art_default", content: str = "test") -> ReviewArtifact:
    return ReviewArtifact(
        id=artifact_id,
        domain="test",
        source_uri="test://example",
        content_blocks=[ContentBlock(id="blk_1", kind="text", name="test.txt", content=content)],
        created_at=datetime.now(UTC),
        content_hash="c" * 64,
    )
