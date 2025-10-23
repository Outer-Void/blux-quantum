"""Best-effort telemetry writer for BLUX Quantum."""
from __future__ import annotations

import json
import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from prometheus_client import CollectorRegistry, Counter

from .config import BLUXQ_HOME_ENV, load_config

TELEMETRY_ENV = "BLUXQ_TELEMETRY"
TELEMETRY_WARN_ENV = "BLUXQ_TELEMETRY_WARN"
_LOG_DIR_NAME = "logs"
_JSONL_NAME = "audit.jsonl"
_SQLITE_NAME = "telemetry.db"

_registry = CollectorRegistry()
_events_counter = Counter(
    "bluxq_events_total",
    "Number of telemetry events recorded by BLUX Quantum.",
    ["event"],
    registry=_registry,
)
_warned_lock = threading.Lock()
_warned = False


def _telemetry_disabled() -> bool:
    return os.environ.get(TELEMETRY_ENV, "on").lower() in {"0", "false", "off"}


def _should_warn() -> bool:
    global _warned
    mode = os.environ.get(TELEMETRY_WARN_ENV, "never").lower()
    if mode not in {"once", "always"}:
        return False
    if mode == "always":
        return True
    with _warned_lock:
        if not _warned:
            _warned = True
            return True
    return False


def _log_dir() -> Path:
    config_dir = Path(os.environ.get(BLUXQ_HOME_ENV) or Path.home() / ".config" / "blux-quantum")
    return config_dir / _LOG_DIR_NAME


def telemetry_status() -> Dict[str, Any]:
    log_dir = _log_dir()
    jsonl_path = log_dir / _JSONL_NAME
    sqlite_path = log_dir / _SQLITE_NAME
    return {
        "enabled": not _telemetry_disabled(),
        "log_path": str(jsonl_path),
        "sqlite_path": str(sqlite_path),
    }


def _ensure_log_dir(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError:
        if _should_warn():
            print("[bluxq] telemetry log directory unavailable; continuing without persistence")


def _write_jsonl(path: Path, payload: Dict[str, Any]) -> None:
    try:
        with path.open("a", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False)
            handle.write("\n")
    except OSError:
        if _should_warn():
            print("[bluxq] telemetry JSONL write failed; continuing")


def _write_sqlite(path: Path, payload: Dict[str, Any]) -> None:
    try:
        conn = sqlite3.connect(path)
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS events (timestamp TEXT, name TEXT, payload TEXT)"
            )
            conn.execute(
                "INSERT INTO events (timestamp, name, payload) VALUES (?, ?, ?)",
                (payload["timestamp"], payload["event"], json.dumps(payload.get("payload", {}))),
            )
            conn.commit()
        finally:
            conn.close()
    except sqlite3.Error:
        if _should_warn():
            print("[bluxq] telemetry SQLite write failed; continuing")


def record_event(event: str, payload: Dict[str, Any] | None = None) -> bool:
    if _telemetry_disabled():
        return False

    timestamp = datetime.now(timezone.utc).isoformat()
    entry = {
        "timestamp": timestamp,
        "event": event,
        "payload": payload or {},
        "config": load_config(),
    }

    log_dir = _log_dir()
    _ensure_log_dir(log_dir)

    jsonl_path = log_dir / _JSONL_NAME
    sqlite_path = log_dir / _SQLITE_NAME

    _write_jsonl(jsonl_path, entry)
    _write_sqlite(sqlite_path, entry)

    try:
        _events_counter.labels(event=event).inc()
    except ValueError:
        _events_counter.labels(event="unknown").inc()

    return True


__all__ = ["record_event", "telemetry_status", "_registry"]
