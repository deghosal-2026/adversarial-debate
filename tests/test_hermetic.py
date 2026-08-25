"""Hermetic-only guard: no network in tests (WBS T1.2, global gate 'zero paid-LLM calls in CI')."""

import socket

import pytest


def test_outbound_socket_is_blocked() -> None:
    with pytest.raises(RuntimeError, match="hermetic"):
        socket.create_connection(("example.com", 443))


def test_socket_constructor_is_blocked() -> None:
    with pytest.raises(RuntimeError, match="hermetic"):
        socket.socket(socket.AF_INET, socket.SOCK_STREAM)
