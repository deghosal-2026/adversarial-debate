# M8 — Release Readiness

> Goal: security scan, CI/tooling verification, documentation updates, OSS community files, OpenSSF badge refresh, PyPI publish, GitHub release and tag, and merge all changes to main. This is the final milestone — ship v0.2.0. Part of [index](index.md).

## PRD coupling

- [09-roadmap §9.2 v0.2.0 scope](../../design/prd/09-roadmap.md): "fix v0.1.0 postmortem items, ship corrected field-test data"
- [17-security-disclosure](../../design/prd/17-security-disclosure.md): security policy files
- [26-brand-guide](../../design/prd/26-brand-guide.md): README voice lint
- Fleet house standard: OpenSSF Best Practices Passing at ship

## Dependencies

Upstream: M7. Downstream: none — this is the last milestone.

## Workstreams & tasks

### WS 8.a — Security & quality

- [ ] T8.1 (#116) Security scan: bandit, pip-audit, secret-scan clean or findings fixed; verify no API key leak regression (#77)
- [ ] T8.2 (#117) Run lint, type checking, and full test suite: ruff, mypy, pytest with coverage
- [ ] T8.3 (#125) Verify CI pipeline, pre-commit hooks, and strict tooling are fully operational

### WS 8.b — Documentation & version

- [ ] T8.4 (#118) Update version to 0.2.0 in pyproject.toml, update CHANGELOG.md, update README.md badges
- [ ] T8.5 (#124) Update OSS community files: CONTRIBUTING, CODE_OF_CONDUCT, SUPPORT, GOVERNANCE, CHANGELOG v0.2.0
- [ ] T8.6 (#123) Refresh OpenSSF Best Practices badge for v0.2.0

### WS 8.c — Ship

- [ ] T8.7 (#119) Build and publish to PyPI: sdist+wheel, twine check, TestPyPI verification, PyPI publish
- [ ] T8.8 (#120) Create GitHub release v0.2.0 with annotated tag and changelog; attach distribution artifacts
- [ ] T8.9 (#115) Publish v0.2.0 release notes and article updates on dev.to
- [ ] T8.10 (#121) Merge all M1-M7 feature branches to main via PRs; resolve conflicts; verify CI passes on main; close all M1-M7 milestones

## Documents, plans & tests to update

- `pyproject.toml` — bump version to 0.2.0
- `CHANGELOG.md` — add v0.2.0 entry with all M1-M7 changes
- `README.md` — update badges, version references, feature list
- `SECURITY.md` — update with v0.2.0 changes (isolation audit, canary test)
- `CONTRIBUTING.md` — update if workflows changed
- `CODE_OF_CONDUCT.md` — review for currency
- `SUPPORT.md` — update version references
- `GOVERNANCE.md` — review for currency
- `docs/reference/quickstart.md` — update if CLI flags changed
- `docs/wbs/0.2.0/index.md` — mark all milestones complete
- `.github/workflows/ci.yml` — verify pipeline config is current
- `.pre-commit-config.yaml` — verify hooks are current
- `Makefile` — verify targets are up to date
- `README.md` — update OpenSSF Best Practices badge URL if needed

## Acceptance criteria / exit gate

- All security scans green; zero known Critical/High open
- `pip install adversarial-debate==0.2.0` works on Python 3.11/3.12 in clean environments
- GitHub Release v0.2.0 live with changelog and assets
- PyPI package published
- All M1-M7 milestones show 100% complete
- Ruff clean, mypy strict clean, full test suite green
- Code review completed on all changes
- All changes merged to main via PRs

## Explicitly out of scope

v0.3 features (UI, second adapter, etc.) — next cycle.