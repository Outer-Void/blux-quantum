# Integrations

## Plugin Contract
External packages expose Typer apps via the `blux.plugins` entry-point group.

```toml
[project.entry-points."blux.plugins"]
guard = "blux_guard.cli:get_app"
```

## cA
- cA emits discernment reports for incoming requests.
- Ensure the `blux-ca` command is available on PATH.

## Guard
- Guard executes receipt generation for routed requests.
- Quantum forwards discernment reports to Guard and persists the receipt artifacts.
- Ensure the `blux-guard` command is available on PATH.

## Lite
- Lite executes approved tasks after Guard returns an ALLOW/WARN receipt.
- Quantum forwards Guard receipts and captures Lite receipts.
- Ensure the `blux-lite` command is available on PATH.

## Future Plugins
- `blux-ca`, `blux-guard`, and `blux-lite` can register entry points without patching the core CLI.
