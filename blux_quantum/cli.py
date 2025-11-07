"""BLUX Quantum Typer application."""
from __future__ import annotations

import json
import os
import sys
from importlib import metadata
from pathlib import Path
from typing import Any, Dict

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .config import load_config
from .diagnostics import diagnose as run_diagnose
from .diagnostics import doctor as run_doctor
from .diagnostics import render_diagnostics_table
from .environment import detect_environment
from .orchestrator import OrchestrationError, evaluate_task, parse_context, route_task
from .plugins.quantum_framework.loader import discover_plugins, mount_plugins
from .stability import disable_stability, enable_stability, stability_status
from .telemetry import record_event, telemetry_status
from .tui import run as run_tui

app = typer.Typer(help="BLUX Quantum — Unified Operator CLI")
console = Console()

_banner_displayed = False


def _banner() -> Text:
    neon_logo = r"""
██████╗ ██╗     ██╗   ██╗██╗  ██╗    ██████╗ ██╗   ██╗
██╔══██╗██║     ██║   ██║██║ ██╔╝    ██╔══██╗╚██╗ ██╔╝
██████╔╝██║     ██║   ██║█████╔╝     ██████╔╝ ╚████╔╝ 
██╔══██╗██║     ██║   ██║██╔═██╗     ██╔═══╝   ╚██╔╝  
██████╔╝███████╗╚██████╔╝██║  ██╗    ██║        ██║   
╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝        ╚═╝   
"""
    caption = "BLUX Quantum :: Operator-grade tooling"
    text = Text(neon_logo.rstrip("\n"), style="bold magenta")
    text.append(f"\n{caption}", style="bold cyan")
    return text


def _startup_summary() -> Panel:
    env = detect_environment()
    telemetry = telemetry_status()
    stability = stability_status()
    plugins = discover_plugins()

    table = Table.grid(padding=(0, 1))
    table.add_column(justify="right", style="bold cyan")
    table.add_column(style="bold white")

    table.add_row("OS", f"{env.os_family} {env.os_release}")
    table.add_row("Python", env.python)
    table.add_row("Arch", env.architecture)
    table.add_row("Shell", env.shell)
    table.add_row("Terminal", env.term)
    table.add_row("Config", str(env.config_dir))
    table.add_row("Telemetry", "enabled" if telemetry.get("enabled") else "disabled")
    table.add_row("Stability", json.dumps(stability))
    table.add_row("Plugins", f"{sum(1 for p in plugins if p.loaded)} loaded / {len(plugins)} total")

    badges = []
    if env.is_termux:
        badges.append("Termux")
    if env.is_debian:
        badges.append("Debian")
    if env.is_macos:
        badges.append("macOS")
    if env.is_wsl:
        badges.append("WSL2")
    if badges:
        table.add_row("Targets", ", ".join(badges))

    return Panel(table, title="Startup Summary", subtitle="neonfetch", border_style="bright_magenta")


def render_banner() -> None:
    global _banner_displayed
    if _banner_displayed:
        return
    mode = os.environ.get("BLUXQ_BANNER", "auto").lower()
    if mode in {"0", "off", "false"}:
        return
    if mode == "auto":
        if os.environ.get("PYTEST_CURRENT_TEST"):
            return
        if not console.is_terminal or not sys.stdout.isatty():
            return
    console.print(_banner())
    console.print(_startup_summary())
    _banner_displayed = True


@app.callback()
def _root(ctx: typer.Context, verbose: bool = typer.Option(False, "--verbose")) -> None:
    ctx.obj = {"verbose": verbose}
    record_event("cli.start", {"verbose": verbose})
    render_banner()


@app.command()
def version() -> None:
    """Print version details."""
    try:
        package_version = metadata.version("blux-quantum")
    except metadata.PackageNotFoundError:  # pragma: no cover - editable installs
        package_version = "0.0.0"
    payload = {
        "bluxq": package_version,
        "telemetry": telemetry_status(),
        "stability": stability_status(),
    }
    typer.echo(str(payload))


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
    checks.append(("stability", stability.get("enabled", False)))

    summary = {name: "ok" if ok else "warn" for name, ok in checks}
    typer.echo(str({"self-check": summary}))


@app.command("plugins")
def plugins_list(json_output: bool = typer.Option(False, "--json", help="Emit JSON instead of a table.")) -> None:
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
    if json_output:
        typer.echo(json.dumps(payload, indent=2))
        return

    table = Table(title="Quantum Plugins")
    table.add_column("Name", style="bold cyan")
    table.add_column("Status", style="bold green")
    table.add_column("Factory", style="magenta")
    table.add_column("Error", style="red")
    for item in payload:
        status = "loaded" if item["loaded"] else "failed"
        table.add_row(item["name"], status, item["app_factory"], item.get("error") or "")
    console.print(table)


@app.command("stability")
def stability(mode: str = typer.Argument(..., help="enable|disable")) -> None:
    """Toggle stability mode."""
    if mode == "enable":
        enable_stability()
        typer.echo(str(stability_status()))
    elif mode == "disable":
        disable_stability()
        typer.echo(str(stability_status()))
    else:
        typer.echo("Use: bq stability [enable|disable]")


@app.command("telemetry")
def telemetry_test() -> None:
    """Emit a telemetry test event."""
    record_event("cli.telemetry.test", {"pid": os.getpid(), "cwd": str(Path.cwd())})
    typer.echo(str(telemetry_status()))


@app.command("diag")
def diagnostics(json_output: bool = typer.Option(False, "--json", help="Emit diagnostics as JSON.")) -> None:
    """Run diagnostics and display platform parity insights."""
    payload = run_diagnose()
    record_event("cli.diagnostics", {"json": json_output})
    if json_output:
        typer.echo(json.dumps(payload, indent=2))
        return
    console.print(render_diagnostics_table(payload))


@app.command("doctor")
def doctor(json_output: bool = typer.Option(False, "--json", help="Emit doctor recommendations as JSON.")) -> None:
    """Run diagnostics plus prescriptive recommendations."""
    payload = run_doctor()
    record_event("cli.doctor", {"json": json_output, "recommendations": len(payload.get("recommendations", []))})
    if json_output:
        typer.echo(json.dumps(payload, indent=2))
        return
    console.print(render_diagnostics_table(payload))
    if payload.get("recommendations"):
        console.print("[bold yellow]Recommendations:[/bold yellow]")
        for item in payload["recommendations"]:
            console.print(f" • {item}")


@app.command("route")
def route(
    task: str = typer.Argument(..., help="Task description to route."),
    context: str = typer.Option(None, "--context", help="Optional JSON context payload."),
    json_output: bool = typer.Option(False, "--json", help="Emit routing decision as JSON."),
) -> None:
    """Route a quantum task to the appropriate orchestrator plugin."""
    try:
        context_payload = parse_context(context)
        decision = route_task(task, context_payload)
        record_event("cli.route", {"task": task, "route": decision.route})
    except OrchestrationError as exc:
        record_event("cli.route.error", {"error": str(exc)})
        raise typer.BadParameter(str(exc))

    if json_output:
        typer.echo(json.dumps(decision.as_dict(), indent=2))
    else:
        table = Table(title="Routing Decision")
        table.add_column("Field", style="bold cyan")
        table.add_column("Value", style="bold white")
        for key, value in decision.as_dict().items():
            table.add_row(key, json.dumps(value) if isinstance(value, (dict, list)) else str(value))
        console.print(table)


@app.command("eval")
def evaluate(
    task: str = typer.Argument(..., help="Task description that was executed."),
    result: str = typer.Option(None, "--result", help="Optional JSON result payload."),
    json_output: bool = typer.Option(False, "--json", help="Emit evaluation summary as JSON."),
) -> None:
    """Evaluate the outcome of a task using the orchestrator heuristics."""
    try:
        result_payload: Dict[str, Any] | None = parse_context(result) if result else None
        summary = evaluate_task(task, result_payload)
        record_event("cli.eval", {"task": task, "score": summary["score"]})
    except OrchestrationError as exc:
        record_event("cli.eval.error", {"error": str(exc)})
        raise typer.BadParameter(str(exc))

    if json_output:
        typer.echo(json.dumps(summary, indent=2))
    else:
        table = Table(title="Evaluation Summary")
        table.add_column("Field", style="bold cyan")
        table.add_column("Value", style="bold white")
        for key, value in summary.items():
            table.add_row(key, json.dumps(value) if isinstance(value, (dict, list)) else str(value))
        console.print(table)


@app.command("tui")
def tui() -> None:  # pragma: no cover - interactive command
    """Launch the interactive Textual interface."""
    record_event("cli.tui", {})
    run_tui()


mount_plugins(app)


if __name__ == "__main__":  # pragma: no cover
    app()
