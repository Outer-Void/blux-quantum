# Operations

## Command Overview
- `bluxq version` reports versions and telemetry paths.
- `bluxq self-check` performs non-destructive diagnostics.
- `bluxq stability enable|disable` toggles stability mode.
- `bluxq telemetry` emits a test event.
- `bluxq plugins` lists mounted modules.

## Logging
- JSONL and SQLite logs are located under `~/.config/blux-quantum/logs/` by default.
- Override the location with `BLUXQ_HOME`.

## Verbose Mode
- Use `bluxq --verbose ...` to annotate telemetry events with the verbose flag.

## Plugin Lifecycle
- Plugins discovered via entry points are hot-mounted at startup.
- Failures are logged to the console but do not stop the CLI.

## Stability Mode
- When enabled, downstream services can interpret the state and quiesce workloads.
- Telemetry events capture the transition to inform operations analytics.
