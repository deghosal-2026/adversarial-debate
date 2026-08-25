"""ProviderRegistry tests (WBS T2.1 #8): config → instances, pair_mode, errors."""

from datetime import UTC, datetime

import pytest

from adversarial_debate.config import AdvdebConfig, ConfigError, ProviderConfig, ProvidersConfig
from adversarial_debate.providers.contract import ReviewRequest
from adversarial_debate.providers.langgraph_adapter import LangGraphAdapter
from adversarial_debate.providers.openai_transport import OpenAITransport
from adversarial_debate.providers.pydanticai_adapter import PydanticAIAdapter
from adversarial_debate.providers.registry import (
    _REVIEWER_FACTORIES,
    ProviderRegistry,
    _factory_langgraph,
    _factory_openai,
    _factory_pydantic_ai,
    _factory_scripted,
    _infer_family,
    _resolve_key,
)
from adversarial_debate.providers.scripted_reviewer import ScriptedReviewer
from adversarial_debate.schemas.artifact import ContentBlock, ReviewArtifact


class TestFamilyInference:
    """_infer_family maps model identifiers to family strings."""

    def test_openai(self) -> None:
        assert _infer_family("gpt-4o") == "openai"
        assert _infer_family("gpt-4-turbo") == "openai"
        assert _infer_family("o1-mini") == "openai"
        assert _infer_family("o3-2025-04-17") == "openai"

    def test_anthropic(self) -> None:
        assert _infer_family("claude-sonnet-4-5") == "anthropic"
        assert _infer_family("claude-3-opus") == "anthropic"

    def test_google(self) -> None:
        assert _infer_family("gemini-2.0-flash") == "google"
        assert _infer_family("gemini-1.5-pro") == "google"

    def test_third_party_prefix(self) -> None:
        assert _infer_family("mistral/mistral-large") == "mistral"
        assert _infer_family("groq/llama3") == "groq"

    def test_unknown(self) -> None:
        assert _infer_family("custom-model-v1") == "other"


class TestResolveKey:
    """_resolve_key reads env vars or raises ConfigError."""

    def test_missing_env_raises(self) -> None:
        with pytest.raises(ConfigError) as exc:
            _resolve_key("ADVDEB_NONEXISTENT_KEY_XXXXXX", "a")
        assert "providers.a" in str(exc.value)

    def test_present_env_returns_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ADVDEB_TEST_KEY", "sk-test-123")
        assert _resolve_key("ADVDEB_TEST_KEY", "b") == "sk-test-123"


class TestFactoryFunctions:
    """Internal factory functions produce correct provider instances."""

    def test_factory_openai(self) -> None:
        cfg = ProviderConfig(type="openai_compatible", model="gpt-4o", key_env="TEST_KEY")
        instance = _factory_openai(cfg, "sk-test")
        assert isinstance(instance, OpenAITransport)

    def test_factory_scripted(self) -> None:
        cfg = ProviderConfig(type="scripted", model="test", key_env="TEST_KEY")
        instance = _factory_scripted(cfg, "sk-test")
        assert isinstance(instance, ScriptedReviewer)

    def test_factory_pydantic_ai(self) -> None:
        cfg = ProviderConfig(type="pydantic_ai", model="openai:gpt-4o", key_env="TEST_KEY")
        instance = _factory_pydantic_ai(cfg, "sk-test")
        assert isinstance(instance, PydanticAIAdapter)

    def test_factory_langgraph(self) -> None:
        cfg = ProviderConfig(type="langgraph", model="gpt-4o", key_env="TEST_KEY")
        instance = _factory_langgraph(cfg, "sk-test")
        assert isinstance(instance, LangGraphAdapter)


class TestProviderRegistry:
    """ProviderRegistry creates instances from AdvdebConfig."""

    def _make_config(self, model_a: str, model_b: str) -> AdvdebConfig:
        """Build an AdvdebConfig with scripted reviewers (no network)."""
        return AdvdebConfig(
            providers=ProvidersConfig(
                a=ProviderConfig(type="scripted", model=model_a, key_env="ADVDEB_A_KEY"),
                b=ProviderConfig(type="scripted", model=model_b, key_env="ADVDEB_B_KEY"),
            ),
        )

    def test_create(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ADVDEB_A_KEY", "key-a")
        monkeypatch.setenv("ADVDEB_B_KEY", "key-b")
        config = self._make_config("gpt-4o", "claude-sonnet-4-5")
        registry = ProviderRegistry(config)
        assert registry.pair_mode == "diverse"
        assert registry.families == {"a": "openai", "b": "anthropic"}

    def test_same_family_pair(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ADVDEB_A_KEY", "key-a")
        monkeypatch.setenv("ADVDEB_B_KEY", "key-b")
        config = self._make_config("gpt-4o", "gpt-4-turbo")
        registry = ProviderRegistry(config)
        assert registry.pair_mode == "same"

    def test_unknown_type(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ADVDEB_A_KEY", "key-a")
        monkeypatch.setenv("ADVDEB_B_KEY", "key-b")
        config = AdvdebConfig(
            providers=ProvidersConfig(
                a=ProviderConfig(type="nonexistent_driver", model="gpt-4o", key_env="ADVDEB_A_KEY"),
                b=ProviderConfig(type="scripted", model="claude-3", key_env="ADVDEB_B_KEY"),
            ),
        )
        with pytest.raises(ConfigError) as exc:
            ProviderRegistry(config)
        assert "nonexistent_driver" in str(exc.value)

    def test_missing_env_in_slot(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ADVDEB_A_KEY", "key-a")
        config = AdvdebConfig(
            providers=ProvidersConfig(
                a=ProviderConfig(type="scripted", model="gpt-4o", key_env="ADVDEB_A_KEY"),
                b=ProviderConfig(type="scripted", model="claude-3", key_env="ADVDEB_B_MISSING"),
            ),
        )
        with pytest.raises(ConfigError) as exc:
            ProviderRegistry(config)
        assert "providers.b" in str(exc.value)

    def test_review_dispatches_to_instance(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ADVDEB_A_KEY", "key-a")
        monkeypatch.setenv("ADVDEB_B_KEY", "key-b")
        config = self._make_config("gpt-4o", "claude-sonnet-4-5")
        registry = ProviderRegistry(config)

        art = _make_artifact("art_test_123")
        req = ReviewRequest(artifact=art, prompt_version="test_v1")
        result = registry.review("A", req)
        assert result.raw_text == "No matching scenario"

        result_b = registry.review("B", req)
        assert result_b.raw_text == "No matching scenario"

    def test_review_unknown_slot(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ADVDEB_A_KEY", "key-a")
        monkeypatch.setenv("ADVDEB_B_KEY", "key-b")
        config = self._make_config("gpt-4o", "claude-sonnet-4-5")
        registry = ProviderRegistry(config)
        art = _make_artifact("art_test")
        req = ReviewRequest(artifact=art, prompt_version="test_v1")

        with pytest.raises(ValueError, match="unknown slot"):
            registry.review("C", req)  # type: ignore[arg-type]

    def test_review_type_error_on_wrong_return(self, monkeypatch: pytest.MonkeyPatch) -> None:
        class BadProvider:
            def review(self, request: object) -> str:
                return "not a ReviewResult"

        monkeypatch.setenv("ADVDEB_A_KEY", "key-a")
        monkeypatch.setenv("ADVDEB_B_KEY", "key-b")

        original = _REVIEWER_FACTORIES["scripted"]

        def bad_factory(_cfg: ProviderConfig, _key: str) -> BadProvider:
            return BadProvider()

        _REVIEWER_FACTORIES["scripted"] = bad_factory
        try:
            config = AdvdebConfig(
                providers=ProvidersConfig(
                    a=ProviderConfig(type="scripted", model="x", key_env="ADVDEB_A_KEY"),
                    b=ProviderConfig(type="scripted", model="x", key_env="ADVDEB_B_KEY"),
                ),
            )
            registry = ProviderRegistry(config)
            art = _make_artifact("art_001")
            req = ReviewRequest(artifact=art, prompt_version="v1")
            with pytest.raises(TypeError, match="unexpected type"):
                registry.review("A", req)
        finally:
            _REVIEWER_FACTORIES["scripted"] = original


def _make_artifact(artifact_id: str = "art_default") -> ReviewArtifact:
    return ReviewArtifact(
        id=artifact_id,
        domain="test",
        source_uri="test://example",
        content_blocks=[
            ContentBlock(id="blk_1", kind="text", name="test.txt", content="test content")
        ],
        created_at=datetime.now(UTC),
        content_hash="b" * 64,
    )
