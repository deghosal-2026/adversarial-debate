# Design — AdversarialDebate

> This README is the **overview and index** for the product requirements (the `prd/` sub-docs), plus future design decisions and scenario designs. Start here.

**Version:** 0.1 (Seed)
**Date:** 2026-08-23
**Owner:** Debashish Ghosal
**Repo:** `deghosal-2026/adversarial-debate` (private → OSS at ship)
**Package:** `adversarial-debate` / import `adversarial_debate` / CLI `advdeb` *(proposed)*

---

## Executive Summary

AdversarialDebate is a **multi-agent adversarial review engine**. Two independent LLM reviewers analyze the same artifact — PR diff, design doc, incident summary, rollout plan — **without seeing each other's answers**. Only after both have committed their reviews does the revelation gate open. Each reviewer then responds point-by-point to the other's claims in bounded debate rounds. The engine produces either a **converged joint decision** with the strongest surviving arguments from both sides, or a **structured disagreement report** that preserves the dissent: what is disputed, why, what evidence matters, and what would resolve it.

The insight that justifies the project: **most AI second opinions are fake because the second model sees the first answer before it has reasoned independently.** That setup biases the result toward agreement — it is review-shaped agreement, not review. The most expensive agent failures are rarely missing information; they are prematurely accepted reasoning. AdversarialDebate separates the independent pass from the interaction pass so conclusions survive real adversarial pressure.

**Core architectural principle:** independence is enforced mechanically, not prompted. Context separation and delayed revelation are engine-level invariants; debate quality is tracked as evidence shifts, concessions, and unresolved points — not rhetorical confidence.

## Scope Snapshot (draft, to be locked at AD-M1)

- **Delivery surfaces:** Python library + CLI; FastAPI service + React side-by-side review UI
- **Isolation:** strict context separation per reviewer; revelation only after both commit; provable via transcript audit
- **Debate:** bounded rounds (default 2-3); mandatory point-by-point response; claims/objections/concessions schema
- **Synthesis:** convergence detection → joint verdict or disagreement report (`verdict`, `resolved`, `unresolved[].would_resolve_if`)
- **Domains:** PR review first; architecture review + incident hypothesis adapters later
- **Storage:** SQLite for transcripts, debate state, evidence objects
- **Providers:** model-agnostic (PydanticAI, LangGraph, raw API); heterogeneous models encouraged for diversity of thought

## Documents

| Document | Status |
|----------|--------|
| [prd/](prd/) | Sub-docs authored next (AD-M1) |
| `design-decisions.md` | Authored inline as implementation reveals decisions |
