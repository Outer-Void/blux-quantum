from __future__ import annotations

import json
import json
from pathlib import Path

from typer.testing import CliRunner

from blux_quantum import cli
from blux_quantum.audit import audit_log_path


def _env(tmp_path: Path) -> dict[str, str]:
    return {"BLUXQ_HOME": str(tmp_path)}


def test_command_tree(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["--help"], env=_env(tmp_path))
    assert result.exit_code == 0
    assert "system" in result.stdout
    assert "key" in result.stdout
    assert "help" in result.stdout


def test_audit_written(tmp_path: Path, monkeypatch: object) -> None:
    runner = CliRunner()
    monkeypatch.setenv("BLUXQ_HOME", str(tmp_path))
    result = runner.invoke(cli.app, ["version"], env=_env(tmp_path))
    assert result.exit_code == 0
    log = audit_log_path()
    assert log.exists()
    event = json.loads(log.read_text(encoding="utf-8").splitlines()[-1])
    assert event["cmd"] == "version"


def test_god_fallback(tmp_path: Path, monkeypatch: object) -> None:
    runner = CliRunner()
    monkeypatch.setenv("PATH", "")
    result = runner.invoke(cli.app, ["help", "stats"], env=_env(tmp_path))
    assert "GOD not installed" in result.stdout


def test_gating_denies_without_key(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["system", "up"], env=_env(tmp_path))
    assert result.exit_code != 0
    assert "Reg key required" in result.stdout


def test_system_doctor(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["system", "doctor", "--json"], env=_env(tmp_path))
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert "checks" in payload
