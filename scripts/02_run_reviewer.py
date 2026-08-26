#!/usr/bin/env python3
"""Run a single LLM reviewer against all PRs in the corpus.

Each model runs independently with its own checkpoint. If interrupted,
re-run the same command — it picks up where it left off.

Usage:
    # Run GPT-4o-mini (will resume from checkpoint)
    python3 02_run_reviewer.py --model openai/gpt-4o-mini

    # Run Gemini 2.5 Flash
    python3 02_run_reviewer.py --model google/gemini-2.5-flash

    # Run DeepSeek
    python3 02_run_reviewer.py --model deepseek/deepseek-chat

    # Test on 5 PRs first (cost control)
    python3 02_run_reviewer.py --model openai/gpt-4o-mini --limit 5

    # Dry run (show what would run, no API calls)
    python3 02_run_reviewer.py --model openai/gpt-4o-mini --dry-run

    # Run a single PR (debugging)
    python3 02_run_reviewer.py --model openai/gpt-4o-mini --pr kubernetes_kubernetes_PR12345

Requires: OPENROUTER_API_KEY env var
Output: results/field-test/v0.1.0/results/<model_slug>/<pr_id>.json
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CORPUS_CSV = BASE / "results" / "field-test" / "v0.1.0" / "corpus.csv"
CORPUS_DIR = BASE / "results" / "field-test" / "v0.1.0" / "corpus"
RESULTS_DIR = BASE / "results" / "field-test" / "v0.1.0" / "results"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

PRICING = {
    "openai/gpt-4o-mini": (0.15, 0.60),
    "google/gemini-2.5-flash": (0.15, 0.60),
    "deepseek/deepseek-chat": (0.27, 1.10),
    "mistralai/mistral-small-3.2-24b-instruct": (0.075, 0.20),
}

MAX_RETRIES = 3
RETRY_DELAY = 5


def compute_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    if model not in PRICING:
        return 0.0
    in_price, out_price = PRICING[model]
    return round((prompt_tokens / 1_000_000) * in_price + (completion_tokens / 1_000_000) * out_price, 6)


def load_diffs(corpus_csv: Path, pr_filter: str | None = None) -> list[dict]:
    if not corpus_csv.is_file():
        print(f"ERROR: corpus file not found: {corpus_csv}")
        sys.exit(1)

    with open(corpus_csv) as f:
        rows = list(csv.DictReader(f))

    result = []
    for row in rows:
        url = row["url"].strip()
        repo = row["repo"]
        pr_num = int(url.rstrip("/").split("/")[-1])
        prefix = repo.replace("/", "_")
        pr_id = f"{prefix}_PR{pr_num}"
        diff_path = CORPUS_DIR / f"{pr_id}.diff"

        if pr_filter and pr_filter != pr_id:
            continue

        if not diff_path.is_file():
            continue

        result.append({"url": url, "pr_id": pr_id, "diff_path": diff_path})
    return result


def call_llm(model: str, diff_text: str, api_key: str) -> dict:
    import urllib.request

    system_prompt = (
        "You are a code reviewer. Review the following git diff and identify "
        "issues. For each issue, provide: severity (high/medium/low), "
        "evidence references (file path + line numbers), and a clear "
        "description. Also note any non-claim risks. Return your response "
        "as plain text with structured sections."
    )

    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Review this diff:\n\n{diff_text}"},
        ],
        "temperature": 0.0,
        "max_tokens": 2000,
    }).encode()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/deghosal-2026/adversarial-debate",
    }

    for attempt in range(MAX_RETRIES):
        try:
            start = time.time()
            req = urllib.request.Request(OPENROUTER_URL, data=body, headers=headers)
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
            elapsed = int((time.time() - start) * 1000)

            raw_text = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            cost = compute_cost(model, prompt_tokens, completion_tokens)

            return {
                "raw_text": raw_text,
                "latency_ms": elapsed,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "cost": cost,
            }
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                print(f"retry {attempt+1}/{MAX_RETRIES} ({e})", end=" ", flush=True)
                time.sleep(RETRY_DELAY * (attempt + 1))
            else:
                raise
    return {}  # unreachable but satisfies type checker


def run_for_model(model: str, limit: int | None = None, dry_run: bool = False,
                  pr_filter: str | None = None,
                  corpus_csv: Path | None = None) -> None:
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key and not dry_run:
        print("ERROR: OPENROUTER_API_KEY env var not set")
        sys.exit(1)

    csv_path = corpus_csv or CORPUS_CSV
    model_slug = model.replace("/", "_").replace(".", "-").replace(":", "-")
    model_dir = RESULTS_DIR / model_slug
    model_dir.mkdir(parents=True, exist_ok=True)
    checkpoint = model_dir / "CHECKPOINT"

    diffs = load_diffs(csv_path, pr_filter)
    if not diffs:
        print("No PRs to process (check corpus.csv and downloaded diffs)")
        return

    done_ids: set[str] = set()
    if checkpoint.is_file():
        done_ids = set(checkpoint.read_text().strip().split("\n"))

    pending = [d for d in diffs if d["pr_id"] not in done_ids]
    if limit:
        pending = pending[:limit]

    if not pending:
        print(f"All {len(diffs)} PRs already done for {model}")
        return

    # Cost estimate
    est_cost = len(pending) * 0.002  # rough: ~2k tokens per PR at cheap rates
    print(f"Model: {model}")
    print(f"Pending: {len(pending)}/{len(diffs)} ({len(diffs) - len(pending)} cached)")
    print(f"Est cost: ~${est_cost:.2f}")

    if dry_run:
        print("\nDRY RUN — would process:")
        for d in pending:
            print(f"  {d['pr_id']}")
        return

    total_cost = 0.0
    for i, pr in enumerate(pending):
        pr_id = pr["pr_id"]
        print(f"  [{i+1}/{len(pending)}] {pr_id} ...", end=" ", flush=True)

        try:
            diff_text = pr["diff_path"].read_text()
            result = call_llm(model, diff_text, api_key)
            total_cost += result["cost"]

            output = {
                "model": model,
                "pr_url": pr["url"],
                "pr_id": pr_id,
                "diff_lines": len(diff_text.splitlines()),
                "raw_text": result["raw_text"],
                "latency_ms": result["latency_ms"],
                "prompt_tokens": result["prompt_tokens"],
                "completion_tokens": result["completion_tokens"],
                "cost": result["cost"],
            }
            (model_dir / f"{pr_id}.json").write_text(json.dumps(output, indent=2))

            done_ids.add(pr_id)
            checkpoint.write_text("\n".join(sorted(done_ids)))
            print(f"ok ({result['latency_ms']}ms, "
                  f"{result['prompt_tokens']}+{result['completion_tokens']} tok, "
                  f"${result['cost']:.4f})")

            time.sleep(1)  # rate limit politeness

        except Exception as e:
            print(f"ERROR: {e}")

    print(f"\nDone: {len(pending)} processed, ${total_cost:.4f} spent")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Run a single LLM reviewer")
    parser.add_argument("--model", required=True,
                        help="OpenRouter model (e.g. openai/gpt-4o-mini)")
    parser.add_argument("--corpus", default=None,
                        help="Path to corpus CSV (default: results/field-test/v0.1.0/corpus.csv)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Max PRs to process (for testing)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would run without API calls")
    parser.add_argument("--pr", default=None,
                        help="Run a single PR by pr_id (debugging)")
    args = parser.parse_args()

    corpus_path = Path(args.corpus) if args.corpus else None
    run_for_model(args.model, args.limit, args.dry_run, args.pr, corpus_path)


if __name__ == "__main__":
    main()
