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
    docs/field-test/v0.1.0/analysis/distinctness-ratings.csv
    docs/field-test/v0.1.0/analysis/cross-model-overlap.csv
    docs/field-test/v0.1.0/analysis/cost-latency.csv
    docs/field-test/v0.1.0/FIELD_TEST_REPORT.md  (placeholder — written manually)
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "../v0.1.0/results"
PAIRS_DIR = Path(__file__).parent / "../v0.1.0/pairs"
ANALYSIS_DIR = Path(__file__).parent / "../v0.1.0/analysis"
OUT_DIR = Path(__file__).parent / "../v0.1.0"

MODEL_NAMES = ["gpt-4o-mini", "gemini-2.5-flash", "deepseek-chat"]


def extract_issues(raw_text: str) -> list[str]:
    """Extract distinct issue descriptors from raw LLM output.

    Simple heuristic: look for bullet points, numbered items, or
    severity-marked lines. For v0.1 this is approximate.
    """
    issues = []
    for line in raw_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if re.match(r"^[\*\-]\s", line) or re.match(r"^\d+[\.\)]\s", line):
            issues.append(line)
        elif re.search(r"\b(high|medium|low)\b", line, re.IGNORECASE):
            issues.append(line)
    return issues


def jaccard_similarity(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


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
            all_results[model][data["pr_id"]] = data

    pr_ids = list(all_results[MODEL_NAMES[0]])
    print(f"Loaded results for {len(pr_ids)} PRs across {len(MODEL_NAMES)} models")

    # 1. Cross-model overlap
    overlap_rows = []
    for pr_id in pr_ids:
        issues_by_model = {}
        for model in MODEL_NAMES:
            data = all_results[model].get(pr_id)
            issues_by_model[model] = set(extract_issues(data["raw_text"])) if data else set()

        row = {"pr_id": pr_id}
        for a in MODEL_NAMES:
            for b in MODEL_NAMES:
                if a < b:
                    sim = jaccard_similarity(issues_by_model[a], issues_by_model[b])
                    row[f"jaccard_{a}_vs_{b}"] = str(round(sim, 3))
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
        row = {"pr_id": pr_id}
        for model in MODEL_NAMES:
            data = all_results[model].get(pr_id)
            row[f"{model}_total_issues"] = str(len(extract_issues(data["raw_text"]))) if data else "0"
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
            w.writerow([model, stats["total_cost"], stats["avg_latency_ms"],
                       stats["total_tokens"], stats["pr_count"]])
        w.writerow(["TOTAL", round(total_cost, 4), total_latency, total_tokens,
                   sum(s["pr_count"] for s in model_stats.values())])
    print(f"Wrote {cost_path}")

    # 4. Print summary
    print("\n=== COST & LATENCY SUMMARY ===")
    for model, stats in model_stats.items():
        print(f"  {model}: {stats['total_cost']} USD, "
              f"{stats['avg_latency_ms']}ms avg, "
              f"{stats['total_tokens']} tokens, "
              f"{stats['pr_count']} PRs")
    print(f"  TOTAL: {round(total_cost, 4)} USD")

    avg_jaccard = sum(r.get("jaccard_gpt-4o-mini_vs_gemini-2.5-flash", 0)
                       for r in overlap_rows) / len(overlap_rows) if overlap_rows else 0
    print(f"\n=== CROSS-MODEL OVERLAP ===")
    print(f"  Avg Jaccard (GPT-4o-mini vs Gemini): {avg_jaccard:.3f}")
    print(f"  (0 = completely different, 1 = identical)")

    print(f"\nAnalysis artifacts written to {ANALYSIS_DIR}")


if __name__ == "__main__":
    main()
