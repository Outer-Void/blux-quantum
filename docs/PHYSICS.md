# BLUX Quantum Physics (Phase 9)

## Invariants
- Quantum remains dispatcher-only: dispatch CLI exposes preview + routing only (no execution surfaces).
- Guard receipts are required for any routing that targets Lite.
- Phase 0 envelopes always include `schema_version`, `trace_id`, and `payload`.
- Guard receipts carry a human-readable `decision` string, but logic must rely on non-enum fields (e.g., `authorized`).
- Dispatch preview output always includes a `trace_id` for observability.
- High-level intent routing defaults to cA rather than Lite.
- Plugin discovery uses the canonical `blux.plugins` entry-point group or bundled defaults.

## Violations (must never happen)
- Using decision enums (ALLOW/WARN/BLOCK) as control-flow logic in core code.
- Emitting envelopes without a `trace_id` in dispatch outputs.
- Routing to Lite without a guard receipt requirement.
- Expanding Quantum into an execution runtime instead of a dispatcher.
