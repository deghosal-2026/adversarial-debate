#!/usr/bin/env python3
"""Download non-PR artifacts for the v0.2.0 mixed-domain field test.

PR artifacts are already copied from v0.1.0 corpus; this script skips
them and only downloads incident, change, and security artifacts.

Usage:
    python3 scripts/01_download_corpus_v2.py
    python3 scripts/01_download_corpus_v2.py --corpus docs/field-test/v0.2.0/corpus.csv
    python3 scripts/01_download_corpus_v2.py --force

Requires: gh CLI authenticated, curl.
Output:   results/field-test/v0.2.0/corpus/<domain>/<artifact_id>/
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DEFAULT_CORPUS_CSV = BASE / "results" / "field-test" / "v0.2.0" / "corpus.csv"
DEFAULT_CORPUS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "corpus"

# Domains we already have PR artifacts for
PR_DOMAIN = "pr_review"


def _gh_run(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["gh"] + args, capture_output=True, text=True, timeout=timeout
    )


def _curl(url: str, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["curl", "-sS", "-L", "--max-time", str(timeout), url],
        capture_output=True, text=True, timeout=timeout + 5,
    )


# ── Web (generic) ──────────────────────────────────────────────────────────────


def _download_web(url: str, out_dir: Path, force: bool) -> bool:
    """Save a web page as content.md."""
    content_path = out_dir / "content.md"
    if content_path.exists() and not force:
        return True
    r = _curl(url)
    if r.returncode != 0:
        print(f"    FAIL curl: {r.stderr.strip()[:80]}")
        return False
    content_path.write_text(r.stdout)
    time.sleep(0.5)
    return True


def _download_raw_github(url: str, out_dir: Path, force: bool) -> bool:
    """Fetch a raw GitHub content URL (convert blob URL to raw URL)."""
    raw_url = (
        url.replace("https://github.com/", "https://raw.githubusercontent.com/")
        .replace("/blob/", "/")
    )
    ext = Path(url).suffix or ".md"
    out_path = out_dir / f"content{ext}"
    if out_path.exists() and not force:
        return True
    r = _curl(raw_url)
    if r.returncode != 0:
        print(f"    FAIL curl raw: {r.stderr.strip()[:80]}")
        return False
    out_path.write_text(r.stdout)
    time.sleep(0.5)
    return True


def _download_github_api(endpoint: str, out_dir: Path, force: bool) -> bool:
    """Fetch a GitHub API endpoint as JSON."""
    safe = endpoint.replace("/", "_").replace("?", "_").replace("&", "_")
    out_path = out_dir / f"api_{safe}.json"
    if out_path.exists() and not force:
        return True
    r = _gh_run(["api", endpoint])
    if r.returncode != 0:
        print(f"    FAIL gh api: {r.stderr.strip()[:80]}")
        return False
    out_path.write_text(r.stdout)
    time.sleep(0.3)
    return True


# ── Domain dispatch ────────────────────────────────────────────────────────────


def _download_incident(row: dict, out_dir: Path, force: bool) -> bool:
    """Download incident response artifact (always web page)."""
    url = row.get("source_url", "")
    return _download_web(url, out_dir, force)


def _download_change(row: dict, out_dir: Path, force: bool) -> bool:
    """Download change management artifact (web or raw GitHub)."""
    url = row.get("source_url", "")
    if "raw.githubusercontent.com" in url:
        return _download_web(url, out_dir, force)
    if "github.com" in url and "/blob/" in url:
        return _download_raw_github(url, out_dir, force)
    return _download_web(url, out_dir, force)


def _download_security(row: dict, out_dir: Path, force: bool) -> bool:
    """Download security incident artifact (web + possibly GH API)."""
    url = row.get("source_url", "")
    if "/advisories/" in url and "github.com" in url:
        ghsa_id = url.rstrip("/").split("/")[-1]
        _download_github_api(f"/advisories/{ghsa_id}", out_dir, force)
    return _download_web(url, out_dir, force)


DISPATCH = {
    "incident_response": _download_incident,
    "change_management": _download_change,
    "security_incidents": _download_security,
}


# ── Main loop ──────────────────────────────────────────────────────────────────


def download_artifact(row: dict, out_dir: Path, force: bool) -> bool:
    domain = row.get("domain", "").strip()
    artifact_id = row.get("artifact_id", "").strip()

    if not artifact_id:
        return False

    # Skip PRs — already copied from v0.1.0
    if domain == PR_DOMAIN:
        return True

    downloader = DISPATCH.get(domain)
    if downloader is None:
        return False

    artifact_dir = out_dir / domain / artifact_id
    artifact_dir.mkdir(parents=True, exist_ok=True)

    if not (artifact_dir / "source.json").exists() or force:
        (artifact_dir / "source.json").write_text(
            json.dumps(dict(row), indent=2, sort_keys=True)
        )

    return downloader(row, artifact_dir, force)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Download non-PR corpus for v0.2.0 field test"
    )
    parser.add_argument(
        "--corpus", default=str(DEFAULT_CORPUS_CSV),
        help=f"Corpus CSV path (default: {DEFAULT_CORPUS_CSV})",
    )
    parser.add_argument(
        "--out", default=str(DEFAULT_CORPUS_DIR),
        help=f"Output directory (default: {DEFAULT_CORPUS_DIR})",
    )
    parser.add_argument("--force", action="store_true", help="Re-download all")
    parser.add_argument(
        "--domain", help="Restrict to one domain (e.g. incident_response)"
    )
    parser.add_argument("--limit", type=int, help="Max artifacts to download")
    args = parser.parse_args()

    corpus_path = Path(args.corpus)
    if not corpus_path.is_file():
        print(f"ERROR: corpus file not found: {corpus_path}")
        sys.exit(1)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(corpus_path) as f:
        rows = list(csv.DictReader(f))

    if args.domain:
        rows = [r for r in rows if r.get("domain", "").strip() == args.domain]
    if args.limit:
        rows = rows[: args.limit]

    to_download = [r for r in rows if r.get("domain", "").strip() != PR_DOMAIN]
    print(f"Downloading {len(to_download)} non-PR artifacts to {out_dir}")
    print(f"  (skipping {len(rows) - len(to_download)} PR artifacts)")

    ok = 0
    fail = 0
    for i, r in enumerate(to_download):
        aid = r.get("artifact_id", f"row-{i}")
        dom = r.get("domain", "?")
        print(f"  [{i+1}/{len(to_download)}] {dom}/{aid} ...", end=" ", flush=True)
        if download_artifact(r, out_dir, args.force):
            print("ok")
            ok += 1
        else:
            print("FAIL")
            fail += 1

    print(f"\nDone: {ok} ok, {fail} failed")


if __name__ == "__main__":
    main()