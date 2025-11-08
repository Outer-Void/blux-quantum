"""Core scanning utilities for bq-fsp."""
from __future__ import annotations

import hashlib
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .ignore import load_spec, should_skip
from .rules import Rule, load_rules

_TEXT_EXTENSIONS = {
    ".py",
    ".sh",
    ".js",
    ".ts",
    ".go",
    ".rb",
    ".rs",
    ".c",
    ".cpp",
    ".java",
    ".php",
    ".ps1",
    ".yaml",
    ".yml",
    ".toml",
    ".json",
    ".cfg",
    ".ini",
    ".md",
    ".txt",
}


@dataclass(slots=True)
class Finding:
    """Single suspicious pattern match."""

    rule_id: str
    message: str
    severity: str
    file: str
    line: int
    match: str
    hash: str


def _iter_staged_files() -> Iterable[str]:
    try:
        output = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):  # pragma: no cover - git missing
        return []
    for entry in output.decode().splitlines():
        if entry and Path(entry).is_file():
            yield entry


def iter_files(root: str, only_staged: bool = False) -> Iterable[str]:
    """Yield candidate files for scanning."""

    if only_staged:
        yield from _iter_staged_files()
        return

    spec = load_spec(root)
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), root)
            if should_skip(spec, root, rel):
                continue
            if Path(name).suffix.lower() in _TEXT_EXTENSIONS:
                yield rel


def scan(root: str = ".", rules: list[Rule] | None = None, only_staged: bool = False) -> list[Finding]:
    """Scan a repository path and return suspicious findings."""

    base = Path(root)
    rule_set = rules or load_rules()
    findings: list[Finding] = []

    for rel in iter_files(str(base), only_staged=only_staged):
        file_path = base / rel
        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
                for lineno, line in enumerate(handle, start=1):
                    for rule in rule_set:
                        match = rule.pattern.search(line)
                        if not match:
                            continue
                        fingerprint = hashlib.sha1(
                            f"{rel}:{lineno}:{match.group(0)}".encode("utf-8"),
                        ).hexdigest()[:12]
                        findings.append(
                            Finding(
                                rule_id=rule.id,
                                message=rule.message,
                                severity=rule.severity,
                                file=str(rel),
                                line=lineno,
                                match=match.group(0)[:200],
                                hash=fingerprint,
                            )
                        )
        except OSError:  # pragma: no cover - permission/encoding errors
            continue

    return findings


__all__ = ["Finding", "scan", "iter_files"]
