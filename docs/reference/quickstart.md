# Quickstart

## Installation

```bash
pip install adversarial-debate
```

## Configure

```bash
advdeb init
```

Edit `advdeb.toml` to add your LLM provider API keys:

```toml
[providers.a]
type = "openai_compatible"
model = "gpt-4o-mini"
key_env = "OPENAI_API_KEY"

[providers.b]
type = "openai_compatible"
model = "gemini-2.5-flash"
key_env = "GEMINI_API_KEY"
```

## Review a PR

```bash
advdeb review \
  --pr https://github.com/kubernetes/kubernetes/pull/140860 \
  --domain pr_review \
  --store ./debates.db
```

The engine:
1. Fetches the PR diff
2. Sends it to reviewer A in isolation
3. Sends the same diff to reviewer B in isolation (no peeking)
4. Opens the revelation gate — both reviews are revealed
5. Runs bounded debate rounds (default 2)
6. Produces a verdict or disagreement report

## View Results

```bash
# List runs
advdeb list --store ./debates.db

# View a report
advdeb report <run_id> --store ./debates.db

# Export transcript
advdeb transcript <run_id> --store ./debates.db --export jsonl

# With redaction for sensitive content
advdeb transcript <run_id> --store ./debates.db --export jsonl --redact
```

## Resume a Partial Run

If a debate is interrupted (e.g., provider outage), resume from the last completed round:

```bash
advdeb resume <run_id> --store ./debates.db
```

## Using Scripted Providers (No API Key)

For testing without API keys, use `scripted` providers:

```toml
[providers.a]
type = "scripted"
model = "test"
key_env = "MISSING"

[providers.b]
type = "scripted"  
model = "test"
key_env = "MISSING"
```

## Next Steps

- [Architecture](docs/architecture/architecture-v0.1.0.md)
- [PRD overview](docs/design/README.md)
- [Example reports](results/field-test/v0.1.0/)