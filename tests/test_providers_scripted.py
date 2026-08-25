"""ScriptedReviewer tests (WBS T2.6 #13): canned YAML scenarios, malformed output."""

from datetime import UTC, datetime
from pathlib import Path

from adversarial_debate.providers.contract import ReviewRequest
from adversarial_debate.providers.scripted_reviewer import ScriptedReviewer
from adversarial_debate.schemas.artifact import ContentBlock, ReviewArtifact


class TestScriptedReviewer:
    """ScriptedReviewer returns canned responses from YAML scenarios."""

    def test_matching_scenario_returns_canned_data(self) -> None:
        reviewer = ScriptedReviewer(
            model="test",
            scenarios_path="tests/scenarios/review_scenarios.yaml",
        )
        art = _make_artifact("art_standard_001")
        req = ReviewRequest(artifact=art, prompt_version="v1")
        result = reviewer.review(req)
        assert len(result.claims) == 2
        assert result.claims[0].text.startswith("Unvalidated input")
        assert result.confidence == 0.78
        assert "I found the following" in result.raw_text

    def test_empty_scenario_returns_no_claims(self) -> None:
        reviewer = ScriptedReviewer(
            model="test",
            scenarios_path="tests/scenarios/review_scenarios.yaml",
        )
        art = _make_artifact("art_clean_001")
        req = ReviewRequest(artifact=art, prompt_version="v1")
        result = reviewer.review(req)
        assert result.claims == []
        assert result.risks == []
        assert result.confidence == 0.95

    def test_malformed_scenario_returns_empty_claims(self) -> None:
        reviewer = ScriptedReviewer(
            model="test",
            scenarios_path="tests/scenarios/review_scenarios.yaml",
        )
        art = _make_artifact("art_nonsense_001")
        req = ReviewRequest(artifact=art, prompt_version="v1")
        result = reviewer.review(req)
        assert result.claims == []
        assert result.confidence == 0.0
        assert "500 Internal Server Error" in result.raw_text

    def test_no_match_returns_fallback(self) -> None:
        reviewer = ScriptedReviewer(
            model="test",
            scenarios_path="tests/scenarios/review_scenarios.yaml",
        )
        art = _make_artifact("unmatched_artifact_xyz")
        req = ReviewRequest(artifact=art, prompt_version="v1")
        result = reviewer.review(req)
        assert result.raw_text == "No matching scenario"
        assert result.claims == []

    def test_scenario_metadata_has_seed_and_version(self) -> None:
        reviewer = ScriptedReviewer(
            model="test-model",
            scenarios_path="tests/scenarios/review_scenarios.yaml",
        )
        art = _make_artifact("art_standard_001")
        req = ReviewRequest(artifact=art, prompt_version="v3", seed=42)
        result = reviewer.review(req)
        assert result.metadata.seed == 42
        assert result.metadata.prompt_version == "v3"
        assert result.metadata.model == "test-model"

    def test_missing_scenarios_file(self, tmp_path: object) -> None:
        p = Path(str(tmp_path)) / "nonexistent.yaml"
        reviewer = ScriptedReviewer(model="test", scenarios_path=str(p))
        art = _make_artifact("anything")
        req = ReviewRequest(artifact=art, prompt_version="v1")
        result = reviewer.review(req)
        assert result.raw_text == "No matching scenario"


def _make_artifact(artifact_id: str = "art_default") -> ReviewArtifact:
    return ReviewArtifact(
        id=artifact_id,
        domain="test",
        source_uri="test://example",
        content_blocks=[
            ContentBlock(id="blk_1", kind="text", name="test.txt", content="test content")
        ],
        created_at=datetime.now(UTC),
        content_hash="f" * 64,
    )
