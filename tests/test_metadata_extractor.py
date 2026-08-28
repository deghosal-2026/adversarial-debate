"""PR metadata extractor contract (WBS T4.3): local paths, gh URLs, FM-10."""

import json
import subprocess
from collections.abc import Sequence
from pathlib import Path

import pytest

from adversarial_debate.adapters.base import MetadataExtractionError
from adversarial_debate.adapters.pr_review.language import (
    classification_tag,
    guess_language,
    summarize_languages,
)
from adversarial_debate.adapters.pr_review.metadata import (
    ExtractionResult,
    GhCli,
    PrMetadataExtractor,
)

SAMPLE_DIFF = """diff --git a/src/auth.py b/src/auth.py
--- a/src/auth.py
+++ b/src/auth.py
@@ -1,1 +1,2 @@
+import bcrypt
"""


class FakeGh:
    def __init__(
        self,
        *,
        available: bool = True,
        responses: dict[tuple[str, str], tuple[int, str, str]] | None = None,
    ) -> None:
        self._available = available
        self.responses = responses or {}
        self.calls: list[list[str]] = []

    def available(self) -> bool:
        return self._available

    def run(self, args: Sequence[str]) -> tuple[int, str, str]:
        self.calls.append(list(args))
        key = (args[0], args[1])
        return self.responses.get(key, (0, "", ""))


def fake_gh(
    *, available: bool = True, responses: dict[tuple[str, str], tuple[int, str, str]] | None = None
) -> FakeGh:
    return FakeGh(available=available, responses=responses)


def view_payload(diff_paths: list[str], commits: int = 2) -> str:
    payload = {
        "number": 482,
        "title": "Fix login flow",
        "body": "Please review carefully.",
        "url": "https://github.com/acme/widgets/pull/482",
        "author": {"login": "octocat"},
        "baseRefName": "main",
        "headRefName": "fix-login",
        "files": [{"path": p} for p in diff_paths],
        "commits": [{"oid": f"{i:040x}"} for i in range(commits)],
    }
    return json.dumps(payload)


def url_responses(view_json: str) -> dict[tuple[str, str], tuple[int, str, str]]:
    return {("pr", "view"): (0, view_json, ""), ("pr", "diff"): (0, SAMPLE_DIFF, "")}


def test_guess_language_by_extension() -> None:
    assert guess_language("app/main.py") == "python"
    assert guess_language("web/ui.tsx") == "typescript"
    assert guess_language("deploy.sh") == "shell"
    assert guess_language("assets/logo.png") is None


def test_guess_language_no_extension() -> None:
    assert guess_language("Makefile") is None
    assert guess_language("Dockerfile") is None


def test_summarize_languages_sorted_unique() -> None:
    langs = summarize_languages(["b.py", "a.py", "c.ts", "blob.bin"])
    assert langs == ["python", "typescript"]


def test_classification_tag_majority() -> None:
    assert classification_tag(["a.py", "b.py", "c.md"]) == "python-diff"


def test_classification_tag_mixed() -> None:
    assert classification_tag(["a.py", "b.ts", "c.go"]) == "mixed-diff"


def test_classification_tag_no_known_extensions() -> None:
    assert classification_tag(["logo.png", "data.bin"]) == "generic-diff"


def test_pull_request_url_detection() -> None:
    extractor = PrMetadataExtractor(gh=fake_gh())
    assert extractor.is_pull_request_url("https://github.com/acme/widgets/pull/482")
    assert extractor.is_pull_request_url("http://github.com/acme/widgets/pull/7/")
    assert not extractor.is_pull_request_url("https://github.com/acme/widgets")
    assert not extractor.is_pull_request_url("https://gitlab.com/acme/widgets/pull/9")
    assert not extractor.is_pull_request_url("diff.patch")


def test_fetch_diff_local_reads_content(tmp_path: Path) -> None:
    diff_path = tmp_path / "change.diff"
    diff_path.write_text(SAMPLE_DIFF)
    extractor = PrMetadataExtractor(gh=fake_gh())
    text, path = extractor.fetch_diff(str(diff_path))
    assert text == SAMPLE_DIFF
    assert path is not None and path.name == "change.diff"


def test_fetch_diff_missing_local_file_is_actionable(tmp_path: Path) -> None:
    missing = tmp_path / "nope.diff"
    extractor = PrMetadataExtractor(gh=fake_gh())
    with pytest.raises(MetadataExtractionError, match=r"nope\.diff") as excinfo:
        extractor.fetch_diff(str(missing))
    assert "GitHub PR URL" in str(excinfo.value)


def test_fetch_diff_directory_rejected(tmp_path: Path) -> None:
    extractor = PrMetadataExtractor(gh=fake_gh())
    with pytest.raises(MetadataExtractionError, match="not a file"):
        extractor.fetch_diff(str(tmp_path))


def test_fetch_diff_url_requires_available_gh() -> None:
    extractor = PrMetadataExtractor(gh=fake_gh(available=False))
    with pytest.raises(MetadataExtractionError, match="local diff"):
        extractor.fetch_diff("https://github.com/acme/widgets/pull/482")


def test_fetch_diff_url_via_gh() -> None:
    extractor = PrMetadataExtractor(gh=fake_gh(responses=url_responses("{}")))
    text, path = extractor.fetch_diff("https://github.com/acme/widgets/pull/482")
    assert text == SAMPLE_DIFF
    assert path is None


def test_gh_view_failure_raises_with_stderr() -> None:
    responses = {("pr", "view"): (1, "", "gh: auth expired")}
    extractor = PrMetadataExtractor(gh=fake_gh(responses=responses))
    with pytest.raises(MetadataExtractionError, match="auth expired"):
        extractor.extract("https://github.com/acme/widgets/pull/482", ["src/auth.py"])


def test_gh_invalid_json_raises() -> None:
    responses = {("pr", "view"): (0, "not-json{{", "")}
    extractor = PrMetadataExtractor(gh=fake_gh(responses=responses))
    with pytest.raises(MetadataExtractionError, match="invalid JSON"):
        extractor.extract("https://github.com/acme/widgets/pull/482", ["src/auth.py"])


def test_github_extraction_full_metadata() -> None:
    gh = fake_gh(responses=url_responses(view_payload(["src/auth.py"])))
    extractor = PrMetadataExtractor(gh=gh)
    result = extractor.extract("https://github.com/acme/widgets/pull/482", ["src/auth.py"])
    md = result.metadata
    assert md["source_type"] == "github_pr"
    assert md["pr_number"] == "482"
    assert md["pr_title"] == "Fix login flow"
    assert md["pr_body"] == "Please review carefully."
    assert md["pr_author"] == "octocat"
    assert md["base_ref"] == "main"
    assert md["head_ref"] == "fix-login"
    assert md["commit_count"] == "2"
    assert md["commit_shas"].startswith("00000000")
    assert md["files_changed"] == "src/auth.py"
    assert md["languages"] == "python"


def test_commit_shas_capped_at_ten() -> None:
    gh = fake_gh(responses=url_responses(view_payload(["src/auth.py"], commits=12)))
    extractor = PrMetadataExtractor(gh=gh)
    result = extractor.extract("https://github.com/acme/widgets/pull/482", ["src/auth.py"])
    assert result.metadata["commit_count"] == "12"
    assert len(result.metadata["commit_shas"].split(",")) == 10


def test_fm10_claimed_file_absent_from_diff_dropped_and_warned() -> None:
    claims = view_payload(["src/auth.py", "ghost.py", "phantom.rb"])
    gh = fake_gh(responses=url_responses(claims))
    extractor = PrMetadataExtractor(gh=gh)
    result = extractor.extract("https://github.com/acme/widgets/pull/482", ["src/auth.py"])
    assert result.metadata["files_changed"] == "src/auth.py"
    assert any("ghost.py" in w and "phantom.rb" in w for w in result.warnings)


def test_fm10_diff_file_missing_from_claims_warns() -> None:
    gh = fake_gh(responses=url_responses(view_payload(["src/auth.py"])))
    extractor = PrMetadataExtractor(gh=gh)
    result = extractor.extract(
        "https://github.com/acme/widgets/pull/482", ["src/auth.py", "surprise.py"]
    )
    assert "surprise.py" not in result.metadata["files_changed"]
    assert any("surprise.py" in w for w in result.warnings)


def test_local_extraction_metadata(tmp_path: Path) -> None:
    diff_path = tmp_path / "change.diff"
    diff_path.write_text(SAMPLE_DIFF)
    extractor = PrMetadataExtractor(gh=fake_gh())
    result = extractor.extract(str(diff_path), ["src/auth.py"], source_path=diff_path)
    md = result.metadata
    assert md["source_type"] == "local_diff"
    assert md["file_count"] == "1"
    assert md["languages"] == "python"
    assert result.warnings == []


def test_extract_returns_result_type() -> None:
    extractor = PrMetadataExtractor(gh=fake_gh(responses=url_responses("{}")))
    result = extractor.extract("https://github.com/acme/widgets/pull/482", [])
    assert isinstance(result, ExtractionResult)


def test_gh_cli_run_wraps_subprocess(monkeypatch: pytest.MonkeyPatch) -> None:
    recorded: dict[str, object] = {}

    def fake_run(args: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        recorded["args"] = args
        return subprocess.CompletedProcess(args, 0, stdout="ok", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    rc, out, err = GhCli().run(["pr", "view", "x"])
    assert (rc, out, err) == (0, "ok", "")
    assert recorded["args"] == ["gh", "pr", "view", "x"]


def test_extract_github_with_unavailable_gh() -> None:
    """_extract_github raises actionable error when gh is not available."""
    extractor = PrMetadataExtractor(gh=FakeGh(available=False))
    with pytest.raises(MetadataExtractionError, match="gh CLI is not installed"):
        extractor.extract("https://github.com/acme/widgets/pull/482", [])
