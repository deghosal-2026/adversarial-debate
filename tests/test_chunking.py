"""Budget-aware chunker contract (WBS T4.4, PRD §2.8): property + goldens."""

import pytest

from adversarial_debate.adapters.pr_review.chunking import (
    DEFAULT_BUDGET_FRACTION,
    DEFAULT_CONTEXT_WINDOW_TOKENS,
    estimate_tokens,
    plan_chunks,
)
from adversarial_debate.adapters.pr_review.chunking import (
    chunk_metadata as build_chunk_metadata,
)
from adversarial_debate.schemas.artifact import ContentBlock


def make_block(name: str, content: str, sequence: int) -> ContentBlock:
    return ContentBlock(id=f"cb_{name}", kind="diff", name=name, content=content, sequence=sequence)


def big_file_block(hunks: int, hunk_lines: int = 10) -> ContentBlock:
    lines = [
        "diff --git a/big.py b/big.py",
        "--- a/big.py",
        "+++ b/big.py",
    ]
    for i in range(hunks):
        lines.append(f"@@ -{i * 100 + 1},9 +{i * 100 + 1},9 @@ section {i}")
        for j in range(hunk_lines):
            lines.append(f"+x{i}_{j} = '{j}'  # padding to grow the hunk body size")
    return make_block("big.py", "\n".join(lines), 0)


def varied_blocks(count: int) -> list[ContentBlock]:
    blocks = []
    for i in range(count):
        lines = [f"context {i}-{k} some steady padding text" for k in range((i * 37) % 80 + 5)]
        blocks.append(make_block(f"f{i}.py", "\n".join(lines), i))
    return blocks


def test_estimate_tokens_is_chars_over_four_with_floor_of_one() -> None:
    assert estimate_tokens("") == 1
    assert estimate_tokens("ab") == 1
    assert estimate_tokens("a" * 40) == 10


def test_defaults_are_documented_heuristic_values() -> None:
    assert DEFAULT_BUDGET_FRACTION == 0.8
    assert DEFAULT_CONTEXT_WINDOW_TOKENS > 0


def test_small_plan_single_chunk_under_budget() -> None:
    plan = plan_chunks([make_block("a.py", "+x = 1", 0)], window_tokens=64)
    assert len(plan.chunks) == 1
    chunk = plan.chunks[0]
    assert chunk.over_budget is False
    assert 0 < chunk.budget_pct <= 100
    assert plan.fraction == 0.8


def test_empty_blocks_rejected() -> None:
    with pytest.raises(ValueError, match="at least one"):
        plan_chunks([])


@pytest.mark.parametrize(
    ("window", "fraction"),
    [(0, 0.8), (-5, 0.8), (1000, 0.0), (1000, -0.1), (1000, 1.5)],
)
def test_invalid_parameters_rejected(window: int, fraction: float) -> None:
    with pytest.raises(ValueError, match=r"fraction|window"):
        plan_chunks([make_block("a.py", "+x", 0)], window_tokens=window, fraction=fraction)


def test_property_no_chunk_exceeds_budget_and_coverage_exact() -> None:
    blocks = varied_blocks(40)
    plan = plan_chunks(blocks, window_tokens=800, fraction=0.8)
    budget = plan.budget_tokens
    assert len(plan.chunks) > 1
    for chunk in plan.chunks:
        if chunk.over_budget:
            assert len(chunk.units) == 1
            assert chunk.estimated_tokens > budget
        else:
            assert chunk.estimated_tokens <= budget
    covered = "\n".join(u.content for c in plan.chunks for u in c.units)
    original = "\n".join(b.content for b in blocks)
    assert covered == original
    flat_sequences = [u.sequence for c in plan.chunks for u in c.units]
    assert flat_sequences == sorted(flat_sequences)


def test_order_preserved_across_chunk_boundaries() -> None:
    blocks = varied_blocks(12)
    plan = plan_chunks(blocks, window_tokens=400, fraction=0.8)
    sequences = [u.sequence for c in plan.chunks for u in c.units]
    assert sequences == [b.sequence for b in blocks]


def test_oversized_file_splits_into_hunk_groups() -> None:
    block = big_file_block(hunks=30)
    plan = plan_chunks([block], window_tokens=2000, fraction=0.8)
    units = [u for c in plan.chunks for u in c.units]
    assert len(units) >= 3
    assert units[0].name == "big.py"
    assert all(unit.name.startswith("big.py#part") for unit in units[1:])
    reconstructed = "\n".join(unit.content for unit in units)
    assert reconstructed == block.content
    budget = plan.budget_tokens
    assert all(estimate_tokens(unit.content) <= budget for unit in units)


def test_single_hunk_over_budget_flagged_not_dropped() -> None:
    block = big_file_block(hunks=1, hunk_lines=400)
    plan = plan_chunks([block], window_tokens=500, fraction=0.8)
    assert len(plan.chunks) == 1
    assert plan.chunks[0].over_budget is True
    assert plan.chunks[0].units[0].content == block.content


def test_smaller_fraction_produces_more_chunks() -> None:
    blocks = varied_blocks(20)
    wide = plan_chunks(blocks, window_tokens=800, fraction=0.8)
    narrow = plan_chunks(blocks, window_tokens=800, fraction=0.4)
    assert narrow.budget_tokens < wide.budget_tokens
    assert len(narrow.chunks) >= len(wide.chunks)


def test_dedup_keys_deterministic_and_distinct() -> None:
    blocks = varied_blocks(20)
    first = plan_chunks(blocks, window_tokens=600)
    second = plan_chunks(blocks, window_tokens=600)
    keys_first = [c.dedup_key for c in first.chunks]
    keys_second = [c.dedup_key for c in second.chunks]
    assert keys_first == keys_second
    assert len(set(keys_first)) == len(keys_first)
    assert all(key.startswith("cdk_") for key in keys_first)


def test_chunk_metadata_shape_and_types() -> None:
    blocks = [
        make_block("a.py", "+one\n+two", 0),
        make_block("b.py", "+three", 1),
    ]
    plan = plan_chunks(blocks, window_tokens=64, fraction=0.5)
    md = build_chunk_metadata(plan)
    count = len(plan.chunks)
    assert md["chunk_count"] == str(count)
    assert md["chunk_window_tokens"] == "64"
    assert md["chunk_budget_tokens"] == str(plan.budget_tokens)
    assert md["chunk_budget_fraction"] == "0.5"
    assert md["estimated_total_tokens"] == str(sum(c.estimated_tokens for c in plan.chunks))
    for i, chunk in enumerate(plan.chunks, start=1):
        assert md[f"chunk_{i}_estimated_tokens"] == str(chunk.estimated_tokens)
        assert md[f"chunk_{i}_budget_pct"] == f"{chunk.budget_pct:.2f}"
        assert md[f"chunk_{i}_over_budget"] == ("true" if chunk.over_budget else "false")
        assert md[f"chunk_{i}_dedup_key"] == chunk.dedup_key
        expected_ids = ",".join(u.id for u in chunk.units)
        assert md[f"chunk_{i}_block_ids"] == expected_ids
    assert set(md) == {
        "chunk_count",
        "chunk_window_tokens",
        "chunk_budget_tokens",
        "chunk_budget_fraction",
        "estimated_total_tokens",
        *{
            f"chunk_{i}_{suffix}"
            for i in range(1, count + 1)
            for suffix in (
                "estimated_tokens",
                "budget_pct",
                "over_budget",
                "dedup_key",
                "block_ids",
            )
        },
    }
