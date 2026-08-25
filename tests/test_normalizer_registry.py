"""Normalizer registry contract (WBS T4.1, PRD §5.3 adapter protocol)."""

from collections.abc import Iterator, Sequence
from datetime import UTC, datetime

import pytest

from adversarial_debate.adapters import (
    DuplicateDomainError,
    Normalizer,
    UnknownDomainError,
    available_domains,
    get_normalizer,
    normalize,
    register,
    unregister,
)
from adversarial_debate.schemas.artifact import ContentBlock, ReviewArtifact, RubricHint

NOW = datetime(2026, 8, 24, 12, 0, tzinfo=UTC)


def make_minimal_artifact(raw: str) -> ReviewArtifact:
    return ReviewArtifact(
        id="art_dummy",
        domain="dummy_domain",
        source_uri=raw,
        content_blocks=[
            ContentBlock(
                id="cb_1", kind="text", name="placeholder", content="placeholder", sequence=0
            )
        ],
        created_at=NOW,
        content_hash="a" * 64,
    )


class DummyNormalizer:
    domain = "dummy_domain"

    def normalize(self, raw: str, hints: Sequence[RubricHint] | None = None) -> ReviewArtifact:
        return make_minimal_artifact(raw)


@pytest.fixture
def dummy() -> Iterator[DummyNormalizer]:
    normalizer = DummyNormalizer()
    register("dummy_domain", normalizer)
    yield normalizer
    unregister("dummy_domain")


def test_runtime_protocol_isinstance(dummy: DummyNormalizer) -> None:
    assert isinstance(dummy, Normalizer)


def test_register_and_get_roundtrip(dummy: DummyNormalizer) -> None:
    assert get_normalizer("dummy_domain") is dummy


def test_duplicate_registration_raises(dummy: DummyNormalizer) -> None:
    with pytest.raises(DuplicateDomainError, match="dummy_domain"):
        register("dummy_domain", dummy)


def test_unknown_domain_error_lists_available(dummy: DummyNormalizer) -> None:
    with pytest.raises(UnknownDomainError, match="dummy_domain"):
        get_normalizer("nonexistent_domain")


def test_unknown_domain_message_includes_requested_name(
    dummy: DummyNormalizer,
) -> None:
    with pytest.raises(UnknownDomainError, match="ghost_domain"):
        get_normalizer("ghost_domain")


def test_unregister_removes_domain() -> None:
    normalizer = DummyNormalizer()
    register("dummy_domain", normalizer)
    unregister("dummy_domain")
    with pytest.raises(UnknownDomainError):
        get_normalizer("dummy_domain")


def test_unregister_unknown_domain_raises() -> None:
    with pytest.raises(UnknownDomainError, match="never_registered"):
        unregister("never_registered")


def test_normalize_dispatches_to_registered(dummy: DummyNormalizer) -> None:
    artifact = normalize("RAW_INPUT", hints=None, domain="dummy_domain")
    assert artifact.source_uri == "RAW_INPUT"
    assert artifact.domain == "dummy_domain"


def test_normalize_unknown_domain_is_actionable(dummy: DummyNormalizer) -> None:
    with pytest.raises(UnknownDomainError, match="dummy_domain"):
        normalize("RAW", hints=None, domain="missing_domain")


def test_available_domains_sorted(dummy: DummyNormalizer) -> None:
    register("aaa_other", DummyOther())
    try:
        assert available_domains() == sorted(available_domains())
        assert "aaa_other" in available_domains()
    finally:
        unregister("aaa_other")


class DummyOther:
    domain = "aaa_other"

    def normalize(self, raw: str, hints: Sequence[RubricHint] | None = None) -> ReviewArtifact:
        return make_minimal_artifact(raw)
