# M7 — Synthesis & Reports

> Goal: turn final claim states into the two product outputs — Joint Verdict (converged) or Disagreement Report (dissent preserved with `would_resolve_if`) — fail-closed, and exportable as versioned JSONL. Part of [index](index.md).

## PRD coupling

- [05-features](../../design/prd/05-features.md): F5 (verdict + surviving strongest args both sides), F6 (`resolved[]`, `unresolved[].position_a/b/would_resolve_if`), F9 (JSONL export)
- [02-architecture §2.2 Synthesis Layer](../../design/prd/02-architecture.md); [§2.7](../../design/prd/02-architecture.md) score displayed, never hidden
- [08-risks "reports accurate but unusable"](../../design/prd/08-risks.md): top-N cap on unresolved points; `would_resolve_if` mandatory discipline
- [06-security §6.3 fail-closed synthesis](../../design/prd/06-security-baseline.md): malformed data never silently accepted

## Dependencies

Upstream: M6 (Outcome + claim states). Downstream: M8 persists; M9 renders.

## Workstreams & tasks

### WS 7.a — Outputs

- [ ] T7.1 (#31) JointVerdict synthesizer: when convergence reached — decision summary + per-side strongest surviving arguments (top claims by severity upheld) + convergence_score + model/prompt-version/seed header block ([06 §6.4 honest disclosure](../../design/prd/06-security-baseline.md))
- [ ] T7.2 (#32) DisagreementReporter: `resolved[]` (with which side conceded), `unresolved[]` each with position_a, position_b, severity, and **mandatory** `would_resolve_if`; top-N cap (default 10, by severity×impact); report states debate-usefulness flags (theater/capitulation/degraded from M6/M5)

### WS 7.b — Integrity & export

- [ ] T7.3 (#33) Fail-closed synthesis: schema-validate all inputs; violation → one repair retry (regenerate offending section via ScriptedReviewer in tests) → else artifact marked `error` and excluded; no partial/silent acceptance ([06 §6.3](../../design/prd/06-security-baseline.md))
- [ ] T7.4 (#34) JSONL exporter: `export_format: v1` header (engine version, prompt versions, seeds, content hash, round count expected); one line per event in sequence order; completeness check hook for M8 verifier

## Acceptance criteria / exit gate

- Golden-output tests: same fixture+scripted reviewers ⇒ byte-stable report (determinism of synthesis layer)
- Missing `would_resolve_if` on any unresolved point is unrepresentable (schema-enforced, tested)
- Export/re-import round-trip test; truncated export detected by completeness hook
- Coverage ≥95% on `engine/synthesis*`

## Explicitly out of scope

Terminal rendering/colors (M9); SQLite storage of reports (M8).
