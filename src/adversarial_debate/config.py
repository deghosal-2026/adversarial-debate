"""Config model + TOML loader (WBS T1.6, F8 BYOM registry, PRD §6.4 reproducibility).

Design decisions honored here: DD-01 (rounds default 2), DD-03/§6.4 (seed for
reproducible runs). Secrets are referenced by environment-variable name
(``key_env``) and never stored in config files — raw keys are rejected.
Validation errors are human-readable: no raw tracebacks reach the user.
"""

import tomllib
from pathlib import Path
from typing import Any

from pydantic import Field, ValidationError

from adversarial_debate.schemas.base import SchemaBase


class ConfigError(Exception):
    """Raised when advdeb.toml is missing or invalid; message is user-facing."""


class ProviderConfig(SchemaBase):
    """One reviewer's model endpoint — registry key resolved by the M2 provider layer."""

    type: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    base_url: str | None = None
    model: str = Field(min_length=1)
    key_env: str = Field(min_length=1)


class ProvidersConfig(SchemaBase):
    """The two reviewer slots. Heterogeneous pairs encouraged (DD-04)."""

    a: ProviderConfig
    b: ProviderConfig


class AdvdebConfig(SchemaBase):
    """Full v0.1.0 configuration surface (F8 shape); retention is a stub until M8."""

    providers: ProvidersConfig
    rounds: int = Field(default=2, ge=1, le=10)
    max_llm_calls: int = Field(default=50, ge=1)
    keep_transcripts_days: int | None = Field(default=None, ge=1)
    seed: int | None = None


def _readable_errors(exc: ValidationError) -> str:
    lines = []
    for error in exc.errors():
        loc = ".".join(str(part) for part in error["loc"])
        msg = error["msg"].removeprefix("Value error, ")
        lines.append(f"  - {loc}: {msg}")
    return "\n".join(lines)


def _build(raw: dict[str, Any]) -> AdvdebConfig:
    try:
        return AdvdebConfig.model_validate(raw)
    except ValidationError as exc:
        msg = f"invalid advdeb.toml:\n{_readable_errors(exc)}"
        raise ConfigError(msg) from exc


def parse_toml(text: str) -> AdvdebConfig:
    """Parse TOML text into [AdvdebConfig][adversarial_debate.config.AdvdebConfig]."""
    try:
        raw = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        msg = f"invalid advdeb.toml: TOML syntax error: {exc}"
        raise ConfigError(msg) from exc
    return _build(raw)


def load_config(path: Path | str) -> AdvdebConfig:
    """Load and validate ``advdeb.toml`` from disk; raises [ConfigError][...]."""
    file_path = Path(path)
    if not file_path.is_file():
        msg = f"config file not found: {file_path} (run 'advdeb init' to scaffold one)"
        raise ConfigError(msg)
    try:
        raw = tomllib.loads(file_path.read_text())
    except tomllib.TOMLDecodeError as exc:
        msg = f"invalid advdeb.toml at {file_path}: TOML syntax error: {exc}"
        raise ConfigError(msg) from exc
    try:
        return AdvdebConfig.model_validate(raw)
    except ValidationError as exc:
        msg = f"invalid advdeb.toml at {file_path}:\n{_readable_errors(exc)}"
        raise ConfigError(msg) from exc
