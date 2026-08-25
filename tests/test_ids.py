"""ID/hash utilities contract (WBS T1.7): SHA-256 hashes, sequences, deterministic IDs."""

from datetime import UTC, datetime

import pytest

from adversarial_debate.ids import SequenceCounter, content_hash, deterministic_id
from adversarial_debate.schemas import ReviewArtifact


def test_content_hash_known_sha256_vector() -> None:
    assert (
        content_hash("hello") == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    )


def test_content_hash_accepts_bytes_and_str_equally() -> None:
    assert content_hash(b"hello") == content_hash("hello")


def test_deterministic_id_stable_and_prefixed() -> None:
    first = deterministic_id("cb", "src/app.py:+ pass\n")
    second = deterministic_id("cb", "src/app.py:+ pass\n")
    assert first == second
    assert first.startswith("cb_")
    body = first.removeprefix("cb_")
    assert len(body) == 16
    int(body, 16)  # raises if not pure hex


def test_deterministic_id_differs_for_different_payloads() -> None:
    assert deterministic_id("cb", "a") != deterministic_id("cb", "b")


def test_sequence_counter_is_monotonic_per_instance() -> None:
    counter_a = SequenceCounter()
    counter_b = SequenceCounter()
    assert [counter_a.next(), counter_a.next(), counter_a.next()] == [1, 2, 3]
    assert counter_b.next() == 1  # independent per artifact/session


def test_sequence_counter_value_tracks_last_issued() -> None:
    counter = SequenceCounter()
    assert counter.value == 0
    counter.next()
    counter.next()
    assert counter.value == 2


def test_deterministic_id_requires_prefix() -> None:
    with pytest.raises(ValueError, match="prefix"):
        deterministic_id("", "payload")


def test_generated_hash_satisfies_artifact_schema() -> None:
    """Utility output must be drop-in valid for ReviewArtifact.content_hash."""
    artifact = ReviewArtifact.model_validate(
        {
            "id": "art_x",
            "domain": "pr_review",
            "source_uri": "file:///tmp/x.diff",
            "content_blocks": [{"id": "cb_1", "kind": "diff", "name": "f.py", "content": "+ x"}],
            "created_at": datetime(2026, 8, 24, tzinfo=UTC),
            "content_hash": content_hash("+ x"),
        }
    )
    assert artifact.content_hash == content_hash("+ x")
