"""Artifact schemas contract (WBS T1.3, PRD §2.4 + i18n §22.2)."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from adversarial_debate.schemas import (
    ContentBlock,
    DetectedLanguage,
    ReviewArtifact,
    RubricHint,
)

NOW = datetime(2026, 8, 24, 12, 0, tzinfo=UTC)
SHA = "a" * 64


def make_block() -> ContentBlock:
    return ContentBlock(id="cb_000001", kind="diff", name="src/app.py", content="+ pass")


def make_artifact(**overrides: object) -> ReviewArtifact:
    fields: dict[str, object] = {
        "id": "art_test",
        "domain": "pr_review",
        "source_uri": "https://github.com/acme/repo/pull/482",
        "content_blocks": [make_block()],
        "rubric_hints": [
            RubricHint(id="rh_1", dimension="security", guidance="Look for injection.")
        ],
        "created_at": NOW,
        "content_hash": SHA,
        "detected_language": DetectedLanguage(code="en"),
        "classification_tag": "python-diff",
        "metadata": {"pr_title": "Add feature"},
    }
    fields.update(overrides)
    return ReviewArtifact.model_validate(fields)


def test_content_block_json_round_trip() -> None:
    block = make_block()
    assert ContentBlock.model_validate_json(block.model_dump_json()) == block


def test_review_artifact_json_round_trip() -> None:
    artifact = make_artifact()
    restored = ReviewArtifact.model_validate_json(artifact.model_dump_json())
    assert restored == artifact


def test_content_hash_must_be_sha256_hex() -> None:
    with pytest.raises(ValidationError, match="content_hash"):
        make_artifact(content_hash="deadbeef")


@pytest.mark.parametrize(
    ("field", "value"),
    [("id", ""), ("domain", ""), ("source_uri", "")],
)
def test_empty_required_strings_rejected(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        make_artifact(**{field: value})


def test_naive_datetime_rejected() -> None:
    with pytest.raises(ValidationError):
        make_artifact(created_at=datetime(2026, 8, 24, 12, 0))


def test_rubric_hint_weight_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        RubricHint(id="rh_bad", dimension="security", guidance="x", weight=0)


def test_extra_fields_forbidden() -> None:
    with pytest.raises(ValidationError, match=r"[Ee]xtra"):
        make_artifact(surprise="nope")


def test_detected_language_defaults_and_confidence_bounds() -> None:
    lang = DetectedLanguage(code="en")
    assert lang.source == "auto_detected"
    assert lang.confidence is None
    with pytest.raises(ValidationError):
        DetectedLanguage(code="en", confidence=1.5)


def test_classification_tag_nonempty() -> None:
    with pytest.raises(ValidationError):
        make_artifact(classification_tag="")
