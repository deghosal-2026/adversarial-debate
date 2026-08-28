"""PR metadata extraction: local diff paths or GitHub PR URLs via ``gh`` (WBS T4.3).

``gh`` runs behind an injected [GhRunner][...] so tests stay hermetic
(tests/conftest.py blocks all sockets); when the CLI is missing, callers get a
clear degrade-to-local-path message. FM-10 discipline
([13-failure-modes](docs/design/prd/13-failure-modes.md)): every claimed changed
file is validated against the *actual* parsed diff — mismatches are dropped and
surfaced as warnings, never silently invented.
"""

import json
import re
import shutil
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from adversarial_debate.adapters.base import MetadataExtractionError
from adversarial_debate.adapters.pr_review.language import summarize_languages

_PR_URL_RE = re.compile(r"^https?://github\.com/[\w.-]+/[\w.-]+/pull/\d+/?$")
_VIEW_FIELDS = "number,title,body,url,author,baseRefName,headRefName,files,commits"
_MAX_COMMIT_SHAS = 10
_ERROR_SNIPPET_MAX = 300


class GhRunner(Protocol):
    """Minimal ``gh`` seam: availability probe + argument-vector execution."""

    def available(self) -> bool:
        """Whether the gh CLI can be invoked on this machine."""
        ...

    def run(self, args: Sequence[str]) -> tuple[int, str, str]:
        """Run ``gh <args>``; returns (exit code, stdout, stderr)."""
        ...


class GhCli:
    """Default runner shelling out to the real ``gh`` binary."""

    def available(self) -> bool:
        """True when ``gh`` is on PATH."""
        return shutil.which("gh") is not None

    def run(self, args: Sequence[str]) -> tuple[int, str, str]:
        """Run ``gh`` capturing output as UTF-8 text; never raises on exit codes."""
        completed = subprocess.run(
            ["gh", *args], capture_output=True, check=False, text=True, encoding="utf-8"
        )
        return completed.returncode, completed.stdout, completed.stderr


@dataclass(frozen=True)
class ExtractionResult:
    """Validated metadata plus warnings about anything dropped or unclaimed."""

    metadata: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


class PrMetadataExtractor:
    """Extracts PR/diff metadata for a source that is a local path or GitHub URL."""

    def __init__(self, gh: GhRunner | None = None) -> None:
        """``gh`` defaults to the real CLI; inject a fake for hermetic tests."""
        self._gh: GhRunner = gh if gh is not None else GhCli()

    def is_pull_request_url(self, source: str) -> bool:
        """True when ``source`` looks like a github.com pull-request URL."""
        return _PR_URL_RE.match(source.strip()) is not None

    def fetch_diff(self, source: str) -> tuple[str, Path | None]:
        """Return diff text for ``source``; ``Path`` is set for local files."""
        if self.is_pull_request_url(source):
            return self._gh_diff(source.strip()), None
        path = Path(source)
        if not path.exists():
            msg = (
                f"diff not found: {source}. Pass an existing diff file path "
                "(e.g. pr-482.diff) or a GitHub PR URL"
            )
            raise MetadataExtractionError(msg)
        if not path.is_file():
            msg = f"diff source is not a file: {source}"
            raise MetadataExtractionError(msg)
        return path.read_text(encoding="utf-8", errors="replace"), path

    def extract(
        self,
        source: str,
        diff_filenames: Sequence[str],
        *,
        source_path: Path | None = None,
    ) -> ExtractionResult:
        """Build validated metadata for ``source`` given actual diff file names."""
        names = list(diff_filenames)
        if self.is_pull_request_url(source):
            return self._extract_github(source.strip(), names)
        assert source_path is not None  # fetch_diff supplies it for local sources
        return ExtractionResult(
            metadata={
                "source_type": "local_diff",
                "source_path": str(source_path),
                "file_count": str(len(names)),
                "languages": ",".join(summarize_languages(names)),
            }
        )

    def _gh_diff(self, url: str) -> str:
        if not self._gh.available():
            msg = (
                "GitHub PR URL given but the gh CLI is not installed. "
                "Install gh (https://cli.github.com), authenticate with "
                "'gh auth login', or pass a local diff file path instead."
            )
            raise MetadataExtractionError(msg)
        rc, out, err = self._gh.run(["pr", "diff", url])
        if rc != 0:
            msg = f"gh pr diff failed (exit {rc}): {_clean(err)}"
            raise MetadataExtractionError(msg)
        return out

    def _extract_github(self, url: str, names: list[str]) -> ExtractionResult:
        if not self._gh.available():
            msg = (
                "GitHub PR URL given but the gh CLI is not installed. "
                "Install gh (https://cli.github.com), authenticate with "
                "'gh auth login', or pass a local diff file path instead."
            )
            raise MetadataExtractionError(msg)
        rc, out, err = self._gh.run(["pr", "view", url, "--json", _VIEW_FIELDS])
        if rc != 0:
            msg = f"gh pr view failed (exit {rc}): {_clean(err)}"
            raise MetadataExtractionError(msg)
        try:
            data = json.loads(out)
        except json.JSONDecodeError as exc:
            msg = (
                f"gh pr view returned invalid JSON ({exc}); is the URL a real "
                "github.com pull request?"
            )
            raise MetadataExtractionError(msg) from exc

        claimed_raw = data.get("files") or []
        claimed = {str(f["path"]) for f in claimed_raw if f.get("path")}
        actual = set(names)
        kept = sorted(claimed & actual)

        author = data.get("author") or {}
        commits = [str(c["oid"]) for c in (data.get("commits") or []) if c.get("oid")]
        metadata = {
            "source_type": "github_pr",
            "pr_number": str(data.get("number", "")),
            "pr_title": str(data.get("title") or ""),
            "pr_body": str(data.get("body") or ""),
            "pr_url": str(data.get("url") or url),
            "pr_author": str(author.get("login") or ""),
            "base_ref": str(data.get("baseRefName") or ""),
            "head_ref": str(data.get("headRefName") or ""),
            "commit_count": str(len(commits)),
            "commit_shas": ",".join(commits[:_MAX_COMMIT_SHAS]),
            "files_changed": ",".join(kept),
            "languages": ",".join(summarize_languages(names)),
        }
        return ExtractionResult(metadata=metadata, warnings=_fm10_warnings(claimed, actual))


def _fm10_warnings(claimed: set[str], actual: set[str]) -> list[str]:
    warnings: list[str] = []
    dropped = sorted(claimed - actual)
    if dropped:
        warnings.append(
            "FM-10 validation: PR metadata claims file(s) absent from the diff, "
            f"dropped: {', '.join(dropped)}"
        )
    unclaimed = sorted(actual - claimed)
    if unclaimed:
        warnings.append(
            "FM-10 validation: diff contains file(s) not reported by gh "
            f"(kept for review): {', '.join(unclaimed)}"
        )
    return warnings


def _clean(text: str) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) > _ERROR_SNIPPET_MAX:
        return f"{collapsed[:_ERROR_SNIPPET_MAX]}..."
    return collapsed
