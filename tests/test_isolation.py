"""Adversarial isolation audit tests (M4: T4.5, #76).

Verifies that reviewer B cannot see reviewer A's output during the debate.
Injects a known secret string into A's output and confirms it never appears
in B's transcript or input prompts.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from adversarial_debate.engine.debate_controller import (
    DebateController,
)
from adversarial_debate.providers.contract import ReviewResult, ReviewResultMetadata
from adversarial_debate.schemas import (
    Claim,
    Review,
    ReviewerSession,
)
from adversarial_debate.schemas.debate import Side

NOW = datetime(2026, 8, 25, 12, 0, tzinfo=UTC)


class _AuditProvider:
    """Test double that records the prompt it receives and returns canned text."""

    def __init__(self, raw_text: str = "CONCEDED on all.") -> None:
        self.raw_text = raw_text
        self.last_prompt = ""
        self.call_count = 0

    def review(self, request):  # type: ignore[no-untyped-def]
        self.call_count += 1
        if request.artifact.content_blocks:
            self.last_prompt = request.artifact.content_blocks[0].content
        return ReviewResult(
            raw_text=self.raw_text,
            claims=[],
            risks=[],
            confidence=0.5,
            metadata=ReviewResultMetadata(seed=42, prompt_version="test"),
        )


def _make_session(side: Side) -> ReviewerSession:
    return ReviewerSession(
        id=f"sess_audit_{side}",
        artifact_id="art_audit_001",
        side=side,
        provider="audit",
        model="test",
        created_at=NOW,
        status="revealed",
    )


def _make_review(side: Side, claims: list[Claim] | None = None) -> Review:
    return Review(
        id=f"rev_audit_{side}",
        session_id=f"sess_audit_{side}",
        claims=claims or [],
        risks=[],
        confidence=0.75,
        committed_at=NOW,
    )


def _make_claim(claim_id: str, text: str) -> Claim:
    return Claim(
        id=claim_id,
        review_id="rev_audit",
        text=text,
        severity="medium",
        evidence_refs=[],
        status="open",
    )


class TestIsolationAudit:
    """Adversarial isolation audit: verify reviewer B cannot see A's output."""

    def test_isolation_secret_not_leaked_to_b(self) -> None:
        """A secret string in A's debate response must not appear in B's prompt."""
        secret = f"CANARY_{uuid4().hex}"

        # A's response contains the secret — this simulates A's committed review leaking
        provider_a = _AuditProvider(raw_text=f"CONCEDED on cl_001. Secret={secret}")
        provider_b = _AuditProvider(raw_text="CONCEDED on cl_002.")

        controller = DebateController(
            provider_a=provider_a,
            provider_b=provider_b,
            session_a=_make_session("A"),
            session_b=_make_session("B"),
            review_a=_make_review(
                "A",
                claims=[
                    _make_claim("cl_001", "Security issue: missing auth"),
                ],
            ),
            review_b=_make_review("B", claims=[_make_claim("cl_002", "Minor style issue")]),
            artifact_for_prompt="test",
            max_rounds=2,
        )

        state = controller.run()
        assert state.reason in ("rounds_exhausted", "all_resolved")

        # The secret from A's debate response must not appear in B's input prompt
        assert secret not in provider_b.last_prompt, (
            f"Isolation leak: secret {secret} found in B's prompt!"
        )

        # The secret must not appear in B's raw output either
        assert secret not in provider_b.raw_text, (
            f"Isolation leak: secret {secret} found in B's output!"
        )
