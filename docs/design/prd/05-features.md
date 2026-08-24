# 05 — Features (What v0.1.0 Ships)

> Sub-document of the [Design overview](../README.md). Feature list for v0.1.0 — must-have vs nice-to-have — plus explicit exclusions.

## 5.1 Must-have (v0.1.0)

| # | Feature | Notes |
|---|---------|-------|
| F1 | **Independent dual-review pass** | Two isolated reviewer sessions per artifact; engine-enforced context separation |
| F2 | **Delayed answer revelation** | Explicit state transition `isolated → revealed`; provable from audit log |
| F3 | **Structured debate schema** | First-class `Claim`, `Objection`, `Concession`, `UnresolvedPoint` objects |
| F4 | **Bounded debate rounds** | Default 2 rounds; mandatory point-by-point response to outstanding objections; configurable cap |
| F5 | **Converged-verdict output** | Joint decision + strongest surviving arguments from each side |
| F6 | **Disagreement-report output** | `resolved[]`, `unresolved[].position_a/position_b/would_resolve_if` |
| F7 | **PR-review domain adapter** | Git diff + metadata → `ReviewArtifact`; the one shipping domain |
| F8 | **Bring-your-own-model registry** | Config-driven provider registry; any OpenAI-compatible endpoint; PydanticAI + LangGraph adapters; heterogeneous pairs supported |
| F9 | **Transcript storage** | SQLite persistence of full lineage: every LLM call, claim event, concession, verdict; JSONL export |
| F10 | **CLI** | `advdeb review`, `advdeb report <artifact-id>`, `advdeb init` |
| F11 | **Basic review UI** | Side-by-side A/B reviews with agreement/disagreement highlighting; debate timeline showing concessions and unresolved threads |
| F12 | **Hermetic test suite** | Scripted reviewers in CI; zero paid LLM calls; coverage gate ≥95% target |

## 5.2 Nice-to-have (stretch for 0.1.0, first candidates for 0.2.0)

- GitHub Action wrapper for PR-review adapter
- Debate-usefulness score ("did anything change?") surfaced in reports
- Heterogeneous pairing presets (`--pair diverse`) and same-model mode flag
- Convergence-threshold tuning per artifact severity class
- Cost tiering config (cheap pair default → frontier pair on dispute)
- Redaction hooks for transcripts

## 5.3 Adapter contribution protocol (design direction, no code in v0.1)

Each domain adapter is a spec and an implementation — no engine changes required to add a new domain:

1. **Artifact normalizer** — converts domain-specific input (git diff, contract PDF, CR ticket) → `ReviewArtifact` schema (content blocks, metadata, domain tags).
2. **Claim extraction rubric** — tells the reviewer *what constitutes a relevant claim* in this domain (e.g., for contracts: "find uncapped liabilities"; for CRs: "find missing rollback steps").
3. **Evidence expectations** — what counts as evidence in this domain (code diff lines, contract clause cross-references, ticket timeline entries).
4. **No engine changes required** — adapters sit in `adversarial_debate/adapters/<domain>/`; the engine routes `ReviewArtifact` through the generic loop regardless of domain tag.

Anyone writing a new domain adapter can do so without modifying a single line of engine code. The protocol spec ships as a design document in v0.1; the first external adapter (change management) validates it in v0.2.

## 5.4 Mid-debate human injection (scoped to v0.2)

Users in CAB, incident response, and legal workflows ask: *"Can I interrupt the debate to ask both reviewers a clarifying question?"* This is valuable during live decisions but adds complexity:

- **v0.1 stance:** human reads the final report only. Reports include `would_resolve_if` — the question is asked post-hoc.
- **v0.2 commitment:** optional human-injection turn: at any debate round, a human operator can submit a clarifying question that both reviewers must address. The question (and human's identity) are logged as part of the audit trail.

## 5.5 Explicitly out of scope for v0.1.0

- N-agent jury orchestration (→ AgentJury companion project)
- Fully automated production action based on debate outcome — output is advisory to humans
- Additional domain adapters beyond PR review (change-management adapter is the planned second)
- Fine-tuning or training of any model
- Hosted multi-tenant service
