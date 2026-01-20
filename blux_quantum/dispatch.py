"""Thin BLUX dispatcher CLI."""
from __future__ import annotations

import json
from typing import Any

import typer

from . import cli as core
from .envelope import create_envelope

app = typer.Typer(help="BLUX dispatcher — single activator entrypoint")

_PREVIEW_MATRIX: dict[str, dict[str, Any]] = {
    "doctor": {
        "capability_ref": "capability:blux.doctor",
        "next_repo": "Guard",
        "guard_receipt_required": False,
    },
    "status": {
        "capability_ref": "capability:blux.status",
        "next_repo": "Lite",
        "guard_receipt_required": False,
    },
    "aim": {
        "capability_ref": "capability:blux.aim",
        "next_repo": "cA",
        "guard_receipt_required": True,
    },
    "trace": {
        "capability_ref": "capability:blux.trace",
        "next_repo": "Guard",
        "guard_receipt_required": False,
    },
    "verify": {
        "capability_ref": "capability:blux.verify",
        "next_repo": "Guard",
        "guard_receipt_required": True,
    },
}


def _emit_preview(command: str) -> dict[str, Any]:
    preview = _PREVIEW_MATRIX[command]
    envelope = create_envelope(
        "dispatch_preview",
        {"capability_ref": preview["capability_ref"], "command": command},
        source="blux.dispatch",
    )
    payload = {
        "execution_preview": {
            "trace_id": envelope["trace_id"],
            "requested_capability": preview["capability_ref"],
            "next_repo": preview["next_repo"],
            "guard_receipt_required": preview["guard_receipt_required"],
        }
    }
    typer.echo(json.dumps(payload))
    return envelope


@app.command()
def doctor() -> None:
    """Dispatch to doctor diagnostics."""

    _emit_preview("doctor")
    core.doctor()


@app.command()
def status() -> None:
    """Dispatch to status summary."""

    _emit_preview("status")
    core.status()


@app.command()
def aim(intent: str = typer.Argument(..., help="High-level intent")) -> None:
    """Dispatch an intent for routing."""

    _emit_preview("aim")
    core.aim(intent)


@app.command()
def trace(trace_id: str = typer.Argument(..., help="Envelope trace identifier")) -> None:
    """Dispatch a trace lookup."""

    _emit_preview("trace")
    typer.echo(json.dumps({"trace_id": trace_id, "status": "queued"}))


@app.command()
def verify(artifact: str = typer.Argument(..., help="Artifact or token reference")) -> None:
    """Dispatch a verification request."""

    _emit_preview("verify")
    typer.echo(json.dumps({"artifact": artifact, "status": "queued"}))
