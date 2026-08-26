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
import re
import sys
import time
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE / "results" / "field-test" / "v0.1.0" / "analysis"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MAX_RETRIES = 3

JUDGE_PROMPT = """You are auditing an AI code-review debate. A PR was merged then reverted (or fixed/advisory). The KNOWN REASON explains why. Below are CLAIMS made by AI reviewers during debate.

Does any part of the claim describe the SAME root cause as the known reason?

Rules:
- MATCH: claim identifies the same underlying problem/cause (same file, same bug type, same failure mode)
- PARTIAL: claim is related or touches the same area but is not the actual cause
- NO_MATCH: claim is about something unrelated

Answer with exactly one word: MATCH, PARTIAL, or NO_MATCH."""


def call_llm(model: str, known_reason: str, claim_text: str, api_key: str) -> str:
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": (
                f"KNOWN REASON:\n{known_reason}\n\n"
                f"CLAIM:\n{claim_text}\n\n"
                f"Verdict (MATCH/PARTIAL/NO_MATCH):"
            )},
        ],
        "temperature": 0.0,
        "max_tokens": 10,
    }).encode()
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


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="LLM judge for ground truth")
    parser.add_argument("--model", default="openai/gpt-4o-mini",
                        help="Judge model")
    parser.add_argument("--input", default=str(ANALYSIS_DIR / "ground-truth-comparison.csv"))
    parser.add_argument("--output", default=str(ANALYSIS_DIR / "ground-truth-judged.csv"))
    parser.add_argument("--limit", type=int, default=None, help="Max rows to judge")
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
        pending = pending[:args.limit]

    print(f"Judging {len(pending)}/{len(rows)} rows with {args.model}")
    est = len(pending) * 0.0002
    print(f"Est cost: ~${est:.2f}")

    counts = {"MATCH": 0, "PARTIAL": 0, "NO_MATCH": 0, "ERROR": 0}
    for i, row in enumerate(pending):
        verdict = call_llm(args.model, row["known_reason"], row["claim_text"], api_key)
        row["human_judgment"] = f"{verdict} (llm-judge)"
        counts[verdict] = counts.get(verdict, 0) + 1

        if (i + 1) % 50 == 0:
            print(f"  [{i+1}/{len(pending)}] {counts}")
            # Incremental save
            _save(rows, out_path)

        time.sleep(0.3)

    _save(rows, out_path)
    print(f"\nDone: {counts}")
    print(f"Wrote {out_path}")


def _save(rows: list[dict], path: Path) -> None:
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
