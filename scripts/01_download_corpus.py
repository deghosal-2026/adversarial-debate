#!/usr/bin/env python3
"""Download PR diffs from corpus.csv.

Usage:
    python3 01_download_corpus.py                          # default paths
    python3 01_download_corpus.py --corpus path/to.csv     # custom corpus
    python3 01_download_corpus.py --force                  # re-download all

Requires: gh CLI authenticated.
Output: results/field-test/v0.1.0/corpus/<repo>_PR<num>.diff + .json
"""

import csv
import json
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CORPUS_CSV = BASE / "results" / "field-test" / "v0.1.0" / "corpus.csv"
CORPUS_DIR = BASE / "results" / "field-test" / "v0.1.0" / "corpus"


def download_pr(repo: str, pr_num: int, force: bool = False) -> bool:
    prefix = repo.replace("/", "_")
    diff_path = CORPUS_DIR / f"{prefix}_PR{pr_num}.diff"
    meta_path = CORPUS_DIR / f"{prefix}_PR{pr_num}.json"

    if diff_path.exists() and meta_path.exists() and not force:
        return True

    try:
        r = subprocess.run(
            ["gh", "pr", "view", str(pr_num), "--repo", repo,
             "--json", "title,body,author,state,mergedAt,additions,deletions,changedFiles,labels,comments"],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode != 0:
            print(f"  FAIL meta: {r.stderr.strip()[:80]}")
            return False
        meta_path.write_text(json.dumps(json.loads(r.stdout), indent=2))

        r = subprocess.run(
            ["gh", "pr", "diff", str(pr_num), "--repo", repo],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode != 0:
            print(f"  FAIL diff: {r.stderr.strip()[:80]}")
            return False
        diff_path.write_text(r.stdout)
        time.sleep(0.3)
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Download PR corpus")
    parser.add_argument("--corpus", default=str(CORPUS_CSV), help="Path to corpus.csv")
    parser.add_argument("--force", action="store_true", help="Re-download all")
    args = parser.parse_args()

    corpus_path = Path(args.corpus)
    if not corpus_path.is_file():
        print(f"ERROR: corpus file not found: {corpus_path}")
        sys.exit(1)

    CORPUS_DIR.mkdir(parents=True, exist_ok=True)

    with open(corpus_path) as f:
        rows = list(csv.DictReader(f))

    print(f"Downloading {len(rows)} PRs to {CORPUS_DIR}")
    ok = 0
    fail = 0

    for i, row in enumerate(rows):
        url = row["url"].strip()
        repo = row["repo"]
        pr_num = int(url.rstrip("/").split("/")[-1])
        print(f"  [{i+1}/{len(rows)}] {repo}#{pr_num} ...", end=" ", flush=True)
        if download_pr(repo, pr_num, args.force):
            print("ok")
            ok += 1
        else:
            fail += 1

    print(f"\nDone: {ok} ok, {fail} failed")


if __name__ == "__main__":
    main()
