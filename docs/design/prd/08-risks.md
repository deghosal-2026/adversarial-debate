# 08 — Risks & Mitigations

> Sub-document of the [Design overview](../README.md). What can go wrong — technically, product-wise, as research counter-evidence, and strategically — and the design answer to each.

## 8.1 Product risks

| Risk | Why it's real | Mitigation |
|------|--------------|------------|
| **Fake disagreement (prompt theater)** | Personas told to "be adversarial" perform opposition without reasoning; research shows forced stances produce rhetorical rigidity ([ACL ArgMining 2025](https://aclanthology.org/2025.argmining-1.6/)) | No forced personas, ever. Agents argue their own committed views. Theater-rate metric exposes zero-change debates in reports |
| **Convergence too easy** | Shared model priors + same rubric → both reviewers agree; system degenerates into expensive single review | Heterogeneous pairing encouraged by default; convergence-rate monitoring with healthy bands; rubric design that asks orthogonal questions |
| **Shared blind spots** | Two strong debaters miss the same thing; independence ≠ omniscience | Reports state coverage honestly ("both reviewers missed X" is knowable post-hoc on seeded fixtures); never claim certainty — claim survived-pressure |
| **Disagreement reports accurate but unusable** | Ten unresolved points with hedged positions = noise humans skip | `would_resolve_if` discipline: every unresolved point must name a concrete resolution path; top-N cap; verbosity is a bug tracked in metrics |
| **Token-cost blowout** | Debate multiplies inference 2-4×; teams churn on cost | Bounded rounds, per-artifact budgets, cost tiering (cheap pair → frontier pair only on dispute); selective-debate triggers researched for 0.2+ ([iMAD pattern](https://arxiv.org/abs/2511.11306)) |
| **Isolation leakage** | Framework memory/cache accidentally bridges reviewer contexts | Engine-level session separation; dedicated adversarial tests that attempt leakage and fail loudly; audit log proves separation |
| **Domain-adapter sprawl** | Twenty-seven verticals tempt building 27 normalizers at once | One adapter protocol, one shipping domain until it proves the loop; verticals expand by community pull |
| **Independence may not generalize beyond code** | The thesis depends on adversarial framing working for non-code artifacts where evidence norms, citation standards, and disagreement vocabulary differ radically from software | **Kill criterion:** Tier 1 breadth sweep (see [field-testing strategy](../../field-test/field-testing-strategy.md)) tests this *before* investing in adapters. If >50% of non-code artifacts across ≥5 domains show no measurable independence effect (theater rate ≥80%, distinctness rated low), the vertical thesis is wrong — discovered for the cost of prompts, not code |

## 8.2 Research counter-evidence we design against

| Finding | Our position |
|---------|-------------|
| Debate ≈ majority voting when response counts are equal on some reasoning tasks ([Huang et al. 2023](https://arxiv.org/abs/2311.17371)) | We don't sell raw accuracy on closed-answer tasks. We sell *oversight of open-ended artifacts* — where voting is undefined and argument traces matter ([Khan et al. 2024](https://arxiv.org/html/2407.04622v1) supports debate precisely under information asymmetry) |
| Debate gains saturate after ~2 rounds | Bounded rounds is the default, not a compromise |
| Judges weaker than debaters gain little | The human judge always has artifact context; our reports cite evidence refs so verification is cheap |
| **As models improve and converge, does debate still add value?** | If frontier models converge on reasoning quality, the diversity-of-thought thesis weakens. **Our position:** debate addresses *oversight of open-ended artifacts under information asymmetry* — an AI-safety property, not an accuracy property. As models take higher-stakes actions, the need for independent scrutiny *grows*, whether or not the models agree. The product is the audit trail and the dissent, not the accuracy bump. |

## 8.3 Market risks

| Risk | Mitigation |
|------|------------|
| Code-review incumbents add "debate mode" | They can't easily retrofit mechanical isolation + dissent preservation onto shared-context pipelines; we compete on auditability and BYOM neutrality |
| "Two models = 2× cost" objection | Reframe with the [break-even math](10-business-case.md): one caught miss funds thousands of passes; tiering controls spend |
| OSS project stalls after launch week | Fleet integrations (ToolTrust, EvalForge, PlannerCritic articles) create recurring surface area; adapter roadmap gives contributors clear entry points |
| "This is just two API calls + prompt engineering" | The hard parts are invisible from outside: mechanical isolation enforcement, convergence detection on semantic claims, dissent-preserving synthesis, flakiness control, and the adapter protocol. The [convergence-detection problem](02-architecture.md#27-convergence-detection-the-hardest-design-problem) alone is a research-grade challenge — dismissing the project as prompt engineering is dismissing the existence of the unsolved part. |
