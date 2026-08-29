#!/usr/bin/env python3
"""Run the debate engine on stored single-pass reviews.

Takes paired reviews from 03_combine_results.py and runs them through
the M5 DebateController → M6 EvidenceTracker → M7 SynthesisReport pipeline.

During debate rounds, calls the LLM API live via OpenRouter using the same
model that did the initial review. The stored review is round 0 only.

Usage:
    python3 04_run_debate.py --corpus results/field-test/v0.2.0/corpus.csv

    # Run a specific pair only
    python3 04_run_debate.py --corpus results/field-test/v0.2.0/corpus.csv --pair pair1_gpt_gemini

    # Run a single PR (debugging)
    python3 04_run_debate.py --corpus results/field-test/v0.2.0/corpus.csv --artifact kubernetes_kubernetes_PR141554

    # Limit PRs (testing)
    python3 04_run_debate.py --corpus results/field-test/v0.2.0/corpus.csv --limit 5

Requires: OPENROUTER_API_KEY env var

Input:  results/field-test/v0.2.0/pairs/<pair_name>/<artifact_id>.json
Output: results/field-test/v0.2.0/debates/<pair_name>/<artifact_id>/report.json
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

from scripts._seam_assert import assert_seam

BASE = Path(__file__).resolve().parent.parent
CORPUS_CSV = BASE / "results" / "field-test" / "v0.2.0" / "corpus.csv"
PAIRS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "pairs"
DEBATES_DIR = BASE / "results" / "field-test" / "v0.2.0" / "debates"


def default_pairs_for_corpus(corpus_path: Path) -> list[str]:
    name = corpus_path.name
    if name == "validation_subset.csv":
        return ["pair5_deepseek_mistral"]
    if name == "negative_control_subset.csv":
        return ["pair1_gpt_gemini"]
    return ["pair3_gpt_mistral", "pair8_deepseek_gpt_mini"]


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MAX_RETRIES = 3
RETRY_DELAY = 5

DEBATE_SYSTEM_PROMPT = (
    "You are a code reviewer in a structured adversarial debate. You committed "
    "a review independently. Now you see the other reviewer's claims and "
    "objections targeting your claims.\n\n"
    "For each objection, you MUST respond with exactly one of:\n"
    "  CONCEDED <obj_id>: you accept the objection — your claim was wrong or overstated\n"
    "  REBUTTED <obj_id>: you provide SPECIFIC evidence (file:line, test case, spec) "
    "that the objection is wrong\n"
    "  CARRIED <obj_id>: you decline to change — but you MUST cite a specific reason "
    "why the objection does not apply\n\n"
    "Rules:\n"
    "- If the other reviewer's evidence is stronger than yours, you MUST CONCEDE. "
    "Do not stubbornly CARRY — that defeats the purpose of debate.\n"
    "- CARRIED without a specific technical reason is invalid.\n"
    "- REBUTTED requires new evidence, not just restating your original claim.\n"
    "- Reference the objection ID (e.g. obj_initial_a_0) in each response.\n"
    "- Be honest: if they found a real problem you missed, concede it."
)


def load_corpus_ids(corpus_csv: Path) -> list[str]:
    """Load artifact ids from corpus CSV."""
    with open(corpus_csv) as f:
        rows = list(csv.DictReader(f))
    ids = []
    for row in rows:
        artifact_id = row.get("artifact_id", "").strip()
        if artifact_id:
            ids.append(artifact_id)
            continue
        repo = row["repo"]
        pr_num = int(row.get("url", row.get("source_url", "")).strip().rstrip("/").split("/")[-1])
        ids.append(f"{repo.replace('/', '_')}_PR{pr_num}")
    return ids


def load_pair(pair_name: str, pr_id: str) -> dict | None:
    """Load a paired review file."""
    path = PAIRS_DIR / pair_name / f"{pr_id}.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text())


def call_openrouter(model: str, prompt: str, api_key: str) -> dict:
    """Call OpenRouter API and return raw_text + usage stats."""
    body = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": DEBATE_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
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
                data = json.loads(resp.read())
            elapsed = int((time.time() - start) * 1000)

            raw_text = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)

            return {
                "raw_text": raw_text,
                "latency_ms": elapsed,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
            }
        except Exception:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
            else:
                raise
    return {}  # unreachable


class LiveProvider:
    """Provider that calls the LLM API live during debate rounds.

    Implements the DebateProvider protocol: takes a ReviewRequest,
    extracts the debate prompt from the content blocks, calls the LLM,
    and returns a ReviewResult.
    """

    def __init__(self, model: str, api_key: str) -> None:
        self._model = model
        self._api_key = api_key
        self.total_cost = 0.0
        self.total_tokens = 0
        self.call_count = 0

    def review(self, request):  # type: ignore[no-untyped-def]
        from adversarial_debate.providers.contract import (
            ReviewResult as _RR,
        )
        from adversarial_debate.providers.contract import (
            ReviewResultMetadata,
        )

        # Extract the debate prompt from the content blocks
        prompt = ""
        if request.artifact.content_blocks:
            prompt = request.artifact.content_blocks[0].content

        result = call_openrouter(self._model, prompt, self._api_key)
        self.total_tokens += result["prompt_tokens"] + result["completion_tokens"]
        self.call_count += 1

        time.sleep(1)  # rate limit politeness

        return _RR(
            raw_text=result["raw_text"],
            confidence=0.7,
            metadata=ReviewResultMetadata(
                seed=42,
                prompt_version="debate_round_v1",
                model=self._model,
            ),
        )


def parse_claims_from_review(raw_text: str, side: str, review_id: str) -> list:
    """Parse claims from raw LLM review text."""
    from adversarial_debate.schemas import Claim

    claims = []
    for i, line in enumerate(raw_text.split("\n")):
        line = line.strip()
        if not line:
            continue
        # Bullet points, numbered items, or severity-marked lines
        is_bullet = line.startswith(("-", "*", "•"))
        is_numbered = len(line) > 0 and line[0].isdigit() and "." in line[:4]
        is_severity_line = any(
            w in line.lower() for w in ["high:", "medium:", "low:", "critical:", "severity:"]
        )
        if not (is_bullet or is_numbered or is_severity_line):
            continue

        # Clean the line
        text = line.lstrip("-*•0123456789. )").strip()
        if len(text) < 5:
            continue

        # Infer severity with negation awareness
        lower = text.lower()
        negation_patterns = ["not a", "no ", "isn't", "doesn't", "won't", "without"]
        is_negated = any(n in lower for n in negation_patterns)
        if is_negated:
            severity = "medium"
        elif any(
            w in lower for w in ["high", "critical", "security", "vulnerability", "injection"]
        ):
            severity = "high"
        elif any(w in lower for w in ["low", "minor", "style", "nit", "cosmetic"]):
            severity = "low"
        else:
            severity = "medium"

        claims.append(
            Claim(
                id=f"cl_{side}_{i}",
                review_id=review_id,
                text=text[:300],
                severity=severity,
                evidence_refs=[],
                status="open",
            )
        )
    return claims


def run_debate_for_pr(pair_data: dict, api_key: str) -> dict:
    """Run the full debate pipeline on a single PR's paired reviews."""
    from adversarial_debate.engine.debate_controller import (
        DebateController,
        TokenBudget,
    )
    from adversarial_debate.engine.evidence import EvidenceTracker
    from adversarial_debate.engine.synthesis import (
        HeaderBlock,
        synthesize_verdict,
    )
    from adversarial_debate.schemas import Review, ReviewerSession

    side_a = pair_data["side_a"]
    side_b = pair_data.get("side_b")
    if side_b is None:
        msg = (
            f"side_b is null for pair {pair_data.get('pair', 'unknown')} "
            f"artifact {pair_data.get('artifact_id', 'unknown')}. "
            "Baseline pairs (single-reviewer) should use a different pipeline."
        )
        raise ValueError(msg)
    now = datetime.now(UTC)

    # Build Review objects from stored LLM output (round 0)
    artifact_id = side_a.get("artifact_id", side_a.get("pr_id"))
    review_id_a = f"rev_A_{artifact_id}"
    review_id_b = f"rev_B_{side_b.get('artifact_id', side_b.get('pr_id'))}"

    claims_a = parse_claims_from_review(side_a["raw_text"], "A", review_id_a)
    claims_b = parse_claims_from_review(side_b["raw_text"], "B", review_id_b)

    review_a = Review(
        id=review_id_a,
        session_id=f"sess_{artifact_id}_A",
        claims=claims_a,
        risks=[],
        confidence=0.7,
        committed_at=now,
    )
    review_b = Review(
        id=review_id_b,
        session_id=f"sess_{side_b.get('artifact_id', side_b.get('pr_id'))}_B",
        claims=claims_b,
        risks=[],
        confidence=0.7,
        committed_at=now,
    )

    session_a = ReviewerSession(
        id=f"sess_{artifact_id}_A",
        artifact_id=artifact_id,
        side="A",
        provider="openrouter",
        model=side_a.get("model", "unknown"),
        created_at=now,
        status="revealed",
    )
    session_b = ReviewerSession(
        id=f"sess_{side_b.get('artifact_id', side_b.get('pr_id'))}_B",
        artifact_id=side_b.get("artifact_id", side_b.get("pr_id")),
        side="B",
        provider="openrouter",
        model=side_b.get("model", "unknown"),
        created_at=now,
        status="revealed",
    )

    # Create live providers — each side calls its own model
    model_a = side_a.get("model", "openai/gpt-4o-mini")
    model_b = side_b.get("model", "google/gemini-2.5-flash")
    provider_a = LiveProvider(model_a, api_key)
    provider_b = LiveProvider(model_b, api_key)

    # Run DebateController (M5)
    controller = DebateController(
        provider_a=provider_a,
        provider_b=provider_b,
        session_a=session_a,
        session_b=session_b,
        review_a=review_a,
        review_b=review_b,
        artifact_for_prompt=artifact_id,
        max_rounds=2,
        token_budget=TokenBudget(limit=50000),
    )

    start = time.time()
    termination = controller.run()
    elapsed = int((time.time() - start) * 1000)

    # Run EvidenceTracker (M6)
    all_claims = list(claims_a) + list(claims_b)
    tracker = EvidenceTracker(
        claims=all_claims,
        concessions=termination.concessions,
        events=termination.events,
        objections=termination.objections,
    )
    evidence = tracker.compute()

    # Run SynthesisReport (M7)
    report = synthesize_verdict(
        artifact_id=artifact_id,
        evidence=evidence,
        claims_by_side={"A": claims_a, "B": claims_b},
        concessions=termination.concessions,
        header=HeaderBlock(engine_version="0.1.0"),
        events=termination.events,
    )

    # Build output
    return {
        "artifact_id": artifact_id,
        "pair": pair_data["pair"],
        "model_a": model_a,
        "model_b": model_b,
        "termination_reason": termination.reason,
        "rounds_completed": termination.rounds_completed,
        "convergence_score": evidence.convergence_score,
        "verdict_kind": evidence.verdict_kind,
        "theater": evidence.theater,
        "capitulation_cascade": evidence.capitulation_cascade,
        "resolved_count": evidence.resolved_count,
        "total_claims": evidence.total_claims,
        "concessions_count": len(termination.concessions),
        "events_count": len(termination.events),
        "latency_ms": elapsed,
        "api_calls_a": provider_a.call_count,
        "api_calls_b": provider_b.call_count,
        "total_tokens": provider_a.total_tokens + provider_b.total_tokens,
        "report": {
            "kind": report.kind,
            "verdict": report.verdict,
            "convergence_score": report.convergence_score,
            "strongest_a": report.strongest_a,
            "strongest_b": report.strongest_b,
            "resolved": [
                {
                    "claim_id": r.claim_id,
                    "conceded_by": r.conceded_by,
                    "rationale": r.rationale,
                }
                for r in report.resolved
            ],
            "unresolved": [
                {
                    "claim_ids": u.claim_ids,
                    "position_a": u.position_a,
                    "position_b": u.position_b,
                    "severity": u.severity,
                    "would_resolve_if": u.would_resolve_if,
                }
                for u in report.unresolved
            ],
            "flags": {
                "theater": report.flags.theater,
                "capitulation_cascade": report.flags.capitulation_cascade,
            },
        },
        "events": [
            {
                "round": e.round_index,
                "side": e.side,
                "kind": e.kind,
                "degraded": e.degraded,
                "error": e.error,
                "content": e.message.content if e.message else None,
            }
            for e in termination.events
        ],
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run debate engine on paired reviews")
    parser.add_argument("--corpus", default=str(CORPUS_CSV), help="Path to corpus CSV")
    parser.add_argument("--pair", default=None, help="Only run this pair (e.g. pair1_gpt_gemini)")
    parser.add_argument("--artifact", default=None, help="Only run this artifact ID")
    parser.add_argument("--limit", type=int, default=None, help="Max PRs to process")
    parser.add_argument("--force", action="store_true", help="Re-run debates even if output exists")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY env var not set")
        sys.exit(1)

    corpus_path = Path(args.corpus)
    if not corpus_path.is_file():
        print(f"ERROR: corpus file not found: {corpus_path}")
        sys.exit(1)

    pr_ids = load_corpus_ids(corpus_path)
    if args.artifact:
        pr_ids = [p for p in pr_ids if p == args.artifact]

    pair_dirs = [p for p in default_pairs_for_corpus(corpus_path) if (PAIRS_DIR / p).is_dir()]
    if args.pair:
        pair_dirs = [p for p in pair_dirs if p == args.pair]

    print(f"Running debate on {len(pr_ids)} artifacts across {len(pair_dirs)} pairs")

    total = 0
    errors = 0

    for pair_name in sorted(pair_dirs):
        if pair_name == "baseline_gpt":
            continue

        pair_out = DEBATES_DIR / pair_name
        pair_out.mkdir(parents=True, exist_ok=True)

        count = 0
        skipped_ids: list[str] = []
        for pr_id in pr_ids:
            if args.limit and count >= args.limit:
                break

            out_path = pair_out / pr_id
            if out_path.exists() and not args.force:
                # Re-run if the previous run errored (e.g. HTTP 429 rate limit)
                report_file = out_path / "report.json"
                if report_file.is_file():
                    try:
                        prev = json.loads(report_file.read_text())
                        if prev.get("termination_reason") != "error":
                            continue
                        print(f"  [{pair_name}] {pr_id} ... retrying previous error", flush=True)
                    except json.JSONDecodeError:
                        pass  # corrupt file — re-run
                else:
                    continue

            pair_data = load_pair(pair_name, pr_id)
            if pair_data is None:
                skipped_ids.append(pr_id)
                continue

            print(f"  [{pair_name}] {pr_id} ...", end=" ", flush=True)
            try:
                result = run_debate_for_pr(pair_data, api_key)
                out_path.mkdir(parents=True, exist_ok=True)
                (out_path / "report.json").write_text(json.dumps(result, indent=2))

                # Write transcript.jsonl — one JSON line per event
                with open(out_path / "transcript.jsonl", "w") as f:
                    for event in result["events"]:
                        f.write(json.dumps(event, sort_keys=True) + "\n")

                print(
                    f"ok ({result['termination_reason']}, "
                    f"score={result['convergence_score']:.2f}, "
                    f"{result['concessions_count']} concessions, "
                    f"{result['api_calls_a'] + result['api_calls_b']} API calls)"
                )
                count += 1
                total += 1
            except Exception as e:
                print(f"ERROR: {e}")
                errors += 1

        assert_seam("pair→debate", len(pr_ids), count,
                    expected="less_equal", skipped_ids=skipped_ids or None)

        print(f"  {pair_name}: {count} debates run")

    print(f"\nDone: {total} debates, {errors} errors")


if __name__ == "__main__":
    main()
