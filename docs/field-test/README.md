# Field Test — AdversarialDebate

> Field test plans, corpora, and reports, one directory per version.

## v0.2.1

Measurement methodology release: Mistral effect confirmed, pipeline invariants, false-negative measurement. 150 artifacts across 4 domains, 367 debates, $0.57 total cost.

- [`v0.2.1/field-test-plan.md`](v0.2.1/field-test-plan.md) — separating experiment design, pipeline integrity methodology, false-negative measurement
- [`v0.2.1/FIELD_TEST_REPORT.md`](v0.2.1/FIELD_TEST_REPORT.md) — full report with narrative, scorecards, ground truth, flakiness
- [`v0.2.1/findings-learnings.md`](v0.2.1/findings-learnings.md) — detailed findings and learnings

Key v0.2.1 results: Mistral effect confirmed (DeepSeek+GPT 0.246 vs GPT+Mistral 0.536), 87.4% MATCH, 5/5 pipeline seams pass, 0 flaky, 1.7-3.4% missed-issue rate.

## v0.2.0

Mixed-domain field test across 4 domains: PR review (80), incident response (30), change management (20), security incidents (20). 217 debates, $0.42 total cost.

- [`v0.2.0/field-test-plan.md`](v0.2.0/field-test-plan.md) — corpus design, model strategy, success criteria
- [`v0.2.0/FIELD_TEST_REPORT_full_corpus.md`](v0.2.0/FIELD_TEST_REPORT_full_corpus.md) — full report with narrative, scorecards, ground truth, flakiness
- Candidate corpus lists: `v0.2.0/{incident_response,change_management,security_incidents}_corpus_candidates.csv`
- PR reuse list: `v0.2.0/pr_reuse_80.csv`

## v0.1.0

PR-only field test on 70 real PRs across 6 model pairs. 411 debates, $0.53 total cost.

- [`v0.1.0/field-test-plan.md`](v0.1.0/field-test-plan.md) — corpus selection, sweep matrix, pass criteria
- [`v0.1.0/FIELD_TEST_REPORT_full_corpus.md`](v0.1.0/FIELD_TEST_REPORT_full_corpus.md) — full report
- [`v0.1.0/FIELD_TEST_REPORT_small_corpus.md`](v0.1.0/FIELD_TEST_REPORT_small_corpus.md) — small corpus validation
- [`v0.1.0/learnings.md`](v0.1.0/learnings.md) — issues found and fixed during v0.1.0