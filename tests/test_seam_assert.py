"""Tests for the row-count invariant assertion utility (_seam_assert.py).

These tests validate that the assertion logic correctly handles:
- Expected equal counts (pass)
- Expected less_equal counts (pass)
- Unexpected unequal counts (fail — SystemExit)
- Unexpected greater counts (fail — SystemExit)
- --strict mode warnings on expected exclusions
- Edge cases: zero counts, negative counts, large counts
"""

from __future__ import annotations

import pytest
from scripts._seam_assert import assert_seam


class TestSeamAssertEqual:
    """Tests for expected='equal' mode."""

    def test_equal_counts_pass(self):
        assert_seam("test", 100, 100, expected="equal")

    def test_unequal_counts_fail(self):
        with pytest.raises(SystemExit, match="SEAM FAIL"):
            assert_seam("test", 100, 99, expected="equal")

    def test_zero_counts_pass(self):
        assert_seam("empty", 0, 0, expected="equal")

    def test_large_unequal_counts_fail(self):
        with pytest.raises(SystemExit):
            assert_seam("bulk", 10000, 1, expected="equal")

    def test_seam_name_included_in_failure(self):
        with pytest.raises(SystemExit, match="corpus→review"):
            assert_seam("corpus→review", 100, 50, expected="equal")


class TestSeamAssertLessEqual:
    """Tests for expected='less_equal' mode."""

    def test_less_counts_pass(self):
        assert_seam("test", 100, 95, expected="less_equal")

    def test_equal_counts_pass(self):
        assert_seam("test", 100, 100, expected="less_equal")

    def test_greater_counts_fail(self):
        with pytest.raises(SystemExit, match="SEAM FAIL"):
            assert_seam("test", 100, 105, expected="less_equal")

    def test_within_tolerance_pass(self):
        assert_seam("test", 100, 102, expected="less_equal", tolerance=5)

    def test_beyond_tolerance_fail(self):
        with pytest.raises(SystemExit):
            assert_seam("test", 100, 110, expected="less_equal", tolerance=5)


class TestSeamAssertSkipIds:
    """Tests for skipped_ids tracking."""

    def test_skip_ids_in_failure_message(self):
        with pytest.raises(SystemExit, match="pr-123"):
            assert_seam("test", 100, 98, skipped_ids=["pr-123"])

    def test_multiple_skip_ids_in_failure_message(self):
        with pytest.raises(SystemExit, match="pr-123.*pr-456"):
            assert_seam("test", 100, 98, skipped_ids=["pr-123", "pr-456"])


class TestSeamAssertStrictMode:
    """Tests for --strict mode."""

    def test_strict_mode_warns_on_exclusion(self, capsys):
        assert_seam("test", 100, 98, expected="less_equal", strict=True)
        captured = capsys.readouterr()
        assert "SEAM WARNING" in captured.out
        assert "100 → 98" in captured.out

    def test_strict_mode_no_warning_on_equal(self, capsys):
        assert_seam("test", 100, 100, expected="equal", strict=True)
        captured = capsys.readouterr()
        assert "SEAM WARNING" not in captured.out


class TestSeamAssertEdgeCases:
    """Tests for edge cases."""

    def test_negative_counts_raise_value_error(self):
        with pytest.raises(ValueError, match="negative"):
            assert_seam("negative", -1, 0, expected="equal")

    def test_unknown_expected_raises_value_error(self):
        with pytest.raises(ValueError, match="unknown expected"):
            assert_seam("bad", 10, 10, expected="invalid")
