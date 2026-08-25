"""Fixture corpus v1 validation (WBS T4.5): schema round-trip, manifest consistency, exit-bar."""

import json
from pathlib import Path
from typing import Any

from adversarial_debate.adapters.pr_review import PrReviewNormalizer
from adversarial_debate.schemas.artifact import ReviewArtifact

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "pr_review"
MANIFEST = FIXTURES / "fixtures.json"


def _manifest() -> list[dict[str, Any]]:
    return json.loads(MANIFEST.read_text())  # type: ignore[no-any-return]


def test_manifest_exists() -> None:
    assert MANIFEST.is_file(), f"manifest missing at {MANIFEST}"


def test_fixture_count_is_in_range() -> None:
    entries = _manifest()
    assert 8 <= len(entries) <= 10, f"expected 8-10 fixtures, got {len(entries)}"


def test_every_fixture_file_exists() -> None:
    for entry in _manifest():
        diff = FIXTURES / entry["diff_file"]
        assert diff.is_file(), f"{entry['diff_file']} missing for {entry['id']}"


def test_every_fixture_normalizes_to_valid_artifact() -> None:
    normalizer = PrReviewNormalizer()
    for entry in _manifest():
        diff = FIXTURES / entry["diff_file"]
        artifact = normalizer.normalize(str(diff))
        assert isinstance(artifact, ReviewArtifact)
        assert artifact.domain == "pr_review"


def test_manifest_content_consistency() -> None:
    for entry in _manifest():
        assert entry["id"]
        assert entry["title"]
        assert entry["diff_file"]
        assert entry["expected_severity"] in ("low", "medium", "high")
        assert isinstance(entry["should_disagree"], bool)
        known = entry.get("known_issues", [])
        assert len(known) >= 1, f"{entry['id']}: at least 1 known_issue required"
        for issue in known:
            assert issue["description"]
            assert issue["severity"] in ("low", "medium", "high")


def test_exit_bar_rehearsal_scenario_present() -> None:
    """At least one fixture where only reviewer B's framing would catch the issue."""
    hits = [e for e in _manifest() if e.get("only_b_catches")]
    assert len(hits) >= 1, "no only_b_catches fixture found (needed for M10 exit-bar)"


def test_fixtures_schema_validate() -> None:
    """Every fixture produces a schema-valid artifact with populated content_blocks."""
    normalizer = PrReviewNormalizer()
    for entry in _manifest():
        diff = FIXTURES / entry["diff_file"]
        artifact = normalizer.normalize(str(diff))
        assert len(artifact.content_blocks) >= 1
        assert artifact.content_hash
