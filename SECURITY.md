# Security Policy

## Reporting a Vulnerability

**Do NOT open a public GitHub issue for security vulnerabilities.** Use private channels first.

| Channel | Scope | Response SLA |
|---------|-------|--------------|
| **security@deghosal-2026** (email, PGP encrypted) | Engine, isolation bypass, data-handling flaw | 48h ack · 7d triage · 30d fix |
| **GitHub Security Advisory** (private vulnerability reporting) | Same scope, preferred for auditability | Same SLA |
| **Public GitHub issue** | Non-security bugs, feature requests, docs | Best-effort |

## Severity Rubric

| Severity | Definition | Fix SLA |
|----------|-----------|---------|
| **Critical** | Isolation invariant bypassed; reviewer context leakage; artifact content exposed to unintended parties | 7 days |
| **High** | Prompt injection from artifact leads to arbitrary reviewer behavior; audit log tampering | 14 days |
| **Medium** | Schema validation bypass; partial transcript corruption on crash; budget ceiling evasion | 30 days |
| **Low** | Information disclosure in logs; minor invariant weakening | Next release |

## Disclosure Timeline

```
Day 0:  Reporter privately discloses
Day 2:  Maintainer acknowledges, assigns severity
Day 7:  Severity confirmed; fix in progress
Day 30: Fix released (or mitigation published)
Day 37: Public disclosure (CVE requested if Critical/High)
```

Coordinated disclosure timelines up to 90 days honored on request.

## Security Posture

- **Reviewer independence** is mechanically enforced (separate sessions, delayed revelation), not prompted
- **Artifacts are untrusted content** — structured output validation on every reviewer message
- **No tool access** for reviewers in v0.1 (read-only reasoning)
- **Full audit lineage** persisted locally (SQLite), exportable JSONL
- **Local-first** — transcripts never leave the user's machine unless explicitly exported
- **No telemetry** by default, ever

See [docs/design/prd/06-security-baseline.md](docs/design/prd/06-security-baseline.md) for the full threat model.