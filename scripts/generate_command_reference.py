"""Generate the README command reference from the real Typer surface."""
from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List, Tuple

from typer.testing import CliRunner

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from blux_quantum.cli import app

MARKER_START = "<!-- BEGIN AUTO-GENERATED COMMANDS -->"
MARKER_END = "<!-- END AUTO-GENERATED COMMANDS -->"


def _run_help(args: Iterable[str], home: Path) -> str:
    env = os.environ.copy()
    env.setdefault("BLUXQ_HOME", str(home))
    env.setdefault("BLUXQ_BANNER", "off")
    result = CliRunner().invoke(app, [*args, "--help"], env=env, prog_name="blux")
    return result.stdout.strip()


def _extract_usage(help_text: str) -> str | None:
    for line in help_text.splitlines():
        if line.strip().startswith("Usage:"):
            usage = line.strip().replace("Usage:", "").strip()
            return usage.replace("python -m blux_quantum.cli", "blux")
    return None


def _extract_commands(help_text: str) -> List[Tuple[str, str]]:
    commands: List[Tuple[str, str]] = []
    capture = False
    for line in help_text.splitlines():
        if "Commands" in line:
            capture = True
            continue
        if not capture:
            continue
        if line.strip().startswith("╰"):
            break

        clean = line.strip().strip("│").strip()
        if not clean:
            continue
        match = re.match(r"([\w-]+)\s*(.*)", clean)
        if match:
            name, desc = match.groups()
            if name:
                commands.append((name.strip(), desc.strip()))
    return commands


def _render_reference(home: Path) -> str:
    root_help = _run_help([], home)
    top_level_commands = _extract_commands(root_help)

    lines: List[str] = [MARKER_START, "", "_Generated via `python scripts/generate_command_reference.py`._", ""]

    for name, desc in top_level_commands:
        description = desc or "No description provided."
        help_text = _run_help([name], home)
        usage = _extract_usage(help_text) or f"blux {name}"
        subcommands = _extract_commands(help_text)
        lines.append(f"- `blux {name}` — {description}")
        lines.append(f"  - Example: `{usage}`")
        if subcommands:
            lines.append("  - Subcommands:")
            for sub_name, sub_desc in subcommands:
                sub_description = sub_desc or "No description provided."
                sub_help = _run_help([name, sub_name], home)
                sub_usage = _extract_usage(sub_help) or f"blux {name} {sub_name}"
                lines.append(f"    - `blux {name} {sub_name}` — {sub_description}")
                lines.append(f"      - Example: `{sub_usage}`")
        lines.append("")

    lines.append(MARKER_END)
    return "\n".join(lines) + "\n"


def _rewrite_readme(readme_path: Path, block: str) -> None:
    content = readme_path.read_text(encoding="utf-8")
    if MARKER_START not in content or MARKER_END not in content:
        raise SystemExit("README is missing the auto-generated command markers")
    start = content.index(MARKER_START)
    end = content.index(MARKER_END) + len(MARKER_END)
    new_content = content[:start] + block + content[end:]
    readme_path.write_text(new_content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate README command reference")
    parser.add_argument("--readme", type=Path, default=Path(__file__).resolve().parent.parent / "README.md")
    parser.add_argument("--stdout", action="store_true", help="Print the block instead of writing")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        block = _render_reference(Path(tmpdir))

    if args.stdout:
        sys.stdout.write(block)
        return

    _rewrite_readme(args.readme, block)

if __name__ == "__main__":
    main()
