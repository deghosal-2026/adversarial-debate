# Changelog

## v0.2.1 (2026-08-28)

**Separate the Signal** — Mistral effect confirmed, pipeline invariants, false-negative measurement.

### Key Findings
- **Mistral effect confirmed** — DeepSeek+GPT separating experiment (0.246 convergence) disproves diversity-of-training-objective hypothesis. Mistral is the unique variable driving productive debate.
- **Pipeline integrity** — 5 row-count invariant assertions added at every pipeline seam. All pass. 2,333→359 collapse class eliminated.
- **False-negative measurement** — 1.7–3.4% missed-issue rate across 59 known-bad PRs. First recall data the project has ever reported.
- **0 flaky artifacts**, **0 theatre**, **87.4% MATCH** ground truth (3,008/3,440).

### Model Selection
- Default production pair remains GPT+Mistral (0.536 convergence)
- Validation pair: DeepSeek+Mistral (0.572 convergence)
- Recommendation changes: "include Mistral" replaces "pick from different labs"

### New Code
- `scripts/_seam_assert.py` — row-count invariant assertion utility
- `scripts/missed_issues.py` — false-negative measurement module (importable)
- `scripts/scripts_common.py` — shared pipeline utilities
- `scripts/09_missed_issues.py` — CLI entry point for missed-issue measurement
- `pair8_deepseek_gpt_mini` added to pipeline configuration

### Tests
- 55 new deterministic unit tests (zero LLM calls)
- `test_pairs.py` — 15 tests for pair configuration
- `test_seam_assert.py` — 19 tests for assertion logic
- `test_missed_issues.py` — 21 tests for detection and rate computation

### Field Test
- 367 debates across 5 pairs (150 artifacts, 4 domains)
- $0.57 total cost
- All results in `results/field-test/v0.2.1/`

## v0.2.0 (2026-08-27)

**Fix the Data** — Mixed-domain corpus, corrected pipeline, postmortem fixes.

### Field Test
- Mixed-domain corpus: 150 artifacts across 4 domains (PR review, incident response, change management, security incidents)
- 80 PRs reused from v0.1.0 corpus with stratified selection
- 30 incident response, 20 change management, 20 security incident artifacts
- 217 debates across 4 active pair roles (primary, validation, negative control, homogeneous control)
- Total cost: $0.42

### Pipeline Fixes
- Migrated all scripts from flat `pr_id`-only layout to nested `artifact_id`/`domain` layout
- Fixed `07_llm_judge.py` merge bug (keyed on `pr_id` instead of `artifact_id`)
- Fixed `06_ground_truth.py` output-path parent creation
- Added non-PR artifact HTML stripping and prompt size bounding
- Added corpus-aware default pair selection to `03_combine_results.py` and `04_run_debate.py`
- Created subset corpus files for validation (`validation_subset.csv`) and negative control (`negative_control_subset.csv`)
- Updated all scripts from `v0.1.0` to `v0.2.0` result paths

### Key Findings
- `pair3_gpt_mistral` confirmed as the best full-corpus default pair
- `pair1_gpt_gemini` confirmed as a weak negative control (0.033 avg convergence, 0/24 verdicts)
- `pair5_deepseek_mistral` remains stronger on subset (0.572 avg convergence)
- Zero theater across all 217 debates
- Binary bar met: 2070/2333 MATCH (88.7%), 0 NO_MATCH
- Sampled flakiness: 2/2 artifacts stable at 100% verdict stability
- 2-model primary strategy validated; full 4-model matrix not needed for v0.2.0

## v0.1.0 (2026-08-27)

**Prove the Loop** — Independent dual-review pass with bounded adversarial debate.

### Features
- Independent dual-review pass with delayed revelation (F1, F2)
- Structured debate schema: Claim, Objection, Concession, UnresolvedPoint (F3)
- Bounded rounds (default 2), point-by-point enforcement (F4)
- Convergence scoring + theater detection (F5, F6)
- Joint verdict + disagreement report with `would_resolve_if` (F7, F8)
- PR-review domain adapter: diff parsing, chunking, metadata extraction (F9)
- BYOM provider registry: OpenAI-compatible transport, PydanticAI/LangGraph adapters, ScriptedReviewer (F10)
- SQLite persistence with schema versioning, resume, budget/backoff, crash safety
- CLI: `init`, `review`, `report`, `transcript`, `resume`, `list`
- JSONL transcript export with optional redaction
- Flakiness detection: multi-run stability reporting

### Field Test Results
- 411 debates across 70 real PRs (kubernetes, prometheus, golang/go, etcd, rails, django)
- 6 model pairs × 4 models (GPT-4o-mini, Gemini 2.5 Flash, DeepSeek-V3, Mistral Small 3.2)
- Total cost: $0.53
- Binary bar PASSED: 49/49 PRs with known outcomes had ≥1 debate claim matching the actual cause
- Theater rate: 0.2% (1/411)
- Verdict stability: 96% (5-run flakiness sweep)
- Engine errors: 0

### Key Findings
- Model diversity is the strongest predictor of productive debate
- The debate prompt is the critical path, not the engine
- Maximum diversity (DeepSeek+Mistral) has a dark side: 65% capitulation cascade
- Homogeneous (GPT+GPT) outperforms weak diversity (GPT+Gemini)

### What's New
- Initial public release
- MIT licensed
- Python 3.11+ support