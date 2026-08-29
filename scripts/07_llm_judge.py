#!/usr/bin/env python3
"""LLM-as-judge: fill human_judgment column in ground-truth-comparison.csv.

Uses an LLM to classify each debate claim against the known revert/advisory
reason: MATCH / PARTIAL / NO_MATCH. Spot-check results before trusting.

Usage:
    python3 07_llm_judge.py --model openai/gpt-4o-mini
    python3 07_llm_judge.py --model deepseek/deepseek-chat --limit 100

Requires OPENROUTER_API_KEY.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE / "results" / "field-test" / "v0.2.1" / "analysis"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_RETRIES = 3

JUDGE_PROMPT = """You are auditing an AI code-review debate. A PR was merged then reverted (or fixed/advisory). The KNOWN REASON explains why. Below are CLAIMS made by AI reviewers during debate.

Does any part of the claim describe the SAME root cause as the known reason?

Rules:
- MATCH: claim identifies the same underlying problem/cause (same file, same bug type, same failure mode)
- PARTIAL: claim is related or touches the same area but is not the actual cause
- NO_MATCH: claim is about something unrelated

Answer with exactly one word: MATCH, PARTIAL, or NO_MATCH."""


def _row_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    artifact_id = row.get("artifact_id", row.get("pr_id", ""))
    return (
        artifact_id,
        row.get("pair", ""),
        row.get("claim_id", ""),
        row.get("claim_source", ""),
    )


def _merge_chunk_outputs(chunk_dir: Path, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    merged_dict: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for cf in sorted(chunk_dir.glob("chunk_*.csv")):
        with open(cf, newline="") as f:
            for r in csv.DictReader(f):
                key = _row_key(r)
                existing = merged_dict.get(key)
                if existing is None or (
                    not existing.get("human_judgment") and r.get("human_judgment")
                ):
                    merged_dict[key] = r

    merged = list(merged_dict.values())
    judged_keys = {_row_key(r) for r in merged}
    for r in rows:
        key = _row_key(r)
        if key not in judged_keys:
            merged.append(r)
    return merged


def call_llm(model: str, known_reason: str, claim_text: str, api_key: str) -> str:
    body = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": JUDGE_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"KNOWN REASON:\n{known_reason}\n\n"
                        f"CLAIM:\n{claim_text}\n\n"
                        f"Verdict (MATCH/PARTIAL/NO_MATCH):"
                    ),
                },
            ],
            "temperature": 0.0,
            "max_tokens": 10,
        }
    ).encode()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(OPENROUTER_URL, data=body, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read())
            answer = data["choices"][0]["message"]["content"].strip().upper()
            # Extract the verdict
            for verdict in ("MATCH", "PARTIAL", "NO_MATCH"):
                if verdict in answer:
                    return verdict
            return "NO_MATCH"  # fallback
        except Exception:
            if attempt < MAX_RETRIES - 1:
                time.sleep(5 * (attempt + 1))
            else:
                return "ERROR"
    return "ERROR"  # unreachable


def judge_chunk(
    chunk: list[dict], model: str, api_key: str, chunk_path: Path, worker_id: int
) -> dict:
    """Judge a chunk of rows and save to its own file."""
    counts = {"MATCH": 0, "PARTIAL": 0, "NO_MATCH": 0, "ERROR": 0}
    for i, row in enumerate(chunk):
        verdict = call_llm(model, row["known_reason"], row["claim_text"], api_key)
        row["human_judgment"] = f"{verdict} (llm-judge:{model})"
        counts[verdict] = counts.get(verdict, 0) + 1

        if (i + 1) % 25 == 0:
            _save(chunk, chunk_path)

        time.sleep(0.3)

    _save(chunk, chunk_path)
    return counts


def main() -> None:
    import argparse
    from concurrent.futures import ThreadPoolExecutor, as_completed

    parser = argparse.ArgumentParser(description="LLM judge for ground truth")
    parser.add_argument("--model", default="openai/gpt-4o-mini", help="Judge model")
    parser.add_argument("--input", default=str(ANALYSIS_DIR / "ground-truth-comparison.csv"))
    parser.add_argument("--output", default=str(ANALYSIS_DIR / "ground-truth-judged.csv"))
    parser.add_argument("--limit", type=int, default=None, help="Max rows to judge")
    parser.add_argument("--workers", type=int, default=6, help="Parallel workers (default 6)")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set")
        sys.exit(1)

    in_path = Path(args.input)
    out_path = Path(args.output)
    if not in_path.is_file():
        print(f"ERROR: {in_path} not found — run 06_ground_truth.py first")
        sys.exit(1)

    with open(in_path) as f:
        rows = list(csv.DictReader(f))

    # Skip already-judged rows on resume
    pending = [r for r in rows if not r.get("human_judgment")]
    if args.limit:
        pending = pending[: args.limit]

    total_workers = args.workers
    print(f"Judging {len(pending)}/{len(rows)} rows with {args.model} ({total_workers} workers)")
    est = len(pending) * 0.0002
    print(f"Est cost: ~${est:.2f}")

    # Split pending into chunks, one per worker — each writes its own file
    # Chunk dir is unique per input file so parallel runs don't collide
    input_stem = in_path.stem  # e.g. ground-truth-comparison or ground-truth-comparison-c0
    chunk_dir = ANALYSIS_DIR / f"judge-chunks-{input_stem}"
    chunk_dir.mkdir(parents=True, exist_ok=True)

    chunk_size = max(1, len(pending) // total_workers + 1)
    chunks = [pending[i : i + chunk_size] for i in range(0, len(pending), chunk_size)]

    total_counts = {"MATCH": 0, "PARTIAL": 0, "NO_MATCH": 0, "ERROR": 0}

    with ThreadPoolExecutor(max_workers=total_workers) as pool:
        futures = {}
        for w, chunk in enumerate(chunks):
            chunk_path = chunk_dir / f"chunk_{w:02d}.csv"
            # Resume: load existing chunk progress if present
            if chunk_path.is_file():
                with open(chunk_path, newline="") as f:
                    judged = {
                        (
                            r.get("pr_id", ""),
                            r.get("pair", ""),
                            r.get("claim_id", ""),
                            r.get("claim_source", ""),
                        ): r.get("human_judgment", "")
                        for r in csv.DictReader(f)
                    }
                for r in chunk:
                    key = (
                        r.get("pr_id", ""),
                        r.get("pair", ""),
                        r.get("claim_id", ""),
                        r.get("claim_source", ""),
                    )
                    if not r.get("human_judgment") and key in judged and judged[key]:
                        r["human_judgment"] = judged[key]
            futures[pool.submit(judge_chunk, chunk, args.model, api_key, chunk_path, w)] = (
                w,
                chunk,
            )

        for future in as_completed(futures):
            worker_id, chunk = futures[future]
            try:
                counts = future.result()
                for k, v in counts.items():
                    total_counts[k] += v
                print(f"  worker {worker_id}: finished ({len(chunk)} rows) {counts}")
            except Exception as e:
                print(f"  worker {worker_id}: ERROR {e}")

    merged = _merge_chunk_outputs(chunk_dir, rows)

    _save(merged, out_path)
    print(f"\nDone: {total_counts}")
    print(f"Merged {len(merged)} rows -> {out_path}")


def _save(rows: list[dict], path: Path) -> None:
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
