# Field Test Plan — v0.1.0 "Prove the Loop"

> **Status:** Approved · **Version:** 0.1.0 · **Window:** Aug 25-31, 2026
> **Owner:** Deb Ghosal · **Exit bar:** [PRD §7.1](../../design/prd/07-success-metrics.md)
>
> This plan describes **how** we test the falsifiable v0.1.0 bar, **where** the corpus comes from, **which** models and pairs we run, and **what** success looks like. It is the execution companion to the [field-testing strategy](../field-testing-strategy.md) (Tier 0) and the [competitor benchmark protocol](../design/prd/19-competitor-benchmark.md).

---

## §1 Objective

Prove the engine works end-to-end on real PRs from public repos, answering four questions:

| # | Question | How answered |
|---|----------|-------------|
| Q1 | **Does independent review surface what a single reviewer misses?** | Distinct-issue yield vs single-reviewer baseline on the same 300 PRs |
| Q2 | **Is the debate real, not theater?** | Theater rate < 30%; convergence/disputed bands both healthy |
| Q3 | **Is the result stable?** | Flakiness sweep: N=5 seed-controlled runs per artifact; verdict flips < 20% |
| Q4 | **Does heterogeneity matter?** | Homogeneous vs heterogeneous pair delta on a 50-PR subsample |

If Q1 produces ≥1 artifact where the adversarial output contains a materially distinct issue not found by the baseline — **and** that issue is confirmed by the known outcome (revert reason, advisory) — the v0.1.0 bar is met. If not, the report says FAIL with root-cause analysis ([§9 roadmap kill criterion](../../design/prd/09-roadmap.md)).

---

## §2 Scope Lock (v0.1.0)

Per [PRD §5.1](../../design/prd/05-features.md), v0.1.0 ships:

| Dimension | Scope | Rationale |
|-----------|-------|-----------|
| **Domain** | PR review only (single adapter) | Only adapter that exists in v0.1 |
| **Language** | English only | i18n deferred to v0.2 ([§22](../../design/prd/22-internationalization.md)) |
| **Artifact type** | Git diffs | PR-review adapter normalizer |
| **Interface** | CLI (`advdeb review --pr`) | No UI, no HTTP, no GitHub Action |
| **Source** | Public repos only | No private data in v0.1 field test |
| **Models** | OpenAI-compatible endpoints | BYOM registry; scripted reviewers in CI |

**Explicitly out of scope for this test:** non-code domains (Tier 1+), multi-language PRs, private repos, latency benchmarking, cost optimization, CodeRabbit-style third-party tool comparison.

---

## §3 Corpus Selection

### 3.1 Outcome Types (15 categories, 300 PRs total)

| Outcome | Count | Ground truth | Why it tests the thesis |
|---------|-------|-------------|------------------------|
| **Merged-then-reverted** | 30 | ✅ Revert commit message | Reviewer missed what caused the revert |
| **Merged-then-hotfixed** | 20 | ✅ Hotfix PR references original | Reviewer missed an immediate breakage |
| **Merged-then-security-advisory** | 20 | ✅ CVE/GHSA description | Reviewer missed a latent vulnerability |
| **Merged-then-fixed (follow-up)** | 20 | ✅ Fix PR references original | Reviewer missed a non-critical bug |
| **Merged-then-perf-regression** | 15 | ✅ Benchmark degradation | Reviewer missed a performance issue |
| **Merged-then-flaky-tests** | 15 | ⚠️ CI flake reports | Reviewer missed test coverage gap |
| **Rejected/closed-without-merge** | 30 | ✅ Reviewer comments | Reviewer caught the issue pre-merge |
| **Closed-by-author-after-review** | 15 | ✅ Author conceded | Reviewer persuaded author |
| **Race condition caught in review** | 15 | ✅ Reviewer comments | Hardest bug type to catch |
| **Breaking API change caught in review** | 15 | ✅ Reviewer comments | Backward compat reasoning |
| **Refactoring that introduced regression** | 20 | ✅ Follow-up fix or revert | "Cleanup" broke something |
| **AI-generated PR accepted** | 15 | ⚠️ Copilot/ChatGPT attribution | Was the review fooled? |
| **AI-generated PR rejected** | 15 | ✅ Reviewer caught AI mistake | Human caught what AI got wrong |
| **Dependency bot PR that broke things** | 15 | ✅ CI failure or revert | Automated change, human review |
| **Clean merge (control)** | 40 | ⚠️ No known issue | Baseline false-positive rate |
| **Total** | **300** | | |

### 3.2 Target Repos (50+ repos, 15+ languages)

| Repo | Language | Why | PRs |
|------|----------|-----|-----|
| **kubernetes/kubernetes** | Go | 89k closed PRs, SIG review, frequent reverts | 20 |
| **golang/go** | Go | Compiler/runtime bugs, security CVEs | 10 |
| **prometheus/prometheus** | Go | TSDB corruption, query bugs | 10 |
| **etcd-io/etcd** | Go | Raft correctness, data loss CVEs | 8 |
| **cockroachdb/cockroach** | Go | Distributed SQL, transaction bugs | 8 |
| **moby/moby** | Go | Container security, namespace bugs | 6 |
| **django/django** | Python | Security advisories, ORM correctness | 15 |
| **python/cpython** | Python | GIL, security CVEs, corner cases | 12 |
| **pandas-dev/pandas** | Python | Numerical correctness, edge cases | 10 |
| **ansible/ansible** | Python | Idempotency bugs, module compat | 8 |
| **scikit-learn/scikit-learn** | Python | Algorithm correctness | 6 |
| **pallets/flask** | Python | Security advisory track record | 5 |
| **microsoft/vscode** | TypeScript | 62k PRs, 50+ comment debates | 15 |
| **microsoft/TypeScript** | TypeScript | Compiler correctness, type edge cases | 12 |
| **facebook/react** | TypeScript | Concurrency model, subtle state bugs | 10 |
| **vercel/next.js** | TypeScript | Dep bumps that break, security issues | 8 |
| **angular/angular** | TypeScript | Strict review, revert cycles | 8 |
| **sveltejs/svelte** | TypeScript | Reactivity model bugs | 5 |
| **rust-lang/rust** | Rust | Compiler bugs, perf regressions | 12 |
| **denoland/deno** | Rust | API changes, async internals | 8 |
| **tokio-rs/tokio** | Rust | Async runtime, concurrency correctness | 8 |
| **servo/servo** | Rust | Browser engine, security-critical | 5 |
| **rails/rails** | Ruby | Security CVEs, migration bugs | 12 |
| **Homebrew/brew** | Ruby | Reverted formula updates | 8 |
| **jekyll/jekyll** | Ruby | Plugin compat, parsing edge cases | 5 |
| **torvalds/linux** | C | 1.48M commits, security, memory safety | 15 |
| **git/git** | C | Data integrity, filesystem race bugs | 8 |
| **curl/curl** | C | 15k PRs, security advisories, TLS | 10 |
| **redis/redis** | C | Data structure correctness, persistence | 8 |
| **openssh/openssh-portable** | C | Auth, crypto implementation bugs | 5 |
| **spring-projects/spring-boot** | Java | Security advisories, dep management | 10 |
| **elastic/elasticsearch** | Java | Distributed correctness, data integrity | 8 |
| **apache/kafka** | Java | Data loss, exactly-once debates | 8 |
| **google/guava** | Java | API compat, concurrency fixes | 5 |
| **llvm/llvm-project** | C++ | Codegen bugs, optimization correctness | 10 |
| **facebook/folly** | C++ | Template metaprog, memory bugs | 5 |
| **swiftlang/swift** | Swift | Type system, async/await bugs | 8 |
| **JetBrains/kotlin** | Kotlin | Type inference, backward compat | 8 |
| **square/okhttp** | Kotlin | TLS, timeout race conditions | 5 |
| **flutter/flutter** | Dart | Rendering bugs, platform-specific | 8 |
| **elixir-lang/elixir** | Elixir | Pattern matching, actor concurrency | 5 |
| **phoenixframework/phoenix** | Elixir | WebSocket, live view state | 5 |
| **apache/spark** | Scala | Query optimization, shuffle bugs | 8 |
| **ziglang/zig** | Zig | Comptime eval, stage1/stage2 correctness | 5 |
| **ghc/ghc** | Haskell | Type system, lazy eval edge cases | 4 |
| **nvm-sh/nvm** | Shell | POSIX portability | 4 |
| **ohmyzsh/ohmyzsh** | Shell | Plugin compat, cross-platform | 4 |
| **protocolbuffers/protobuf** | C++/Java | Serialization correctness | 5 |
| **hashicorp/terraform** | Go | State management, provider compat | 8 |
| **grafana/grafana** | Go/TS | Data viz correctness, plugin security | 5 |
| **Total** | | | **300** |

### 3.3 Stratification Matrix

| Dimension | Buckets | Target per bucket |
|-----------|---------|-------------------|
| **Size (lines changed)** | XS (1-10), S (11-100), M (101-500), L (501-2000), XL (2001-10k), XXL (10k+) | ≥40 per tier |
| **Language** | Go, Python, TypeScript, Rust, C, Java, C++, Ruby, Swift, Kotlin, Dart, Elixir, Scala, Zig, Haskell, Shell | ≥5 per primary (Go/Python/TS), ≥3 per secondary |
| **Outcome** | 15 types (see §3.1) | 15-40 per type |
| **Purpose** | Feature, Bugfix, Refactor, Docs, Perf, Security, Test-only, Deps, CI/Build | ≥25 per primary (feature/bugfix/refactor) |
| **Review depth** | Low (<10 comments), Medium (10-50), High (50+) | ~100/100/100 |
| **Contributor type** | First-time, Regular, Core maintainer, Bot (Dependabot/Renovate) | ~60/180/40/20 |
| **Diff content type** | Source code, Tests-only, Docs-only, Config/CI (YAML/Docker/Terraform), Generated code (protobuf/openapi) | ≥40 per type |

### 3.4 PR Subtypes (content variety within git diffs)

All subtypes are git diffs — but they test different reviewer capabilities:

| Subtype | Count | What it tests | Source examples |
|---------|-------|---------------|-----------------|
| **Source code (primary)** | 180 | Core logic, security, correctness reasoning | All repos |
| **Tests-only** | 30 | Can reviewers assess test quality and coverage gaps? | k8s, django, rust-lang, vscode |
| **Docs-only** | 20 | Can reviewers catch documentation errors? | All repos (docs: prefix PRs) |
| **Config/CI (YAML, Docker, Terraform)** | 30 | Can reviewers reason about IaC correctness? | k8s manifests, GitHub Actions, Dockerfiles |
| **Generated code (protobuf, openapi stubs)** | 15 | Can reviewers spot hand-edits to generated files? | protobuf, grpc, openapi repos |
| **Multi-language diffs** | 15 | Can reviewers reason across language boundaries? | Full-stack repos (vscode, grafana, next.js) |
| ** vendored dependency updates** | 10 | Can reviewers spot breaking changes in vendored code? | Go vendor dirs, npm lockfiles |
| **Total** | **300** | | |

### 3.5 Corpus Publication

Per [§19.2 Step 1](../../design/prd/19-competitor-benchmark.md), the corpus is **published before any runs**:

- File: `docs/field-test/v0.1.0/corpus.csv`
- Fields: `url, repo, language, lines_changed, size_label, outcome, purpose, review_depth, contributor_type, diff_content_type, revert_reason, expected_debate_flag, notes`
- Committed to git **before** the first sweep timestamp (verifiable via git history)

### 3.6 Corpus Curation Rules

1. **No cherry-picking:** every PR from the selected repos that matches the stratification criteria in the search window is included. No post-hoc exclusion.
2. **Revert reason must be documented:** the revert commit message or linked issue must explain *why* the change was reverted.
3. **Advisory must be public:** only CVEs/ghsa-* advisories that are already public at corpus selection time.
4. **Clean merges are random:** selected by random sampling of merged PRs in the matching size/language/purpose bucket.
5. **Corpus is frozen after commit:** no additions, removals, or substitutions after the first run.
6. **Review depth tier is based on comment count at corpus selection time** (not post-sweep).
7. **First-time contributor PRs** must have ≥10 lines changed (exclude trivial typo fixes).
8. **Bot PRs** must be from Dependabot, Renovate, or equivalent — not CI/CD pipeline bots.
9. **Generated code PRs** must be diffs of files that are typically auto-generated (`.pb.go`, `_pb2.py`, `openapi.go`, etc.).
10. **Multi-language diffs** must touch ≥2 distinct file extensions in one PR.

---

## §4 Model Pairs

All models via OpenRouter (single API key: `OPENROUTER_API_KEY`).

### 4.1 Models (4 models, maximally diverse families)

| Model | OpenRouter ID | Family | Origin | Input $/MTok | Output $/MTok |
|-------|--------------|--------|--------|-------------|--------------|
| GPT-4o-mini | `openai/gpt-4o-mini` | openai | US | $0.15 | $0.60 |
| Gemini 2.5 Flash | `google/gemini-2.5-flash` | google | US | $0.15 | $0.60 |
| DeepSeek-V3 | `deepseek/deepseek-chat` | deepseek | China | $0.27 | $1.10 |
| Mistral Small 3.2 | `mistralai/mistral-small-3.2-24b-instruct` | mistral | EU | $0.075 | $0.20 |

### 4.2 Debate Pairs (5 pairs, 150 PRs each)

| Pair | Slot A | Slot B | Diversity | Why |
|------|--------|--------|-----------|-----|
| pair1_gpt_gemini | GPT-4o-mini | Gemini 2.5 Flash | OpenAI vs Google | US mainstream pair |
| pair2_gemini_deepseek | Gemini 2.5 Flash | DeepSeek-V3 | Google vs DeepSeek | US vs China (best performer in test) |
| pair3_gpt_mistral | GPT-4o-mini | Mistral Small | OpenAI vs Mistral | US vs EU |
| pair4_gemini_mistral | Gemini 2.5 Flash | Mistral Small | Google vs Mistral | US vs EU |
| pair5_deepseek_mistral | DeepSeek-V3 | Mistral Small | China vs EU | Maximally diverse |

### 4.3 Single-Reviewer Baseline (150 PRs)

| Slot | OpenRouter Model |
|------|-----------------|
| A | `openai/gpt-4o-mini` |

One pass, no debate. This is the "Tool X" baseline for blind comparison.

### 4.4 Homogeneous Subsample (30 PRs)

| Slot | OpenRouter Model |
|------|-----------------|
| A | `openai/gpt-4o-mini` |
| B | `openai/gpt-4o-mini` |

Same model both sides — measures debate process value without model diversity.

### 4.5 Total Cost Estimate

| Component | Cost |
|-----------|------|
| 4 models × 150 PRs (single pass each) | ~$0.32 |
| 5 pairs × 150 PRs (debate rounds) | ~$1.50 |
| Flakiness subsample (50 PRs × 5 seeds) | ~$0.50 |
| Round saturation (20 PRs × 3 rounds) | ~$0.10 |
| **Total** | **~$2.50** |

---

## §5 Configuration

### 5.1 CLI Invocation

```bash
# Standard review
advdeb review --pr <url> --rounds 2 --pair diverse

# With budget cap
advdeb review --pr <url> --rounds 2 --pair diverse --budget 50000

# Verbose (for debugging)
advdeb review --pr <url> --rounds 2 --pair diverse --verbose
```

### 5.2 Config Template

```toml
[providers.a]
type = "openai_compatible"
base_url = "https://openrouter.ai/api/v1"
model = "openai/gpt-4o-mini"
key_env = "OPENROUTER_API_KEY"

[providers.b]
type = "openai_compatible"
base_url = "https://openrouter.ai/api/v1"
model = "google/gemini-2.5-flash"
key_env = "OPENROUTER_API_KEY"

rounds = 2
max_llm_calls = 50
seed = 42
```

### 5.3 Seed Strategy

- Flakiness sweep: N=5 runs per artifact, seeds `[42, 43, 44, 45, 46]`
- Primary run: seed=42
- Homogeneous subsample: seed=42
- Single-reviewer baseline: seed=42

### 5.4 Budget

- Default budget: 50,000 tokens per artifact
- Large PRs (>2000 lines): 100,000 tokens
- Budget exhaustion is **not a failure** — it produces a `partial: budget_exhausted` report (M8 T8.4), which is valid data for the flakiness/cost analysis

---

## §6 Execution Plan

### 6.1 Phase 1 — Corpus Assembly (Day 1-2)

| Task | Output | Owner |
|------|--------|-------|
| Search candidate PRs from 50 repos via `gh search prs` | Long list (~500 candidates) | You |
| Verify revert/advisory/review documentation | Corpus shortlist (300) | You |
| Stratify by size × language × outcome × purpose × review_depth × contributor_type × diff_content_type | `corpus.csv` | You |
| Commit corpus to `docs/field-test/v0.1.0/corpus.csv` | Git commit (timestamped) | You |

### 6.2 Phase 2 — Single-Reviewer Baseline (Day 2-3)

| Task | Details |
|------|---------|
| Run `advdeb review --pr <url> --rounds 0` | 300 PRs × 1 run = 300 single passes |
| Capture: issues found, issue text, severity, confidence, latency, cost |
| Store results in `docs/field-test/v0.1.0/baseline/` |
| **Do NOT look at results yet** (blind rating protocol) |

### 6.3 Phase 3 — Adversarial Sweep (Day 3-5)

| Task | Details |
|------|---------|
| Run `advdeb review --pr <url> --rounds 2 --pair diverse` | 300 PRs × 1 run = 300 debates |
| Run `advdeb review --pr <url> --rounds 2 --pair same` | 50 PRs × 1 run = 50 debates |
| Run flakiness sweep: `--seed 42..46` | 300 PRs × 5 seeds = 1500 runs (stagger overnight) |
| Capture: transcripts, latency, cost, verdict, resolved/unresolved, flags |
| Export transcripts: `advdeb transcript <run_id> --export jsonl` |
| Store in `docs/field-test/v0.1.0/sweep/` |

### 6.4 Phase 4 — Analysis (Day 3-4)

| Step | What | Method |
|------|------|--------|
| 1 | Distinctness rating | Blind rater: baseline ("Tool X") vs adversarial ("Tool Y") on each PR |
| 2 | Ground-truth verification | For reverted/advisory PRs: was the distinct issue the actual cause? |
| 3 | Flakiness computation | Verdict stability across N=5 runs; flag >20% flips |
| 4 | Theater rate | % of debates with zero state changes |
| 5 | Pair-diversity delta | Heterogeneous vs homogeneous distinct-issue yield on subsample |
| 6 | `would_resolve_if` self-rating | Rate each unresolved point: actionable? decision-changing? |
| 7 | False positive analysis | Issues raised on clean-merge control group; FP rate vs baseline |
| 8 | Cost & latency breakdown | Per-PR token cost (prompt + completion), p50/p90 latency, cost per distinct issue |
| 9 | Round saturation | Run 20-PR subsample with 3 rounds; does R3 add value over R2? |
| 10 | Cross-model issue overlap | What types does GPT-4o find that Claude misses (and vice versa)? |
| 11 | Human review comparison | For 50+ comment PRs: what did humans catch that debate missed? |
| 12 | Failure mode catalog | Categorize: timeout, budget exhaustion, degradation, theater, crash, schema validation |
| 13 | PR category performance matrix | All metrics broken down by language × size × outcome × purpose × diff_content_type |
| 14 | Concession quality | Genuine vs capitulation cascade; are conceded claims actually wrong? |
| 15 | `would_resolve_if` deep dive | Categorize: "need more tests", "need runtime data", "need security audit", "need design doc" — flag cop-outs |

### 6.5 Phase 5 — Report (Day 5-7)

Write `FIELD_TEST_REPORT.md` per [T10.5 (#50)](../../wbs/0.1.0/M10-field-test-tier0.md).

---

## §7 Success Criteria

### 7.1 Binary Bar (PRD §7.1)

> **One realistic case where reviewer B finds a materially different issue before convergence — or a disagreement report that measurably improves a human call — demonstrated on real PRs from a public repo, with full transcripts.**

**Operationalized:**

1. The single-reviewer baseline finds issues A, B, C.
2. The adversarial debate finds issues A, B, C, D.
3. Issue D is **materially distinct** (not a paraphrase of A, B, or C).
4. Issue D is **confirmed by the known outcome** (revert reason, advisory description).
5. Full transcripts are published.
6. **PASS** if this happens for ≥1 artifact in the corpus.
7. **FAIL** if it does not — report must include root-cause analysis.

### 7.2 Secondary Metrics (Reported, Not Gated)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Distinct-issue yield | > 0 on ≥20% of artifacts | Blind rater comparison |
| Theater rate | < 30% | % of debates with zero state changes |
| Convergence rate | 30-70% | % of debates ending converged (both bands healthy) |
| Verdict stability | > 80% | % of runs producing same verdict (flakiness sweep) |
| `would_resolve_if` actionable | > 50% | Self-rater: could I act on this? |
| Heterogeneous vs homogeneous delta | +30% distinct issues | Pair-diversity subsample |
| Budget exhaustion rate | < 20% | % of debates hitting budget cap |
| False positive rate | < 15% | Issues raised on clean-merge control group |
| Cost per distinct issue | < $1.00 | Total cost / distinct issues found |
| Round saturation | R2 adds > R1, R3 adds < R2 | Round-by-round claim state changes on 20-PR subsample |
| Concession correctness | > 70% | Conceded claims that are actually wrong (ground truth check) |
| Cross-model overlap | < 70% | % of issues found by both models (lower = more diverse) |

### 7.3 Kill Criteria

Per [§9 roadmap](../../design/prd/09-roadmap.md):

- **FAIL on binary bar:** do not ship v0.1.0. Publish report with root-cause analysis. File issues for each root cause.
- **Theater rate > 50%:** prompts/rubrics are broken. Fix before shipping.
- **Flakiness > 40% on > 20% of artifacts:** seed-controlled reproducibility is broken. Investigate before shipping.

---

## §8 Measurement Methodology

### 8.1 Rubric: "Materially Distinct"

An issue is **materially distinct** if it meets ALL of:

1. **Different root cause** — not a paraphrase of a baseline issue. If baseline says "XSS in search endpoint" and adversarial says "XSS in search endpoint but worse", that's NOT distinct.
2. **Actionable** — a human could act on the finding. "This code is bad" is not actionable. "Missing input validation on line 42 allows SQL injection" is actionable.
3. **Confirmed by evidence** — the issue references specific code locations, diff lines, or evidence that can be verified.

**Not distinct:** style nits, formatting complaints, naming suggestions, duplicate findings, paraphrases.

### 8.2 Rubric: "would_resolve_if Actionable"

Rate each unresolved point on a 3-point scale:

| Score | Label | Definition |
|-------|-------|------------|
| 3 | **Actionable** | Specific next step: "load test at production row count", "add validation for edge case X", "review Y's security model" |
| 2 | **Vague** | Directional but not specific: "need more testing", "should be more secure", "review this more carefully" |
| 1 | **Cop-out** | Noncommittal: "need more information", "this depends on context", "would need to see the full picture" |

Target: >70% of unresolved points rated 3 or 2.

### 8.3 Rubric: "False Positive"

An issue is a **false positive** if:

- It is raised on a **clean-merge control group** PR (no known issues)
- It is **incorrect** — the code change is fine and the claimed issue does not exist
- It is a **style nit** that the project's maintainers would not consider an issue

For reverted/advisory PRs, an issue is a **false positive** if it:
- Points to a different problem than the actual revert reason
- Would not have prevented the revert if caught

### 8.4 Rubric: "Concession Correctness"

A concession is **correct** if the conceded claim is **actually wrong** — verified against the known outcome (revert reason, advisory, or reviewer comments). A concession is **incorrect** (capitulation) if the reviewer conceded a valid claim under pressure.

### 8.5 Theater Detection

Theater = zero claim state changes across the entire debate:
- No concessions, no new objections, no evidence shifts
- `convergence_score == 1.0` because all claims started and ended in the same state
- Exposed in report flags. Any theater > 30% is a prompt/rubric bug.

### 8.6 Flakiness Measurement

For each of the 150 PRs, run N=5 seed-controlled debates:

| Threshold | Classification |
|-----------|---------------|
| 100% same verdict | Stable |
| 80-99% same verdict | Mostly stable |
| 60-79% same verdict | Somewhat flaky |
| < 60% same verdict | Flaky — exclude from pass/fail analysis |

### 8.7 Cost & Latency Measurement

Captured per debate run:

| Metric | Collection |
|--------|-----------|
| Prompt tokens | Provider response metadata |
| Completion tokens | Provider response metadata |
| Wall time (seconds) | `time.time()` before and after each provider call |
| Cost | Tokens × provider pricing (computed post-hoc, not live) |
| Cost per distinct issue | Total cost / distinct issues found (stratum-level) |

### 8.8 Round Saturation

On a 20-PR subsample, run 3 rounds instead of 2. Measure:

1. New claims surfaced in R2 vs R1
2. New claims surfaced in R3 vs R2
3. Concessions in R2 vs R1
4. Concessions in R3 vs R2

If R3 adds < 10% new value, 2 rounds is validated as the default.

### 8.9 Cross-Model Overlap

For each PR, compare the issues found by model A vs model B:

| Category | Definition |
|----------|-----------|
| **Both found** | Both models raised the same issue (same root cause) |
| **A only** | Only GPT-4o-mini found it |
| **B only** | Only Gemini/DeepSeek found it |
| **Neither** | Known issue from ground truth that neither model caught |

Reported as a Venn diagram per pair and per language.

### 8.10 Human Review Comparison

For the 30 high-comment (50+) PRs:

1. Extract all human reviewer comments from the PR
2. Categorize each comment by issue type
3. Compare with adversarial debate output
4. Report: what did humans catch that debate missed? What did debate catch that humans missed?

### 8.11 Decision Framework

```
Binary bar met? (≥1 artifact with materially distinct issue confirmed by ground truth)
├── YES
│   ├── Theater rate < 30%?
│   │   ├── YES → SHIP (v0.1.0 passes)
│   │   └── NO  → SHIP WITH WARNING (flag in report, file issues)
│   └── Flakiness < 20%?
│       ├── YES → SHIP
│       └── NO  → SHIP WITH WARNING (flag flaky artifacts, file issues)
│
└── NO
    ├── Theater rate > 50%?
    │   ├── YES → FAIL (prompts are broken, fix before retry)
    │   └── NO  → FAIL (thesis not proven — publish report, file issues, iterate)
    └── Always: publish honest report, file issues for each root cause
```

---

## §9 Artifact Layout

All field-test artifacts live under `docs/field-test/v0.1.0/`:

```
docs/field-test/v0.1.0/
├── field-test-plan.md                  # This plan
├── corpus.csv                          # Published corpus (300 PRs)
├── baseline/
│   ├── <pr-id>.json                    # Single-reviewer baseline results
│   └── baseline-summary.csv
├── sweep/
│   ├── primary/                        # Heterogeneous pair (300 PRs)
│   │   ├── <pr-id>/
│   │   │   ├── transcript.jsonl        # Full debate lineage
│   │   │   ├── report.json             # SynthesisReport
│   │   │   └── metadata.json           # Latency, cost, config
│   │   └── ...
│   ├── homogeneous/                    # Homogeneous pair subsample (50 PRs)
│   │   └── ...
│   ├── flakiness/                      # N=5 seed-controlled runs (300 PRs)
│   │   ├── <pr-id>/
│   │   │   ├── seed-42/
│   │   │   ├── seed-43/
│   │   │   ├── seed-44/
│   │   │   ├── seed-45/
│   │   │   └── seed-46/
│   │   └── flakiness-summary.csv
│   └── round-saturation/              # 3-round subsample (20 PRs)
│       └── ...
├── analysis/
│   ├── distinctness-ratings.csv        # Blind rater output
│   ├── ground-truth-verification.csv   # Known-issue match analysis
│   ├── diversity-delta.csv             # Heterogeneous vs homogeneous comparison
│   ├── false-positives.csv             # FP analysis on clean-merge control group
│   ├── cost-latency.csv                # Per-PR cost and latency breakdown
│   ├── cross-model-overlap.csv         # GPT vs Claude issue overlap
│   ├── human-review-comparison.csv     # Debate vs human review (50+ comment PRs)
│   ├── failure-modes.csv               # Categorized engine failures
│   ├── category-matrix.csv             # Performance by language × size × outcome × purpose
│   └── concession-quality.csv          # Concession correctness vs ground truth
├── reproduce.sh                        # Reproducibility script
└── FIELD_TEST_REPORT.md                # Final report (T10.5)
```

---

## §10 Expected Outcomes

### 10.1 Best Case

- **≥3 artifacts** where adversarial debate surfaces a materially distinct issue confirmed by the revert/advisory reason
- **Theater rate < 15%** — debates are genuinely changing claim states
- **Convergence rate ~50%** — healthy balance of agreement and disagreement
- **Heterogeneous pair finds 2× more distinct issues** than homogeneous pair
- **Flakiness < 10%** — verdicts are stable across seeds
- **`would_resolve_if` actionable** on > 60% of unresolved points

### 9.2 Acceptable Case

- **≥1 artifact** meets the binary bar (PASS on v0.1.0)
- **Theater rate < 30%**
- **Convergence rate 30-70%**
- **Heterogeneous delta > 0** (any improvement)
- **Flakiness < 20%**

### 9.3 Failure Case (Ship Blocked)

- **0 artifacts** meet the binary bar
- **Theater rate > 50%** — prompts are producing empty debates
- **Flakiness > 40%** — verdicts are random
- **Convergence rate 100% or 0%** — reviewers aren't independent or aren't engaging

---

## §10 Known Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **API cost exceeds budget** | Medium | Can't complete sweep | Use `--budget` flag; run primary sweep first, defer flakiness if needed |
| **Rate limiting from API providers** | High | Delays | Stagger runs; implement backoff (M8 T8.4); run overnight |
| **Corpus PRs no longer available** | Low | Can't reproduce | Fork PRs to local repo; use `gh pr diff` to capture |
| **Blind rating is subjective** | Medium | Inconsistent results | Use strict rubric: "materially distinct" = different root cause, not different phrasing |
| **Engine crashes mid-sweep** | Low | Data loss | M8 crash safety: transcripts survive; resume from last round |
| **Adversarial debate finds nothing** | High (first run) | Binary bar not met | This is valid data. Report honestly. File issues for prompt/rubric improvements. |

---

## §11 Exit Gate Checklist

- [ ] Corpus published: `docs/field-test/v0.1.0/corpus.csv` (150 PRs, 15 outcome types, 3 primary languages) committed before first run
- [ ] Single-reviewer baseline results stored in `docs/field-test/v0.1.0/baseline/` (150 PRs)
- [ ] Pair 1 sweep (GPT-4o-mini + Gemini, 150 PRs) complete with transcripts
- [ ] Pair 2 sweep (Gemini + DeepSeek, 150 PRs) complete with transcripts
- [ ] Homogeneous subsample (30 PRs) complete with transcripts
- [ ] Flakiness sweep (N=5) complete on a 50-PR subsample
- [ ] Round saturation subsample (20 PRs, 3 rounds) complete
- [ ] Blind distinctness rating completed
- [ ] Ground-truth verification completed (reverted/advisory/rejected PRs)
- [ ] False positive analysis completed (clean-merge control group)
- [ ] Cost & latency breakdown completed
- [ ] Cross-model issue overlap completed (Pair 1 vs Pair 2)
- [ ] Human review comparison completed (30 high-comment PRs)
- [ ] Failure mode catalog completed
- [ ] `FIELD_TEST_REPORT.md` written with PASS/FAIL determination
- [ ] Every claim in report traceable to a transcript file path
- [ ] Report includes honest misses section ("both reviewers missed X")
- [ ] If PASS: proceed to M11 (Release)
- [ ] If FAIL: publish report with root-cause analysis, file issues, do not ship

---

## §12 Reproducibility

To reproduce the full sweep:

```bash
git checkout <commit-hash>
pip install adversarial-debate==0.1.0
export OPENAI_API_KEY=...
export GOOGLE_API_KEY=...
export DEEPSEEK_API_KEY=...

# Pair 1: GPT-4o-mini + Gemini 2.5 Flash
advdeb review --pr <url> --rounds 2 --pair diverse --config config-pair1.toml

# Pair 2: Gemini 2.5 Flash + DeepSeek-V3
advdeb review --pr <url> --rounds 2 --pair diverse --config config-pair2.toml

# Baseline (single pass)
advdeb review --pr <url> --rounds 0
```

**Reproducibility package:** `corpus.csv`, `config-pair1.toml`, `config-pair2.toml`, engine commit hash, seed values, provider model versions. All committed under `docs/field-test/v0.1.0/`.

---

## §13 References

| Document | Section | Relevance |
|----------|---------|-----------|
| [PRD — Success Metrics](../../design/prd/07-success-metrics.md) | §7.1, §7.6 | Binary bar, measurement methodology |
| [PRD — Features](../../design/prd/05-features.md) | §5.1 | v0.1.0 scope (F1-F10) |
| [PRD — Competitor Benchmark](../../design/prd/19-competitor-benchmark.md) | §19.2 | Protocol steps 1-5 |
| [PRD — Eval Harness](../../design/prd/21-eval-harness.md) | §21.3-21.5 | Fixture format, rating protocols |
| [PRD — Business Case](../../design/prd/10-business-case.md) | §10.7, §10.10 | Credibility, time-to-first-value |
| [Field-Testing Strategy](../field-testing-strategy.md) | Tier 0 | 4-tier strategy, measurement protocol |
| [WBS M10](../../wbs/0.1.0/M10-field-test-tier0.md) | T10.1-T10.5 | Tasks this plan executes |