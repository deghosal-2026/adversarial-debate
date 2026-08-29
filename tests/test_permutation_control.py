"""Tests for the permutation control logic.

These tests verify that the Jaccard similarity, tokenization, and
simulated judge verdict functions are correct. Zero LLM calls. Deterministic.
"""

from __future__ import annotations

from pathlib import Path


def test_tokenize_basic() -> None:
    from scripts.permutation_control import tokenize

    tokens = tokenize("this is a test of the tokenization function")
    assert "test" in tokens
    assert "tokenization" in tokens
    assert "function" in tokens
    assert "the" not in tokens
    assert "this" not in tokens
    assert "is" not in tokens


def test_tokenize_lowercases() -> None:
    from scripts.permutation_control import tokenize

    tokens = tokenize("UPPERCASE Word")
    assert "uppercase" in tokens
    assert "word" in tokens


def test_tokenize_short_tokens() -> None:
    from scripts.permutation_control import tokenize

    tokens = tokenize("a be cat dog")
    assert "a" not in tokens  # too short
    assert "be" not in tokens  # stopword
    assert "cat" in tokens
    assert "dog" in tokens


def test_tokenize_skips_stopwords() -> None:
    from scripts.permutation_control import STOPWORDS, tokenize

    text = " ".join(list(STOPWORDS)[:20])
    tokens = tokenize(text)
    assert len(tokens) == 0


def test_jaccard_identical() -> None:
    from scripts.permutation_control import jaccard, tokenize

    a = tokenize("the quick brown fox jumps")
    assert jaccard(a, a) == 1.0


def test_jaccard_disjoint() -> None:
    from scripts.permutation_control import jaccard, tokenize

    a = tokenize("quick brown fox")
    b = tokenize("lazy sleeping dog")
    assert jaccard(a, b) == 0.0


def test_jaccard_partial() -> None:
    from scripts.permutation_control import jaccard, tokenize

    a = tokenize("quick brown fox")
    b = tokenize("brown fox jumps")
    sim = jaccard(a, b)
    assert 0.0 < sim < 1.0
    assert abs(sim - 2 / 4) < 0.001  # 2 of 4 tokens match


def test_jaccard_empty() -> None:
    from scripts.permutation_control import jaccard

    assert jaccard(frozenset(), frozenset({"a"})) == 0.0
    assert jaccard(frozenset(), frozenset()) == 0.0


def test_simulate_judge_match() -> None:
    from scripts.permutation_control import simulate_judge

    assert simulate_judge(0.20) == "MATCH"
    assert simulate_judge(0.15) == "MATCH"


def test_simulate_judge_partial() -> None:
    from scripts.permutation_control import simulate_judge

    assert simulate_judge(0.10) == "PARTIAL"
    assert simulate_judge(0.05) == "PARTIAL"


def test_simulate_judge_no_match() -> None:
    from scripts.permutation_control import simulate_judge

    assert simulate_judge(0.04) == "NO_MATCH"
    assert simulate_judge(0.00) == "NO_MATCH"


def test_permutation_control_loads() -> None:
    """The permutation control script should import without errors."""
    import importlib.util

    base = Path(__file__).resolve().parent.parent
    script_path = base / "scripts" / "permutation_control.py"
    spec = importlib.util.spec_from_file_location("permutation_control", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "main")
