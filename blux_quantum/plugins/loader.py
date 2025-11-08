"""Compatibility wrapper for the relocated plugin loader."""
from __future__ import annotations

import warnings

from .quantum_framework.loader import PluginInfo, discover_plugins, mount_plugins

warnings.warn(
    "blux_quantum.plugins.loader is deprecated; use blux_quantum.plugins.quantum_framework.loader",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["PluginInfo", "discover_plugins", "mount_plugins"]
