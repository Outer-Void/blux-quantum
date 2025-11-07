"""Standalone shim for the BLUX Quantum CLI with optional security plugin."""
from __future__ import annotations

import os
import pathlib
from typing import Any

from blux_quantum.cli import app as _app


def _mount_optional_fsp(app: Any) -> None:
    """Mount the optional bq-fsp plugin if it is importable."""
    try:
        import bq_fsp.cli as fsp_cli
    except ImportError:  # pragma: no cover - optional dependency
        return
    register = getattr(fsp_cli, "register", None)
    if callable(register):
        register(app)


def default_fsp_log() -> str:
    """Resolve the default JSONL log path for bq-fsp output."""
    override = os.environ.get("FSP_LOG")
    if override:
        return override
    path = pathlib.Path.home() / ".config" / "blux-lite-gold" / "logs" / "fsp.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


app = _app

# Mount optional security scanner as `bq fsp` if installed.
_mount_optional_fsp(app)


__all__ = ["app", "default_fsp_log"]
