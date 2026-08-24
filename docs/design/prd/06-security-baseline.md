# 06 — Security Baseline

> Sub-document of the [Design overview](../README.md). Isolation guarantees, data handling, threat model, reproducibility, and operational failure modes for v0.1.0.

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

## 6.4 Reproducibility & flakiness

LLM debate is stochastic — the same artifact can produce a different verdict on a second run. For audit, compliance, and trial-use cases (legal, finance), this must be controlled, not hidden.

| Concern | Stance |
|---------|--------|
| **Seed control** | All provider calls pass a configurable seed; the seed is recorded in the transcript. Re-running with the same seed + same model must reproduce the verdict. |
| **Prompt versioning** | Reviewer prompt templates are versioned (`prompt_v1`, `prompt_v2`); the version is stamped into every transcript entry. A re-run states which prompt version produced which verdict. |
| **Verdict stability** | The field-test harness runs each artifact ≥5 times (see [field-testing strategy](../../field-test/field-testing-strategy.md#measurement-protocol-all-tiers)). Artifacts where the verdict flips across >20% of runs are flagged as **flaky** in reports — never silently averaged. |
| **Honest disclosure** | Every report header states: model, model version, prompt version, seed, run count, stability rate. A single-run verdict is labeled "single-run — stability unknown." |

**What we do not promise:** determinism across *different* models or *different* prompt versions. We promise reproducibility of a specific configuration, and we expose the configuration. Buyers comparing across model pairs use the stability rate to judge whether a verdict is trustworthy or a coin-flip.

## 6.5 Operational failure modes

Real teams run this in pipelines (CI, CAB batch, contract-review queue). What happens when things break:

| Failure | Behavior |
|---------|----------|
| **Provider outage mid-debate** | Debate pauses; partial state persisted to SQLite. CLI offers `advdeb resume <artifact-id>` to continue from the last completed round. If the provider is down for >24h, the artifact is marked `incomplete` and excluded from reports. |
| **Partial transcript state** | Every claim, objection, and concession is committed individually with a sequence number. A crash at any point leaves a valid, partial transcript — never a corrupt one. Resumability is guaranteed by the audit log's append-only design. |
| **Rate-limit hit** | Engine backs off with exponential retry (configurable). If the budget ceiling is hit before debate completes, the engine produces a **partial disagreement report** with the rounds completed so far, clearly labeled `incomplete: budget_exhausted`. |
| **Schema validation failure** | If a reviewer returns malformed structured output (invalid claim, missing evidence ref), the engine fails closed: that round is retried once with a repair prompt; if it fails again, the review is marked `error` and the artifact is excluded. No silent acceptance of malformed data. |
| **Concurrent runs on same artifact** | SQLite enforces a lock per artifact ID; a second run on the same artifact while the first is in progress is rejected with a clear message. |

## 6.6 Alignment with house standards

- OWASP Agentic Top 10 awareness from day one (injection ASI01/05 posture inherited from fleet practice).
- OpenSSF Best Practices badge target at ship (fleet standard: all public repos at Passing+).
- Zero paid-LLM calls in CI; hermetic scripted-reviewer tests only.
