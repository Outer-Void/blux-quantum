# BLUX Quantum (`blux`)

BLUX Quantum is the dispatcher-only router CLI for the BLUX constellation. The `blux`
binary provides a single, auditable control spine that routes requests between cA,
Guard, and Lite without making permission decisions. Quantum does not decide outcomes
or execute tools directly; it only dispatches and surfaces what will happen. Install
`blux-ca`, `blux-guard`, and `blux-lite` to complete the chain.

The legacy `bluxq` binary remains available as a backward-compatible alias.

## Role and non-goals
BLUX Quantum is dispatcher-only: it provides routing, visibility, and preview
surfaces for constellation requests. It does not act as a policy engine or an
execution runtime.

Non-capabilities:
- Execution or enforcement.
- Tokens, signatures, or verification.
- Doctrine, policy, or discernment.

Routing chain:
`request` → `discernment_report` (cA) → `guard_receipt` (Guard) → `lite` execute (or dry-run).

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## 60-second quickstart
1. Create a request envelope:
   ```bash
   blux request "Summarize the repo" --out-dir ./artifacts
   ```
2. Route a request through cA and Guard without executing:
   ```bash
   blux dry-run "Plan the change" --out-dir ./artifacts
   ```
3. Route the full chain (Guard receipt required before Lite):
   ```bash
   blux run "Apply the change" --out-dir ./artifacts
   ```

Legacy alias (still supported):
```bash
bluxq request "Summarize the repo"
```

## Router-only examples
```bash
blux request "Draft a release plan" --out-dir ./artifacts
blux dry-run "Draft the run" --out-dir ./artifacts
blux run "Execute the run" --out-dir ./artifacts
```

## Full command reference
The section below is generated directly from the Typer application surface via
`python scripts/generate_command_reference.py`. Run `make gen-readme` to refresh it after
CLI changes.

<!-- BEGIN AUTO-GENERATED COMMANDS -->

_Generated via `python scripts/generate_command_reference.py`._

- `blux request` — Create a request envelope.
  - Example: `blux request [OPTIONS] TASK`

- `blux inspect` — Print a stored artifact.
  - Example: `blux inspect [OPTIONS] ARTIFACT`

- `blux dry-run` — Route through cA and Guard without invoking Lite.
  - Example: `blux dry-run [OPTIONS] TASK`

- `blux run` — Route through cA, Guard, and Lite with receipt enforcement.
  - Example: `blux run [OPTIONS] TASK`

<!-- END AUTO-GENERATED COMMANDS -->









## Config, logs, and audit
- **Config home:** defaults to `~/.config/blux-quantum` or `${BLUXQ_HOME}`/`${XDG_CONFIG_HOME}`
  if set. User config file: `<config_dir>/config.yaml`.
- **Audit log:** `<config_dir>/logs/audit.jsonl` (append-only JSONL).
- **Telemetry:** JSONL at `<config_dir>/logs/audit.jsonl`, SQLite at
  `<config_dir>/logs/telemetry.db`. Disable with `BLUXQ_TELEMETRY=off`.
- **Banner control:** set `BLUXQ_BANNER=off` to silence the startup banner in non-interactive
  environments.

## Plugin model
- Plugins are discovered through the `blux.plugins` entry-point group and mounted under their
  entry-point name.
- A minimal plugin skeleton:
  ```toml
  [project.entry-points."blux.plugins"]
  myplugin = "my_package.cli:get_app"
  ```
  ```python
  import typer

  app = typer.Typer(help="My BLUX extension")

  @app.command()
  def status():
      print({"status": "ok"})

  def get_app():
      return app
  ```

## Operator runbook highlights
- Build a request envelope: `blux request "<text>"`
- Route without Lite: `blux dry-run "<text>"`
- Route the full chain: `blux run "<text>"`

## Maintenance
- Format and lint: `make fmt` / `make lint`
- Tests: `make test`
- Regenerate README command reference: `make gen-readme`

## Support
Support / Contact: outervoid.blux@gmail.com
