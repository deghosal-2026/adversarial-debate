"""Contract tests (WBS T2.1 #8): ReviewRequest / ReviewResult shape and constraints."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from adversarial_debate.providers.contract import (
    ReviewRequest,
    ReviewResult,
    ReviewResultMetadata,
    ReviewUsage,
)
from adversarial_debate.schemas.artifact import ContentBlock, ReviewArtifact, RubricHint
from adversarial_debate.schemas.debate import Claim
from adversarial_debate.schemas.review import Risk


class TestReviewRequest:
    """ReviewRequest requires at minimum artifact + prompt_version."""

    def test_minimal(self) -> None:
        art = _make_artifact()
        req = ReviewRequest(artifact=art, prompt_version="test_v1")
        assert req.artifact.id == "art_test"
        assert req.prompt_version == "test_v1"
        assert req.seed is None
        assert req.rubric_hints == []

    def test_with_seed(self) -> None:
        art = _make_artifact()
        req = ReviewRequest(artifact=art, prompt_version="test_v1", seed=42)
        assert req.seed == 42

    def test_with_rubric_hints(self) -> None:
        art = _make_artifact()
        hints = [RubricHint(id="rh_1", dimension="security", guidance="Check for SQLi", weight=1.5)]
        req = ReviewRequest(artifact=art, prompt_version="test_v1", rubric_hints=hints)
        assert len(req.rubric_hints) == 1
        assert req.rubric_hints[0].dimension == "security"


class TestReviewResult:
    """ReviewResult carries claims, risks, confidence, raw_text, metadata."""

    def test_empty(self) -> None:
        result = ReviewResult()
        assert result.claims == []
        assert result.risks == []
        assert result.confidence == 0.0
        assert result.raw_text == ""
        assert result.metadata.seed is None
        assert result.metadata.prompt_version == "unknown"

    def test_with_data(self) -> None:
        claim = Claim(id="cl_001", review_id="rv_001", text="bug", severity="high")
        risk = Risk(id="risk_001", text="vulnerability", severity="high")
        usage = ReviewUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
        metadata = ReviewResultMetadata(seed=42, prompt_version="v1", usage=usage, model="gpt-4o")

        result = ReviewResult(
            claims=[claim],
            risks=[risk],
            confidence=0.85,
            raw_text="Found issues",
            metadata=metadata,
        )
        assert len(result.claims) == 1
        assert result.claims[0].text == "bug"
        assert len(result.risks) == 1
        assert result.risks[0].text == "vulnerability"
        assert result.confidence == 0.85
        assert result.metadata.seed == 42
        assert result.metadata.prompt_version == "v1"
        assert result.metadata.usage.total_tokens == 30
        assert result.metadata.model == "gpt-4o"

    def test_is_empty_property(self) -> None:
        assert ReviewResult().is_empty is True
        claim = Claim(id="cl_001", review_id="rv_001", text="x", severity="low")
        assert ReviewResult(claims=[claim]).is_empty is False

    def test_confidence_bounds(self) -> None:
        ReviewResult(confidence=0.0)
        ReviewResult(confidence=1.0)
        with pytest.raises(ValidationError):
            ReviewResult(confidence=-0.1)
        with pytest.raises(ValidationError):
            ReviewResult(confidence=1.1)

    def test_serialization_roundtrip(self) -> None:
        usage = ReviewUsage(prompt_tokens=5, completion_tokens=3, total_tokens=8)
        meta = ReviewResultMetadata(seed=0, prompt_version="v1", usage=usage, model="m")
        result = ReviewResult(
            claims=[Claim(id="cl_001", review_id="rv_001", text="x", severity="low")],
            risks=[Risk(id="risk_001", text="y")],
            confidence=0.5,
            raw_text="hello",
            metadata=meta,
        )
        data = result.model_dump()
        restored = ReviewResult.model_validate(data)
        assert restored.claims[0].text == "x"
        assert restored.metadata.seed == 0
        assert restored.metadata.usage.total_tokens == 8


def _make_artifact() -> ReviewArtifact:
    return ReviewArtifact(
        id="art_test",
        domain="test",
        source_uri="test://example",
        content_blocks=[
            ContentBlock(id="blk_1", kind="text", name="test.txt", content="hello world")
        ],
        created_at=datetime.now(UTC),
        content_hash="a" * 64,
    )
