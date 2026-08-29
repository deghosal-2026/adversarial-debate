"""Tests for the noise-floor bootstrap resampling logic.

These tests verify that the bootstrap CI computation is correct
and that the noise-floor script handles edge cases gracefully.
Zero LLM calls. Deterministic.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from scripts._seam_assert import assert_seam


def _bootstrap_ci(
    values: list[float],
    n_resamples: int = 10000,
    seed: int = 0,
) -> dict[str, float]:
    """Replicate bootstrap logic from noise_floor.py for testing."""
    if not values:
        return {"mean": 0.0, "std": 0.0, "ci_low": 0.0, "ci_high": 0.0, "n": 0}

    rng = random.Random(seed)
    means = []
    n = len(values)
    for _ in range(n_resamples):
        sample = [rng.choice(values) for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    tail = (1 - 0.95) / 2
    low_idx = int(tail * n_resamples)
    high_idx = int((1 - tail) * n_resamples) - 1
    mean_of_means = sum(means) / len(means)
    std = math.sqrt(sum((m - mean_of_means) ** 2 for m in means) / len(means))
    return {
        "mean": sum(values) / n,
        "std": std,
        "ci_low": means[low_idx],
        "ci_high": means[high_idx],
        "n": n,
    }


def test_bootstrap_identical_values() -> None:
    """Identical values should yield zero standard deviation."""
    result = _bootstrap_ci([0.5] * 100, n_resamples=1000)
    assert result["std"] == 0.0
    assert result["mean"] == 0.5


def test_bootstrap_single_value() -> None:
    """Single value should have zero std and mean equals value."""
    result = _bootstrap_ci([0.75], n_resamples=1000)
    assert result["n"] == 1
    assert result["mean"] == 0.75
    assert result["std"] == 0.0


def test_bootstrap_empty() -> None:
    """Empty list returns zeroed result."""
    result = _bootstrap_ci([], n_resamples=1000)
    assert result["n"] == 0
    assert result["mean"] == 0.0


def test_bootstrap_ci_contains_mean() -> None:
    """The observed mean should fall within the CI."""
    random.seed(42)
    values = [random.gauss(0.5, 0.1) for _ in range(100)]
    result = _bootstrap_ci(values, n_resamples=5000, seed=42)
    assert result["ci_low"] <= result["mean"] <= result["ci_high"]


def test_bootstrap_reproducible() -> None:
    """Same seed produces identical results."""
    values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    r1 = _bootstrap_ci(values, n_resamples=5000, seed=42)
    r2 = _bootstrap_ci(values, n_resamples=5000, seed=42)
    assert r1["mean"] == r2["mean"]
    assert r1["ci_low"] == r2["ci_low"]
    assert r1["ci_high"] == r2["ci_high"]


def test_bootstrap_wider_ci_for_fewer_samples() -> None:
    """Fewer samples should produce wider confidence intervals."""
    random.seed(42)
    values = [random.gauss(0.5, 0.2) for _ in range(5)]
    many_values = [random.gauss(0.5, 0.2) for _ in range(100)]
    few = _bootstrap_ci(values, n_resamples=2000, seed=42)
    many = _bootstrap_ci(many_values, n_resamples=2000, seed=42)
    few_range = few["ci_high"] - few["ci_low"]
    many_range = many["ci_high"] - many["ci_low"]
    assert few_range > many_range, f"few={few_range:.3f} should be > many={many_range:.3f}"


def test_bootstrap_binary_metric() -> None:
    """Binary (0/1) metrics should produce sensible CIs."""
    values = [1.0] * 8 + [0.0] * 2
    result = _bootstrap_ci(values, n_resamples=5000, seed=42)
    assert abs(result["mean"] - 0.8) < 0.01
    assert result["std"] > 0


def test_seam_assert_importable() -> None:
    """Verify the seam assert helper is accessible."""
    assert_seam("test", 5, 5, expected="equal", strict=True)
    assert_seam("test", 5, 3, expected="less_equal", strict=True)


def test_noise_floor_script_loads() -> None:
    """The noise-floor script should import without errors."""
    import importlib.util
    base = Path(__file__).resolve().parent.parent
    script_path = base / "scripts" / "noise_floor.py"
    spec = importlib.util.spec_from_file_location("noise_floor", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "main")