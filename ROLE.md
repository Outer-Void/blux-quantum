# BLUX Quantum Role

BLUX Quantum is a dispatcher-only activator. It builds request envelopes, routes to cA,
calls Guard, and forwards receipts to Lite. It does not enforce permissions, decide
outcomes, or execute tools directly; it only dispatches and surfaces what will happen.

Non-capabilities: execution, enforcement, tokens, doctrine, discernment.

Routing chain: request → discernment_report → guard_receipt → lite execute (or dry-run).
