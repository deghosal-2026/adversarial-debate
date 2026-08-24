# 09 — Roadmap (v0.1.0 → v1.0.0)

> Sub-document of the [Design overview](../README.md). From lean MVP beachhead to stable 1.0.0. Every version ends with a shipped, inspectable artifact — never a benchmark-only release.

## 9.1 v0.1.0 — Prove the loop (Week 6, Aug 25-31, 2026)

**MVP goal:** prove that two isolated reviewers produce materially different conclusions than a single reviewer, on real code, with full transcripts. Nothing else.

| Ships | What |
|-------|------|
| F1-F4 | Independent dual-review pass, delayed revelation, structured debate schema, bounded rounds |
| F5-F6 | Converged verdict + disagreement report outputs |
| F7 | PR-review domain adapter (the only adapter) |
| F8 | BYOM provider registry (config-driven, OpenAI-compatible) |
| F9 | SQLite transcript storage + JSONL export |
| F10 | CLI: `advdeb init`, `advdeb review --pr`, `advdeb report` |

**Explicitly deferred from 0.1.0 to keep MVP lean:**
- UI (F11) → terminal output only in 0.1.0; UI in 0.2.0
- Multi-language (F13) → 0.2.0
- Hermetic test suite as a *feature* → it's an engineering practice, not a shipping feature; ≥95% coverage enforced but not advertised as a feature
- GitHub Action, cost tiering, redaction hooks → 0.2.0 nice-to-haves

**Exit bar:** one inspectable case where independent review surfaced what a single reviewer missed — or a disagreement report that improved a human call — on a real public-repo PR with full transcripts.

## 9.2 v0.2.0 — Broaden judgment

- **Second domain adapter: change management / ITSM** (CAB pre-processing story)
- **Basic review UI** (F11) — side-by-side A/B, debate timeline, terminal + browser
- Stronger disagreement taxonomy (interpretation vs evidence vs values)
- Argument-importance scoring — rank unresolved points by decision impact
- Debate-usefulness scoring as first-class metric
- Selective-debate triggers (iMAD-style: debate where it changes outcomes)
- Redaction hooks + retention policies (from [25-data-retention.md](25-data-retention.md))
- Multi-language artifact support (F13)
- GitHub Action wrapper for PR review

## 9.3 v0.3.0 — Scale and see

- N-agent extension mode (bridges toward AgentJury)
- Side-by-side debate visualization (full UI)
- Quality metrics dashboard: diversity, convergence quality, theater rate over time
- Additional adapters by community pull (contracts, incident hypotheses, procurement)
- Mid-debate human injection (from [05-features.md](05-features.md) §5.4)
- Heterogeneous pairing presets + diversity sweep reporting

## 9.4 v0.4.0 — Integrate with the fleet

- EvalForge integration: debate benchmark scenarios as reusable eval packs
- ToolTrust integration: debate verdicts as advisory layer before risky tool execution
- Historical learning: past unresolved disagreements → recurring-pattern surfacing
- `debate-eval` package extracted as standalone (from [21-eval-harness.md](21-eval-harness.md))
- Competitor benchmark protocol executed on 30-50 PRs (from [19-competitor-benchmark.md](19-competitor-benchmark.md))

## 9.5 v0.5.0 — Enterprise readiness

- PlannerCritic integration (from [24-fleet-integrations.md](24-fleet-integrations.md))
- HTTP service auth + RBAC (runner / reader / admin roles)
- Report localization (5 languages, from [22-internationalization.md](22-internationalization.md))
- Data retention & deletion policies implemented (from [25-data-retention.md](25-data-retention.md))
- Telemetry opt-in (anonymous adoption metrics)
- Data-classification tags on artifacts (public / internal / confidential)
- Schema migration tooling (`advdeb migrate`, from [14-schema-migration.md](14-schema-migration.md))

## 9.6 v0.6.0 — Vertical expansion

- AgentJury integration (disputed debates escalate to N-agent jury)
- 5+ community-contributed domain adapters (target: legal, finance, insurance-mock, media, academia)
- Adapter contribution protocol validated by external contributors (from [16-contributor-journey.md](16-contributor-journey.md))
- Cultural calibration: `--disagreement-style` (direct / diplomatic / formal)
- Contributor recognition program live

## 9.7 v0.7.0 — Eval & benchmark suite

- `debate-eval` v1.0 as standalone package with public benchmark suite
- Cross-domain field-test report published (Tier 1 breadth sweep results, from [field-testing strategy](../../field-test/field-testing-strategy.md))
- Model language coverage matrix community-maintained
- Flakiness benchmark: stability rates across model pairs published
- Article series (8 parts, from [18-article-plan.md](18-article-plan.md)) complete

## 9.8 v0.8.0 — Performance & scale

- Postgres backend (SQLite remains default; Postgres for fleet-scale)
- Streaming debate output (real-time claim/concession events via SSE)
- Batch pipeline mode (100+ artifacts, concurrent debates, queue management)
- High-availability deployment (stateless engine, shared Postgres, load balancer)
- Performance targets validated (from [15-performance.md](15-performance.md)): latency, cost, throughput

## 9.9 v0.9.0 — Internationalization & accessibility

- UI localization (5 languages)
- WCAG 2.1 AA accessibility audit + remediation
- Cultural calibration expanded (regional disagreement norms)
- Report localization (10+ languages)
- Enterprise SSO (SAML, OIDC)

## 9.10 v1.0.0 — Stable, proven, production-grade

**What 1.0.0 means:**
- **Stable public API** — no breaking changes without major version bump; deprecation policy documented
- **10+ domain adapters** — community-contributed and maintained
- **Production deployments** at 3+ organizations (at least 1 non-code vertical)
- **External security audit** passed (from [17-security-disclosure.md](17-security-disclosure.md))
- **Eval harness** as standalone package with reproducible benchmark suite
- **Full fleet integration** — ToolTrust, EvalForge, PlannerCritic, AgentJury
- **Accessibility:** WCAG 2.1 AA certified
- **Internationalization:** 10+ report languages, 5+ UI languages
- **Postgres** backend for fleet-scale; SQLite for single-machine
- **Documented SLA** for enterprise (latency, availability, security response)

**1.0.0 is not "feature complete."** It's "the API is stable, the product is proven across verticals, and the project is sustainable." Features continue post-1.0 via the adapter protocol and community contributions.

## 9.11 Kill criteria per version

| Version | Kill criterion | Action if fired |
|---------|---------------|-----------------|
| **v0.1.0** | Zero cases where B finds a materially different issue OR reports rated not-actionable | Reassess isolation mechanics; do not ship |
| **v0.2.0** | Tier 1 breadth sweep: >50% of non-code artifacts with no independence effect (theater ≥80%) | Vertical thesis wrong — pivot to code-only deepening |
| **v0.2.0** | Change-management adapter: no improvement over single-reviewer on real CRs | Drop ITSM; pick next domain by community pull |
| **v0.3.0** | N-agent mode: no quality gain over 2-agent on same artifacts | Drop N-agent; keep 2-agent as the product |
| **v0.4.0** | Fleet integrations add no value over standalone engine | Keep standalone; don't maintain integrations |
| **v0.6.0** | <3 community adapters contributed within 2 months of adapter protocol ship | Reassess contributor friction; simplify protocol |
| **v0.8.0** | Postgres backend shows no throughput improvement over SQLite at 50 concurrent debates | Keep SQLite as default; defer Postgres |
| **v1.0.0** | <3 production deployments after 12 months | Reassess market fit; consider narrowing to single vertical |

## 9.12 Sequencing principle

Every version must end with **a shipped, inspectable artifact** — never a benchmark-only release. Adapter breadth follows proof; proof follows field tests; field tests follow real artifacts. Versions don't ship because the calendar says so; they ship because the kill criterion didn't fire and the exit bar was met.
