"""Package scaffold contract: public API is importable from a normal install."""

import adversarial_debate
from adversarial_debate import adapters, cli, engine, providers, schemas, store


def test_public_api_importable() -> None:
    assert adversarial_debate.__version__


def test_subpackages_importable() -> None:
    assert adapters and cli and engine and providers and schemas and store
