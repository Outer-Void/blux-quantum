from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from typer.testing import CliRunner

from blux_quantum import cli
from blux_quantum.audit import audit_log_path


def _env(tmp_path: Path) -> dict[str, str]:
    return {"BLUXQ_HOME": str(tmp_path)}


def _extract_json_objects(text: str) -> list[Any]:
    decoder = json.JSONDecoder()
    index = 0
    objects: list[Any] = []
    while index < len(text):
        if text[index].isspace():
            index += 1
            continue
        try:
            obj, end = decoder.raw_decode(text, index)
        except json.JSONDecodeError:
            index += 1
            continue
        objects.append(obj)
        index = end
    return objects


def _write_component_stub(
    tmp_path: Path,
    name: str,
    envelope_type: str,
    payload: dict[str, Any],
    payload_schema: str,
) -> Path:
    script_path = tmp_path / name
    script = f"""#!/usr/bin/env python3
import json
import sys
import uuid
from datetime import datetime, timezone

payload = {json.dumps(payload)}
request = json.load(sys.stdin)
trace_id = request.get("trace_id") or str(uuid.uuid4())
response = {{
    "schema": "blux://contracts/envelope.schema.json",
    "envelope_id": str(uuid.uuid4()),
    "type": "{envelope_type}",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "source": {{"repo": "{name}", "component": "{name}", "instance": "test"}},
    "trace_id": trace_id,
    "span_id": str(uuid.uuid4()),
    "payload_schema": "{payload_schema}",
    "payload": payload,
}}
print(json.dumps(response))
"""
    script_path.write_text(script, encoding="utf-8")
    script_path.chmod(0o755)
    return script_path


def _with_component_bins(tmp_path: Path) -> dict[str, str]:
    _write_component_stub(
        tmp_path,
        "blux-ca",
        "discernment_report",
        {"decision_band": "ALLOW", "decision_score": 0.9, "execution_manifest": "plans/exec.json"},
        "blux://contracts/discernment_report.schema.json",
    )
    _write_component_stub(
        tmp_path,
        "blux-guard",
        "guard_receipt",
        {"decision": "ALLOW"},
        "blux://contracts/guard_receipt.schema.json",
    )
    _write_component_stub(
        tmp_path,
        "blux-lite",
        "lite_receipt",
        {"status": "queued"},
        "blux://contracts/lite_receipt.schema.json",
    )
    env = _env(tmp_path)
    env["PATH"] = f"{tmp_path}{os.pathsep}{env.get('PATH', '')}"
    return env


def test_command_tree(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["--help"], env=_env(tmp_path))
    assert result.exit_code == 0
    assert "request" in result.stdout
    assert "inspect" in result.stdout
    assert "dry-run" in result.stdout
    assert "run" in result.stdout


def test_audit_written(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["request", "hello"], env=_env(tmp_path))
    assert result.exit_code == 0
    log = audit_log_path()
    assert log.exists()
    event = json.loads(log.read_text(encoding="utf-8").splitlines()[-1])
    assert event["cmd"] == "request"


def test_dry_run_outputs_audit_preview(tmp_path: Path) -> None:
    runner = CliRunner()
    env = _with_component_bins(tmp_path)
    result = runner.invoke(cli.app, ["dry-run", "hello"], env=env)
    assert result.exit_code == 0
    objects = _extract_json_objects(result.stdout)
    preview = objects[-1]["audit_preview"]
    assert preview["trace_id"]
    assert preview["decision_band"] == "ALLOW"
    assert preview["receipt_decision"] == "ALLOW"


def test_run_outputs_lite_receipt(tmp_path: Path) -> None:
    runner = CliRunner()
    env = _with_component_bins(tmp_path)
    result = runner.invoke(cli.app, ["run", "hello"], env=env)
    assert result.exit_code == 0
    objects = _extract_json_objects(result.stdout)
    types = [obj.get("type") for obj in objects if isinstance(obj, dict) and "type" in obj]
    assert "lite_receipt" in types
