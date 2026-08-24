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

## 7.6 Measurement methodology

Each metric in §7.2 requires a defined measurement protocol. This section makes the v0.1.0 success bar **falsifiable**.

### How distinct-issue yield is measured

1. Run single-reviewer baseline (one pass, no debate) on the same artifact.
2. Run adversarial debate (two independent passes + debate).
3. A domain-expert rater (you for v0.1.0 code artifacts) compares the outputs.
4. **Distinct issue** = an issue surfaced in the adversarial output that was not present in the single-reviewer baseline AND is judged materially relevant by the rater.
5. Reported as: `X distinct issues / Y artifacts^`.

^For artifacts where the outcome is known (merged-then-reverted PRs, security advisory PRs), the rater also checks: *was the distinct issue actually the cause of the known failure?* This converts distinctness into correctness.

### How theater rate is computed

Count of debates where `convergence_score == total_claims` (no claim ever changed state — no concessions, no new objections across rounds). Report as a percentage. **Any debate flagged as theater is a bug in the prompt/rubric design for that artifact.**

### How flakiness is bounded

Each artifact in the v0.1.0 bar sweep runs ≥5 times with seed-controlled providers. Verdict is considered flaky if >20% of runs produce a different outcome (converged vs disputed) or if the `resolved[]` set varies across runs. Flaky artifacts are reported but excluded from the v0.1.0 pass/fail bar — they are filed as issues.

### Bifurcated metric (cross-domain)

Code and change-management with known outcomes use **binary** measurement (caught the real issue? yes/no). All other domains (contracts, compliance, media) use the **expert-rater triad** (distinctness, actionability, decision-impact) defined in the [field-testing strategy](../../field-test/field-testing-strategy.md#measurement-protocol-all-tiers). The PRD never pretends a contract field test "found a real bug" — it produced a useful disagreement rated actionable by a domain reader.
