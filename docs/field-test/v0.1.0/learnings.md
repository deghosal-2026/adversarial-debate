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

### Critical: No Debate Is Happening

The scripts call the LLM API directly and store raw text. The M5 DebateController, M6 EvidenceTracker, and M7 SynthesisReport never run. We have 3 independent single-pass reviews — not a debate.

**Impact:** Cannot test the v0.1.0 thesis (does adversarial debate surface what single review misses?).

**Fix needed:** Add `05_run_debate.py` that takes stored single-pass reviews and feeds them into the engine pipeline:
- Load reviews from `results/<model>/<pr_id>.json`
- Convert to `Review` schema objects
- Run `DebateController` (M5) with the pair's two models
- Run `EvidenceTracker` (M6) on the debate events
- Run `synthesize_verdict` (M7) to produce the report
- Store transcript + report

### Critical: Issue Extraction Is Too Crude

`04_analyze.py` extracts issues by looking for bullet points and severity-marked lines. This produces 0.0 Jaccard similarity across all PRs — not because models find different issues, but because formatting differs.

**Impact:** Cross-model overlap metric is meaningless. Cannot tell if models find the same or different issues.

**Fix needed:** Normalize issue text before comparison:
- Lowercase, strip formatting, remove bullet markers
- Extract the core claim sentence (first sentence after severity marker)
- Compare using substring matching, not exact set equality

### Bug: 04_analyze.py Had Wrong Paths

`ANALYSIS_DIR` was `Path(__file__).parent / "../v0.1.0/analysis"` which resolved to `scripts/../v0.1.0/` instead of `results/field-test/v0.1.0/`.

**Status:** Fixed — now uses `BASE / "results" / "field-test" / "v0.1.0" / "analysis"`.

### Bug: 04_analyze.py Had Wrong Model Names

Script looked for `gpt-4o-mini` but directories are `openai_gpt-4o-mini` (model slug includes provider prefix).

**Status:** Fixed — `MODEL_NAMES` now matches directory slugs.

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
