"""Git unified-diff parser goldens (WBS T4.2): binary, renames, malformed hunks."""

import pytest

from adversarial_debate.adapters.pr_review.diff_parser import ParsedDiff, parse_diff

SIMPLE = (
    """diff --git a/src/app.py b/src/app.py
index 1a2b3c4..5d6e7f8 100644
--- a/src/app.py
+++ b/src/app.py
@@ -1,4 +1,5 @@
 import os
+import sys
"""
    " \n"
    " def main():\n"
    "-    pass\n"
    '+    print("hi")\n'
)


def names(parsed: ParsedDiff) -> list[str]:
    return [block.name for block in parsed.blocks]


def test_single_file_block_content_preserved_verbatim() -> None:
    parsed = parse_diff(SIMPLE)
    assert len(parsed.blocks) == 1
    block = parsed.blocks[0]
    assert block.kind == "diff"
    assert block.name == "src/app.py"
    assert block.content == SIMPLE.rstrip("\n")


def test_hunk_markers_preserved() -> None:
    content = parse_diff(SIMPLE).blocks[0].content
    assert "\n+import sys\n" in content
    assert "\n-    pass\n" in content
    assert "\n import os\n" in content
    assert "@@ -1,4 +1,5 @@" in content


def test_multi_file_blocks_in_order() -> None:
    multi = SIMPLE + (
        "diff --git a/docs/readme.md b/docs/readme.md\n"
        "--- a/docs/readme.md\n"
        "+++ b/docs/readme.md\n"
        "@@ -1 +1 @@\n"
        "-hello\n"
        "+world\n"
    )
    assert names(parse_diff(multi)) == ["src/app.py", "docs/readme.md"]


def test_new_file_uses_added_path() -> None:
    new_file = (
        "diff --git a/brand/new.py b/brand/new.py\n"
        "new file mode 100644\n"
        "index 0000000..3f2a1b9\n"
        "--- /dev/null\n"
        "+++ b/brand/new.py\n"
        "@@ -0,0 +1,2 @@\n"
        "+VALUE = 1\n"
        "+OTHER = 2\n"
    )
    assert names(parse_diff(new_file)) == ["brand/new.py"]


def test_deleted_file_uses_removed_path() -> None:
    deleted = (
        "diff --git a/legacy/old.py b/legacy/old.py\n"
        "deleted file mode 100644\n"
        "index 3f2a1b9..0000000\n"
        "--- a/legacy/old.py\n"
        "+++ /dev/null\n"
        "@@ -1,2 +0,0 @@\n"
        "-VALUE = 1\n"
        "-OTHER = 2\n"
    )
    assert names(parse_diff(deleted)) == ["legacy/old.py"]


def test_rename_keeps_new_name_and_metadata() -> None:
    rename = (
        "diff --git a/docs/guide.txt b/docs/manual.txt\n"
        "similarity index 92%\n"
        "rename from docs/guide.txt\n"
        "rename to docs/manual.txt\n"
        "--- a/docs/guide.txt\n"
        "+++ b/docs/manual.txt\n"
        "@@ -1 +1 @@\n"
        "-old title\n"
        "+new title\n"
    )
    parsed = parse_diff(rename)
    assert names(parsed) == ["docs/manual.txt"]
    assert "rename from docs/guide.txt" in parsed.blocks[0].content


def test_mode_change_only_section_still_emits_block() -> None:
    mode_change = "diff --git a/scripts/run.sh b/scripts/run.sh\nold mode 100644\nnew mode 100755\n"
    parsed = parse_diff(mode_change)
    assert names(parsed) == ["scripts/run.sh"]
    assert "new mode 100755" in parsed.blocks[0].content


def test_binary_files_notice_form() -> None:
    binary = (
        "diff --git a/assets/logo.png b/assets/logo.png\n"
        "index 9a03e21..7c11d40 100644\n"
        "Binary files a/assets/logo.png and b/assets/logo.png differ\n"
    )
    parsed = parse_diff(binary)
    assert names(parsed) == ["assets/logo.png"]
    assert "Binary files a/assets/logo.png and b/assets/logo.png differ" in (
        parsed.blocks[0].content
    )


def test_git_binary_patch_base64_preserved() -> None:
    blob = (
        "diff --git a/assets/banner.png b/assets/banner.png\n"
        "new file mode 100644\n"
        "index 0000000..c41d9e2\n"
        "GIT binary patch\n"
        "literal 128\n"
        "zcmeAS@N?(olHy`uVBq!ia0vp^0zkxY!3HGtU4qL<^T-Ka92hW$[=?g\n"
        "zrPe4Ml^%0b`&QvX#q7VJzz?|Yzx{-Oz5D  #%w~{=Zc\n"
        "\n"
        "literal 0\n"
        "HcmV?d00001\n"
        "\n"
    )
    parsed = parse_diff(blob)
    assert names(parsed) == ["assets/banner.png"]
    assert "zcmeAS@N?(olHy`uVBq!ia0vp^0zkxY" in parsed.blocks[0].content
    assert parsed.warnings == []


def test_indented_binary_notice_preserved() -> None:
    """Whitespace-prefixed 'Binary files ... differ' lines are preserved."""
    binary = (
        "diff --git a/assets/logo.png b/assets/logo.png\n"
        "index 9a03e21..7c11d40 100644\n"
        " Binary files a/assets/logo.png and b/assets/logo.png differ\n"
    )
    parsed = parse_diff(binary)
    assert names(parsed) == ["assets/logo.png"]
    content = parsed.blocks[0].content
    assert "Binary files a/assets/logo.png" in content
    # No "diff body outside any hunk skipped" warning should be emitted
    binary_warnings = [w for w in parsed.warnings if "Binary" in w or "outside any hunk" in w]
    assert not binary_warnings


MALFORMED = (
    "diff --git a/ok.py b/ok.py\n"
    "--- a/ok.py\n"
    "+++ b/ok.py\n"
    "@@ -1,2 +1,2 @@\n"
    " context line\n"
    "-removed\n"
    "+added\n"
    "@@ definitely not a hunk header @@\n"
    "-orphan deletion\n"
    "+orphan addition\n"
    "@@ -10,1 +10,2 @@\n"
    " later context\n"
    "+later added\n"
)


def test_malformed_hunk_header_skipped_with_warning() -> None:
    parsed = parse_diff(MALFORMED)
    assert len(parsed.warnings) == 1
    assert "malformed hunk header" in parsed.warnings[0]
    assert "@@ definitely not a hunk header @@" not in parsed.blocks[0].content
    assert "orphan deletion" not in parsed.blocks[0].content


def test_valid_hunks_around_malformed_one_survive() -> None:
    content = parse_diff(MALFORMED).blocks[0].content
    assert "-removed" in content
    assert "+added" in content
    assert "+later added" in content


TRUNCATED = (
    "diff --git a/truncated.py b/truncated.py\n"
    "--- a/truncated.py\n"
    "+++ b/truncated.py\n"
    "@@ -1,10 +1,10 @@\n"
    "-only one of ten declared lines\n"
)


def test_truncated_hunk_warns_but_preserves_received_lines() -> None:
    parsed = parse_diff(TRUNCATED)
    assert len(parsed.warnings) == 1
    assert "declared hunk counts" in parsed.warnings[0]
    assert "-only one of ten declared lines" in parsed.blocks[0].content


def test_crlf_input_handled() -> None:
    parsed = parse_diff(SIMPLE.replace("\n", "\r\n"))
    assert names(parsed) == ["src/app.py"]
    assert parsed.blocks[0].content == SIMPLE.rstrip("\n")


@pytest.mark.parametrize("junk", ["", "   ", "\n\n"])
def test_empty_or_blank_diff_has_no_blocks(junk: str) -> None:
    parsed = parse_diff(junk)
    assert parsed.blocks == []
    assert parsed.warnings == []


def test_preamble_noise_before_first_header_warns_and_is_excluded() -> None:
    noisy = f"warning: something odd\n{'x' * 80}\n{SIMPLE}"
    parsed = parse_diff(noisy)
    assert len(parsed.warnings) == 2
    assert "non-diff preamble" in parsed.warnings[0]
    assert names(parsed) == ["src/app.py"]
    assert "warning: something odd" not in parsed.blocks[0].content


def test_ids_deterministic_across_parses() -> None:
    first = [b.id for b in parse_diff(SIMPLE).blocks]
    second = [b.id for b in parse_diff(SIMPLE).blocks]
    assert first == second
    assert all(bid.startswith("cb_") for bid in first)


def test_duplicate_paths_get_distinct_ids() -> None:
    twice = SIMPLE + SIMPLE
    blocks = parse_diff(twice).blocks
    assert len(blocks) == 2
    assert blocks[0].id != blocks[1].id


def test_header_only_fallback_name_when_paths_missing() -> None:
    bare = "diff --git a/weird/no-paths-here.txt b/weird/no-paths-here.txt\nsome junk\n"
    assert names(parse_diff(bare)) == ["weird/no-paths-here.txt"]


def test_unparseable_header_falls_back_to_unknown() -> None:
    weird = "diff --git total-garbage-no-slashes\njunk line\n"
    assert names(parse_diff(weird)) == ["unknown"]


def test_body_line_before_any_hunk_warns_and_skips() -> None:
    body = "diff --git a/x.py b/x.py\n--- a/x.py\n+++ b/x.py\n+body without hunk\n"
    parsed = parse_diff(body)
    assert len(parsed.warnings) == 1
    assert "outside any hunk" in parsed.warnings[0]
    assert "+body without hunk" not in parsed.blocks[0].content


def test_unrecognized_header_line_falls_back_to_unknown() -> None:
    body = "diff --git \n---\n+++\n@@ -1,1 +1,1 @@\n-no\n+yes\n"
    parsed = parse_diff(body)
    assert len(parsed.warnings) == 2
    assert parsed.blocks[0].name == "unknown"


def test_sequences_are_dense_from_zero() -> None:
    two_files = SIMPLE.replace("src/app.py", "a.py") + SIMPLE.replace("src/app.py", "b.py")
    blocks = parse_diff(two_files).blocks
    assert [b.sequence for b in blocks] == [0, 1]


def test_no_trailing_newline_last_line_kept() -> None:
    no_newline = SIMPLE.rstrip("\n")
    parsed = parse_diff(no_newline)
    assert parsed.blocks[0].content.endswith('+    print("hi")')


def test_no_newline_marker_line_preserved() -> None:
    marker = (
        "diff --git a/tail.py b/tail.py\n"
        "--- a/tail.py\n"
        "+++ b/tail.py\n"
        "@@ -1 +1 @@\n"
        "-old end\n"
        "\\ No newline at end of file\n"
        "+new end\n"
        "\\ No newline at end of file\n"
    )
    content = parse_diff(marker).blocks[0].content
    assert "\\ No newline at end of file" in content
    assert parsed_warnings(marker) == []


def parsed_warnings(text: str) -> list[str]:
    return parse_diff(text).warnings
