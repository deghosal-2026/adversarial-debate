# M6 — Evidence Tracker & Convergence Detection

> Goal: first-class evidence objects with append-only state transitions, mechanical convergence scoring, theater detection, and evidence-reference validation. This is where "did anything actually change?" becomes computable. Part of [index](index.md).

## PRD coupling

- [05-features](../../design/prd/05-features.md): F3 (schema), F4 (concessions as events)
- [02-architecture §2.7 convergence detection](../../design/prd/02-architecture.md): claim-state lifecycle; convergence = no `open` claims; score = resolved/total; concession-theater mitigation
- [07-success §7.2 theater rate](../../design/prd/07-success-metrics.md) + [§7.6 how computed](../../design/prd/07-success-metrics.md)
- [13-failure-modes FM-2 capitulation cascade, FM-7 confidence-without-evidence](../../design/prd/13-failure-modes.md)

## Dependencies

Upstream: M5 (debate events). Downstream: M7 (synthesis reads final states).

## Workstreams & tasks

### WS 6.a — Evidence tracking

- [ ] T6.1 EvidenceTracker: applies controller events to claim lifecycle (`open→conceded|upheld|resolved`); every transition is an append-only `Concession`/`ResolutionEvent` with round + rationale; committed reviews remain immutable (M3), transitions are separate records
- [ ] T6.2 Convergence scoring: `resolved_claims / total_claims` at debate end → `Outcome.convergence_score`; healthy-band telemetry emitted (feeds 0.2 dashboards); verdict kind derived: all resolved ⇒ candidate-verdict else disputed

### WS 6.b — Honesty checks

- [ ] T6.3 Theater detector: debate with zero state changes (no concessions, no new objections, no evidence shifts) → `theater=true` on Outcome + explicit report flag ([07 §7.2](../../design/prd/07-success-metrics.md)); capitulation-cascade signature (≥80% round-1 concessions, zero rebuttals) flagged separately ([FM-2](../../design/prd/13-failure-modes.md))
- [ ] T6.4 Evidence-reference validator: every `evidence_refs[]` must resolve to artifact content blocks; unresolved refs → warning + claim marked `unverified_evidence`; high-severity claim with empty refs rejected at validation ([FM-7](../../design/prd/13-failure-modes.md))

## Acceptance criteria / exit gate

- Golden tests: converge / dispute / theater / capitulation scenarios each produce expected Outcome fields
- Score math property tests (edge cases: zero claims, all conceded, mixed)
- Validator catches planted hallucinated refs in fixtures ([FM-10](../../design/prd/13-failure-modes.md) cross-check)
- Coverage ≥95% on `engine/evidence*`

## Explicitly out of scope

Semantic-similarity convergence ([DD-08](../../design/prd/12-design-decisions.md) — explicitly rejected); rendering reports (M7).
