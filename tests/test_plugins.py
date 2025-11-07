from __future__ import annotations

from blux_quantum.plugins.quantum_framework.loader import discover_plugins


def test_example_plugins_discovered() -> None:
    plugins = discover_plugins()
    names = {plugin.name for plugin in plugins}
    assert {"guard", "lite", "doctrine"}.issubset(names)
