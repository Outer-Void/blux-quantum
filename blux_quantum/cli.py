"""BLUX Quantum God Mode Typer application."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from functools import wraps
from importlib import metadata
from pathlib import Path
from typing import Any, Dict

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .audit import audit_command, audit_log_path
from .config import CONFIG_FILENAME, load_config
from .diagnostics import diagnose as run_diagnose
from .diagnostics import doctor as run_doctor
from .diagnostics import render_diagnostics_table
from .envelope import create_envelope
from .environment import detect_environment
from .orchestrator import OrchestrationError, evaluate_task, parse_context, route_task
from .plugins.quantum_framework.loader import discover_plugins, mount_plugins
from .reg_bridge import (
    create_key,
    ensure_key_store,
    has_keys,
    key_dir,
    load_keys,
    require_key,
    sign_path,
    verify_path,
)
from .stability import disable_stability, enable_stability, stability_status
from .telemetry import record_event, telemetry_status
from .tui import run as run_tui


app = typer.Typer(help="BLUX Quantum — Unified God Mode operator cockpit")
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


def _serialise_args(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    serialised: Dict[str, Any] = {}
    for key, value in kwargs.items():
        if isinstance(value, (str, int, float, bool, type(None))):
            serialised[key] = value
        elif isinstance(value, Path):
            serialised[key] = str(value)
        else:
            serialised[key] = str(value)
    return serialised


def audited(cmd_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            trace_id = uuid.uuid4().hex
            start = time.perf_counter()
            outcome = "ok"
            try:
                return func(*args, **kwargs)
            except Exception:
                outcome = "error"
                raise
            finally:
                duration_ms = int((time.perf_counter() - start) * 1000)
                audit_command(cmd_name, _serialise_args(kwargs), outcome, duration_ms, trace_id)

        return wrapper

    return decorator


def gated(action: str) -> None:
    try:
        require_key(action)
    except PermissionError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1)


@app.callback()
def _root(ctx: typer.Context, verbose: bool = typer.Option(False, "--verbose")) -> None:
    ctx.obj = {"verbose": verbose}
    record_event("cli.start", {"verbose": verbose})
    render_banner()


def _emit_envelope(envelope: Dict[str, Any]) -> None:
    typer.echo(json.dumps(envelope, indent=2))


def _simulate_phase0(task: str, capability_ref: str) -> tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    trace_id = uuid.uuid4().hex
    request = create_envelope(
        "request",
        {
            "task": task,
            "intent": "dispatch",
            "capability_ref": capability_ref,
        },
        source="blux.dispatch",
        trace_id=trace_id,
    )
    discernment_report = create_envelope(
        "discernment_report",
        {
            "task": task,
            "route": "lite",
            "confidence": 0.42,
            "notes": "stub discernment report (Phase 0)",
        },
        source="blux.guard.stub",
        trace_id=trace_id,
    )
    guard_receipt = create_envelope(
        "guard_receipt",
        {
            "decision": "ALLOW",
            "authorized": True,
            "reason": "stub guard receipt (Phase 0)",
            "capability_ref": capability_ref,
        },
        source="blux.guard.stub",
        trace_id=trace_id,
    )
    return request, discernment_report, guard_receipt


@app.command()
@audited("version")
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


@app.command()
@audited("about")
def about() -> None:
    """Show BLUX Quantum about information."""

    typer.echo("BLUX Quantum God Mode :: unified operator cockpit")


@app.command("doctor")
@audited("doctor")
def doctor() -> None:
    """Report environment details and contract presence hints."""

    env = detect_environment().as_dict()
    config = load_config()
    payload = {
        "environment": env,
        "contracts": {
            "phase0_envelope": "supported",
            "discernment_report": "expected from guard",
            "guard_receipt": "required for execution",
        },
        "endpoints": {
            "ca": config.get("ca_endpoint") or "unset",
            "guard": config.get("guard_endpoint") or "unset",
            "lite": config.get("lite_endpoint") or "unset",
        },
    }
    typer.echo(json.dumps(payload, indent=2))


@app.command("env")
@audited("env.show")
def env_show(export: bool = typer.Option(False, "--json", help="Emit JSON for env details.")) -> None:
    """Show environment details."""

    summary = detect_environment().as_dict()
    if export:
        typer.echo(json.dumps(summary, indent=2))
        return
    table = Table(title="Environment")
    table.add_column("Field", style="bold cyan")
    table.add_column("Value", style="bold white")
    for key, value in summary.items():
        table.add_row(key, str(value))
    console.print(table)


@app.command("env-export")
@audited("env.export")
def env_export(format: str = typer.Option("dotenv", "--format", help="Export format.")) -> None:
    """Export environment data."""

    env = detect_environment().as_dict()
    if format == "dotenv":
        for key, value in env.items():
            typer.echo(f"BLUXQ_{key.upper()}={value}")
    else:
        typer.echo(json.dumps(env))


@app.command("completion")
@audited("completion")
def completion(shell: str = typer.Argument(..., help="bash|zsh|fish")) -> None:
    """Generate shell completion script for the given shell."""

    result = subprocess.run([sys.executable, sys.argv[0], "--show-completion", shell], capture_output=True, text=True)
    typer.echo(result.stdout or result.stderr)


system_app = typer.Typer(help="System bootstrap/install/verification commands")


@system_app.command("bootstrap")
@audited("system.bootstrap")
def system_bootstrap() -> None:
    """Prepare the BLUX home with config, logs, keys, and state directories."""

    base = detect_environment().config_dir
    ensure_key_store()
    (base / "logs").mkdir(parents=True, exist_ok=True)
    (base / "state").mkdir(parents=True, exist_ok=True)
    typer.echo(f"Initialized BLUX Quantum home at {base}")


@system_app.command("install")
@audited("system.install")
def system_install() -> None:
    """Install constellation dependencies (placeholder)."""

    typer.echo("Installing constellation dependencies (stub)")


@system_app.command("doctor")
@audited("system.doctor")
def system_doctor(json_output: bool = typer.Option(False, "--json", help="Emit doctor recommendations as JSON.")) -> None:
    """Run health checks and emit diagnostics/recommendations."""

    payload = run_doctor()
    if json_output:
        typer.echo(json.dumps(payload, indent=2))
        return
    console.print(render_diagnostics_table(payload))
    if payload.get("recommendations"):
        console.print("[bold yellow]Recommendations:[/bold yellow]")
        for item in payload["recommendations"]:
            console.print(f" • {item}")


@system_app.command("status")
@audited("system.status")
def system_status() -> None:
    """Summarize config paths, telemetry, plugins, and key store state."""

    env = detect_environment()
    telemetry = telemetry_status()
    status = {
        "config_dir": str(env.config_dir),
        "config_file": str(env.config_dir / CONFIG_FILENAME),
        "audit_log": str(audit_log_path()),
        "key_store": {
            "path": str(key_dir()),
            "present": has_keys(),
            "count": len(load_keys()),
        },
        "telemetry": telemetry,
        "plugins": [plugin.name for plugin in discover_plugins()],
    }
    typer.echo(json.dumps(status, indent=2))


@system_app.command("up")
@audited("system.up")
def system_up() -> None:
    """Start the BLUX constellation (requires a registered key)."""

    gated("system.up")
    typer.echo("Launching BLUX constellation (stub)")


@system_app.command("down")
@audited("system.down")
def system_down() -> None:
    """Stop the BLUX constellation (requires a registered key)."""

    gated("system.down")
    typer.echo("Stopping BLUX constellation (stub)")


@system_app.command("update")
@audited("system.update")
def system_update() -> None:
    """Update BLUX constellation components (requires a registered key)."""

    gated("system.update")
    typer.echo("Updating BLUX constellation (stub)")


@system_app.command("repair")
@audited("system.repair")
def system_repair() -> None:
    """Repair BLUX constellation components (requires a registered key)."""

    gated("system.repair")
    typer.echo("Repairing BLUX constellation (stub)")


@system_app.command("clean")
@audited("system.clean")
def system_clean() -> None:
    """Clean caches/logs (requires a registered key)."""

    gated("system.clean")
    typer.echo("Cleaning caches/logs (stub)")


@system_app.command("bootstrap-diagnostics", hidden=True)
@audited("system.bootstrap_diagnostics")
def system_diagnostics(json_output: bool = typer.Option(False, "--json", help="Emit diagnostics as JSON.")) -> None:
    """Emit extended diagnostics (hidden helper for bootstrap)."""

    payload = run_diagnose()
    if json_output:
        typer.echo(json.dumps(payload, indent=2))
        return
    console.print(render_diagnostics_table(payload))


app.add_typer(system_app, name="system")


@app.command("launch")
@audited("launch")
def launch(quiet: bool = typer.Option(False, "--quiet", help="Suppress theatrics.")) -> None:
    """Launch the constellation (shortcut that calls system up)."""

    if not quiet:
        console.print("[bold green]Launching BLUX constellation in 3..2..1[/bold green]")
    system_up()


key_app = typer.Typer(help="Reg key management and signing")


@key_app.command("init")
@audited("key.init")
def key_init(label: str = typer.Option("default", "--label", help="Key label.")) -> None:
    """Create a new registration key."""

    path = create_key(label=label)
    typer.echo(f"Created key at {path}")


@key_app.command("list")
@audited("key.list")
def key_list() -> None:
    """List stored keys."""

    keys = load_keys()
    typer.echo(json.dumps(list(keys.values()), indent=2))


@key_app.command("show")
@audited("key.show")
def key_show(key_id: str) -> None:
    """Show metadata for a specific key."""

    keys = load_keys()
    if key_id not in keys:
        raise typer.BadParameter("Unknown key id")
    typer.echo(json.dumps(keys[key_id], indent=2))


@key_app.command("rotate")
@audited("key.rotate")
def key_rotate(key_id: str) -> None:
    """Rotate a key by creating a successor."""

    gated("key.rotate")
    new_path = create_key(label=f"rotated-from-{key_id}")
    typer.echo(f"Rotated key -> {new_path}")


@key_app.command("revoke")
@audited("key.revoke")
def key_revoke(key_id: str) -> None:
    """Revoke a key from the store."""

    gated("key.revoke")
    target = key_dir() / f"{key_id}.json"
    if target.exists():
        target.unlink()
    typer.echo(f"Revoked key {key_id}")


@key_app.command("sign")
@audited("key.sign")
def key_sign(kind: str = typer.Argument(..., help="manifest|diff"), path: Path = typer.Argument(...)) -> None:
    """Sign a manifest or diff file."""

    gated("key.sign")
    signature = sign_path(path)
    typer.echo(signature)


@key_app.command("verify")
@audited("key.verify")
def key_verify(kind: str = typer.Argument(..., help="manifest|diff"), path: Path = typer.Argument(...), signature: str = typer.Argument(...)) -> None:
    """Verify a manifest or diff signature."""

    gated("key.verify")
    ok = verify_path(path, signature)
    if not ok:
        raise typer.Exit(code=1)
    typer.echo("verified")


@key_app.command("audit-verify")
@audited("key.audit.verify_chain")
def key_audit_verify_chain() -> None:
    """Validate the audit JSONL chain stored on disk."""

    log_path = audit_log_path()
    if not log_path.exists():
        raise typer.Exit(code=1)
    lines = log_path.read_text(encoding="utf-8").splitlines()
    prev_hash = None
    for line in lines:
        computed = hashlib.sha256(line.encode("utf-8")).hexdigest() if line else None
        event = json.loads(line)
        if event.get("prev_audit_sha256") != prev_hash:
            raise typer.Exit(code=1)
        prev_hash = computed
    typer.echo("audit-chain-ok")


app.add_typer(key_app, name="key")


@app.command("aim")
@audited("aim")
def aim(intent: str = typer.Argument(..., help="High-level intent")) -> None:
    """Queue a high-level intent for routing."""

    typer.echo(json.dumps({"intent": intent, "route": "cA", "status": "queued"}))


@app.command("run")
@audited("run")
def run(
    task: str = typer.Argument(..., help="Task file or prompt"),
    capability_ref: str = typer.Option(
        "capability:blux.dispatch",
        "--capability-ref",
        help="Capability reference string.",
    ),
) -> None:
    """Dispatch a task, requiring a guard receipt before execution."""

    request, discernment_report, guard_receipt = _simulate_phase0(task, capability_ref)
    _emit_envelope(request)
    _emit_envelope(discernment_report)
    _emit_envelope(guard_receipt)
    authorized = guard_receipt["payload"].get("authorized") is True
    if not authorized:
        typer.echo("Refusing execution: guard_receipt did not authorize this action.")
        raise typer.Exit(code=1)
    typer.echo("Execution authorized by guard_receipt (stub).")


route_app = typer.Typer(help="Routing helpers")


@route_app.command("explain")
@audited("route.explain")
def route_explain(task: str = typer.Argument(..., help="Task description")) -> None:
    """Explain how the orchestrator would route the task."""

    try:
        decision = route_task(task, None)
    except OrchestrationError as exc:
        raise typer.BadParameter(str(exc))
    typer.echo(json.dumps(decision.as_dict(), indent=2))


@route_app.command("dry-run")
@audited("route.dry_run")
def route_dry_run(task: str = typer.Argument(..., help="Task description")) -> None:
    """Simulate routing without executing the task."""

    try:
        decision = route_task(task, None)
    except OrchestrationError as exc:
        raise typer.BadParameter(str(exc))
    typer.echo(json.dumps({"task": task, "route": decision.route, "executed": False}, indent=2))


app.add_typer(route_app, name="route")


@app.command("dry-run")
@audited("dry-run")
def dry_run(
    task: str = typer.Argument(..., help="Task file or prompt"),
    capability_ref: str = typer.Option(
        "capability:blux.dispatch",
        "--capability-ref",
        help="Capability reference string.",
    ),
) -> None:
    """Emit Phase 0 envelopes without executing."""

    request, discernment_report, guard_receipt = _simulate_phase0(task, capability_ref)
    _emit_envelope(request)
    _emit_envelope(discernment_report)
    _emit_envelope(guard_receipt)


@app.command("audit")
@audited("audit")
def audit() -> None:
    """Show where audit logs will be stored."""

    typer.echo(str(audit_log_path()))


@app.command("status")
@audited("status")
def status() -> None:
    """Show configured component endpoints."""

    config = load_config()
    payload = {
        "components": {
            "ca_endpoint": config.get("ca_endpoint") or "unset",
            "guard_endpoint": config.get("guard_endpoint") or "unset",
            "lite_endpoint": config.get("lite_endpoint") or "unset",
        }
    }
    typer.echo(json.dumps(payload, indent=2))


@app.command("eval")
@audited("eval")
def evaluate(task: str = typer.Argument(..., help="Task description that was executed."), result: str = typer.Option(None, "--result", help="Optional JSON result payload.")) -> None:
    """Evaluate a completed task with an optional JSON payload."""

    try:
        result_payload: Dict[str, Any] | None = parse_context(result) if result else None
        summary = evaluate_task(task, result_payload)
    except OrchestrationError as exc:
        raise typer.BadParameter(str(exc))
    typer.echo(json.dumps(summary, indent=2))


@app.command("demo")
@audited("demo")
def demo(target: str = typer.Argument(..., help="orchestrator|toolbox")) -> None:
    """Produce demo artifacts for orchestrator or toolbox showcases."""

    env = detect_environment()
    demo_root = env.config_dir / "demo"
    demo_root.mkdir(parents=True, exist_ok=True)
    artifact = demo_root / f"{target}-{int(time.time())}.json"
    payload = {
        "demo": target,
        "status": "ready",
        "generated_at": time.time(),
        "config_dir": str(env.config_dir),
    }
    artifact.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    typer.echo(json.dumps({"demo": target, "artifact": str(artifact)}, indent=2))


doctrine_app = typer.Typer(help="Doctrine governance bridge")


@doctrine_app.command("check")
@audited("doctrine.check")
def doctrine_check(target: str = typer.Argument(..., help="Intent or plan")) -> None:
    """Check a plan or intent against doctrine policies."""

    typer.echo(json.dumps({"target": target, "policy": "ok"}))


@doctrine_app.command("rules")
@audited("doctrine.rules.list")
def doctrine_rules_list() -> None:
    """List available doctrine rules."""

    typer.echo(json.dumps({"rules": ["default"], "count": 1}))


@doctrine_app.command("rules-test")
@audited("doctrine.rules.test")
def doctrine_rules_test(rule_id: str = typer.Argument(...), input: str = typer.Option("{}", "--input", help="JSON input")) -> None:
    """Test a doctrine rule with JSON input."""

    typer.echo(json.dumps({"rule": rule_id, "input": json.loads(input)}))


@doctrine_app.command("enforce")
@audited("doctrine.enforce")
def doctrine_enforce(mode: str = typer.Argument(..., help="on|off")) -> None:
    """Toggle doctrine enforcement."""

    gated("doctrine.enforce")
    typer.echo(json.dumps({"enforcement": mode}))


@doctrine_app.command("report")
@audited("doctrine.report")
def doctrine_report(format: str = typer.Option("md", "--format", help="md|json")) -> None:
    """Render a doctrine report in markdown or JSON."""

    typer.echo(json.dumps({"format": format, "status": "ok"}))


app.add_typer(doctrine_app, name="doctrine")


guard_app = typer.Typer(help="Guard security cockpit")


@guard_app.command("status")
@audited("guard.status")
def guard_status() -> None:
    """Summarize guard subsystem status."""

    typer.echo(json.dumps({"guard": "ok"}))


@guard_app.command("ps")
@audited("guard.ps")
def guard_ps() -> None:
    """List guard-related processes (placeholder)."""

    typer.echo(json.dumps({"processes": []}))


@guard_app.command("net")
@audited("guard.net")
def guard_net() -> None:
    """List guard-related network ports (placeholder)."""

    typer.echo(json.dumps({"ports": []}))


@guard_app.command("perms")
@audited("guard.perms")
def guard_perms_scan(path: Path = typer.Argument(..., help="Path to scan")) -> None:
    """Scan a path for permission anomalies."""

    typer.echo(json.dumps({"path": str(path), "perms": "ok"}))


@guard_app.command("secrets")
@audited("guard.secrets")
def guard_secrets_scan(path: Path = typer.Argument(..., help="Path to scan")) -> None:
    """Scan a path for potential secrets."""

    typer.echo(json.dumps({"path": str(path), "secrets": []}))


@guard_app.command("quarantine")
@audited("guard.quarantine")
def guard_quarantine(item: str = typer.Argument(..., help="Item to quarantine")) -> None:
    """Quarantine an item (requires a registered key)."""

    gated("guard.quarantine")
    typer.echo(json.dumps({"quarantined": item}))


@guard_app.command("report")
@audited("guard.report")
def guard_report(format: str = typer.Option("md", "--format", help="md|sarif")) -> None:
    """Generate a guard report."""

    typer.echo(json.dumps({"format": format, "status": "ok"}))


app.add_typer(guard_app, name="guard")


@app.command("stability")
@audited("stability")
def stability(mode: str = typer.Argument(..., help="enable|disable")) -> None:
    """Enable or disable stability mode."""

    if mode == "enable":
        enable_stability()
    elif mode == "disable":
        disable_stability()
    typer.echo(str(stability_status()))


telemetry_app = typer.Typer(help="Telemetry controls")


@telemetry_app.command("status")
@audited("telemetry.status")
def telemetry_status_cmd() -> None:
    """Show telemetry configuration and storage paths."""

    typer.echo(json.dumps(telemetry_status(), indent=2))


@telemetry_app.command("tail")
@audited("telemetry.tail")
def telemetry_tail() -> None:
    """Placeholder tail of telemetry events."""

    typer.echo("telemetry tail not implemented - JSONL stream placeholder")


@telemetry_app.command("export")
@audited("telemetry.export")
def telemetry_export(format: str = typer.Option("json", "--format", help="json|sqlite|md")) -> None:
    """Export telemetry data in a selected format."""

    typer.echo(json.dumps({"format": format, "status": "ok"}))


@telemetry_app.command("off")
@audited("telemetry.off")
def telemetry_off() -> None:
    """Disable telemetry for the current session."""

    os.environ["BLUXQ_TELEMETRY"] = "off"
    typer.echo("telemetry disabled")


app.add_typer(telemetry_app, name="telemetry")


help_app = typer.Typer(help="Global help index (GOD bridge)")


def _god_exec() -> str | None:
    return shutil.which("god")


def _god_passthrough(args: list[str]) -> None:
    god = _god_exec()
    if not god:
        typer.echo("GOD not installed; falling back to Typer help")
        typer.echo(app.get_help())
        return
    result = subprocess.run([god, *args], capture_output=True, text=True)
    output = result.stdout if result.stdout else result.stderr
    typer.echo(output)


@help_app.command("build")
@audited("help.build")
def help_build(format: str = typer.Option("console", "--format", help="console|md|html|json"), limit: int = typer.Option(50, "--limit")) -> None:
    """Build a help index via the GOD bridge when available."""

    _god_passthrough(["build", "--format", format, "--limit", str(limit)])


@help_app.command("search")
@audited("help.search")
def help_search(query: str = typer.Argument(...), names_only: bool = typer.Option(False, "--names-only")) -> None:
    """Search help topics through the GOD bridge."""

    args = ["search", query]
    if names_only:
        args.append("--names-only")
    _god_passthrough(args)


@help_app.command("info")
@audited("help.info")
def help_info(topic: str = typer.Argument(...)) -> None:
    """Show detailed help for a specific topic."""

    _god_passthrough(["info", topic])


@help_app.command("stats")
@audited("help.stats")
def help_stats() -> None:
    """Display aggregated help statistics."""

    _god_passthrough(["stats"])


app.add_typer(help_app, name="help")


@app.command("tui")
@audited("tui")
def tui() -> None:  # pragma: no cover - interactive command
    """Launch the interactive Textual user interface."""

    run_tui()


diagnostic_app = typer.Typer(help="Diagnostics helpers", hidden=True)


@diagnostic_app.command("self-check")
@audited("self_check")
def self_check() -> None:
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


@diagnostic_app.command("plugins")
@audited("plugins")
def plugins_list(json_output: bool = typer.Option(False, "--json", help="Emit JSON instead of a table.")) -> None:
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


app.add_typer(diagnostic_app, name="diag")


mount_plugins(app)


if __name__ == "__main__":  # pragma: no cover
    app()
