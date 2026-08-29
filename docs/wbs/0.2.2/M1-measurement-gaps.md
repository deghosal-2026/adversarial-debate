# WBS — AdversarialDebate v0.2.2-M1: Measurement Gaps 🔄 In progress

> Part of the v0.2.2 release. See [index](index.md) for milestone overview.
>
> **Branch:** `feature-v0.2.2` · **Milestone:** [v0.2.2-M1](https://github.com/deghosal-2026/adversarial-debate/milestone/15)
>
> **Status:** 🔄 In progress
>
> **Scope:** Three community-raised measurement gaps. All changes are post-hoc analysis on existing artifacts — no new debates, no field test sweep.

## Overview

M1 addresses three gaps identified by readers after the v0.2.1 release. None require new LLM calls or new debate runs — each is a measurement or documentation change on existing data.

## #164 — LLM-as-Judge Permutation Control

**Source:** Vinh Nguyen ([dev.to comment](https://dev.to/vinhnguyenthanhdn/comment/3dmh4))

**Problem:** 0 NO_MATCH across 7,612 claims in v0.1.0 and 3,440 claims in v0.2.1 is suspicious. A matcher that never fires its negative verdict may be measuring its own leniency rather than the debates' accuracy. The null is not zero — claims from the same repo share vocabulary (file paths, identifiers, issue idioms), so the permuted rate has a corpus-specific floor.

**Changes:**
- Add `--permutation-control` flag to `07_llm_judge.py`
- Shuffle claim-to-ground-truth pairings: for each claim, assign a revert reason from a different PR
- Run N >= 100 shuffles to build a stable null distribution
- Report null mean ± std as the corpus-specific vocabulary floor
- Report real match rate as a z-score or percentile above that floor
- Include result in field test report as matcher quality metric

**Acceptance criteria:**
- [ ] `--permutation-control` flag added to `07_llm_judge.py`
- [ ] N >= 100 shuffles for stable null distribution
- [ ] Null distribution (mean, std, histogram) reported alongside real match rate
- [ ] Real match rate reported as distance from null (z-score or percentile)
- [ ] Documentation: "a residual of ~40% is the corpus floor, not a failed control"
- [ ] Existing ground-truth CSV format unchanged

## #165 — Metric Noise-Floor Baseline

**Source:** Bert Shim ([dev.to comment](https://dev.to/bert_programmer/comment/3dmi0))

**Problem:** No core metric has ever been measured for baseline variance under identical conditions. A shift from 0.536 to 0.572 could be signal or instrument noise. Bert's story — "I read the same value four times in four seconds: 124, 121, 119, 123" — is the exact failure class.

**Changes:**
- Create noise-floor measurement script: runs a single pair against a pinned artifact subset N times
- Record per-run values for: average convergence score, verdict rate, capitulation rate, concession count, theater count
- Report mean, standard deviation, and 95% CI per metric
- Commit baseline run artifacts for future drift detection

**Acceptance criteria:**
- [ ] Noise-floor measurement script created
- [ ] Single pair run against pinned 10–20 artifact subset, N >= 10 times
- [ ] Per-metric table: mean, std, 95% CI under identical conditions
- [ ] Baseline run artifacts committed to repo
- [ ] Zero LLM calls (uses existing stored results)

## #166 — Shared RLHF Priors Design Note

**Source:** Reid Marlow ([dev.to comment](https://dev.to/reidmarlow/comment/3dmh1))

**Problem:** The Mistral effect is confirmed empirically, but the causal mechanism is underspecified. Two competing stories: (a) Mistral is positively good at debate, or (b) non-Mistral models share RLHF priors and rubber-stamp each other. The negative mechanism — "nominal lab diversity can mask shared conversational defaults" — has never been formally captured.

**Changes:**
- Add design note to learnings log: shared RLHF priors mechanism
- Distinguish positive (Mistral-specific) from negative (shared-prior) causal stories
- Suggest next experiment: RLHF-distance vs convergence correlation

**Acceptance criteria:**
- [ ] Design note added to learnings log
- [ ] Causal mechanism explicitly distinguished from positive Mistral-effect story
- [ ] Next experiment suggestion: RLHF-distance vs convergence

## Issue Summary

| Issue | Title | Type | Status |
|-------|-------|------|--------|
| #164 | [v0.2.2-M1] LLM-as-Judge Permutation Control | Code change + analysis | 🔄 Open |
| #165 | [v0.2.2-M1] Metric noise-floor baseline | Code change + analysis | 🔄 Open |
| #166 | [v0.2.2-M1] Design note: shared RLHF priors | Documentation | 🔄 Open |

## Exit gate

- [ ] All 3 issues closed
- [ ] All changes use existing stored data — zero new LLM calls
- [ ] Ruff clean, mypy strict clean
- [ ] Full existing test suite green
- [ ] Code review completed
- [ ] Merged to `feature-v0.2.2`