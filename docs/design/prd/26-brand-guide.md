# 26 — Brand & Naming Guide

> Sub-document of the [Design overview](../README.md). Voice, terminology consistency, and naming rules. Contributors and article authors read this before writing anything public.

## 26.1 Names

| Context | Name | Example |
|---------|------|---------|
| **Project / repo name** | AdversarialDebate (PascalCase) | "AdversarialDebate is a multi-agent review engine" |
| **Package name** | adversarial-debate (kebab-case) | `pip install adversarial-debate` |
| **Python import** | adversarial_debate (snake_case) | `from adversarial_debate import Engine` |
| **CLI binary** | advdeb | `advdeb review --pr 482` |
| **Engine class** | Engine | `engine = Engine(config="advdeb.toml")` |
| **Short form (articles, prose)** | the engine | "the engine produces a disagreement report" |
| **Never** | AD, AdvDeb, adversarial debate (lowercase as proper noun) | ❌ "AD is a review engine" |

## 26.2 Voice

- **Direct, not academic.** "Most AI second opinions are fake." Not "Contemporary AI review systems exhibit a structural bias toward consensus."
- **Honest about limitations.** Every claim of strength is paired with a stated limitation. "Debate catches independent issues. It does not catch shared blind spots."
- **Evidence over assertion.** Cite research or show a transcript. Never say "dramatically improves" without a number.
- **No hype words.** Banned: revolutionary, game-changing, cutting-edge, next-generation, robust, scalable (without a number). Use: faster, cheaper, independent, auditable, dissent-preserving.
- **The user is smart.** Don't over-explain. A VP Engineering knows what a PR is. A GC knows what an indemnity clause is.

## 26.3 Terminology consistency

| Use | Don't use | Why |
|-----|-----------|-----|
| Reviewer | Agent, critic, judge, evaluator | "Agent" implies tool access; "critic" implies single-side; "judge" implies verdict-only. Reviewer is precise. |
| Artifact | Document, file, input, diff | "Artifact" is domain-neutral (PR, contract, CR). "Document" implies text-only. |
| Disagreement report | Error, failure, unresolved, fallback | Disagreement is the product, not an error state. |
| Convergence | Agreement, consensus, resolution | "Agreement" implies social consensus; convergence is a mechanical claim (no open claims remain). |
| Revelation gate | Reveal step, sharing phase, turn | "Revelation gate" is a specific engine state transition, not a conversational turn. |
| Would_resolve_if | Next steps, recommendations, suggestions | `would_resolve_if` is a structured field, not a suggestion. It names the specific evidence/action that would close the dispute. |
| Theater | Fake debate, bad debate, useless debate | "Theater" is the metric name; it's neutral, not pejorative. |

## 26.4 Article voice rules

1. **Every article title is a sentence, not a label.** "I Asked Two AI Models to Review the Same PR Independently. They Disagreed." Not "Adversarial Debate: A New Approach to AI Review."
2. **First-person for build articles.** "I ran 30 PRs through the engine." Not "The engine was run against 30 PRs."
3. **Transcript excerpts are sacred.** Never edit a transcript for readability. If it's unclear, that's the finding.
4. **Honest limitation in every article.** At least one paragraph starting with "What this doesn't do:" or "The honest limitation:"
5. **No comparative claims without the benchmark protocol.** Don't say "better than CodeRabbit" without running [19-competitor-benchmark.md](19-competitor-benchmark.md).

## 26.5 Visual identity (direction, not final)

- **Logo concept:** Two speech bubbles facing each other, one with a checkmark (converged) and one with a split arrow (disputed). Minimal, monochrome.
- **Color palette:** Neutral base (slate/charcoal). Disagreement highlighted in amber, not red — red implies error; amber implies "attention needed."
- **Terminal output:** Green for converged verdicts, amber for disputed, gray for informational. Never red (reserved for engine errors only).
- **Diagram style:** ASCII art for architecture (works in terminal + markdown). Mermaid for complex flows. No screenshots of UI in docs until UI exists.
