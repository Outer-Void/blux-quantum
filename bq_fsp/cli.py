"""Typer entry-point for the bq-fsp plugin."""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

import typer
from rich.console import Console
from rich.table import Table

from .rules import load_rules
from .sarif import to_sarif
from .scanner import Finding, scan

console = Console()
app = typer.Typer(name="bq-fsp", help="BLUX Quantum — Find Suspicious Patterns")


def _default_log_path() -> str | None:
    try:
        from bq.cli import default_fsp_log
    except Exception:  # pragma: no cover - optional shim missing
        return None
    return default_fsp_log()


def _dump_jsonl(findings: Sequence[Finding], destination: str | None) -> None:
    target = destination or _default_log_path()
    if target is None:
        sink = sys.stdout
        for finding in findings:
            sink.write(json.dumps(asdict(finding)) + "\n")
        return

    path = Path(target)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as sink:
        for finding in findings:
            sink.write(json.dumps(asdict(finding)) + "\n")


def _dump_table(findings: Sequence[Finding]) -> None:
    table = Table(title=f"bq-fsp findings ({len(findings)})")
    table.add_column("SEV", style="bold red")
    table.add_column("RULE", style="cyan")
    table.add_column("FILE", style="magenta")
    table.add_column("LINE", justify="right")
    table.add_column("SNIPPET")
    table.add_column("ID", style="green")

    for finding in findings:
        table.add_row(
            finding.severity,
            finding.rule_id,
            finding.file,
            str(finding.line),
            finding.match,
            finding.hash,
        )

    console.print(table)


def _dump_sarif(findings: Sequence[Finding], destination: str | None) -> None:
    payload = to_sarif(findings)
    data = json.dumps(payload, indent=2)
    if destination:
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding="utf-8")
    else:
        typer.echo(data)


@app.command("scan")
def cmd_scan(
    path: str = typer.Argument(".", help="Repository root to scan."),
    staged: bool = typer.Option(False, "--staged", help="Scan staged files only."),
    rules: str | None = typer.Option(None, "--rules", "-r", help="Override rules YAML."),
    fmt: str = typer.Option("table", "--format", "-f", help="Output format: table|jsonl|sarif."),
    out: str | None = typer.Option(None, "--out", "-o", help="Optional output path."),
) -> None:
    """Scan a path for suspicious patterns."""

    try:
        rule_set = load_rules(rules)
    except Exception as exc:
        console.print(f"[red]Failed to load rules: {exc}[/red]")
        raise typer.Exit(code=2)

    findings = scan(path, rule_set, only_staged=staged)
    findings_seq = list(findings)

    format_mode = fmt.lower()
    if format_mode == "table":
        _dump_table(findings_seq)
    elif format_mode == "jsonl":
        _dump_jsonl(findings_seq, out)
    elif format_mode == "sarif":
        _dump_sarif(findings_seq, out)
    else:  # pragma: no cover - guarded by Typer choice but kept defensive
        raise typer.BadParameter("format must be table, jsonl, or sarif")

    raise typer.Exit(code=0 if not findings_seq else 1)


@app.command("semgrep")
def cmd_semgrep(
    path: str = typer.Argument(".", help="Repository root to scan with Semgrep."),
    config: str = typer.Option("p/ci", "--config", "-c", help="Semgrep configuration"),
) -> None:
    """Thin wrapper around Semgrep for parity with bq-fsp."""

    try:
        exit_code = subprocess.call(["semgrep", "--config", config, path])
    except FileNotFoundError:
        console.print("[red]Semgrep is not installed.[/red]")
        raise typer.Exit(code=2)

    raise typer.Exit(code=exit_code)


def register(bq_app) -> None:
    """Register the plugin with the BLUX Quantum CLI."""

    fsp_app = typer.Typer(name="fsp", help="Find Suspicious Patterns")
    fsp_app.command("scan")(cmd_scan)
    fsp_app.command("semgrep")(cmd_semgrep)
    bq_app.add_typer(fsp_app, name="fsp")


__all__ = ["app", "register"]
