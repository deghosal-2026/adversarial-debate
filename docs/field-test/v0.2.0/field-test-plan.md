# Field Test Plan — v0.2.0 "Fix the Data"

> **Status:** Draft · **Version:** 0.2.0 · **Window:** Aug 28-31, 2026
> **Owner:** Deb Ghosal · **Milestone:** [M7 — Field Test Rerun](../../wbs/0.2.0/M7-field-test-rerun.md)
>
> This plan copies the v0.1.0 field-test plan structure, but updates the scope for v0.2.0: correct the data-integrity failures found in v0.1.0, re-run the PR corpus on a cleaner basis, and extend the field test into three adjacent non-code domains that stress the same independence and dissent-preservation thesis.

---

## 1. Objective

Prove two things after the v0.1.0 postmortem fixes are complete:

| # | Question | How answered |
|---|----------|-------------|
| Q1 | **Did M1-M6 actually fix the field-test integrity problems?** | Re-run all measurement pipelines with corrected engine/scripts and verify no zero-claim artifacts, no corpus/prose mismatches, and no overlap/report inconsistencies |
| Q2 | **Does the independence invariant generalize beyond PR review?** | Run a mixed 150-artifact corpus across PR review, incident response, change management, and security incidents |
| Q3 | **Does adversarial debate add value where outcome truth is mixed?** | Use bifurcated scoring: ground-truth validation for PRs, expert-rated usefulness for non-code artifacts |
| Q4 | **Are the results stable enough to publish honestly?** | Run a seed-controlled flakiness sweep on representative artifacts from each domain |

v0.2.0 is a **rerun plus breadth extension**. It is not just a bigger corpus. The point is to verify that the corrected engine and analysis pipeline produce trustworthy results, and then test whether the debate mechanism still produces useful, non-theatrical disagreement outside code review.

---

## 2. Scope Lock (v0.2.0)

This field test covers **4 domains, 150 total artifacts**:

| Domain | Count | Measurement mode | Why included |
|--------|-------|------------------|--------------|
| **PR review** | 80 | Ground truth + baseline comparison | Continuity with v0.1.0 and strongest falsifiable signal |
| **Incident response** | 30 | Outcome-informed + expert-rated | Public postmortems expose competing hypotheses and remediation sufficiency |
| **Change management** | 20 | Expert-rated with partial outcomes where available | Closest non-code analog to PR approval under uncertainty |
| **Security incidents** | 20 | Outcome-informed + expert-rated | High-value test of evidence quality, exploitability, and mitigation reasoning |

**Explicitly in scope:**

- corrected rerun methodology from v0.1.0 postmortem
- mixed-domain corpus with domain tags and measurement-mode tags
- heterogeneous vs homogeneous pair comparison on representative subsets
- full transcript publication for every included artifact
- flakiness, theater, capitulation, overlap, and false-positive analysis where applicable

**Explicitly out of scope:**

- regulated/private domains (healthcare, live contracts, real claims)
- private repos or private incident artifacts
- UI benchmarking or latency-only benchmarking
- claims that non-code domains have binary "ground truth" when they do not

---

## 3. Corpus Selection

### 3.1 Corpus Summary

| Domain | Count | Primary evidence type | Rating mode |
|--------|-------|-----------------------|-------------|
| **PR review** | 80 | Git diff + PR discussion + follow-up outcome | `ground_truth` |
| **Incident response** | 30 | Public incident report + timeline + postmortem | `expert_rated`, outcome-informed |
| **Change management** | 20 | Rollout / migration / change plan + rollback path | `expert_rated` |
| **Security incidents** | 20 | Advisory / patch narrative / incident disclosure | `expert_rated`, outcome-informed |
| **Total** | **150** | | |

### 3.2 PR Review Corpus (80)

Use PRs with meaningful review surface, not trivial typo fixes. Favor artifacts with documented outcomes.

| Bucket | Count | Ground truth | Notes |
|--------|-------|-------------|-------|
| **Merged-then-reverted** | 15 | Yes: revert commit or linked issue | Strongest falsifiable signal |
| **Merged-then-hotfixed / follow-up fix** | 15 | Yes: fix PR references original | Captures latent correctness gaps |
| **Merged-then-security-fix** | 10 | Yes: CVE / GHSA / linked security patch | Security reasoning inside code review |
| **Rejected / closed after substantive review** | 10 | Yes: human review comments | Human-caught issue comparison |
| **Race / concurrency / perf / API breakage** | 10 | Yes: follow-up discussion or issue | Harder reasoning categories |
| **Dependency / CI / config / generated-code risk** | 10 | Yes: CI failure, revert, or fix PR | Non-core-code reasoning |
| **Clean merge controls** | 10 | No known issue | False-positive control |

Target repos for the 80 PRs:

- `kubernetes/kubernetes`
- `django/django`
- `microsoft/vscode`
- `golang/go`
- `rails/rails`
- `vercel/next.js`
- `prometheus/prometheus`
- `rust-lang/rust`

Selection rules:

1. At least 4 languages represented: Go, Python, TypeScript, and one of Rust/Ruby.
2. At least 20 PRs must involve non-trivial config, tests, CI, generated files, or dependency changes.
3. At least 20 PRs must have review threads substantial enough to compare human review vs debate output.
4. Clean-merge controls must be randomly sampled within the same size/purpose buckets as risky PRs.

### 3.3 Incident Response Corpus (30)

Use public incidents with enough technical detail to support point-by-point disagreement.

Target sources:

- Cloudflare incident reports
- GitHub engineering or status postmortems
- Google Cloud incident reports
- AWS post-event summaries where technical detail is sufficient
- Stripe engineering incident writeups
- public SRE incident writeups from large OSS or infrastructure vendors

Suggested subtype mix:

| Bucket | Count | What it tests |
|--------|-------|---------------|
| **Single-root-cause postmortems** | 10 | Whether debate converges when evidence is relatively complete |
| **Multi-factor incidents** | 10 | Whether disagreement surfaces ambiguity instead of fake certainty |
| **Timeline-heavy incident reports** | 5 | Whether agents can reason from chronology and causal chain |
| **Remediation-plan disputes** | 5 | Whether `would_resolve_if` yields useful next steps |

Selection rules:

1. Every artifact must include either a final postmortem or enough timeline detail to reconstruct competing hypotheses.
2. At least 10 incidents must have a clearly stated remediation section.
3. At least 5 incidents must be operationally "clean" controls where the incident analysis appears complete and low-ambiguity.

### 3.4 Change Management Corpus (20)

This is the first non-code domain closest to the product thesis: approval under uncertainty.

Target sources:

- public migration plans in engineering blogs
- architecture / rollout RFCs in OSS repos
- deployment runbooks or release plans with rollback steps
- public incident writeups that include the pre-change plan and the eventual failure
- clearly labeled synthetic CAB-style packets derived from public materials only, if needed to round out the corpus

Suggested subtype mix:

| Bucket | Count | What it tests |
|--------|-------|---------------|
| **Migration / data-move plans** | 6 | Rollback realism, lock/time/race risk |
| **Infra / config rollout plans** | 6 | Blast radius and sequencing |
| **Feature launch / staged rollout plans** | 4 | Guardrails, rollback triggers, observability |
| **Controls (apparently solid plans)** | 4 | False-positive pressure |

Selection rules:

1. Every artifact must contain an intended change, risk statement, and some form of rollback or mitigation path.
2. At least 8 artifacts must have a later outcome signal (postmortem, rollback, successful rollout, or public issue thread).
3. Synthetic artifacts are allowed only when they are explicitly marked and derived from public source material.

### 3.5 Security Incidents Corpus (20)

Use public security artifacts with sufficient technical detail to debate exploitability, scope, and mitigation sufficiency.

Target sources:

- GitHub Security Advisories
- CVE disclosures with patch context
- vendor incident disclosures with root-cause and mitigation detail
- OSS security postmortems
- exploit writeups paired with maintainer remediation notes

Suggested subtype mix:

| Bucket | Count | What it tests |
|--------|-------|---------------|
| **Patch + advisory pairs** | 8 | Can agents connect mitigation to root cause? |
| **Exploitability ambiguity cases** | 4 | Severity disagreement with evidence |
| **Incomplete-disclosure cases** | 4 | Honest dissent under sparse data |
| **Controls / straightforward advisories** | 4 | False-positive pressure in lower-ambiguity cases |

Selection rules:

1. Every artifact must include at least one of: remediation guidance, patch summary, exploit conditions, or affected-version range.
2. At least 8 security artifacts must be paired with a code patch, commit, or advisory update.
3. Artifacts that require private exploit detail are excluded.

### 3.6 Corpus Metadata Schema

Publish the corpus before the first rerun under:

- `results/field-test/v0.2.0/corpus.csv`

Required fields:

- `artifact_id`
- `domain`
- `subtype`
- `source_url`
- `title`
- `measurement_mode` (`ground_truth` | `expert_rated`)
- `outcome_known` (`yes` | `partial` | `no`)
- `control` (`yes` | `no`)
- `expected_disagreement_surface`
- `notes`

PR-only fields:

- `repo`
- `language`
- `lines_changed`
- `purpose`
- `review_depth`
- `documented_outcome`

Non-PR fields:

- `organization`
- `artifact_kind`
- `timeline_available`
- `remediation_available`
- `rater_profile`

### 3.7 Corpus Curation Rules

1. No post-hoc removal of artifacts because the debate result was boring or inconvenient.
2. Every artifact must have a documented reason it belongs in the corpus.
3. Controls must remain in the corpus even if they create false positives.
4. Every non-PR artifact must be clearly tagged as `outcome_known`, `partial`, or `no`.
5. Do not overclaim certainty on narrative-only artifacts.
6. Synthetic change-management artifacts must be labeled in both corpus metadata and final reporting.

---

## 4. Model Pairs

Use the v0.1.0 learnings to avoid rerunning an unnecessary full 4-model matrix. v0.2.0 should use a **2-model primary strategy** for the main corpus, with the other models retained only for targeted control subsets.

### 4.1 Core Models

| Model | OpenRouter ID | Family | Role in v0.2.0 |
|-------|--------------|--------|----------------|
| GPT-4o-mini | `openai/gpt-4o-mini` | OpenAI | stable baseline reviewer |
| Gemini 2.5 Flash | `google/gemini-2.5-flash` | Google | stubborn / contrastive pair member |
| DeepSeek-V3 | `deepseek/deepseek-chat` | DeepSeek | diverse reasoning style |
| Mistral Small 3.2 | `mistralai/mistral-small-3.2-24b-instruct` | Mistral | cheapest heterogeneous partner |

### 4.2 v0.2.0 Model Strategy

Canonical pair roles for v0.2.0:

- **Primary / positive pair:** `pair3_gpt_mistral`
- **Validation pair:** `pair5_deepseek_mistral`
- **Negative control:** `pair1_gpt_gemini`
- **Homogeneous control:** `homogeneous_gpt`

Primary recommendation:

1. Run the full `150`-artifact corpus on **GPT-4o-mini + Mistral Small 3.2**.
2. Use **DeepSeek-V3 + Mistral Small 3.2** only on a representative validation subset.
3. Use **GPT-4o-mini + Gemini 2.5 Flash** only as an optional negative-control subset if we want to confirm the v0.1.0 stubborn-pair result.

Why this is the default:

- `pair3_gpt_mistral` looked like the most balanced heterogeneous pair in v0.1.0.
- `pair5_deepseek_mistral` was very strong, but often over-converged through capitulation.
- `pair1_gpt_gemini` was informative mainly as a negative control, not as a productive default pair.
- v0.2.0 is primarily a data-integrity rerun plus domain extension, not another broad model bake-off.

#### Why not run all 4 models on the full v0.2.0 corpus?

Because the central model-selection question was already answered well enough in v0.1.0.

v0.1.0 established four useful facts:

1. Model diversity matters.
2. `GPT + Gemini` is a weak default pair and behaves best as a negative control.
3. `DeepSeek + Mistral` can be very productive, but its high convergence rate is partly inflated by capitulation cascades.
4. `GPT + Mistral` is the best candidate for a balanced default rerun pair.

Given those learnings, a full 4-model matrix in v0.2.0 would mostly repeat known pair-ranking behavior while multiplying run count, analysis burden, and opportunities for report inconsistency. The purpose of v0.2.0 is to verify the corrected pipeline and extend into new domains with honest measurement, not to spend most of the budget rediscovering the same pair ordering.

The leaner design has three advantages:

- **Cleaner interpretation:** most result changes can be attributed to corpus/domain differences or M1-M6 fixes, not a sprawling pair matrix.
- **Lower operational risk:** fewer runs means fewer rate-limit, bookkeeping, and reporting opportunities for error.
- **Better comparison discipline:** subset controls are enough to check whether the old pair-level lessons still hold without letting model-comparison work dominate the milestone.

### 4.3 Debate Pairs

| Pair | Slot A | Slot B | Why retained |
|------|--------|--------|--------------|
| `pair1_gpt_gemini` | GPT-4o-mini | Gemini 2.5 Flash | negative control from v0.1.0 |
| `pair3_gpt_mistral` | GPT-4o-mini | Mistral Small 3.2 | balanced heterogeneous pair |
| `pair5_deepseek_mistral` | DeepSeek-V3 | Mistral Small 3.2 | strongest v0.1.0 performer |
| `homogeneous_gpt` | GPT-4o-mini | GPT-4o-mini | homogeneous control |

Recommended run shape:

- run all 150 artifacts on `pair3_gpt_mistral`
- run a 30-40 artifact representative validation subset on `pair5_deepseek_mistral`
- optionally run a 20-30 artifact negative-control subset on `pair1_gpt_gemini`
- run a 30-40 artifact representative control subset on `homogeneous_gpt`

This preserves continuity with the v0.1.0 pair findings without wasting calls on the least informative combinations.

### 4.4 Baseline Comparison

Use a single-reviewer baseline on:

- all 80 PR artifacts
- a 20-artifact stratified sample from the non-PR domains

The baseline is still most meaningful on PR review, but a smaller non-PR baseline sample helps distinguish "debate adds nothing" from "the domain itself is vague."

---

## 5. Configuration

### 5.1 Standard Invocation Pattern

```bash
advdeb review --pr <url> --rounds 2 --pair pair3_gpt_mistral
```

For non-PR domains, use the corresponding artifact loader or normalized input path once the M1-M6 adapter fixes land. The important invariants remain:

- 2-round default unless a saturation check says otherwise
- all transcripts exported
- seeds recorded in metadata
- per-run content hash preserved

### 5.2 Seed Strategy

- primary run: `seed=42`
- flakiness sweep: `seed in [42, 43, 44, 45, 46]`
- homogeneous and negative-control subsets: `seed=42`

### 5.3 Budget

- default budget: 50,000 tokens per artifact
- large or timeline-heavy artifacts: 100,000 tokens
- budget exhaustion is valid data, but must be marked and excluded from any claim of successful convergence

---

## 6. Execution Plan

### 6.1 Phase 1 — Corpus Assembly

| Task | Output |
|------|--------|
| Assemble 80 PR artifacts | PR rows in `corpus.csv` |
| Assemble 30 incident-response artifacts | incident rows in `corpus.csv` |
| Assemble 20 change-management artifacts | change rows in `corpus.csv` |
| Assemble 20 security-incident artifacts | security rows in `corpus.csv` |
| Freeze and commit corpus before first rerun | committed `corpus.csv` |

### 6.2 Phase 2 — Baseline Runs

| Task | Details |
|------|---------|
| Run single-reviewer baseline on 80 PRs | same artifact set as debate runs |
| Run single-reviewer baseline on 20 non-PR sample artifacts | stratified across the 3 non-code domains |
| Store outputs under baseline directory | one result per artifact |

### 6.3 Phase 3 — Debate Rerun

| Task | Details |
|------|---------|
| Run primary sweep on `pair3_gpt_mistral` | all 150 artifacts |
| Run validation sweep on `pair5_deepseek_mistral` | 30-40 artifact sample |
| Run optional negative control on `pair1_gpt_gemini` | 20-30 artifact sample |
| Run homogeneous control on `homogeneous_gpt` | 30-40 artifact sample |
| Export transcripts and metadata for every run | transcript + report + metadata |

### 6.4 Phase 4 — Flakiness Sweep

| Task | Details |
|------|---------|
| Select 5 PRs, 3 incidents, 2 change artifacts, 2 security artifacts | 12-artifact representative sweep |
| Re-run each artifact N=5 seeds on primary pair(s) | stability analysis |
| Flag verdict flips, missing runs, and degraded rounds | flakiness report |

### 6.5 Phase 5 — Analysis

| Step | What |
|------|------|
| 1 | Verify no zero-claim no-op artifacts remain |
| 2 | Verify prose metrics derive from CSV/JSON outputs, not manual math |
| 3 | Compute theater, capitulation, convergence, and degraded-round rates |
| 4 | Compute PR distinct-issue yield vs ground truth |
| 5 | Compute PR false-positive / false-negative rates on controls and known-outcome buckets |
| 6 | Rate non-PR artifacts on distinctness, `would_resolve_if` actionability, and decision impact |
| 7 | Compare heterogeneous, homogeneous, and negative-control pair behavior |
| 8 | Measure overlap consistency using corrected extraction rules |
| 9 | Produce per-domain failure-mode catalog |
| 10 | Break down cost and latency per domain and pair |

### 6.6 Phase 6 — Report

Write:

- `docs/field-test/v0.2.0/FIELD_TEST_REPORT_full_corpus.md`
- `docs/field-test/v0.2.0/FIELD_TEST_REPORT_small_corpus.md`

The small corpus should be a representative smoke subset, not an entirely different methodology.

---

## 7. Success Criteria

### 7.1 Data-Integrity Gate

These are hard requirements for publishing the v0.2.0 results:

1. No zero-claim or no-op artifacts counted as successful debates.
2. Report prose must match generated CSV/JSON metrics.
3. Overlap statistics must be self-consistent and derived from the corrected extraction pipeline.
4. MATCH / false-positive / false-negative claims must clearly state the population they were measured on.

### 7.2 PR-Domain Gate

For the 80 PRs:

1. At least one artifact must again satisfy the binary bar: materially distinct issue confirmed by known outcome.
2. Distinct-issue yield must be reported against the single-reviewer baseline.
3. False positives on clean controls must be explicitly reported.
4. Results must exclude artifacts where the engine or analysis pipeline failed integrity checks.

### 7.3 Non-PR Domain Gate

For incident response, change management, and security incidents:

1. At least 50% of artifacts in each domain should show a non-theatrical debate.
2. At least 50% of unresolved points should have `would_resolve_if` rated actionable or directionally useful.
3. At least one artifact per domain should demonstrate preserved dissent that a rater judges decision-changing or materially clarifying.

### 7.4 Secondary Metrics

| Metric | Target |
|--------|--------|
| Theater rate | < 20% overall |
| Capitulation cascade rate | reported, not hidden |
| Convergence rate | domain-specific, not a universal success gate |
| Verdict stability | > 80% on flakiness subset |
| Heterogeneous vs homogeneous delta | positive on at least one primary metric |
| Cost per artifact | reported by pair and domain |

### 7.5 Model-Selection Gate

v0.2.0 is successful if the main conclusions can be supported from the **2-model primary strategy** plus subset controls. We do not need to repeat a full 4-model matrix unless the rerun reveals that pair ranking materially changed after the M1-M6 fixes.

---

## 8. Measurement Methodology

### 8.1 Bifurcated Measurement

Use two regimes and never blur them:

| Domain type | Primary method |
|-------------|----------------|
| **PR review** | Ground-truth validation + baseline comparison |
| **Incident / change / security narrative artifacts** | Expert-rated usefulness, optionally outcome-informed |

### 8.2 Expert-Rated Triad

For non-PR artifacts, each debate is rated on:

1. **Distinctness** — did the second side surface a materially different concern or interpretation?
2. **Actionability** — is the `would_resolve_if` path specific enough to act on?
3. **Decision impact** — would this disagreement have changed or delayed your approval / conclusion?

### 8.3 Controls

Each domain must include controls to measure false-positive pressure:

- PR clean merges
- low-ambiguity incident postmortems
- apparently solid change plans
- straightforward security advisories

### 8.4 Honest Constraints

1. Non-PR artifacts often do not have binary truth.
2. Narrative domains can support useful disagreement even when they do not support hard pass/fail claims.
3. Synthetic change packets are acceptable only if clearly labeled and not mixed silently with public real artifacts.

---

## 9. Artifact Layout

All v0.2.0 artifacts live under:

```text
docs/field-test/v0.2.0/
|-- field-test-plan.md
|-- corpus.csv
|-- baseline/
|   |-- <artifact-id>.json
|-- sweep/
|   |-- primary/
|   |-- controls/
|   |-- flakiness/
|   |-- small-corpus/
|-- analysis/
|   |-- domain-summary.csv
|   |-- pr-ground-truth.csv
|   |-- non-pr-ratings.csv
|   |-- overlap.csv
|   |-- failure-modes.csv
|   |-- cost-latency.csv
|-- FIELD_TEST_REPORT_full_corpus.md
```

Execution outputs live under:

```text
results/field-test/v0.2.0/
|-- corpus/
|-- debates/
|-- analysis/
|-- flakiness/
```

---

## 10. Proposed Corpus Quality Bar

This corpus is only worth running if it contains artifacts with real disagreement surface.

Use these heuristics while selecting the 150 artifacts:

1. Prefer artifacts where a smart reviewer could plausibly disagree with another smart reviewer.
2. Avoid tiny or ceremonial artifacts unless they are explicit controls.
3. Prefer sources with follow-up evidence, remediation text, or review discussion.
4. Keep a balanced mix of easy, ambiguous, and adversarial cases.
5. Do not overweight a single vendor or repo family.

---

## 11. Exit Gate Checklist

- [ ] `docs/field-test/v0.2.0/corpus.csv` committed before first rerun
- [ ] 80 PR artifacts selected and tagged
- [ ] 30 incident-response artifacts selected and tagged
- [ ] 20 change-management artifacts selected and tagged
- [ ] 20 security-incident artifacts selected and tagged
- [ ] Baseline runs complete on all PRs and sampled non-PR artifacts
- [ ] Primary sweeps complete on retained heterogeneous pairs
- [ ] Negative-control and homogeneous-control subsets complete
- [ ] Flakiness sweep complete on representative cross-domain subset
- [ ] Zero-claim / no-op artifacts excluded from results
- [ ] PR ground-truth evaluation complete
- [ ] Non-PR expert ratings complete
- [ ] Report prose derived from generated metrics and cross-checked
- [ ] `FIELD_TEST_REPORT_full_corpus.md` written
- [ ] `FIELD_TEST_REPORT_small_corpus.md` written

---

## 12. References

| Document | Relevance |
|----------|-----------|
| [v0.1.0 field-test plan](../v0.1.0/field-test-plan.md) | structural source for this copied-and-revised plan |
| [field-testing strategy](../field-testing-strategy.md) | mixed-domain measurement model |
| [M7 — Field Test Rerun](../../wbs/0.2.0/M7-field-test-rerun.md) | milestone alignment |
| [WBS v0.2.0 index](../../wbs/0.2.0/index.md) | release sequence and dependencies |

---

## 13. Corpus Sourcing Notes

### 13.1 PR Corpus Reuse

For the `80` PR mix, start by reusing the `v0.1.0` corpus we already have before collecting new artifacts.

Recommended approach:

1. Treat `results/field-test/v0.1.0/corpus.csv`, `corpus0.csv`, and `corpus1.csv` as the first candidate pool.
2. Keep only PRs whose metadata and outcome labels still hold after the v0.2.0 integrity fixes.
3. Re-tag reused PRs with the v0.2.0 corpus schema so the new analysis pipeline does not inherit old assumptions silently.
4. Fill the remaining gaps only where the old corpus is weak: language coverage, control quality, review-depth coverage, and non-code-risk categories such as config, dependency, and CI changes.

This reuse-first approach also matches the v0.2.0 model strategy: because the main corpus runs on a single primary pair (`pair3_gpt_mistral`) rather than a full 4-model matrix, the highest-value PR selection work is improving corpus quality and coverage, not recollecting an entirely new PR set just to feed redundant pair comparisons.

This gives v0.2.0 continuity with the already-run field test while avoiding unnecessary recollection work.

### 13.2 Incident Response Sources

Preferred public sources for the `30` incident-response artifacts:

- Cloudflare incident reports and postmortems
- GitHub engineering or GitHub Status postmortems
- Google Cloud incident reports
- AWS public post-event summaries with enough technical detail
- Stripe engineering incident writeups
- Datadog, Grafana Labs, Vercel, and similar infrastructure/vendor writeups when they include timeline and remediation detail
- public SREcon-style incident writeups or engineering blogs with concrete outage analysis

Selection rule: prefer artifacts with a clear timeline, stated root cause, and remediation section.

#### Incident Response Sourcing Table

| Source family | Example source | Target count | Why it is useful |
|---------------|----------------|--------------|------------------|
| Cloudflare | `blog.cloudflare.com/tag/postmortem/` and incident writeups | 6 | Usually strong on timeline, root cause, and remediation |
| GitHub | GitHub engineering incident writeups and `githubstatus.com` postmortems | 5 | Good operational detail; relevant to developer infrastructure |
| Google Cloud | public status incident reports and RCAs | 5 | Good multi-service failure scenarios and rollback reasoning |
| AWS | post-event summaries with enough technical detail | 4 | Useful for partial-information incident narratives |
| Stripe | engineering incident writeups | 4 | Strong remediation and systems reasoning |
| Datadog / Grafana / Vercel / similar vendors | public outage or RCA posts | 4 | Broadens vendor style and incident taxonomy |
| Public SRE / engineering writeups | SREcon-style or engineering-blog incident analyses | 2 | Helps avoid overfitting to hyperscaler incident style |

Target total: `30`

### 13.3 Change Management Sources

Preferred sources for the `20` change-management artifacts:

- rollout or migration RFCs in OSS repos
- architecture proposals that include rollout and rollback steps
- public release plans or deployment runbooks
- engineering blog posts describing planned migrations before execution
- public postmortems that reference the original planned change and where it failed
- issue threads or design docs around risky operational changes in projects such as Kubernetes, Backstage, Grafana, or large infrastructure systems

If real public CAB-style packets are too sparse, derive a small number of synthetic change packets from public source material and mark them explicitly as synthetic in the corpus and final report.

#### Change Management Sourcing Table

| Source family | Example source | Target count | Why it is useful |
|---------------|----------------|--------------|------------------|
| OSS rollout / migration RFCs | Kubernetes enhancement proposals, rollout RFCs, datastore migrations | 5 | Closest public analog to real CAB review |
| Architecture proposals with rollout plans | Backstage, Grafana, platform/infrastructure RFCs | 4 | Includes sequencing, blast radius, and rollback logic |
| Deployment runbooks / release plans | public release engineering docs or staged rollout plans | 3 | Useful for approval and guardrail reasoning |
| Incident-linked pre-change plans | postmortems that reference the original intended change | 4 | Best source for plan-vs-outcome comparison |
| Public issue/design threads for risky changes | infra projects discussing migrations, config changes, or feature rollouts | 2 | Captures review-like operational debate |
| Synthetic CAB packets from public materials | structured from real public incidents or migrations | 2 | Fills gaps when public artifacts lack standardized change-ticket format |

Target total: `20`

### 13.4 Security Incident Sources

Preferred sources for the `20` security-incident artifacts:

- GitHub Security Advisories
- CVE records with linked patch commits or advisories
- vendor security incident disclosures with mitigation details
- OSS security postmortems
- writeups that pair exploit conditions with maintainer fixes or advisory updates
- incident disclosures from projects with transparent patch discussion, such as Kubernetes, Django, Rails, curl, and container/runtime ecosystems

Selection rule: prefer artifacts that let the debate test exploitability, mitigation sufficiency, affected-scope reasoning, or patch completeness.

#### Security Incident Sourcing Table

| Source family | Example source | Target count | Why it is useful |
|---------------|----------------|--------------|------------------|
| GitHub Security Advisories | `github.com/advisories` entries with linked repo context | 6 | Standardized advisory structure and broad OSS coverage |
| CVE + patch pairs | CVE records with linked commits or fix PRs | 5 | Strong for exploitability and patch-completeness debate |
| OSS security postmortems | Kubernetes, Django, Rails, curl, container/runtime ecosystems | 4 | Rich technical detail and real remediation tradeoffs |
| Vendor security disclosures | public incident disclosures with mitigation guidance | 3 | Tests non-repo narrative security reasoning |
| Exploit writeup + maintainer response pairs | researcher writeup plus advisory/update | 2 | Good for disagreement on severity and sufficient mitigation |

Target total: `20`
