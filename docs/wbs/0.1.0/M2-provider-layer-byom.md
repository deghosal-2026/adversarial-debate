# M2 — Provider Layer (BYOM Registry)

> Goal: config-driven model registry so any OpenAI-compatible endpoint, PydanticAI or LangGraph model can fill reviewer slots A/B — with seed control and hermetic scripted reviewers for CI. Part of [index](index.md).

## PRD coupling

- [05-features](../../design/prd/05-features.md): F8 (BYOM registry — heterogeneous pairs supported)
- [02-architecture §2.5 provider layer](../../design/prd/02-architecture.md): model-agnostic registry; heterogeneous default; zero paid LLM in CI
- [06-security §6.4 reproducibility](../../design/prd/06-security-baseline.md): per-call seed + `prompt_version` stamped into every payload/log
- [10-business-case §10.2 BYOM unlock](../../design/prd/10-business-case.md): this milestone *is* the procurement unlock

## Dependencies

Upstream: M1 (config, schemas). Downstream: M5 (controller drives reviewers via this layer).

## Workstreams & tasks

### WS 2.a — Registry & transports

- [ ] T2.1 (#8) ProviderRegistry: TOML slots A/B → provider instances; validates heterogeneous vs same-family; exposes `pair_mode` (`diverse|same`); clear errors for missing key-env
- [ ] T2.2 (#9) OpenAI-compatible transport: chat completions; connect/read timeouts; exponential-backoff retries on 429/5xx (jitter); structured-output mode (JSON schema response_format) with fallback
- [ ] T2.3 (#10) PydanticAI adapter: wrap a PydanticAI model as a reviewer backend honoring the same ReviewRequest/ReviewResult contract as T2.2 (#9)

### WS 2.b — Adapters & determinism

- [ ] T2.4 (#11) LangGraph adapter: wrap a LangGraph chat model node as a reviewer backend (same contract)
- [ ] T2.5 (#12) Seed + prompt-version plumbing: every call passes `seed`, stamps `prompt_version`; both recorded in returned metadata (feeds M8 transcripts and flakiness sweeps)
- [ ] T2.6 (#13) ScriptedReviewer: deterministic test double implementing the reviewer contract from canned YAML scenarios — including malformed-output cases (feeds fail-closed tests in M7); CI uses ONLY these

## Acceptance criteria / exit gate

- Same config runs against real endpoint locally and ScriptedReviewer in CI with zero code change
- Retry/backoff unit tests simulated (no network)
- Seed+prompt_version present on every call result (tested)
- Heterogeneous/same validation tested; misconfig produces actionable error naming the offending slot
- Coverage ≥95% on `providers/`

## Explicitly out of scope

Tool access for reviewers ([DD-07](../../design/prd/12-design-decisions.md)); streaming; vLLM-specific tuning.
