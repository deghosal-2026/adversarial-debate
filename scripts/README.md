# Field Test Scripts — v0.1.0

Scripts to run the AdversarialDebate field test. Run in order.

## Prerequisites

```bash
# 1. gh CLI authenticated (for downloading PRs)
gh auth login

# 2. OpenRouter API key (same key for all LLMs)
export OPENROUTER_API_KEY=sk-or-...

# 3. corpus.csv at results/field-test/v0.1.0/corpus.csv
#    Generate with: python3 scripts/gen_corpus.py --out results/field-test/v0.1.0/corpus.csv
```

## Workflow

### Step 0 — Generate corpus (one-time)

```bash
python3 scripts/gen_corpus.py --out results/field-test/v0.1.0/corpus.csv
```

Creates `corpus.csv` with 150 PRs from 45+ repos across 12+ languages. Fetches real PR data via `gh` CLI.

### Step 1 — Download corpus diffs (one-time)

```bash
python3 scripts/01_download_corpus.py --corpus results/field-test/v0.1.0/corpus.csv

# Re-download everything
python3 scripts/01_download_corpus.py --corpus results/field-test/v0.1.0/corpus.csv --force
```

Downloads PR diffs + metadata from GitHub. Stores under `results/field-test/v0.1.0/corpus/`. Skips already-downloaded PRs.

### Step 2 — Run LLM reviewers (one model at a time)

```bash
# GPT-4o-mini (run independently, resumes from checkpoint)
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.1.0/corpus.csv

# Gemini 2.5 Flash
python3 scripts/02_run_reviewer.py --model google/gemini-2.5-flash --corpus results/field-test/v0.1.0/corpus.csv

# DeepSeek
python3 scripts/02_run_reviewer.py --model deepseek/deepseek-chat --corpus results/field-test/v0.1.0/corpus.csv

# Mistral Small
python3 scripts/02_run_reviewer.py --model mistralai/mistral-small --corpus results/field-test/v0.1.0/corpus.csv
```

Each model runs independently. If one fails, re-run that model — it skips completed PRs via a `CHECKPOINT` file.

**Useful flags:**
```bash
# Test on 5 PRs first (cost control)
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.1.0/corpus.csv --limit 5

# Use mini test corpus
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.1.0/corpus_test.csv

# Dry run (no API calls, shows cost estimate)
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.1.0/corpus.csv --dry-run

# Run a single PR (debugging)
python3 scripts/02_run_reviewer.py --model openai/gpt-4o-mini --corpus results/field-test/v0.1.0/corpus.csv --pr kubernetes_kubernetes_PR12345
```

**Output:** `results/field-test/v0.1.0/results/<model_slug>/<pr_id>.json` — raw LLM response, latency, token counts, computed cost.

### Step 3 — Combine into pairs

```bash
python3 scripts/03_combine_results.py --corpus results/field-test/v0.1.0/corpus.csv
```

Maps individual model outputs into pair configurations:
- `pair1_gpt_gemini` — GPT-4o-mini + Gemini 2.5 Flash
- `pair2_gemini_deepseek` — Gemini 2.5 Flash + DeepSeek
- `pair3_gpt_mistral` — GPT-4o-mini + Mistral Small
- `pair4_gemini_mistral` — Gemini 2.5 Flash + Mistral Small
- `pair5_deepseek_mistral` — DeepSeek + Mistral Small
- `homogeneous_gpt` — GPT-4o-mini both sides
- `baseline_gpt` — GPT-4o-mini single pass (no debate)

### Step 4 — Run debate engine

```bash
python3 scripts/04_run_debate.py --corpus results/field-test/v0.1.0/corpus.csv

# Run a specific pair only
python3 scripts/04_run_debate.py --corpus results/field-test/v0.1.0/corpus.csv --pair pair1_gpt_gemini

# Run a single PR (debugging)
python3 scripts/04_run_debate.py --corpus results/field-test/v0.1.0/corpus.csv --pr kubernetes_kubernetes_PR141554

# Limit PRs (testing)
python3 scripts/04_run_debate.py --corpus results/field-test/v0.1.0/corpus.csv --limit 5
```

Runs the full engine pipeline on paired reviews:
- M5 DebateController (bounded rounds, point-by-point enforcement)
- M6 EvidenceTracker (claim lifecycle, convergence score, theater detection)
- M7 SynthesisReport (verdict/disputed, `would_resolve_if`, flags)

**Output:** `results/field-test/v0.1.0/debates/<pair_name>/<pr_id>/`
- `report.json` — termination reason, convergence score, concessions, unresolved points, theater/capitulation flags, full event log
- `transcript.jsonl` — one JSON line per debate event

### Step 5 — Analyze and compare

```bash
python3 scripts/05_analyze.py
```

Produces:
- `results/field-test/v0.1.0/analysis/cross-model-overlap.csv` — overlap similarity per PR per model pair (substring containment)
- `results/field-test/v0.1.0/analysis/distinctness-ratings.csv` — Issue counts per model per PR
- `results/field-test/v0.1.0/analysis/cost-latency.csv` — Cost, latency, token totals per model
- `results/field-test/v0.1.0/analysis/debate-summary.csv` — Per-PR debate outcomes (verdict, score, theater, concessions)

Prints summary tables to stdout.

## Output Structure

```
results/field-test/v0.1.0/
├── corpus.csv                # input: 150 PRs
├── corpus/                   # downloaded diffs + metadata
├── results/                  # raw LLM outputs (per model, from step 2)
│   ├── openai_gpt-4o-mini/
│   ├── google_gemini-2-5-flash/
│   ├── deepseek_deepseek-chat/
│   └── mistralai_mistral-small/
├── pairs/                    # combined pair data (from step 3)
│   ├── pair1_gpt_gemini/
│   ├── pair2_gemini_deepseek/
│   ├── pair3_gpt_mistral/
│   ├── pair4_gemini_mistral/
│   ├── pair5_deepseek_mistral/
│   ├── homogeneous_gpt/
│   └── baseline_gpt/
├── debates/                  # debate engine output (from step 4)
│   └── <pair_name>/
│       └── <pr_id>/
│           ├── report.json
│           └── transcript.jsonl
├── analysis/                 # analysis CSVs (from step 5)
│   ├── cross-model-overlap.csv
│   ├── distinctness-ratings.csv
│   ├── cost-latency.csv
│   └── debate-summary.csv
└── FIELD_TEST_REPORT.md      # final report (written manually)
```

## Notes

- **Keys are never saved or logged.** `OPENROUTER_API_KEY` is read from env var only.
- **Cost is computed per PR** from token counts using the pricing table in `02_run_reviewer.py`.
- **Resume is automatic.** Steps 2 and 4 skip already-completed PRs.
- **Rate limiting:** 1 second sleep between API calls, 3 retries with backoff on failure.
- **All LLM calls go through OpenRouter** (`openrouter.ai/api/v1`) with a single API key.
