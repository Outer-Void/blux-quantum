"""Ignore rules for the bq-fsp scanner."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

try:  # pragma: no cover - optional dependency branch
    from pathspec import PathSpec
except ImportError:  # pragma: no cover - fallback implementation
    PathSpec = None  # type: ignore[assignment]

DEFAULT_IGNORES = (
    ".git/",
    ".venv/",
    "venv/",
    "node_modules/",
    "dist/",
    "build/",
    "__pycache__/",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.pdf",
    "*.mp4",
    "*.zip",
    "*.tar",
    "*.gz",
    "*.bz2",
)


@dataclass
class _FallbackSpec:
    patterns: tuple[str, ...]

    def match_file(self, filename: str) -> bool:  # pragma: no cover - simple fallback
        for pattern in self.patterns:
            if pattern.endswith("/") and filename.startswith(pattern.rstrip("/")):
                return True
            if pattern.startswith("*") and filename.endswith(pattern.lstrip("*")):
                return True
        return False


def _build_spec(patterns: Iterable[str]):
    if PathSpec is None:
        return _FallbackSpec(tuple(patterns))
    return PathSpec.from_lines("gitwildmatch", patterns)


def load_spec(repo_root: str):
    """Load ignore specification merging defaults with repository .gitignore."""

    patterns = list(DEFAULT_IGNORES)
    gitignore_path = f"{repo_root}/.gitignore"
    try:
        with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    except FileNotFoundError:
        pass
    return _build_spec(patterns)


def should_skip(spec, root: str, relpath: str) -> bool:
    """Check if a path should be skipped according to the ignore spec."""

    if hasattr(spec, "match_file"):
        return bool(spec.match_file(relpath))
    return False


__all__ = ["DEFAULT_IGNORES", "load_spec", "should_skip"]
