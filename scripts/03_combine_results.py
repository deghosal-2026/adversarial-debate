#!/usr/bin/env python3
"""Combine individual model results into pair outputs for analysis.

Usage:
    python3 03_combine_results.py

Reads:  results/field-test/v0.2.1/results/<model>/<artifact_id>.json
Writes: results/field-test/v0.2.1/pairs/<pair_name>/<artifact_id>.json
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from scripts._seam_assert import assert_seam

BASE = Path(__file__).resolve().parent.parent
CORPUS_CSV = BASE / "results" / "field-test" / "v0.2.1" / "corpus.csv"
RESULTS_DIR = BASE / "results" / "field-test" / "v0.2.1" / "results"
PAIRS_DIR = BASE / "results" / "field-test" / "v0.2.1" / "pairs"

PAIRS = {
    "pair1_gpt_gemini": {"a": "openai_gpt-4o-mini", "b": "google_gemini-2-5-flash"},
    "pair2_gemini_deepseek": {"a": "google_gemini-2-5-flash", "b": "deepseek_deepseek-chat"},
    "pair3_gpt_mistral": {
        "a": "openai_gpt-4o-mini",
        "b": "mistralai_mistral-small-3-2-24b-instruct",
    },
    "pair4_gemini_mistral": {
        "a": "google_gemini-2-5-flash",
        "b": "mistralai_mistral-small-3-2-24b-instruct",
    },
    "pair5_deepseek_mistral": {
        "a": "deepseek_deepseek-chat",
        "b": "mistralai_mistral-small-3-2-24b-instruct",
    },
    "homogeneous_gpt": {"a": "openai_gpt-4o-mini", "b": "openai_gpt-4o-mini"},
    "baseline_gpt": {"a": "openai_gpt-4o-mini", "b": None},
    "pair8_deepseek_gpt_mini": {"a": "deepseek_deepseek-chat", "b": "openai_gpt-4o-mini"},
}


def default_pairs_for_corpus(corpus_path: Path) -> list[str]:
    name = corpus_path.name
    if name == "validation_subset.csv":
        return ["pair5_deepseek_mistral"]
    if name == "negative_control_subset.csv":
        return ["pair1_gpt_gemini"]
    return ["pair3_gpt_mistral", "pair8_deepseek_gpt_mini", "baseline_gpt"]


def load_artifact_ids(rows: list[dict[str, str]]) -> list[str]:
    """Extract artifact ids from a mixed v0.2.1 corpus CSV."""
    artifact_ids: list[str] = []
    for row in rows:
        artifact_id = row.get("artifact_id", "").strip()
        if artifact_id:
            artifact_ids.append(artifact_id)
            continue

        repo = row.get("repo", "").strip()
        url = row.get("url", row.get("source_url", "")).strip()
        if not repo or not url:
            continue

        pr_num = int(url.rstrip("/").split("/")[-1])
        artifact_ids.append(f"{repo.replace('/', '_')}_PR{pr_num}")
    return artifact_ids


def load_result(model_slug: str, pr_id: str) -> dict | None:
    path = RESULTS_DIR / model_slug / f"{pr_id}.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text())


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Combine model results into pairs")
    parser.add_argument(
        "--corpus",
        default=None,
        help="Path to corpus CSV (default: results/field-test/v0.2.1/corpus.csv)",
    )
    parser.add_argument(
        "--pair",
        action="append",
        default=None,
        help="Pair(s) to combine. Defaults to the approved v0.2.1 set.",
    )
    args = parser.parse_args()

    csv_path = Path(args.corpus) if args.corpus else CORPUS_CSV
    if not csv_path.is_file():
        print(f"ERROR: corpus file not found at {csv_path}")
        sys.exit(1)

    with open(csv_path) as f:
        rows = list(csv.DictReader(f))

    artifact_ids = load_artifact_ids(rows)

    selected_pairs = args.pair or default_pairs_for_corpus(csv_path)
    print(f"Combining {len(artifact_ids)} artifacts across {len(selected_pairs)} pairs\n")

    for pair_name in selected_pairs:
        slots = PAIRS[pair_name]
        pair_dir = PAIRS_DIR / pair_name
        pair_dir.mkdir(parents=True, exist_ok=True)
        combined = 0
        missing_a: list[str] = []
        missing_b: list[str] = []

        for artifact_id in artifact_ids:
            result_a = load_result(slots["a"], artifact_id)
            result_b = load_result(slots["b"], artifact_id) if slots["b"] else None

            if result_a is None:
                missing_a.append(artifact_id)
                continue
            if slots["b"] and result_b is None:
                missing_b.append(artifact_id)
                continue

            output = {
                "pair": pair_name,
                "artifact_id": artifact_id,
                "artifact_url": result_a.get("artifact_url", result_a.get("pr_url", "")),
                "side_a": result_a,
                "side_b": result_b,
            }
            (pair_dir / f"{artifact_id}.json").write_text(json.dumps(output, indent=2))
            combined += 1

        assert_seam("review→pair", len(artifact_ids), combined,
                    expected="less_equal",
                    skipped_ids=(missing_a + missing_b) or None)
        print(f"  {pair_name}: {combined} combined")
        if missing_a:
            print(f"    missing A ({slots['a']}): {len(missing_a)} — {missing_a[:5]}")
        if missing_b:
            print(f"    missing B ({slots['b']}): {len(missing_b)} — {missing_b[:5]}")


if __name__ == "__main__":
    main()
