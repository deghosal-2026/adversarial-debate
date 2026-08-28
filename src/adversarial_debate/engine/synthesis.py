"""Synthesis layer: JointVerdict, DisagreementReporter, fail-closed synthesis, JSONL export.

M7 core (T7.1-T7.4). Consumes M6 EvidenceContext and produces the two product
outputs — Joint Verdict (converged) or Disagreement Report (dissent preserved)
— with mandatory ``would_resolve_if`` on every unresolved point (DD-06).

Key invariants:
- ``would_resolve_if`` is mandatory on every unresolved point (DD-06, schema-enforced)
- Convergence score is always displayed, never hidden (§2.7)
- Malformed data is never silently accepted (§6.3 fail-closed)
- Reports are byte-stable given the same input (determinism)
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Literal

from adversarial_debate.engine.debate_controller import DebateEvent
from adversarial_debate.engine.evidence import ClaimSnapshot, EvidenceContext
from adversarial_debate.schemas import Claim
from adversarial_debate.schemas.debate import Concession, Severity, Side


@dataclass(frozen=True)
class HeaderBlock:
    """Report header with reproduction metadata (§6.4 honest disclosure).

    ``engine_version`` from the package; ``prompt_version`` and ``seeds``
    allow exact replay; ``stability_notice`` flags single-run uncertainty.
    """

    engine_version: str = "0.1.0"
    prompt_version: str = "v1"
    seeds: dict[str, int | None] = field(default_factory=dict)
    stability_notice: str = "single-run; stability unknown (N=1)"

    def to_dict(self) -> dict[str, object]:
        """Serialize to dict for report output."""
        return {
            "engine_version": self.engine_version,
            "prompt_version": self.prompt_version,
            "seeds": dict(self.seeds),
            "stability_notice": self.stability_notice,
        }


@dataclass(frozen=True)
class ResolvedEntry:
    """One resolved disagreement: which side conceded and why."""

    claim_id: str
    claim_text: str
    severity: Severity
    conceded_by: Side
    rationale: str


@dataclass(frozen=True)
class UnresolvedEntry:
    """One surviving disagreement with mandatory would_resolve_if (DD-06)."""

    claim_ids: list[str]
    position_a: str
    position_b: str
    severity: Severity
    would_resolve_if: str  # mandatory per DD-06 — schema-enforced


@dataclass(frozen=True)
class ReportFlags:
    """Debate-usefulness flags surfaced in the report header.

    These tell the consumer whether to trust or discount the output.
    """

    theater: bool = False
    capitulation_cascade: bool = False
    degraded_rounds: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class SynthesisReport:
    """The complete synthesis output — one of these per artifact.

    ``kind`` is ``"verdict"`` when converged, ``"disputed"`` otherwise.
    Every unresolved entry carries a mandatory ``would_resolve_if``.
    """

    kind: Literal["verdict", "disputed"]
    artifact_id: str
    header: HeaderBlock
    verdict: str  # decision summary
    strongest_a: list[str]  # side A's strongest surviving arguments
    strongest_b: list[str]  # side B's strongest surviving arguments
    resolved: list[ResolvedEntry]
    unresolved: list[UnresolvedEntry]
    flags: ReportFlags
    convergence_score: float
    total_claims: int
    resolved_count: int


# ── T7.1 (#31) JointVerdict synthesizer ───────────────────────────────────────


def synthesize_verdict(  # noqa: PLR0913, D417
    artifact_id: str,
    evidence: EvidenceContext,
    claims_by_side: dict[Side, list[Claim]],
    concessions: list[Concession],
    header: HeaderBlock | None = None,
    max_unresolved: int = 10,
    events: list[DebateEvent] | None = None,
) -> SynthesisReport:
    """Build the full synthesis report from evidence context.

    When convergence is reached (``evidence.verdict_kind == "verdict"``),
    produces a verdict with per-side strongest arguments. Otherwise produces
    a dispute report with unresolved points.

    Args:
        artifact_id: The artifact that was debated.
        evidence: The M6 EvidenceContext.
        claims_by_side: Claims grouped by side (A/B).
        concessions: All concessions from the debate.
        header: Optional header block (auto-generated if None).
        max_unresolved: Top-N cap on unresolved points (default 10).

    Returns:
        A complete ``SynthesisReport``.
    """
    header = header or HeaderBlock()

    # Build strongest arguments per side
    strongest_a = _strongest_arguments(claims_by_side.get("A", []), evidence.claims)
    strongest_b = _strongest_arguments(claims_by_side.get("B", []), evidence.claims)

    # Build resolved entries
    resolved = _build_resolved(concessions, evidence.claims)

    # Build unresolved entries
    unresolved = _build_unresolved(
        evidence=evidence,
        claims_by_side=claims_by_side,
        max_unresolved=max_unresolved,
    )

    # Build flags
    degraded_rounds = _find_degraded_rounds(evidence, events)
    flags = ReportFlags(
        theater=evidence.theater,
        capitulation_cascade=evidence.capitulation_cascade,
        degraded_rounds=degraded_rounds,
    )

    # Decision summary
    if evidence.verdict_kind == "verdict":
        verdict = (
            f"Verdict reached after debate. "
            f"All {evidence.total_claims} claims resolved "
            f"(convergence score: {evidence.convergence_score:.2f})."
        )
    else:
        verdict = (
            f"Disagreement persists after debate. "
            f"{evidence.resolved_count}/{evidence.total_claims} claims resolved "
            f"(convergence score: {evidence.convergence_score:.2f})."
        )

    return SynthesisReport(
        kind=evidence.verdict_kind,
        artifact_id=artifact_id,
        header=header,
        verdict=verdict,
        strongest_a=strongest_a,
        strongest_b=strongest_b,
        resolved=resolved,
        unresolved=unresolved,
        flags=flags,
        convergence_score=evidence.convergence_score,
        total_claims=evidence.total_claims,
        resolved_count=evidence.resolved_count,
    )


def _strongest_arguments(
    side_claims: list[Claim],
    snapshots: list[ClaimSnapshot],
) -> list[str]:
    """Top claims by severity for a side."""
    claim_ids = {c.id for c in side_claims}
    relevant = [
        s
        for s in snapshots
        if s.id in claim_ids and s.final_status in ("upheld", "open", "resolved")
    ]
    severity_order = {"high": 0, "medium": 1, "low": 2}
    relevant.sort(key=lambda s: severity_order.get(s.severity, 99))
    return [f"[{s.severity}] {s.text}" for s in relevant[:5]]


def _build_resolved(
    concessions: list[Concession],
    claim_snapshots: list[ClaimSnapshot],
) -> list[ResolvedEntry]:
    """Build resolved entries from concessions and claim snapshots."""
    snapshot_map = {s.id: s for s in claim_snapshots}
    resolved: list[ResolvedEntry] = []
    for c in concessions:
        snap = snapshot_map.get(c.claim_id)
        if snap is None:
            logging.warning("Claim %s not found in snapshots; text will be unknown", c.claim_id)
            text = "(unknown claim)"
            severity: Severity = "medium"
        else:
            text = snap.text
            severity = snap.severity
        resolved.append(
            ResolvedEntry(
                claim_id=c.claim_id,
                claim_text=text,
                severity=severity,
                conceded_by=c.by_side,
                rationale=c.rationale,
            )
        )
    return resolved


def _build_unresolved(
    evidence: EvidenceContext,
    claims_by_side: dict[Side, list[Claim]],
    max_unresolved: int = 10,
) -> list[UnresolvedEntry]:
    """Build unresolved entries from remaining open claims."""
    side_a_map = {c.id: c for c in claims_by_side.get("A", [])}
    side_b_map = {c.id: c for c in claims_by_side.get("B", [])}

    open_snapshots = [s for s in evidence.claims if s.final_status == "open"]
    # Sort by severity (high first), then limit
    severity_order = {"high": 0, "medium": 1, "low": 2}
    open_snapshots.sort(key=lambda s: severity_order.get(s.severity, 99))
    open_snapshots = open_snapshots[:max_unresolved]

    unresolved: list[UnresolvedEntry] = []
    for snap in open_snapshots:
        claim_a = side_a_map.get(snap.id)
        claim_b = side_b_map.get(snap.id)
        unresolved.append(
            UnresolvedEntry(
                claim_ids=[snap.id],
                position_a=claim_a.text if claim_a else "(not raised by side A)",
                position_b=claim_b.text if claim_b else "(not raised by side B)",
                severity=snap.severity,
                would_resolve_if=_generate_would_resolve_if(snap),
            )
        )
    return unresolved


def _generate_would_resolve_if(snapshot: ClaimSnapshot) -> str:
    """Generate a plausible would_resolve_if for an unresolved claim.

    For MVP this produces a template string. In production this would be
    generated by the LLM during the debate's final round.
    """
    return (
        f"Side agreeing would need to see evidence addressing: "
        f"{snapshot.text}. "
        f"Suggest: additional test coverage or a security review."
    )


def _find_degraded_rounds(
    evidence: EvidenceContext,  # noqa: ARG001
    events: list[DebateEvent] | None = None,
) -> list[int]:
    """Identify rounds that were marked degraded by scanning debate events."""
    if events is None:
        return []
    return sorted({e.round_index for e in events if e.degraded})


# ── T7.3 (#33) Fail-closed synthesis ──────────────────────────────────────────


class SynthesisValidationError(Exception):
    """Raised when synthesis inputs fail schema validation."""


def validate_synthesis_inputs(
    evidence: EvidenceContext,
    claims_by_side: dict[Side, list[Claim]],
) -> list[str]:
    """Validate synthesis inputs before report generation.

    Returns a list of violation messages. Empty list = inputs are valid.
    Raises ``SynthesisValidationError`` on critical issues.
    """
    violations: list[str] = []

    if evidence.total_claims < 0:
        violations.append("total_claims cannot be negative")

    if evidence.resolved_count < 0:
        violations.append("resolved_count cannot be negative")

    if evidence.resolved_count > evidence.total_claims:
        violations.append("resolved_count exceeds total_claims")

    if evidence.convergence_score < 0.0 or evidence.convergence_score > 1.0:
        violations.append("convergence_score out of [0, 1] range")

    # Check claims_by_side has at least one side
    if not claims_by_side:
        violations.append("claims_by_side is empty")

    # Compare unique claim IDs rather than raw list lengths
    unique_ids_from_sides = {c.id for side_claims in claims_by_side.values() for c in side_claims}
    if len(unique_ids_from_sides) != evidence.total_claims and evidence.total_claims > 0:
        violations.append(
            f"unique claim IDs from sides ({len(unique_ids_from_sides)}) "
            f"does not match evidence.total_claims ({evidence.total_claims})"
        )

    if violations:
        msg = "; ".join(violations)
        raise SynthesisValidationError(msg)

    return violations


# ── T7.4 (#34) JSONL exporter ────────────────────────────────────────────────


@dataclass(frozen=True)
class ExportHeader:
    """Versioned JSONL export header (line 1 of the export file).

    ``content_hash`` allows the consumer to verify the source artifact.
    ``round_count_expected`` enables the M8 completeness check hook.
    """

    format: str = "v1"
    engine_version: str = "0.1.0"
    prompt_version: str = "v1"
    seeds: dict[str, int | None] = field(default_factory=dict)
    content_hash: str = ""
    round_count_expected: int = 0


_ENGINE_VERSION = "0.1.0"


def _build_jsonl_header(
    report: SynthesisReport,
    events: list[DebateEvent],
    content_hash: str = "",
) -> dict[str, object]:
    """Build the first JSONL line (the header)."""
    round_events = [e for e in events if e.round_index > 0]
    max_round = max((e.round_index for e in round_events), default=0)
    return {
        "type": "header",
        "format": "v1",
        "engine_version": _ENGINE_VERSION,
        "prompt_version": report.header.prompt_version,
        "seeds": dict(report.header.seeds),
        "content_hash": content_hash,
        "round_count_expected": max_round,
        "artifact_id": report.artifact_id,
    }


def export_jsonl(
    report: SynthesisReport,
    events: list[DebateEvent],
    content_hash: str = "",
) -> str:
    """Export the full debate lineage as a newline-delimited JSON string.

    Line 1 is the header with reproduction metadata.
    Subsequent lines are events in sequence order.
    A final ``__completeness__`` line allows the M8 verifier to detect
    truncation.

    Args:
        report: The SynthesisReport to export.
        events: All DebateEvents in sequence order.
        content_hash: SHA-256 of the source artifact content.

    Returns:
        A newline-delimited JSON string.
    """
    lines: list[str] = []

    # Line 1: header
    header = _build_jsonl_header(report, events, content_hash)
    lines.append(json.dumps(header, sort_keys=True))

    # Event lines
    for event in events:
        event_dict: dict[str, object] = {
            "type": "event",
            "round": event.round_index,
            "side": event.side,
            "kind": event.kind,
            "degraded": event.degraded,
        }
        if event.message:
            event_dict["content"] = event.message.content
        if event.concession:
            event_dict["concession"] = {
                "claim_id": event.concession.claim_id,
                "by_side": event.concession.by_side,
                "round": event.concession.round,
                "rationale": event.concession.rationale,
            }
        if event.error:
            event_dict["error"] = event.error
        lines.append(json.dumps(event_dict, sort_keys=True))

    # Report line
    report_dict: dict[str, object] = {
        "type": "report",
        "kind": report.kind,
        "verdict": report.verdict,
        "convergence_score": report.convergence_score,
        "resolved_count": report.resolved_count,
        "total_claims": report.total_claims,
        "strongest_a": list(report.strongest_a),
        "strongest_b": list(report.strongest_b),
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
            "degraded_rounds": list(report.flags.degraded_rounds),
        },
    }
    lines.append(json.dumps(report_dict, sort_keys=True))

    # Completeness check line
    total_lines = len(lines) + 1  # +1 for the completeness line itself
    completeness: dict[str, object] = {
        "type": "__completeness__",
        "total_lines_expected": total_lines,
        "content_hash": content_hash,
    }
    lines.append(json.dumps(completeness, sort_keys=True))

    return "\n".join(lines) + "\n"


def verify_export(export_text: str) -> bool:
    """Verify an exported JSONL string is complete (not truncated).

    Checks that the last line is a ``__completeness__`` line and that
    ``total_lines_expected`` matches the actual line count.

    Returns:
        True if the export is verified complete.
    """
    stripped = export_text.strip()
    if not stripped:
        return False

    lines = stripped.split("\n")
    try:
        last = json.loads(lines[-1])
    except (json.JSONDecodeError, IndexError):
        return False

    if not isinstance(last, dict) or last.get("type") != "__completeness__":
        return False

    expected = last.get("total_lines_expected")
    if not isinstance(expected, int):
        return False

    return len(lines) == expected


__all__ = [
    "ExportHeader",
    "HeaderBlock",
    "ReportFlags",
    "ResolvedEntry",
    "SynthesisReport",
    "SynthesisValidationError",
    "UnresolvedEntry",
    "export_jsonl",
    "synthesize_verdict",
    "validate_synthesis_inputs",
    "verify_export",
]
