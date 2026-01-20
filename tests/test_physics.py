from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from blux_quantum import cli
from blux_quantum.envelope import EnvelopeSource, create_envelope


def _env(tmp_path: Path) -> dict[str, str]:
    return {"BLUXQ_HOME": str(tmp_path)}


def _extract_json_objects(text: str) -> list[object]:
    decoder = json.JSONDecoder()
    index = 0
    objects: list[object] = []
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


def test_envelope_contract_fields() -> None:
    envelope = create_envelope(
        "guard_receipt",
        {"decision": "ALLOW"},
        source=EnvelopeSource(repo="blux-quantum", component="guard", instance="test"),
    )
    assert envelope["schema"]
    assert envelope["type"] == "guard_receipt"
    assert isinstance(envelope["trace_id"], str)
    assert isinstance(envelope["span_id"], str)
    assert isinstance(envelope["timestamp"], str)
    assert set(envelope["source"].keys()) == {"repo", "component", "instance"}
    assert envelope["payload"] == {"decision": "ALLOW"}


def test_request_outputs_trace_id(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["request", "task.txt"], env=_env(tmp_path))
    assert result.exit_code == 0
    objects = _extract_json_objects(result.stdout)
    envelope = objects[0]
    assert isinstance(envelope["trace_id"], str)
    assert envelope["trace_id"]
    assert envelope["payload_schema"] == "blux://contracts/request.schema.json"
