# PRD — AdversarialDebate v0.1.0

> Sub-documents of the [Design overview](../README.md). Customer-focused product requirements: why the market needs independent adversarial review, who buys it across twenty-seven industry domains, what ships, why the business case closes, and how we prove it works.

| # | Document | Covers | Status |
|---|----------|--------|--------|
| 01 | [01-why.md](01-why.md) | Market context, the primed-agreement pain, why now | ✅ authored |
| 02 | [02-architecture.md](02-architecture.md) | The loop, components, data model, **convergence detection**, **context-window strategy**, provider layer | ✅ authored + revised |
| 03 | [03-landscape.md](03-landscape.md) | AI review vendors vs MAD research vs judges; the open position | ✅ authored |
| 04 | [04-users-and-cujs.md](04-users-and-cujs.md) | **27 industry domains**, 8 core user journeys, BYOM-per-cluster fit | ✅ authored |
| 05 | [05-features.md](05-features.md) | Must-have / nice-to-have / **adapter protocol** / **mid-debate injection** / **API surface sketch** / exclusions | ✅ authored + revised |
| 06 | [06-security-baseline.md](06-security-baseline.md) | Isolation, data handling, threat model, **reproducibility & flakiness**, **operational failure modes**, **telemetry stance**, **data-classification** | ✅ authored + revised |
| 07 | [07-success-metrics.md](07-success-metrics.md) | The binary v0.1.0 bar; debate-quality + anti-metrics; **measurement methodology** | ✅ authored + revised |
| 08 | [08-risks.md](08-risks.md) | Theater, shared blind spots, cost blowout, research counter-evidence, **strategic risk**, **kill criterion**, **skeptic pre-emption** | ✅ authored + revised |
| 09 | [09-roadmap.md](09-roadmap.md) | v0.1.0 → v0.4.0 sequencing; **per-version kill criteria** | ✅ authored + revised |
| 10 | [10-business-case.md](10-business-case.md) | Economic argument, buyer personas, BYOM, GTM, **human baseline**, **OSS sustainability**, **time-to-first-value** | ✅ authored + revised |
| 11 | [11-glossary.md](11-glossary.md) | 22 terms defined once — contributor onboarding reference | ✅ authored |
| 12 | [12-design-decisions.md](12-design-decisions.md) | 8 decision records — *why* 2 rounds, no personas, SQLite, MIT, no tools, dissent first-class, claim-state convergence | ✅ authored |
| 13 | [13-failure-modes.md](13-failure-modes.md) | 10 debate-quality failure modes with signatures, detection, mitigation | ✅ authored |
| 14 | [14-schema-migration.md](14-schema-migration.md) | Transcript continuity across versions; forward-only migrations; export stability | ✅ authored |
| 15 | [15-performance.md](15-performance.md) | Latency targets, cost ceilings, throughput; what we do NOT promise | ✅ authored |
| 16 | [16-contributor-journey.md](16-contributor-journey.md) | 4 contribution types (adapter/engine/fixtures/docs); review criteria; recognition | ✅ authored |
| 17 | [17-security-disclosure.md](17-security-disclosure.md) | Vulnerability reporting, severity rubric, coordinated disclosure timeline | ✅ authored |
| 18 | [18-article-plan.md](18-article-plan.md) | ≥2 launch articles + 8-part series arc; content principles | ✅ authored |
| 19 | [19-competitor-benchmark.md](19-competitor-benchmark.md) | Exact protocol for AdversarialDebate vs single-reviewer on same artifacts | ✅ authored |

**Related:** [Field-testing strategy](../../field-test/field-testing-strategy.md) — 4-tier plan for testing across all 27 verticals.

**Reading order:**
- **Newcomers:** 01 → 04 → 10 → 05
- **Contributors:** 11 → 16 → 12 → 05
- **Buyers:** 10 → 08 → 19 → 07
- **Maintainers:** 12 → 13 → 14 → 17
