"""Tests for missed-issue detection logic.

These tests validate that the detection logic correctly identifies whether
a reviewer's claims address a known revert reason. The detection uses
keyword matching and structured comparison — no LLM calls.
"""

from __future__ import annotations

import pytest
from scripts.missed_issues import ReviewResult, compute_missed_issue_rate, detect_missed_issue


class TestMissedIssueDetection:
    """Tests for detect_missed_issue() function."""

    def test_issue_detected_when_claim_matches(self):
        result = ReviewResult(
            artifact_id="pr-123",
            model="gpt-4o-mini",
            claims=["Missing null check on user input", "No rollback for failed migration"],
        )
        revert_reason = "Null pointer exception on user input"
        assert detect_missed_issue(result, revert_reason) is False

    def test_issue_missed_when_no_claim_matches(self):
        result = ReviewResult(
            artifact_id="pr-123",
            model="gpt-4o-mini",
            claims=["Minor formatting issue", "Variable naming could be clearer"],
        )
        revert_reason = "Null pointer exception on user input"
        assert detect_missed_issue(result, revert_reason) is True

    def test_empty_claims_always_missed(self):
        result = ReviewResult(
            artifact_id="pr-123",
            model="gpt-4o-mini",
            claims=[],
        )
        assert detect_missed_issue(result, "Service crashed") is True

    def test_multiple_claims_one_match_is_sufficient(self):
        result = ReviewResult(
            artifact_id="pr-123",
            model="gpt-4o-mini",
            claims=[
                "Color scheme could be improved",
                "Missing authentication check on admin endpoint",
                "Typo in comment",
            ],
        )
        revert_reason = "Unauthorized admin access via missing auth check"
        assert detect_missed_issue(result, revert_reason) is False

    def test_case_insensitive_matching(self):
        result = ReviewResult(
            artifact_id="pr-123",
            model="gpt-4o-mini",
            claims=["No rollback for database migration"],
        )
        revert_reason = "Database Migration failure required manual rollback"
        assert detect_missed_issue(result, revert_reason) is False

    def test_partial_keyword_match_is_sufficient(self):
        result = ReviewResult(
            artifact_id="pr-123",
            model="gpt-4o-mini",
            claims=["Race condition in concurrent requests"],
        )
        revert_reason = "Race condition caused data corruption"
        assert detect_missed_issue(result, revert_reason) is False

    def test_stop_words_do_not_count_as_match(self):
        result = ReviewResult(
            artifact_id="pr-123",
            model="gpt-4o-mini",
            claims=["The system should be just really quite robust indeed"],
        )
        revert_reason = "The failure was caused by the system again"
        assert detect_missed_issue(result, revert_reason) is True

    def test_very_short_claims_are_ignored(self):
        result = ReviewResult(
            artifact_id="pr-123",
            model="gpt-4o-mini",
            claims=["LGTM", "OK", "x"],
        )
        assert detect_missed_issue(result, "Service crashed") is True


class TestMissedIssueRateComputation:
    """Tests for compute_missed_issue_rate() function."""

    def test_all_issues_missed_returns_100_percent(self):
        results = {
            "gpt": {"pr-1": False, "pr-2": False, "pr-3": False},
            "mistral": {"pr-1": False, "pr-2": False, "pr-3": False},
        }
        report = compute_missed_issue_rate(results, {"pr-1": "a", "pr-2": "b", "pr-3": "c"})
        assert report["pairs"]["gpt"]["missed_rate"] == 1.0
        assert report["pairs"]["mistral"]["missed_rate"] == 1.0

    def test_no_issues_missed_returns_zero_percent(self):
        results = {
            "gpt": {"pr-1": True, "pr-2": True},
            "mistral": {"pr-1": True, "pr-2": True},
        }
        report = compute_missed_issue_rate(results, {"pr-1": "a", "pr-2": "b"})
        assert report["pairs"]["gpt"]["missed_rate"] == 0.0
        assert report["pairs"]["mistral"]["missed_rate"] == 0.0

    def test_partial_miss_rate_is_correct(self):
        results = {"gpt": {f"pr-{i}": False for i in range(3)}}
        results["gpt"].update({f"pr-{i}": True for i in range(3, 10)})
        report = compute_missed_issue_rate(results, {f"pr-{i}": "a" for i in range(10)})
        assert report["pairs"]["gpt"]["missed_rate"] == pytest.approx(0.3)

    def test_dual_vs_single_comparison(self):
        results = {
            "gpt": {"pr-1": True, "pr-2": False, "pr-3": True},
            "mistral": {"pr-1": False, "pr-2": False, "pr-3": True},
        }
        report = compute_missed_issue_rate(results, {"pr-1": "a", "pr-2": "b", "pr-3": "c"})
        assert report["dual"]["missed_rate"] <= report["single_max"]["missed_rate"]
        assert report["improvement_ratio"] >= 1.0

    def test_improvement_ratio_is_correct(self):
        results = {
            "gpt": {"pr-1": True, "pr-2": False, "pr-3": True},
            "mistral": {"pr-1": False, "pr-2": False, "pr-3": False},
        }
        report = compute_missed_issue_rate(results, {"pr-1": "a", "pr-2": "b", "pr-3": "c"})
        assert report["improvement_ratio"] == pytest.approx(3.0, rel=0.1)

    def test_empty_results_returns_zero_rate(self):
        report = compute_missed_issue_rate({}, {})
        assert report["improvement_ratio"] == 1.0


class TestMissedIssuePerDomain:
    """Tests for per-domain breakdown."""

    def test_per_domain_breakdown(self):
        results = {
            "gpt": {
                "pr-1": True, "pr-2": False,
                "pr-3": True, "pr-4": True, "pr-5": False,
            },
        }
        domains = {
            "pr-1": "code_review", "pr-2": "code_review",
            "pr-3": "incident", "pr-4": "incident", "pr-5": "incident",
        }
        report = compute_missed_issue_rate(
            results, {"pr-1": "a", "pr-2": "b", "pr-3": "c", "pr-4": "d", "pr-5": "e"},
            domains=domains,
        )
        assert report["per_domain"]["code_review"]["missed_rate"] == pytest.approx(0.5)
        assert report["per_domain"]["incident"]["missed_rate"] == pytest.approx(1.0 / 3.0)


class TestSurvivorshipBoundary:
    """Tests for survivorship boundary annotation."""

    def test_report_includes_lower_bound(self):
        results = {"gpt": {"pr-1": True}}
        report = compute_missed_issue_rate(results, {"pr-1": "a"})
        assert "lower bound" in report["survivorship_boundary"]

    def test_boundary_includes_failure_count(self):
        results = {"gpt": {"pr-1": True, "pr-2": False}}
        report = compute_missed_issue_rate(results, {"pr-1": "a", "pr-2": "b"})
        assert "2" in report["survivorship_boundary"]

    def test_boundary_does_not_overclaim(self):
        results = {"gpt": {"pr-1": True}}
        report = compute_missed_issue_rate(results, {"pr-1": "a"})
        assert "complete" not in report["survivorship_boundary"].lower()


class TestMissedIssueCSVOutput:
    """Tests for CSV output formatting."""

    def test_csv_has_expected_columns(self):
        from scripts.missed_issues import format_csv_output

        report = {
            "pairs": {"gpt_mistral": {"missed_rate": 0.057, "missed": 4, "total": 70}},
            "per_domain": {},
            "improvement_ratio": 2.5,
        }
        output = format_csv_output(report)
        assert "pair_name" in output
        assert "missed_rate" in output
        assert "improvement_ratio" in output

    def test_csv_has_one_row_per_pair(self):
        from scripts.missed_issues import format_csv_output

        report = {
            "pairs": {
                "gpt_mistral": {"missed_rate": 0.057, "missed": 4, "total": 70},
                "deepseek_mistral": {"missed_rate": 0.071, "missed": 5, "total": 70},
            },
            "per_domain": {},
            "improvement_ratio": 2.2,
        }
        output = format_csv_output(report)
        rows = output.strip().split("\n")
        assert len(rows) == 3  # header + 2 pairs

    def test_csv_missed_rate_is_percentage(self):
        from scripts.missed_issues import format_csv_output

        report = {
            "pairs": {"gpt_mistral": {"missed_rate": 0.057, "missed": 4, "total": 70}},
            "per_domain": {},
            "improvement_ratio": 2.5,
        }
        output = format_csv_output(report)
        assert "5.7%" in output
