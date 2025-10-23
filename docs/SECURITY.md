# Security

## Threat Model
- CLI executes with local user privileges; avoid escalated contexts when possible.
- Plugins are isolated Typer apps loaded from trusted packages.
- Telemetry is append-only and does not transmit externally by default.

## Supply Chain
- Dependencies pinned with lower bounds to ensure compatibility while enabling security updates.
- CI includes linting, typing, and testing gates before release.

## Telemetry Hardening
- Users can disable telemetry entirely or suppress warnings.
- Log directories are created with user permissions in the configuration home.

## Secrets Handling
- Sensitive configuration should be injected via environment variables, not YAML files committed to source control.

## Reporting
- Use `SECURITY.md` contact (ops@blux.systems) for disclosures.
