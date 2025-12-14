"""Append-only JSONL audit logging for bluxq commands."""
from __future__ import annotations

import getpass
import hashlib
import json
import os
import socket
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def audit_log_path() -> Path:
    """Return the audit log path (configurable via BLUXQ_HOME/XDG_CONFIG_HOME)."""

    base_home = os.environ.get("BLUXQ_HOME") or os.environ.get("XDG_CONFIG_HOME")
    if base_home:
        return Path(base_home) / "blux-quantum" / "logs" / "audit.jsonl"
    return Path.home() / ".config" / "blux-quantum" / "logs" / "audit.jsonl"


def _last_line_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        last_line = path.read_text(encoding="utf-8").splitlines()[-1]
    except (OSError, IndexError):
        return None
    if not last_line:
        return None
    return hashlib.sha256(last_line.encode("utf-8")).hexdigest()


def append_event(event: Dict[str, Any]) -> Path:
    """Append an audit event to the JSONL log and return the path."""

    path = audit_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    event.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    event.setdefault("user", getpass.getuser())
    event.setdefault("host", socket.gethostname())
    event.setdefault("cwd", str(Path.cwd()))
    event.setdefault("trace_id", uuid.uuid4().hex)
    event.setdefault("prev_audit_sha256", _last_line_hash(path))
    with path.open("a", encoding="utf-8") as handle:
        json.dump(event, handle, ensure_ascii=False)
        handle.write("\n")
    return path


def audit_command(cmd: str, args: Dict[str, Any] | None, outcome: str, duration_ms: int, trace_id: str) -> None:
    """Helper to write a structured audit event for a CLI command."""

    payload: Dict[str, Any] = {
        "cmd": cmd,
        "args": args or {},
        "outcome": outcome,
        "duration_ms": duration_ms,
        "trace_id": trace_id,
    }
    append_event(payload)


__all__ = ["append_event", "audit_command", "audit_log_path"]
