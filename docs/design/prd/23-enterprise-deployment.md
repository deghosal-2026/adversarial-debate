# 23 — Enterprise Deployment Guide

> Sub-document of the [Design overview](../README.md). How to deploy AdversarialDebate in air-gapped, VPC, and on-prem configurations. For buyers whose data cannot leave their boundary.

## 23.1 Deployment topologies

```
Topology 1: Local CLI (developer machine)
  artifact → engine → user's API keys → cloud LLM provider
  Use: individual developer, OSS contributor

Topology 2: CI pipeline (GitHub Actions / GitLab CI)
  PR event → engine in CI runner → cloud or self-hosted LLM
  Use: team-level PR review automation

Topology 3: VPC deployment (enterprise)
  PR/contract → engine in VPC → LLM endpoint inside VPC (vLLM / Azure OpenAI private endpoint)
  Use: enterprise with data-residency requirements; artifacts never leave VPC

Topology 4: Air-gapped (regulated)
  artifact → engine on-prem → local model (Ollama / vLLM on GPU box)
  Use: government, defense, healthcare — no external network access
```

## 23.2 Self-hosted model configuration

### vLLM (recommended for GPU-equipped on-prem)

```toml
# advdeb.toml
[reviewer_a]
provider = "openai_compatible"
base_url = "http://vllm-server:8000/v1"
model = "meta-llama/Llama-3.1-70B-Instruct"
api_key = "local"  # vLLM doesn't require real key

[reviewer_b]
provider = "openai_compatible"
base_url = "http://vllm-server:8001/v1"
model = "Qwen/Qwen2.5-72B-Instruct"  # different family = heterogeneous pair
api_key = "local"
```

### Ollama (for smaller models / development)

```toml
[reviewer_a]
provider = "openai_compatible"
base_url = "http://localhost:11434/v1"
model = "llama3.1:70b"
api_key = "ollama"  # Ollama doesn't require a real key

[reviewer_b]
provider = "openai_compatible"
base_url = "http://localhost:11434/v1"
model = "qwen2.5:72b"
api_key = "ollama"
```

> **Note:** These use the `openai_compatible` provider type, which works with any OpenAI-compatible API (including Ollama and vLLM). The provider registry supports `openai_compatible`, `scripted`, `pydantic_ai`, and `langgraph`.

### Azure OpenAI (private endpoint)

```toml
[reviewer_a]
provider = "openai_compatible"
base_url = "https://my-private.openai.azure.com/openai/deployments/gpt-4o-reviewer-a"
model = "gpt-4o"
api_key = "${AZURE_OPENAI_KEY_A}"

[reviewer_b]
provider = "openai_compatible"
base_url = "https://my-private.openai.azure.com/openai/deployments/gpt-4o-reviewer-b"
model = "gpt-4o"
api_key = "${AZURE_OPENAI_KEY_B}"
```

> **Note:** Azure OpenAI uses the OpenAI-compatible API under the hood. Use the `openai_compatible` provider type with your Azure endpoint and deployment name as the model.

## 23.3 Air-gapped considerations

| Concern | Solution |
|---------|----------|
| No pip install | Ship as Docker image with all deps pre-installed; `docker load < adversarial-debate.tar` |
| No model download | Pre-load model weights into vLLM/Ollama image; ship as separate container |
| No telemetry (already default) | Confirmed: no outbound network calls except to configured LLM endpoints |
| No GitHub access | Git clone on connected machine → `git bundle` → transfer → `git clone bundle` |
| Updates | Quarterly Docker image release; SHA-256 verified; changelog with security fixes |

## 23.4 Authentication & access control (v0.5.0+)

- HTTP service supports API key auth (`Authorization: Bearer <key>`)
- Role-based access: `runner` (submit/review), `reader` (read reports only), `admin` (manage config)
- Audit log records who submitted what artifact and who read which report
- v1.0.0: SSO integration (SAML, OIDC) for enterprise identity providers

## 23.5 High availability (v0.8.0+)

- Stateless engine — all state in SQLite (v0.1) or Postgres (v0.8)
- Horizontal scaling: multiple engine instances behind load balancer, shared Postgres
- Debate state is per-artifact (locked) — no cross-instance coordination needed
- Health check endpoint: `GET /health` → `{"status": "ok", "version": "0.8.0", "db": "connected"}`
