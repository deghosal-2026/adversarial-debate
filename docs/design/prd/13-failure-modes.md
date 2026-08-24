# 13 — Debate-Quality Failure-Mode Catalog

> Sub-document of the [Design overview](../README.md). What a *bad* debate looks like — so users can calibrate trust and contributors can recognize bugs. Each failure mode has a signature, a detection signal, and a mitigation.

## 13.1 Why this catalog exists

A buyer who sees a Disagreement Report asks: *"Is this real disagreement or is the engine broken?"* This catalog names the ways debate goes wrong, how each manifests in the transcript, and what the engine does about it. If a failure mode isn't here, it's a bug — report it.

## 13.2 Failure modes

| # | Failure mode | Signature in transcript | Detection signal | Mitigation |
|---|-------------|------------------------|-------------------|------------|
| FM-1 | **Shared hallucination** | Both reviewers cite the same non-existent evidence (a function that doesn't exist, a clause that isn't in the contract) | Evidence refs validated against artifact content; hallucinated refs flagged in report | Heterogeneous pairing reduces shared priors; report states "evidence not found in artifact" warnings |
| FM-2 | **Capitulation cascade** | One reviewer concedes every objection in round 1 without argument; debate ends converged in <30 seconds | Concession rate >80% in round 1 with zero rebuttals | Flagged as theater; report shows concession pattern; user warned "reviewer B capitulated — convergence may be unreliable" |
| FM-3 | **Loop on one point** | Same claim objected to, rebutted, re-objected across all rounds; other claims never debated | Single claim consumes >60% of debate messages | Round cap forces termination; unresolved point reported with `would_resolve_if`; other claims marked "undebated — round limit reached" |
| FM-4 | **Rubric mismatch** | Reviewers argue about what the rubric *means* rather than the artifact | Objections target the rubric, not the artifact content | Adapter rubric version stamped in transcript; mismatch between expected and actual rubric surfaced as config error |
| FM-5 | **Verbose non-disagreement** | Reviewers produce long reviews that say the same thing differently; "disagreement" is stylistic, not substantive | High token spend, zero claim-state changes, high semantic overlap | Theater-rate metric flags it; report shows "both reviewers reached equivalent conclusions via different paths" |
| FM-6 | **Asymmetric effort** | Reviewer A produces 15 claims; Reviewer B produces 2 generic ones | Claim count delta >5:1 | Report states claim counts per reviewer; sparse review flagged; user can configure minimum-claim threshold |
| FM-7 | **Confidence without evidence** | Reviewer assigns high severity to a claim with zero evidence refs | Claims with `severity == high` and `evidence_refs == []` | Validation layer rejects evidence-less high-severity claims; reviewer must either cite evidence or downgrade severity |
| FM-8 | **Revelation contamination** | Reviewer B's round-1 response suspiciously mirrors A's pre-revelation claims | B's post-revelation claims contain A's pre-revelation phrasing/priorities | Isolation invariant tests in CI; audit log proves session separation; if detected in production, filed as critical bug |
| FM-9 | **Model degradation mid-debate** | One reviewer's round-2 quality drops sharply (truncation, repetition, refusal) | Response length / coherence metrics drop between rounds | Engine detects degradation (repetition, truncation); flags round as `degraded`; user can resume with different model |
| FM-10 | **Domain adapter hallucination** | PR-review adapter invents metadata (claims a file was modified when it wasn't) | Normalizer output validated against actual artifact content | Adapter tests in CI against real diffs; hallucinated metadata fails validation before review begins |

## 13.3 How users use this catalog

1. **Before trusting a report:** check the failure-mode flags in the report header (theater flag, concession pattern, evidence-validation warnings, claim-count balance).
2. **When debugging a bad result:** match the transcript against the signatures above to identify which failure mode fired.
3. **When contributing an adapter:** test against FM-4 (rubric mismatch) and FM-10 (adapter hallucination) — the two domain-specific failure modes.

## 13.4 What's NOT a failure mode

- **Genuine disagreement that survives debate** — that's the product, not a bug. The Disagreement Report is the correct output.
- **One reviewer being wrong** — if the debate surfaced it and the report shows the resolution path, the system worked.
- **Convergence** — convergence is not failure. Forced convergence is. The theater-rate metric distinguishes them.
