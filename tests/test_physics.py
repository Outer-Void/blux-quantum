from __future__ import annotations

import ast
import json
from pathlib import Path

from typer.testing import CliRunner

from blux_quantum import cli, dispatch
from blux_quantum.envelope import PHASE0_SCHEMA_VERSION, create_envelope

DECISION_ENUMS = {"ALLOW", "WARN", "BLOCK"}


def _env(tmp_path: Path) -> dict[str, str]:
    return {"BLUXQ_HOME": str(tmp_path)}


def _collect_python_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*.py") if path.is_file()]


def _decision_enums_used_as_logic(py_file: Path) -> list[tuple[int, str]]:
    violations: list[tuple[int, str]] = []
    tree = ast.parse(py_file.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.While, ast.Match)):
            for child in ast.walk(node):
                if isinstance(child, ast.Constant) and isinstance(child.value, str):
                    if child.value in DECISION_ENUMS:
                        violations.append((child.lineno, child.value))
        if isinstance(node, ast.Compare):
            constants = [
                child.value
                for child in ast.walk(node)
                if isinstance(child, ast.Constant) and isinstance(child.value, str)
            ]
            for value in constants:
                if value in DECISION_ENUMS:
                    violations.append((node.lineno, value))
    return violations


def test_phase0_envelope_contract() -> None:
    envelope = create_envelope("guard_receipt", {"capability_ref": "capability:blux.test"}, source="blux.guard")
    assert envelope["schema_version"] == PHASE0_SCHEMA_VERSION
    assert envelope["type"] == "guard_receipt"
    assert envelope["source"] == "blux.guard"
    assert isinstance(envelope["trace_id"], str)
    assert isinstance(envelope["payload"], dict)


def test_dispatch_preview_outputs_trace_id(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(dispatch.app, ["status"], env=_env(tmp_path))
    assert result.exit_code == 0
    preview = json.loads(result.stdout.splitlines()[0])
    trace_id = preview["execution_preview"]["trace_id"]
    assert isinstance(trace_id, str)
    assert trace_id


def test_run_outputs_trace_id(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["run", "task.txt"], env=_env(tmp_path))
    assert result.exit_code == 0
    envelope = json.loads(result.stdout.splitlines()[0])
    assert isinstance(envelope["trace_id"], str)
    assert envelope["trace_id"]


def test_no_decision_enum_logic_in_core() -> None:
    project_root = Path(__file__).resolve().parents[1]
    violations: list[str] = []
    for py_file in _collect_python_files(project_root / "blux_quantum"):
        for line, value in _decision_enums_used_as_logic(py_file):
            violations.append(f"{py_file.relative_to(project_root)}:{line}:{value}")
    assert not violations, "Decision enums used as logic:\n" + "\n".join(violations)
