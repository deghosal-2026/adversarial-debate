# #133 — Execute Field Test Sweep: v0.2.1

> Run these commands from the repo root (`/Users/deghosal/Desktop/code/github/adversarial-debate`).
> All results go to `results/field-test/v0.2.1/`.
> Corpus reused from v0.2.0 (150 artifacts, 4 domains).
> Existing model results (GPT-4o-mini, Gemini, Mistral, DeepSeek partial) already copied to v0.2.1.

---

## Step 1: Run DeepSeek on remaining artifacts (parallel)

DeepSeek has 36 of 150 artifacts cached. Need to run the remaining ~114.

Corpus split into 6 parts (25 artifacts each) so you can run in parallel across 6 terminals:

```bash
# Terminal 1 — corpus1
python3 -m scripts.02_run_reviewer \
    --model deepseek/deepseek-chat \
    --corpus results/field-test/v0.2.1/corpus1.csv

# Terminal 2 — corpus2
python3 -m scripts.02_run_reviewer \
    --model deepseek/deepseek-chat \
    --corpus results/field-test/v0.2.1/corpus2.csv

# Terminal 3 — corpus3
python3 -m scripts.02_run_reviewer \
    --model deepseek/deepseek-chat \
    --corpus results/field-test/v0.2.1/corpus3.csv

# Terminal 4 — corpus4
python3 -m scripts.02_run_reviewer \
    --model deepseek/deepseek-chat \
    --corpus results/field-test/v0.2.1/corpus4.csv

# Terminal 5 — corpus5
python3 -m scripts.02_run_reviewer \
    --model deepseek/deepseek-chat \
    --corpus results/field-test/v0.2.1/corpus5.csv

# Terminal 6 — corpus6
python3 -m scripts.02_run_reviewer \
    --model deepseek/deepseek-chat \
    --corpus results/field-test/v0.2.1/corpus6.csv
```

Each processes ~19 new artifacts (25 minus the 6 already cached from v0.2.0).
Wait for all 6 to finish before proceeding to Step 2.

---

## Step 2: Combine results into pairs

Combines all 5 pairs including the new `pair8_deepseek_gpt_mini`.

```bash
python3 -m scripts.03_combine_results \
    --corpus results/field-test/v0.2.1/corpus.csv
```

---

## Step 3: Run debates for the new pair (parallel)

Only `pair8_deepseek_gpt_mini` needs debates — existing pairs are already in the copied v0.2.1 directory.

Run 6 parallel terminals, one per corpus split:

```bash
# Terminal 1 — corpus1
python3 -m scripts.04_run_debate \
    --corpus results/field-test/v0.2.1/corpus1.csv \
    --pair pair8_deepseek_gpt_mini

# Terminal 2 — corpus2
python3 -m scripts.04_run_debate \
    --corpus results/field-test/v0.2.1/corpus2.csv \
    --pair pair8_deepseek_gpt_mini

# Terminal 3 — corpus3
python3 -m scripts.04_run_debate \
    --corpus results/field-test/v0.2.1/corpus3.csv \
    --pair pair8_deepseek_gpt_mini

# Terminal 4 — corpus4
python3 -m scripts.04_run_debate \
    --corpus results/field-test/v0.2.1/corpus4.csv \
    --pair pair8_deepseek_gpt_mini

# Terminal 5 — corpus5
python3 -m scripts.04_run_debate \
    --corpus results/field-test/v0.2.1/corpus5.csv \
    --pair pair8_deepseek_gpt_mini

# Terminal 6 — corpus6
python3 -m scripts.04_run_debate \
    --corpus results/field-test/v0.2.1/corpus6.csv \
    --pair pair8_deepseek_gpt_mini
```

Each processes 25 artifacts. Wait for all 6 to finish before proceeding to Step 4.

---

## Step 4: Run analysis

Re-runs analysis with all 5 pairs, includes seam assertions.

```bash
python3 -m scripts.05_analyze
```

---

## Step 5: Export ground truth

Re-exports ground-truth comparison CSV. Includes seam assertions.

```bash
python3 -m scripts.06_ground_truth \
    --corpus results/field-test/v0.2.1/corpus.csv
```

---

## Step 6: LLM judge

Auto-fills human_judgment column for the new pair.

```bash
python3 -m scripts.07_llm_judge \
    --input results/field-test/v0.2.1/analysis/ground-truth-comparison.csv \
    --output results/field-test/v0.2.1/analysis/ground-truth-judged.csv
```

---

## Step 7: False-negative measurement

Measures missed-issue rate from 70 known-bad PRs.

```bash
python3 -m scripts.09_missed_issues \
    --corpus results/field-test/v0.2.1/corpus.csv \
    --output results/field-test/v0.2.1/analysis/missed-issue-report.csv
```

---

## Step 8: Flakiness sweep

Runs stability test on representative artifacts.

```bash
python3 -m scripts.08_flakiness \
    --corpus results/field-test/v0.2.1/corpus.csv \
    --runs 5 \
    --limit 10
```

---

## Verification

After all steps complete, verify:

```bash
# Check seam assertions all passed (no SEAM FAIL messages in output)
# Check debate summary includes pair8
ls results/field-test/v0.2.1/debates/pair8_deepseek_gpt_mini/

# Check missed-issue report exists
cat results/field-test/v0.2.1/analysis/missed-issue-report.csv

# Check pipeline integrity in analysis output
# Look for "SEAM" messages in step 4-6 output
```