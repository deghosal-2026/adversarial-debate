#!/usr/bin/env python3
"""Ground-truth verification: side-by-side of known revert reasons vs debate claims.

Produces a CSV for manual judgment: did any debate pair surface the actual
cause of the revert/advisory?

Usage:
    python3 06_ground_truth.py --corpus results/field-test/v0.2.0/corpus.csv

Output:
    results/field-test/v0.2.0/analysis/ground-truth-comparison.csv
    Columns: artifact_id, outcome, known_reason, pair, claim_id, claim_text, severity,
             conceded_by_or_status, human_judgment (blank - fill in)
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DEBATES_DIR = BASE / "results" / "field-test" / "v0.2.0" / "debates"
ANALYSIS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "analysis"

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


def _is_substantive_claim(text: str) -> bool:
    """Check if claim text is a substantive issue statement, not metadata.

    Excludes:
    - Severity labels only (e.g. 'Severity: High', 'high')
    - Evidence headings (e.g. 'Evidence References:', 'Evidence:')
    - File paths only
    - Generic remediation text (e.g. 'Suggest: additional test coverage')
    - Very short fragments (< 15 chars)
    """
    text = text.strip()
    if len(text) < 15:
        return False

    # Severity-only patterns
    if re.match(r"^(severity|priority|risk)[:\s]*", text, re.IGNORECASE) and len(text) < 30:
        return False

    # Evidence heading patterns
    if re.match(r"^(evidence|references?|sources?)[:\s]", text, re.IGNORECASE):
        return False

    # File path only
    if re.match(r"^[\w./\\-]+\.[a-zA-Z]{2,4}(:\d+)?$", text.strip()):
        return False

    # Generic remediation template
    if text.startswith("Suggest:") or text.startswith("suggest:"):
        return False

    return True


def load_corpus(corpus_csv: Path) -> dict[str, dict]:
    """Load PR-review corpus rows keyed by artifact_id."""
    rows = {}
    with open(corpus_csv) as f:
        for row in csv.DictReader(f):
            if row.get("domain") != "pr_review":
                continue
            artifact_id = row.get("artifact_id", "").strip()
            if not artifact_id:
                repo = row["repo"]
                pr_num = int(row.get("url", row.get("source_url", "")).strip().rstrip("/").split("/")[-1])
                artifact_id = f"{repo.replace('/', '_')}_PR{pr_num}"
            row["artifact_id"] = artifact_id
            rows[artifact_id] = row
    return rows


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Ground-truth verification export")
    parser.add_argument("--corpus", required=True, help="Path to corpus CSV")
    parser.add_argument("--output", default=None,
                        help="Output CSV (default: analysis/ground-truth-comparison.csv)")
    args = parser.parse_args()

    corpus = load_corpus(Path(args.corpus))

    # Only PRs with known ground truth (revert reason documented)
    gt_prs = {
        pid: row for pid, row in corpus.items()
        if row.get("outcome") in GROUND_TRUTH_OUTCOMES and row.get("revert_reason", "").strip()
    }
    print(f"PRs with ground truth: {len(gt_prs)}")

    out_rows = []
    for pr_dir in sorted(DEBATES_DIR.iterdir()):
        if not pr_dir.is_dir():
            continue
        pair_name = pr_dir.name

        for report_path in sorted(pr_dir.glob("*/report.json")):
            d = json.loads(report_path.read_text())
            pr_id = d.get("artifact_id", d.get("pr_id", ""))

            if pr_id not in gt_prs:
                continue

            known_reason = gt_prs[pr_id]["revert_reason"].strip()

            # Resolved claims (concessions) — these are claims where one side admitted fault
            report = d.get("report", {})
            for r in report.get("resolved", []):
                claim_text = r.get("claim_text", r.get("rationale", ""))[:300]
                if not _is_substantive_claim(claim_text):
                    continue
                out_rows.append({
                    "artifact_id": pr_id,
                    "outcome": gt_prs[pr_id]["outcome"],
                    "known_reason": known_reason,
                    "pair": pair_name,
                    "claim_source": "resolved(conceded)",
                    "claim_id": r.get("claim_id", ""),
                    "claim_text": claim_text,
                    "severity": "",
                    "human_judgment": "",  # fill: MATCH / NO_MATCH / PARTIAL
                })

            # Unresolved points — surviving disagreement
            for u in report.get("unresolved", []):
                text = f"A: {u.get('position_a', '')[:150]} | B: {u.get('position_b', '')[:150]}"
                if not _is_substantive_claim(text):
                    continue
                out_rows.append({
                    "artifact_id": pr_id,
                    "outcome": gt_prs[pr_id]["outcome"],
                    "known_reason": known_reason,
                    "pair": pair_name,
                    "claim_source": "unresolved",
                    "claim_id": ",".join(u.get("claim_ids", [])),
                    "claim_text": text[:300],
                    "severity": u.get("severity", ""),
                    "human_judgment": "",
                })

    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = Path(args.output) if args.output else ANALYSIS_DIR / "ground-truth-comparison.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        if out_rows:
            w = csv.DictWriter(f, fieldnames=out_rows[0].keys())
            w.writeheader()
            w.writerows(out_rows)

    print(f"Wrote {out_path} ({len(out_rows)} rows)")
    print()
    print("Next: open the CSV and fill human_judgment column:")
    print("  MATCH    — claim text describes the same root cause as known_reason")
    print("  PARTIAL  — related but not the exact cause")
    print("  NO_MATCH — unrelated")
    print()
    matched_prs = {r["artifact_id"] for r in out_rows}
    print(f"PRs covered: {len(matched_prs)}")


if __name__ == "__main__":
    main()
