"""Update README file tree section."""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from gen_filetree import build_tree

MARKER_BEGIN = "<!-- FILETREE:BEGIN -->"
MARKER_END = "<!-- FILETREE:END -->"


def update_readme(readme_path: Path) -> None:
    content = readme_path.read_text(encoding="utf-8")
    if MARKER_BEGIN not in content or MARKER_END not in content:
        raise SystemExit("Markers not found in README")

    tree = build_tree(readme_path.parent)
    snippet = (
        f"{MARKER_BEGIN}\n"
        "<!-- generated; do not edit manually -->\n"
        "<details><summary><strong>Repository File Tree</strong> (click to expand)</summary>\n\n"
        "```text\n"
        f"{tree}\n"
        "```\n\n"
        "</details>\n"
        f"{MARKER_END}"
    )

    start = content.index(MARKER_BEGIN)
    end = content.index(MARKER_END) + len(MARKER_END)
    updated = content[:start] + snippet + content[end:]
    readme_path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    update_readme(Path("README.md"))
