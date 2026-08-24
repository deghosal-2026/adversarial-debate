# 17 — Security Disclosure Policy

> Sub-document of the [Design overview](../README.md). How vulnerabilities are reported, triaged, and disclosed. Beyond "OpenSSF badge" — the operational process buyers and researchers need.

## 17.1 Reporting a vulnerability

| Channel | When to use | Response SLA |
|---------|------------|--------------|
| **security@deghosal-2026** (email, PGP encrypted) | Vulnerability in the engine, isolation bypass, or data-handling flaw | 48 hours: acknowledgment · 7 days: triage + severity · 30 days: fix or mitigation |
| **GitHub Security Advisory** (private vulnerability reporting) | Same scope, preferred for auditability | Same SLA |
| **Public GitHub issue** | Non-security bugs, feature requests, documentation | Best-effort |

**Do NOT open a public issue for security vulnerabilities.** Use private channels first.

## 17.2 Severity rubric

| Severity | Definition | Example | Fix SLA |
|----------|-----------|---------|---------|
| **Critical** | Isolation invariant bypassed; reviewer context leakage; artifact content exposed to unintended parties | Reviewer B can read A's pre-revelation output via framework memory leak | 7 days |
| **High** | Prompt injection from artifact leads to arbitrary reviewer behavior; audit log tampering | Malicious diff text causes reviewer to exfiltrate artifact content via model output | 14 days |
| **Medium** | Schema validation bypass; partial transcript corruption on crash; budget ceiling evasion | Malformed reviewer output accepted without validation | 30 days |
| **Low** | Information disclosure in logs; minor invariant weakening | Transcript contains model provider name when `--anonymous` is set | Next release |

## 17.3 Disclosure timeline

```
Day 0:    Reporter privately discloses
Day 2:    Maintainer acknowledges, assigns severity
Day 7:    Maintainer confirms or adjusts severity; fix in progress
Day 30:   Fix released (or mitigation published with timeline for full fix)
Day 37:   Public disclosure (CVE requested if Critical/High)
```

**Coordinated disclosure:** if the reporter prefers a longer timeline for research, we honor it — up to 90 days. We do not publish before the reporter agrees unless the vulnerability is being actively exploited.

## 17.4 What buyers need to hear

- "Vulnerabilities are reported privately, triaged within 48 hours, and fixed within 30 days for Critical/High."
- "Every security fix ships with a postmortem in the release notes explaining what happened, why, and how it was detected."
- "The isolation invariant has dedicated adversarial tests in CI — any change that weakens it fails the build."
- "No security through obscurity: the engine's security model is fully documented in [06-security-baseline.md](06-security-baseline.md). If it's not documented, it's not a guarantee."
