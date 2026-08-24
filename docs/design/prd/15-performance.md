# 15 — Performance & Scale Targets

> Sub-document of the [Design overview](../README.md). Soft SLAs buyers need to plan deployment. These are *targets*, not guarantees — LLM latency depends on the user's chosen providers.

## 15.1 Latency targets (per artifact)

| Artifact size | Target wall-clock | Breakdown |
|---------------|-------------------|-----------|
| Small PR (<200 lines) | <90 seconds | ~30s independent passes (parallel) + ~30s 2 debate rounds + ~15s synthesis |
| Medium PR (200-2000 lines) | <5 minutes | Chunking adds ~60s; debate on merged claims |
| Large PR (>2000 lines) | <15 minutes | Hierarchical chunking; may exceed single-context — chunk budget reported |
| Contract (50-200 pages) | <10 minutes | Clause-group chunking; cross-reference resolution adds overhead |

**Note:** these assume frontier-tier API models. Local models (Ollama, vLLM) will be slower; the engine reports actual latency in every report header.

## 15.2 Cost ceilings (per artifact class)

| Class | Default pair | Target cost | Mechanism |
|-------|-------------|-------------|-----------|
| Routine (low-risk PR, standard CR) | Cheap pair (e.g., Haiku + Flash) | <$0.05 | Cost tiering: cheap pair for first pass; frontier pair only if first-round disagreement |
| Standard (medium-risk PR, contract review) | Mid-tier pair | <$0.50 | Budget ceiling per artifact; partial report if exhausted |
| High-stakes (security PR, MSA before signature) | Frontier pair | <$5.00 | No ceiling — buyer opts in via `--no-budget-limit` |

**Engine behavior on budget exhaustion:** debate pauses at the current round; engine emits a `partial` disagreement report labeled `incomplete: budget_exhausted`. Never silent truncation.

## 15.3 Throughput targets (batch mode)

| Mode | Target | Bottleneck |
|------|--------|------------|
| CLI single artifact | 1 debate at a time | Provider rate limits |
| Batch CLI (`advdeb review --batch dir/`) | 10 concurrent debates | Configurable concurrency; bounded by provider rate limits |
| HTTP service | 50 concurrent debates | FastAPI worker pool; SQLite write-lock is the ceiling (Postgres removes this in v0.3) |

## 15.4 What we do NOT promise

- **Real-time** (<10s) — debate is inherently multi-round; if you need real-time, use a single-reviewer tool.
- **Deterministic latency** — LLM providers have variable response times; we report actual, not estimated.
- **Unlimited scale on SQLite** — SQLite handles ~50 concurrent debates; beyond that, Postgres (v0.3) is the answer.
