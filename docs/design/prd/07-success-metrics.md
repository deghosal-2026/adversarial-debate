# 07 — Success Metrics

> Sub-document of the [Design overview](../README.md). What makes v0.1.0 good enough — and how we'll know debate is real, not theater.

## 7.1 The v0.1.0 bar (binary)

> **One realistic case where reviewer B finds a materially different issue before convergence — or a disagreement report that measurably improves a human call — demonstrated on real PRs from a public repo, with full transcripts.**

If this doesn't happen, nothing else matters. If it does, the project is real.

## 7.2 Debate-quality metrics

| Metric | Definition | Target signal |
|--------|-----------|---------------|
| **Distinct-issue yield** | Materially distinct issues surfaced by the independent pass (issues neither single-reviewer baseline found) | > 0 on a meaningful % of artifacts |
| **Convergence rate** | % of debates ending converged vs disputed | Both bands healthy: ~100% convergence means reviewers aren't independent; ~0% means prompts/rubrics are broken |
| **Theater rate** | Debates with zero state changes (no concessions, no evidence shifts, no new objections) | Minimize — and expose honestly in reports |
| **`would_resolve_if` actionability** | Human rating: could I act on this resolution path? | Rated actionable on most unresolved points |
| **Report usefulness** | Human rating of disagreement reports as decision aids | Beats "forced answer" baseline in side-by-side comparison |

## 7.3 Engineering gates

- ≥95% test coverage target; ruff clean; mypy strict clean
- Hermetic CI: scripted reviewers, zero paid LLM calls
- Isolation invariant covered by dedicated tests (attempting cross-context leakage must fail loudly)
- Field-test report published from real public-repo PRs

## 7.4 Adoption & engagement signals (post-ship)

- Article traction from concrete before/after review examples
- External users running debates on their own repos/issues
- Adapter pull: which non-code vertical the community asks for next (hypothesis: change management)

## 7.5 Anti-metrics (what we refuse to optimize)

- Convergence rate alone (easy agreement is failure wearing a bow tie)
- Token cost per review without quality context (debate costs more *by design*)
- "Issues found" counts without distinctness verification (single-reviewer vendors play that game)
