"""Phase 0 envelope helpers for BLUX Quantum."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import os
import socket
import uuid
from typing import Any, Dict


ENVELOPE_SCHEMA = "blux://contracts/envelope.schema.json"
REQUEST_SCHEMA = "blux://contracts/request.schema.json"
DISCERNMENT_SCHEMA = "blux://contracts/discernment_report.schema.json"
GUARD_RECEIPT_SCHEMA = "blux://contracts/guard_receipt.schema.json"

PAYLOAD_SCHEMAS = {
    "request": REQUEST_SCHEMA,
    "discernment_report": DISCERNMENT_SCHEMA,
    "guard_receipt": GUARD_RECEIPT_SCHEMA,
}


@dataclass(frozen=True)
class EnvelopeSource:
    repo: str
    component: str
    instance: str

    def as_dict(self) -> Dict[str, str]:
        return {"repo": self.repo, "component": self.component, "instance": self.instance}


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_instance() -> str:
    return os.environ.get("BLUXQ_INSTANCE") or socket.gethostname()


def create_envelope(
    envelope_type: str,
    payload: Dict[str, Any],
    *,
    source: EnvelopeSource,
    trace_id: str | None = None,
    span_id: str | None = None,
    payload_schema: str | None = None,
) -> Dict[str, Any]:
    """Create a Phase 0 envelope payload."""

    if "capability_ref" in payload and not isinstance(payload["capability_ref"], str):
        raise ValueError("capability_ref must be a string")
    resolved_payload_schema = payload_schema or PAYLOAD_SCHEMAS.get(envelope_type)
    return {
        "schema": ENVELOPE_SCHEMA,
        "envelope_id": str(uuid.uuid4()),
        "type": envelope_type,
        "timestamp": _utc_timestamp(),
        "source": source.as_dict(),
        "trace_id": trace_id or str(uuid.uuid4()),
        "span_id": span_id or str(uuid.uuid4()),
        "payload_schema": resolved_payload_schema,
        "payload": payload,
    }


__all__ = [
    "ENVELOPE_SCHEMA",
    "REQUEST_SCHEMA",
    "DISCERNMENT_SCHEMA",
    "GUARD_RECEIPT_SCHEMA",
    "EnvelopeSource",
    "create_envelope",
]
