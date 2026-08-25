"""ProviderRegistry: config slots A/B → provider instances (WBS T2.1 #8, PRD §2.5).

Validates heterogeneous vs same-family pairs (DD-04), exposes ``pair_mode``,
and produces actionable errors for missing API-key environment variables.
"""

import os
from collections.abc import Callable
from typing import Literal

from adversarial_debate.config import AdvdebConfig, ConfigError, ProviderConfig
from adversarial_debate.providers.contract import ReviewRequest, ReviewResult
from adversarial_debate.providers.openai_transport import OpenAITransport
from adversarial_debate.providers.scripted_reviewer import ScriptedReviewer


def _infer_family(model: str) -> str:
    """Infer model family from the model identifier string.

    Used to determine whether a pair is ``diverse`` (different families) or
    ``same`` (PRD §2.5, DD-04).
    """
    model_lower = model.lower()
    if model_lower.startswith(("gpt-", "o1", "o3")):
        return "openai"
    if model_lower.startswith("claude"):
        return "anthropic"
    if model_lower.startswith("gemini"):
        return "google"
    if "/" in model_lower:
        return model_lower.split("/")[0].strip()
    return "other"


def _resolve_key(key_env: str, slot: str) -> str:
    """Resolve ``key_env`` to an API key; raises [ConfigError] naming the slot."""
    value = os.environ.get(key_env)
    if not value:
        msg = (
            f"missing required environment variable {key_env!r} "
            f"for config slot providers.{slot} — "
            f"set it in your shell or .env file before running advdeb"
        )
        raise ConfigError(msg)
    return value


# Lazy-import factories for optional extras.
def _factory_openai(cfg: ProviderConfig, api_key: str) -> OpenAITransport:
    return OpenAITransport(base_url=cfg.base_url or "", model=cfg.model, api_key=api_key)


def _factory_scripted(cfg: ProviderConfig, _api_key: str) -> ScriptedReviewer:
    return ScriptedReviewer(model=cfg.model)


def _factory_pydantic_ai(cfg: ProviderConfig, api_key: str) -> object:
    try:
        from adversarial_debate.providers.pydanticai_adapter import (  # noqa: PLC0415
            PydanticAIAdapter,
        )

        return PydanticAIAdapter(base_url=cfg.base_url or "", model=cfg.model, api_key=api_key)
    except ImportError as exc:
        msg = (
            f"provider type {cfg.type!r} requires the [pydanticai] extra; "
            f"install with: uv add adversarial-debate[pydanticai]"
        )
        raise ConfigError(msg) from exc


def _factory_langgraph(cfg: ProviderConfig, api_key: str) -> object:
    try:
        from adversarial_debate.providers.langgraph_adapter import (  # noqa: PLC0415
            LangGraphAdapter,
        )

        return LangGraphAdapter(base_url=cfg.base_url or "", model=cfg.model, api_key=api_key)
    except ImportError as exc:
        msg = (
            f"provider type {cfg.type!r} requires the [langgraph] extra; "
            f"install with: uv add adversarial-debate[langgraph]"
        )
        raise ConfigError(msg) from exc


_REVIEWER_FACTORIES: dict[str, Callable[[ProviderConfig, str], object]] = {
    "openai_compatible": _factory_openai,
    "scripted": _factory_scripted,
    "pydantic_ai": _factory_pydantic_ai,
    "langgraph": _factory_langgraph,
}


class ProviderRegistry:
    """Config-driven model registry (F8). Creates two reviewer instances for slots A/B.

    Usage::

        registry = ProviderRegistry(config)
        result = registry.review("A", ReviewRequest(...))
        print(registry.pair_mode)  # "diverse" or "same"
    """

    def __init__(self, config: AdvdebConfig) -> None:
        """Build provider instances from config; validates keys and family diversity."""
        self._config = config
        self._instances: dict[str, object] = {}
        self._families: dict[str, str] = {}

        for slot_key in ("a", "b"):
            provider_cfg: ProviderConfig = getattr(config.providers, slot_key)
            family = _infer_family(provider_cfg.model)
            self._families[slot_key] = family

            api_key = _resolve_key(provider_cfg.key_env, slot_key)

            factory = _REVIEWER_FACTORIES.get(provider_cfg.type)
            if factory is None:
                available = ", ".join(sorted(_REVIEWER_FACTORIES))
                msg = (
                    f"unknown provider type {provider_cfg.type!r} for "
                    f"slot providers.{slot_key}. Available types: {available}"
                )
                raise ConfigError(msg)

            self._instances[slot_key] = factory(provider_cfg, api_key)

    @property
    def pair_mode(self) -> Literal["diverse", "same"]:
        """``diverse`` when A and B belong to different model families; ``same`` otherwise."""
        if self._families["a"] != self._families["b"]:
            return "diverse"
        return "same"

    @property
    def families(self) -> dict[str, str]:
        """Per-slot model families (read-only view)."""
        return dict(self._families)

    def review(self, slot: Literal["A", "B"], request: ReviewRequest) -> ReviewResult:
        """Run a review on the given slot."""
        key = slot.lower()
        instance = self._instances.get(key)
        if instance is None:
            msg = f"unknown slot {slot!r}; expected A or B"
            raise ValueError(msg)
        result = instance.review(request)  # type: ignore[attr-defined]
        if not isinstance(result, ReviewResult):
            msg = f"provider for slot {slot} returned unexpected type {type(result).__name__}"
            raise TypeError(msg)
        return result


__all__ = [
    "_REVIEWER_FACTORIES",
    "ProviderRegistry",
    "_infer_family",
    "_resolve_key",
]
