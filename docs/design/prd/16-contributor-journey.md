# 16 — Contributor Journey

> Sub-document of the [Design overview](../README.md). How a contributor goes from fork to merged PR. OSS projects die without this path being clear and low-friction.

## 16.1 The four contribution types

| Type | Skill required | Effort | Example |
|------|---------------|--------|---------|
| **Adapter** | Domain knowledge (contracts, CRs, claims) + basic Python | Medium | `adapters/itsm/` — change-request normalizer + rubric |
| **Engine** | Python, async, Pydantic, testing | High | Fix isolation-leakage bug in reviewer engine |
| **Fixtures** | Domain knowledge only — no code | Low | Add 5 seeded contract artifacts with known issues |
| **Docs / rubrics** | Domain expertise | Low | Write the claim-extraction rubric for insurance claims |

## 16.2 Adapter contribution path (the most common)

```
1. Read docs/design/prd/05-features.md §5.3 (adapter protocol)
2. Fork the repo
3. cp -r adapters/pr_review/ adapters/<your_domain>/
4. Implement 3 files:
   - normalizer.py    (artifact → ReviewArtifact)
   - rubric.py        (claim extraction rules, evidence expectations)
   - __init__.py      (adapter metadata: domain name, version, description)
5. Add fixtures: tests/fixtures/<your_domain>/ (3-5 artifacts with known issues)
6. Run: pytest tests/adapters/test_<your_domain>.py
7. Add docs: docs/design/prd/04-users-and-cujs.md row (if new vertical)
8. PR with title: "adapter: <domain name>"
```

**Review criteria for adapter PRs:**
- Normalizer produces valid `ReviewArtifact` (schema-validated)
- Rubric defines ≥3 claim categories specific to the domain
- ≥3 fixtures with known issues; at least 1 where reviewers are expected to disagree
- No engine code modified (if engine changes are needed, split into 2 PRs)
- Tests pass hermetically (scripted reviewers, no paid LLM)

## 16.3 Engine contribution path

```
1. Read docs/design/prd/12-design-decisions.md (don't fight established decisions)
2. Read docs/design/prd/02-architecture.md (understand the invariant)
3. Pick an issue labeled "good first issue" or "help wanted"
4. Fork → branch → implement → test
5. All checks must pass: ruff, mypy strict, ≥95% coverage, hermetic tests
6. PR with title describing the change, not the file
```

**Review criteria for engine PRs:**
- Isolation invariant tests still pass (non-negotiable)
- No new paid-LLM calls in CI
- Coverage doesn't drop below 95%
- Design decisions (DD-01 through DD-08) respected or explicitly revised via a new DD record

## 16.4 Fixture contribution path (lowest barrier)

```
1. Pick a domain from docs/design/prd/04-users-and-cujs.md
2. Create tests/fixtures/<domain>/
3. Add 3-5 artifacts (redacted, public, or clearly-labeled fictional)
4. Add a fixtures.json: { "artifact": "filename", "known_issues": [...], "expected_disagreement": true|false }
5. PR with title: "fixtures: <domain>"
```

**No code required.** Domain experts who can't write Python can contribute fixtures and rubrics — this is how we reach 27 verticals with one maintainer.

## 16.5 Recognition

- All contributors added to CONTRIBUTORS.md
- Adapter authors credited in the adapter's `__init__.py` metadata
- Significant contributions mentioned in release notes
- No CLA — MIT license is sufficient (fleet standard)
