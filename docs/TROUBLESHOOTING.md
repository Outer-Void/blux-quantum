# Troubleshooting

## Windows Terminal Issues
- Use Windows Terminal or PowerShell 7+ for UTF-8 rendering.
- If commands hang, run `set PYTHONIOENCODING=utf-8`.

## Missing Typer
- Ensure dependencies installed: `pip install blux-quantum`.
- Validate Python path with `python -m site`.

## Permission Errors
- Verify the telemetry directory is writable or set `BLUXQ_HOME` to a writable path.

## Plugin Not Found
- Confirm the plugin package exposes an entry point under `blux.plugins`.
- Run `python -m importlib.metadata entry-points --group blux.plugins` for debugging.

## Self-Check Warnings
- Review config file syntax and ensure YAML is valid.
- Use `BLUXQ_TELEMETRY_WARN=always` during diagnostics to see degradation messages.
