"""Diagnostics utilities surfaced via the CLI."""
from __future__ import annotations

import importlib
import json
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from rich.table import Table

from .environment import detect_environment
from .plugins.quantum_framework.loader import discover_plugins
from .stability import stability_status
from .telemetry import telemetry_status


def _command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def _check_writable(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        sentinel = path / ".write_test"
        sentinel.write_text("ok", encoding="utf-8")
        sentinel.unlink(missing_ok=True)
        return True
    except OSError:
        return False


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

    checks = payload.get("checks", [])
    if checks:
        check_lines = [
            f"{check['name']}: {'ok' if check['ok'] else 'warn'} ({check['detail']})"
            for check in checks
        ]
        table.add_row("Checks", "\n".join(check_lines))

    return table


def diagnose() -> Dict[str, Any]:
    return collect_diagnostics()


def doctor() -> Dict[str, Any]:
    payload = collect_diagnostics()
    recommendations: List[str] = []
    checks: List[Dict[str, Any]] = []

    execs = payload.get("executables", {})
    for binary, available in execs.items():
        if not available:
            recommendations.append(f"Install '{binary}' via your package manager for richer features.")

    env = detect_environment()
    python_ok = sys.version_info >= (3, 9)
    checks.append(
        {
            "name": "python_version",
            "ok": python_ok,
            "detail": f"running {platform.python_version()} (requires >=3.9)",
        }
    )
    if not python_ok:
        recommendations.append("Upgrade Python to >=3.9 for full support.")

    config_ok = _check_writable(env.config_dir)
    checks.append(
        {
            "name": "config_dir",
            "ok": config_ok,
            "detail": f"{env.config_dir}",
        }
    )
    if not config_ok:
        recommendations.append(f"Config directory is not writable: {env.config_dir}")

    imports_ok = True
    import_errors: list[str] = []
    for module in ["blux_quantum", "blux_quantum.cli"]:
        try:
            importlib.import_module(module)
        except Exception as exc:  # pragma: no cover - defensive
            imports_ok = False
            import_errors.append(f"{module}: {exc}")
    checks.append(
        {
            "name": "core_imports",
            "ok": imports_ok,
            "detail": "; ".join(import_errors) if import_errors else "ok",
        }
    )
    if not imports_ok:
        recommendations.append("Core modules failed to import; check installation.")

    telemetry = payload.get("telemetry", {})
    if not telemetry.get("enabled", False):
        recommendations.append("Telemetry disabled — insights may be limited.")

    plugins = payload.get("plugins", [])
    if not any(plugin.get("loaded") for plugin in plugins):
        recommendations.append("No plugins loaded. Install extras or check entry-points.")

    checks.append(
        {
            "name": "plugins",
            "ok": any(plugin.get("loaded") for plugin in plugins),
            "detail": f"{len(plugins)} discovered",
        }
    )

    payload["recommendations"] = recommendations
    payload["recommendations_json"] = json.dumps(recommendations)
    payload["checks"] = checks
    return payload


__all__ = ["diagnose", "doctor", "render_diagnostics_table"]
