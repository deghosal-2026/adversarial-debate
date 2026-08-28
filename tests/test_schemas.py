"""Schema validation tests (M1: T1.10)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from adversarial_debate.schemas.debate import UnresolvedPoint


class TestUnresolvedPoint:
    """UnresolvedPoint schema: claim_ids must have non-empty elements."""

    def test_valid_claim_ids(self) -> None:
        point = UnresolvedPoint(
            id="up_1",
            claim_ids=["cl_001"],
            position_a="A position",
            position_b="B position",
            would_resolve_if="Need more evidence",
        )
        assert point.claim_ids == ["cl_001"]

    def test_multiple_valid_claim_ids(self) -> None:
        point = UnresolvedPoint(
            id="up_1",
            claim_ids=["cl_001", "cl_002"],
            position_a="A",
            position_b="B",
            would_resolve_if="More testing required",
        )
        assert len(point.claim_ids) == 2

    def test_empty_string_claim_id_raises(self) -> None:
        """Empty-string claim IDs should be rejected."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            UnresolvedPoint(
                id="up_1",
                claim_ids=[""],
                position_a="A",
                position_b="B",
                would_resolve_if="Need more evidence",
            )

    def test_empty_claim_ids_list_raises(self) -> None:
        """Empty list of claim IDs should be rejected."""
        with pytest.raises(ValidationError, match="List should have at least 1 item"):
            UnresolvedPoint(
                id="up_1",
                claim_ids=[],
                position_a="A",
                position_b="B",
                would_resolve_if="Need more evidence",
            )

    def test_mixed_empty_and_valid_raises(self) -> None:
        """Mixed list with empty string should be rejected."""
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            UnresolvedPoint(
                id="up_1",
                claim_ids=["cl_001", ""],
                position_a="A",
                position_b="B",
                would_resolve_if="Need more evidence",
            )
