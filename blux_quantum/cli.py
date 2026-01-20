"""BLUX Quantum router CLI."""
from __future__ import annotations

import json
import os
import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import typer

from .audit import audit_command
from .envelope import (
    DISCERNMENT_SCHEMA,
    GUARD_RECEIPT_SCHEMA,
    EnvelopeSource,
    REQUEST_SCHEMA,
    create_envelope,
)
from .environment import detect_environment

app = typer.Typer(help="BLUX Quantum — dispatcher-only activator")

ALLOW_DECISIONS = {"ALLOW", "WARN"}


class RouterError(RuntimeError):
    pass


@dataclass
class ChainResult:
    trace_id: str
    artifacts: list[Path]
    request: Dict[str, Any]
    discernment_report: Dict[str, Any] | None = None
    guard_receipt: Dict[str, Any] | None = None
    lite_receipt: Dict[str, Any] | None = None
    execution_manifest: str | None = None


def _source(component: str) -> EnvelopeSource:
    instance = os.environ.get("BLUXQ_INSTANCE") or os.environ.get("HOSTNAME") or "local"
    return EnvelopeSource(repo="blux-quantum", component=component, instance=instance)


def _default_out_dir() -> Path:
    env = detect_environment()
    out_dir = env.config_dir / "artifacts" / "router"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def _emit_json(payload: Dict[str, Any]) -> None:
    typer.echo(json.dumps(payload, indent=2))


def _persist_artifacts(envelopes: list[Dict[str, Any]], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[Path] = []
    for index, envelope in enumerate(envelopes, start=1):
        name = f"{index:02d}-{envelope['type']}-{envelope['trace_id']}.json"
        path = out_dir / name
        path.write_text(json.dumps(envelope, indent=2), encoding="utf-8")
        artifacts.append(path)
    return artifacts


def _invoke_component(component: str, envelope: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if component == "ca":
            result = subprocess.run(
                ["blux-ca"],
                input=json.dumps(envelope),
                text=True,
                capture_output=True,
                check=True,
            )
        elif component == "guard":
            result = subprocess.run(
                ["blux-guard"],
                input=json.dumps(envelope),
                text=True,
                capture_output=True,
                check=True,
            )
        elif component == "lite":
            result = subprocess.run(
                ["blux-lite"],
                input=json.dumps(envelope),
                text=True,
                capture_output=True,
                check=True,
            )
        else:
            raise RouterError(f"Unknown component '{component}'")
    except FileNotFoundError as exc:
        raise RouterError(f"Missing component command: {component}") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or "component execution failed"
        raise RouterError(message) from exc
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RouterError("Component output was not JSON") from exc


def _extract_decision(report: Dict[str, Any]) -> tuple[str | None, float | None, str | None]:
    payload = report.get("payload") if isinstance(report, dict) else None
    if not isinstance(payload, dict):
        return None, None, None
    band = payload.get("decision_band") or payload.get("band")
    score = payload.get("decision_score") or payload.get("score")
    manifest = payload.get("execution_manifest")
    return band, score, manifest


def _extract_receipt_decision(receipt: Dict[str, Any]) -> str | None:
    payload = receipt.get("payload") if isinstance(receipt, dict) else None
    if not isinstance(payload, dict):
        return None
    return payload.get("decision")


def _assert_uuid(value: str, label: str) -> None:
    try:
        uuid.UUID(value)
    except (ValueError, TypeError) as exc:
        raise RouterError(f"{label} must be a UUID") from exc


def _validate_envelope(envelope: Dict[str, Any], expected_type: str | None = None) -> Dict[str, Any]:
    if expected_type and envelope.get("type") != expected_type:
        raise RouterError(f"Expected {expected_type} envelope")
    for field in ("trace_id", "span_id", "timestamp", "source", "payload"):
        if field not in envelope:
            raise RouterError(f"Envelope missing {field}")
    _assert_uuid(envelope.get("trace_id"), "trace_id")
    _assert_uuid(envelope.get("span_id"), "span_id")
    source = envelope.get("source")
    if not isinstance(source, dict) or not {"repo", "component", "instance"}.issubset(source.keys()):
        raise RouterError("Envelope source must include repo, component, and instance")
    if envelope.get("type") == "discernment_report" and not envelope.get("payload_schema"):
        envelope["payload_schema"] = DISCERNMENT_SCHEMA
    if envelope.get("type") == "guard_receipt" and not envelope.get("payload_schema"):
        envelope["payload_schema"] = GUARD_RECEIPT_SCHEMA
    return envelope


def _emit_audit_preview(result: ChainResult) -> None:
    band, score, manifest = _extract_decision(result.discernment_report or {})
    receipt_decision = _extract_receipt_decision(result.guard_receipt or {})
    preview = {
        "trace_id": result.trace_id,
        "artifacts": [str(path) for path in result.artifacts],
        "decision_band": band,
        "decision_score": score,
        "receipt_decision": receipt_decision,
        "execution_manifest": manifest or result.execution_manifest,
    }
    _emit_json({"audit_preview": preview})


def _build_request(task: str, trace_id: str) -> Dict[str, Any]:
    return create_envelope(
        "request",
        {"text": task},
        source=_source("quantum"),
        trace_id=trace_id,
        payload_schema=REQUEST_SCHEMA,
    )


def _build_guard_request(
    request: Dict[str, Any],
    report: Dict[str, Any],
    trace_id: str,
) -> Dict[str, Any]:
    return create_envelope(
        "guard_request",
        {"request": request, "discernment_report": report},
        source=_source("quantum"),
        trace_id=trace_id,
    )


def _build_lite_request(
    request: Dict[str, Any],
    receipt: Dict[str, Any],
    trace_id: str,
) -> Dict[str, Any]:
    return create_envelope(
        "lite_request",
        {"request": request, "guard_receipt": receipt},
        source=_source("quantum"),
        trace_id=trace_id,
    )


def _route_chain(task: str, include_lite: bool, out_dir: Path) -> ChainResult:
    trace_id = str(uuid.uuid4())
    request = _build_request(task, trace_id)
    envelopes: list[Dict[str, Any]] = [request]

    report = _validate_envelope(_invoke_component("ca", request), expected_type="discernment_report")
    envelopes.append(report)
    guard_request = _build_guard_request(request, report, trace_id)
    envelopes.append(guard_request)
    guard_receipt = _validate_envelope(_invoke_component("guard", guard_request), expected_type="guard_receipt")
    envelopes.append(guard_receipt)

    if include_lite:
        if not guard_receipt:
            raise RouterError("Guard receipt required before invoking Lite")
        decision = _extract_receipt_decision(guard_receipt)
        if decision == "REQUIRE_CONFIRM":
            artifacts = _persist_artifacts(envelopes, out_dir)
            result = ChainResult(trace_id=trace_id, artifacts=artifacts, request=request, discernment_report=report, guard_receipt=guard_receipt)
            _emit_audit_preview(result)
            raise typer.Exit(code=2)
        if decision == "BLOCK":
            artifacts = _persist_artifacts(envelopes, out_dir)
            result = ChainResult(trace_id=trace_id, artifacts=artifacts, request=request, discernment_report=report, guard_receipt=guard_receipt)
            _emit_audit_preview(result)
            raise typer.Exit(code=3)
        if decision and decision not in ALLOW_DECISIONS:
            raise RouterError(f"Unsupported receipt decision: {decision}")
        lite_request = _build_lite_request(request, guard_receipt, trace_id)
        envelopes.append(lite_request)
        lite_receipt = _validate_envelope(_invoke_component("lite", lite_request))
        envelopes.append(lite_receipt)
    else:
        lite_receipt = None

    artifacts = _persist_artifacts(envelopes, out_dir)
    return ChainResult(
        trace_id=trace_id,
        artifacts=artifacts,
        request=request,
        discernment_report=report,
        guard_receipt=guard_receipt,
        lite_receipt=lite_receipt,
    )


def _audit(cmd: str, args: Dict[str, Any], outcome: str) -> None:
    audit_command(cmd, args, outcome, 0, str(uuid.uuid4()))


@app.command("request")
def request(task: str = typer.Argument(..., help="Request text"), out_dir: Path | None = typer.Option(None, "--out-dir")) -> None:
    """Create a request envelope."""

    trace_id = str(uuid.uuid4())
    envelope = _build_request(task, trace_id)
    _emit_json(envelope)
    artifacts = _persist_artifacts([envelope], out_dir or _default_out_dir())
    _emit_json({"trace_id": trace_id, "artifacts": [str(path) for path in artifacts]})
    _audit("request", {"task": task}, "ok")


@app.command("inspect")
def inspect(artifact: Path = typer.Argument(..., help="Artifact JSON path")) -> None:
    """Print a stored artifact."""

    payload = json.loads(artifact.read_text(encoding="utf-8"))
    _emit_json(payload)
    _audit("inspect", {"artifact": str(artifact)}, "ok")


@app.command("dry-run")
def dry_run(task: str = typer.Argument(..., help="Request text"), out_dir: Path | None = typer.Option(None, "--out-dir")) -> None:
    """Route through cA and Guard without invoking Lite."""
    try:
        result = _route_chain(task, include_lite=False, out_dir=out_dir or _default_out_dir())
    except RouterError as exc:
        _audit("dry-run", {"task": task}, "error")
        raise typer.Exit(code=1, message=str(exc))
    for envelope in [result.request, result.discernment_report, result.guard_receipt]:
        if envelope:
            _emit_json(envelope)
    _emit_audit_preview(result)
    _audit("dry-run", {"task": task}, "ok")


@app.command("run")
def run(task: str = typer.Argument(..., help="Request text"), out_dir: Path | None = typer.Option(None, "--out-dir")) -> None:
    """Route through cA, Guard, and Lite with receipt enforcement."""

    try:
        result = _route_chain(task, include_lite=True, out_dir=out_dir or _default_out_dir())
    except RouterError as exc:
        _audit("run", {"task": task}, "error")
        raise typer.Exit(code=1, message=str(exc))
    for envelope in [
        result.request,
        result.discernment_report,
        result.guard_receipt,
        result.lite_receipt,
    ]:
        if envelope:
            _emit_json(envelope)
    _emit_audit_preview(result)
    _audit("run", {"task": task}, "ok")


if __name__ == "__main__":  # pragma: no cover
    app()
