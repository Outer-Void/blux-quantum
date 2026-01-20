"""Plugin discovery for the Quantum framework namespace."""
from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import List

import typer
from importlib import metadata
from rich import print

DEFAULT_PLUGINS = {
    "doctrine": "blux_quantum.plugins.examples.doctrine_plugin:get_app",
}


@dataclass
class PluginInfo:
    name: str
    app_factory: str
    loaded: bool
    error: str | None = None


def _iter_entry_points() -> List[metadata.EntryPoint]:
    entries: List[metadata.EntryPoint] = []
    try:
        entry_points = metadata.entry_points()
    except Exception:  # pragma: no cover - defensive fallback
        entry_points = ()
    if hasattr(entry_points, "select"):
        entries.extend(list(entry_points.select(group="blux.plugins")))
    else:
        entries.extend(list(entry_points.get("blux.plugins", [])))  # type: ignore[attr-defined]

    if not entries:
        for name, value in DEFAULT_PLUGINS.items():
            entries.append(metadata.EntryPoint(name=name, value=value, group="blux.plugins"))
    return entries


def _resolve_plugin(entry: metadata.EntryPoint) -> typer.Typer:
    module, _, attr = entry.value.partition(":")
    module_obj = importlib.import_module(module)
    plugin_obj = getattr(module_obj, attr) if attr else module_obj
    plugin_app = plugin_obj() if callable(plugin_obj) else plugin_obj
    if not isinstance(plugin_app, typer.Typer):
        raise TypeError("Plugin app must be a Typer application")
    return plugin_app


def discover_plugins() -> List[PluginInfo]:
    plugins: List[PluginInfo] = []
    for entry in _iter_entry_points():
        target = entry.value
        try:
            _resolve_plugin(entry)
            plugins.append(PluginInfo(name=entry.name, app_factory=target, loaded=True))
        except Exception as exc:  # pragma: no cover - defensive
            print(f"[bluxq] plugin '{entry.name}' failed to load: {exc}")
            plugins.append(
                PluginInfo(name=entry.name, app_factory=target, loaded=False, error=str(exc))
            )
    return plugins


def mount_plugins(app: typer.Typer) -> List[PluginInfo]:
    results: List[PluginInfo] = []
    for entry in _iter_entry_points():
        target = entry.value
        try:
            plugin_app = _resolve_plugin(entry)
            app.add_typer(plugin_app, name=entry.name)
            results.append(PluginInfo(name=entry.name, app_factory=target, loaded=True))
        except Exception as exc:  # pragma: no cover - defensive
            print(f"[bluxq] plugin '{entry.name}' failed to mount: {exc}")
            results.append(
                PluginInfo(name=entry.name, app_factory=target, loaded=False, error=str(exc))
            )
    return results


__all__ = ["PluginInfo", "discover_plugins", "mount_plugins"]
