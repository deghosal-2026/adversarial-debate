"""PR-review domain adapter (F7): git diff + metadata → ``ReviewArtifact``.

Public surface of the reference §5.3 adapter. Importing this package
registers [PR_REVIEW_NORMALIZER][...] under the ``pr_review`` domain.
"""

from adversarial_debate.adapters import register
from adversarial_debate.adapters.pr_review.chunking import (
    Chunk,
    ChunkPlan,
    chunk_metadata,
    estimate_tokens,
    plan_chunks,
)
from adversarial_debate.adapters.pr_review.diff_parser import ParsedDiff, parse_diff
from adversarial_debate.adapters.pr_review.language import (
    classification_tag,
    guess_language,
    summarize_languages,
)
from adversarial_debate.adapters.pr_review.metadata import (
    ExtractionResult,
    GhCli,
    GhRunner,
    PrMetadataExtractor,
)
from adversarial_debate.adapters.pr_review.normalizer import (
    DEFAULT_RUBRIC_HINTS,
    PrReviewNormalizer,
)

__all__ = [
    "DEFAULT_RUBRIC_HINTS",
    "PR_REVIEW_NORMALIZER",
    "Chunk",
    "ChunkPlan",
    "ExtractionResult",
    "GhCli",
    "GhRunner",
    "ParsedDiff",
    "PrMetadataExtractor",
    "PrReviewNormalizer",
    "chunk_metadata",
    "classification_tag",
    "estimate_tokens",
    "guess_language",
    "parse_diff",
    "plan_chunks",
    "summarize_languages",
]

PR_REVIEW_NORMALIZER = PrReviewNormalizer()
register("pr_review", PR_REVIEW_NORMALIZER)
