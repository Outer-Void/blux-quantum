# Integrations

## Plugin Contract
External packages expose Typer apps via the `blux.plugins` entry-point group.

```toml
[project.entry-points."blux.plugins"]
guard = "blux_guard.cli:get_app"
```

## Guard
- Provides incident response tooling under `bluxq guard`.
- Shares telemetry with Quantum for unified auditing.

## Lite
- Lightweight deployment helpers accessible at `bluxq lite`.
- Designed for rapid prototyping and staging environments.

## Doctrine
- Governance and compliance operations anchored at `bluxq doctrine`.
- Synchronises policy definitions across the BLUX fleet.

## Future Plugins
- `blux-ca`, `blux-reg`, `blux-commander`, and others can register entry points without patching the core CLI.
