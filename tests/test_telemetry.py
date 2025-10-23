from __future__ import annotations

from pathlib import Path

from blux_quantum.telemetry import record_event, telemetry_status


def test_record_event_respects_env_off(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("BLUXQ_HOME", str(tmp_path))
    monkeypatch.setenv("BLUXQ_TELEMETRY", "off")
    assert record_event("test.off") is False


def test_record_event_writes_files(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("BLUXQ_HOME", str(tmp_path))
    monkeypatch.delenv("BLUXQ_TELEMETRY", raising=False)
    assert record_event("test.on", {"value": 1}) is True
    status = telemetry_status()
    assert Path(status["log_path"]).exists()
    assert Path(status["sqlite_path"]).exists()
