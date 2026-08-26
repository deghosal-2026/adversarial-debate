#!/usr/bin/env python3
"""Run the debate engine on stored single-pass reviews.

Takes paired reviews from 03_combine_results.py and runs them through
the M5 DebateController → M6 EvidenceTracker → M7 SynthesisReport pipeline.

Usage:
    python3 05_run_debate.py --corpus results/field-test/v0.1.0/corpus.csv

Input:  results/field-test/v0.1.0/pairs/<pair_name>/<pr_id>.json
Output: results/field-test/v0.1.0/debates/<pair_name>/<pr_id>/
          ├── transcript.jsonl
          ├── report.json
          └── metadata.json
"""

from __future__ import annotations

import csv
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CORPUS_CSV = BASE / "results" / "field-test" / "v0.1.0" / "corpus.csv"
PAIRS_DIR = BASE / "results" / "field-test" / "v0.1.0" / "pairs"
DEBATES_DIR = BASE / "results" / "field-test" / "v0.1.0" / "debates"


def load_corpus_ids(corpus_csv: Path) -> list[str]:
    """Load PR IDs from corpus CSV."""
    with open(corpus_csv) as f:
        rows = list(csv.DictReader(f))
    ids = []
    for row in rows:
        repo = row["repo"]
        pr_num = int(row["url"].strip().rstrip("/").split("/")[-1])
        ids.append(f"{repo.replace('/', '_')}_PR{pr_num}")
    return ids


def load_pair(pair_name: str, pr_id: str) -> dict | None:
    """Load a paired review file."""
    path = PAIRS_DIR / pair_name / f"{pr_id}.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text())


def run_debate_for_pr(pair_data: dict) -> dict:
    """Run the debate engine on a single PR's paired reviews.

    This wires M5 (DebateController) → M6 (EvidenceTracker) → M7 (SynthesisReport).
    """
    from adversarial_debate.engine.debate_controller import (
        DebateController,
        DebateEvent,
        TokenBudget,
    )
    from adversarial_debate.engine.evidence import EvidenceTracker
    from adversarial_debate.engine.synthesis import (
        HeaderBlock,
        synthesize_verdict,
    )
    from adversarial_debate.providers.contract import (
        ReviewRequest,
        ReviewResult,
        ReviewResultMetadata,
    )
    from adversarial_debate.schemas import Claim, Review, ReviewerSession

    side_a = pair_data["side_a"]
    side_b = pair_data["side_b"]

    # Build Review objects from stored LLM output
    now = datetime.now(UTC)

    def make_review(side_data: dict, side: str) -> Review:
        review_id = f"rev_{side}_{side_data['pr_id']}"
        session_id = f"sess_{side_data['pr_id']}"

        # Parse claims from raw text (lightweight)
        claims = []
        for i, line in enumerate(side_data["raw_text"].split("\n")):
            line = line.strip()
            if line and (line.startswith(("-", "*", "•")) or line[0].isdigit()):
                severity = "medium"
                lower = line.lower()
                if "high" in lower or "critical" in lower or "security" in lower:
                    severity = "high"
                elif "low" in lower or "minor" in lower or "style" in lower:
                    severity = "low"
                claims.append(Claim(
                    id=f"cl_{side}_{i}",
                    review_id=review_id,
                    text=line[:200],
                    severity=severity,
                    evidence_refs=[],
                    status="open",
                ))

        return Review(
            id=review_id,
            session_id=session_id,
            claims=claims,
            risks=[],
            confidence=0.7,
            committed_at=now,
        )

    def make_session(side_data: dict, side: str) -> ReviewerSession:
        return ReviewerSession(
            id=f"sess_{side_data['pr_id']}_{side}",
            artifact_id=side_data["pr_id"],
            side=side,  # type: ignore[arg-type]
            provider=side_data.get("provider", "unknown"),
            model=side_data.get("model", "unknown"),
            created_at=now,
            status="revealed",
        )

    review_a = make_review(side_a, "A")
    review_b = make_review(side_b, "B")
    session_a = make_session(side_a, "A")
    session_b = make_session(side_b, "B")

    # Create a simple provider that returns the stored review text
    class StoredProvider:
        def __init__(self, review_text: str) -> None:
            self._text = review_text

        def review(self, request: ReviewRequest) -> ReviewResult:
            return ReviewResult(
                raw_text=self._text,
                confidence=0.7,
                metadata=ReviewResultMetadata(
                    seed=42,
                    prompt_version="v1",
                    model="stored",
                ),
            )

    provider_a = StoredProvider(side_a["raw_text"])
    provider_b = StoredProvider(side_b["raw_text"])

    # Run DebateController (M5)
    controller = DebateController(
        provider_a=provider_a,
        provider_b=provider_b,
        session_a=session_a,
        session_b=session_b,
        review_a=review_a,
        review_b=review_b,
        artifact_for_prompt=side_a["pr_id"],
        max_rounds=2,
        token_budget=TokenBudget(limit=50000),
    )

    start = time.time()
    termination = controller.run()
    elapsed = int((time.time() - start) * 1000)

    # Run EvidenceTracker (M6)
    all_claims = list(review_a.claims) + list(review_b.claims)
    tracker = EvidenceTracker(
        claims=all_claims,
        concessions=termination.concessions,
        events=termination.events,
    )
    evidence = tracker.compute()

    # Run SynthesisReport (M7)
    report = synthesize_verdict(
        artifact_id=side_a["pr_id"],
        evidence=evidence,
        claims_by_side={"A": review_a.claims, "B": review_b.claims},
        concessions=termination.concessions,
        header=HeaderBlock(engine_version="0.1.0"),
    )

    # Build output
    return {
        "pr_id": side_a["pr_id"],
        "pair": pair_data["pair"],
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
    parser.add_argument("--corpus", default=str(CORPUS_CSV),
                        help="Path to corpus CSV")
    parser.add_argument("--pair", default=None,
                        help="Only run this pair (e.g. pair1_gpt_gemini)")
    parser.add_argument("--pr", default=None,
                        help="Only run this PR ID")
    parser.add_argument("--limit", type=int, default=None,
                        help="Max PRs to process")
    args = parser.parse_args()

    corpus_path = Path(args.corpus)
    pr_ids = load_corpus_ids(corpus_path)
    if args.pr:
        pr_ids = [p for p in pr_ids if p == args.pr]

    pair_dirs = [d.name for d in PAIRS_DIR.iterdir() if d.is_dir()]
    if args.pair:
        pair_dirs = [p for p in pair_dirs if p == args.pair]

    print(f"Running debate on {len(pr_ids)} PRs across {len(pair_dirs)} pairs")

    total = 0
    errors = 0

    for pair_name in sorted(pair_dirs):
        if pair_name == "baseline_gpt":
            continue  # baseline has no debate

        pair_out = DEBATES_DIR / pair_name
        pair_out.mkdir(parents=True, exist_ok=True)

        count = 0
        for pr_id in pr_ids:
            if args.limit and count >= args.limit:
                break

            out_path = pair_out / pr_id
            if out_path.exists():
                continue

            pair_data = load_pair(pair_name, pr_id)
            if pair_data is None:
                continue

            print(f"  [{pair_name}] {pr_id} ...", end=" ", flush=True)
            try:
                result = run_debate_for_pr(pair_data)
                out_path.mkdir(parents=True, exist_ok=True)
                (out_path / "report.json").write_text(json.dumps(result, indent=2))

                print(f"ok ({result['termination_reason']}, "
                      f"score={result['convergence_score']:.2f}, "
                      f"{result['concessions_count']} concessions)")
                count += 1
                total += 1
            except Exception as e:
                print(f"ERROR: {e}")
                errors += 1

        print(f"  {pair_name}: {count} debates run")

    print(f"\nDone: {total} debates, {errors} errors")


if __name__ == "__main__":
    main()
