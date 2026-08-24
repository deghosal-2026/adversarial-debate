# 12 — Design Decisions

> Sub-document of the [Design overview](../README.md). Decision records capturing *why* specific choices were made. Contributors read this before proposing changes to established decisions.

## DD-01: Default 2 debate rounds, not 3 or 5

**Decision:** Default round cap = 2. Configurable up to 5.

**Why:** Research shows debate gains saturate after ~2 rounds ([Kenton et al. 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/899511e37a8e01e1bd6f6f1d377cc250-Paper-Conference.pdf) — "number of turns (1 vs 3): no significant difference"). More rounds multiply token cost without measurable quality gain. 2 rounds gives each reviewer one rebuttal pass after revelation — enough to concede, hold, or raise new objections.

**Revisit if:** field tests show material issues surfacing only in round 3+ on a meaningful % of artifacts.

## DD-02: No forced personas — agents argue their own committed views

**Decision:** Reviewers are never told "be the skeptic" or "argue against." They analyze independently and argue what they actually concluded.

**Why:** Forced stances produce rhetorical rigidity, not truth ([ACL ArgMining 2025](https://aclanthology.org/2025.argmining-1.6/) — "forcing models to defend assigned stances degrades performance"). Independence comes from context separation, not role assignment. A reviewer told to disagree performs disagreement; a reviewer who genuinely concluded differently produces real disagreement.

**Revisit if:** never. This is a founding principle.

## DD-03: SQLite for v0.1, not Postgres

**Decision:** SQLite is the default and only storage backend for v0.1.0. Postgres-ready interface designed but not implemented.

**Why:** v0.1 proves the loop on single-machine workflows (CLI, local CI). SQLite is zero-config, file-portable, and sufficient for transcript persistence. Postgres adds operational overhead (connection management, migrations, deployment) that buys nothing until multi-user or fleet-scale scenarios exist. The store interface is pluggable — Postgres is a config change, not a rewrite.

**Revisit at:** v0.3 (N-agent mode, fleet-scale validation) or when a user needs concurrent multi-process access.

## DD-04: Heterogeneous pairs encouraged by default

**Decision:** Default configuration encourages two different model families. Same-model-twice mode is supported but flagged in reports.

**Why:** Diversity of thought is the empirical driver — heterogeneous debate beats homogeneous ([Mila 2025](https://www.alphaxiv.org/overview/2410.12853v2): 91% GSM-8K via architectural diversity). Same-model pairs share training-data priors and failure modes, weakening the independence that is the entire point. Reports must state the pairing so buyers can calibrate trust.

**Revisit if:** a single model family becomes provably self-correcting across all artifact types (unlikely; would collapse the thesis).

## DD-05: MIT license, not AGPL or source-available

**Decision:** MIT, forever. Engine, CLI, all adapters.

**Why:** The fleet standard (all 7 shipped repos are MIT). Enterprise buyers can deploy internally without GPL-style disclosure concerns — critical for the BYOM / self-hosted deployment model. AGPL would block the exact regulated buyers (healthcare, finance, legal) who need on-prem deployment most. The moat is execution and adoption, not license lock-in.

**Revisit if:** never. This is a fleet-level decision.

## DD-06: Disagreement reports are a first-class output, not a fallback

**Decision:** The Disagreement Report is not an error state or a "couldn't decide" fallback. It is a primary product output with equal standing to the Joint Verdict.

**Why:** The most valuable result of adversarial review is often *where uncertainty lives*, not a forced answer. Collapsing dissent into a synthetic verdict throws away the signal humans need most. Reports include `would_resolve_if` — the actionable path forward — making disagreement a decision aid, not a dead end.

**Revisit if:** never. This is a founding principle.

## DD-07: Reviewers get no tool access in v0.1

**Decision:** Reviewers reason over the artifact only. No web search, no code execution, no API calls.

**Why:** Tool access introduces prompt-injection attack surface (artifact text steering a reviewer to fetch a crafted URL) and complicates the isolation invariant (tool state could bridge contexts). v0.1 proves the reasoning loop; tool-augmented reviewers are a v0.3+ research direction, gated behind ToolTrust integration for safety.

**Revisit at:** v0.3, with ToolTrust gating on every tool call.

## DD-08: Convergence is claim-state-based, not semantic-similarity-based

**Decision:** Convergence = no `open` claims remain. Not: "two reviews say similar things."

**Why:** Semantic similarity of natural language is unreliable, expensive, and gameable (a reviewer could paraphrase the other's conclusion without agreeing). Claim-state tracking is mechanical, auditable, and honest — a claim is resolved when the objecting party concedes or the target is modified, not when text looks similar. The limitation (concession-theater) is addressed by the theater-rate metric, not by fancier similarity.

**Revisit if:** a reliable, cheap semantic-equivalence method emerges that adds value beyond state tracking.
