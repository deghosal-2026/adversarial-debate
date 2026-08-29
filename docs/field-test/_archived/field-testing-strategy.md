# Field-Testing Strategy — 27 Domains, 4 Tiers

> Cross-version strategy for how we field-test adversarial debate across all 27 vertical domains when v0.1.0 ships only **one** domain adapter. This doc describes *what* we test at each tier, *how* we measure success given that ground truth exists for code but not for contracts/claims, and *which* domains earn a test before we build an adapter for them.

## The core tension

You cannot build 27 adapters before testing — and for most non-code domains, **ground truth does not exist** because the disagreement *is* the signal. So field-testing must split into two measurement regimes:

- **Ground-truth domains** (code, change requests with postmortems): binary — *did independent debate catch what was actually wrong?*
- **Expert-rated domains** (contracts, claims, policies): triad — *is the disagreement distinct? actionable? decision-changing?*

## The four tiers

| Tier | What's tested | Ground truth | Who runs it | Version |
|------|---------------|--------------|-------------|---------|
| **0 — Prove the loop** | Code only (PR-review adapter) | Real: merged-then-reverted PRs, security-advisory PRs, SWE-bench | You, public repos | **v0.1.0** (the falsifiable bar) |
| **1 — Breadth sweep, generic normalizer** | ~10 domains, 1-2 artifacts each, generic normalizer + domain prompt pack — *no adapters built* | Expert-rated usefulness (triad) | You + OSS community raters | v0.2.0 |
| **2 — Deep on one vertical** | Change-management/ITSM adapter, real CRs + outcomes | Postmortem-linked CRs, public incident reports | You + early users | v0.2.0 |
| **3 — Partner-gated regulated** | Healthcare, legal, finance, insurance | Partner's expert raters on their data, their boundary, their models | Domain partner, never the project | v0.3.0+ |

### Tier 0 — Prove the loop (v0.1.0)

The falsifiable binary bar from the charter:

> One realistic case where reviewer B finds a materially different issue before convergence — or a disagreement report that measurably improves a human call — on a real public-repo PR with full transcripts.

**Corpus:** merged-then-reverted PRs, GitHub Security Advisory PRs, SWE-bench verified tasks. These have known outcomes you can test against.

**Sweep:** 20-50 PRs; heterogeneous pair + homogeneous pair on each; flakiness sweep (N=5 runs); single-reviewer baseline comparison (code-review-style one-pass).

**Exit gate:** at least one PR where the independent pass surfaced what a single pass missed AND the report enabled a better human decision.

### Tier 1 — Breadth sweep, no adapters (v0.2.0)

This is the cheapest way to test whether the *independence invariant + debate mechanics* generalize **before** investing in adapters. Use a generic normalizer (accepts any text with a domain hint) + a domain-specific prompt pack (claim extraction rubric, evidence expectations). No domain-specific code.

**Corpus per domain (1-2 artifacts):**

| Domain | Source | Ground truth? | Rater |
|--------|--------|---------------|-------|
| Change management / CAB | Public postmortems (Cloudflare, AWS, GitHub Status) | ⚠️ outcome-known | Yourself/SRE peers |
| Legal — contracts | EDGAR filings, CC-BY model contracts, public MSA templates | ❌ (expert-rating only) | Your expert judgment + documented external counsel commentary (never legal advice) |
| Finance — credit memo | Public credit-rating rationale docs (Moody's, S&P) | ⚠️ subsequent downgrades | Yourself + sourced commentary |
| Media — fact-check | Published articles + later corrections (Wayback Machine before/after) | ✅ retraction pairs | OSS community |
| Academia — peer review | arXiv preprints + Retraction Watch entries | ✅ retraction pairs | Academic peers |
| Compliance — KYC narrative | Publicly available FCPA/AML case summaries + mock narratives | ⚠️ case outcomes known | Yourself |
| Incident — root cause | Public incident reports with known root cause | ✅ outcome-known | SRE community |
| Product — go/no-go | Public product launch postmortems, "why we killed X" blog posts | ❌ (narrative only) | Yourself |
| Procurement — SOWs | Public RFP/award documents + bidder proposals | ❌ (expert only) | Yourself |
| Insurance — claims | Public regulatory filings + mock claim scenarios (clearly marked) | ❌ (mock only) | Yourself (clearly marked fictional) |

**Measurement:** expert-rater triad on each debate:
1. **Distinctness** — is this issue materially different from what a single pass would find?
2. **`would_resolve_if` actionability** — could you act on this resolution path?
3. **Decision impact** — would this have changed your judgment on the artifact?

**Kill criterion:** if >50% of non-code artifacts across ≥5 domains show **no measurable independence effect** (theater rate ≥80%, distinctness rated low by multiple raters), the vertical thesis is wrong. This is discovered for the cost of prompts, not code.

### Tier 2 — Deep on one non-code vertical (v0.2.0)

The first new adapter built after code. **Hypothesis: change management / CAB.** Reason: artifacts are machine-readable (ticket metadata, CR forms), outcomes are often documented (postmortems), and the pain is loudest (CAB queuing).

**Corpus:** public CRs from open-source change management systems (backstage.io, cab-triage repos) + public postmortems referencing specific changes.

**Sweep:** same as Tier 0 (real outcomes, 20-50 artifacts, flakiness sweep, baseline comparison).

### Tier 3 — Partner-gated regulated (v0.3.0+)

Healthcare (protocol amendments, PV signals), finance (underwriting memos, real credit memos), legal (actual contracts under NDA), insurance (live claims). **The project never touches artifact content.** The process:

1. Project provides the engine + adapter skeleton + safe normalizer contract.
2. Partner deploys on *their* infrastructure, *their* models, *their* data boundary.
3. Partner runs debate, keeps artifacts, shares **anonymized disagreement reports only** — no artifact content.
4. Anonymized reports contribute to cross-domain fixture library for non-domain-specific quality metrics.

This is the only honest path to regulated verticals. Any PRD claim about these domains without a partner is speculative.

## Measurement protocol (all tiers)

| Regime | Metric | How measured |
|--------|--------|-------------|
| **Ground-truth tiers** (0, 2) | Distinct-issue yield | Did independent pass surface what was actually wrong? Measure vs revert/advisory/postmortem |
| **All tiers** | Verdict stability (flakiness) | N runs (seed-controlled, N≥5) → % of runs producing same verdict. Flag artifacts where verdict flips |
| **All tiers** | Homogeneous control falsifiable thresholds | Homogeneous pair (GPT+GPT) must fall within defined band: 0.4–0.8 avg convergence, 30–70% verdict rate. If outside this band, flag for isolation leak investigation. |
| **All tiers** | Theater rate | % of debates with zero claim-state changes (no concessions, no evidence shifts, no new objections). Exposed in reports |
| **All tiers** | Pair-diversity sweep | Homogeneous vs heterogeneous pair on identical artifact → delta in distinct-issue yield. Empirically tests the BYOM thesis |
| **Tiers 1-3** | Expert-rater triad | Domain expert rates: distinctness, `would_resolve_if` actionability, decision impact (binary: would this have changed my call?) |
| **Tiers 0, 2** | Baseline comparison | Single-reviewer pass (CodeRabbit-style) on same artifact vs adversarial result. Side-by-side report |

## Domain-selection rubric for field-test priority

Score each vertical on four axes; high-scorers earn Tier 1 (breadth) before Tier 2 (adapter):

| Axis | Weight | What to ask |
|------|--------|-------------|
| **Ground truth available?** | high | Can we know what the right answer was (revert, retraction, postmortem)? |
| **Artifacts publicly accessible?** | high | Can we run without a partner's private data? |
| **Expert rater accessible?** | medium | Can we find a domain-literate rater in the OSS community? |
| **Harm if wrong?** | critical | Would a false/misleading debate report cause real harm? (regulated = partner-gated only) |

**Results of the rubric applied (high-scorers first):**

| Domain | Ground truth | Public | Rater | Harm | Tier |
|--------|-------------|--------|-------|------|------|
| Software engineering | ✅ | ✅ | ✅ | low | **0** (ships) |
| Change mgmt / ITSM | ⚠️ | ✅ | ✅ | low | **1 → 2** |
| Media / publishing | ✅ | ✅ | ⚠️ | low | **1** |
| Academia | ✅ | ✅ | ⚠️ | low | **1** |
| Incident response | ✅ | ✅ | ✅ | low | **1** |
| Compliance (mock) | ⚠️ | ⚠️ | ✅ | low (mock) | **1** |
| Contracts (public) | ❌ | ⚠️ | ❌ | medium | **1** (rated only, not deployed) |
| Finance (public data) | ❌ | ⚠️ | ❌ | medium | **1** (rated only) |
| Insurance (mock) | ❌ | ❌ | ❌ | high | **3** (partnered) |
| Healthcare | ❌ | ❌ | ❌ | highest | **3** (partnered) |

## Harness design (as OSS contribution vector)

A separate `debate-eval` package (not the engine) that takes `(artifact, optional ground_truth, rating_rubric)` and emits a standardized cross-domain field-test report. Domain experts **contribute fixtures + rubrics without touching engine code** — this is how we reach 27 verticals with one maintainer.

EvalForge integration is natural here: each domain's seeded fixtures become reusable eval scenarios.

## Honest constraints

1. **Bifurcated success metric:** Tier 0/2 = bug-caught (binary); Tier 1/3 = expert-rated usefulness (triad). Don't pretend a contract field test "found a real bug." It produced a disagreement a counsel rated actionable. State it.
2. **Tier 1 is breadth, not depth:** 1-2 artifacts per domain proves mechanism, not deployment readiness.
3. **Regulated verticals are partner-gated, full stop.** No public-data field test of PHI, real contracts under NDA, or live claims.
4. **Anonymized disagreement reports can flow back; artifact content cannot.** That is the contribution loop for Tier 3.
5. **This strategy is itself a contribution surface** — domain experts propose artifact sources and rubrics for their domain via GitHub issues, no code required.