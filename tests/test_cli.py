from __future__ import annotations

import ast
from pathlib import Path

from typer.testing import CliRunner

from blux_quantum import cli


def _env(tmp_path: Path) -> dict[str, str]:
    return {"BLUXQ_HOME": str(tmp_path)}


def test_version_command(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["version"], env=_env(tmp_path))
    assert result.exit_code == 0
    data = ast.literal_eval(result.stdout.strip())
    assert "bluxq" in data
    assert "telemetry" in data


def test_self_check(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["self-check"], env=_env(tmp_path))
    assert result.exit_code == 0
    payload = ast.literal_eval(result.stdout.strip())
    assert "self-check" in payload


def test_plugins_command(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["plugins"], env=_env(tmp_path))
    assert result.exit_code == 0
    assert "guard" in result.stdout
