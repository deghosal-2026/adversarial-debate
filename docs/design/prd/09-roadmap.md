# 09 — Roadmap

> Sub-document of the [Design overview](../README.md). From v0.1.0 beachhead to the vertical engine.

## 9.1 v0.1.0 — Prove the loop (Week 6, Aug 25-31, 2026)

Independent dual-review pass with delayed revelation · structured claims/objections/concessions schema · bounded debate rounds · converged verdict + disagreement report outputs · PR-review domain adapter · BYOM provider registry · SQLite transcripts · CLI + basic UI · field test on real public-repo PRs · ship to PyPI/GitHub (public) + ≥2 dev.to articles.

**Exit bar:** one inspectable case where independent review surfaced what a single reviewer missed — or a disagreement report that improved a human call.

## 9.2 v0.2.0 — Broaden judgment

- **Second domain adapter: change management / ITSM** (community-pull hypothesis; CAB pre-processing story)
- Stronger disagreement taxonomy (disagreement *types*: interpretation vs evidence vs values)
- Argument-importance scoring — rank unresolved points by decision impact
- Debate-usefulness scoring shipped as first-class metric
- Selective-debate triggers (iMAD-style: debate where it changes outcomes)
- Redaction hooks + retention policies

## 9.3 v0.3.0 — Scale and see

- N-agent extension mode (bridges toward AgentJury companion project)
- Side-by-side debate visualization in full UI
- Quality metrics dashboard: diversity, convergence quality, theater rate over time
- Additional adapters by community pull (contracts, incident hypotheses, procurement)

## 9.4 v0.4.0 — Integrate with the fleet

- EvalForge integration: debate benchmark scenarios as reusable eval packs
- ToolTrust integration: debate verdicts as advisory layer before risky tool execution
- Historical learning: past unresolved disagreements → recurring-pattern surfacing (feeds LessonExtractor)
- Braintrust-compatible export for enterprise eval pipelines

## 9.5 Long-term direction (non-committed)

- Vertical partnerships for regulated clusters (healthcare, gov) under strict human-in-the-loop framing
- Debate-as-evidence standards: transcript format as an interop spec other review tools can adopt
- Hosted UI/dashboard only if OSS pull demands it

## 9.6 Sequencing principle

Every version must end with **a shipped, inspectable artifact** — never a benchmark-only release. Adapter breadth follows proof; proof follows field tests; field tests follow real artifacts.
