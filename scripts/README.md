# Field Test Scripts — v0.2.2

Scripts to run the field test. Run in order.

## Prerequisites

```bash
gh auth login
export OPENROUTER_API_KEY=sk-or-...
```

## Workflow

## Pair Roles

- **Primary / positive pair:** `pair3_gpt_mistral`
- **Validation pair:** `pair5_deepseek_mistral`
- **Negative control:** `pair1_gpt_gemini`
- **Homogeneous control:** `homogeneous_gpt`

### Step 0 — Download corpus

PR artifacts are already copied from v0.1.0. For non-PR artifacts:

```bash
python3 scripts/01_download_corpus_v2.py
```

Output: `results/field-test/v0.2.0/corpus/<domain>/<artifact_id>/`

### Step 1 — Run LLM reviewers

Run only the two full-corpus models for the primary sweep.

```bash
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/corpus.csv
python3 scripts/02_run_reviewer.py --model mistralai/mistral-small-3.2-24b-instruct --corpus results/field-test/v0.2.0/corpus.csv
```

Do **not** run DeepSeek or Gemini against the full corpus. They are subset-only.

Resume is automatic via CHECKPOINT files.

Subset corpus files:

- `results/field-test/v0.2.0/validation_subset.csv` — 36 artifacts for `DeepSeek + Mistral`
- `results/field-test/v0.2.0/negative_control_subset.csv` — 24 artifacts for `GPT + Gemini`

### Step 2 — Combine into pairs

```bash
python3 scripts/03_combine_results.py --corpus results/field-test/v0.2.0/corpus.csv
```

Pairs produced:

| Pair | Slot A | Slot B | Coverage |
|------|--------|--------|----------|
| `pair3_gpt_mistral` | GPT-4o-mini | Mistral Small 3.2 | All 150 artifacts |
| `pair5_deepseek_mistral` | DeepSeek-V3 | Mistral Small 3.2 | 30-40 validation subset |
| `pair1_gpt_gemini` | GPT-4o-mini | Gemini 2.5 Flash | Optional 20-30 negative control |
| `homogeneous_gpt` | GPT-4o-mini | GPT-4o-mini | 30-40 control subset |
| `baseline_gpt` | GPT-4o-mini | — | Single pass baseline |

### Step 3 — Run debate engine

```bash
python3 scripts/04_run_debate.py --corpus results/field-test/v0.2.0/corpus.csv
```

If the full run is too slow, keep `corpus.csv` as the canonical full corpus and run debate in parallel across these deterministic splits:

```bash
python3 scripts/04_run_debate.py --corpus results/field-test/v0.2.0/corpus_part1.csv
python3 scripts/04_run_debate.py --corpus results/field-test/v0.2.0/corpus_part2.csv
python3 scripts/04_run_debate.py --corpus results/field-test/v0.2.0/corpus_part3.csv
```

Each split contains 50 artifacts. Together they cover the full `corpus.csv`.

Output: `results/field-test/v0.2.0/debates/<pair_name>/<artifact_id>/`

### Step 4 — Analyze

```bash
python3 scripts/05_analyze.py
```

### Step 5 — Ground-truth verification (PR review domain only)

```bash
python3 scripts/06_ground_truth.py --corpus results/field-test/v0.2.0/corpus.csv --output analysis/ground-truth-comparison.csv
python3 scripts/07_llm_judge.py --model openai/gpt-4o-mini --workers 10 --input analysis/ground-truth-comparison.csv --output analysis/ground-truth-judged.csv
```

### Step 6 — Flakiness sweep

```bash
python3 scripts/08_flakiness.py --corpus results/field-test/v0.2.0/corpus.csv --runs 5 --limit 12
```

### Step 7 — Missed-issue (recall) measurement

```bash
python3 scripts/09_missed_issues.py
```

### Step 8 — Noise-floor baseline

Measures statistical uncertainty of aggregate metrics via bootstrap resampling. Run after debates complete. Zero LLM calls.

```bash
python3 scripts/noise_floor.py --trials 10000 --seed 42
```

Output: `results/field-test/v0.2.2/noise-floor-report.json` and `.md`

### Step 9 — Permutation control

Validates the LLM judge's match rate is discrimination, not vocabulary overlap. Run after ground-truth judging. Zero LLM calls.

```bash
python3 scripts/permutation_control.py --shuffles 500 --seed 42
```

Output: `results/field-test/v0.2.2/permutation-control-report.json` and `.md`

### Step 10 — Expert ratings (non-PR domains only)

Rate incident response, change management, and security incidents on the expert-rater triad:

1. **Distinctness** — is the second side's concern materially different?
2. **Actionability** — is the `would_resolve_if` path specific enough?
3. **Decision impact** — would this change or delay your conclusion?

## Optional Commands

These are for debugging, spot checks, or subset work.

```bash
# Single domain download
python3 scripts/01_download_corpus_v2.py --domain incident_response

# Test download 5 artifacts
python3 scripts/01_download_corpus_v2.py --limit 5

# Dry-run reviewer
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/corpus.csv --dry-run

# Limited reviewer sample
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/corpus.csv --limit 5

# Single artifact reviewer
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/corpus.csv --artifact etcd-io_etcd_PR22178

# Single pair debate
python3 scripts/04_run_debate.py --corpus results/field-test/v0.2.0/corpus.csv --pair pair3_gpt_mistral

# Limited debate sample
python3 scripts/04_run_debate.py --corpus results/field-test/v0.2.0/corpus.csv --limit 5

# Validation subset: DeepSeek + Mistral
python3 scripts/02_run_reviewer.py --model deepseek/deepseek-chat --corpus results/field-test/v0.2.0/validation_subset.csv
python3 scripts/02_run_reviewer.py --model mistralai/mistral-small-3.2-24b-instruct --corpus results/field-test/v0.2.0/validation_subset.csv
python3 scripts/03_combine_results.py --corpus results/field-test/v0.2.0/validation_subset.csv --pair pair5_deepseek_mistral
python3 scripts/04_run_debate.py --corpus results/field-test/v0.2.0/validation_subset.csv --pair pair5_deepseek_mistral

# Optional negative control: GPT + Gemini
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/negative_control_subset.csv
python3 scripts/02_run_reviewer.py --model google/gemini-2.5-flash --corpus results/field-test/v0.2.0/negative_control_subset.csv
python3 scripts/03_combine_results.py --corpus results/field-test/v0.2.0/negative_control_subset.csv --pair pair1_gpt_gemini
python3 scripts/04_run_debate.py --corpus results/field-test/v0.2.0/negative_control_subset.csv --pair pair1_gpt_gemini
```

## Output Structure

```
results/field-test/v0.2.0/    # results from the debate pipeline
results/field-test/v0.2.1/    # results from the v0.2.1 sweep
results/field-test/v0.2.2/    # measurement infrastructure outputs
├── noise-floor-report.json   # bootstrap CIs per pair
├── noise-floor-report.md     # summary table
├── permutation-control-report.json  # null distribution analysis
└── permutation-control-report.md    # summary table

results/field-test/
├── corpus.csv
├── corpus_part1.csv
├── corpus_part2.csv
├── corpus_part3.csv
├── corpus/
│   ├── pr_review/
│   ├── incident_response/
│   ├── change_management/
│   └── security_incidents/
├── results/
│   └── <model_slug>/<artifact_id>.json
├── pairs/
│   ├── pair3_gpt_mistral/
│   ├── pair5_deepseek_mistral/
│   ├── pair1_gpt_gemini/
│   ├── homogeneous_gpt/
│   └── baseline_gpt/
├── debates/
│   └── <pair_name>/<artifact_id>/
│       ├── report.json
│       └── transcript.jsonl
├── flakiness/
│   └── <pair_name>/<artifact_id>/
│       ├── run1/ ... runN/
└── analysis/
    ├── cross-model-overlap.csv
    ├── distinctness-ratings.csv
    ├── cost-latency.csv
    ├── debate-summary.csv
    ├── ground-truth-comparison.csv
    ├── ground-truth-judged.csv
    └── flakiness-summary.csv
```

## Model Strategy

v0.2.0 uses a 2-model primary strategy instead of a full 4-model matrix:

- **Primary pair:** GPT-4o-mini + Mistral Small 3.2 on all 150 artifacts
- **Validation subsets:** DeepSeek-V3 + Mistral Small 3.2, GPT-4o-mini + GPT-4o-mini
- **Optional negative control:** GPT-4o-mini + Gemini 2.5 Flash

See `docs/field-test/v0.2.0/field-test-plan.md` for the rationale.

## Notes

- Keys are never saved or logged.
- Cost is computed per artifact from token counts.
- Resume is automatic via CHECKPOINT.
- Rate limit: 1s sleep between API calls, 3 retries with backoff.
- All LLM calls go through OpenRouter with a single API key.
