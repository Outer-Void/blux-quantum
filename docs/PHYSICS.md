# BLUX Quantum Physics (Phase 9)

## Invariants
- Quantum remains dispatcher-only: dispatch CLI exposes preview + routing only (no execution surfaces).
- Guard receipts are required for any routing that targets Lite.
- Phase 0 envelopes always include `trace_id`, `span_id`, `timestamp`, `source`, and `payload_schema`.
- Audit previews always include `trace_id`, artifact paths, decision band/score, receipt decision, and execution manifest (if known).
- Dispatch preview output always includes a `trace_id` for observability.
- Plugin discovery uses the canonical `blux.plugins` entry-point group or bundled defaults.

## Violations (must never happen)
- Emitting envelopes without a `trace_id` in dispatch outputs.
- Routing to Lite without a guard receipt requirement.
- Expanding Quantum into an execution runtime instead of a dispatcher.
