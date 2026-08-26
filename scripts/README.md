# Field Test Scripts — v0.1.0

Scripts to run the AdversarialDebate field test. Run in order.

## Prerequisites

```bash
# 1. gh CLI authenticated (for downloading PRs)
gh auth login

# 2. OpenRouter API key (same key for all LLMs)
export OPENROUTER_API_KEY=sk-or-...

# 3. corpus.csv created at results/field-test/v0.1.0/corpus.csv
```

## Workflow

### Step 1 — Download corpus (one-time)

```bash
python3 scripts/01_download_corpus.py

# Re-download everything
python3 scripts/01_download_corpus.py --force

# Custom corpus path
python3 scripts/01_download_corpus.py --corpus path/to/corpus.csv
```

Downloads PR diffs + metadata from GitHub via `gh` CLI. Stores under `results/field-test/v0.1.0/corpus/`. Skips already-downloaded PRs.

### Step 2 — Run LLM reviewers (one model at a time)

```bash
# GPT-4o-mini (run independently, resumes from checkpoint)
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini

# Gemini 2.5 Flash
python3 scripts/02_run_reviewer.py --model google/gemini-2.5-flash

# DeepSeek
python3 scripts/02_run_reviewer.py --model deepseek/deepseek-chat
```

Each model runs independently. If one fails, just re-run that model — it skips already-completed PRs via a `CHECKPOINT` file.

**Useful flags:**
```bash
# Test on 5 PRs first (cost control)
python3 02_run_reviewer.py --model openai/gpt-4o-mini --limit 5

# Dry run (no API calls, just shows what would run + cost estimate)
python3 02_run_reviewer.py --model openai/gpt-4o-mini --dry-run

# Run a single PR (debugging)
python3 02_run_reviewer.py --model openai/gpt-4o-mini --pr kubernetes_kubernetes_PR12345
```

**Output:** `results/field-test/v0.1.0/results/<model_slug>/<pr_id>.json`

Each JSON contains: raw LLM response, latency, token counts, computed cost.

### Step 3 — Combine into pairs

```bash
python3 scripts/03_combine_results.py
```

Maps individual model outputs into the pair configurations defined in the field test plan:
- `pair1_gpt_gemini` — GPT-4o-mini + Gemini 2.5 Flash
- `pair2_gemini_deepseek` — Gemini 2.5 Flash + DeepSeek
- `homogeneous_gpt` — GPT-4o-mini both sides
- `baseline_gpt` — GPT-4o-mini single pass (no debate)

Reports missing results per pair. Re-run step 2 for any missing models.

### Step 4 — Analyze and compare

```bash
python3 scripts/04_analyze.py
```

Produces:
- `results/field-test/v0.1.0/analysis/cross-model-overlap.csv` — Jaccard similarity per PR per model pair
- `results/field-test/v0.1.0/analysis/distinctness-ratings.csv` — Issue counts per model per PR
- `results/field-test/v0.1.0/analysis/cost-latency.csv` — Cost, latency, token totals per model

Prints a summary table to stdout.

## Output Structure

```
results/field-test/v0.1.0/
├── corpus.csv                # input: 150 PRs
├── corpus/                   # downloaded diffs + metadata
│   ├── <repo>_PR<num>.diff
│   └── <repo>_PR<num>.json
├── results/                  # raw LLM outputs (per model)
│   ├── openai_gpt-4o-mini/
│   │   ├── <pr_id>.json
│   │   └── CHECKPOINT
│   ├── google_gemini-2.5-flash/
│   └── deepseek_deepseek-chat/
├── pairs/                    # combined pair data
│   ├── pair1_gpt_gemini/
│   ├── pair2_gemini_deepseek/
│   ├── homogeneous_gpt/
│   └── baseline_gpt/
├── analysis/                 # analysis CSVs
│   ├── cross-model-overlap.csv
│   ├── distinctness-ratings.csv
│   └── cost-latency.csv
└── FIELD_TEST_REPORT.md      # final report (written manually)
```

## Notes

- **Keys are never saved or logged.** `OPENROUTER_API_KEY` is read from env var only.
- **Cost is computed per PR** from token counts using the pricing table in `02_run_reviewer.py`.
- **Resume is automatic.** Each model tracks completed PRs in a `CHECKPOINT` file.
- **Rate limiting:** 1 second sleep between API calls, 3 retries with backoff on failure.
- **All LLM calls go through OpenRouter** (`openrouter.ai/api/v1`) with a single API key.
