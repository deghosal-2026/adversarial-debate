"""Normalizer framework: protocol, registry, shared errors (WBS T4.1).

Plugin contract per PRD [05-features §5.3](docs/design/prd/05-features.md):
each domain ships a ``Normalizer`` under ``adapters/<domain>/`` and registers
itself on import; the engine stays domain-agnostic. Registry errors are
user-facing and actionable — an unknown domain always lists what *is*
available.
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Protocol, TypeAlias, runtime_checkable

from adversarial_debate.ids import deterministic_id
from adversarial_debate.schemas.artifact import ReviewArtifact, RubricHint

Hints: TypeAlias = Sequence[RubricHint] | None


class AdapterError(Exception):
    """Base class for adapter-layer failures; messages are user-facing."""


class UnknownDomainError(AdapterError):
    """Requested domain has no registered normalizer; message lists domains."""


class DuplicateDomainError(AdapterError):
    """Two normalizers claim the same domain key; registration refused."""


class NormalizationError(AdapterError):
    """Raw input cannot be turned into a valid ReviewArtifact."""


class MetadataExtractionError(AdapterError):
    """PR metadata could not be extracted (missing file, gh failure, bad URL)."""


@runtime_checkable
class Normalizer(Protocol):
    """Converts raw domain input into a ReviewArtifact (PRD §5.3 step 1)."""

    def normalize(self, raw: str, hints: Hints = None) -> ReviewArtifact:
        """Normalize ``raw`` (path/URL/domain payload) using optional hints."""
        ...


_REGISTRY: dict[str, Normalizer] = {}


def register(domain: str, normalizer: Normalizer) -> None:
    """Register ``normalizer`` under ``domain``; refuses duplicate keys."""
    if domain in _REGISTRY:
        msg = f"domain {domain!r} already registered"
        raise DuplicateDomainError(msg)
    _REGISTRY[domain] = normalizer


def unregister(domain: str) -> None:
    """Remove a registration; raises [UnknownDomainError][...] if absent."""
    if domain not in _REGISTRY:
        msg = f"unknown domain {domain!r}; available: {_available_csv()}"
        raise UnknownDomainError(msg)
    del _REGISTRY[domain]


def _lazy_load_builtins() -> None:
    """Ensure built-in adapters are registered."""
    if "pr_review" not in _REGISTRY:
        from adversarial_debate.adapters import pr_review  # noqa: F401


def available_domains() -> list[str]:
    """Sorted list of registered domain keys."""
    _lazy_load_builtins()
    return sorted(_REGISTRY)


def get_normalizer(domain: str) -> Normalizer:
    """Look up a registered normalizer; unknown domains list availability."""
    _lazy_load_builtins()
    if domain not in _REGISTRY:
        msg = (
            f"unknown domain {domain!r}: no adapter is registered for it. "
            f"Available domains: {_available_csv()}"
        )
        raise UnknownDomainError(msg)
    return _REGISTRY[domain]


def normalize(raw: str, hints: Hints = None, domain: str = "pr_review") -> ReviewArtifact:
    """Dispatch ``raw`` to the normalizer registered for ``domain``."""
    return get_normalizer(domain).normalize(raw, hints)


def artifact_id_for(domain: str, source_uri: str) -> str:
    """Deterministic artifact id derived from domain + source (ids.py contract)."""
    return deterministic_id("art", f"{domain}|{source_uri}")


def utc_now() -> datetime:
    """Timezone-aware UTC timestamp; default clock for normalization."""
    return datetime.now(UTC)


def _available_csv() -> str:
    domains = available_domains()
    return ", ".join(domains) if domains else "(none registered)"
