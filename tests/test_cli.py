"""CLI tests (M9: T9.1-T9.6, WBS M9 exit gate)."""

from __future__ import annotations

import json
import tempfile
from argparse import Namespace
from pathlib import Path
from typing import Any

from adversarial_debate.cli.cli import (
    ExitCode,
    _format_report,
    build_parser,
    cmd_init,
    cmd_list,
    cmd_report,
    cmd_resume,
    cmd_review,
    cmd_transcript,
)
from adversarial_debate.cli.cli import main as _cli_main
from adversarial_debate.engine.debate_controller import DebateEvent
from adversarial_debate.store.store import SQLiteStore


def _make_args(**kwargs: Any) -> Namespace:
    return Namespace(**kwargs)


# ── T9.1 (#40) advdeb init ───────────────────────────────────────────────────


class TestCmdInit:
    def test_init_writes_config(self, tmp_path: Path) -> None:
        path = tmp_path / "advdeb.toml"
        rc = cmd_init(_make_args(path=str(path), force=False))
        assert rc == ExitCode.OK
        assert path.is_file()
        assert "openai_compatible" in path.read_text()

    def test_init_refuses_overwrite_without_force(self, tmp_path: Path) -> None:
        path = tmp_path / "advdeb.toml"
        path.write_text("existing")
        rc = cmd_init(_make_args(path=str(path), force=False))
        assert rc == ExitCode.USAGE
        assert path.read_text() == "existing"

    def test_init_force_overwrites(self, tmp_path: Path) -> None:
        path = tmp_path / "advdeb.toml"
        path.write_text("existing")
        rc = cmd_init(_make_args(path=str(path), force=True))
        assert rc == ExitCode.OK
        assert "openai_compatible" in path.read_text()


# ── T9.2 (#41) advdeb review ─────────────────────────────────────────────────


class TestCmdReview:
    def test_review_fails_without_config(self, tmp_path: Path) -> None:
        path = tmp_path / "nonexistent.toml"
        rc = cmd_review(
            _make_args(
                pr="https://github.com/test/repo/pull/1",
                config=str(path),
                store=str(tmp_path / "test.db"),
                domain="pr_review",
                rounds=2,
                pair=None,
                verbose=False,
            )
        )
        assert rc == ExitCode.USAGE

    def test_review_accepts_valid_config(self, tmp_path: Path) -> None:
        config = tmp_path / "advdeb.toml"
        config.write_text("""
[providers.a]
type = "scripted"
model = "test"
key_env = "MISSING"

[providers.b]
type = "scripted"
model = "test"
key_env = "MISSING"
""")
        rc = cmd_review(
            _make_args(
                pr="https://github.com/test/repo/pull/1",
                config=str(config),
                store=str(tmp_path / "test.db"),
                domain="pr_review",
                rounds=2,
                pair=None,
                verbose=False,
            )
        )
        assert rc == ExitCode.OK

    def test_review_verbose_shows_providers(self, tmp_path: Path, capsys: Any) -> None:
        config = tmp_path / "advdeb.toml"
        config.write_text("""
[providers.a]
type = "scripted"
model = "gpt-4o"
key_env = "MISSING"

[providers.b]
type = "scripted"
model = "claude-3"
key_env = "MISSING"
""")
        cmd_review(
            _make_args(
                pr="https://github.com/test/repo/pull/1",
                config=str(config),
                store=str(tmp_path / "test.db"),
                domain="pr_review",
                rounds=2,
                pair=None,
                verbose=True,
            )
        )
        captured = capsys.readouterr()
        assert "gpt-4o" in captured.out
        assert "claude-3" in captured.out

    def test_review_with_budget(self, tmp_path: Path) -> None:
        config = tmp_path / "advdeb.toml"
        config.write_text("""
[providers.a]
type = "scripted"
model = "test"
key_env = "MISSING"

[providers.b]
type = "scripted"
model = "test"
key_env = "MISSING"
""")
        rc = cmd_review(
            _make_args(
                pr="https://github.com/test/repo/pull/1",
                config=str(config),
                store=str(tmp_path / "test.db"),
                domain="pr_review",
                rounds=2,
                pair="diverse",
                verbose=False,
            )
        )
        assert rc == ExitCode.OK


# ── T9.3 (#42) advdeb report ─────────────────────────────────────────────────


class TestCmdReport:
    def test_report_fails_without_store(self, tmp_path: Path) -> None:
        rc = cmd_report(
            _make_args(
                run_id="run_test",
                store=str(tmp_path / "nonexistent.db"),
                verbose=False,
            )
        )
        assert rc == ExitCode.USAGE

    def test_report_fails_for_unknown_run(self, tmp_path: Path) -> None:
        store_path = tmp_path / "test.db"
        store = SQLiteStore(str(store_path))
        store.initialize()
        rc = cmd_report(
            _make_args(
                run_id="nonexistent",
                store=str(store_path),
                verbose=False,
            )
        )
        assert rc == ExitCode.USAGE


# ── T9.4 (#43) advdeb transcript / list ──────────────────────────────────────


class TestCmdTranscript:
    def test_transcript_fails_without_store(self, tmp_path: Path) -> None:
        rc = cmd_transcript(
            _make_args(
                run_id="run_test",
                store=str(tmp_path / "nonexistent.db"),
                export="jsonl",
                redact=False,
            )
        )
        assert rc == ExitCode.USAGE

    def test_transcript_fails_for_unknown_run(self, tmp_path: Path) -> None:
        store_path = tmp_path / "test.db"
        store = SQLiteStore(str(store_path))
        store.initialize()
        rc = cmd_transcript(
            _make_args(
                run_id="nonexistent",
                store=str(store_path),
                export="jsonl",
                redact=False,
            )
        )
        assert rc == ExitCode.USAGE

    def test_transcript_export_jsonl(self, tmp_path: Path) -> None:
        store_path = tmp_path / "test.db"
        store = SQLiteStore(str(store_path))
        store.initialize()
        run_id = store.create_run("art_001")
        event = DebateEvent(round_index=1, side="A", kind="defense")
        store.append_event(run_id, event)

        store_dir = store_path.resolve().parent
        rc = cmd_transcript(
            _make_args(
                run_id=run_id,
                store=str(store_path),
                export="jsonl",
                redact=False,
            )
        )
        assert rc == ExitCode.OK
        out_path = store_dir / f"transcript_{run_id}.jsonl"
        assert out_path.is_file()
        content = out_path.read_text()
        lines = content.strip().split("\n")
        assert len(lines) >= 2
        header = json.loads(lines[0])
        assert header["type"] == "header"
        assert header["run_id"] == run_id
        assert header["event_count"] >= 1
        last = json.loads(lines[-1])
        assert last["type"] == "__completeness__"


class TestCmdList:
    def test_list_fails_without_store(self, tmp_path: Path) -> None:
        rc = cmd_list(_make_args(store=str(tmp_path / "nonexistent.db")))
        assert rc == ExitCode.USAGE

    def test_list_succeeds_with_store(self, tmp_path: Path) -> None:
        store_path = tmp_path / "test.db"
        store = SQLiteStore(str(store_path))
        store.initialize()
        rc = cmd_list(_make_args(store=str(store_path)))
        assert rc == ExitCode.OK


# ── T9.5 (#44) advdeb resume ─────────────────────────────────────────────────


class TestCmdResume:
    def test_resume_fails_without_store(self, tmp_path: Path) -> None:
        rc = cmd_resume(
            _make_args(
                run_id="run_test",
                store=str(tmp_path / "nonexistent.db"),
            )
        )
        assert rc == ExitCode.USAGE

    def test_resume_fails_for_unknown_run(self, tmp_path: Path) -> None:
        store_path = tmp_path / "test.db"
        store = SQLiteStore(str(store_path))
        store.initialize()
        rc = cmd_resume(
            _make_args(
                run_id="nonexistent",
                store=str(store_path),
            )
        )
        assert rc == ExitCode.USAGE

    def test_resume_warns_for_completed_run(self, tmp_path: Path) -> None:
        store_path = tmp_path / "test.db"
        store = SQLiteStore(str(store_path))
        store.initialize()
        run_id = store.create_run("art_001")
        store.mark_complete(run_id)
        rc = cmd_resume(
            _make_args(
                run_id=run_id,
                store=str(store_path),
            )
        )
        assert rc == ExitCode.OK

    def test_resume_active_run(self, tmp_path: Path) -> None:
        store_path = tmp_path / "test.db"
        store = SQLiteStore(str(store_path))
        store.initialize()
        run_id = store.create_run("art_001")
        event = DebateEvent(round_index=1, side="A", kind="defense")
        store.append_event(run_id, event)
        rc = cmd_resume(
            _make_args(
                run_id=run_id,
                store=str(store_path),
            )
        )
        assert rc == ExitCode.OK


# ── Report formatting ────────────────────────────────────────────────────────


class TestFormatReport:
    def test_converged_verdict_banner(self) -> None:
        text = _format_report(
            {
                "kind": "verdict",
                "convergence_score": 1.0,
                "verdict": "All resolved.",
                "flags": {},
                "resolved": [],
                "unresolved": [],
                "strongest_a": [],
                "strongest_b": [],
                "header": {"engine_version": "0.1.0", "stability_notice": "single-run"},
            },
            no_color=True,
        )
        assert "CONVERGED" in text
        assert "1.00" in text

    def test_disputed_banner(self) -> None:
        text = _format_report(
            {
                "kind": "disputed",
                "convergence_score": 0.5,
                "verdict": "Disagreement persists.",
                "flags": {},
                "resolved": [],
                "unresolved": [],
                "strongest_a": [],
                "strongest_b": [],
                "header": {"engine_version": "0.1.0", "stability_notice": "single-run"},
            },
            no_color=True,
        )
        assert "DISPUTED" in text
        assert "0.50" in text

    def test_theater_flag_shown(self) -> None:
        text = _format_report(
            {
                "kind": "verdict",
                "convergence_score": 1.0,
                "verdict": "All resolved.",
                "flags": {"theater": True},
                "resolved": [],
                "unresolved": [],
                "strongest_a": [],
                "strongest_b": [],
                "header": {"engine_version": "0.1.0", "stability_notice": "single-run"},
            },
            no_color=True,
        )
        assert "theater" in text.lower()

    def test_resolved_entries_displayed(self) -> None:
        text = _format_report(
            {
                "kind": "verdict",
                "convergence_score": 1.0,
                "verdict": "All resolved.",
                "flags": {},
                "resolved": [
                    {"claim_id": "cl_001", "conceded_by": "A"},
                ],
                "unresolved": [],
                "strongest_a": [],
                "strongest_b": [],
                "header": {"engine_version": "0.1.0", "stability_notice": "single-run"},
            },
            no_color=True,
        )
        assert "cl_001" in text
        assert "conceded by" in text.lower()

    def test_unresolved_with_would_resolve_if(self) -> None:
        text = _format_report(
            {
                "kind": "disputed",
                "convergence_score": 0.0,
                "verdict": "Disputed.",
                "flags": {},
                "resolved": [],
                "unresolved": [
                    {"claim_ids": ["cl_002"], "would_resolve_if": "Need more data"},
                ],
                "strongest_a": [],
                "strongest_b": [],
                "header": {"engine_version": "0.1.0", "stability_notice": "single-run"},
            },
            no_color=True,
        )
        assert "cl_002" in text
        assert "Need more data" in text

    def test_strongest_arguments_displayed(self) -> None:
        text = _format_report(
            {
                "kind": "verdict",
                "convergence_score": 1.0,
                "verdict": "All resolved.",
                "flags": {},
                "resolved": [],
                "unresolved": [],
                "strongest_a": ["[high] Input validation"],
                "strongest_b": ["[medium] Error handling"],
                "header": {"engine_version": "0.1.0", "stability_notice": "single-run"},
            },
            no_color=True,
        )
        assert "Input validation" in text
        assert "Error handling" in text
        assert "Side A" in text
        assert "Side B" in text


# ── Parser / help ────────────────────────────────────────────────────────────


class TestParser:
    def test_build_parser_creates_subcommands(self) -> None:
        parser = build_parser()
        assert parser.prog == "advdeb"

    def test_help_contains_no_hype_words(self) -> None:
        """Brand voice: no hype words in help text."""
        parser = build_parser()
        help_text = parser.format_help().lower()
        hype_words = [
            "revolutionary",
            "game-changing",
            "best",
            "incredible",
            "amazing",
            "lightning",
            "blazing",
            "ultra-fast",
        ]
        for word in hype_words:
            assert word not in help_text, f"Hype word found: {word!r}"


# ── Exit codes ───────────────────────────────────────────────────────────────


class TestExitCodes:
    def test_exit_code_values(self) -> None:
        assert ExitCode.OK == 0
        assert ExitCode.USAGE == 1
        assert ExitCode.ENGINE_ERROR == 2
        assert ExitCode.BUDGET_EXHAUSTED == 3


# ── Error handling ───────────────────────────────────────────────────────────


class TestErrorHandling:
    def test_init_missing_path_is_handled(self) -> None:
        """No unhandled exceptions from CLI commands."""
        with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as f:
            path = f.name
        Path(path).unlink()
        rc = cmd_init(_make_args(path=path, force=False))
        # cmd_init should create the file when the path doesn't exist
        assert rc == ExitCode.OK
        assert Path(path).is_file()


# ── Main entry point ─────────────────────────────────────────────────────────


class TestMain:
    def test_main_init(self, tmp_path: Path) -> None:
        path = tmp_path / "advdeb.toml"
        rc = _cli_main(["init", "--path", str(path), "--force"])
        assert rc == ExitCode.OK

    def test_main_init_no_force(self, tmp_path: Path) -> None:
        path = tmp_path / "advdeb.toml"
        path.write_text("existing")
        rc = _cli_main(["init", "--path", str(path)])
        assert rc == ExitCode.USAGE

    def test_main_unknown_command(self) -> None:
        rc = _cli_main(["unknown"])
        assert rc == ExitCode.USAGE

    def test_main_list_no_store(self, tmp_path: Path) -> None:
        rc = _cli_main(["list", "--store", str(tmp_path / "nonexistent.db")])
        assert rc == ExitCode.USAGE

    def test_main_review_no_config(self, tmp_path: Path) -> None:
        rc = _cli_main(
            [
                "review",
                "--pr",
                "https://example.com/pr/1",
                "--config",
                str(tmp_path / "nonexistent.toml"),
            ]
        )
        assert rc == ExitCode.USAGE

    def test_main_report(self, tmp_path: Path) -> None:
        rc = _cli_main(["report", "run_test", "--store", str(tmp_path / "nonexistent.db")])
        assert rc == ExitCode.USAGE

    def test_main_transcript(self, tmp_path: Path) -> None:
        rc = _cli_main(["transcript", "run_test", "--store", str(tmp_path / "nonexistent.db")])
        assert rc == ExitCode.USAGE

    def test_main_resume(self, tmp_path: Path) -> None:
        rc = _cli_main(["resume", "run_test", "--store", str(tmp_path / "nonexistent.db")])
        assert rc == ExitCode.USAGE


# ── Flag display in reports ──────────────────────────────────────────────────


class TestFlagDisplay:
    def test_capitulation_cascade_flag(self) -> None:
        text = _format_report(
            {
                "kind": "disputed",
                "convergence_score": 0.0,
                "verdict": "Disputed.",
                "flags": {"capitulation_cascade": True},
                "resolved": [],
                "unresolved": [],
                "strongest_a": [],
                "strongest_b": [],
                "header": {"engine_version": "0.1.0", "stability_notice": "single-run"},
            },
            no_color=True,
        )
        assert "capitulation" in text.lower()

    def test_degraded_rounds_flag(self) -> None:
        text = _format_report(
            {
                "kind": "disputed",
                "convergence_score": 0.0,
                "verdict": "Disputed.",
                "flags": {"degraded_rounds": [1, 2]},
                "resolved": [],
                "unresolved": [],
                "strongest_a": [],
                "strongest_b": [],
                "header": {"engine_version": "0.1.0", "stability_notice": "single-run"},
            },
            no_color=True,
        )
        assert "degraded" in text.lower()
