# Installation

## Requirements
- Python 3.9 or newer.
- Supported on Linux, macOS, Windows (PowerShell), and Termux on Android.

## Quick Start
```bash
pip install blux-quantum
```

## Development Install
```bash
pip install -e .[dev]
```

## Shell Completion
Enable Typer auto-completion by exporting `_BLUXQ_COMPLETE`:
```bash
eval "$(bluxq --install-completion)"
```

## Termux Notes
- Install Python via `pkg install python`.
- Use `pip install --user blux-quantum` and ensure `$HOME/.local/bin` is on PATH.

## PowerShell Alias
- Run `scripts/demo_install_alias.ps1` to register a convenience alias for `bluxq`.

## Telemetry Controls
- Disable telemetry with `BLUXQ_TELEMETRY=off`.
- Surface one-time warnings with `BLUXQ_TELEMETRY_WARN=once`.
