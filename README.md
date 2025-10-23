# blux-quantum
bluq-cli

## Overview
BLUX Quantum (`bluxq`) is the unified operator cockpit for the BLUX ecosystem. It aggregates security, observability, and governance modules through a plugin model while delivering enterprise-ready tooling.

## Quick Start
```bash
pip install blux-quantum
bluxq --help
```

## Plugin Architecture
- Plugins register Typer apps via the `blux.plugins` entry-point group.
- The core CLI auto-discovers plugins and mounts them under their namespace.
- Example: `bluxq guard status` invokes the Guard plugin's status command.

### External Plugin Example
Add the following to a plugin package's `pyproject.toml`:
```toml
[project.entry-points."blux.plugins"]
guard = "blux_guard.cli:get_app"
```

## Stability & Telemetry
- Toggle stability mode: `bluxq stability enable` / `disable`.
- Telemetry writes JSONL and SQLite logs under `~/.config/blux-quantum/logs/`.
- Disable telemetry with `BLUXQ_TELEMETRY=off`.

## Documentation
Enterprise runbooks live under `docs/` and are published via MkDocs Material.

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

## License
Licensed under the [Apache License 2.0](LICENSE).
