# 11 — Glossary

> Sub-document of the [Design overview](../README.md). Terms used across the PRD, defined once. Contributors start here.

| Term | Definition |
|------|-----------|
| **Artifact** | The thing under review — a PR diff, contract, change request, incident summary. Normalized into a `ReviewArtifact` by a domain adapter. |
| **Reviewer** | An LLM agent that analyzes an artifact independently and commits a structured review. v0.1 ships two per artifact (A and B). |
| **Independent pass** | A reviewer analyzing an artifact without seeing any other reviewer's output. The foundational invariant. |
| **Revelation gate** | The engine state transition `isolated → revealed`. Before this gate, reviewers cannot see each other's conclusions. After, debate begins. Enforced mechanically, not prompted. |
| **Claim** | A structured assertion made by a reviewer about the artifact — has text, severity, evidence refs, and a status lifecycle (`open → conceded | upheld | resolved`). |
| **Objection** | A structured challenge from one reviewer targeting a specific claim from the other — has an argument, round number, and evidence refs. |
| **Concession** | A reviewer formally withdrawing or modifying a claim in response to an objection. A new event in the audit log, not an edit to the original claim. |
| **UnresolvedPoint** | A disagreement that survives all debate rounds — has both positions (`position_a`, `position_b`) and a `would_resolve_if` field naming what would close it. |
| **Would_resolve_if** | The concrete action, evidence, or test that would resolve an unresolved point. The most important field in a disagreement report — without it, dissent is noise. |
| **Convergence** | The state where no `open` claims remain at debate end. Measured as `resolved_claims / total_claims`. |
| **Convergence score** | The ratio above, displayed in every report alongside the verdict. Never hidden. |
| **Theater** | A debate where zero claims changed state — no concessions, no new objections, no evidence shifts. Flagged in reports. High theater rate = broken prompts/rubrics. |
| **Joint Verdict** | The output when reviewers converge — a decision plus the strongest surviving arguments from each side. |
| **Disagreement Report** | The output when reviewers do NOT converge — `resolved[]`, `unresolved[].position_a/position_b/would_resolve_if`. The differentiated product. |
| **Adapter** | A domain-specific module (normalizer + rubric + evidence expectations) that converts a domain artifact into `ReviewArtifact`. Ships in `adversarial_debate/adapters/<domain>/`. |
| **BYOM** | Bring-your-own-model. The engine sells no model; reviewers run on user-configured providers. |
| **Heterogeneous pair** | Two reviewers from different model families. Encouraged by default — produces measurably stronger diversity of thought. |
| **Homogeneous pair** | Two reviewers from the same model family. Supported but weaker for independence; surfaced honestly in reports. |
| **Flakiness** | Run-to-run verdict instability. Measured by N≥5 seed-controlled runs. Artifacts where verdict flips >20% of runs are flagged flaky. |
| **Bifurcated metric** | The split measurement regime: ground-truth domains use binary (bug-caught?); expert-rated domains use the triad (distinctness, actionability, decision-impact). |
| **Expert-rater triad** | The three ratings for non-ground-truth domains: (1) distinctness — materially different from single pass? (2) `would_resolve_if` actionability — could I act on this? (3) decision impact — would this have changed my call? |
| **Tier (0-3)** | Field-test tier: 0 = code with ground truth, 1 = breadth sweep with generic normalizer, 2 = deep on one vertical, 3 = partner-gated regulated. See [field-testing strategy](../../field-test/field-testing-strategy.md). |
