"""Stability mode helpers for BLUX Quantum."""
from __future__ import annotations

import threading
from typing import Dict

from .telemetry import record_event

_lock = threading.Lock()
_enabled = False


def enable_stability(metadata: Dict[str, str] | None = None) -> bool:
    """Enable stability mode."""
    global _enabled
    with _lock:
        _enabled = True
    record_event("stability.enable", metadata or {})
    return _enabled


def disable_stability(metadata: Dict[str, str] | None = None) -> bool:
    """Disable stability mode."""
    global _enabled
    with _lock:
        _enabled = False
    record_event("stability.disable", metadata or {})
    return _enabled


def stability_status() -> Dict[str, bool]:
    with _lock:
        status = _enabled
    return {"enabled": status}


__all__ = ["enable_stability", "disable_stability", "stability_status"]
