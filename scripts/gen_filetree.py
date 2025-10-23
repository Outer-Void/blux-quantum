"""Generate a repository file tree."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

IGNORED = {".git", "__pycache__", "dist", "build", ".mypy_cache", ".pytest_cache", "site"}


def iter_directory(path: Path, prefix: str = "") -> Iterable[str]:
    entries = sorted(p for p in path.iterdir() if p.name not in IGNORED)
    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        yield f"{prefix}{connector}{entry.name}"
        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            yield from iter_directory(entry, prefix + extension)


def build_tree(root: Path | None = None) -> str:
    root = (root or Path.cwd()).resolve()
    lines = [root.name or str(root)]
    lines.extend(iter_directory(root))
    return "\n".join(lines)


def main() -> None:
    print(build_tree())


if __name__ == "__main__":
    main()
