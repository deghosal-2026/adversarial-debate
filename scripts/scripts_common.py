#!/usr/bin/env python3
"""Shared utilities for field-test scripts.

Provides common helper functions used across multiple pipeline scripts.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

GROUND_TRUTH_OUTCOMES = {
    "Merged-then-reverted",
    "Merged-then-hotfixed",
    "Merged-then-security-advisory",
    "Merged-then-fixed",
    "Rejected/closed-without-merge",
    "Closed-by-author-after-review",
    "Race condition caught in review",
    "Breaking API change caught in review",
    "Refactoring that introduced regression",
}


def load_corpus_with_ground_truth(corpus_csv: Path) -> dict[str, dict]:
    """Load PR-review corpus rows with known ground truth (revert reasons)."""
    rows = {}
    with open(corpus_csv) as f:
        for row in csv.DictReader(f):
            if row.get("domain") != "pr_review":
                continue
            artifact_id = row.get("artifact_id", "").strip()
            if not artifact_id:
                repo = row["repo"]
                pr_num = int(
                    row.get("url", row.get("source_url", "")).strip().rstrip("/").split("/")[-1]
                )
                artifact_id = f"{repo.replace('/', '_')}_PR{pr_num}"
            row["artifact_id"] = artifact_id

            if (
                row.get("outcome") in GROUND_TRUTH_OUTCOMES
                and row.get("revert_reason", "").strip()
            ):
                rows[artifact_id] = row
    return rows


def load_reviewer_results(results_dir: Path) -> dict[str, dict[str, dict]]:
    """Load all reviewer results from a results directory.

    Returns:
        {model_slug: {artifact_id: result_data}}
    """
    all_results: dict[str, dict[str, dict]] = {}
    for model_dir in sorted(results_dir.iterdir()):
        if not model_dir.is_dir():
            continue
        model_slug = model_dir.name
        all_results[model_slug] = {}
        for f in sorted(model_dir.glob("*.json")):
            if f.name == "CHECKPOINT":
                continue
            data = json.loads(f.read_text())
            artifact_id = data.get("artifact_id", data.get("pr_id", ""))
            if artifact_id:
                all_results[model_slug][artifact_id] = data
    return all_results
