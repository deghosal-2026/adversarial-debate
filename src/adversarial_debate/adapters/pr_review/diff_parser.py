"""Unified git-diff parser → per-file ``ContentBlock`` s (WBS T4.2, PRD §2.8).

Pure-text parse of diff strings (no subprocess). Robust to binary files (both
``GIT binary patch`` base64 bodies and ``Binary files ... differ`` notices),
renames, copies, mode changes, and new/deleted files. The parser never raises
on malformed input ([13-failure-modes FM-10](docs/design/prd/13-failure-modes.md)):
unparseable hunk headers are skipped with a surfaced warning, and hunks whose
declared line counts are never satisfied are warned about while still keeping
every received line as evidence.
"""

import re
from dataclasses import dataclass

from adversarial_debate.ids import deterministic_id
from adversarial_debate.schemas.artifact import ContentBlock

_HUNK_HEADER_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@")
_GIT_HEADER_RE = re.compile(r"^diff --git (.+)$")
_META_PREFIXES = (
    "index ",
    "similarity index ",
    "dissimilarity index ",
    "rename from ",
    "rename to ",
    "copy from ",
    "copy to ",
    "old mode ",
    "new mode ",
    "new file mode ",
    "deleted file mode ",
)
_BINARY_NOTE_PREFIX = "Binary files "
_GIT_BINARY_MARKER = "GIT binary patch"
_SNIPPET_MAX = 60


@dataclass(frozen=True)
class ParsedDiff:
    """Per-file blocks plus every parser warning surfaced along the way."""

    blocks: list[ContentBlock]
    warnings: list[str]


def parse_diff(diff_text: str) -> ParsedDiff:
    """Parse a unified git diff into one [ContentBlock][...] per file section."""
    sections: list[_Section] = []
    warnings: list[str] = []
    current: _Section | None = None
    skipping_bad_hunk = False

    for lineno, line in enumerate(diff_text.splitlines(), start=1):
        if line.startswith("diff --git "):
            current = _Section(line)
            sections.append(current)
            skipping_bad_hunk = False
            continue
        if current is None:
            if line.strip():
                warnings.append(f"line {lineno}: non-diff preamble ignored: {_snippet(line)}")
            continue
        skipping_bad_hunk = _consume_line(current, line, lineno, warnings, skipping_bad_hunk)

    for position, section in enumerate(sections, start=1):
        if section.unfinished_hunk():
            warnings.append(
                f"section {position} ({section.resolve_name()}): "
                "declared hunk counts not satisfied (truncated or corrupt hunk); "
                "received lines were preserved"
            )

    return ParsedDiff(blocks=_blocks_for(sections), warnings=warnings)


class _Section:
    """Mutable accumulator for one ``diff --git`` file section."""

    def __init__(self, header_line: str) -> None:
        self.lines: list[str] = [header_line]
        self.old_path: str | None = None
        self.new_path: str | None = None
        self.header_name: str | None = _name_from_git_header(header_line)
        self.binary_mode = False
        self.hunk_counters: tuple[int, int] | None = None

    def unfinished_hunk(self) -> bool:
        if self.hunk_counters is None:
            return False
        return any(count > 0 for count in self.hunk_counters)

    def resolve_name(self) -> str:
        for path in (self.new_path, self.old_path, self.header_name):
            if path and path != "/dev/null":
                return path
        return "unknown"


def _consume_line(
    section: _Section,
    line: str,
    lineno: int,
    warnings: list[str],
    skipping: bool,
) -> bool:
    """Fold one line into ``section``; returns the new bad-hunk-skipping flag."""
    if section.binary_mode:
        section.lines.append(line)
        return False
    if _consume_metadata_line(section, line):
        return False
    if line.startswith("@@"):
        warnings.append(f"line {lineno}: malformed hunk header skipped: {_snippet(line)}")
        section.hunk_counters = None
        return True
    if skipping and _is_body_line(line):
        return True
    if _is_body_line(line):
        _consume_body_line(section, line, lineno, warnings)
    else:
        section.lines.append(line)
    return skipping


def _consume_metadata_line(section: _Section, line: str) -> bool:
    if line == _GIT_BINARY_MARKER:
        section.lines.append(line)
        section.binary_mode = True
        return True
    if line.startswith(_BINARY_NOTE_PREFIX):
        section.lines.append(line)
        return True
    if section.hunk_counters is None and line.startswith(("--- ", "+++ ")):
        if line.startswith("--- "):
            section.old_path = _clean_path(line[4:])
        else:
            section.new_path = _clean_path(line[4:])
        section.lines.append(line)
        return True
    if line.startswith(_META_PREFIXES):
        section.lines.append(line)
        return True
    if _HUNK_HEADER_RE.match(line):
        section.lines.append(line)
        section.hunk_counters = _counts_for(line)
        return True
    return False


def _consume_body_line(section: _Section, line: str, lineno: int, warnings: list[str]) -> None:
    if section.hunk_counters is None:
        warnings.append(f"line {lineno}: diff body outside any hunk skipped: {_snippet(line)}")
        return
    section.lines.append(line)
    old_left, new_left = section.hunk_counters
    if line.startswith("-"):
        old_left -= 1
    elif line.startswith("+"):
        new_left -= 1
    elif not line.startswith("\\"):
        old_left -= 1
        new_left -= 1
    section.hunk_counters = (max(old_left, 0), max(new_left, 0))


def _counts_for(header_line: str) -> tuple[int, int]:
    payload = header_line.strip("@ ").split(" +")
    old_part = payload[0].lstrip("- ")
    new_part = payload[1].split(" @@")[0] if len(payload) > 1 else "1"
    return (_count_or_one(old_part), _count_or_one(new_part))


def _count_or_one(spec: str) -> int:
    _, _, count = spec.partition(",")
    return int(count) if count else 1


def _blocks_for(sections: list[_Section]) -> list[ContentBlock]:
    blocks: list[ContentBlock] = []
    occurrences: dict[str, int] = {}
    for section in sections:
        name = section.resolve_name()
        occurrence = occurrences.get(name, 0)
        occurrences[name] = occurrence + 1
        blocks.append(
            ContentBlock(
                id=deterministic_id("cb", f"diff|{name}|{occurrence}"),
                kind="diff",
                name=name,
                content="\n".join(section.lines),
                sequence=len(blocks),
            )
        )
    return blocks


def _name_from_git_header(header_line: str) -> str | None:
    match = _GIT_HEADER_RE.match(header_line)
    if match is None:
        return None
    rest = match.group(1)
    _, separator, b_side = rest.rpartition(" b/")
    if not separator:
        return None
    return _clean_path(b_side)


def _clean_path(raw: str) -> str:
    path = raw.strip().strip('"')
    if path.startswith(("a/", "b/")):
        path = path[2:]
    return path


def _is_body_line(line: str) -> bool:
    return line == "" or line[0] in "+- \\"


def _snippet(line: str) -> str:
    return line if len(line) <= _SNIPPET_MAX else f"{line[:_SNIPPET_MAX]}..."
