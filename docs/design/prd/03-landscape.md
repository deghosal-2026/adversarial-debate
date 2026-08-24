# 03 — Landscape

> Sub-document of the [Design overview](../README.md). Who else operates here, what they solve, and the gap AdversarialDebate owns.

## 3.1 The three adjacent camps — and what none of them do

| Camp | Examples | What they do | What's missing |
|------|----------|--------------|----------------|
| **AI code review vendors** | CodeRabbit ($1.5B val, ~140K users), Greptile (Benchmark-led Series A), Graphite Diamond, Qodo | Single-agent review at scale; fast bug detection on PRs | One reviewer = one blind-spot profile. No independence mechanism, no dissent, no argument trace |
| **MAD research frameworks** | ChatEval, Society of Minds (Du et al.), iMAD, Free-MAD, Encouraging-Divergent-Thinking | Prove debate improves accuracy; novel topologies/trigger policies | Research artifacts: benchmarks and papers, not productized review engines with audit trails and domain adapters |
| **LLM-as-judge / ensembles** | JudgeBench-style judges, self-consistency, majority voting (SoM) | Cheap aggregation of N outputs | Voting counts positions; it never models *why* agents disagreed or whether the disagreement resolved |

## 3.2 The evidence that debate wins — and where voting stops

- Debate **beats consultancy** for oversight: 76% vs 54% judge accuracy ([Khan et al. 2024](https://arxiv.org/html/2407.04622v1)); an unopposed wrong answer is nearly as persuasive as a right one ([Kenton et al. 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/899511e37a8e01e1bd6f6f1d377cc250-Paper-Conference.pdf)).
- Debate **beats majority voting** on judgment benchmarks (JudgeBench SOTA) while modeling consensus dynamics ([arXiv 2510.12697](http://arxiv.org/abs/2510.12697)).
- Heterogeneous debate beats single frontier models through diversity of thought (91% GSM-8K, [alphaXiv/Mila](https://www.alphaxiv.org/overview/2410.12853v2)).
- Honest counterpoints we design against: with equal response counts, debate ≈ majority voting on some reasoning tasks ([Huang et al. 2023](https://arxiv.org/abs/2311.17371)); forced assigned stances *degrade* performance into rhetorical rigidity ([ACL ArgMining 2025](https://aclanthology.org/2025.argmining-1.6/)). Our answer: debate only what independent passes actually disagree on, and let agents argue their own committed views.

## 3.3 Adjacent portfolio positioning

| Fleet project | Relationship |
|---------------|--------------|
| PlannerCritic | Critiques a *plan before execution* (one critic vs one draft). AdversarialDebate arbitrates between *two independent conclusions* |
| AgentJury (#145) | Extends to N-agent consensus with forced-dissent mechanics; pairs as follow-on |
| ToolTrust Engine | Consumes debate verdicts as advisory input before risky tool execution |
| EvalForge / Braintrust | Measure debate quality: distinct-issue yield, convergence rates, report usefulness |

## 3.4 The open position

> **Independent-pass adversarial debate with dissent preservation, productized as a model-agnostic OSS review engine with audit-grade transcripts.**

Not a paper, not a feature inside a code-review SaaS, not a vote counter. The institution-grade pattern — independent review, structured challenge, preserved dissent — applied to every consequential artifact an AI system touches.

## 3.5 Defensibility (OSS terms)

1. **The isolation invariant is architectural**, so results are auditable — competitors bolting "debate mode" onto a shared-context pipeline can't prove independence.
2. **Evidence objects are first-class** (claims/objections/concessions), enabling quality measurement nobody else can compute.
3. **Domain adapters are pluggable** — PR review is v0.1; contracts, change requests, claims memos follow without core changes.
