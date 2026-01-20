from __future__ import annotations

from blux_quantum.plugins.quantum_framework.loader import discover_plugins


def test_plugin_discovery_executes() -> None:
    plugins = discover_plugins()
    assert isinstance(plugins, list)
