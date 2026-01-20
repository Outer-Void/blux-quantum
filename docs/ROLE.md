# BLUX Quantum Role

BLUX Quantum is the dispatcher-only front door for the BLUX constellation. It provides
routing, visibility, and preview surfaces for requests, and it forwards receipts from
downstream systems without making decisions locally.

## Allowed responsibilities
- Build and emit request/receipt envelopes for routing visibility.
- Route tasks to the appropriate constellation component without enforcing outcomes.
- Surface previews of what will happen, including required receipt dependencies.
- Report status, configuration, and telemetry paths.

## Prohibited responsibilities
- Making policy, ethics, or permission decisions.
- Executing tools, commands, or subprocesses locally.
- Issuing, minting, signing, or verifying tokens.
- Performing Guard or Lite enforcement actions locally.
