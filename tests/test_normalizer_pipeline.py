"""End-to-end PR-review normalization pipeline (WBS T4.1-T4.4 integration)."""

from datetime import UTC, datetime
from pathlib import Path

import pytest

from adversarial_debate.adapters import (
    AdapterError,
    DuplicateDomainError,
    MetadataExtractionError,
    NormalizationError,
    available_domains,
    normalize,
    register,
    utc_now,
)
from adversarial_debate.adapters.pr_review import (
    DEFAULT_RUBRIC_HINTS,
    PrReviewNormalizer,
)
from adversarial_debate.ids import content_hash
from adversarial_debate.schemas.artifact import RubricHint
from tests.test_metadata_extractor import fake_gh, url_responses, view_payload

NOW = datetime(2026, 8, 24, 12, 0, tzinfo=UTC)

CLEAN_DIFF = """diff --git a/src/app.py b/src/app.py
index 1a2b3c4..5d6e7f8 100644
--- a/src/app.py
+++ b/src/app.py
@@ -1,2 +1,3 @@
 import os
+import sys
"""


@pytest.fixture
def diff_file(tmp_path: Path) -> Path:
    path = tmp_path / "pr-482.diff"
    path.write_text(CLEAN_DIFF)
    return path


@pytest.fixture
def normalizer() -> PrReviewNormalizer:
    return PrReviewNormalizer(clock=lambda: NOW)


def test_domain_registered_on_import() -> None:
    assert "pr_review" in available_domains()


def test_duplicate_pr_review_registration_rejected(normalizer: PrReviewNormalizer) -> None:
    with pytest.raises(DuplicateDomainError, match="pr_review"):
        register("pr_review", normalizer)


def test_normalize_local_path_end_to_end(normalizer: PrReviewNormalizer, diff_file: Path) -> None:
    artifact = normalizer.normalize(str(diff_file))
    assert artifact.domain == "pr_review"
    assert artifact.source_uri == str(diff_file.resolve())
    assert artifact.id.startswith("art_")
    assert artifact.created_at == NOW
    assert [b.sequence for b in artifact.content_blocks] == list(
        range(len(artifact.content_blocks))
    )
    expected_hash = content_hash("\x1e".join(b.content for b in artifact.content_blocks))
    assert artifact.content_hash == expected_hash


def test_detected_language_and_classification_tag(
    normalizer: PrReviewNormalizer, diff_file: Path
) -> None:
    artifact = normalizer.normalize(str(diff_file))
    assert artifact.detected_language is not None
    assert artifact.detected_language.code == "en"
    assert artifact.detected_language.source == "auto_detected"
    assert artifact.classification_tag == "python-diff"


def test_default_rubric_hints_plus_caller_hints(
    normalizer: PrReviewNormalizer, diff_file: Path
) -> None:
    custom = RubricHint(id="rh_custom", dimension="perf", guidance="Check allocations.")
    artifact = normalizer.normalize(str(diff_file), hints=[custom])
    ids = [h.id for h in artifact.rubric_hints]
    assert ids == [*DEFAULT_RUBRIC_HINT_IDS, "rh_custom"]
    assert all(h.weight > 0 for h in artifact.rubric_hints)


DEFAULT_RUBRIC_HINT_IDS = [h.id for h in DEFAULT_RUBRIC_HINTS]


def test_chunk_metadata_always_present(normalizer: PrReviewNormalizer, diff_file: Path) -> None:
    artifact = normalizer.normalize(str(diff_file))
    assert artifact.metadata["chunk_count"] == "1"
    assert artifact.metadata["chunk_budget_fraction"] == "0.8"
    assert "chunk_1_budget_pct" in artifact.metadata
    assert artifact.metadata["chunk_1_dedup_key"].startswith("cdk_")


def test_small_window_produces_multiple_chunks(tmp_path: Path) -> None:
    hunks = "\n".join(
        f"@@ -{i},1 +{i},1 @@\n+line {i} padding padding padding padding" for i in range(40)
    )
    big = "diff --git a/big.py b/big.py\n--- a/big.py\n+++ b/big.py\n" + hunks + "\n"
    path = tmp_path / "big.diff"
    path.write_text(big)
    normalizer = PrReviewNormalizer(clock=lambda: NOW, window_tokens=512)
    artifact = normalizer.normalize(str(path))
    count = int(artifact.metadata["chunk_count"])
    assert count > 1
    assert artifact.metadata["estimated_total_tokens"] >= artifact.metadata["chunk_budget_tokens"]
    for i in range(1, count + 1):
        assert f"chunk_{i}_budget_pct" in artifact.metadata


def test_missing_file_raises_actionable_error(
    normalizer: PrReviewNormalizer, tmp_path: Path
) -> None:
    with pytest.raises(AdapterError, match="diff not found"):
        normalizer.normalize(str(tmp_path / "absent.diff"))


def test_directory_input_rejected(normalizer: PrReviewNormalizer, tmp_path: Path) -> None:
    with pytest.raises(MetadataExtractionError, match="not a file"):
        normalizer.normalize(str(tmp_path))


def test_empty_input_rejected(normalizer: PrReviewNormalizer) -> None:
    with pytest.raises(NormalizationError, match="empty"):
        normalizer.normalize("   ")


def test_diff_without_parsable_files_rejected(
    normalizer: PrReviewNormalizer, tmp_path: Path
) -> None:
    path = tmp_path / "blank.diff"
    path.write_text("")
    with pytest.raises(NormalizationError, match="no parsable file changes"):
        normalizer.normalize(str(path))


def test_parser_warnings_surface_in_metadata(
    normalizer: PrReviewNormalizer, tmp_path: Path
) -> None:
    noisy = CLEAN_DIFF.replace("@@ -1,2 +1,3 @@", "@@ bogus header @@")
    path = tmp_path / "noisy.diff"
    path.write_text(noisy)
    artifact = normalizer.normalize(str(path))
    warnings = [v for k, v in artifact.metadata.items() if k.startswith("parse_warning_")]
    assert any("malformed hunk header" in w for w in warnings)


def test_github_url_flow_end_to_end() -> None:
    gh = fake_gh(responses=url_responses(view_payload(["src/auth.py"])))
    normalizer = PrReviewNormalizer(gh=gh, clock=lambda: NOW)
    url = "https://github.com/acme/widgets/pull/482"
    artifact = normalizer.normalize(url)
    assert artifact.source_uri == url
    assert artifact.metadata["pr_title"] == "Fix login flow"
    assert artifact.metadata["files_changed"] == "src/auth.py"


def test_normalize_via_registry_dispatch(diff_file: Path) -> None:
    artifact = normalize(str(diff_file), hints=None, domain="pr_review")
    assert artifact.domain == "pr_review"
    assert artifact.content_blocks


def test_normalization_is_deterministic(diff_file: Path) -> None:
    first = PrReviewNormalizer(clock=lambda: NOW).normalize(str(diff_file))
    second = PrReviewNormalizer(clock=lambda: NOW).normalize(str(diff_file))
    assert first == second


def test_utc_now_default_clock_is_aware() -> None:
    assert utc_now().tzinfo is UTC
