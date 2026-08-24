# M10 — Field Test (Tier 0)

> Goal: run the engine against real PRs from a public repo — merged-then-reverted, security-advisory, and clean merges — with flakiness sweeps and a single-reviewer baseline, then publish the honest report against the exit bar. This milestone *is* the v0.1.0 proof. Part of [index](index.md).

## PRD coupling

- [07-success §7.1 binary bar + §7.6 methodology](../../design/prd/07-success-metrics.md): the falsifiable v0.1.0 bar and exactly how it's measured
- [field-testing-strategy Tier 0](../../field-test/field-testing-strategy.md): corpus (reverted/advisory PRs), sweep design, baseline comparison, report shape
- [19-competitor-benchmark §19.2 steps 1-4](../../design/prd/19-competitor-benchmark.md): corpus published before runs; single-reviewer baseline on same models; blind distinctness rating
- [10-business-case §10.7 credibility](../../design/prd/10-business-case.md): one inspectable case study

## Dependencies

Upstream: M9 (CLI drives everything). Downstream: M11 publishes results; articles feed off transcripts.

## Workstreams & tasks

### WS 10.a — Corpus & harness

- [ ] T10.1 (#46) Corpus selection: 20-30 public-repo PRs stratified by size (S/M/L) × outcome (merged-clean / merged-then-reverted / security-advisory); **corpus list published in repo before any runs**; each entry: URL, outcome, revert/advisory reason, expected-debate flag
- [ ] T10.2 (#47) Flakiness sweep runner: N=5 seed-controlled runs per artifact; stability rate per artifact; flags verdict flips >20%; output feeds report stability table ([06 §6.4](../../design/prd/06-security-baseline.md))
- [ ] T10.3 (#48) Single-reviewer baseline runner: same model(s), one pass, no debate; captures issues/cost/latency; anonymized as "Tool X" for rating ([19 §19.2](../../design/prd/19-competitor-benchmark.md))

### WS 10.b — Execution & reporting

- [ ] T10.4 (#49) Full sweep execution: adversarial run on all corpus artifacts (heterogeneous pair primary; homogeneous subsample for diversity delta); collect transcripts, latency, cost; resume/budget exercised naturally on failures
- [ ] T10.5 (#50) FIELD_TEST_REPORT.md: per-PR results vs exit bar — distinct-issue yield (vs baseline, blind-rated), theater rate, convergence/disputed bands, actionability of would_resolve_if (self-rater for Tier 0 with rubric from [21-eval-harness](../../design/prd/21-eval-harness.md)), flakiness table, honest misses section ("both reviewers missed X"); explicit PASS/FAIL vs [§7.1](../../design/prd/07-success-metrics.md) bar

## Acceptance criteria / exit gate

- Corpus committed before sweep timestamps (verifiable via git history)
- ≥1 artifact meets the exit bar OR the report says FAIL with root-cause analysis ([09-roadmap kill criterion](../../design/prd/09-roadmap.md) — do not ship on FAIL)
- Every claim in the report traceable to a transcript file path
- Sweep artifacts stored under `docs/field-test/v0.1.0/` following house layout

## Explicitly out of scope

Non-code domains (Tier 1 is v0.2); CodeRabbit-style third-party tool comparison (protocol ready, execution post-launch).
