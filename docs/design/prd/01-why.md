# 01 — Why (Business Requirements)

> Sub-document of the [Design overview](../README.md). Covers the market context, the pain we remove, and why this matters now — for the OSS portfolio and for every team that lets an AI system near a consequential decision.

## 1.1 The market context

The agent ecosystem has spent enormous energy on **generation** — writing code, drafting contracts, summarizing incidents, producing answers — and almost none on **review independence**. The emerging discipline of AI review is mostly one model glancing at another model's answer. That is not review. It is agreement with extra steps.

Meanwhile the volume problem is exploding:

- **AI writes the code; humans can't read it fast enough.** ~84% of developers now use AI coding tools and roughly **41% of commits are AI-assisted**. The primary constraint in 2026 is **review capacity, not generation capacity**: organizations generate more parallel changes than human reviewers can validate ([zylos.ai research, 2026](https://zylos.ai/research/2026-01-19-ai-code-review-tools)).
- **AI review became a category — fast.** Pure-play AI code review vendors hit roughly **$420M ARR growing ~133% YoY**, with ~44% of engineering teams using AI review on some PRs. Search demand for "AI code review" grew **+310%** between mid-2025 and Q1 2026 ([IdeaPlan, 2026](https://www.ideaplan.io/blog/ai-code-review-tools-market-share-2026)). CodeRabbit alone reached **~140K paid users and a $1.5B valuation within three years** ([Reuters, Aug 2026](https://www.reuters.com/technology/ai-code-review-platform-coderabbit-valued-15-billion-latest-funding-round-2026-08-12/)); Greptile raised $25M from Benchmark reporting **180K+ bugs surfaced in a month**.
- **Every generated artifact creates a review liability.** Contracts drafted by LLMs, incident hypotheses proposed by agents, rollout plans authored by copilots — all of them inherit the generator's blind spots *and* its confident tone.

But the category being built is **single-reviewer** review: one agent, one pass, one confident comment stream. Nobody has productized what human institutions learned over centuries — that the value of a second opinion collapses the moment the second opinioner knows what the first one said.

## 1.2 The painful truth: most AI "second opinions" are primed to agree

The standard setup is: model A produces an answer; model B is asked to double-check **while looking at A's answer**. B absorbs A's framing, assumptions, and conclusion before forming its own view. Convergence is baked in.

The scalable-oversight literature quantifies how bad this is:

- **Without an adversary, a wrong consultant is nearly as convincing as a right one.** In open consultancy, judges follow the consultant at roughly the same rate whether the consultant is correct or incorrect ([Kenton et al., NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/899511e37a8e01e1bd6f6f1d377cc250-Paper-Conference.pdf)).
- **Adversarial debate measurably fixes this.** With GPT-4-Turbo debaters, judge accuracy was **76% under debate vs 54% under consultancy vs 48% naive baseline** ([Khan et al., 2024](https://arxiv.org/html/2407.04622v1)). When the protagonist is wrong, an antagonist substantially raises judge accuracy ([UChicago lecture summary of Kenton et al.](https://uchicago-llm-course.github.io/spring2026-lectures/lecture-09/)).
- **Truth has a structural advantage under pressure.** Across cross-play tournaments, debaters assigned the correct answer consistently achieve higher Elo — persuasiveness correlates with truthfulness *only* under adversarial conditions ([Pham et al., "Debating with More Persuasive LLMs"](https://www.alphaxiv.org/overview/2402.06782)).

And the multi-agent-debate (MAD) literature shows independent reasoning passes convert directly into quality:

- Debate improved factuality and reasoning across math, fact-checking, and translation benchmarks ([Du et al., ICML 2023](https://arxiv.org/abs/2305.14325)).
- **Heterogeneous models debating beat any single frontier model** — 91% on GSM-8K via diversity of thought ([Hegazy, Mila, 2025](https://www.alphaxiv.org/overview/2410.12853v2)).
- Selective MAD yields **up to +13.5% accuracy at up to −92% token cost** ([iMAD, arXiv 2511.11306](https://arxiv.org/abs/2511.11306)) — the economics are tractable when debate triggers where it matters.

### 1.2.1 Why shared-context review is blind

A second reviewer that sees the first answer inherits three failure modes at once: **anchoring** (adopts the same reading of the diff), **social proof** (a confident first answer reads as validated), and **effort minimization** (paraphrase is cheaper than independent analysis). The output looks like diligence. None occurred.

### 1.2.2 Why collapsing dissent destroys the signal

Even multi-agent systems usually end with a forced synthetic answer — a vote count or an averaged paragraph. What gets thrown away is the *reasoning trace of the disagreement*: which assumption broke, whose evidence held up, what would change the loser's mind. For high-stakes review, that trace is worth more than the verdict.

### 1.2.3 The institution precedent

Humans solved this already, domain by domain: four-eyes principles in banking, red teams in security, devil's-advocate offices in intelligence, defense-in-depth peer review in medicine and academia, dissent channels in judicial panels (Supreme Courts publish dissents because they are valuable). Every serious review institution on earth enforces **independence before interaction** and **preserves minority arguments**. AI review pipelines do neither. AdversarialDebate closes that gap.

## 1.3 Why this matters beyond code

Code review is just the beachhead. Any consequential decision artifact benefits from independent adversarial review — contracts before signature, credit memos before approval, claims before payout, incident hypotheses before mitigation, launch plans before go/no-go. Section [04-users-and-cujs.md](04-users-and-cujs.md) maps **fourteen industry verticals** to the same underlying loop: normalize the artifact → two isolated passes → structured debate → verdict or preserved dissent.

## 1.4 Why now

1. **Generation exploded; review did not.** The review-capacity bottleneck is the stated #1 constraint of 2026 engineering orgs — and the identical pattern is repeating in legal ops, claims, and compliance.
2. **The evidence base matured.** 2023-2025 produced replicated results: debate beats consultancy, heterogeneous debate beats single models, dissent carries information.
3. **Nobody owns the category.** Code-review vendors compete on single-agent bug detection. MAD lives in research repos. The productization gap — *independent-pass debate with dissent preservation, as a model-agnostic OSS engine* — is open.
4. **It compounds with our fleet.** EvalForge measures agents, Observatory observes them, ToolTrust gates their actions, PlannerCritic audits their plans. AdversarialDebate adds the missing layer: **independent judgment on their conclusions**.
