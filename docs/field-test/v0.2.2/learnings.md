# Learnings — v0.2.2

> Documented as issues are discovered during the field test. Updated throughout the M1-M2 execution window.

## Design note: shared RLHF priors — [Reid Marlow](https://dev.to/reidmarlow/comment/3dmh1) ([#166](https://github.com/deghosal-2026/adversarial-debate/issues/166))

The Mistral effect is confirmed empirically, but the causal mechanism is underspecified. Two competing stories:

1. **Positive mechanism** — Mistral's specific training regime makes it a better debating partner (holds positions, concedes when evidence demands)
2. **Negative mechanism** — non-Mistral models share RLHF priors (same instruction-tuning data, same safety alignment targets, same conversational defaults) and rubber-stamp each other; Mistral happens to break the symmetry

The negative mechanism predicts the v0.2.1 separating experiment result: DeepSeek+GPT (two different labs, no Mistral) converged at 0.246 — statistically indistinguishable from homogeneous GPT+GPT at 0.273. Despite being from different labs, their safety-alignment approaches produce sufficiently similar conversational defaults.

**Implication:** The next experiment should test RLHF-distance vs convergence directly, rather than testing more diverse lab combinations. An uncensored model vs a strongly safety-aligned one would distinguish the positive from the negative mechanism.

Source: Reid Marlow — https://dev.to/reidmarlow/comment/3dmh1

## Noise-floor baseline — [Bert Shim](https://dev.to/bert_programmer/comment/3dmi0) ([#165](https://github.com/deghosal-2026/adversarial-debate/issues/165))

The convergence score for pair3_gpt_mistral (n=150) has a bootstrap standard deviation of ±0.020. The gap between GPT+Mistral (0.536) and DeepSeek+Mistral (0.572) is 0.036 — roughly 1.8 standard deviations. This means the gap is real but narrow.

Key finding: pairs with fewer debates (homogeneous_gpt, n=7) have noise floors wide enough to make any single-run comparison unreliable. The 95% CI for homogeneous_gpt is 0.129–0.432.

Source: Bert Shim — https://dev.to/bert_programmer/comment/3dmi0

## LLM-as-Judge permutation control — [Vinh Nguyen](https://dev.to/vinhnguyenthanhdn/comment/3dmh4) ([#164](https://github.com/deghosal-2026/adversarial-debate/issues/164))

The LLM judge's 87.4% match rate sits 77.8 standard deviations above the null distribution (vocabulary floor = 0.3%). The matcher is discriminating well — vocabulary alone does not explain the result.

The deterministic proxy (Jaccard similarity) significantly underestimates the LLM's match rate (7.2% vs 87.4% real), so the null floor is a lower bound. A full LLM-based permutation control would require ~1.72M LLM calls — cost-prohibitive.

Source: Vinh Nguyen — https://dev.to/vinhnguyenthanhdn/comment/3dmh4