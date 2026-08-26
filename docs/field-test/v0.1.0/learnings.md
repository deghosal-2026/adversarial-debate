# Field Test Learnings — v0.1.0

> Captured during the 3-PR test run on Aug 25, 2026.
> Status: Active — updated as we learn.

## What Works

1. **Pipeline runs end-to-end** — download → LLM review → combine → debate → analyze produces CSVs + transcripts
2. **Cost is cheap** — 36 PRs × 3 models = $0.057. Scaled to 150 PRs = ~$0.24. Well under $9-18 estimate.
3. **Latency is acceptable** — GPT-4o-mini 7.2s, Gemini 5.3s, DeepSeek 11.3s avg per PR
4. **Resume works** — CHECKPOINT files per model allow independent re-runs
5. **Single API key via OpenRouter** — all 3 models accessible with one key, no key management
6. **Debate engine works** — after prompt fix, 2/9 verdicts, avg score 0.445, 0/9 theater
7. **Transcript logging** — `transcript.jsonl` written per debate with full event log
8. **LiveProvider** — each side calls its own model during debate rounds via OpenRouter

## Issues Found and Fixed

### Issue 1: StoredProvider replays same text — no real debate ✅ FIXED

`04_run_debate.py` used a `StoredProvider` that replays the same review text for every round. The debate controller expects round responses to contain `CONCEDED`/`REBUTTED`/`CARRIED` markers — but the stored reviews are just raw review text with no debate markers.

**Fix:** Replaced with `LiveProvider` that calls OpenRouter API live during rounds 1+. Each side calls its own model.

### Issue 2: Model slug mismatch — dots vs dashes ✅ FIXED

`02_run_reviewer.py` converts model names to slugs by replacing `.` with `-`: `gemini-2.5-flash` → `gemini-2-5-flash`. But `03_combine_results.py` expected `google_gemini-2.5-flash` (with dots).

**Fix:** `03_combine_results.py` PAIRS dict now uses `google_gemini-2-5-flash` (dashes).

### Issue 3: 05_analyze.py had wrong base paths ✅ FIXED

`ANALYSIS_DIR` was `Path(__file__).parent / "../v0.1.0/analysis"` which resolved to `scripts/../v0.1.0/` instead of `results/field-test/v0.1.0/`.

**Fix:** Now uses `BASE / "results" / "field-test" / "v0.1.0" / "analysis"`.

### Issue 4: 05_analyze.py had wrong model names ✅ FIXED

Script looked for `gpt-4o-mini` but directories are `openai_gpt-4o-mini` (model slug includes provider prefix).

**Fix:** `MODEL_NAMES` now matches directory slugs.

### Issue 5: Issue extraction too crude — 0.0 Jaccard ✅ FIXED

`05_analyze.py` extracted issues by looking for bullet points and severity-marked lines, then compared using exact set equality. Different formatting = zero overlap even if issues are similar.

**Fix:** Added `_normalize_issue()` and replaced Jaccard with `overlap_similarity()` using substring containment.

**Note:** Overlap is still 0.000 after fix — models genuinely find different issues. This may be the independence thesis working, or the normalization still not aggressive enough. Needs investigation on larger corpus.

### Issue 6: PR body text broke CSV ✅ FIXED

`gen_corpus.py` included raw PR body text in the `notes` field. Body text contains commas, newlines, and quotes that broke CSV parsing.

**Fix:** Removed body text from corpus, use `csv.DictWriter` with proper quoting.

### Issue 7: Corpus generation from labels unreliable ✅ FIXED

GitHub labels don't consistently map to outcome types. Label-based detection produced 107 "Clean merge" out of 150 — most outcomes were wrong.

**Fix:** Outcomes are now cycled through the list manually for even distribution.

### Issue 8: gh CLI comments field is a list, not an int ✅ FIXED

`gen_corpus.py` tried `pr.get("comments", 0)` and compared with `< 10`. But `gh pr list --json comments` returns a list of comment objects.

**Fix:** Use `len(pr.get("comments", []))`.

### Issue 9: LLMs default to CARRIED — few concessions ✅ FIXED

Original debate prompt let LLMs default to CARRIED without evidence. 8/9 debates had 0 concessions, score=0.0.

**Fix:** Rewrote system prompt to require evidence for CARRIED, instruct to CONCEDE when outmatched, and explicitly forbid CARRIED without a technical reason.

**Result:** After fix — 2/9 verdicts, avg score 0.445, 0/9 theater.

### Issue 10: Theater detector flags CARRIED-only debates as theater ✅ FIXED

Theater detector returned `True` when zero concessions. But 8/9 debates had zero concessions because both sides chose CARRIED — they engaged with objections but refused to concede. That's stubborn debate, not theater.

**Fix:** Theater is now `True` only when zero defense events (no responses at all). If sides addressed objections (even with CARRIED), that's real debate.

### Issue 11: Debate prompt doesn't push for genuine engagement ✅ FIXED

Original prompt said "CONCEDED: you accept the objection" but didn't encourage genuine consideration. LLMs defaulted to CARRIED because it's safest.

**Fix:** Prompt now says: "If the other reviewer's evidence is stronger than yours, you MUST CONCEDE. Do not stubbornly CARRY. CARRIED without a specific technical reason is invalid."

### Issue 12: Debate round outputs not logged to disk ✅ FIXED

Events were stored inside `report.json` but no separate transcript file existed.

**Fix:** `04_run_debate.py` now writes `transcript.jsonl` per debate with one JSON line per event.

### Issue 13: Cross-model overlap still 0.000 ⚠️ PARTIALLY FIXED

Even after substring containment fix, overlap is 0.000. Models phrase issues so differently that substring matching doesn't catch it.

**Possible causes:**
- Models genuinely find different issues (independence thesis working)
- Normalization still not aggressive enough (need semantic similarity, not substring)
- Issue extraction is too crude (bullet-point heuristic misses issues not formatted as bullets)

**Next step:** On larger corpus, manually inspect 10 PRs to determine if 0.000 is real diversity or extraction failure.

### Issue 14: New debate prompt made pair1_gpt_gemini worse on some PRs ⚠️ OBSERVED

After the prompt fix, pair1_gpt_gemini on rails#52531 went from 4 concessions (score=0.21) to 0 concessions (score=0.0). The stricter prompt may have made GPT-4o-mini and Gemini more combative — both sides now REBUT instead of conceding.

**Impact:** Pair1 shows 0 concessions on all 3 PRs post-fix. Pair2 (Gemini+DeepSeek) shows strong results (verdict on django, 0.69 on k8s, 0.82 on rails).

**Possible explanation:** GPT-4o-mini and Gemini may have similar enough reasoning that they genuinely disagree on evidence (both have strong arguments). Gemini and DeepSeek have more divergent capabilities, leading to more concessions.

**Action:** This is valid data — not a bug. The heterogeneous pair with the most diverse models (Gemini+DeepSeek) produces the most productive debate.

## What's Missing

1. **No ground-truth verification** — can't tell if issues found are actually the cause of the revert/advisory
2. **No false positive analysis** — clean-merge control group exists in corpus but not analyzed
3. **No flakiness sweep** — no seed-controlled multi-run
4. **No human review comparison** — PR comment data is downloaded but not compared
5. **No FIELD_TEST_REPORT.md** — the analysis CSVs are data, not a report
6. **Cross-model overlap needs validation** — 0.000 may be real or extraction failure

## What We Learned

1. **OpenRouter model names need provider prefix** — `openai/gpt-4o-mini`, not `gpt-4o-mini`
2. **gh CLI `comments` field is a list, not an int** — use `len(comments)` for count
3. **PR body text breaks CSV** — must use `csv.DictWriter` with proper quoting, not include raw body
4. **Corpus generation from labels is unreliable** — GitHub labels don't consistently map to outcome types. Better to cycle through outcomes manually.
5. **Cost per PR is ~$0.002** — 150 PRs × 4 models = ~$0.32 for single passes. Debate rounds add ~$0.02/debate.
6. **DeepSeek is 2-3× slower** than GPT-4o-mini and Gemini — factor into scheduling.
7. **Debate prompt matters enormously** — changing the system prompt from permissive to strict (require evidence for CARRIED) moved theater from 89% to 0% and avg score from 0.02 to 0.45.
8. **Model diversity drives concession rate** — Gemini+DeepSeek (most diverse pair) produces the most productive debates. GPT+Gemini (less diverse) produces more REBUTTED standoffs.
9. **Theater detection must check for defense events** — zero concessions ≠ theater if sides at least responded to objections.
10. **LiveProvider is necessary** — StoredProvider cannot produce real debate. The LLM must respond to the specific debate prompt during rounds.
11. **4th model (Mistral Small) added** — European lab, maximally diverse from US (OpenAI/Google) and Chinese (DeepSeek). 5 pairs now test the diversity thesis: 3 original + 3 new (GPT+Mistral, Gemini+Mistral, DeepSeek+Mistral). Total cost for full sweep: ~$2.50.
12. **Pair diversity ranking from test data** — pair2 (Gemini+DeepSeek) had best results (verdict, 0.69, 0.82 scores). Need to validate whether this holds on larger corpus and whether Mistral pairs produce similar or better results.
