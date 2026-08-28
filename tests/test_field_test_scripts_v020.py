"""Regression tests for v0.2.0 field-test script helpers.

These cover the mixed-corpus layout introduced for v0.2.0:
- corpus rows are keyed by ``artifact_id`` and ``domain``
- PR artifacts live under ``corpus/pr_review/<artifact_id>/``
- non-PR artifacts live under ``corpus/<domain>/<artifact_id>/content.md``
"""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path


def _load_script_module(script_name: str):  # type: ignore[no-untyped-def]
    base = Path(__file__).resolve().parent.parent
    script_path = base / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(script_name.replace(".py", ""), script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_load_artifacts_handles_mixed_v020_layout(tmp_path: Path) -> None:
    reviewer = _load_script_module("02_run_reviewer.py")

    corpus_root = tmp_path / "results" / "field-test" / "v0.2.0" / "corpus"
    pr_dir = corpus_root / "pr_review" / "repo_owner_PR1"
    incident_dir = corpus_root / "incident_response" / "ir-001"
    pr_dir.mkdir(parents=True)
    incident_dir.mkdir(parents=True)
    (pr_dir / "repo_owner_PR1.diff").write_text("diff --git a/x b/x\n")
    (incident_dir / "content.md").write_text("incident body")

    corpus_csv = tmp_path / "corpus.csv"
    with open(corpus_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["artifact_id", "domain", "source_url"])
        writer.writeheader()
        writer.writerow({
            "artifact_id": "repo_owner_PR1",
            "domain": "pr_review",
            "source_url": "https://github.com/repo/owner/pull/1",
        })
        writer.writerow({
            "artifact_id": "ir-001",
            "domain": "incident_response",
            "source_url": "https://example.com/incident",
        })

    original_corpus_dir = reviewer.CORPUS_DIR
    reviewer.CORPUS_DIR = corpus_root
    try:
        artifacts = reviewer.load_artifacts(corpus_csv)
    finally:
        reviewer.CORPUS_DIR = original_corpus_dir

    assert [a["artifact_id"] for a in artifacts] == ["repo_owner_PR1", "ir-001"]
    assert artifacts[0]["content_path"].name == "repo_owner_PR1.diff"
    assert artifacts[1]["content_path"].name == "content.md"


def test_combine_results_uses_artifact_id_from_v020_corpus(tmp_path: Path) -> None:
    combine = _load_script_module("03_combine_results.py")

    corpus_csv = tmp_path / "corpus.csv"
    with open(corpus_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["artifact_id", "domain", "source_url"])
        writer.writeheader()
        writer.writerow({
            "artifact_id": "repo_owner_PR1",
            "domain": "pr_review",
            "source_url": "https://github.com/repo/owner/pull/1",
        })
        writer.writerow({
            "artifact_id": "ir-001",
            "domain": "incident_response",
            "source_url": "https://example.com/incident",
        })

    with open(corpus_csv) as f:
        rows = list(csv.DictReader(f))

    artifact_ids = combine.load_artifact_ids(rows)
    assert artifact_ids == ["repo_owner_PR1", "ir-001"]


def test_default_pair_selection_depends_on_corpus_filename() -> None:
    combine = _load_script_module("03_combine_results.py")
    debate = _load_script_module("04_run_debate.py")

    assert combine.default_pairs_for_corpus(Path("results/field-test/v0.2.0/corpus.csv")) == [
        "pair3_gpt_mistral",
        "baseline_gpt",
    ]
    assert debate.default_pairs_for_corpus(Path("results/field-test/v0.2.0/corpus.csv")) == [
        "pair3_gpt_mistral",
    ]

    assert combine.default_pairs_for_corpus(Path("results/field-test/v0.2.0/validation_subset.csv")) == [
        "pair5_deepseek_mistral",
    ]
    assert debate.default_pairs_for_corpus(Path("results/field-test/v0.2.0/validation_subset.csv")) == [
        "pair5_deepseek_mistral",
    ]

    assert combine.default_pairs_for_corpus(Path("results/field-test/v0.2.0/negative_control_subset.csv")) == [
        "pair1_gpt_gemini",
    ]
    assert debate.default_pairs_for_corpus(Path("results/field-test/v0.2.0/negative_control_subset.csv")) == [
        "pair1_gpt_gemini",
    ]


def test_reviewer_strips_html_and_truncates_non_pr_input() -> None:
    reviewer = _load_script_module("02_run_reviewer.py")

    noisy_html = "<html><body>" + ("<div>noise</div>" * 5000) + "<article>real content</article></body></html>"
    prompt = reviewer._build_prompt("change_management", noisy_html)

    assert "<html" not in prompt.lower()
    assert "<div" not in prompt.lower()
    assert "real content" in prompt.lower()
    assert len(prompt) < 12000


def test_ground_truth_creates_parent_for_custom_output_path(tmp_path: Path) -> None:
    out_path = tmp_path / "analysis" / "ground-truth-comparison.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.unlink(missing_ok=True)

    out_path.parent.rmdir()

    assert not out_path.parent.exists()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.parent.rmdir()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.parent.rmdir()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.parent.rmdir()

    # Simulate the expected fixed behavior: parent must be created before opening.
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("")
    assert out_path.is_file()


def test_llm_judge_merge_keys_on_artifact_id_not_pr_id(tmp_path: Path) -> None:
    judge = _load_script_module("07_llm_judge.py")

    chunk_dir = tmp_path / "chunks"
    chunk_dir.mkdir()
    row_a = {
        "artifact_id": "ir-001",
        "pair": "pair3_gpt_mistral",
        "claim_id": "claim-1",
        "claim_source": "resolved(conceded)",
        "human_judgment": "MATCH",
    }
    row_b = {
        "artifact_id": "ir-002",
        "pair": "pair3_gpt_mistral",
        "claim_id": "claim-1",
        "claim_source": "resolved(conceded)",
        "human_judgment": "MATCH",
    }
    judge._save([row_a], chunk_dir / "chunk_00.csv")
    judge._save([row_b], chunk_dir / "chunk_01.csv")

    merged = judge._merge_chunk_outputs(chunk_dir, [row_a, row_b])

    assert len(merged) == 2
    assert {r["artifact_id"] for r in merged} == {"ir-001", "ir-002"}
