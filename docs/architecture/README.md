# Architecture — AdversarialDebate

> System architecture, component spec, and DB schema. The canonical `architecture-v0.1.0.md` is authored at **AD-M1** (PRD/spec/architecture milestone).

## Core Components (locked direction, v0.1.0)

| # | Component | Responsibility |
|---|-----------|----------------|
| 1 | **Input Normalizer** | Converts PRs, docs, incidents, plans into a common review schema |
| 2 | **Independent Reviewer Engine** | Launches isolated review passes with strict context separation (delayed answer revelation) |
| 3 | **Debate Controller** | Runs bounded structured rebuttal rounds; tracks argument state |
| 4 | **Evidence Tracker** | Stores claims, supporting evidence, unresolved points, concession events |
| 5 | **Synthesis Layer** | Produces a joint decision or a structured disagreement report |
| 6 | **Audit Log** | Persists the full review lineage for inspection |

## Design Principles

- **Independence before interaction** — reviewer B cannot see reviewer A's output until it has fully committed its own.
- **Disagreement is a feature, not a bug** — no forced synthetic consensus.
- **Preserve minority arguments when they matter** — dissent survives into the report.
- **Optimize for auditability, not theatrical conversation** — every claim traceable.

## Planned Documents

- `architecture-v0.1.0.md` — full spec: pipeline stages, data model, isolation mechanics, provider layer, adapters (authored) ✓
