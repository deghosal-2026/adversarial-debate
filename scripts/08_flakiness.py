#!/usr/bin/env python3
"""Flakiness sweep: run each artifact's debate N times, measure verdict stability.

Runs a configured pair on an artifact subset N times.
Each run is stored separately. Then computes stability: % of runs with same
verdict per artifact.

Usage:
    python3 08_flakiness.py --corpus results/field-test/v0.2.0/corpus.csv --runs 5 --limit 10

Requires OPENROUTER_API_KEY.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

CORPUS_DEFAULT = BASE / "results" / "field-test" / "v0.2.0" / "corpus.csv"
PAIRS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "pairs"
FLAKINESS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "flakiness"
ANALYSIS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "analysis"

PAIR = "pair3_gpt_mistral"


def load_corpus_ids(corpus_csv: Path) -> list[str]:
    with open(corpus_csv) as f:
        ids = []
        for row in csv.DictReader(f):
            artifact_id = row.get("artifact_id", "").strip()
            if artifact_id:
                ids.append(artifact_id)
                continue
            repo = row["repo"]
            pr_num = int(
                row.get("url", row.get("source_url", "")).strip().rstrip("/").split("/")[-1]
            )
            ids.append(f"{repo.replace('/', '_')}_PR{pr_num}")
        return ids


def main() -> None:
    # Import 04_run_debate from the scripts directory
    scripts_dir = str(BASE / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    try:
        from importlib import import_module

        rd = import_module("04_run_debate")
    finally:
        if scripts_dir in sys.path:
            sys.path.remove(scripts_dir)

    parser = argparse.ArgumentParser(description="Flakiness sweep")
    parser.add_argument("--corpus", default=str(CORPUS_DEFAULT))
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--limit", type=int, default=10, help="Artifacts to sweep")
    parser.add_argument("--pair", default=PAIR)
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set")
        sys.exit(1)

    pr_ids = load_corpus_ids(Path(args.corpus))[: args.limit]
    out_base = FLAKINESS_DIR / args.pair
    out_base.mkdir(parents=True, exist_ok=True)

    total_runs = len(pr_ids) * args.runs
    done_runs = sum(
        1
        for pr in pr_ids
        for r in range(1, args.runs + 1)
        if (out_base / pr / f"run{r}" / "report.json").is_file()
    )
    print(
        f"Flakiness sweep: {len(pr_ids)} artifacts × {args.runs} runs "
        f"({done_runs}/{total_runs} already done)"
    )

    completed = 0
    for pr_id in pr_ids:
        pair_data = None
        for r in range(1, args.runs + 1):
            run_dir = out_base / pr_id / f"run{r}"
            report_path = run_dir / "report.json"
            if report_path.is_file():
                continue

            # Load pair data once per PR
            if pair_data is None:
                path = PAIRS_DIR / args.pair / f"{pr_id}.json"
                if not path.is_file():
                    print(f"  {pr_id}: no pair data, skipping")
                    break
                pair_data = json.loads(path.read_text())

            print(f"  [{pr_id}] run{r} ...", end=" ", flush=True)
            try:
                result = rd.run_debate_for_pr(pair_data, api_key)
                run_dir.mkdir(parents=True, exist_ok=True)
                result["sweep_run"] = r
                (run_dir / "report.json").write_text(json.dumps(result, indent=2))
                with open(run_dir / "transcript.jsonl", "w") as f:
                    for event in result["events"]:
                        f.write(json.dumps(event, sort_keys=True) + "\n")
                print(f"ok ({result['verdict_kind']}, score={result['convergence_score']:.2f})")
                completed += 1
            except Exception as e:
                print(f"ERROR: {e}")
            time.sleep(1)

    # Compute stability
    print("\n=== STABILITY ANALYSIS ===")
    rows = []
    for pr_id in pr_ids:
        verdicts = []
        scores = []
        for r in range(1, args.runs + 1):
            p = out_base / pr_id / f"run{r}" / "report.json"
            if p.is_file():
                d = json.loads(p.read_text())
                verdicts.append(d["verdict_kind"])
                scores.append(d["convergence_score"])
        if not verdicts:
            continue
        if len(verdicts) < args.runs:
            rows.append(
                {
                    "pr_id": pr_id,
                    "runs": str(len(verdicts)),
                    "verdicts": ",".join(verdicts),
                    "dominant_verdict": "incomplete",
                    "stability": "0.00",
                    "avg_convergence": "0.000",
                    "score_range": "0.00-0.00",
                    "flaky": "True",
                }
            )
            print(f"  {pr_id}: INCOMPLETE ({len(verdicts)}/{args.runs} runs)")
            continue
        counter = Counter(verdicts)
        most_common_verdict, count = counter.most_common(1)[0]
        stability = count / len(verdicts)
        avg_score = sum(scores) / len(scores)
        flaky = stability < 0.8
        rows.append(
            {
                "pr_id": pr_id,
                "runs": str(len(verdicts)),
                "verdicts": ",".join(verdicts),
                "dominant_verdict": most_common_verdict,
                "stability": f"{stability:.2f}",
                "avg_convergence": f"{avg_score:.3f}",
                "score_range": f"{min(scores):.2f}-{max(scores):.2f}",
                "flaky": str(flaky),
            }
        )
        flag = " ⚠️ FLAKY" if flaky else ""
        print(f"  {pr_id}: {most_common_verdict} ({stability:.0%}), avg={avg_score:.2f}{flag}")

    if rows:
        ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
        out = ANALYSIS_DIR / "flakiness-summary.csv"
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)

        stable = sum(1 for r in rows if r["flaky"] == "False")
        print(f"\nStable: {stable}/{len(rows)} artifacts ({stable * 100 // max(len(rows), 1)}%)")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
