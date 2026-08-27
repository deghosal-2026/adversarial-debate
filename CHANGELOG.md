# Changelog

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