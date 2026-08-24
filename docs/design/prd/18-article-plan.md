# 18 — Article & Content Plan

> Sub-document of the [Design overview](../README.md). The narrative arc for the ≥2 dev.to articles committed in AD-M3, plus the series that follows. Articles ship only after v0.1.0 is complete (vault article rule).

## 18.1 Why articles matter for this project

AdversarialDebate's value is *inspectable* — the interesting moments are human-readable (two agents disagreeing about a risky PR, one catching a blind spot). Every article is built around a real transcript, not a benchmark table. This is the content engine that drives adoption.

## 18.2 v0.1.0 launch articles (≥2, committed in AD-M3)

### Article 1 — "I Asked Two AI Models to Review the Same PR Independently. They Disagreed."

**Hook:** The v0.1.0 bar case study — a real public-repo PR where reviewer B found a materially different issue than A, pre-convergence.

**Structure:**
1. The problem: why "second opinion" AI review is fake (shared-context contamination)
2. The setup: two isolated reviewers, same PR, no peeking
3. The debate: transcript excerpts — A's review, B's review, the revelation, the point-by-point challenge
4. The outcome: disagreement report with `would_resolve_if`
5. The resolution: what happened when the human tested reviewer B's finding
6. What this means: independent review is a product, not a prompt trick

**Target:** 2,500-3,500 words. Published on dev.to + Hashnode.

### Article 2 — "Most AI Second Opinions Are Agreement with Extra Steps. Here's the Fix."

**Hook:** The architectural argument — why mechanical independence (engine-enforced isolation) beats prompted independence (telling a model to "be critical").

**Structure:**
1. The painful truth: show a transcript of shared-context "review" where B just paraphrases A
2. Why it happens: anchoring, social proof, effort minimization — the three contamination modes
3. The fix: delayed revelation as an engine state transition, not a prompt instruction
4. Evidence: scalable-oversight research (debate 76% vs consultancy 54%)
5. What you can do: `pip install adversarial-debate` + your models + 10 minutes
6. Honest limitation: shared blind spots still exist; debate ≠ omniscience

**Target:** 2,000-3,000 words. Published on dev.to + Hashnode.

## 18.3 Series arc (post-launch, weekly)

| # | Title | Angle | When |
|---|-------|-------|------|
| 3 | "I Forced Two Models to Debate a Contract Clause. The Disagreement Report Was Better Than the Verdict." | First non-code vertical experiment (Tier 1 breadth sweep) | v0.2.0 |
| 4 | "The Theater Rate: When AI Debate Changes Nothing and How to Detect It" | The anti-metric — debates with zero state changes; why detecting theater matters more than detecting agreement | v0.2.0 |
| 5 | "Heterogeneous Pairs Beat Single Frontier Models. Here's the Evidence." | Diversity-of-thought data from field tests; BYOM as quality dial | v0.2.0 |
| 6 | "I Pre-Screened a Week of CAB Changes with Two AI Reviewers. The Board Read Only the Disagreements." | Change-management adapter field test; the CAB spotlight CUJ | v0.2.0 |
| 7 | "How to Contribute a Domain Adapter Without Touching the Engine" | Contributor journey; the adapter protocol as OSS contribution vector | v0.3.0 |
| 8 | "When Debate Fails: A Catalog of Bad Debates and What They Teach Us" | The failure-mode catalog (FM-1 through FM-10) as readable content | v0.3.0 |

## 18.4 Content principles

1. **Every article includes a real transcript** — no synthetic examples. If we don't have a transcript, we don't write the article.
2. **Honest limitations in every piece** — shared blind spots, theater rate, flakiness. Readers trust writers who name the failures.
3. **The `would_resolve_if` field is the hero** — it's the actionable artifact that makes disagreement useful instead of frustrating.
4. **No benchmark tables without distinctness verification** — "issues found" without proving they're distinct from single-reviewer baseline is the game vendors play. We don't.
