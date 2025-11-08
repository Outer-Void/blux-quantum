"""Diagnostics utilities surfaced via the CLI."""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from typing import Any, Dict, List

from rich.table import Table

from .environment import detect_environment
from .plugins.quantum_framework.loader import discover_plugins
from .stability import stability_status
from .telemetry import telemetry_status


def _command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def collect_diagnostics() -> Dict[str, Any]:
    env = detect_environment()
    plugins = discover_plugins()
    telemetry = telemetry_status()

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": env.as_dict(),
        "plugins": [plugin.__dict__ for plugin in plugins],
        "telemetry": telemetry,
        "stability": stability_status(),
        "executables": {
            "python": _command_exists("python"),
            "python3": _command_exists("python3"),
            "pip": _command_exists("pip"),
            "ssh": _command_exists("ssh"),
            "sqlite3": _command_exists("sqlite3"),
        },
    }


def render_diagnostics_table(payload: Dict[str, Any]) -> Table:
    table = Table(title="BLUX Quantum Diagnostics", show_lines=True)
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Details", style="magenta")

    environment = payload.get("environment", {})
    env_lines = [f"{key}: {value}" for key, value in environment.items()]
    table.add_row("Environment", "\n".join(env_lines))

    execs = payload.get("executables", {})
    exec_lines = [f"{key}: {'yes' if value else 'no'}" for key, value in execs.items()]
    table.add_row("Executables", "\n".join(exec_lines))

    telemetry = payload.get("telemetry", {})
    telemetry_lines = [f"{key}: {value}" for key, value in telemetry.items()]
    table.add_row("Telemetry", "\n".join(telemetry_lines))

    stability = payload.get("stability", {})
    stability_lines = [f"{key}: {value}" for key, value in stability.items()]
    table.add_row("Stability", "\n".join(stability_lines))

    plugins: List[Dict[str, Any]] = payload.get("plugins", [])
    if not plugins:
        table.add_row("Plugins", "None detected")
    else:
        plugin_lines = [f"{plugin['name']}: {'loaded' if plugin['loaded'] else 'error'}" for plugin in plugins]
        table.add_row("Plugins", "\n".join(plugin_lines))

    return table


def diagnose() -> Dict[str, Any]:
    return collect_diagnostics()


def doctor() -> Dict[str, Any]:
    payload = collect_diagnostics()
    recommendations: List[str] = []

    execs = payload.get("executables", {})
    for binary, available in execs.items():
        if not available:
            recommendations.append(f"Install '{binary}' via your package manager for richer features.")

    telemetry = payload.get("telemetry", {})
    if not telemetry.get("enabled", False):
        recommendations.append("Telemetry disabled — insights may be limited.")

    plugins = payload.get("plugins", [])
    if not any(plugin.get("loaded") for plugin in plugins):
        recommendations.append("No plugins loaded. Install extras or check entry-points.")

    payload["recommendations"] = recommendations
    payload["recommendations_json"] = json.dumps(recommendations)
    return payload


__all__ = ["diagnose", "doctor", "render_diagnostics_table"]
