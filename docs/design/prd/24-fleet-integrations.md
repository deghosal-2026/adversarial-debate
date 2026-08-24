# 24 — Fleet Integration Specs

> Sub-document of the [Design overview](../README.md). Exact API contracts for integrating AdversarialDebate with the rest of the fleet. Each integration is bidirectional and documented.

## 24.1 Fleet map

```
                    EvalForge (eval)
                        │
                        ▼
                ┌───────────────┐
                │ AdversarialDebate │
                │   (judgment)   │
                └──────┬────────┘
          ┌────────────┼────────────┐
          ▼            ▼            ▼
    ToolTrust      PlannerCritic  AgentJury
    (enforce)      (plan critique) (N-agent)
```

## 24.2 ToolTrust Engine integration (v0.4.0)

**Direction:** AdversarialDebate → ToolTrust (advisory input before tool execution)

**Use case:** An AI agent proposes a risky action (bulk cert rotation). Before ToolTrust's gate decides allow/deny, it requests an adversarial debate on the action plan.

**API contract:**

```python
# ToolTrust calls AdversarialDebate
from adversarial_debate import Engine

engine = Engine(config="advdeb.toml")
result = engine.review(
    artifact=action_plan,        # ToolTrust's normalized action plan
    domain="agent_action",       # adapter for agent action plans
    config=ReviewConfig(rounds=2, pair="diverse")
)

# ToolTrust consumes the result
if result.verdict == "disputed":
    for point in result.unresolved:
        if point.severity == "high":
            tooltrust.deny(reason=f"Adversarial review disputed: {point.would_resolve_if}")
            break
    else:
        tooltrust.allow_with_advisory(result.unresolved)
else:
    tooltrust.allow(reason="Adversarial review converged")
```

**Data flow:** ToolTrust passes the action plan as a `ReviewArtifact`. AdversarialDebate never calls ToolTrust — the integration is one-directional (ToolTrust requests, AdversarialDebate responds).

## 24.3 EvalForge integration (v0.4.0)

**Direction:** Bidirectional. AdversarialDebate exports fixtures as EvalForge scenarios; EvalForge runs them as regression tests.

**Export format:**

```json
{
  "scenario_id": "advdeb-pr-482-lock-timeout",
  "source": "adversarial-debate",
  "input": "fixtures/pr_review/pr-482-revert.diff",
  "expected_verdict": "disputed",
  "expected_unresolved": ["lock-timeout on 40GB table"],
  "engine_version": "0.1.0",
  "pass_criteria": "verdict == disputed AND lock-timeout in unresolved[].topic"
}
```

**EvalForge calls AdversarialDebate:**

```python
# EvalForge's runner
result = engine.review(artifact=scenario.input, domain="pr_review")
assert result.verdict == scenario.expected_verdict
assert any("lock-timeout" in p.topic for p in result.unresolved)
```

**Value:** every engine change re-runs the eval suite via EvalForge. Regressions (a fix that breaks a previously-passing scenario) are caught before release.

## 24.4 PlannerCritic integration (v0.5.0)

**Direction:** PlannerCritic → AdversarialDebate (second-opinion on critic findings)

**Use case:** PlannerCritic's single critic audits a plan and produces findings. Before escalation, PlannerCritic sends the plan + critic findings to AdversarialDebate for an independent second opinion.

**API contract:**

```python
# PlannerCritic calls AdversarialDebate
result = engine.review(
    artifact=plan_and_findings,    # PlannerCritic's plan + critic output as artifact
    domain="plan_review",          # adapter for plan+critique artifacts
    config=ReviewConfig(rounds=2)
)

# PlannerCritic consumes
if result.verdict == "disputed":
    # The adversarial reviewers disagreed with the original critic on something
    planner.escalate(
        question=f"Adversarial review disputes: {result.unresolved[0].would_resolve_if}"
    )
```

**Key distinction:** PlannerCritic has one critic reviewing one plan (draft → critique → revise). AdversarialDebate has two independent reviewers debating the same artifact. The integration adds a *second independent perspective* to PlannerCritic's single-critic loop.

## 24.5 AgentJury integration (v0.6.0)

**Direction:** AdversarialDebate → AgentJury (graduation from 2-agent to N-agent)

**Use case:** A debate that remains disputed after 2 rounds escalates to AgentJury for N-agent consensus voting with forced-dissent mechanics.

**API contract:**

```python
# AdversarialDebate calls AgentJury on dispute
if result.verdict == "disputed" and config.escalate_to_jury:
    from agent_jury import Jury

    jury = Jury(config="jury.toml")
    jury_result = jury.deliberate(
        artifact=result.artifact,
        initial_positions=[result.reviewer_a_summary, result.reviewer_b_summary],
        unresolved_points=result.unresolved,
        jury_size=5
    )
    result.jury_escalation = jury_result
```

**Key distinction:** AdversarialDebate is 2-agent independent review with dissent preservation. AgentJury is N-agent consensus with forced dissent. The integration uses AdversarialDebate's dispute as the trigger for AgentJury's escalation — disputed debates get a jury; converged debates don't.

## 24.6 Integration versioning

Each integration specifies compatible versions:

```toml
# advdeb.toml
[integrations]
tooltrust = ">=0.2.0"
evalforge = ">=0.1.0"
planner_critic = ">=0.2.0"
agent_jury = ">=0.1.0"
```

Engine checks integration compatibility on startup. Incompatible versions fail with a clear message, not silent misbehavior.
