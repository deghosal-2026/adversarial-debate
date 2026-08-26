# M5 — Debate Controller

> Goal: bounded, structured rebuttal rounds where every outstanding objection must be addressed — conceded, rebutted, or explicitly carried. Round caps, message caps, and degradation detection keep debates honest and affordable. Part of [index](index.md).

## PRD coupling

- [05-features](../../design/prd/05-features.md): F4 (bounded rounds, default 2; mandatory point-by-point)
- [12-design-decisions DD-01/DD-02](../../design/prd/12-design-decisions.md): 2-round default (research: gains saturate); **no forced personas** — reviewers argue their own committed views
- [02-architecture §2.2 Debate Controller](../../design/prd/02-architecture.md): bounded rebuttal rounds; tracks round state
- [13-failure-modes FM-9](../../design/prd/13-failure-modes.md): degradation detection (truncation/refusal → mark round degraded)

## Dependencies

Upstream: M2 (providers), M3 (sessions/gate). Downstream: M6 consumes debate events.

## Workstreams & tasks

### WS 5.a — Orchestration

- [x] T5.1 (#23) DebateController: post-revelation round orchestration; per round builds each reviewer's prompt from (own committed review + other side's claims/objections + outstanding objections to them); termination states: `rounds_exhausted`, `all_resolved`, `budget_exhausted`, `error`
- [x] T5.2 (#24) Point-by-point enforcement: validator requires each reviewer response to reference every outstanding objection targeted at them with verdict `conceded | rebutted(with argument) | carried(explicit) ; unaddressed objection → validation failure + one repair retry → else round marked error`

### WS 5.b — Caps & health

- [x] T5.3 (#25) Caps: max claims per review (default 20), max messages per round, per-artifact token budget hook (enforced with M8; interface here); excess claims dropped with warning event ([FM-6 asymmetric effort guardrail](../../design/prd/13-failure-modes.md))
- [x] T5.4 (#26) Degradation detector ([FM-9](../../design/prd/13-failure-modes.md)): repetition/truncation/refusal heuristics on reviewer messages → mark message+round `degraded`; degraded rounds surface in report header; option to resume with different model

## Acceptance criteria / exit gate

- Scripted end-to-end debate (ScriptedReviewer scenarios from M2): happy path converge; hold-and-dispute path; capitulation path ([FM-2 signature detectable in M6 via events emitted here])
- Unaddressed-objection repair-retry-error ladder covered by tests
- No forced-persona phrasing anywhere in prompts (grep test over prompt templates — [DD-02](../../design/prd/12-design-decisions.md))
- Coverage ≥95% on `engine/debate*`

## Explicitly out of scope

Claim state transitions (M6 records what controller reports); persistence of rounds (M8).
