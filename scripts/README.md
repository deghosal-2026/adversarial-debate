# Field Test Scripts — v0.2.0

Scripts to run the AdversarialDebate field test. Run in order.

## Prerequisites

```bash
# 1. gh CLI authenticated
gh auth login

# 2. OpenRouter API key (same key for all LLMs)
export OPENROUTER_API_KEY=sk-or-...
```

## Workflow

### Step 0 — Download corpus

PR artifacts are already copied from the v0.1.0 corpus. For non-PR artifacts (incident response, change management, security incidents), download with:

```bash
python3 scripts/01_download_corpus_v2.py

# Download a single domain
python3 scripts/01_download_corpus_v2.py --domain incident_response

# Test on 5 artifacts
python3 scripts/01_download_corpus_v2.py --limit 5
```

Skips PR artifacts automatically. Output: `results/field-test/v0.2.0/corpus/<domain>/<artifact_id>/`.

### Step 1 — Run LLM reviewers (one model at a time)

```bash
# Primary model (run on all 150 artifacts)
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/corpus.csv

# Secondary model
python3 scripts/02_run_reviewer.py --model mistralai/mistral-small-3.2-24b-instruct --corpus results/field-test/v0.2.0/corpus.csv

# Validation subset models
python3 scripts/02_run_reviewer.py --model deepseek/deepseek-chat --corpus results/field-test/v0.2.0/corpus.csv
python3 scripts/02_run_reviewer.py --model google/gemini-2.5-flash --corpus results/field-test/v0.2.0/corpus.csv
```

Each model runs independently. Resume is automatic — completed artifacts are tracked via `CHECKPOINT`.

**Useful flags:**
```bash
# Test on 5 artifacts first
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/corpus.csv --limit 5

# Dry run (no API calls, shows cost estimate)
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/corpus.csv --dry-run

# Run a single artifact (debugging)
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.2.0/corpus.csv --pr etcd-io_etcd_PR22178
```

**Output:** `results/field-test/v0.2.0/results/<model_slug>/<artifact_id>.json`

### Step 2 — Combine into pairs

```bash
python3 scripts/03_combine_results.py --corpus results/field-test/v0.2.0/corpus.csv
```

Maps individual model outputs into pair configurations. v0.2.0 uses 2 primary pairs plus subset controls:

| Pair | Slot A | Slot B | Coverage |
|------|--------|--------|----------|
| `pair3_gpt_mistral` | GPT-4o-mini | Mistral Small 3.2 | All 150 artifacts |
| `pair5_deepseek_mistral` | DeepSeek-V3 | Mistral Small 3.2 | 30-40 artifact validation subset |
| `pair1_gpt_gemini` | GPT-4o-mini | Gemini 2.5 Flash | Optional 20-30 negative control |
| `homogeneous_gpt` | GPT-4o-mini | GPT-4o-mini | 30-40 artifact control subset |
| `baseline_gpt` | GPT-4o-mini | — | Single pass baseline |

### Step 3 — Run debate engine

```bash
python3 scripts/04_run_debate.py --corpus results/field-test/v0.2.0/corpus.csv

# Run a specific pair only
python3 scripts/04_run_debate.py --corpus results/field-test/v0.2.0/corpus.csv --pair pair3_gpt_mistral

# Run a single artifact
python3 scripts/04_run_debate.py --corpus results/field-test/v0.2.0/corpus.csv --pr etcd-io_etcd_PR22178

# Limit artifacts (testing)
python3 scripts/04_run_debate.py --corpus results/field-test/v0.2.0/corpus.csv --limit 5
```

**Output:** `results/field-test/v0.2.0/debates/<pair_name>/<artifact_id>/`
- `report.json` — termination reason, convergence score, concessions, unresolved points, flags
- `transcript.jsonl` — one JSON line per debate event

### Step 4 — Analyze and compare

```bash
python3 scripts/05_analyze.py
```

Produces:
- `results/field-test/v0.2.0/analysis/cross-model-overlap.csv`
- `results/field-test/v0.2.0/analysis/distinctness-ratings.csv`
- `results/field-test/v0.2.0/analysis/cost-latency.csv`
- `results/field-test/v0.2.0/analysis/debate-summary.csv`

### Step 5 — Ground-truth verification (PRs only)

```bash
python3 scripts/06_ground_truth.py --corpus results/field-test/v0.2.0/corpus.csv --output analysis/ground-truth-comparison.csv
python3 scripts/07_llm_judge.py --model openai/gpt-4o-mini --workers 10 --input analysis/ground-truth-comparison.csv --output analysis/ground-truth-judged.csv
```

### Step 6 — Flakiness sweep

```bash
python3 scripts/08_flakiness.py --corpus results/field-test/v0.2.0/corpus.csv --runs 5 --limit 12
```

### Step 7 — Expert ratings (non-PR domains only)

Incident response, change management, and security incidents use expert-rater triad scoring instead of ground-truth validation:

1. **Distinctness** — is the second side's concern materially different?
2. **Actionability** — is the `would_resolve_if` path specific enough?
3. **Decision impact** — would this change or delay your conclusion?

## Output Structure

```
results/field-test/v0.2.0/
├── corpus.csv                # input: 150 artifacts (merged from 4 CSVs)
├── corpus/                   # downloaded content per artifact
│   ├── pr_review/            # copied from v0.1.0
│   ├── incident_response/
│   ├── change_management/
│   └── security_incidents/
├── results/                  # raw LLM outputs (per model)
│   └── <model_slug>/<artifact_id>.json
├── pairs/                    # combined pair data
│   ├── pair3_gpt_mistral/
│   ├── pair5_deepseek_mistral/
│   ├── pair1_gpt_gemini/     # subset only
│   ├── homogeneous_gpt/      # subset only
│   └── baseline_gpt/
├── debates/                  # debate engine output
│   └── <pair_name>/
│       └── <artifact_id>/
│           ├── report.json
│           └── transcript.jsonl
├── flakiness/                # sweep runs
│   └── <pair_name>/
│       └── <artifact_id>/
│           ├── run1/ ... runN/
├── analysis/                 # analysis CSVs
│   ├── cross-model-overlap.csv
│   ├── distinctness-ratings.csv
│   ├── cost-latency.csv
│   ├── debate-summary.csv
│   ├── ground-truth-comparison.csv
│   ├── ground-truth-judged.csv
│   └── flakiness-summary.csv
```

## v0.2.0 Model Strategy

Instead of running a full 4-model matrix, v0.2.0 uses a **2-model primary strategy**:

- **Primary pair:** GPT-4o-mini + Mistral Small 3.2 on all 150 artifacts
- **Validation subsets** (30-40 artifacts): DeepSeek-V3 + Mistral Small 3.2, GPT-4o-mini + GPT-4o-mini
- **Optional negative control:** GPT-4o-mini + Gemini 2.5 Flash

See `docs/field-test/v0.2.0/field-test-plan.md` for the full rationale.

## v0.1.0 Scripts

The original v0.1.0 pipeline (`01_download_corpus.py`, `gen_corpus.py`) still exists under `scripts/` and is documented below for reference. It is not needed for the v0.2.0 field test.

```bash
# v0.1.0: Generate and download PR-only corpus
python3 scripts/gen_corpus.py --out results/field-test/v0.1.0/corpus.csv
python3 scripts/01_download_corpus.py --corpus results/field-test/v0.1.0/corpus.csv

# v0.1.0 pairs (full 4-model matrix)
python3 scripts/03_combine_results.py --corpus results/field-test/v0.1.0/corpus.csv
```

## Notes

- **Keys are never saved or logged.** `OPENROUTER_API_KEY` is read from env var only.
- **Cost is computed per artifact** from token counts using the pricing table in `02_run_reviewer.py`.
- **Resume is automatic.** Steps 2 and 4 skip already-completed artifacts.
- **Rate limiting:** 1 second sleep between API calls, 3 retries with backoff on failure.
- **All LLM calls go through OpenRouter** (`openrouter.ai/api/v1`) with a single API key.