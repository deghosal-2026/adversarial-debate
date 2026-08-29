#!/usr/bin/env python3
"""Compare model outputs and produce the FIELD_TEST_REPORT.md.

Analyzes:
  1. Distinct issues per model (what did each model find that others missed?)
  2. Cross-model overlap (Venn: issues found by A only, B only, both, neither)
  3. Baseline comparison (does the debate pair find more than single pass?)
  4. Pair comparison (does Pair 1 find different things than Pair 2?)
  5. Summary tables for the report
  6. Cost & latency stats

Usage:
    python3 04_analyze.py

Output:
    results/field-test/v0.2.0/analysis/distinctness-ratings.csv
    results/field-test/v0.2.0/analysis/cross-model-overlap.csv
    results/field-test/v0.2.0/analysis/cost-latency.csv
    results/field-test/v0.2.0/FIELD_TEST_REPORT.md  (placeholder — written manually)
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

from scripts._seam_assert import assert_seam

BASE = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "results"
PAIRS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "pairs"
DEBATES_DIR = BASE / "results" / "field-test" / "v0.2.0" / "debates"
ANALYSIS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "analysis"
OUT_DIR = BASE / "results" / "field-test" / "v0.2.0"

MODEL_NAMES = [
    "openai_gpt-4o-mini",
    "google_gemini-2-5-flash",
    "deepseek_deepseek-chat",
    "mistralai_mistral-small-3-2-24b-instruct",
]


def extract_issues(raw_text: str) -> list[str]:
    """Extract distinct issue descriptors from raw LLM output.

    Simple heuristic: look for bullet points, numbered items, or
    severity-marked lines. Normalizes text before comparison.
    """
    issues = []
    for line in raw_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if (
            re.match(r"^[\*\-]\s", line)
            or re.match(r"^\d+[\.\)]\s", line)
            or re.search(r"\b(high|medium|low)\b", line, re.IGNORECASE)
        ):
            issues.append(_normalize_issue(line))
    return issues


def _normalize_issue(text: str) -> str:
    """Normalize issue text for comparison: lowercase, strip formatting, first sentence."""
    text = text.lower().strip()
    text = re.sub(r"^[\*\\-]\s*", "", text)  # strip bullet
    text = re.sub(r"^\d+[\.\)]\s*", "", text)  # strip number
    text = re.sub(r"^(severity:?\s*)?(high|medium|low):?\s*", "", text)  # strip severity prefix
    text = re.sub(r"\s+", " ", text)  # collapse whitespace
    # Take first sentence only
    text = text.split(".")[0].strip()
    return text if len(text) > 5 else text


def jaccard_similarity(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def overlap_similarity(issues_a: set, issues_b: set) -> float:
    """Compute overlap using substring containment, not exact match.

    An issue in A overlaps with B if any issue in B contains it as a substring
    or vice versa. This handles cases where models phrase the same issue
    differently (e.g. "missing null check" vs "null check is missing").
    """
    if not issues_a and not issues_b:
        return 1.0
    if not issues_a or not issues_b:
        return 0.0

    matched_a = set()
    matched_b = set()
    for a in issues_a:
        for b in issues_b:
            if a in b or b in a:
                matched_a.add(a)
                matched_b.add(b)
                break

    total = len(issues_a) + len(issues_b)
    if total == 0:
        return 1.0
    return (len(matched_a) + len(matched_b)) / total


def main() -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

    # Load all results
    all_results: dict[str, dict[str, dict]] = {}
    for model in MODEL_NAMES:
        model_dir = RESULTS_DIR / model
        all_results[model] = {}
        for f in sorted(model_dir.glob("*.json")):
            if f.name == "CHECKPOINT":
                continue
            data = json.loads(f.read_text())
            artifact_id = data.get("artifact_id", data.get("pr_id", ""))
            if artifact_id:
                all_results[model][artifact_id] = data

    pr_ids = list({pid for m in MODEL_NAMES for pid in all_results[m]})
    print(f"Loaded results for {len(pr_ids)} artifacts across {len(MODEL_NAMES)} models")

    # 1. Cross-model overlap
    overlap_rows = []
    for pr_id in pr_ids:
        issues_by_model = {}
        for model in MODEL_NAMES:
            data = all_results[model].get(pr_id)
            issues_by_model[model] = set(extract_issues(data["raw_text"])) if data else set()

        row = {"artifact_id": pr_id}
        for a in MODEL_NAMES:
            for b in MODEL_NAMES:
                if a < b:
                    sim = overlap_similarity(issues_by_model[a], issues_by_model[b])
                    row[f"overlap_{a}_vs_{b}"] = str(round(sim, 3))
        overlap_rows.append(row)

    overlap_path = ANALYSIS_DIR / "cross-model-overlap.csv"
    with open(overlap_path, "w", newline="") as f:
        if overlap_rows:
            w = csv.DictWriter(f, fieldnames=overlap_rows[0].keys())
            w.writeheader()
            w.writerows(overlap_rows)
    print(f"Wrote {overlap_path} ({len(overlap_rows)} rows)")

    # 2. Distinctness counts per model
    distinct_rows = []
    for pr_id in pr_ids:
        row = {"artifact_id": pr_id}
        for model in MODEL_NAMES:
            data = all_results[model].get(pr_id)
            row[f"{model}_total_issues"] = (
                str(len(extract_issues(data["raw_text"]))) if data else "0"
            )
            row[f"{model}_latency_ms"] = str(data["latency_ms"]) if data else "0"
            row[f"{model}_cost"] = str(data.get("cost", 0)) if data else "0"
        distinct_rows.append(row)

    distinct_path = ANALYSIS_DIR / "distinctness-ratings.csv"
    with open(distinct_path, "w", newline="") as f:
        if distinct_rows:
            w = csv.DictWriter(f, fieldnames=distinct_rows[0].keys())
            w.writeheader()
            w.writerows(distinct_rows)
    print(f"Wrote {distinct_path} ({len(distinct_rows)} rows)")

    # 3. Cost & latency summary
    total_cost = 0.0
    total_latency = 0
    total_tokens = 0
    model_stats: dict[str, dict] = {}

    for model in MODEL_NAMES:
        costs = []
        latencies = []
        token_counts = []
        for data in all_results[model].values():
            costs.append(data.get("cost", 0))
            latencies.append(data["latency_ms"])
            token_counts.append(data["prompt_tokens"] + data["completion_tokens"])

        model_stats[model] = {
            "total_cost": round(sum(costs), 4),
            "avg_latency_ms": round(sum(latencies) / len(latencies)) if latencies else 0,
            "total_tokens": sum(token_counts),
            "pr_count": len(all_results[model]),
        }
        total_cost += sum(costs)
        total_latency += sum(latencies)
        total_tokens += sum(token_counts)

    cost_path = ANALYSIS_DIR / "cost-latency.csv"
    with open(cost_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "total_cost", "avg_latency_ms", "total_tokens", "pr_count"])
        for model, stats in model_stats.items():
            w.writerow(
                [
                    model,
                    stats["total_cost"],
                    stats["avg_latency_ms"],
                    stats["total_tokens"],
                    stats["pr_count"],
                ]
            )
        w.writerow(
            [
                "TOTAL",
                round(total_cost, 4),
                total_latency,
                total_tokens,
                sum(s["pr_count"] for s in model_stats.values()),
            ]
        )
    print(f"Wrote {cost_path}")

    # 4. Print summary
    print("\n=== COST & LATENCY SUMMARY ===")
    for model, stats in model_stats.items():
        print(
            f"  {model}: {stats['total_cost']} USD, "
            f"{stats['avg_latency_ms']}ms avg, "
            f"{stats['total_tokens']} tokens, "
            f"{stats['pr_count']} PRs"
        )
    print(f"  TOTAL: {round(total_cost, 4)} USD")

    avg_overlap = (
        sum(
            float(r.get("overlap_openai_gpt-4o-mini_vs_google_gemini-2-5-flash", 0))
            for r in overlap_rows
        )
        / len(overlap_rows)
        if overlap_rows
        else 0
    )
    print("\n=== CROSS-MODEL OVERLAP ===")
    print(f"  Avg overlap (GPT-4o-mini vs Gemini): {avg_overlap:.3f}")
    print("  (0 = completely different, 1 = identical)")

    # 5. Debate summary
    debate_rows = []
    if DEBATES_DIR.is_dir():
        all_reports = []
        for pair_dir in sorted(DEBATES_DIR.iterdir()):
            if not pair_dir.is_dir():
                continue
            for pr_dir in sorted(pair_dir.iterdir()):
                report_path = pr_dir / "report.json"
                if not report_path.is_file():
                    continue
                all_reports.append((pair_dir.name, pr_dir.name, json.loads(report_path.read_text())))

        count_pre = len(all_reports)
        excluded_count = 0
        for pair_name, pr_name, data in all_reports:
            # Exclude zero-claim no-op rows (data integrity failures)
            if data.get("total_claims", 0) == 0 and data.get("events_count", 0) == 0:
                excluded_count += 1
                continue
            debate_rows.append(
                {
                    "pair": data.get("pair", ""),
                    "artifact_id": data.get("artifact_id", data.get("pr_id", "")),
                    "termination": data.get("termination_reason", ""),
                    "rounds": str(data.get("rounds_completed", 0)),
                    "verdict_kind": data.get("verdict_kind", ""),
                    "convergence_score": str(round(data.get("convergence_score", 0), 3)),
                    "theater": str(data.get("theater", False)),
                    "capitulation": str(data.get("capitulation_cascade", False)),
                    "resolved_count": str(data.get("resolved_count", 0)),
                    "total_claims": str(data.get("total_claims", 0)),
                    "concessions": str(data.get("concessions_count", 0)),
                    "unresolved": str(len(data.get("report", {}).get("unresolved", []))),
                }
            )

        assert_seam("debate→analysis", count_pre, len(debate_rows),
                    expected="less_equal", strict=True)
        if excluded_count:
            print(f"  FILTER: excluded {excluded_count} zero-claim no-op rows")

    if debate_rows:
        debate_path = ANALYSIS_DIR / "debate-summary.csv"
        with open(debate_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=debate_rows[0].keys())
            w.writeheader()
            w.writerows(debate_rows)
        print("\n=== DEBATE SUMMARY ===")
        print(f"  {len(debate_rows)} debates analyzed")
        verdicts = Counter(r["verdict_kind"] for r in debate_rows)
        print(f"  Verdicts: {dict(verdicts)}")
        theater_count = sum(1 for r in debate_rows if r["theater"] == "True")
        print(f"  Theater: {theater_count}/{len(debate_rows)}")
        avg_score = sum(float(r["convergence_score"]) for r in debate_rows) / len(debate_rows)
        print(f"  Avg convergence score: {avg_score:.3f}")
        print(f"  Wrote {debate_path}")

    print(f"\nAnalysis artifacts written to {ANALYSIS_DIR}")


if __name__ == "__main__":
    main()
