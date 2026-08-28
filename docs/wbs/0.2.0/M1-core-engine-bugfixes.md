# M1 — Core Engine Bugfixes

> Goal: fix all debate controller and evidence engine bugs identified in the v0.1.0 postmortem. These are the highest-priority fixes since downstream consumers (synthesis, reports, field tests) depend on correct engine behavior. Part of [index](index.md).

## PRD coupling

- [13-failure-modes](../../design/prd/13-failure-modes.md): FM-2 (capitulation cascade), FM-7 (theater detection)
- [02-architecture §2.7 convergence](../../design/prd/02-architecture.md): convergence scoring, claim lifecycle

## Dependencies

Upstream: none. Downstream: M2, M3, M4, M5, M6, M7, M8.

## Workstreams & tasks

### WS 1.a — Debate controller fixes

- [ ] T1.1 (#58) `validate_point_by_point`: scope keyword check per-objection instead of global — each objection gets its own verdict from the response region that mentions it
- [ ] T1.2 (#59) `_outstanding_for_side`: filter objections by round number — already-addressed objections must not be re-presented in later rounds
- [ ] T1.3 (#65) `_run_side_turn`: stop updating both `_claims_a` and `_claims_b` unnecessarily — only update the responding side's claim list
- [ ] T1.4 (#66) `TokenBudget.exhausted`: make it a computed property instead of a dead field that is never updated
- [ ] T1.5 (#71) `_build_resolved`: add warning when claim snapshot is missing instead of silent fallback to `"(unknown claim)"`

### WS 1.b — Evidence engine fixes

- [ ] T1.6 (#60) `_detect_theater`: fix dead-code fallthrough branch that is structurally unreachable — make the second branch actually reachable
- [ ] T1.7 (#61) `_detect_capitulation_cascade`: use objections count as denominator instead of claims count — fix the 80% threshold baseline
- [ ] T1.8 (#87) `validate_evidence`: stop stripping `./` and `/` from block IDs before lookup — preserve exact block IDs
- [ ] T1.9 (#88) Evidence snapshots: use last transition instead of first transition for `final_status`
- [ ] T1.10 (#89) `UnresolvedPoint`: enforce non-empty individual claim IDs inside `claim_ids` list
- [ ] T1.11 (#90) Synthesis: wire `_find_degraded_rounds` to actually read debate events instead of returning `[]` always
- [ ] T1.12 (#91) Synthesis input validation: compare unique claim IDs instead of raw list lengths

### WS 1.c — Claim parsing fix

- [ ] T1.13 (#62) `parse_claims_from_review`: add prose-style fallback and negation-aware severity detection

### WS 1.d — Dead code and cleanup

- [ ] T1.14 (#67) `_find_degraded_rounds`: implement the actual scan of debate events for `degraded=True` flags

## Documents, plans & tests to update

- `src/adversarial_debate/engine/debate_controller.py` — `validate_point_by_point`, `_outstanding_for_side`, `_run_side_turn`, `TokenBudget`
- `src/adversarial_debate/engine/evidence.py` — `_detect_theater`, `_detect_capitulation_cascade`, `validate_evidence`, `_build_snapshots`
- `src/adversarial_debate/engine/synthesis.py` — `_build_resolved`, `_find_degraded_rounds`, `validate_synthesis_inputs`
- `src/adversarial_debate/schemas/debate.py` — `UnresolvedPoint.claim_ids` constraint
- `scripts/04_run_debate.py` — `parse_claims_from_review`
- `tests/test_evidence.py` — add tests for theater, capitulation, evidence validation, snapshot ordering
- `tests/test_debate_controller.py` — add tests for keyword scoping, round filtering, side-turn optimization
- `tests/test_synthesis.py` — add tests for degraded rounds, input validation, missing snapshots
- `tests/test_schemas.py` — add test for `UnresolvedPoint` empty-string rejection

## Acceptance criteria / exit gate

- All 14 issues closed with passing tests
- Ruff clean, mypy strict clean, full test suite green
- Code review completed on all changes
- Committed and pushed to `rel-0.2.0`

## Explicitly out of scope

Transport layer fixes (M2), CLI fixes (M3), test corrections (M4), field test data (M5), documentation (M6).