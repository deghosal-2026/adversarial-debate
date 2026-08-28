# WBS — AdversarialDebate

> Work breakdown structure and milestone plans, one directory per version.

## v0.2.0

- [`0.2.0/index.md`](0.2.0/index.md) — 8-milestone WBS index (M1-M8), each task wired to a live GitHub issue on milestones `M1`-`M8`
- Part files per milestone, every task row wired to a GitHub issue, with explicit "Documents, plans & tests to update" sections

| M | File | Focus | Issues |
|---|------|-------|--------|
| M1 | [M1-core-engine-bugfixes.md](0.2.0/M1-core-engine-bugfixes.md) | Core engine bugfixes | #58-#62, #65-#67, #71, #87-#91 |
| M2 | [M2-transport-script-infra.md](0.2.0/M2-transport-script-infra.md) | Transport & script infrastructure | #63-#64, #68-#70, #77-#81, #92, #95, #98-#101 |
| M3 | [M3-cli-adapter-integrations.md](0.2.0/M3-cli-adapter-integrations.md) | CLI & adapter integrations | #82-#86 |
| M4 | [M4-test-corrections-audits.md](0.2.0/M4-test-corrections-audits.md) | Test corrections & audits | #75-#76, #93-#94, #96-#97 |
| M5 | [M5-field-test-data-integrity.md](0.2.0/M5-field-test-data-integrity.md) | Field test data integrity | #72-#74, #102-#104, #111 |
| M6 | [M6-documentation-prd-corrections.md](0.2.0/M6-documentation-prd-corrections.md) | Documentation & PRD corrections | #105-#110 |
| M7 | [M7-field-test-rerun.md](0.2.0/M7-field-test-rerun.md) | Field test rerun | #112-#114, #122 |
| M8 | [M8-release-readiness.md](0.2.0/M8-release-readiness.md) | Release readiness | #115-#121, #123-#125 |

## v0.1.0

- [`0.1.0/index.md`](0.1.0/index.md) — 11-milestone WBS index (M1-M11), each task wired to a live GitHub issue on milestone `[Release-Milestone] v0.1.0`
- Part files per milestone group, every task row wired to a GitHub issue

### Milestone skeleton (from work schedule)

| Milestone | Scope |
|-----------|-------|
| AD-M1 | PRD, specs, architecture |
| AD-M2 | Develop + test + field test against real PRs from a public repo |
| AD-M3 | Ship 0.1.0 (PyPI + GitHub release + repo public) + ≥2 dev.to articles |
