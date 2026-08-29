<div align="center">

# AdversarialDebate

[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-v0.2.2-brightgreen)]()
[![PyPI](https://img.shields.io/pypi/v/adversarial-debate)](https://pypi.org/project/adversarial-debate/)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/14254/badge)](https://www.bestpractices.dev/en/projects/14254/passing)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000)](https://github.com/astral-sh/ruff)

**A multi-agent adversarial review engine. Two independent LLMs analyze the same artifact without seeing each other's answers, debate their conclusions point by point, and produce either a converged decision — or a structured disagreement report that preserves the dissent.**

</div>

> [!NOTE]
> **Status:** v0.2.2 shipped Aug 2026. Measurement infrastructure release adding statistical rigor to every published metric.
> **Key finding:** LLM judge validated (87.4% match rate, 77.8 sigma above vocabulary floor). Convergence noise floor measured at ±0.020.
> **Core improvement:** Every published metric now has a known confidence interval. Causal mechanism for Mistral effect formally documented.
> The core isolation rule is mechanically enforced: **reviewer B cannot see reviewer A's answer until it has fully committed its own.**

---

## Why

Most AI "second opinions" are fake. The usual pattern is one model proposes an answer and a second model is asked to double-check — *after* being shown the first model's framing, assumptions, and conclusion. That setup almost guarantees convergence, even when convergence should not happen. It looks careful. It is actually agreement with extra steps.

The most expensive agent failures are rarely about missing information. They are about prematurely accepted reasoning: a pull request that feels "probably safe," an architecture change that seems "good enough," an incident hypothesis that sounds plausible in the first ten minutes. These are exactly the decisions where human teams rely on *independent* review and constructive conflict.

AdversarialDebate productizes that discipline for LLM systems:

- **Independent passes** — agents analyze the same input in strict isolation.
- **Delayed revelation** — conclusions are revealed only after both sides commit.
- **Structured challenge** — each agent must respond point by point: assumptions, evidence quality, edge cases, risk exposure.
- **Dissent preservation** — if disagreement survives the debate, the system ships a structured disagreement report instead of pretending consensus exists.

The outcome is not always consensus. Sometimes the most valuable result is a sharply defined disagreement showing exactly where uncertainty lives.

## Quickstart

```bash
pip install adversarial-debate

# Scaffold config
advdeb init

# Edit in your API keys
# $EDITOR advdeb.toml

# Review a PR
advdeb review --pr https://github.com/kubernetes/kubernetes/pull/140860 --domain pr_review

# View the report
advdeb report <run_id>

# Export the transcript
advdeb transcript <run_id> --export jsonl
```

See [docs/reference/quickstart.md](docs/reference/quickstart.md) for the full walkthrough.

## What It Is

### The Independent Pass → Debate → Decide Loop

```
                    ┌────────────────────────────┐
        input ────► │  Input Normalizer          │  PR diff / ADR / incident / plan
                    └──────────┬─────────────────┘
                               │  same artifact, isolated contexts
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
           ┌──────────┐                ┌──────────┐
           │ Agent A  │   no peeking   │ Agent B  │
           └────┬─────┘                └────┬─────┘
                │ commit review             │ commit review
                └────────────┬──────────────┘
                             ▼  revelation gate opens
                    ┌─────────────────┐
                    │ Debate Controller│  bounded rounds, point-by-point
                    └────────┬─────────┘
                             ▼
              converged? ─── yes ──► Joint Verdict (strongest surviving arguments)
                  │
                  no
                  ▼
       Disagreement Report (unresolved points + what would resolve them)
```

### Key Properties

| Property | Description |
|----------|-------------|
| **Independence before interaction** | Reviewers never see each other's output before committing |
| **Disagreement is a feature** | Forced synthetic consensus hides exactly what you need to see |
| **Evidence over rhetoric** | Confidence tied to cited evidence and failure modes, not tone |
| **Auditability** | Full transcript lineage: every claim, objection, concession, verdict |

## Architecture (v0.2.2)

| Component | Responsibility |
|-----------|----------------|
| **Input Normalizer** | Converts PRs, docs, incidents, plans into a common review schema |
| **Independent Reviewer Engine** | Isolated review passes with strict context separation |
| **Debate Controller** | Bounded rebuttal rounds; tracks argument state |
| **Evidence Tracker** | Claims, supporting evidence, unresolved points, concessions |
| **Synthesis Layer** | Joint decision or structured disagreement report |
| **Audit Log** | Persists full review lineage (SQLite) |

**Current stack:** Python · Pydantic schemas · SQLite · PydanticAI / LangGraph / raw-API adapters · CLI and field-test scripts.

**Planned additions:** FastAPI service · React side-by-side review UI · broader adapter coverage.

## Example Output

```yaml
verdict: DISPUTED            # 6 of 9 points converged
resolved:
  - claim: "Rate-limit bump is safe under current traffic"
    status: agreed_by_both
unresolved:
  - claim: "Expand/contract migration is safe for pr-482"
    agent_a: sufficient as written
    agent_b: needs lock-timeout analysis on orders table (~40GB)
    would_resolve_if: load test at production row count
audit: transcripts/2026-08-pr482.jsonl
```

## Use Cases

- Code review — two reviewers, one risky diff, zero shared bias
- Architecture tradeoff evaluation under uncertainty
- Change risk assessment before rollout
- Incident hypothesis review — competing root causes, argued out
- Migration plan audit

## Roadmap

| Version | Scope |
|---------|-------|
| v0.1.0 | Independent dual-review pass, bounded debate, claims/objections/concessions schema, consensus + disagreement reports, PR-review domain adapter, transcripts, field test on real public-repo PRs |
| v0.2.0 | Corrected field-test pipeline, mixed-domain corpus (PR review, incident response, change management, security incidents), subset-based model validation, stronger report integrity |
| **v0.2.1** | Mistral effect confirmed, pipeline integrity invariants at 5 seams, false-negative measurement (1.7–3.4% miss rate), 55 new tests |
| **v0.2.2** | Noise-floor baseline (CIs for all metrics), permutation control (77.8 sigma above null), shared RLHF priors documented |
| v0.3.0 | N-agent mode, side-by-side debate visualization, diversity/convergence-quality metrics |
| v0.4.0 | Eval benchmark scenarios, approval-workflow integration, learning from past unresolved disagreements |

## Field Test Reports & Release Docs

### v0.2.2 (current)
- [Full Field Test Report](docs/field-test/v0.2.2/FIELD_TEST_REPORT.md) — noise-floor CIs, permutation control, shared RLHF priors
- [Release Notes](docs/reference/release-notes-v0.2.2.md) — what changed, model selection guidance, upgrade notes
- [Field Test Plan](docs/field-test/v0.2.2/field-test-plan.md) — experimental methodology
- [Learnings](docs/field-test/v0.2.2/learnings.md) — findings and causal mechanism documentation

### v0.2.1
- [Full Corpus Report](docs/field-test/v0.2.1/FIELD_TEST_REPORT.md) — Mistral effect confirmed, 367 debates, pipeline integrity, false-negative measurement
- [Release Notes](docs/reference/release-notes-v0.2.1.md)
- [Field Test Plan](docs/field-test/v0.2.1/field-test-plan.md)
- [Findings & Learnings](docs/field-test/v0.2.1/findings-learnings.md)

### v0.2.0
- [Full Corpus Report](docs/field-test/v0.2.0/FIELD_TEST_REPORT_full_corpus.md) — 150 artifacts, 4 domains, 217 debates
- [Field Test Plan](docs/field-test/v0.2.0/field-test-plan.md)

### v0.1.0
- [Full Corpus Report](docs/field-test/v0.1.0/FIELD_TEST_REPORT_full_corpus.md) — 70 PRs, 6 pairs, 411 debates
- [Field Test Plan](docs/field-test/v0.1.0/field-test-plan.md)

[CHANGELOG](CHANGELOG.md) — full version history

### v0.2.2 Key Results

| Metric | Value | vs v0.2.1 |
|--------|-------|-----------|
| New LLM calls | **0** | 480 debates |
| Noise-floor CIs | **5 pairs measured** | None |
| Permutation control z-score | **77.8 sigma** | Not measured |
| Shared RLHF priors | **Documented** | Implicit |
| New unit tests | **+21** (all deterministic) | +55 |
| Total cost | **$0.00** | $0.57 |

### v0.2.2 Artifacts

- Noise-floor report: `results/field-test/v0.2.2/noise-floor-report.json`
- Permutation control: `results/field-test/v0.2.2/permutation-control-report.json`
- Field test scripts: `scripts/README.md` (see steps 8-9)

## Non-Goals

- Replacing human reviewers for irreversible high-risk decisions
- Forcing consensus when disagreement is more informative
- Optimizing speed over reasoning quality
- Being a generic chat wrapper around multiple models

## Honest Limitation

Debate does not guarantee truth. Two strong debaters can still miss the same blind spot, and poorly designed personas can turn useful disagreement into performance theater. The design answer: measure whether debate *changed* anything, and preserve dissent rather than flattening it.

## License

[MIT](LICENSE) © 2026 Debashish Ghosal
