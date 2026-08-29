"""Tests for model pair configuration and pipeline integration.

These tests validate that model pairs are correctly configured, that
model slugs resolve to valid providers, and that the pipeline handles
the new pair correctly. No LLM calls are made — all tests are deterministic.
"""

from __future__ import annotations

from pathlib import Path


def _load_script_module(script_name: str):
    import importlib.util

    base = Path(__file__).resolve().parent.parent
    script_path = base / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(script_name.replace(".py", ""), script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPairConfiguration:
    """pair8_deepseek_gpt_mini must be correctly configured."""

    def test_pair_is_configured(self):
        combine = _load_script_module("03_combine_results.py")
        assert "pair8_deepseek_gpt_mini" in combine.PAIRS

    def test_pair_has_correct_models(self):
        combine = _load_script_module("03_combine_results.py")
        pair = combine.PAIRS["pair8_deepseek_gpt_mini"]
        assert pair["a"] == "deepseek_deepseek-chat"
        assert pair["b"] == "openai_gpt-4o-mini"

    def test_both_models_are_distinct(self):
        combine = _load_script_module("03_combine_results.py")
        pair = combine.PAIRS["pair8_deepseek_gpt_mini"]
        assert pair["a"] != pair["b"]

    def test_neither_model_is_mistral(self):
        combine = _load_script_module("03_combine_results.py")
        pair = combine.PAIRS["pair8_deepseek_gpt_mini"]
        assert "mistral" not in pair["a"]
        assert "mistral" not in pair["b"]

    def test_no_duplicate_with_existing_pairs(self):
        combine = _load_script_module("03_combine_results.py")
        existing_pairs = {k: v for k, v in combine.PAIRS.items() if k != "pair8_deepseek_gpt_mini"}
        new_pair = combine.PAIRS["pair8_deepseek_gpt_mini"]
        for name, existing in existing_pairs.items():
            same_a = existing["a"] == new_pair["a"]
            same_b = existing["b"] == new_pair["b"]
            assert not (same_a and same_b), f"Duplicate of existing pair {name}"

    def test_llama_pair_is_optional(self):
        combine = _load_script_module("03_combine_results.py")
        if "pair9_llama_gpt" in combine.PAIRS:
            pair = combine.PAIRS["pair9_llama_gpt"]
            assert "llama" in pair["a"] or "llama" in pair["b"]

    def test_baseline_gpt_has_null_side_b(self):
        combine = _load_script_module("03_combine_results.py")
        assert combine.PAIRS["baseline_gpt"]["b"] is None

    def test_all_pairs_have_side_a(self):
        combine = _load_script_module("03_combine_results.py")
        for name, pair in combine.PAIRS.items():
            assert pair["a"] is not None, f"Pair {name} missing side_a"


class TestPairModelSlugs:
    """Model slugs used in pairs must be in the expected format."""

    def test_deepseek_slug_format(self):
        combine = _load_script_module("03_combine_results.py")
        slug = combine.PAIRS["pair8_deepseek_gpt_mini"]["a"]
        assert isinstance(slug, str)
        assert len(slug) > 0
        assert "_" in slug  # slug format: provider_model

    def test_gpt_mini_slug_format(self):
        combine = _load_script_module("03_combine_results.py")
        slug = combine.PAIRS["pair8_deepseek_gpt_mini"]["b"]
        assert isinstance(slug, str)
        assert len(slug) > 0
        assert "_" in slug

    def test_no_duplicate_slugs_across_pairs(self):
        combine = _load_script_module("03_combine_results.py")
        seen = set()
        for name, pair in combine.PAIRS.items():
            key = (pair["a"], pair["b"])
            assert key not in seen, f"Duplicate pair {name}: {key}"
            seen.add(key)

    def test_baseline_has_valid_side_a(self):
        combine = _load_script_module("03_combine_results.py")
        slug = combine.PAIRS["baseline_gpt"]["a"]
        assert isinstance(slug, str)
        assert len(slug) > 0


class TestPairAssignment:
    """The correct pair is assigned to the correct corpus."""

    def test_full_corpus_includes_new_pair(self):
        combine = _load_script_module("03_combine_results.py")
        assigned = combine.default_pairs_for_corpus(Path("full_corpus.csv"))
        assert "pair8_deepseek_gpt_mini" in assigned

    def test_full_corpus_includes_gpt_mistral(self):
        combine = _load_script_module("03_combine_results.py")
        assigned = combine.default_pairs_for_corpus(Path("full_corpus.csv"))
        assert "pair3_gpt_mistral" in assigned

    def test_validation_subset_uses_deepseek_mistral(self):
        combine = _load_script_module("03_combine_results.py")
        assigned = combine.default_pairs_for_corpus(Path("validation_subset.csv"))
        assert "pair5_deepseek_mistral" in assigned

    def test_negative_control_uses_gpt_gemini(self):
        combine = _load_script_module("03_combine_results.py")
        assigned = combine.default_pairs_for_corpus(Path("negative_control_subset.csv"))
        assert "pair1_gpt_gemini" in assigned


class TestDebatePairAssignment:
    """04_run_debate.py must also include the new pair."""

    def test_debate_full_corpus_includes_new_pair(self):
        debate = _load_script_module("04_run_debate.py")
        assigned = debate.default_pairs_for_corpus(Path("full_corpus.csv"))
        assert "pair8_deepseek_gpt_mini" in assigned

    def test_debate_validation_subset_uses_deepseek_mistral(self):
        debate = _load_script_module("04_run_debate.py")
        assigned = debate.default_pairs_for_corpus(Path("validation_subset.csv"))
        assert "pair5_deepseek_mistral" in assigned
