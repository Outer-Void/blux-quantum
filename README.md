# BLUX Quantum (bluxq)
BLUX Quantum (`bluxq`) is the unified command-line interface for the BLUX ecosystem. It delivers a local-first, auditable operator cockpit with plugin-driven extensions for security, governance, and orchestration.

## Installation
```bash
git clone https://github.com/Outer-Void/blux-quantum.git
cd blux-quantum
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Optional extras available during installation:

```bash
pip install -e .[dev]
```

## Quick Start
- Inspect the CLI:
  ```bash
  bluxq --help
  ```
- Print version information:
  ```bash
  bluxq version
  ```
- Show current environment facts:
  ```bash
  bluxq env
  ```
- Initialize the local BLUX home (keys/logs/state):
  ```bash
  bluxq system bootstrap
  ```
- Generate a signing key:
  ```bash
  bluxq key init --label default
  ```
- Route and preview a task without execution:
  ```bash
  bluxq route dry-run "Deploy staging stack"
  ```
- Run a task through the orchestrator:
  ```bash
  bluxq run "Apply database migrations"
  ```
- Toggle stability mode:
  ```bash
  bluxq stability enable
  ```
- Check telemetry configuration:
  ```bash
  bluxq telemetry status
  ```

## Full Command Reference
BLUX Quantum is built with Typer. Commands below are exactly what the current codebase exposes (core plus bundled plugins). Examples are copy/paste ready.

### Top-level commands
- `version` — Print version details.
  ```bash
  bluxq version
  ```
- `about` — Show BLUX Quantum about information.
  ```bash
  bluxq about
  ```
- `env` — Show environment details (add `--json` to export JSON).
  ```bash
  bluxq env --json
  ```
- `env-export` — Export environment data (default `dotenv` format).
  ```bash
  bluxq env-export --format dotenv
  ```
- `completion` — Emit shell completion script for `bash|zsh|fish`.
  ```bash
  bluxq completion bash > /tmp/bluxq.bash
  ```
- `launch` — Shortcut to bring the BLUX constellation up (calls `system up`).
  ```bash
  bluxq launch
  ```
- `aim` — Register a high-level intent for routing.
  ```bash
  bluxq aim "Prepare compliance evidence"
  ```
- `run` — Route and execute a task file or prompt.
  ```bash
  bluxq run "Backup production database"
  ```
- `eval` — Evaluate a completed task with optional JSON payload.
  ```bash
  bluxq eval "Backup production database" --result '{"status": "ok"}'
  ```
- `demo` — Return ready status for demo modules (`orchestrator|toolbox`).
  ```bash
  bluxq demo orchestrator
  ```
- `stability` — Enable or disable stability mode.
  ```bash
  bluxq stability disable
  ```
- `tui` — Launch the interactive Textual TUI (interactive session).
  ```bash
  bluxq tui
  ```

### `system` — Bootstrap and lifecycle helpers
```bash
bluxq system --help
```
- `bootstrap` — Prepare the BLUX home (keys/logs/state).
  ```bash
  bluxq system bootstrap
  ```
- `install` — Install constellation dependencies (stub).
  ```bash
  bluxq system install
  ```
- `doctor` — Run diagnostic checks (add `--json` for machine output).
  ```bash
  bluxq system doctor
  ```
- `status` — Summarize config path, keys, and discovered plugins.
  ```bash
  bluxq system status
  ```
- `up` / `down` / `update` / `repair` / `clean` — Protected lifecycle operations.
  ```bash
  bluxq system up
  bluxq system down
  bluxq system update
  bluxq system repair
  bluxq system clean
  ```
- `bootstrap-diagnostics` (hidden) — Emit extended diagnostics.
  ```bash
  bluxq system bootstrap-diagnostics --json
  ```

### `key` — Key management and signing
```bash
bluxq key --help
```
- `init` — Create a new key with an optional label.
  ```bash
  bluxq key init --label default
  ```
- `list` — Show all stored keys.
  ```bash
  bluxq key list
  ```
- `show <key_id>` — Display a specific key.
  ```bash
  bluxq key show <key_id>
  ```
- `rotate <key_id>` — Create a rotated key.
  ```bash
  bluxq key rotate <key_id>
  ```
- `revoke <key_id>` — Remove a key.
  ```bash
  bluxq key revoke <key_id>
  ```
- `sign manifest|diff <path>` — Sign a manifest or diff file.
  ```bash
  bluxq key sign manifest ./plan.json
  ```
- `verify manifest|diff <path> <signature>` — Verify a signature.
  ```bash
  bluxq key verify manifest ./plan.json <signature>
  ```
- `audit-verify` — Validate the audit chain stored on disk.
  ```bash
  bluxq key audit-verify
  ```

### `route` — Routing helpers
```bash
bluxq route --help
```
- `explain <task>` — Resolve routing plan for a task.
  ```bash
  bluxq route explain "Provision sandbox"
  ```
- `dry-run <task>` — Simulate routing without execution.
  ```bash
  bluxq route dry-run "Provision sandbox"
  ```

### `doctrine` — Bundled doctrine plugin
```bash
bluxq doctrine --help
```
- `schema` — Display doctrine schema version.
  ```bash
  bluxq doctrine schema
  ```
- `sync` — Synchronise doctrine data.
  ```bash
  bluxq doctrine sync --destination ledger
  ```

### `guard` — Bundled guard plugin
```bash
bluxq guard --help
```
- `status` — Show guard status.
  ```bash
  bluxq guard status
  ```
- `ping` — Ping the guard service.
  ```bash
  bluxq guard ping control-plane
  ```

### `lite` — Bundled lite plugin
```bash
bluxq lite --help
```
- `info` — Display lite module info.
  ```bash
  bluxq lite info
  ```
- `activate` — Activate a lite profile.
  ```bash
  bluxq lite activate default
  ```

### `telemetry` — Telemetry controls
```bash
bluxq telemetry --help
```
- `status` — Show telemetry configuration and storage paths.
  ```bash
  bluxq telemetry status
  ```
- `tail` — Placeholder tail of telemetry events.
  ```bash
  bluxq telemetry tail
  ```
- `export` — Export telemetry in `json|sqlite|md` formats.
  ```bash
  bluxq telemetry export --format sqlite
  ```
- `off` — Disable telemetry for the current session.
  ```bash
  BLUXQ_TELEMETRY=off bluxq telemetry status
  ```

### `help` — GOD bridge passthrough
```bash
bluxq help --help
```
- `build` — Generate help index in `console|md|html|json`.
  ```bash
  bluxq help build --format md --limit 20
  ```
- `search` — Search help topics (supports `--names-only`).
  ```bash
  bluxq help search guard
  ```
- `info` — Show details for a topic.
  ```bash
  bluxq help info system
  ```
- `stats` — Show aggregated help statistics.
  ```bash
  bluxq help stats
  ```

### Diagnostics (hidden)
- `diag self-check` — Run internal health checks.
  ```bash
  bluxq diag self-check
  ```
- `diag plugins` — List discovered plugins (table or `--json`).
  ```bash
  bluxq diag plugins --json
  ```

## Configuration
- **Config directory:** defaults to `~/.config/blux-quantum/` or `${BLUXQ_HOME}` if set. User config file: `config.yaml`.
- **Environment overrides:** any `BLUXQ_*` variable (except `BLUXQ_HOME`) is merged into config keys (lowercased).
- **Telemetry control:**
  - `BLUXQ_TELEMETRY=off` disables telemetry writes.
  - `BLUXQ_TELEMETRY_WARN=once|always` emits warnings when log persistence fails.
  - Telemetry JSONL: `<config_dir>/logs/audit.jsonl`; SQLite: `<config_dir>/logs/telemetry.db`.
- **Audit log:** CLI commands are recorded to `<config_dir>/logs/audit.jsonl` (chain-verifiable via `key audit-verify`).
- **Banner:** set `BLUXQ_BANNER=off` to suppress the startup banner.

## Plugin System
- Plugins are discovered via the `blux.plugins` entry-point group and mounted under their entry-point name.
- If no external plugins are installed, bundled defaults are mounted automatically:
  - `guard` → `blux_quantum.plugins.examples.guard_plugin:get_app`
  - `lite` → `blux_quantum.plugins.examples.lite_plugin:get_app`
  - `doctrine` → `blux_quantum.plugins.examples.doctrine_plugin:get_app`
- Minimal plugin skeleton:
  ```python
  import typer

  app = typer.Typer(help="My BLUX extension")

  @app.command()
  def status():
      print({"status": "ok"})

  def get_app():
      return app
  ```
  ```toml
  [project.entry-points."blux.plugins"]
  myplugin = "my_package.cli:get_app"
  ```

## Security and Trust
- Signing and verification are built into the `key` commands for manifests/diffs.
- All CLI invocations are audited with chainable hashes for tamper detection (`key audit-verify`).
- Protected operations (`system up/down/update/repair/clean`, `key rotate/revoke/sign/verify`, `guard quarantine`, etc.) enforce gating through the internal key store.

## Roadmap
Track future work in [docs/ROADMAP.md](docs/ROADMAP.md).

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for coding standards, testing requirements, and release guidelines.

## Licensing
BLUX Quantum is dual-licensed to balance open community use with commercial adoption:
- **Open Source:** Available under the [Apache License 2.0](LICENSE-APACHE), allowing permissive use, modification, and redistribution with proper notices and without warranty.
- **Commercial:** Business or monetized use beyond the Apache terms requires a separate commercial license described in [LICENSE-COMMERCIAL](LICENSE-COMMERCIAL).

For commercial licensing inquiries, contact: theoutervoid@outlook.com.

<!-- FILETREE:BEGIN -->
<!-- generated; do not edit manually -->
<details><summary><strong>Repository File Tree</strong> (click to expand)</summary>

```text
blux-quantum
├── .github
│   └── workflows
│       ├── ci.yml
│       ├── docs.yml
│       └── release.yml
├── .gitignore
├── .ruff.toml
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── blux_quantum
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── plugins
│   │   ├── __init__.py
│   │   ├── examples
│   │   │   ├── doctrine_plugin.py
│   │   │   ├── guard_plugin.py
│   │   │   └── lite_plugin.py
│   │   └── loader.py
│   ├── stability.py
│   └── telemetry.py
├── docs
│   ├── ARCHITECTURE.md
│   ├── CONFIGURATION.md
│   ├── INSTALL.md
│   ├── INTEGRATIONS.md
│   ├── OPERATIONS.md
│   ├── ROADMAP.md
│   ├── SECURITY.md
│   ├── TROUBLESHOOTING.md
│   └── index.md
├── mkdocs.yml
├── mypy.ini
├── pyproject.toml
├── pytest.ini
├── scripts
│   ├── demo_install_alias.ps1
│   ├── gen_filetree.py
│   └── update_readme_filetree.py
└── tests
    ├── test_cli.py
    ├── test_plugins.py
    └── test_telemetry.py
```

</details>
<!-- FILETREE:END -->

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for coding standards, testing requirements, and release guidelines.

## Licensing
BLUX Quantum is dual-licensed to balance open community use with commercial adoption:
- **Open Source:** Available under the [Apache License 2.0](LICENSE-APACHE), allowing permissive use, modification, and redistribution with proper notices and without warranty.
- **Commercial:** Business or monetized use beyond the Apache terms requires a separate commercial license described in [LICENSE-COMMERCIAL](LICENSE-COMMERCIAL).

For commercial licensing inquiries, contact: theoutervoid@outlook.com.
