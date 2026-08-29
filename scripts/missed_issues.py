#!/usr/bin/env python3
"""Missed-issue measurement for adversarial-debate (importable module).

Provides dataclasses and functions for measuring missed-issue rates from
known-bad PRs. The CLI entry point is in 09_missed_issues.py.

Usage (as module):
    from scripts.missed_issues import detect_missed_issue, ReviewResult
    from scripts.missed_issues import compute_missed_issue_rate, format_csv_output
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "results"
ANALYSIS_DIR = BASE / "results" / "field-test" / "v0.2.0" / "analysis"

STOP_WORDS: set[str] = {
    "the", "a", "an", "is", "was", "are", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can",
    "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "through", "during", "before", "after", "above",
    "below", "between", "and", "but", "or", "nor", "not", "so",
    "yet", "both", "either", "neither", "this", "that", "these",
    "those", "it", "its", "they", "them", "their", "we", "our",
    "you", "your", "he", "she", "him", "her", "his", "more",
    "most", "some", "any", "each", "every", "all", "no", "none",
    "if", "then", "else", "when", "where", "why", "how", "what",
    "which", "who", "whom", "about", "up", "down", "out", "off",
    "over", "under", "again", "further", "once", "here", "there",
    "system", "also", "just", "very", "too", "really", "quite",
}


@dataclass
class ReviewResult:
    """Result of a single reviewer on a single artifact."""
    artifact_id: str
    model: str
    claims: list[str]


@dataclass
class KnownBadPR:
    """A PR with a documented revert reason."""
    pr_id: str
    revert_reason: str
    domain: str
    pre_fix_path: str | None = None


@dataclass
class MissedIssueReport:
    """Report of missed-issue rates per pair and per reviewer."""
    per_pair: dict[str, dict[str, float]] = field(default_factory=dict)
    per_domain: dict[str, dict[str, float]] = field(default_factory=dict)
    survivorship_boundary: str = ""


def _get_keywords(text: str) -> set[str]:
    """Extract meaningful keywords from text, excluding stop words."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    words = set(text.split())
    return words - STOP_WORDS


def detect_missed_issue(result: ReviewResult, revert_reason: str) -> bool:
    """Check if the reviewer's claims address the known revert reason.

    Uses keyword overlap between claims and the revert reason.
    Returns True if the issue was missed (no claim addresses the revert reason).
    """
    if not result.claims:
        return True

    revert_keywords = _get_keywords(revert_reason)
    if not revert_keywords:
        return True

    for claim in result.claims:
        claim_text = claim.strip()
        if len(claim_text) < 5:
            continue
        claim_keywords = _get_keywords(claim_text)
        if claim_keywords & revert_keywords:
            return False

    return True


def compute_missed_issue_rate(
    results: dict[str, dict[str, bool]],
    known_revert_reasons: dict[str, str],
    domains: dict[str, str] | None = None,
) -> dict:
    """Compute missed-issue rate per pair and per reviewer.

    Args:
        results: {reviewer_name: {pr_id: not_missed (True if detected)}}
        known_revert_reasons: {pr_id: revert_reason}
        domains: {pr_id: domain} for per-domain breakdown

    Returns:
        dict with per_pair, per_domain, and survivorship_boundary
    """
    total_prs = len(known_revert_reasons)

    if total_prs == 0:
        return {
            "pairs": {r: {"missed_rate": 0.0, "total": 0, "missed": 0}
                     for r in results},
            "dual": {"missed_rate": 0.0, "total": 0, "missed": 0},
            "single_max": {"missed_rate": 0.0, "total": 0, "missed": 0},
            "improvement_ratio": 1.0,
            "per_domain": {},
            "survivorship_boundary": (
                "lower bound — 0 documented failures measured"
            ),
        }

    report: dict = {}

    # Per-reviewer
    per_pair = {}
    for reviewer_name, pr_results in results.items():
        missed = sum(1 for v in pr_results.values() if not v)
        total = len(pr_results) or 1
        per_pair[reviewer_name] = {
            "missed_rate": missed / total,
            "total": len(pr_results),
            "missed": missed,
        }
    report["pairs"] = per_pair

    # Dual-reviewer: both missed
    all_pr_ids = set(known_revert_reasons.keys())
    dual_missed = 0
    for pr_id in all_pr_ids:
        all_reviewers_missed = all(
            not results.get(r, {}).get(pr_id, False)
            for r in results
        )
        if all_reviewers_missed:
            dual_missed += 1
    dual_total = len(all_pr_ids) or 1
    report["dual"] = {
        "missed_rate": dual_missed / dual_total,
        "total": dual_total,
        "missed": dual_missed,
    }

    # Single-reviewer max
    single_max_missed = max(
        (p["missed"] for p in per_pair.values()),
        default=0,
    )
    single_max_total = max(
        (p["total"] for p in per_pair.values()),
        default=1,
    )
    report["single_max"] = {
        "missed_rate": single_max_missed / single_max_total,
        "total": single_max_total,
        "missed": single_max_missed,
    }

    # Improvement ratio
    dual_rate = report["dual"]["missed_rate"]
    single_rate = report["single_max"]["missed_rate"]
    report["improvement_ratio"] = (
        round(single_rate / dual_rate, 1) if dual_rate > 0 else 1.0
    )

    # Per-domain
    per_domain = {}
    if domains:
        domain_prs: dict[str, dict[str, bool]] = {}
        for pr_id, domain in domains.items():
            if domain not in domain_prs:
                domain_prs[domain] = {}
            all_missed = all(
                not results.get(r, {}).get(pr_id, False)
                for r in results
            )
            domain_prs[domain][pr_id] = all_missed

        for domain, prs in domain_prs.items():
            missed = sum(1 for v in prs.values() if v)
            total = len(prs) or 1
            per_domain[domain] = {
                "missed_rate": missed / total,
                "total": total,
                "missed": missed,
            }
    report["per_domain"] = per_domain

    report["survivorship_boundary"] = (
        f"lower bound — {total_prs} documented failures measured. "
        f"Undocumented failures are not measurable."
    )

    return report


def format_csv_output(report: dict) -> str:
    """Format the missed-issue report as CSV."""
    output_lines = []
    output_lines.append("pair_name,missed_rate,missed,total,improvement_ratio")

    for pair_name, stats in report.get("pairs", {}).items():
        pct = f"{stats['missed_rate'] * 100:.1f}%"
        output_lines.append(
            f"{pair_name},{pct},{stats['missed']},{stats['total']},"
            f"{report.get('improvement_ratio', 1.0)}"
        )

    return "\n".join(output_lines) + "\n"


def extract_claims(raw_text: str) -> list[str]:
    """Extract claim text from raw LLM output."""
    claims = []
    for line in raw_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        is_bullet = line.startswith(("-", "*", "•"))
        is_numbered = bool(re.match(r"^\d+[\.\)]\s", line))
        if not (is_bullet or is_numbered):
            continue
        text = re.sub(r"^[-*•\d\.\)\s]+", "", line).strip()
        if len(text) >= 5:
            claims.append(text)
    return claims
