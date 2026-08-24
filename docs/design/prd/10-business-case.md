# 10 — Business Case & Adoption

> Sub-document of the [Design overview](../README.md). The economic argument, buyer personas, why bring-your-own-LLM is the strategic unlock, and the adoption path.

## 10.1 The economic argument

The universal formula across all twenty-seven verticals:

```
Cost(debate)   = ~2× single-review inference per artifact (bounded rounds ≈ 2-4× total)
Cost(miss)     = incident · lawsuit · payout · downtime · regulatory exposure
Break-even     = catching ONE material issue funds thousands of debate passes
```

Illustrative math by domain (conservative, directional):

| Domain | Cost of one miss | Cost of one debate pass | Ratio |
|--------|------------------|------------------------|-------|
| Software PR | hotfix + incident review + on-call hours + trust erosion | cents-to-dollars of tokens | 100-10,000× |
| Emergency change (ITSM) | hours of unplanned downtime for the business | a few dollars | orders of magnitude |
| Contract clause | uncapped indemnity discovered at dispute time | a few dollars | potentially six figures |
| Claim adjudication | wrongful denial → regulator complaint + customer churn | a few dollars | reputation compounding |

And the capacity math: AI already generates more reviewable artifacts than humans can review (~41% of commits AI-assisted; CAB queues lengthening; contract volume scaling with AI drafting). The choice is not "human review vs AI debate." It is **"AI debate vs no meaningful review at all."**

## 10.2 Why bring-your-own-LLM is the strategic unlock

AdversarialDebate sells **no model** — it orchestrates the reviewers the customer already trusts. That single design decision opens doors model-locked vendors can't enter:

1. **Data residency clears procurement.** Regulated buyers (healthcare, banking, government, legal) often *cannot* send artifacts to a vendor's chosen endpoint. With BYOM, both reviewers run wherever the artifact is allowed to live — approved enterprise endpoints, private VPC deployments, or local models for the most sensitive documents.
2. **Existing commitments honored.** Customers have negotiated enterprise agreements, capacity reservations, and compliance sign-offs with specific providers. The engine rides those contracts instead of fighting them.
3. **Heterogeneity becomes a quality dial, not an accident.** Two different model families catch materially different issues (diversity-of-thought evidence, [Mila 2025](https://www.alphaxiv.org/overview/2410.12853v2)). Customers choose the pairing that matches their risk appetite — and can A/B pairings over time as models evolve.
4. **Cost tiering per artifact class.** Cheap reviewer pair for routine PRs and waivers; frontier pairs reserved for first-round disputes and high-severity artifacts. The customer sets spend where their risk lives.
5. **No lock-in, no obsolescence.** Models improve monthly; the engine captures the *debate process* — claims, objections, concessions, verdicts — which outlives any provider's pricing or policy changes.

> Customer-facing one-liner: **"Your models. Your data boundary. Independent second opinions that are actually independent."**

## 10.3 Buyer personas

| Persona | Pain today | Metric they own | Why they buy |
|---------|-----------|-----------------|--------------|
| **VP Engineering / Platform** (beachhead) | Review capacity is the delivery bottleneck; AI review = one confident agent's opinion | Escaped-defect rate; cycle time with confidence | Second opinions that aren't primed to agree; audit trail per PR |
| **Head of ITSM / Change Management** | CAB queues growing; emergency changes skip scrutiny | Failed-change rate; board throughput | Pre-screened queue; humans read only genuine disputes |
| **Legal Ops / GC delegate** | AI-drafted contracts reviewed by one AI reader | Outside-counsel spend; signature velocity with coverage | Ambiguity pinpointed pre-signature, not litigated post-signature |
| **CISO / AppSec lead** | Vuln triage inconsistency; agents proposing actions | Mean time-to-validate; agent action safety | Structured challenge on threat models and agent plans |
| **Chief Risk / Compliance Officer** | Four-eyes obligations satisfied ritually, not substantively | Audit findings; evidence quality | Dissent-preserved reports are audit-ready evidence of real scrutiny |
| **AI platform teams (builders)** | No OSS building block for multi-model judgment in their pipelines | Time-to-integrate | Verdict/disagreement API behind their own models; MIT license |

## 10.4 Market timing (recap from [01-why](01-why.md))

- AI code review: ~$420M ARR, +133% YoY, demand searches +310% — and it's all single-reviewer.
- Review capacity, not generation, is the stated #1 constraint of 2026 engineering orgs.
- MAD research matured (2023-2025): debate beats consultancy 76% vs 54%; heterogeneous pairs beat single frontier models. Productization gap: open.

## 10.5 Go-to-market (OSS-first)

1. **Ship the engine open source (MIT).** Bottom-up adoption seeded exactly how the category leader did it — free for OSS repos, frictionless CLI.
2. **Field-test report as flagship content.** Real PRs from a public repo; publish the transcripts where reviewer B caught what A missed. Articles ride each finding ([article plan](../../../../training/articles-to-be-published/adversarial-debate/article-idea.md)).
3. **Wedges:** GitHub Action for PR review (beachhead) · CLI for every other artifact type · Python API + FastAPI service for platform teams embedding judgment into pipelines.
4. **Vertical expansion via adapters**, prioritized by community pull: change-management adapter next (loudest non-code pain), then contracts.

## 10.6 KPI tree

| Level | Metric |
|-------|--------|
| North star | Materially distinct issues surfaced per 100 artifacts reviewed |
| Debate quality | Convergence rate vs disputed rate; % of disputes with actionable `would_resolve_if`; "theater rate" — debates that changed nothing (minimize, expose honestly) |
| Customer outcome | Escaped-issue delta vs baseline single-reviewer setup; human decision time on disputed items |
| Adoption | Repos/orgs running debates; artifacts processed; adapter diversity in the wild |

## 10.7 What makes v0.1.0 credible to a customer

Not benchmarks — **one inspectable case study**: a real public-repo PR where two isolated reviewers disagreed, the disagreement report named the exact risk and what would resolve it, and resolution confirmed reviewer B. Everything else in this PRD exists to make that moment repeatable and auditable.

## 10.8 Human-reviewer baseline comparison

When a buyer asks "why not just ask another human?" — the realistic calculation, not the ideal:

| Dimension | Human second opinion | Single AI reviewer | AdversarialDebate |
|-----------|--------------------|--------------------|-------------------|
| **Cost per review (code)** | $50-150 (senior eng, 20-40 min) | $0.01-0.10 | $0.02-0.40 |
| **Latency** | 4-24 hrs (async review) | 30-120s | 60-300s |
| **Coverage (24/7)** | No (sleep, meetings, weekends) | Yes | Yes |
| **Independence guarantee** | Social: human can choose not to peek at the first review | None (sees the first answer) | Mechanical: engine-enforced |
| **Dissent preserved?** | Only if reviewer writes it separately | No | Yes — structured |
| **Audit trail** | Memory + comments | One-pass inline comments | Full lineage: claims, objections, concessions, verdicts |
| **Maturing/degrading** | Gets better with experience, slower at scale | Gets better per-model-release, zero marginal accumulation | Gets better per-run (adapters, rubrics), per-model-release |

**Honest trade-off:** AdversarialDebate cannot replace the human who knows the context of a specific decision. What it replaces is the *second human reviewer whose job is to find things the first one missed* — the four-eyes check. And it does that faster, cheaper, and with a better audit trail.

## 10.9 OSS sustainability & open-core boundary

- **Engine + CLI + all adapters:** MIT open source, forever. No source-available bait-and-switch.
- **Revenue boundary (conceptual, post-0.1):** hosted UI/dashboard, enterprise policy server, compliance pack generator, priority support. These are aspirational — not funded, not committed.
- **Patent stance:** zero software patents. The project competes on execution and adoption, not IP.
- **Why build OSS with no revenue model today:** every project in the fleet ships MIT; the portfolio builds career evidence and community pull; the article series funds the effort through reach. If adoption outpaces capacity, the open-core boundary provides a sustainable path without threatening the OSS base.
- **Contributor model:** MIT license means companies can deploy the engine internally without GPL-style disclosure concerns — aligns with the BYOM / self-hosted deployment model. Adapter contributions flow through the protocol (normalizer + rubric) without requiring engine expertise.

## 10.10 Time-to-first-value (the first 10 minutes)

A buyer's first question after "why?" is "how fast do I get value?" The onboarding CUJ:

```
1. pip install adversarial-debate                    # 10 seconds
2. advdeb init                                         # creates config: provider registry, 2 reviewer slots
3. edit config: add 2 model endpoints (your keys)     # 1 minute
4. advdeb review --pr https://github.com/owner/repo/pull/123
                                                       # 60-300 seconds: independent passes + debate
5. read the report                                     # verdict or disagreement, side-by-side in terminal or UI
```

**Target:** from install to first inspectable report in under 10 minutes, using the buyer's own models, on a real PR. No signup, no API key from us, no vendor portal.

**Why this matters:** CodeRabbit's adoption curve was seeded by one-click GitHub marketplace install + free OSS tier. AdversarialDebate's wedge is even lower friction — no account at all, just `pip install` + your models. The first debate a user runs is either the "B caught what A missed" moment or it isn't. If it is, they configure it into CI. If it isn't, nothing else in this PRD matters.

## 10.11 What makes v0.1.0 credible to a customer

Not benchmarks — **one inspectable case study**: a real public-repo PR where two isolated reviewers disagreed, the disagreement report named the exact risk and what would resolve it, and resolution confirmed reviewer B. Everything else in this PRD exists to make that moment repeatable and auditable.
