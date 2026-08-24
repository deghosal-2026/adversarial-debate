# M4 — Input Normalizer & PR-Review Adapter

> Goal: turn any git diff + PR metadata into a `ReviewArtifact`, with budget-aware chunking for oversized diffs, and a seeded fixture corpus with known issues for tests and the M10 field test. Part of [index](index.md).

## PRD coupling

- [05-features](../../design/prd/05-features.md): F7 (PR-review domain adapter — the only shipping domain)
- [02-architecture §2.8 context-window strategy](../../design/prd/02-architecture.md): chunking, claim dedup fields, context-budget reporting
- [05 §5.3 adapter protocol](../../design/prd/05-features.md): normalizer + rubric + evidence expectations — this milestone is the reference implementation other adapters copy
- [13-failure-modes FM-10](../../design/prd/13-failure-modes.md): adapter must not hallucinate metadata — validated against real diff content

## Dependencies

Upstream: M1 (schemas). Downstream: M5/M6 consume artifacts; M10 consumes fixtures.

## Workstreams & tasks

### WS 4.a — Framework

- [ ] T4.1 Normalizer framework: `Normalizer` protocol (`normalize(raw, hints) -> ReviewArtifact`), registry keyed by domain, plugin-style registration under `adapters/<domain>/`; unknown domain → actionable error listing available domains

### WS 4.b — PR-review adapter

- [ ] T4.2 Git diff parser: unified-diff → `ContentBlock[]` (per-file blocks; hunks preserved; add/remove/context markers); robust to binary files, renames, mode changes; never crashes on malformed hunks (skip + warn)
- [ ] T4.3 PR metadata extractor: accepts local path or GitHub PR URL (via `gh` when available); extracts title/body/files/commit info as metadata; language hints per file extension; missing `gh` → clear degrade-to-local-path message ([FM-10](../../design/prd/13-failure-modes.md): metadata validated against actual diff content)
- [ ] T4.4 Chunking strategy: budget-aware split by file then hunk-group when estimated tokens exceed model window fraction (configurable, default 80%); emits chunk count + per-chunk budget % into artifact metadata (report header feeds from here); claim-dedup keys prepared for cross-chunk merge

### WS 4.c — Fixtures

- [ ] T4.5 Fixture corpus v1: 8-10 seeded diffs modeled on real public-repo patterns — each with `fixtures.json` manifest: known_issues[], expected severity, should_disagree flag, one case where only reviewer B's framing would catch it (M10 exit-bar rehearsal); all synthetic/public-domain, PII-free

## Acceptance criteria / exit gate

- Parser golden tests over tricky diffs (binary/renames/malformed) — zero crashes, warnings surfaced
- Chunker property test: no chunk exceeds configured budget; union of chunks == original content coverage
- Every fixture validates against schema; manifest ↔ content consistency check ([FM-10](../../design/prd/13-failure-modes.md))
- Coverage ≥95% on `adapters/pr_review/` and normalizer framework

## Explicitly out of scope

Claim extraction by LLM (that happens in reviews); other domains (change-management is v0.2).
