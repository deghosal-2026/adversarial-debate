"""Config model + TOML loader contract (WBS T1.6, F8 BYOM registry shape, DD-01)."""

from pathlib import Path

import pytest

from adversarial_debate.config import AdvdebConfig, ConfigError, load_config, parse_toml

FULL_TOML = """\
rounds = 3
max_llm_calls = 40
keep_transcripts_days = 30
seed = 1234

[providers.a]
type = "openai_compatible"
base_url = "https://api.example.com/v1"
model = "model-x"
key_env = "EXAMPLE_API_KEY"

[providers.b]
type = "openai_compatible"
base_url = "https://other.example.com/v1"
model = "model-y"
key_env = "OTHER_API_KEY"
"""

MINIMAL_TOML = """\
[providers.a]
type = "scripted"
model = "stub-a"
key_env = "UNUSED_A"

[providers.b]
type = "scripted"
model = "stub-b"
key_env = "UNUSED_B"
"""


def write(tmp_path: Path, text: str) -> Path:
    cfg = tmp_path / "advdeb.toml"
    cfg.write_text(text)
    return cfg


def test_full_config_parses() -> None:
    config = parse_toml(FULL_TOML)
    assert config.rounds == 3
    assert config.providers.a.model == "model-x"
    assert config.providers.b.key_env == "OTHER_API_KEY"
    assert config.seed == 1234
    assert config.max_llm_calls == 40
    assert config.keep_transcripts_days == 30


def test_defaults_match_design_decisions() -> None:
    config = parse_toml(MINIMAL_TOML)
    assert config.rounds == 2  # DD-01: bounded rounds default 2
    assert config.seed is None
    assert config.max_llm_calls > 0
    assert config.keep_transcripts_days is None


def test_rounds_bounds_enforced_with_readable_error() -> None:
    with pytest.raises(ConfigError, match="rounds"):
        parse_toml(FULL_TOML.replace("rounds = 3", "rounds = 0"))


def test_missing_provider_slot_is_actionable() -> None:
    broken = FULL_TOML.partition("[providers.b]")[0]
    with pytest.raises(ConfigError, match=r"(?i)b.*provider|provider.*b"):
        parse_toml(broken)


def test_unknown_keys_rejected_typo_friendly() -> None:
    with pytest.raises(ConfigError, match="seedd"):
        parse_toml(FULL_TOML + "\nseedd = 7\n")


def test_raw_api_key_rejected_by_design() -> None:
    """Secrets live in env vars referenced by ``key_env`` — never in the file."""
    leak = FULL_TOML.replace(
        'key_env = "OTHER_API_KEY"', 'key_env = "OTHER_API_KEY"\napi_key = "sk-secret"'
    )
    with pytest.raises(ConfigError, match="api_key"):
        parse_toml(leak)


def test_missing_file_reports_path(tmp_path: Path) -> None:
    target = tmp_path / "nope.toml"
    with pytest.raises(ConfigError, match=r"nope\.toml"):
        load_config(target)


def test_toml_syntax_error_is_readable() -> None:
    with pytest.raises(ConfigError, match="syntax"):
        parse_toml("rounds = [unbalanced")


def test_file_syntax_error_reports_path(tmp_path: Path) -> None:
    cfg = tmp_path / "broken.toml"
    cfg.write_text("[providers.a\nbroken")
    with pytest.raises(ConfigError, match=r"broken\.toml.*syntax"):
        load_config(cfg)


def test_file_validation_error_lists_fields(tmp_path: Path) -> None:
    cfg = write(tmp_path, FULL_TOML.replace("rounds = 3", "rounds = 99"))
    with pytest.raises(ConfigError, match=r"rounds"):
        load_config(cfg)


def test_loader_reads_real_file(tmp_path: Path) -> None:
    config = load_config(write(tmp_path, FULL_TOML))
    assert isinstance(config, AdvdebConfig)


def test_shipped_example_parses() -> None:
    """The committed advdeb.toml.example must always be valid."""
    example = Path(__file__).resolve().parents[1] / "advdeb.toml.example"
    config = load_config(example)
    assert config.providers.a.model  # heterogeneous pairs encouraged (DD-04)
