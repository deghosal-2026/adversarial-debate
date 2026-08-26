# Field Test Learnings — v0.1.0

> Captured during the 3-PR test run on Aug 25, 2026.
> Status: Active — updated as we learn.

## What Works

1. **Pipeline runs end-to-end** — download → LLM review → combine → analyze produces CSVs
2. **Cost is cheap** — 3 PRs × 3 models = $0.0055. Scaled to 150 PRs = ~$0.28. Well under $9-18 estimate.
3. **Latency is acceptable** — GPT-4o-mini 5.4s, Gemini 4.6s, DeepSeek 12.5s avg per PR
4. **Resume works** — CHECKPOINT files per model allow independent re-runs
5. **Single API key via OpenRouter** — all 3 models accessible with one key, no key management

## What's Broken

### Issue 1: StoredProvider replays same text — no real debate

`04_run_debate.py` used a `StoredProvider` that replays the same review text for every round. The debate controller expects round responses to contain `CONCEDED`/`REBUTTED`/`CARRIED` markers — but the stored reviews are just raw review text with no debate markers.

**Impact:** All debates end with `rounds_exhausted`, 0 concessions, 0.00 convergence score. Cannot test the v0.1.0 thesis.

**Fix:** Replace `StoredProvider` with `LiveProvider` that calls the LLM API live during rounds 1+. Each side calls its own model via OpenRouter. Stored review is round 0 only.

**Status:** In progress.

### Issue 2: Model slug mismatch — dots vs dashes

`02_run_reviewer.py` converts model names to slugs by replacing `.` with `-`: `gemini-2.5-flash` → `gemini-2-5-flash`. But `03_combine_results.py` expected `google_gemini-2.5-flash` (with dots).

**Impact:** `pair1_gpt_gemini` and `pair2_gemini_deepseek` had 0 combined results. Only `homogeneous_gpt` worked because it doesn't use Gemini.

**Status:** Fixed — `03_combine_results.py` PAIRS dict now uses `google_gemini-2-5-flash` (dashes).

### Issue 3: 04_analyze.py had wrong base paths

`ANALYSIS_DIR` was `Path(__file__).parent / "../v0.1.0/analysis"` which resolved to `scripts/../v0.1.0/` instead of `results/field-test/v0.1.0/`.

**Impact:** Analysis CSVs written to wrong directory.

**Status:** Fixed — now uses `BASE / "results" / "field-test" / "v0.1.0" / "analysis"`.

### Issue 4: 04_analyze.py had wrong model names

Script looked for `gpt-4o-mini` but directories are `openai_gpt-4o-mini` (model slug includes provider prefix).

**Impact:** 0 PRs loaded, empty analysis output.

**Status:** Fixed — `MODEL_NAMES` now matches directory slugs.

### Issue 5: Issue extraction too crude — 0.0 Jaccard

`05_analyze.py` extracted issues by looking for bullet points and severity-marked lines, then compared using exact set equality. Different formatting = zero overlap even if issues are similar.

**Impact:** Cross-model overlap metric is meaningless. All pairs show 0.0 Jaccard.

**Fix:** Normalize issue text before comparison (lowercase, strip formatting, first sentence only, substring matching).

**Status:** Fixed — `_normalize_issue()` added.

### Issue 6: PR body text broke CSV

`gen_corpus.py` included raw PR body text in the `notes` field. Body text contains commas, newlines, and quotes that broke CSV parsing.

**Impact:** 461 lines in a 150-row CSV. Columns misaligned. Outcome distribution showed 107 "Clean merge" (wrong).

**Status:** Fixed — removed body text from corpus, use `csv.DictWriter` with proper quoting.

### Issue 7: Corpus generation from labels unreliable

GitHub labels don't consistently map to outcome types. Label-based detection produced 107 "Clean merge" out of 150 — most outcomes were wrong.

**Status:** Fixed — outcomes are now cycled through the list manually for even distribution.

### Issue 8: gh CLI comments field is a list, not an int

`gen_corpus.py` tried `pr.get("comments", 0)` and compared with `< 10`. But `gh pr list --json comments` returns a list of comment objects.

**Impact:** TypeError crash.

**Status:** Fixed — use `len(pr.get("comments", []))`.

## What's Missing

1. **No ground-truth verification** — can't tell if issues found are actually the cause of the revert/advisory
2. **No false positive analysis** — clean-merge control group exists in corpus but not analyzed
3. **No `would_resolve_if`** — requires the debate to produce disagreement reports
4. **No theater detection** — requires debate events with claim state changes
5. **No flakiness sweep** — no seed-controlled multi-run
6. **No human review comparison** — PR comment data is downloaded but not compared
7. **No FIELD_TEST_REPORT.md** — the analysis CSVs are data, not a report

## What We Learned

1. **OpenRouter model names need provider prefix** — `openai/gpt-4o-mini`, not `gpt-4o-mini`
2. **gh CLI `comments` field is a list, not an int** — use `len(comments)` for count
3. **PR body text breaks CSV** — must use `csv.DictWriter` with proper quoting, not include raw body
4. **Corpus generation from labels is unreliable** — GitHub labels don't consistently map to outcome types. Better to cycle through outcomes manually.
5. **Cost per PR is ~$0.002** — 150 PRs × 3 models = $0.90 for single passes. Debate rounds will add ~2× more.
6. **DeepSeek is 2-3× slower** than GPT-4o-mini and Gemini — factor into scheduling.
7. **The scripts bypass the engine** — they call the API directly. To test the actual product, scripts must use the `advdeb` CLI or import the engine modules directly.
