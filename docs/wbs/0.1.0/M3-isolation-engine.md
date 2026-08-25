# M3 — Isolation Engine

> Goal: the non-negotiable invariant, enforced mechanically. Two reviewer sessions with separate contexts; conclusions revealed only after both commit; committed reviews immutable. Plus the adversarial test suite that tries to break it. Part of [index](index.md).

## PRD coupling

- [02-architecture §2.3](../../design/prd/02-architecture.md): **the one non-negotiable invariant** — "Reviewer B cannot see reviewer A's output until B has fully committed its own review — and vice versa"
- [05-features](../../design/prd/05-features.md): F1 (independent dual-review pass), F2 (delayed revelation `isolated → revealed`)
- [06-security §6.1 guarantees](../../design/prd/06-security-baseline.md): reviewer independence + commit immutability
- [07-success §7.3 gates](../../design/prd/07-success-metrics.md): "attempting cross-context leakage must fail loudly"

## Dependencies

Upstream: M1 (schemas). Downstream: M5 (controller orchestrates sessions through the gate).

## Workstreams & tasks

### WS 3.a — Sessions & gate

- [x] T3.1 (#14) ReviewerSessionManager: creates exactly two sessions per artifact with independent conversation contexts; status lifecycle `isolated→revealed→debating→done|error`; no shared memory objects between sides
- [x] T3.2 (#15) RevelationGate: explicit state machine; `reveal()` only callable when both sessions hold committed reviews; every transition emits an audit event (actor=engine, from, to, timestamp)
- [x] T3.3 (#16) Commit immutability: committed `Review` is frozen (Pydantic frozen model); post-commit mutation attempts raise; concessions/objections are *new events*, never edits ([06 §6.1](../../design/prd/06-security-baseline.md))

### WS 3.b — Prove it can't leak

- [x] T3.4 (#17) Isolation adversarial test suite: (a) reveal-before-commit raises; (b) session A prompt-history never contains B content and vice versa (inspect full request logs); (c) shared-cache/framework-memory probes (same registry instance reused) find zero cross-references; (d) ScriptedReviewer scenario asserting a "peeking" reviewer pattern is impossible by construction; all failures loud, named `IsolationViolation`

## Acceptance criteria / exit gate

- Every test in T3.4 (#17) green; any future regression fails CI by design
- Audit log shows full transition lineage for a sample debate (isolated→revealed→debating→done)
- Frozen-review mutation attempt test proves immutability at type level
- Coverage ≥95% on `engine/isolation*`

## Explicitly out of scope

Debate round logic (M5); transcript persistence (M8). This milestone owns the invariant only.
