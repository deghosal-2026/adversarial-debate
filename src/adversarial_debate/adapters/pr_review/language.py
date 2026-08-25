"""File-extension → language heuristics for PR artifacts (WBS T4.3).

Feeds ``DetectedLanguage``/``classification_tag`` on the artifact. These are
deliberately shallow filename heuristics — never claims about content semantics
([13-failure-modes FM-10](docs/design/prd/13-failure-modes.md): no invented
metadata).
"""

from collections import Counter
from collections.abc import Iterable

_EXTENSION_LANGUAGES = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".java": "java",
    ".kt": "kotlin",
    ".swift": "swift",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".php": "php",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".sql": "sql",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".md": "markdown",
    ".rst": "rst",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".xml": "xml",
}

_MAJORITY_SHARE = 0.5
_PATH_PARTS = 2


def guess_language(path: str) -> str | None:
    """Language name for a file path, or ``None`` for unknown extensions."""
    suffix = path.rsplit(".", 1)
    if len(suffix) != _PATH_PARTS or not suffix[1]:
        return None
    return _EXTENSION_LANGUAGES.get(f".{suffix[1].lower()}")


def summarize_languages(paths: Iterable[str]) -> list[str]:
    """Sorted unique languages implied by the given paths."""
    return sorted({lang for lang in (guess_language(p) for p in paths) if lang})


def classification_tag(paths: Iterable[str]) -> str:
    """Dominant-language tag (``python-diff``), else ``mixed-diff``/``generic-diff``.

    A language wins on a strict majority of *all* files; otherwise any known
    languages yield ``mixed-diff``, and none yield ``generic-diff``.
    """
    names = list(paths)
    counts = Counter(lang for lang in (guess_language(p) for p in names) if lang)
    if not counts:
        return "generic-diff"
    top_lang, top_count = counts.most_common(1)[0]
    if top_count / len(names) > _MAJORITY_SHARE:
        return f"{top_lang}-diff"
    return "mixed-diff"
