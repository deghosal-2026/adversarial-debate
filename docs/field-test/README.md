# Field Test — AdversarialDebate

> Field test plans, corpora, and reports, one directory per version. Cross-version strategy lives in [field-testing-strategy.md](field-testing-strategy.md).

## Cross-version strategy

[field-testing-strategy.md](field-testing-strategy.md) — the 4-tier plan for testing across all 27 verticals. Covers measurement protocol (bifurcated: bug-caught vs expert-rated), domain-selection rubric, public data sources, and the `debate-eval` harness design.

## v0.2.0

Mixed-domain field test across 4 domains: PR review (80), incident response (30), change management (20), security incidents (20). 217 debates, $0.42 total cost.

- [`v0.2.0/field-test-plan.md`](v0.2.0/field-test-plan.md) — corpus design, model strategy, success criteria
- [`v0.2.0/FIELD_TEST_REPORT_full_corpus.md`](v0.2.0/FIELD_TEST_REPORT_full_corpus.md) — full report with narrative, scorecards, ground truth, flakiness
- Candidate corpus lists: `v0.2.0/{incident_response,change_management,security_incidents}_corpus_candidates.csv`
- PR reuse list: `v0.2.0/pr_reuse_80.csv`

Key v0.2.0 results: zero theater, 88.7% ground-truth MATCH, 100% sampled verdict stability, `pair3_gpt_mistral` confirmed as primary default.

## v0.1.0

PR-only field test on 70 real PRs across 6 model pairs. 411 debates, $0.53 total cost.

- [`v0.1.0/field-test-plan.md`](v0.1.0/field-test-plan.md) — corpus selection, sweep matrix, pass criteria
- [`v0.1.0/FIELD_TEST_REPORT_full_corpus.md`](v0.1.0/FIELD_TEST_REPORT_full_corpus.md) — full report
- [`v0.1.0/FIELD_TEST_REPORT_small_corpus.md`](v0.1.0/FIELD_TEST_REPORT_small_corpus.md) — small corpus validation
- [`v0.1.0/learnings.md`](v0.1.0/learnings.md) — issues found and fixed during v0.1.0
