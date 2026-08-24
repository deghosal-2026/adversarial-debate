# 21 — Eval Harness Spec (`debate-eval`)

> Sub-document of the [Design overview](../README.md). Design for the separate `debate-eval` package that standardizes cross-domain field testing. Domain experts contribute fixtures + rubrics without touching engine code.

## 21.1 Why a separate package

The engine runs debates. The harness *measures* them. Mixing the two couples measurement to implementation — every engine change risks breaking eval compatibility. `debate-eval` is a standalone package that imports the engine as a dependency and produces standardized reports.

## 21.2 Architecture

```
debate-eval/
├── debate_eval/
│   ├── runner.py          # orchestrates: load fixture → run engine → collect result → rate
│   ├── raters/
│   │   ├── ground_truth.py  # binary: did debate catch the known issue?
│   │   ├── expert.py        # triad: distinctness, actionability, decision-impact
│   │   └── flakiness.py     # N-run sweep: verdict stability %
│   ├── sweeps/
│   │   ├── diversity.py     # homogeneous vs heterogeneous pair on same artifacts
│   │   ├── baseline.py      # single-reviewer vs adversarial comparison
│   │   └── theater.py       # zero-state-change detection across corpus
│   ├── fixtures/            # seeded artifacts with known issues (per domain)
│   │   ├── pr_review/
│   │   ├── itsm/
│   │   └── ...
│   └── report.py           # standardized cross-domain report generator
├── pyproject.toml
└── README.md
```

## 21.3 Fixture format

```json
{
  "domain": "pr_review",
  "artifact_path": "fixtures/pr_review/pr-482-revert.diff",
  "ground_truth": {
    "known_issues": [
      {
        "description": "Missing lock-timeout on 40GB table migration",
        "severity": "high",
        "evidence": "orders table row count in schema dump"
      }
    ],
    "outcome": "merged-then-reverted",
    "revert_reason": "timeout in production at 2AM"
  },
  "expected": {
    "should_disagree": true,
    "should_surface": "lock-timeout risk",
    "min_distinct_issues": 1
  },
  "rater": "ground_truth",
  "notes": "Real PR from public repo; PII redacted"
}
```

## 21.4 Rating protocols

### Ground-truth rater (Tier 0, 2)

```
Input:  debate result + known_issues[]
Output: {
  "issues_caught": [...],        # which known issues appeared in the debate
  "issues_missed": [...],        # which known issues neither reviewer found
  "distinct_issues": [...],      # issues surfaced that weren't in known_issues (bonus finds)
  "false_positives": [...],      # issues raised that are actually fine
  "verdict_correct": bool        # did the verdict align with the known outcome?
}
```

### Expert-rater triad (Tier 1, 3)

```
Input:  debate result (no ground truth)
Output: {
  "distinctness": 1-5,           # is this issue materially different from single-pass?
  "actionability": 1-5,          # could I act on would_resolve_if?
  "decision_impact": bool,       # would this have changed my call?
  "rater_notes": "..."
}
```

### Flakiness sweep

```
Input:  artifact + N (default 5)
Output: {
  "runs": [...],                 # verdict per run
  "stability_rate": float,       # % of runs with same verdict
  "flaky": bool,                 # stability_rate < 0.80
  "flaky_points": [...]          # which unresolved points flip across runs
}
```

## 21.5 Standardized report

```yaml
domain: pr_review
fixtures_evaluated: 30
rating_protocol: ground_truth

aggregate:
  issues_caught: 24/30          # 80% of known issues surfaced
  distinct_issues_total: 18     # issues found beyond known set
  false_positive_rate: 12%      # issues raised that were fine
  verdict_accuracy: 87%         # verdict aligned with known outcome
  theater_rate: 8%              # debates with zero state changes
  median_latency: 94s
  median_cost: $0.08

flakiness_subsample:
  artifacts_tested: 6
  stability_rate: 0.83
  flaky_artifacts: 1            # pr-482: verdict flips on lock-timeout point

diversity_sweep:
  homogeneous_distinct: 8
  heterogeneous_distinct: 18
  delta: +125%                  # heterogeneous pairs found 125% more distinct issues
```

## 21.6 EvalForge integration

Each fixture + result pair exports as an EvalForge-compatible scenario:

```json
{
  "scenario_id": "pr-review-482",
  "input": "pr-482-revert.diff",
  "expected": "dispute on lock-timeout",
  "engine_version": "0.1.0",
  "result": "disputed — would_resolve_if: load test at production row count",
  "pass": true
}
```

This makes debate quality measurable over time — every engine change re-runs the eval suite and tracks regressions.

## 21.7 Contribution model

Domain experts contribute without writing Python:

```
1. Create fixtures/<your_domain>/
2. Add 3-5 artifacts (redacted, public, or fictional)
3. Add fixtures.json with known_issues and expected behavior
4. (Optional) Add a rubric.json with domain-specific claim categories
5. PR: "eval fixtures: <domain>"
```

The harness auto-discovers fixtures by directory. No code registration required.
