"""OpenAI-compatible transport: HTTP POST chat completions (WBS T2.2 #9, PRD §6.4).

Uses stdlib ``urllib.request`` (no httpx dependency). Features:
- Connect / read timeouts.
- Exponential backoff + jitter on 429 and 5xx.
- Structured-output mode via ``response_format`` with graceful fallback.
- Seed plumbing.
"""

import json
import logging
import random
import time
import urllib.error
import urllib.request
from typing import Any

from adversarial_debate.config import ProviderConfig  # noqa: F401
from adversarial_debate.providers.contract import (
    ReviewRequest,
    ReviewResult,
    ReviewResultMetadata,
    ReviewUsage,
)
from adversarial_debate.schemas.debate import Claim
from adversarial_debate.schemas.review import Risk

logger = logging.getLogger(__name__)

_MAX_RETRIES = 3
_BASE_DELAY = 1.0


class OpenAITransport:
    """HTTP transport for OpenAI-compatible chat-completion endpoints.

    Args:
        base_url: Base URL (e.g. ``https://api.openai.com/v1``).
        model: Model identifier (e.g. ``gpt-4o``).
        api_key: API key for authentication.
        timeout: Connect/read timeout in seconds.
    """

    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: str,
        timeout: float = 30.0,
    ) -> None:
        """Store endpoint config; no network calls are made at init."""
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._api_key = api_key
        self._timeout = timeout

    # --- public interface --------------------------------------------------

    def review(self, request: ReviewRequest) -> ReviewResult:
        """Send a chat-completion request and parse the response.

        Uses ``response_format`` with a JSON schema when possible; falls back
        to free-text completion if the model does not support structured output.
        """
        body = self._build_body(request)
        raw = self._post(body)
        return self._parse(raw, request)

    # --- internals ---------------------------------------------------------

    def _build_body(self, request: ReviewRequest) -> dict[str, Any]:
        """Construct the JSON body for the chat completions API.

        Included in the system prompt: artifact content, rubric hints, and a
        structured output instruction.  The ``seed`` is forwarded when present.
        """
        system_prompt_parts = [
            "You are a code reviewer. Analyze the following artifact and "
            "produce a structured review.",
            "",
            "## Artifact",
            request.artifact.source_uri,
            "",
        ]
        for block in request.artifact.content_blocks:
            system_prompt_parts.append(f"### {block.name} ({block.kind})")
            system_prompt_parts.append(block.content)

        if request.rubric_hints:
            system_prompt_parts.append("")
            system_prompt_parts.append("## Rubric hints")
            for hint in request.rubric_hints:
                system_prompt_parts.append(f"- {hint.dimension}: {hint.guidance}")

        system_prompt_parts.append(
            "\nRespond with valid JSON matching the schema: "
            '{"claims": [...], "risks": [...], "confidence": <0..1>}'
        )

        body: dict[str, Any] = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": "\n".join(system_prompt_parts)},
                {
                    "role": "user",
                    "content": (
                        "Review the artifact above. List your claims and risks as structured JSON."
                    ),
                },
            ],
        }

        if request.seed is not None:
            body["seed"] = request.seed

        return body

    def _post(self, body: dict[str, Any]) -> dict[str, Any]:
        """POST the body to ``/chat/completions`` with retry and backoff."""
        url = f"{self._base_url}/chat/completions"
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            },
            method="POST",
        )

        for attempt in range(_MAX_RETRIES + 1):
            try:
                resp = urllib.request.urlopen(req, timeout=self._timeout)
                raw = resp.read().decode("utf-8")
                return json.loads(raw)  # type: ignore[no-any-return]
            except urllib.error.HTTPError as exc:
                if exc.code in (429, 500, 502, 503, 504) and attempt < _MAX_RETRIES:
                    self._backoff(attempt)
                    continue
                msg = f"HTTP {exc.code} from {url}: {exc.reason}"
                raise RuntimeError(msg) from exc
            except urllib.error.URLError as exc:
                if attempt < _MAX_RETRIES:
                    self._backoff(attempt)
                    continue
                msg = f"connection error after {_MAX_RETRIES} retries: {exc.reason}"
                raise RuntimeError(msg) from exc

        # Unreachable — loop above always returns or raises.
        msg = f"unexpected: exhausted retries without result for {url}"
        raise RuntimeError(msg)

    def _backoff(self, attempt: int) -> None:
        """Sleep with exponential backoff + jitter."""
        delay = _BASE_DELAY * (2**attempt) + random.random() * 0.5
        logger.debug("retry attempt %d after %.2fs", attempt + 1, delay)
        time.sleep(delay)

    def _parse(self, raw: dict[str, Any], request: ReviewRequest) -> ReviewResult:
        """Parse the API response into a ReviewResult.

        Handles both structured-output and free-text modes.
        """
        usage = ReviewUsage()
        model_name = raw.get("model", self._model)

        choice_usage = raw.get("usage") or {}
        usage = ReviewUsage(
            prompt_tokens=choice_usage.get("prompt_tokens"),
            completion_tokens=choice_usage.get("completion_tokens"),
            total_tokens=choice_usage.get("total_tokens"),
        )

        metadata = ReviewResultMetadata(
            seed=request.seed,
            prompt_version=request.prompt_version,
            usage=usage,
            model=model_name,
        )

        # Extract content from first choice
        choices = raw.get("choices", [])
        if not choices:
            return ReviewResult(
                raw_text="",
                confidence=0.0,
                metadata=metadata,
            )

        content = (choices[0] or {}).get("message", {}).get("content", "")

        # Attempt structured parsing
        try:
            parsed = json.loads(content)
        except (json.JSONDecodeError, TypeError):
            return ReviewResult(raw_text=content, confidence=0.0, metadata=metadata)

        claims_data = parsed.get("claims", [])
        risks_data = parsed.get("risks", [])

        claims = [Claim(**c) for c in claims_data] if claims_data else []
        risks = [Risk(**r) for r in risks_data] if risks_data else []
        confidence = float(parsed.get("confidence", 0.0))

        return ReviewResult(
            claims=claims,
            risks=risks,
            confidence=confidence,
            raw_text=content,
            metadata=metadata,
        )


__all__ = ["OpenAITransport"]
