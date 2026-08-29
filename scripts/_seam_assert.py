#!/usr/bin/env python3
"""Row-count invariant assertion utility for pipeline integrity.

Usage:
    from scripts._seam_assert import assert_seam

    # Before processing
    count_pre = len(artifact_ids)

    # ... processing ...

    # After processing — assert no rows were lost
    assert_seam("corpus→review", count_pre, processed_count, expected="equal")

    # For filters with expected exclusions
    assert_seam("debate→analysis", count_pre, count_post, expected="less_equal", strict=True)
"""

from __future__ import annotations


def assert_seam(
    seam_name: str,
    count_pre: int,
    count_post: int,
    expected: str = "equal",
    tolerance: int = 0,
    strict: bool = False,
    skipped_ids: list[str] | None = None,
) -> None:
    """Assert row-count invariant at a pipeline seam.

    Args:
        seam_name: Human-readable name of the seam (e.g. "corpus→review").
        count_pre: Row count before the seam operation.
        count_post: Row count after the seam operation.
        expected: "equal" or "less_equal".
        tolerance: Allowed difference for expected "less_equal".
        strict: If True, any count change emits a warning even if within tolerance.
        skipped_ids: Optional list of artifact IDs that were skipped.

    Raises:
        SystemExit: If the assertion fails (unexpected row loss).
        ValueError: If counts are negative.
    """
    if count_pre < 0 or count_post < 0:
        msg = f"SEAM ERROR: {seam_name}: negative counts ({count_pre}, {count_post})"
        raise ValueError(msg)

    if expected == "equal":
        if count_post != count_pre:
            msg = f"SEAM FAIL: {seam_name}: expected {count_pre}, found {count_post}"
            if skipped_ids:
                msg += f" — MISSING: {skipped_ids}"
            raise SystemExit(msg)
    elif expected == "less_equal":
        if count_post > count_pre + tolerance:
            msg = f"SEAM FAIL: {seam_name}: expected ≤{count_pre + tolerance}, found {count_post}"
            raise SystemExit(msg)
    else:
        msg = f"SEAM ERROR: {seam_name}: unknown expected relation {expected!r}"
        raise ValueError(msg)

    if strict and count_post != count_pre:
        diff = count_pre - count_post
        print(f"SEAM WARNING: {seam_name}: {count_pre} → {count_post} (Δ={diff})")