"""Domain adapters: normalizer + rubric + evidence expectations per domain.

Adapter contribution protocol per PRD [05-features §5.3](docs/design/prd/05-features.md);
adapters live in ``adversarial_debate/adapters/<domain>/``, self-register on
import (plugin style), and require no engine changes. Built-in adapters are
loaded lazily on first registry access; importing an adapter package directly
also registers it.
"""

from adversarial_debate.adapters.base import (
    AdapterError,
    DuplicateDomainError,
    Hints,
    MetadataExtractionError,
    NormalizationError,
    Normalizer,
    UnknownDomainError,
    artifact_id_for,
    available_domains,
    get_normalizer,
    normalize,
    register,
    unregister,
    utc_now,
)

__all__ = [
    "AdapterError",
    "DuplicateDomainError",
    "Hints",
    "MetadataExtractionError",
    "NormalizationError",
    "Normalizer",
    "UnknownDomainError",
    "artifact_id_for",
    "available_domains",
    "get_normalizer",
    "normalize",
    "register",
    "unregister",
    "utc_now",
]
