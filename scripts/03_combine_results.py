#!/usr/bin/env python3
"""Combine individual model results into pair outputs for analysis.

Usage:
    python3 03_combine_results.py

Reads:  results/field-test/v0.1.0/results/<model>/<pr_id>.json
Writes: results/field-test/v0.1.0/pairs/<pair_name>/<pr_id>.json
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CORPUS_CSV = BASE / "results" / "field-test" / "v0.1.0" / "corpus.csv"
RESULTS_DIR = BASE / "results" / "field-test" / "v0.1.0" / "results"
PAIRS_DIR = BASE / "results" / "field-test" / "v0.1.0" / "pairs"

PAIRS = {
    "pair1_gpt_gemini": {"a": "openai_gpt-4o-mini", "b": "google_gemini-2.5-flash"},
    "pair2_gemini_deepseek": {"a": "google_gemini-2.5-flash", "b": "deepseek_deepseek-chat"},
    "homogeneous_gpt": {"a": "openai_gpt-4o-mini", "b": "openai_gpt-4o-mini"},
    "baseline_gpt": {"a": "openai_gpt-4o-mini", "b": None},
}


def load_result(model_slug: str, pr_id: str) -> dict | None:
    path = RESULTS_DIR / model_slug / f"{pr_id}.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text())


def main() -> None:
    if not CORPUS_CSV.is_file():
        print(f"ERROR: corpus.csv not found at {CORPUS_CSV}")
        sys.exit(1)

    with open(CORPUS_CSV) as f:
        rows = list(csv.DictReader(f))

    pr_ids = []
    for row in rows:
        repo = row["repo"]
        pr_num = int(row["url"].strip().rstrip("/").split("/")[-1])
        pr_ids.append(f"{repo.replace('/', '_')}_PR{pr_num}")

    print(f"Combining {len(pr_ids)} PRs across {len(PAIRS)} pairs\n")

    for pair_name, slots in PAIRS.items():
        pair_dir = PAIRS_DIR / pair_name
        pair_dir.mkdir(parents=True, exist_ok=True)
        combined = 0
        missing_a = 0
        missing_b = 0

        for pr_id in pr_ids:
            result_a = load_result(slots["a"], pr_id)
            result_b = load_result(slots["b"], pr_id) if slots["b"] else None

            if result_a is None:
                missing_a += 1
                continue
            if slots["b"] and result_b is None:
                missing_b += 1
                continue

            output = {
                "pair": pair_name,
                "pr_id": pr_id,
                "pr_url": result_a["pr_url"],
                "side_a": result_a,
                "side_b": result_b,
            }
            (pair_dir / f"{pr_id}.json").write_text(json.dumps(output, indent=2))
            combined += 1

        print(f"  {pair_name}: {combined} combined")
        if missing_a:
            print(f"    missing A ({slots['a']}): {missing_a}")
        if missing_b:
            print(f"    missing B ({slots['b']}): {missing_b}")


if __name__ == "__main__":
    main()
