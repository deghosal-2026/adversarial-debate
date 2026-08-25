"""PR-review normalizer: diff + metadata → ``ReviewArtifact`` (WBS T4.2-T4.4, F7).

Reference implementation of the §5.3 adapter protocol. Accepts a local diff
file path or a GitHub PR URL (via ``gh``); never invents metadata (FM-10);
emits budget-aware chunk metadata for report headers (§2.8). Determinism: same
input + clock ⇒ identical artifact, so transcripts are reproducible (PRD §6.4).
"""

from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from adversarial_debate.adapters import (
    Hints,
    NormalizationError,
    artifact_id_for,
    utc_now,
)
from adversarial_debate.adapters.pr_review.chunking import (
    DEFAULT_BUDGET_FRACTION,
    DEFAULT_CONTEXT_WINDOW_TOKENS,
    chunk_metadata,
    plan_chunks,
)
from adversarial_debate.adapters.pr_review.diff_parser import parse_diff
from adversarial_debate.adapters.pr_review.language import classification_tag
from adversarial_debate.adapters.pr_review.metadata import GhRunner, PrMetadataExtractor
from adversarial_debate.ids import content_hash
from adversarial_debate.schemas.artifact import (
    ContentBlock,
    DetectedLanguage,
    ReviewArtifact,
    RubricHint,
)

_HASH_SEPARATOR = "\x1e"
_DEFAULT_LANGUAGE = "en"
_DEFAULT_LANGUAGE_CONFIDENCE = 0.5

DEFAULT_RUBRIC_HINTS = (
    RubricHint(
        id="rh_pr_security",
        dimension="security",
        guidance=(
            "Flag injection, committed secrets, unsafe "
            "deserialization, and authz gaps visible in this diff."
        ),
        weight=1.0,
    ),
    RubricHint(
        id="rh_pr_correctness",
        dimension="correctness",
        guidance=(
            "Flag logic errors, boundary conditions, race "
            "conditions, and error-handling gaps introduced by this diff."
        ),
        weight=1.0,
    ),
    RubricHint(
        id="rh_pr_performance",
        dimension="performance",
        guidance=(
            "Flag complexity regressions, N+1 queries, and unbounded loops introduced by this diff."
        ),
        weight=1.0,
    ),
)


class PrReviewNormalizer:
    """Normalizer for domain ``pr_review`` — the only shipping v0.1.0 domain."""

    def __init__(
        self,
        gh: GhRunner | None = None,
        clock: Callable[[], datetime] | None = None,
        window_tokens: int = DEFAULT_CONTEXT_WINDOW_TOKENS,
        fraction: float = DEFAULT_BUDGET_FRACTION,
    ) -> None:
        """Inject dependencies: gh runner, clock, and budget params."""
        self._gh = gh
        self._clock = clock if clock is not None else utc_now
        self._window_tokens = window_tokens
        self._fraction = fraction

    @property
    def domain(self) -> str:
        """Registry key for this adapter."""
        return "pr_review"

    def normalize(self, raw: str, hints: Hints = None) -> ReviewArtifact:
        """Normalize a diff path or GitHub PR URL into a ReviewArtifact."""
        source = raw.strip()
        if not source:
            msg = (
                "empty input: pass a diff file path or a GitHub PR URL "
                "(e.g. https://github.com/owner/repo/pull/482)"
            )
            raise NormalizationError(msg)

        extractor = PrMetadataExtractor(gh=self._gh)
        text, path = extractor.fetch_diff(source)
        parsed = parse_diff(text)
        if not parsed.blocks:
            msg = (
                f"no parsable file changes in {source}: input does not look like a unified git diff"
            )
            raise NormalizationError(msg)

        names = [block.name for block in parsed.blocks]
        extraction = extractor.extract(source, names, source_path=path)
        plan = plan_chunks(
            parsed.blocks, window_tokens=self._window_tokens, fraction=self._fraction
        )
        blocks = _resequenced([unit for chunk in plan.chunks for unit in chunk.units])

        metadata = {**extraction.metadata, **chunk_metadata(plan)}
        for i, warning in enumerate(parsed.warnings, start=1):
            metadata[f"parse_warning_{i}"] = warning
        for i, warning in enumerate(extraction.warnings, start=1):
            metadata[f"metadata_warning_{i}"] = warning

        return ReviewArtifact(
            id=artifact_id_for(self.domain, _source_uri(source, path)),
            domain=self.domain,
            source_uri=_source_uri(source, path),
            content_blocks=blocks,
            rubric_hints=[*DEFAULT_RUBRIC_HINTS, *(hints or [])],
            created_at=self._clock(),
            content_hash=content_hash(_HASH_SEPARATOR.join(b.content for b in blocks)),
            detected_language=DetectedLanguage(
                code=_DEFAULT_LANGUAGE,
                source="auto_detected",
                confidence=_DEFAULT_LANGUAGE_CONFIDENCE,
            ),
            classification_tag=classification_tag(names),
            metadata=metadata,
        )


def _source_uri(source: str, path: Path | None) -> str:
    return str(path.resolve()) if path is not None else source


def _resequenced(blocks: list[ContentBlock]) -> list[ContentBlock]:
    return [
        ContentBlock(id=b.id, kind=b.kind, name=b.name, content=b.content, sequence=index)
        for index, b in enumerate(blocks)
    ]
