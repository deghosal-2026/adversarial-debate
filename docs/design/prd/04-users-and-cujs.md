# 04 — Users & CUJs (Who Needs This, and Why)

> Sub-document of the [Design overview](../README.md). Primary users, the vertical map — **twenty-seven industry domains** where independent adversarial review of a consequential artifact pays for itself — and the core user journeys.

## 4.1 Primary user

Teams that use AI to produce or evaluate **consequential decision artifacts** — where the cost of a wrong call is far higher than the cost of one more review pass. They already believe in second opinions; they've noticed their AI second opinions always agree.

## 4.2 Secondary users

- Code review / platform teams building AI-assisted review pipelines
- Legal ops and deal desks drowning in AI-drafted contracts
- Change managers and CAB chairs reviewing AI-proposed changes
- Incident commanders arbitrating competing root-cause hypotheses
- Risk, compliance, and audit functions with four-eyes obligations
- AI safety / eval engineers who need disagreement metrics, not vote counts

## 4.3 Not for

- Low-stakes single-turn tasks where disagreement has no value
- Teams that want a faster yes instead of a more trustworthy answer
- Workflows where reviewer B must see private context A never had (the engine surfaces this honestly rather than pretending)

## 4.4 The universal pattern

Every vertical below shares one shape:

```
consequential artifact → independent pass ×2 → structured challenge → verdict OR preserved dissent
```

Only the adapter changes: what gets normalized, what claims look like, what "evidence" means.

## 4.5 Vertical map — twenty-seven industry domains

Because reviewers are **user-chosen models** (bring-your-own-LLM), every domain below is addressable with whatever provider its regulators, contracts, and budgets allow — a hospital can run both reviewers on private in-VPC deployments; a startup can mix two frontier APIs. The engine is the product; the model is the customer's choice.

### Cluster A — Software & Digital Infrastructure

| # | Domain | Artifact under review | What adversarial debate catches | v0.1.0? |
|---|--------|----------------------|--------------------------------|---------|
| 1 | **Software engineering** | PR diffs, ADRs, migration plans | The bug the first reviewer's framing hid; missing rollback analysis | ✅ ships |
| 2 | **Change management / ITSM** | Change requests, CAB agendas, emergency-change justifications | Underestimated blast radius; freeze-window conflicts; "standard change" that isn't; rollback that doesn't reverse anything | roadmap |
| 3 | **Cybersecurity** | Threat models, pentest-report triage, AI-agent action plans | Overrated/underrated vulns; compensating-control assumptions nobody verified | roadmap |
| 4 | **SRE / incident response** | Root-cause hypotheses, postmortem drafts | Timeline evidence that only holds under one reading; coincidental correlations promoted to causes | roadmap |
| 5 | **Data & ML engineering** | Pipeline changes, model release notes, eval regressions | Silent upstream dependency breaks; metric definitions that shifted between reviewers' assumptions | roadmap |

### Cluster B — Commercial & Legal

| # | Domain | Artifact under review | What adversarial debate catches | v0.1.0? |
|---|--------|----------------------|--------------------------------|---------|
| 6 | **Legal & contracts** | MSAs, NDAs, DPAs, redlines before signature | Limitation-of-liability gaps; conflicting cross-referenced clauses; jurisdiction traps the drafting model papered over | roadmap |
| 7 | **Sales & deal desk** | Non-standard terms, RFP responses before submission | Commitment language sales didn't notice it made; revenue-recognition landmines | roadmap |
| 8 | **Procurement & vendor risk** | Vendor security questionnaires, bid evaluations, SOWs | Copy-paste vendor answers contradicting their own docs; scoring criteria applied unevenly across bidders | roadmap |
| 9 | **Marketing & advertising** | Claim substantiation before campaigns launch | Comparative claims the source doesn't support; disclosure language missing where regulators expect it | roadmap |
| 10 | **Media & publishing** | Pre-publication fact-check passes, editorial judgments | Claims sourced to their own echo; counter-evidence neither pass found alone | roadmap |

### Cluster C — Financial & Risk Operations

| # | Domain | Artifact under review | What adversarial debate catches | v0.1.0? |
|---|--------|----------------------|--------------------------------|---------|
| 11 | **Banking & lending** | Credit memos, committee papers | Cherry-picked comps; covenant headroom under the downside case never tested | roadmap |
| 12 | **Investment management** | IC memos, diligence summaries | Concentration risk glossed by both analyst and sponsor; exit assumptions taken from the pitch deck | roadmap |
| 13 | **Insurance** | Claims adjudication memos, underwriting referrals | Fraud-signal vs legitimate-explanation ambiguity kept explicit instead of force-resolved | roadmap |
| 14 | **Compliance & audit** | SAR narratives, KYC decisions, audit-finding responses | Narrative that satisfies the checklist but not the facts; remediation claims that don't match evidence | roadmap |
| 15 | **Tax & accounting** | Position memos, provision reviews | Authority cited for a proposition it doesn't reach; treatment inconsistent with prior-year filing | exploratory |

### Cluster D — Industrial & Physical Operations

| # | Domain | Artifact under review | What adversarial debate catches | v0.1.0? |
|---|--------|----------------------|--------------------------------|---------|
| 16 | **Manufacturing** | Engineering change orders (ECOs), quality deviations, supplier corrective actions | BOM line affected downstream that neither reviewer traced; deviation disposition inconsistent with history | roadmap |
| 17 | **Energy & utilities** | Switching plans, safety cases, maintenance windows | Step that de-energizes the wrong feeder; safety-case assumption invalidated by another step in the same plan | roadmap |
| 18 | **Construction & real estate** | Change orders, RFIs, draw requests, lease abstracts | Cost-impact chain broken at an unpriced dependency; abstract missing a clause that contradicts the summary | roadmap |
| 19 | **Automotive & aerospace** *(human-certified always)* | OTA update risk reviews, maintenance compliance records | Fleet-segment edge case; certification basis touched by a change described as cosmetic | exploratory |
| 20 | **Telecommunications** | Network change windows, capacity plans | Peering/routing impact outside the change scope; capacity math valid only at current traffic mix | roadmap |
| 21 | **Logistics & supply chain** | Customs classifications, carrier contracts, network redesigns | HS-code reasoning that fails on the tariff's exception clause; single-sourcing risk introduced silently | exploratory |

### Cluster E — People, Public & Knowledge

| # | Domain | Artifact under review | What adversarial debate catches | v0.1.0? |
|---|--------|----------------------|--------------------------------|---------|
| 22 | **Healthcare & pharma** *(clinician-in-the-loop always)* | Protocol amendments, differential write-ups, pharmacovigilance signals | Excluded confounder; eligibility-criterion conflict; signal-vs-noise disagreement preserved for clinician judgment | exploratory |
| 23 | **HR & people ops** | High-stakes policy decisions, termination justifications | Inconsistent precedent application; documentation gaps that create legal exposure | exploratory |
| 24 | **Government & grants** | Application reviews, permit decisions, procurement awards | Scoring drift between reviewers; criterion applied differently across applicants | exploratory |
| 25 | **Academia** | Peer-review assist, thesis committee memos | Methodological objection raised and dismissed too fast; related-work claim that doesn't survive citation check | exploratory |
| 26 | **Product management** | Go/no-go launch reviews, tradeoff memos | Success metric nobody committed to; dependency both owners assumed the other held | roadmap |
| 27 | **Customer support operations** | Escalation/refund exceptions, policy waivers | Waiver inconsistent with the last ten identical cases; goodwill cost underestimated by policy-only framing | roadmap |

> **Beachhead logic:** software engineering ships first because artifacts are machine-readable (diffs), ground truth is cheap (CI, tests), and demand is proven ($420M+ category). Clusters B-D reuse the identical engine behind new normalizers + rubrics — each new vertical is an adapter, not a rewrite. Exploratory rows ship only with domain-expert partnership and strict human-in-the-loop framing.

### 4.5.1 Spotlight: change management (ITSM)

CAB is humanity's oldest deployed adversarial-review institution — and it is drowning: AI coding agents propose changes faster than boards can convene, emergency changes bypass scrutiny precisely when risk is highest, and rubber-stamping is endemic. AdversarialDebate as a CAB pre-processor:

1. Every change request → two isolated risk analyses (blast radius, sequencing, rollback adequacy, freeze conflicts).
2. Disagreements surface *before* the meeting: "Reviewer B finds rollback step 2 assumes the config schema that step 1 removes."
3. Converged low-risk changes auto-clear with the debate transcript attached; human attention concentrates on genuine disputes.

The board stops reading every request and starts reading only the disagreements.

### 4.5.2 Why bring-your-own-LLM wins each cluster

- **Regulated clusters (C, E-healthcare):** artifacts often *cannot* leave the buyer's boundary. A vendor with hardcoded models is disqualified on day one; an engine that runs reviewers on the buyer's approved endpoints (including private VPC or local deployments) clears procurement.
- **Commercial clusters (A, B):** heterogeneity is quality. Two different model families catch materially different issues ([diversity-of-thought evidence](https://www.alphaxiv.org/overview/2410.12853v2)) — customers pick the pairing that fits their risk profile.
- **Everyone:** cost tiering. Cheap reviewer pair for routine artifacts; escalate to frontier pairs only when first-round disagreement appears. The customer controls spend per artifact class — impossible when the vendor owns the model choice.

## 4.6 Core user journeys

### CUJ-1 — Platform engineer: the risky infra PR *(ships in v0.1.0)*

> Maya opens a PR migrating the orders table to a new partitioning scheme. CI is green; her single AI reviewer says "looks good." She runs `advdeb review pr 482`.
>
> Two isolated reviewers commit independently: A sees a clean migration; B flags lock-timeout risk on a 40GB table. Revelation opens; A rebuts with row-count estimates; B holds — the debate transcript shows exactly which assumption broke. **Verdict: DISPUTED**, with `would_resolve_if: load test at production row count`. Maya runs the load test in 20 minutes instead of discovering the timeout at 2 AM.

**Value:** the second opinion that wasn't primed to agree — and an audit trail showing why the extra check was worth it.

### CUJ-2 — In-house counsel: contract redline before signature *(roadmap)*

> Dev signs off on a vendor MSA drafted by an AI assistant. Before signature, legal ops runs adversarial review. Reviewer A reads limitation-of-liability as capped; B reads the indemnity carve-out as uncapped — they disagree on cross-reference interpretation. The disagreement report pins clause §11.2 vs §14.1 and states what resolves it: the insurer's confirmation letter. Dev negotiates one clause instead of discovering the gap at claim time.

**Value:** ambiguity *preserved and pinpointed* rather than flattened into false confidence.

### CUJ-3 — CAB chair: pre-screening the week's change queue *(roadmap)*

> Twelve change requests, forty minutes of board time. The engine converges eight as low-risk (transcripts attached) and disputes four. One dispute: an "emergency" patch whose rollback plan references a backup job retired last quarter. The board spends its entire slot on the four that deserve it.

**Value:** human judgment allocated by disagreement, not by queue order.

### CUJ-4 — Incident commander: two root causes, one burning system *(roadmap)*

> Midnight outage; agent tooling proposes two competing hypotheses: deploy vs upstream DNS. AdversarialDebate forces each hypothesis to attack the other's timeline evidence. A concedes the deploy correlation is coincidental (canary cluster unaffected); B concedes DNS alone can't explain the error-rate shape. Report: partial convergence, two decisive probes listed. On-call tests those first.

**Value:** faster MTTR through structured hypothesis combat instead of loudest-voice debugging.

### CUJ-5 — Credit analyst: borderline memo goes to committee *(roadmap)*

> A credit memo recommends approval. Adversarial review: A upholds; B challenges the covenant headroom under the downside case. DISPUTED on one point — sensitivity to rate reset timing — resolved analysis attached. Committee sees the strongest version of both sides, not just the sponsor's memo.

**Value:** four-eyes compliance that produces real scrutiny, not countersigned ritual.

### CUJ-6 — Claims adjuster: the ambiguous file *(roadmap)*

> A water-damage claim matches three fraud indicators and two innocent explanations. Debate keeps the ambiguity alive and names the single document (plumber's invoice timestamp) that discriminates between them. Adjuster requests one item instead of denying or paying blind.

**Value:** better decisions at the ambiguity boundary — exactly where money is won or lost.

### CUJ-7 — Fact-checker: pre-publication pass *(roadmap)*

> An explainer article cites a statistic twice; both passes initially agree it's fine. Under challenge, B traces it to a press release citing itself. Converged verdict post-concession: replace or attribute. The concession event is logged — proof the check had teeth.

**Value:** editorial trust backed by inspectable process, not vibes.

### CUJ-8 — Security engineer: reviewing what an AI agent is about to do *(roadmap, ToolTrust integration)*

> An ops agent proposes bulk certificate rotation. Before execution, its plan gets adversarial review: B objects the plan skips the DR-region issuer. Verdict: blocked pending revision — with the argument trace attached to the audit log.

**Value:** advisory judgment layer on top of enforcement — the fleet integration story.

## 4.7 Anti-journeys (what we will NOT pretend)

- **Not autonomous sign-off.** Irreversible high-stakes calls keep human owners; the output is a better-informed human, faster.
- **Not a lie detector.** Two debaters can share a blind spot; reports state coverage, not certainty.
- **Not theater.** If debate changed nothing, the report says so — debate-usefulness is a measured metric, not a vibe.
