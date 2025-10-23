# Configuration

## Sources
1. Environment variables prefixed with `BLUXQ_`.
2. User config file at `~/.config/blux-quantum/config.yaml` (override with `BLUXQ_HOME`).
3. Local `config.yaml` in the working directory.

## YAML Structure
```yaml
telemetry:
  enabled: true
plugins:
  guard:
    endpoint: https://guard.blux.systems
```

## Environment Variables
- `BLUXQ_HOME`: override the configuration base directory.
- `BLUXQ_TELEMETRY`: set to `off` to disable writes.
- `BLUXQ_TELEMETRY_WARN`: set to `once` or `always` for warning behavior.

## Merge Rules
- Later sources override earlier ones.
- Nested dictionaries merge recursively.
