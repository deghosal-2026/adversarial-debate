"""Hermetic-only test guard (WBS T1.2).

Global exit gate: zero paid-LLM calls and zero network access in CI (PRD §2.5).
Every test runs with outbound sockets disabled; a test that needs the network is
a bug, not a configuration problem. Set ``ADVDEB_ALLOW_NETWORK=1`` only when
debugging locally — never in CI.
"""

import os
import socket

import pytest

_BLOCK_MESSAGE = (
    "hermetic test suite: network access is disabled "
    "(zero paid-LLM calls in CI; use scripted reviewers). "
    "Set ADVDEB_ALLOW_NETWORK=1 only for local debugging."
)


def _blocked(*_args: object, **_kwargs: object) -> None:
    raise RuntimeError(_BLOCK_MESSAGE)


@pytest.fixture(autouse=True)
def _hermetic(monkeypatch: pytest.MonkeyPatch) -> None:
    if os.environ.get("ADVDEB_ALLOW_NETWORK") == "1":
        return
    monkeypatch.setattr(socket, "socket", _blocked)
    monkeypatch.setattr(socket, "create_connection", _blocked)
    monkeypatch.setattr(socket, "getaddrinfo", _blocked)
