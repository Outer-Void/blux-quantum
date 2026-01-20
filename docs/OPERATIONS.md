# Operations

## Command Overview
- `blux request "<text>"` builds a request envelope.
- `blux dry-run "<text>"` routes through cA + Guard without Lite.
- `blux run "<text>"` routes the full chain when receipts allow.
- `blux inspect <artifact.json>` prints stored artifacts.

## Logging
- JSONL and SQLite logs are located under `~/.config/blux-quantum/logs/` by default.
- Override the location with `BLUXQ_HOME`.

## Plugin Lifecycle
- Plugins discovered via entry points are mounted at startup.
- Failures are logged to the console but do not stop the CLI.
