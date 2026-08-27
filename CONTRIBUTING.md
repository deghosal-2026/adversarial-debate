# Contributing to AdversarialDebate

## Adapter-First Contribution Path

The fastest way to contribute is to write a **domain adapter** — a new normalizer that converts a different input type (architecture review, incident hypothesis, contract clause, change request) into the common review schema.

### Adapter Contract

1. Create a new directory under `src/adversarial_debate/adapters/<domain>/`
2. Implement the normalizer interface (see `src/adversarial_debate/adapters/base.py`)
3. Add a `language.py` that maps file extensions to review rubrics
4. Add fixtures to `tests/fixtures/<domain>/`
5. Wire it into the CLI in `src/adversarial_debate/cli/cli.py`

### Development Setup

```bash
git clone https://github.com/deghosal-2026/adversarial-debate
cd adversarial-debate
make setup
make ci          # lint + typecheck + test (must pass before PR)
```

### CI Gates

Every PR must pass:

- `make lint` — Ruff clean
- `make typecheck` — Mypy strict
- `make cover` — ≥95% test coverage
- Isolation invariant tests green

### PR Guidelines

- One feature or fix per PR
- Include tests for new code
- Update docs/ if adding a new adapter or changing behavior
- No paid-LLM calls in CI tests (use `ScriptedDebateProvider`)

## Code of Conduct

All contributors must follow the [Code of Conduct](CODE_OF_CONDUCT.md).