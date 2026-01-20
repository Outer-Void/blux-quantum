# BLUX Quantum (`blux`)

BLUX Quantum is the unified router CLI for the BLUX constellation. The `blux` binary
provides a single, auditable control spine that routes requests between cA, Guard,
and Lite without making permission decisions. Everything shipped here is
self-contained—no external repositories are required.

The legacy `bluxq` binary remains available as a backward-compatible alias.

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## 60-second quickstart
1. Inspect the surface and ensure dependencies resolve:
   ```bash
   BLUXQ_BANNER=off blux system doctor
   ```
2. Bootstrap the local operator home (config, logs, keys, state):
   ```bash
   blux system bootstrap
   ```
3. Run the required demos (artifacts are written under the config directory):
   ```bash
   blux demo orchestrator
   blux demo toolbox
   ```
4. Route a task through the router-only pipeline (artifacts are persisted locally):
   ```bash
   blux ask "Summarize the repo" --confirm --out-dir ./artifacts
   blux dry-run "Plan the change" --token token-123 --revocations revoke-1,revoke-2 --out-dir ./artifacts
   blux run "Apply the change" --token token-123 --confirm --out-dir ./artifacts
   ```
5. Verify the constellation wiring and telemetry paths:
   ```bash
   blux system status
   blux telemetry status
   ```

Legacy alias (still supported):
```bash
bluxq system doctor
```

## Router-only examples
```bash
blux ask "Draft a release plan" --confirm --out-dir ./artifacts
blux dry-run "Draft the run" --token tok-001 --revocations revoke-9 --out-dir ./artifacts
blux run "Execute the run" --token tok-001 --confirm --out-dir ./artifacts
```

## Full command reference
The section below is generated directly from the Typer application surface (including bundled
plugins) via `python scripts/generate_command_reference.py`. Run `make gen-readme` to refresh it
after CLI changes.

<!-- BEGIN AUTO-GENERATED COMMANDS -->

_Generated via `python scripts/generate_command_reference.py`._

- `bluxq version` — Print version details.
  - Example: `bluxq version [OPTIONS]`

- `bluxq about` — Show BLUX Quantum about information.
  - Example: `bluxq about [OPTIONS]`

- `bluxq env` — Show environment details.
  - Example: `bluxq env [OPTIONS]`

- `bluxq env-export` — Export environment data.
  - Example: `bluxq env-export [OPTIONS]`

- `bluxq completion` — Generate shell completion script for the given shell.
  - Example: `bluxq completion [OPTIONS] SHELL`

- `bluxq launch` — Launch the constellation (shortcut that calls system up).
  - Example: `bluxq launch [OPTIONS]`

- `bluxq aim` — Queue a high-level intent for routing.
  - Example: `bluxq aim [OPTIONS] INTENT`

- `bluxq run` — Route and execute a task prompt or file.
  - Example: `bluxq run [OPTIONS] TASK`

- `bluxq eval` — Evaluate a completed task with an optional JSON payload.
  - Example: `bluxq eval [OPTIONS] TASK`

- `bluxq demo` — Produce demo artifacts for orchestrator or toolbox showcases.
  - Example: `bluxq demo [OPTIONS] TARGET`

- `bluxq stability` — Enable or disable stability mode.
  - Example: `bluxq stability [OPTIONS] MODE`

- `bluxq tui` — Launch the interactive Textual user interface.
  - Example: `bluxq tui [OPTIONS]`

- `bluxq system` — System bootstrap/install/verification commands
  - Example: `bluxq system [OPTIONS] COMMAND [ARGS]...`
  - Subcommands:
    - `bluxq system bootstrap` — Prepare the BLUX home with config, logs, keys, and state directories.
      - Example: `bluxq system bootstrap [OPTIONS]`
    - `bluxq system install` — Install constellation dependencies (placeholder).
      - Example: `bluxq system install [OPTIONS]`
    - `bluxq system doctor` — Run health checks and emit diagnostics/recommendations.
      - Example: `bluxq system doctor [OPTIONS]`
    - `bluxq system status` — Summarize config paths, telemetry, plugins, and key store state.
      - Example: `bluxq system status [OPTIONS]`
    - `bluxq system up` — Start the BLUX constellation (requires a registered key).
      - Example: `bluxq system up [OPTIONS]`
    - `bluxq system down` — Stop the BLUX constellation (requires a registered key).
      - Example: `bluxq system down [OPTIONS]`
    - `bluxq system update` — Update BLUX constellation components (requires a registered key).
      - Example: `bluxq system update [OPTIONS]`
    - `bluxq system repair` — Repair BLUX constellation components (requires a registered key).
      - Example: `bluxq system repair [OPTIONS]`
    - `bluxq system clean` — Clean caches/logs (requires a registered key).
      - Example: `bluxq system clean [OPTIONS]`

- `bluxq key` — Reg key management and signing
  - Example: `bluxq key [OPTIONS] COMMAND [ARGS]...`
  - Subcommands:
    - `bluxq key init` — Create a new registration key.
      - Example: `bluxq key init [OPTIONS]`
    - `bluxq key list` — List stored keys.
      - Example: `bluxq key list [OPTIONS]`
    - `bluxq key show` — Show metadata for a specific key.
      - Example: `bluxq key show [OPTIONS] KEY_ID`
    - `bluxq key rotate` — Rotate a key by creating a successor.
      - Example: `bluxq key rotate [OPTIONS] KEY_ID`
    - `bluxq key revoke` — Revoke a key from the store.
      - Example: `bluxq key revoke [OPTIONS] KEY_ID`
    - `bluxq key sign` — Sign a manifest or diff file.
      - Example: `bluxq key sign [OPTIONS] KIND PATH`
    - `bluxq key verify` — Verify a manifest or diff signature.
      - Example: `bluxq key verify [OPTIONS] KIND PATH SIGNATURE`
    - `bluxq key audit-verify` — Validate the audit JSONL chain stored on disk.
      - Example: `bluxq key audit-verify [OPTIONS]`

- `bluxq route` — Routing helpers
  - Example: `bluxq route [OPTIONS] COMMAND [ARGS]...`
  - Subcommands:
    - `bluxq route explain` — Explain how the orchestrator would route the task.
      - Example: `bluxq route explain [OPTIONS] TASK`
    - `bluxq route dry-run` — Simulate routing without executing the task.
      - Example: `bluxq route dry-run [OPTIONS] TASK`

- `bluxq doctrine` — Example BLUX Doctrine integration.
  - Example: `bluxq doctrine [OPTIONS] COMMAND [ARGS]...`
  - Subcommands:
    - `bluxq doctrine schema` — Display doctrine schema version.
      - Example: `bluxq doctrine schema [OPTIONS]`
    - `bluxq doctrine sync` — Synchronise doctrine data.
      - Example: `bluxq doctrine sync [OPTIONS]`

- `bluxq guard` — Example BLUX Guard integration.
  - Example: `bluxq guard [OPTIONS] COMMAND [ARGS]...`
  - Subcommands:
    - `bluxq guard status` — Show guard status.
      - Example: `bluxq guard status [OPTIONS]`
    - `bluxq guard ping` — Send a ping to the guard service.
      - Example: `bluxq guard ping [OPTIONS]`

- `bluxq telemetry` — Telemetry controls
  - Example: `bluxq telemetry [OPTIONS] COMMAND [ARGS]...`
  - Subcommands:
    - `bluxq telemetry status` — Show telemetry configuration and storage paths.
      - Example: `bluxq telemetry status [OPTIONS]`
    - `bluxq telemetry tail` — Placeholder tail of telemetry events.
      - Example: `bluxq telemetry tail [OPTIONS]`
    - `bluxq telemetry export` — Export telemetry data in a selected format.
      - Example: `bluxq telemetry export [OPTIONS]`
    - `bluxq telemetry off` — Disable telemetry for the current session.
      - Example: `bluxq telemetry off [OPTIONS]`

- `bluxq help` — Global help index (GOD bridge)
  - Example: `bluxq help [OPTIONS] COMMAND [ARGS]...`
  - Subcommands:
    - `bluxq help build` — Build a help index via the GOD bridge when available.
      - Example: `bluxq help build [OPTIONS]`
    - `bluxq help search` — Search help topics through the GOD bridge.
      - Example: `bluxq help search [OPTIONS] QUERY`
    - `bluxq help info` — Show detailed help for a specific topic.
      - Example: `bluxq help info [OPTIONS] TOPIC`
    - `bluxq help stats` — Display aggregated help statistics.
      - Example: `bluxq help stats [OPTIONS]`

- `bluxq lite` — Example BLUX Lite integration.
  - Example: `bluxq lite [OPTIONS] COMMAND [ARGS]...`
  - Subcommands:
    - `bluxq lite info` — Display lite module info.
      - Example: `bluxq lite info [OPTIONS]`
    - `bluxq lite activate` — Activate a lite profile.
      - Example: `bluxq lite activate [OPTIONS]`

<!-- END AUTO-GENERATED COMMANDS -->








## Config, logs, and audit
- **Config home:** defaults to `~/.config/blux-quantum` or `${BLUXQ_HOME}`/`${XDG_CONFIG_HOME}`
  if set. User config file: `<config_dir>/config.yaml`.
- **Audit log:** `<config_dir>/logs/audit.jsonl` (append-only; chain-verifiable via
  `bluxq key audit-verify`).
- **Telemetry:** JSONL at `<config_dir>/logs/audit.jsonl`, SQLite at
  `<config_dir>/logs/telemetry.db`. Disable with `BLUXQ_TELEMETRY=off`.
- **Demo artifacts:** `<config_dir>/demo/<target>-<timestamp>.json` from `bluxq demo <target>`.
- **Banner control:** set `BLUXQ_BANNER=off` to silence the startup banner in non-interactive
  environments.

## Plugin model
- Plugins are discovered through the `blux.plugins` entry-point group and mounted under their
  entry-point name.
- Bundled plugins shipped with this repo: `doctrine`, `guard`, and `lite`.
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
- System health: `bluxq system doctor`
- Lifecycle controls: `bluxq system bootstrap|status|up|down`
- Demo contract: `bluxq demo orchestrator` and `bluxq demo toolbox` (writes artifacts)
- Telemetry contract: `bluxq telemetry status|export|off`
- Help bridge: `bluxq help build|search|info|stats`

## Maintenance
- Format and lint: `make fmt` / `make lint`
- Tests: `make test`
- Regenerate README command reference: `make gen-readme`

## Support
Support / Contact: outervoid.blux@gmail.com
