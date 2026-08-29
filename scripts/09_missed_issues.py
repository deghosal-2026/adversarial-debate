#!/usr/bin/env python3
"""CLI entry point for missed-issue measurement.

Usage:
    python3 09_missed_issues.py --corpus results/field-test/v0.2.1/corpus.csv

Output:
    results/field-test/v0.2.1/analysis/missed-issue-report.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.missed_issues import (
    ANALYSIS_DIR,
    RESULTS_DIR,
    ReviewResult,
    compute_missed_issue_rate,
    detect_missed_issue,
    extract_claims,
    format_csv_output,
)
from scripts.scripts_common import load_corpus_with_ground_truth, load_reviewer_results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Missed-issue measurement: compute recall from known-bad PRs"
    )
    parser.add_argument(
        "--corpus", required=True, help="Path to corpus CSV with ground-truth outcomes"
    )
    parser.add_argument("--output", default=None, help="Output CSV path")
    args = parser.parse_args()

    corpus_path = Path(args.corpus)
    if not corpus_path.is_file():
        print(f"ERROR: corpus file not found: {corpus_path}")
        sys.exit(1)

    gt_prs = load_corpus_with_ground_truth(corpus_path)
    if not gt_prs:
        print("No PRs with ground truth found in corpus")
        sys.exit(1)

    print(f"Loaded {len(gt_prs)} PRs with known revert reasons")

    all_results = load_reviewer_results(RESULTS_DIR)

    results: dict[str, dict[str, bool]] = {}
    for pr_id, pr_data in gt_prs.items():
        revert_reason = pr_data["revert_reason"]
        for model, model_results in all_results.items():
            if model not in results:
                results[model] = {}
            review = model_results.get(pr_id)
            if review is None:
                results[model][pr_id] = True
                continue
            claims = extract_claims(review.get("raw_text", ""))
            review_result = ReviewResult(
                artifact_id=pr_id,
                model=model,
                claims=claims,
            )
            results[model][pr_id] = not detect_missed_issue(review_result, revert_reason)

    report = compute_missed_issue_rate(
        results,
        {pid: p["revert_reason"] for pid, p in gt_prs.items()},
        domains={pid: p.get("domain", "unknown") for pid, p in gt_prs.items()},
    )

    print("\n=== Missed-Issue Rate Report ===")
    print(f"Survivorship boundary: {report['survivorship_boundary']}")
    print()
    print(f"{'Reviewer':<40} {'Rate':>8} {'Missed':>8} {'Total':>8}")
    print("-" * 68)
    for name, stats in sorted(report["pairs"].items()):
        pct = f"{stats['missed_rate'] * 100:.1f}%"
        print(f"{name:<40} {pct:>8} {stats['missed']:>8} {stats['total']:>8}")

    print()
    print(f"Dual-reviewer missed rate:  {report['dual']['missed_rate'] * 100:.1f}%")
    print(f"Single-reviewer max rate:   {report['single_max']['missed_rate'] * 100:.1f}%")
    print(f"Improvement ratio:          {report['improvement_ratio']:.1f}x")

    if report.get("per_domain"):
        print("\nPer-domain breakdown:")
        for domain, stats in report["per_domain"].items():
            pct = f"{stats['missed_rate'] * 100:.1f}%"
            print(f"  {domain:<25} {pct:>8} ({stats['missed']}/{stats['total']})")

    out_path = (
        Path(args.output) if args.output else ANALYSIS_DIR / "missed-issue-report.csv"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    csv_output = format_csv_output(report)
    out_path.write_text(csv_output)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()