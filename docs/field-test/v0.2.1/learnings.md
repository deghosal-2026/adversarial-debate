# Learnings — v0.2.1

> Documented as issues are discovered during the field test. Updated throughout the M2 execution window.

## Planned

- DeepSeek+GPT pairing results — diversity hypothesis vs Mistral effect
- Row-count invariant effectiveness — any seams where silent loss was caught
- False-negative measurement methodology improvements
- Survivorship boundary documentation
-
- ## Design note: shared RLHF priors (added v0.2.2)
-
- The Mistral effect is confirmed empirically, but the causal mechanism is
- underspecified. Two competing stories:
-
- 1. **Positive mechanism** — Mistral's specific training regime makes it a
-    better debating partner (holds positions, concedes when evidence demands)
- 2. **Negative mechanism** — non-Mistral models share RLHF priors (same
-    instruction-tuning data, same safety alignment targets, same conversational
-    defaults) and rubber-stamp each other; Mistral happens to break the symmetry
-
- The negative mechanism predicts the v0.2.1 separating experiment result:
- DeepSeek+GPT (two labs, no Mistral) converged at 0.246 — statistically
- indistinguishable from homogeneous GPT+GPT at 0.273. Despite being from
- different labs, their safety-alignment approaches produce sufficiently similar
- conversational defaults.
-
- **Implication:** The next experiment should test RLHF-distance vs convergence
- directly, rather than testing more diverse lab combinations. An uncensored
- model vs a strongly safety-aligned one would distinguish the positive from
- the negative mechanism.
-
- Source: Reid Marlow — https://dev.to/reidmarlow/comment/3dmh1