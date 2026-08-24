# 19 — Competitor Benchmark Protocol

> Sub-document of the [Design overview](../README.md). Exactly *how* to run AdversarialDebate and a single-reviewer tool on the same artifacts and compare. The procurement-defeating experiment needs a protocol, not a vibe.

## 19.1 Why a protocol matters

A buyer asks: *"Show me AdversarialDebate is better than CodeRabbit on the same PR."* Without a defined protocol, the comparison is cherry-picked. With one, it's falsifiable — and if we lose on some artifacts, that's honest data that improves the product.

## 19.2 The protocol

### Step 1 — Corpus selection

- 30-50 PRs from public repos, stratified by:
  - Size: small (<200 lines), medium (200-2000), large (>2000)
  - Outcome: merged-clean, merged-then-reverted, rejected, security-advisory
  - Language: Python, TypeScript, Go, Java (minimum)
- Corpus is **published** before running — no post-hoc filtering.

### Step 2 — Baseline run (single-reviewer)

- Run CodeRabbit (or equivalent single-reviewer tool) on each PR
- Capture: issues found, issue text, severity, latency, cost
- Do NOT look at results yet

### Step 3 — Adversarial run

- Run AdversarialDebate on each PR with the same model family as the baseline (fair comparison — same underlying capability)
- Capture: issues found by A, issues found by B, issues surfaced only after debate, convergence/disputed status, latency, cost
- Run flakiness sweep (N=5) on a 20% subsample

### Step 4 — Distinctness rating (blind)

- A rater (who hasn't seen which tool produced which output) receives:
  - Baseline issues list (anonymized as "Tool X")
  - Adversarial issues list (anonymized as "Tool Y")
- Rater marks each issue as: `distinct` (only one tool found it) or `overlap` (both found it)
- Rater marks each `distinct` issue as: `material` (affects the decision) or `noise` (style, nitpick)

### Step 5 — Report

| Metric | Baseline (single) | Adversarial | Delta |
|--------|-------------------|-------------|-------|
| Total issues found | | | |
| Distinct material issues | | | |
| False positives (issues not in revert/advisory) | | | |
| Latency (median) | | | |
| Cost (median) | | | |
| Flakiness (verdict stability %) | N/A | | |

## 19.3 What "winning" looks like

We win if AdversarialDebate surfaces **more distinct material issues** than the single-reviewer baseline on the same artifacts — especially on reverted/advisory PRs where the issue was real.

We lose honestly if:
- Adversarial finds the same issues but slower and more expensive
- Adversarial's distinct issues are rated `noise` by the rater
- Flakiness makes verdicts unreliable on a meaningful % of artifacts

If we lose, the field-test report says so — and the next version's roadmap addresses why.

## 19.4 What we do NOT compare on

- **Total issue count** — vendors inflate this with style nits. We compare distinct *material* issues only.
- **Speed** as a primary axis — debate is slower by design. Speed is reported, not optimized for.
- **Model quality** — both tools use the same model family in the comparison. The variable is the *process*, not the model.
