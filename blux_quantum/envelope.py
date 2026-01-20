"""Phase 0 envelope helpers for BLUX Quantum."""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict


PHASE0_SCHEMA_VERSION = "0.1"


def create_envelope(
    envelope_type: str,
    payload: Dict[str, Any],
    *,
    source: str,
    trace_id: str | None = None,
) -> Dict[str, Any]:
    """Create a Phase 0 envelope payload."""

    if "capability_ref" in payload and not isinstance(payload["capability_ref"], str):
        raise ValueError("capability_ref must be a string")
    return {
        "schema_version": PHASE0_SCHEMA_VERSION,
        "envelope_id": uuid.uuid4().hex,
        "type": envelope_type,
        "created_at": time.time(),
        "source": source,
        "trace_id": trace_id or uuid.uuid4().hex,
        "payload": payload,
    }


__all__ = ["PHASE0_SCHEMA_VERSION", "create_envelope"]
