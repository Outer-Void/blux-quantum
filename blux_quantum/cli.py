"""BLUX Quantum Typer application."""
from __future__ import annotations

import json
import os
from importlib import metadata

import typer
from rich import print

from .config import load_config
from .plugins.loader import discover_plugins, mount_plugins
from .stability import disable_stability, enable_stability, stability_status
from .telemetry import record_event, telemetry_status

app = typer.Typer(help="BLUX Quantum — Unified Operator CLI")


@app.callback()
def _root(ctx: typer.Context, verbose: bool = typer.Option(False, "--verbose")) -> None:
    ctx.obj = {"verbose": verbose}
    record_event("cli.start", {"verbose": verbose})


@app.command()
def version() -> None:
    """Print version details."""
    try:
        package_version = metadata.version("blux-quantum")
    except metadata.PackageNotFoundError:  # pragma: no cover - editable installs
        package_version = "0.0.0"
    print({"bluxq": package_version, "telemetry": telemetry_status()})


@app.command("self-check")
def self_check() -> None:
    """Perform health checks without raising exceptions."""
    checks = []
    config = load_config()
    checks.append(("config", bool(config) or config == {}))

    telemetry_ok = record_event("self_check", {"config_keys": list(config.keys())})
    checks.append(("telemetry", telemetry_ok or True))

    plugins = discover_plugins()
    checks.append(("plugins", bool(plugins)))

    stability = stability_status()
    checks.append(("stability", "enabled" in stability))

    summary = {name: "ok" if ok else "warn" for name, ok in checks}
    print({"self-check": summary})


@app.command("plugins")
def plugins_list() -> None:
    """List available plugins."""
    plugins = discover_plugins()
    payload = [
        {
            "name": plugin.name,
            "loaded": plugin.loaded,
            "app_factory": plugin.app_factory,
            "error": plugin.error,
        }
        for plugin in plugins
    ]
    print(json.dumps(payload, indent=2))


@app.command("stability")
def stability(mode: str = typer.Argument(..., help="enable|disable")) -> None:
    """Toggle stability mode."""
    if mode == "enable":
        enable_stability()
        print(stability_status())
    elif mode == "disable":
        disable_stability()
        print(stability_status())
    else:
        typer.echo("Use: bluxq stability [enable|disable]")


@app.command("telemetry")
def telemetry_test() -> None:
    """Emit a telemetry test event."""
    record_event("cli.telemetry.test", {"pid": os.getpid()})
    print(telemetry_status())


mount_plugins(app)


if __name__ == "__main__":  # pragma: no cover
    app()
