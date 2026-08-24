# PRD — AdversarialDebate v0.1.0 → v1.0.0

> Sub-documents of the [Design overview](../README.md). 26 documents covering everything from market context to 1.0.0 graduation. Customer-focused, contributor-friendly, maintainer-grade.

## Core PRD (01-10)

| # | Document | Covers |
|---|----------|--------|
| 01 | [01-why.md](01-why.md) | Market context, primed-agreement pain, why now |
| 02 | [02-architecture.md](02-architecture.md) | Loop, components, data model, convergence detection, context-window strategy |
| 03 | [03-landscape.md](03-landscape.md) | Vendors vs MAD research vs judges; the open position |
| 04 | [04-users-and-cujs.md](04-users-and-cujs.md) | 27 industry domains, 8 CUJs, BYOM-per-cluster fit |
| 05 | [05-features.md](05-features.md) | **Lean MVP** (F1-F10 only), deferred list, adapter protocol, API surface |
| 06 | [06-security-baseline.md](06-security-baseline.md) | Isolation, data handling, threat model, reproducibility, ops failures, telemetry, data-classification |
| 07 | [07-success-metrics.md](07-success-metrics.md) | Binary v0.1.0 bar, debate-quality metrics, measurement methodology |
| 08 | [08-risks.md](08-risks.md) | Theater, blind spots, cost, research counter-evidence, strategic risks, kill criteria, skeptic pre-emption |
| 09 | [09-roadmap.md](09-roadmap.md) | **v0.1.0 → v1.0.0** (10 versions), per-version kill criteria |
| 10 | [10-business-case.md](10-business-case.md) | Economics, personas, BYOM unlock, GTM, human baseline, OSS sustainability, time-to-first-value |

## Reference (11-12)

| # | Document | Covers |
|---|----------|--------|
| 11 | [11-glossary.md](11-glossary.md) | 22 terms defined once — contributor onboarding reference |
| 12 | [12-design-decisions.md](12-design-decisions.md) | 8 decision records — why 2 rounds, no personas, SQLite, MIT, no tools, dissent first-class |

## Quality & Operations (13-17)

| # | Document | Covers |
|---|----------|--------|
| 13 | [13-failure-modes.md](13-failure-modes.md) | 10 debate-quality failure modes with signatures, detection, mitigation |
| 14 | [14-schema-migration.md](14-schema-migration.md) | Transcript continuity across versions; forward-only migrations |
| 15 | [15-performance.md](15-performance.md) | Latency targets, cost ceilings, throughput; what we do NOT promise |
| 16 | [16-contributor-journey.md](16-contributor-journey.md) | 4 contribution types, step-by-step paths, review criteria, recognition |
| 17 | [17-security-disclosure.md](17-security-disclosure.md) | Vulnerability reporting, severity rubric, coordinated disclosure timeline |

## Content & Benchmarking (18-19)

| # | Document | Covers |
|---|----------|--------|
| 18 | [18-article-plan.md](18-article-plan.md) | 2 launch articles + 8-part series arc; content principles |
| 19 | [19-competitor-benchmark.md](19-competitor-benchmark.md) | Exact protocol for AdversarialDebate vs single-reviewer comparison |

## Deep Dives (20-26)

| # | Document | Covers |
|---|----------|--------|
| 20 | [20-threat-model.md](20-threat-model.md) | Attack trees: injection, tampering, exhaustion; residual risk |
| 21 | [21-eval-harness.md](21-eval-harness.md) | `debate-eval` package spec: fixture format, rating protocols, EvalForge integration |
| 22 | [22-internationalization.md](22-internationalization.md) | 3-layer i18n: artifact language, report localization, UI localization; cultural calibration |
| 23 | [23-enterprise-deployment.md](23-enterprise-deployment.md) | 4 topologies: local, CI, VPC, air-gapped; vLLM/Ollama/Azure config; auth & HA |
| 24 | [24-fleet-integrations.md](24-fleet-integrations.md) | API contracts: ToolTrust, EvalForge, PlannerCritic, AgentJury |
| 25 | [25-data-retention.md](25-data-retention.md) | Lifecycle, GDPR/CCPA alignment, deletion mechanics, partner data boundary |
| 26 | [26-brand-guide.md](26-brand-guide.md) | Names, voice, terminology consistency, article rules, visual identity |

**Related:** [Field-testing strategy](../../field-test/field-testing-strategy.md) — 4-tier plan for testing across all 27 verticals.

**Reading order:**
- **Newcomers:** 01 → 04 → 10 → 05
- **Contributors:** 11 → 16 → 12 → 05
- **Buyers:** 10 → 08 → 19 → 07
- **Maintainers:** 12 → 13 → 14 → 17 → 20
- **Security reviewers:** 06 → 20 → 17 → 25
