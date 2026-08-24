# Field Test — AdversarialDebate

> Field test plans, corpora, and reports, one directory per version. Cross-version strategy lives in [field-testing-strategy.md](field-testing-strategy.md).

## Cross-version strategy

[field-testing-strategy.md](field-testing-strategy.md) — the 4-tier plan for testing across all 27 verticals when v0.1.0 ships only one adapter. Covers measurement protocol (bifurcated: bug-caught vs expert-rated), domain-selection rubric, public data sources, and the `debate-eval` harness design.

## v0.1.0 Goal

Run the engine against **real PRs from a public GitHub repo**. Success bar (from the project charter): at least one case where reviewer B surfaces a materially different issue before convergence — or a disagreement report that measurably improves a human decision.

## Planned Documents

- `v0.1.0/field-test-plan.md` — corpus selection, sweep matrix, pass criteria
- `v0.1.0/field-test-results-0.1.0.md` — per-PR traces, debate transcripts, findings
