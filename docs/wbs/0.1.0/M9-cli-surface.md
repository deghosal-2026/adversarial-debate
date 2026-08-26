# M9 — CLI Surface

> Goal: the five commands that make the engine a product — init, review, report, resume, transcript — with terminal rendering that follows the brand palette (amber for disputed, never red except errors). Part of [index](index.md).

## PRD coupling

- [05-features](../../design/prd/05-features.md): F10 (CLI) + [§5.5 API surface sketch](../../design/prd/05-features.md)
- [10-business-case §10.10 time-to-first-value](../../design/prd/10-business-case.md): install → first report in <10 minutes; no signup
- [26-brand-guide §26.5 terminal colors](../../design/prd/26-brand-guide.md): green converged, amber disputed, gray informational, red errors only
- [13-failure-modes §13.3](../../design/prd/13-failure-modes.md): report header surfaces failure-mode flags so users calibrate trust

## Dependencies

Upstream: M8 (store/resume), M7 (reports). Downstream: M10 field test drives everything through this CLI.

## Workstreams & tasks

### WS 9.a — Commands

- [x] T9.1 (#40) `advdeb init`: writes commented `advdeb.toml` (slots A/B examples incl. OpenAI-compatible + Ollama), validates on next run; refuses to overwrite without `--force`
- [x] T9.2 (#41) `advdeb review`: accepts `--pr <url|path>` (URL requires `gh`, degrades gracefully per T4.3 (#20)), `--domain pr_review`, `--rounds`, `--pair diverse|same`, `--budget`; streams progress (passes/rounds/events); exits non-zero on error with actionable message
- [x] T9.3 (#42) `advdeb report <id>`: terminal rendering — verdict banner (green CONVERGED / amber DISPUTED), convergence score + denominator, resolved[], unresolved[] with positions + would_resolve_if, header block (models, prompt versions, seeds, stability-unknown notice per single-run), failure-mode flags ([06 §6.4](../../design/prd/06-security-baseline.md))
- [x] T9.4 (#43) `advdeb transcript <id> --export jsonl [--redact]` and `advdeb list` (recent artifacts): export honors completeness header; `--redact` replaces content blocks with `[REDACTED]` preserving structure
- [x] T9.5 (#44) `advdeb resume <id>`: wires M8 resume; UX pass over all commands — consistent exit codes (0 ok / 1 usage / 2 engine error / 3 budget), no raw tracebacks, `--verbose` for debug

### WS 9.b — DX polish

- [x] T9.6 (#45) Onboarding rehearsal script: fresh venv → pip install -e . → init → scripted-reviewer smoke debate → report; asserted in CI as the "first 10 minutes" test ([10 §10.10](../../design/prd/10-business-case.md))

## Acceptance criteria / exit gate

- Every command has happy-path + failure-path tests; snapshot tests for report rendering (colors stripped in CI)
- Onboarding rehearsal green in CI from clean env
- `--help` outputs reviewed against [26-brand voice](../../design/prd/26-brand-guide.md) (direct, no hype words — lint via banned-word grep)
- Coverage ≥95% on `cli/`

## Explicitly out of scope

HTTP service (v0.5); UI/browser rendering (v0.2); GitHub Action (v0.2).
