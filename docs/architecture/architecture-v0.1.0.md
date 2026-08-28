# Architecture — AdversarialDebate v0.1.0

> Full spec: pipeline stages, data model, isolation mechanics, provider layer, adapters.
> This is the canonical architecture document referenced throughout the docs.

## Core Components

| # | Component | Responsibility |
|---|-----------|----------------|
| 1 | **Input Normalizer** | Converts PRs, docs, incidents, plans into a common review schema |
| 2 | **Independent Reviewer Engine** | Launches isolated review passes with strict context separation (delayed answer revelation) |
| 3 | **Debate Controller** | Runs bounded structured rebuttal rounds; tracks argument state |
| 4 | **Evidence Tracker** | Stores claims, supporting evidence, unresolved points, concession events |
| 5 | **Synthesis Layer** | Produces a joint decision or a structured disagreement report |
| 6 | **Audit Log** | Persists the full review lineage for inspection |

## Pipeline

```
artifact → Input Normalizer → ReviewArtifact
  → Reviewer A (isolated) + Reviewer B (isolated)
  → Revelation gate opens
  → Debate Controller (bounded rounds)
  → Evidence Tracker
  → Synthesis Layer → Joint Verdict or Disagreement Report
  → Audit Log (SQLite)
```

## Isolation

Reviewer B cannot see reviewer A's output until B has fully committed its own review — and vice versa. This is enforced mechanically: separate conversation contexts, no shared memory, revelation handled by the engine as an explicit state transition (`isolated → revealed`).

## Data Model

See `src/adversarial_debate/schemas/` for the canonical Pydantic model definitions.

## Provider Layer

Model-agnostic registry (config-driven): any OpenAI-compatible endpoint; PydanticAI and LangGraph adapters. Heterogeneous pairs encouraged. Zero paid LLM calls in CI.

## Design Principles

1. Independence before interaction.
2. Disagreement is a feature, not a bug.
3. Preserve minority arguments when they matter.
4. Optimize for auditability, not theatrical conversation.
5. Forced personas are banned.