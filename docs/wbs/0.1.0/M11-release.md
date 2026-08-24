# M11 — Pre-Release & Release

> Goal: security sweep, docs to match reality, OSS community files, OpenSSF badge, packaging, PyPI + GitHub release, repo public flip — and the two launch articles. Ship it. Part of [index](index.md).

## PRD coupling

- [09-roadmap §9.1 v0.1.0 scope](../../design/prd/09-roadmap.md): "ship to PyPI/GitHub (public) + ≥2 dev.to articles"
- [18-article-plan §18.2](../../design/prd/18-article-plan.md): the two launch articles (transcript-driven)
- [17-security-disclosure](../../design/prd/17-security-disclosure.md): policy files live before public flip
- [26-brand-guide](../../design/prd/26-brand-guide.md): README/report voice lint
- Fleet house standard: OpenSSF Best Practices Passing at ship

## Dependencies

Upstream: M10 PASS (kill criterion: do not ship on FAIL). Downstream: none — this is the last milestone.

## Workstreams & tasks

### WS 11.a — Hardening & docs

- [ ] T11.1 (#51) Security sweep: bandit, pip-audit, secret-scan (gitleaks) clean or findings fixed; dependency pin review; SECURITY.md published with disclosure SLA from [§17](../../design/prd/17-security-disclosure.md)
- [ ] T11.2 (#52) Docs pass: README final (house badge header), quickstart mirrors M9 onboarding test verbatim; docs/ refreshed to match implementation (no aspirational text in v0.1 paths); brand-voice banned-word grep over user-facing strings

### WS 11.b — OSS hygiene

- [ ] T11.3 (#53) Community files: CONTRIBUTING (adapter-first path from [16 §16.2](../../design/prd/16-contributor-journey.md)), CODE_OF_CONDUCT, SUPPORT, GOVERNANCE, CHANGELOG v0.1.0
- [ ] T11.4 (#54) OpenSSF Best Practices: submit project, complete Passing-level checklist, embed badge

### WS 11.c — Ship

- [ ] T11.5 (#55) Packaging: build sdist+wheel; twine check; clean-venv install + `advdeb --help` smoke; version 0.1.0 everywhere (pyproject, __init__, docs)
- [ ] T11.6 (#56) Publish: PyPI `adversarial-debate==0.1.0`; GitHub Release v0.1.0 with notes (incl. field-test headline result); flip repo **public**; set description/topics (`llm`,`multi-agent`,`debate`,`code-review`,`ai-safety`,`llm-agents`,`adversarial-ai`)
- [ ] T11.7 (#57) Launch articles: Article 1 ("…They Disagreed.") and Article 2 ("Agreement with Extra Steps") per [18 §18.2](../../design/prd/18-article-plan.md) — real transcripts only, honest-limitation section each; publish dev.to (+ Hashnode cross-post); announce on LinkedIn

## Acceptance criteria / exit gate

- All sweeps green; zero known Critical/High open at release
- `pip install adversarial-debate` works on Python 3.11/3.12 in clean envs (CI matrix)
- Repo public with ≥7 topics, description matching charter
- Both articles live with links recorded in vault work-schedule + `_INDEX`
- Release notes include the exit-bar case study link (transcript path)

## Explicitly out of scope

v0.2 features (UI, second adapter) — next cycle; hosted anything.
