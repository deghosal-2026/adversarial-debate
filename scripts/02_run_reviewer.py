#!/usr/bin/env python3
"""Run a single LLM reviewer against all artifacts in the v0.2.0 corpus.

Handles both PRs (git diff) and non-PR artifacts (plain text content).
Each model runs independently with its own checkpoint.

Usage:
    # Run GPT-4o-mini on all 150 artifacts
    python3 02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/corpus.csv

    # Test on 5 artifacts first
    python3 02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/corpus.csv --limit 5

    # Dry run
    python3 02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/corpus.csv --dry-run

    # Single artifact (debugging)
    python3 02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/corpus.csv --artifact etcd-io_etcd_PR22178

Requires: OPENROUTER_API_KEY env var
Output: results/field-test/v0.2.0/results/<model_slug>/<artifact_id>.json
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "results"
CORPUS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "corpus"

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
        msg = f"Unknown model {model!r}. Add pricing to PRICING dict."
        raise KeyError(msg)
    in_price, out_price = PRICING[model]
    return round(
        (prompt_tokens / 1_000_000) * in_price + (completion_tokens / 1_000_000) * out_price, 6
    )


def load_artifacts(corpus_csv: Path, artifact_filter: str | None = None) -> list[dict]:  # type: ignore[valid-type]
    """Load artifacts from corpus CSV, resolve content paths."""
    if not corpus_csv or not corpus_csv.is_file():
        print(f"ERROR: corpus file not found: {corpus_csv}")
        sys.exit(1)

    with open(corpus_csv) as f:
        rows = list(csv.DictReader(f))

    result = []
    for row in rows:
        aid = row.get("artifact_id", "").strip()
        domain = row.get("domain", "").strip()
        url = row.get("source_url", row.get("url", "")).strip()

        if not aid or not domain:
            continue

        if artifact_filter and artifact_filter != aid:
            continue

        # Resolve content file based on domain
        artifact_dir = CORPUS_DIR / domain / aid
        content_path = _find_content(artifact_dir, domain)
        if content_path is None:
            continue

        result.append(
            {
                "artifact_id": aid,
                "domain": domain,
                "url": url,
                "content_path": content_path,
            }
        )

    return result


def _find_content(artifact_dir: Path, domain: str) -> Path | None:
    """Find the primary content file for an artifact."""
    if domain == "pr_review":
        # PRs: look for .diff
        diffs = list(artifact_dir.glob("*.diff"))
        if diffs:
            return diffs[0]
        return None

    # Non-PR domains: content.md
    md = artifact_dir / "content.md"
    if md.is_file():
        return md

    # Fallback: any content.* file
    contents = list(artifact_dir.glob("content.*"))
    if contents:
        return contents[0]

    return None


def _build_prompt(domain: str, content: str) -> str:
    """Build a domain-specific review prompt."""
    prompts = {
        "pr_review": (
            "You are a code reviewer. Review the following git diff and identify "
            "issues. For each issue, provide: severity (high/medium/low), "
            "evidence references (file path + line numbers), and a clear "
            "description."
        ),
        "incident_response": (
            "You are an incident analyst. Review the following incident report "
            "and identify issues: missing root-cause evidence, insufficient "
            "remediation, timeline gaps, or ambiguous claims. For each issue "
            "provide severity and specific evidence from the text."
        ),
        "change_management": (
            "You are a change advisory board reviewer. Review the following "
            "change plan and identify: rollback gaps, unmitigated risks, "
            "insufficient testing, ambiguous preconditions, or missing "
            "stakeholder sign-off. For each issue provide severity and "
            "specific evidence."
        ),
        "security_incidents": (
            "You are a security analyst. Review the following security "
            "advisory or incident disclosure and identify: exploitability "
            "ambiguity, insufficient mitigation, scope understatement, or "
            "missing patch details. For each issue provide severity and "
            "specific evidence."
        ),
    }
    base = prompts.get(domain, prompts["pr_review"])
    prepared_content = content if domain == "pr_review" else _prepare_non_pr_content(content)
    return f"{base}\n\n---\n\n{prepared_content}"


def _prepare_non_pr_content(content: str, max_chars: int = 10000) -> str:
    """Strip HTML chrome and bound non-PR content before sending to the model."""
    lowered = content.lower()
    if "<html" in lowered or "<!doctype html" in lowered:
        content = re.sub(
            r"<script\b[^>]*>.*?</script>", " ", content, flags=re.IGNORECASE | re.DOTALL
        )
        content = re.sub(
            r"<style\b[^>]*>.*?</style>", " ", content, flags=re.IGNORECASE | re.DOTALL
        )
        content = re.sub(r"<[^>]+>", " ", content)
        content = re.sub(r"&nbsp;", " ", content, flags=re.IGNORECASE)
        content = re.sub(r"&amp;", "&", content, flags=re.IGNORECASE)

    content = re.sub(r"\s+", " ", content).strip()
    # De-duplicate obvious repetitive dashboard/history noise.
    tokens = content.split(" ")
    compacted: list[str] = []
    repeat_count = 0
    previous = ""
    for token in tokens:
        if token == previous:
            repeat_count += 1
            if repeat_count >= 3:
                continue
        else:
            previous = token
            repeat_count = 0
        compacted.append(token)
    content = " ".join(compacted)

    if len(content) <= max_chars:
        return content
    return content[:max_chars] + "\n\n[truncated for prompt budget]"


def call_llm(model: str, content: str, api_key: str) -> dict:
    import urllib.request

    body = json.dumps(
        {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert reviewer. Be thorough and specific.",
                },
                {"role": "user", "content": content},
            ],
            "temperature": 0.0,
            "max_tokens": 2000,
        }
    ).encode()

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
                raw_body = resp.read()
                data = json.loads(raw_body)
            elapsed = int((time.time() - start) * 1000)

            if "choices" not in data or not data["choices"]:
                error_body = raw_body[:500].decode("utf-8", errors="replace")
                raise ValueError(f"API returned no 'choices': {error_body}")

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
    return {}


def run_for_model(
    model: str,
    limit: int | None = None,
    dry_run: bool = False,
    artifact_filter: str | None = None,
    corpus_csv: Path | None = None,
) -> None:
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key and not dry_run:
        print("ERROR: OPENROUTER_API_KEY env var not set")
        sys.exit(1)

    model_slug = model.replace("/", "_").replace(".", "-").replace(":", "-")
    model_dir = RESULTS_DIR / model_slug
    model_dir.mkdir(parents=True, exist_ok=True)
    checkpoint = model_dir / "CHECKPOINT"

    artifacts = load_artifacts(corpus_csv, artifact_filter)  # type: ignore[arg-type]
    if not artifacts:
        print("No artifacts to process (check corpus.csv and downloaded content)")
        return

    done_ids: set[str] = set()
    if checkpoint.is_file():
        done_ids = set(checkpoint.read_text().strip().split("\n"))

    pending = [a for a in artifacts if a["artifact_id"] not in done_ids]
    if limit:
        pending = pending[:limit]

    if not pending:
        print(f"All {len(artifacts)} artifacts already done for {model}")
        return

    if model in PRICING:
        in_price, out_price = PRICING[model]
        avg_tokens = 2000
        avg_in = avg_out = avg_tokens / 2
        est_cost = len(pending) * (
            (avg_in / 1_000_000) * in_price + (avg_out / 1_000_000) * out_price
        )
    else:
        est_cost = len(pending) * 0.002

    print(f"Model: {model}")
    print(f"Pending: {len(pending)}/{len(artifacts)} ({len(artifacts) - len(pending)} cached)")
    print(f"Domains: {sorted(set(a['domain'] for a in pending))}")
    print(f"Est cost: ~${est_cost:.2f}")

    if dry_run:
        print("\nDRY RUN — would process:")
        for a in pending:
            print(f"  {a['domain']}/{a['artifact_id']}")
        return

    total_cost = 0.0
    for i, art in enumerate(pending):
        aid = art["artifact_id"]
        domain = art["domain"]
        print(f"  [{i+1}/{len(pending)}] {domain}/{aid} ...", end=" ", flush=True)

        try:
            content = art["content_path"].read_text()
            prompt = _build_prompt(domain, content)

            result = call_llm(model, prompt, api_key)
            total_cost += result["cost"]

            output = {
                "model": model,
                "artifact_id": aid,
                "domain": domain,
                "artifact_url": art["url"],
                "content_lines": len(content.splitlines()),
                "raw_text": result["raw_text"],
                "latency_ms": result["latency_ms"],
                "prompt_tokens": result["prompt_tokens"],
                "completion_tokens": result["completion_tokens"],
                "cost": result["cost"],
            }
            (model_dir / f"{aid}.json").write_text(json.dumps(output, indent=2))

            done_ids.add(aid)
            checkpoint.write_text("\n".join(sorted(done_ids)))
            print(
                f"ok ({result['latency_ms']}ms, "
                f"{result['prompt_tokens']}+{result['completion_tokens']} tok, "
                f"${result['cost']:.4f})"
            )

            time.sleep(1)

        except Exception as e:
            print(f"ERROR: {e}")

    print(f"\nDone: {len(pending)} processed, ${total_cost:.4f} spent")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run a single LLM reviewer")
    parser.add_argument("--model", required=True)
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--artifact", default=None)
    args = parser.parse_args()

    corpus_path = Path(args.corpus)
    run_for_model(args.model, args.limit, args.dry_run, args.artifact, corpus_path)  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
