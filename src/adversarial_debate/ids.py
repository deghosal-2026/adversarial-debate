"""ID/hash utilities (WBS T1.7): SHA-256 content hashes, monotonic sequences, IDs.

Deterministic IDs keep transcripts reproducible across runs on the same input
(PRD §6.4): the same payload always yields the same id, so audit logs can be
cross-checked without persisting a mapping.
"""

import hashlib
import threading


def content_hash(data: str | bytes) -> str:
    """SHA-256 hex digest of UTF-8 text or raw bytes."""
    raw = data.encode() if isinstance(data, str) else data
    return hashlib.sha256(raw).hexdigest()


def deterministic_id(prefix: str, payload: str) -> str:
    """Stable ``<prefix>_<16 hex chars>`` id derived from the payload.

    Same payload in, same id out — unlike uuid4 — so entity ids can be
    recomputed from content during resume/replay.
    """
    if not prefix:
        msg = "deterministic_id requires a non-empty prefix"
        raise ValueError(msg)
    return f"{prefix}_{hashlib.sha256(payload.encode()).hexdigest()[:16]}"


class SequenceCounter:
    """Monotonic 1-based sequence numbers; one instance per artifact/session."""

    def __init__(self) -> None:
        """Start a fresh counter at 0; first ``next()`` returns 1."""
        self._value = 0
        self._lock = threading.Lock()

    def next(self) -> int:
        """Return the next monotonic value; thread-safe."""
        with self._lock:
            self._value += 1
            return self._value

    @property
    def value(self) -> int:
        """Last issued number (0 before the first call)."""
        return self._value
