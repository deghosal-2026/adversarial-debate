"""ScriptedReviewer: deterministic test double from canned YAML scenarios (WBS T2.6 #13, PRD §2.5).

Zero paid LLM calls in CI — this is the only reviewer used during automated tests.
Supports malformed-output scenarios to exercise fail-closed paths in M5.
"""

import os
import sys
from pathlib import Path
from typing import Any

import yaml

from adversarial_debate.providers.contract import (
    ReviewRequest,
    ReviewResult,
    ReviewResultMetadata,
)
from adversarial_debate.schemas.debate import Claim
from adversarial_debate.schemas.review import Risk


class ScriptedReviewer:
    """Deterministic reviewer returning canned responses from a YAML scenario file.

    Args:
        model: Not used as a model identifier; kept for API consistency.
        scenarios_path: Path to the YAML scenario file. Defaults to the
            ``ADVDEB_SCENARIOS`` env var or ``scenarios/review_scenarios.yaml``.
    """

    def __init__(self, model: str = "", scenarios_path: str | None = None) -> None:
        """Load YAML scenarios; defaults to env ADVDEB_SCENARIOS or local path."""
        self._model = model
        path = scenarios_path or os.environ.get(
            "ADVDEB_SCENARIOS", "tests/scenarios/review_scenarios.yaml"
        )
        self._scenarios: list[dict[str, Any]] = []
        self._load(path)

    def _load(self, path: str) -> None:
        try:
            data = yaml.safe_load(Path(path).read_text())
        except FileNotFoundError:
            self._scenarios = []
            print(
                f"WARNING: scenarios file not found: {path}; "
                f"reviewer will return empty results",
                file=sys.stderr,
            )
            return
        if isinstance(data, dict) and "scenarios" in data:
            self._scenarios = data["scenarios"]
        else:
            self._scenarios = []
            print(
                f"WARNING: scenarios file {path} has no 'scenarios' key; "
                f"reviewer will return empty results",
                file=sys.stderr,
            )

    def review(self, request: ReviewRequest) -> ReviewResult:
        """Match the request against scenarios and return canned result.

        Matching is by ``artifact_prefix`` against ``request.artifact.id``.
        The first matching scenario wins.  If none match, an empty result is
        returned.
        """
        for scenario in self._scenarios:
            match = scenario.get("match", {})
            prefix = match.get("artifact_prefix", "")
            if prefix and request.artifact.id.startswith(prefix):
                return self._build_result(scenario, request)

        # Fallback: no matching scenario
        return ReviewResult(
            raw_text="No matching scenario",
            confidence=0.0,
            metadata=ReviewResultMetadata(
                seed=request.seed,
                prompt_version=request.prompt_version,
                model=self._model,
            ),
        )

    def _build_result(self, scenario: dict[str, Any], request: ReviewRequest) -> ReviewResult:
        """Build a ReviewResult from a YAML scenario entry."""
        output = scenario.get("output", {})
        raw_text = output.get("raw_text", "")

        claims = [Claim(**c) for c in output.get("claims", [])]
        risks = [Risk(**r) for r in output.get("risks", [])]
        confidence = float(output.get("confidence", 0.0))

        return ReviewResult(
            claims=claims,
            risks=risks,
            confidence=confidence,
            raw_text=raw_text,
            metadata=ReviewResultMetadata(
                seed=request.seed,
                prompt_version=request.prompt_version,
                model=self._model,
            ),
        )


__all__ = ["ScriptedReviewer"]
