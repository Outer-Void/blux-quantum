"""Physics checks for BLUX Quantum guardrails."""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
CODE_DIRS = [ROOT / "blux_quantum"]

POLICY_KEYWORDS = {"policy", "policies", "ethic", "ethics", "doctrine"}
TOKEN_KEYWORDS = {"token", "tokens", "jwt", "signature", "sign", "verify", "mint"}
ALLOWED_COMMANDS = {"blux-ca", "blux-guard", "blux-lite"}


def _iter_python_files() -> Iterable[Path]:
    for base in CODE_DIRS:
        if base.is_dir():
            yield from base.rglob("*.py")


def _file_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _scan_keywords(keyword_set: set[str]) -> list[str]:
    violations: list[str] = []
    for path in _iter_python_files():
        text = _file_text(path).lower()
        for keyword in keyword_set:
            pattern = re.compile(rf"\\b{re.escape(keyword)}\\b")
            if pattern.search(text):
                violations.append(f"{path.relative_to(ROOT)}: contains '{keyword}'")
    return violations


def _scan_contract_copying() -> list[str]:
    violations: list[str] = []
    for path in ROOT.rglob("*.schema.json"):
        violations.append(f"{path.relative_to(ROOT)}: schema file present")
    for path in ROOT.rglob("contracts"):
        if path.is_dir():
            violations.append(f"{path.relative_to(ROOT)}: contracts directory present")
    return violations


def _scan_subprocess_usage() -> list[str]:
    violations: list[str] = []
    for path in _iter_python_files():
        tree = ast.parse(_file_text(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
                    if func.value.id == "subprocess" and func.attr in {"run", "Popen", "call"}:
                        if not node.args:
                            violations.append(f"{path.relative_to(ROOT)}:{node.lineno}: subprocess call without args")
                            continue
                        arg = node.args[0]
                        cmd = None
                        if isinstance(arg, ast.List) and arg.elts and isinstance(arg.elts[0], ast.Constant):
                            cmd = arg.elts[0].value
                        elif isinstance(arg, ast.Tuple) and arg.elts and isinstance(arg.elts[0], ast.Constant):
                            cmd = arg.elts[0].value
                        if cmd not in ALLOWED_COMMANDS:
                            violations.append(
                                f"{path.relative_to(ROOT)}:{node.lineno}: subprocess command '{cmd}' not allowed"
                            )
    return violations


def main() -> int:
    failures: list[str] = []

    failures.extend(_scan_keywords(POLICY_KEYWORDS))
    failures.extend(_scan_keywords(TOKEN_KEYWORDS))
    failures.extend(_scan_contract_copying())
    failures.extend(_scan_subprocess_usage())

    if failures:
        print("Physics guardrails violated:")
        for item in failures:
            print(f"- {item}")
        return 1
    print("Physics guardrails ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
