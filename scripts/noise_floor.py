#!/usr/bin/env python3
"""Noise-floor baseline for debate metrics via bootstrap resampling.

Measures the statistical uncertainty of aggregate debate metrics by
bootstrap-resampling existing debate results. This captures the noise
floor due to finite sample size - how much would each metric vary if
we re-ran the same pair against a resample of the same artifacts?

Does NOT re-run any LLM calls. All computation is on stored results.

Usage:
    python3 scripts/noise_floor.py
    python3 scripts/noise_floor.py --trials 5000 --seed 42

Output:
    results/field-test/v0.2.2/noise-floor-report.json
    results/field-test/v0.2.2/noise-floor-report.md  (summary)
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path
from typing import Any

BASE = Path(__file__).resolve().parent.parent
DEBATES_DIR = BASE / "results" / "field-test" / "v0.2.1" / "debates"
OUT_DIR = BASE / "results" / "field-test" / "v0.2.2"


def load_debates() -> list[dict[str, Any]]:
    """Load all debate report.json files from stored results."""
    rows = []
    for pair_dir in sorted(DEBATES_DIR.iterdir()):
        if not pair_dir.is_dir():
            continue
        for pr_dir in sorted(pair_dir.iterdir()):
            report_path = pr_dir / "report.json"
            if not report_path.is_file():
                continue
            data = json.loads(report_path.read_text())
            if data.get("total_claims", 0) == 0 and data.get("events_count", 0) == 0:
                continue
            rows.append(
                {
                    "pair": data.get("pair", pair_dir.name),
                    "convergence_score": data.get("convergence_score", 0),
                    "verdict": 1 if data.get("verdict_kind") == "verdict" else 0,
                    "theater": 1 if data.get("theater") else 0,
                    "capitulation": 1 if data.get("capitulation_cascade") else 0,
                    "concessions": data.get("concessions_count", 0),
                }
            )
    return rows


def bootstrap_ci(
    values: list[float],
    *,
    n_resamples: int = 10000,
    ci: float = 0.95,
    seed: int = 0,
) -> dict[str, float]:
    """Compute bootstrap confidence interval for a list of values."""
    if not values:
        return {"mean": 0, "std": 0, "ci_low": 0, "ci_high": 0, "n": 0}
    rng = random.Random(seed)
    means = []
    n = len(values)
    for _ in range(n_resamples):
        sample = [rng.choice(values) for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    tail = (1 - ci) / 2
    low_idx = int(tail * n_resamples)
    high_idx = int((1 - tail) * n_resamples) - 1
    mean_of_means = sum(means) / len(means)
    std = math.sqrt(sum((m - mean_of_means) ** 2 for m in means) / len(means))
    return {
        "mean": sum(values) / n,
        "std": std,
        "ci_low": means[low_idx],
        "ci_high": means[high_idx],
        "n": n,
    }


def compute_pair_metrics(
    debates: list[dict[str, Any]],
    *,
    n_resamples: int = 10000,
    seed: int = 0,
) -> dict[str, Any]:
    """Compute bootstrap CIs for all metrics for a single pair."""
    scores = [d["convergence_score"] for d in debates]
    verdicts = [float(d["verdict"]) for d in debates]
    theaters = [float(d["theater"]) for d in debates]
    capitulations = [float(d["capitulation"]) for d in debates]
    concessions = [float(d["concessions"]) for d in debates]

    return {
        "n_debates": len(debates),
        "convergence_score": bootstrap_ci(scores, n_resamples=n_resamples, seed=seed),
        "verdict_rate": bootstrap_ci(verdicts, n_resamples=n_resamples, seed=seed),
        "theater_rate": bootstrap_ci(theaters, n_resamples=n_resamples, seed=seed),
        "capitulation_rate": bootstrap_ci(capitulations, n_resamples=n_resamples, seed=seed),
        "avg_concessions": bootstrap_ci(concessions, n_resamples=n_resamples, seed=seed),
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Noise-floor baseline for debate metrics")
    parser.add_argument("--trials", type=int, default=10000, help="Bootstrap resamples per metric")
    parser.add_argument("--seed", type=int, default=0, help="RNG seed for reproducibility")
    parser.add_argument("--min-debates", type=int, default=5, help="Minimum debates per pair")
    args = parser.parse_args()

    debates = load_debates()
    pair_names = sorted({d["pair"] for d in debates})

    print(f"Loaded {len(debates)} debates across {len(pair_names)} pairs")

    report: dict[str, Any] = {
        "version": "v0.2.2",
        "bootstrap_trials": args.trials,
        "bootstrap_seed": args.seed,
        "min_debates_per_pair": args.min_debates,
        "pairs": {},
    }

    for pair in pair_names:
        pair_debates = [d for d in debates if d["pair"] == pair]
        if len(pair_debates) < args.min_debates:
            print(f"  {pair}: {len(pair_debates)} debates (skipped, below min)")
            continue
        result = compute_pair_metrics(pair_debates, n_resamples=args.trials, seed=args.seed)
        report["pairs"][pair] = result

        score = result["convergence_score"]
        cap = result["capitulation_rate"]
        theatre = result["theater_rate"]
        print(
            f"  {pair}: n={result['n_debates']}, "
            f"conv={score['mean']:.3f} +/-{score['std']:.3f} "
            f"({score['ci_low']:.3f}-{score['ci_high']:.3f}), "
            f"capit={cap['mean']:.2f} +/-{cap['std']:.2f}, "
            f"theatre={theatre['mean']:.2f} +/-{theatre['std']:.2f}"
        )

    md_lines = [
        "# Noise-Floor Baseline Report (v0.2.2)",
        "",
        f"Bootstrap resamples per metric: {args.trials}",
        f"Minimum debates per pair: {args.min_debates}",
        "Confidence interval: 95%",
        "",
        "| Pair | N | Convergence (mean +/- std) | 95% CI |",
        "|------|---|---|---|",
    ]
    for pair in sorted(report["pairs"]):
        p = report["pairs"][pair]
        cs = p["convergence_score"]
        md_lines.append(
            f"| {pair} | {p['n_debates']} | "
            f"{cs['mean']:.3f} +/-{cs['std']:.3f} | "
            f"{cs['ci_low']:.3f}-{cs['ci_high']:.3f} |"
        )

    report["_markdown"] = "\n".join(md_lines)

    json_path = OUT_DIR / "noise-floor-report.json"
    json_path.write_text(json.dumps(report, indent=2, default=str))
    md_path = OUT_DIR / "noise-floor-report.md"
    md_path.write_text(report["_markdown"])

    print(f"\nReport written to:\n  {json_path}\n  {md_path}")


if __name__ == "__main__":
    main()
