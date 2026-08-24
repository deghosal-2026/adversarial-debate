# 06 — Security Baseline

> Sub-document of the [Design overview](../README.md). Isolation guarantees, data handling, and threat model for v0.1.0.

## 6.1 Core guarantees

| Guarantee | Mechanism |
|-----------|-----------|
| **Reviewer independence** | Separate conversation contexts per reviewer; no shared memory; revelation is an explicit engine state transition, logged |
| **Commit immutability** | A committed review cannot be amended — only rebutted in debate; concessions are new events, not edits |
| **Auditability** | Full lineage persisted locally (SQLite): every prompt, response, claim event, concession, verdict — exportable JSONL |
| **Advisory posture** | The engine never executes actions; outputs inform humans and downstream gates |

## 6.2 Data handling

- **Local-first:** transcripts and state live in the user's SQLite database by default. Nothing is sent anywhere except to the LLM endpoints the user configures.
- **BYOM boundary:** artifacts go only to user-designated providers — including private VPC or local deployments for sensitive documents. No telemetry home.
- **Secrets hygiene:** provider keys via env/config, never logged, never persisted into transcripts or reports.
- **Retention controls (nice-to-have 0.1, committed 0.2):** configurable transcript retention + redaction hooks before export.

## 6.3 Threat model (v0.1.0 scope)

| Threat | Vector | Mitigation |
|--------|--------|------------|
| Prompt injection via artifact | Malicious diff/doc text steering a reviewer | Artifacts treated as untrusted content; structured output validation on every reviewer message; reviewers get **no tool access** in v0.1 (read-only reasoning) |
| Debate resource exhaustion | Adversarial loops inflating token spend | Hard round caps, per-artifact budget ceiling, fail-closed synthesis on schema violations |
| Fake independence | "Debate mode" bolted onto shared context | Independence enforced mechanically (separate sessions), not prompted; audit log proves session separation |
| Consensus theater | Reviewers agreeing to agree | Theater-rate metric: debates with zero state changes are flagged as such in reports |
| Transcript leakage | Shared/exported logs containing sensitive artifact content | Local-first storage, redaction hooks, retention policy |

## 6.4 Alignment with house standards

- OWASP Agentic Top 10 awareness from day one (injection ASI01/05 posture inherited from fleet practice).
- OpenSSF Best Practices badge target at ship (fleet standard: all public repos at Passing+).
- Zero paid-LLM calls in CI; hermetic scripted-reviewer tests only.
