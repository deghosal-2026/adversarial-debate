"""Budget-aware chunk planning (WBS T4.4, PRD §2.8 context-window strategy).

Split rule: by file first; a single file whose estimate exceeds the budget is
sub-split at hunk boundaries (header rides with the first part). Token counts
use the documented ``chars // 4`` heuristic. Every emitted value is
deterministic, and per-chunk budget percentages plus claim-dedup keys land in
artifact metadata so report headers (§2.8) can be honest about context usage.
"""

from collections.abc import Sequence
from dataclasses import dataclass

from adversarial_debate.ids import deterministic_id
from adversarial_debate.schemas.artifact import ContentBlock

DEFAULT_CONTEXT_WINDOW_TOKENS = 200_000
DEFAULT_BUDGET_FRACTION = 0.8
_CHARS_PER_TOKEN = 4
_PCT_PRECISION = 2


def estimate_tokens(text: str) -> int:
    """Documented heuristic: one token ≈ four characters (floored at 1)."""
    return max(1, len(text) // _CHARS_PER_TOKEN)


@dataclass(frozen=True)
class Chunk:
    """One reviewer-sized group of content units (PRD §2.8)."""

    units: list[ContentBlock]
    estimated_tokens: int
    budget_pct: float
    over_budget: bool
    dedup_key: str


@dataclass(frozen=True)
class ChunkPlan:
    """Full deterministic split of an artifact's blocks into chunks."""

    chunks: list[Chunk]
    window_tokens: int
    budget_tokens: int
    fraction: float


def plan_chunks(
    blocks: Sequence[ContentBlock],
    *,
    window_tokens: int = DEFAULT_CONTEXT_WINDOW_TOKENS,
    fraction: float = DEFAULT_BUDGET_FRACTION,
) -> ChunkPlan:
    """Group ``blocks`` into chunks within ``window_tokens * fraction`` budget."""
    if not blocks:
        msg = "plan_chunks requires at least one content block"
        raise ValueError(msg)
    if window_tokens < 1:
        msg = f"context window must be positive, got {window_tokens}"
        raise ValueError(msg)
    if not 0.0 < fraction <= 1.0:
        msg = f"budget fraction must be in (0, 1], got {fraction}"
        raise ValueError(msg)

    budget = int(window_tokens * fraction)
    units: list[ContentBlock] = []
    for block in blocks:
        units.extend(_atomic_units(block, budget))
    return ChunkPlan(
        chunks=_group(units, budget),
        window_tokens=window_tokens,
        budget_tokens=budget,
        fraction=fraction,
    )


def chunk_metadata(plan: ChunkPlan) -> dict[str, str]:
    """Flatten a plan into artifact-metadata entries (report header feeds §2.8)."""
    metadata = {
        "chunk_count": str(len(plan.chunks)),
        "chunk_window_tokens": str(plan.window_tokens),
        "chunk_budget_tokens": str(plan.budget_tokens),
        "chunk_budget_fraction": str(plan.fraction),
        "estimated_total_tokens": str(sum(c.estimated_tokens for c in plan.chunks)),
    }
    for i, chunk in enumerate(plan.chunks, start=1):
        metadata[f"chunk_{i}_estimated_tokens"] = str(chunk.estimated_tokens)
        metadata[f"chunk_{i}_budget_pct"] = f"{chunk.budget_pct:.{_PCT_PRECISION}f}"
        metadata[f"chunk_{i}_over_budget"] = "true" if chunk.over_budget else "false"
        metadata[f"chunk_{i}_dedup_key"] = chunk.dedup_key
        metadata[f"chunk_{i}_block_ids"] = ",".join(unit.id for unit in chunk.units)
    return metadata


def _atomic_units(block: ContentBlock, budget: int) -> list[ContentBlock]:
    if estimate_tokens(block.content) <= budget:
        return [block]
    parts = _split_at_hunks(block.content, budget)
    if len(parts) == 1:
        return [block]
    return [
        ContentBlock(
            id=deterministic_id("cb", f"{block.id}#part{k}"),
            kind=block.kind,
            name=block.name if k == 0 else f"{block.name}#part{k}",
            content="\n".join(part),
            sequence=block.sequence,
        )
        for k, part in enumerate(parts)
    ]


def _split_at_hunks(content: str, budget: int) -> list[list[str]]:
    lines = content.split("\n")
    header_end = 0
    while header_end < len(lines) and not lines[header_end].startswith("@@"):
        header_end += 1
    header, hunk_lines = lines[:header_end], lines[header_end:]

    hunks: list[list[str]] = []
    current: list[str] = []
    for line in hunk_lines:
        if line.startswith("@@") and current:
            hunks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        hunks.append(current)

    pieces: list[list[str]] = []
    acc: list[str] = []
    acc_tokens = 0
    if hunks:
        payload = [
            ([*header, *hunk] if i == 0 else list(hunk), _piece_tokens(header, hunk, i))
            for i, hunk in enumerate(hunks)
        ]
    else:
        payload = [(list(header), _tokens_of(header))]
    for piece_lines, piece_tokens in payload:
        if acc and acc_tokens + piece_tokens > budget:
            pieces.append(acc)
            acc, acc_tokens = list(piece_lines), piece_tokens
        else:
            acc = [*acc, *piece_lines] if acc else list(piece_lines)
            acc_tokens += piece_tokens
    if acc:
        pieces.append(acc)
    return pieces or [lines]


def _tokens_of(lines: list[str]) -> int:
    return estimate_tokens("\n".join(lines))


def _piece_tokens(header: list[str], hunk: list[str], index: int) -> int:
    return _tokens_of(hunk) + (_tokens_of(header) if index == 0 else 0)


def _group(units: Sequence[ContentBlock], budget: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    acc: list[ContentBlock] = []
    acc_tokens = 0
    for unit in units:
        tokens = estimate_tokens(unit.content)
        if acc and acc_tokens + tokens > budget:
            chunks.append(_make_chunk(acc, acc_tokens, budget))
            acc, acc_tokens = [], 0
        acc.append(unit)
        acc_tokens += tokens
    if acc:
        chunks.append(_make_chunk(acc, acc_tokens, budget))
    return chunks


def _make_chunk(units: list[ContentBlock], tokens: int, budget: int) -> Chunk:
    dedup_payload = "|".join(unit.id for unit in units)
    return Chunk(
        units=list(units),
        estimated_tokens=tokens,
        budget_pct=round(tokens / budget * 100, _PCT_PRECISION),
        over_budget=tokens > budget,
        dedup_key=deterministic_id("cdk", dedup_payload),
    )
