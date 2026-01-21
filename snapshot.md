# Repository Snapshot

## 1) Metadata
- Repository name: blux-quantum
- Organization / owner: 
- Default branch (if detectable): work
- HEAD commit hash (if available): 04235283476a6aa9502f2f286395673112122c87
- Snapshot timestamp (UTC): 2026-01-21T07:59:06.039092Z
- Total file count (excluding directories): 73
- Short description: BLUX Quantum (`blux`)

## 2) Repository Tree
.github/
  workflows/
    ci.yml [text]
blux_quantum/
  plugins/
    quantum_framework/
      __init__.py [text]
      loader.py [text]
    __init__.py [text]
    loader.py [text]
  __init__.py [text]
  audit.py [text]
  cli.py [text]
  config.py [text]
  diagnostics.py [text]
  dispatch.py [text]
  envelope.py [text]
  environment.py [text]
  orchestrator.py [text]
  stability.py [text]
  telemetry.py [text]
  tui.py [text]
bq/
  __init__.py [text]
  cli.py [text]
bq_fsp/
  README.md [text]
  __init__.py [text]
  cli.py [text]
  ignore.py [text]
  pyproject.toml [text]
  rules.py [text]
  sarif.py [text]
  scanner.py [text]
docs/
  ARCHITECTURE.md [text]
  CONFIGURATION.md [text]
  INSTALL.md [text]
  INTEGRATIONS.md [text]
  OPERATIONS.md [text]
  PHYSICS.md [text]
  ROADMAP.md [text]
  ROLE.md [text]
  SECURITY.md [text]
  TROUBLESHOOTING.md [text]
  fsp.md [text]
  index.md [text]
scripts/
  bluxq [text]
  bq [text]
  demo_install_alias.ps1 [text]
  gen_filetree.py [text]
  generate_command_reference.py [text]
  physics_check.sh [text]
  physics_checks.py [text]
  physics_tests.sh [text]
  update_readme_filetree.py [text]
tests/
  conftest.py [text]
  test_cli.py [text]
  test_physics.py [text]
  test_plugins.py [text]
  test_reference_generator.py [text]
  test_role_contract.py [text]
  test_telemetry.py [text]
.gitignore [text]
.pre-commit-hooks.yaml [text]
.ruff.toml [text]
CHANGELOG.md [text]
CODE_OF_CONDUCT.md [text]
COMMERCIAL.md [text]
CONTRIBUTING.md [text]
LICENSE [text]
LICENSE-APACHE [text]
LICENSE-COMMERCIAL [text]
Makefile [text]
NOTICE [text]
README.md [text]
ROLE.md [text]
mkdocs.yml [text]
mypy.ini [text]
pyproject.toml [text]
pytest.ini [text]

## 3) FULL FILE CONTENTS (MANDATORY)

FILE: .github/workflows/ci.yml
Kind: text
Size: 672
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
name: CI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .[dev]
      - name: Ruff
        run: ruff check .
      - name: Mypy
        run: mypy blux_quantum
      - name: Physics tests
        run: scripts/physics_tests.sh

FILE: .gitignore
Kind: text
Size: 522
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# Gradle files
.gradle/
build/

# Local configuration file (sdk path, etc)
local.properties

# Log/OS Files
*.log

# Android Studio generated files and folders
captures/
.externalNativeBuild/
.cxx/
*.aab
*.apk
output-metadata.json

# IntelliJ
*.iml
.idea/
misc.xml
deploymentTargetDropDown.xml
render.experimental.xml

# Keystore files
*.jks
*.keystore

# Google Services (e.g. APIs or Firebase)
google-services.json

# Android Profiling
*.hprof

# Python artifacts
__pycache__/
*.pyc
*.pyo
*.pyd
*.egg-info/
.eggs/
site/

FILE: .pre-commit-hooks.yaml
Kind: text
Size: 139
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
- id: bq-fsp-scan
  name: bq-fsp scan
  entry: bq-fsp scan --staged -f jsonl
  language: system
  pass_filenames: false
  stages: [commit]

FILE: .ruff.toml
Kind: text
Size: 101
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
target-version = "py39"
line-length = 100
select = ["E", "F", "I", "UP", "B", "A"]
ignore = ["B905"]

FILE: CHANGELOG.md
Kind: text
Size: 166
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# Changelog

## [0.1.0] - 2024-01-01
- Initial enterprise scaffold for BLUX Quantum CLI.
- Added plugin loader, telemetry, stability helpers, and documentation site.

FILE: CODE_OF_CONDUCT.md
Kind: text
Size: 609
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# Code of Conduct

BLUX Quantum follows the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct.

## Our Pledge
We pledge to foster an open, welcoming environment for contributors of all backgrounds and experience levels.

## Our Standards
Examples of positive behavior:
- Using inclusive and respectful language.
- Gracefully accepting constructive criticism.
- Focusing on what is best for the community.

## Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to `ops@blux.systems`. All complaints will be reviewed promptly and fairly.

FILE: COMMERCIAL.md
Kind: text
Size: 734
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# Commercial Licensing

BLUX Quantum is dual-licensed. You may use it under the open-source Apache License 2.0 in LICENSE-APACHE. Commercial use that goes beyond the Apache license requires a separate commercial agreement described in LICENSE-COMMERCIAL.

## When you need a commercial license
- Embedding BLUX Quantum into a paid product or service
- Offering hosted or managed versions of BLUX Quantum for customers
- Integrating BLUX Quantum into internal proprietary systems at scale where the deployment is not governed by the Apache License 2.0
- Any redistribution, sublicensing, or monetization that is not explicitly allowed under Apache-2.0

## Get in touch
For commercial licensing terms, contact: theoutervoid@outlook.com

FILE: CONTRIBUTING.md
Kind: text
Size: 733
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# Contributing

## Development Workflow
1. Create a virtual environment with Python 3.9+.
2. Install dependencies: `pip install -e .[dev]`.
3. Run format and lint checks: `ruff check .` and `mypy blux_quantum`.
4. Execute tests: `pytest`.

## Commit Guidelines
- Use descriptive commit messages (e.g., `[QUANTUM]` prefix for major changes).
- Include relevant documentation updates for new features.

## Pull Requests
- Ensure CI checks pass before requesting review.
- Update the README file tree via `python scripts/update_readme_filetree.py` when adding files.
- Provide context for telemetry or security-sensitive changes.

## Code Style
- Follow Ruff and Mypy guidance.
- Avoid broad exception handling without logging context.

FILE: LICENSE
Kind: text
Size: 258
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
This project is dual-licensed. Open-source use is provided under the Apache License 2.0 in LICENSE-APACHE. Commercial use requires a separate commercial license under LICENSE-COMMERCIAL.

For commercial licensing inquiries, contact: theoutervoid@outlook.com

FILE: LICENSE-APACHE
Kind: text
Size: 11357
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

FILE: LICENSE-COMMERCIAL
Kind: text
Size: 872
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
Proprietary Commercial License

Copyright (c) 2024 BLUX. All rights reserved.

Permission is granted to download and evaluate this software for internal review purposes only. Any other use, including without limitation commercial use, redistribution, modification, sublicensing, or hosting the software as a service, requires a separate commercial agreement with the copyright holder.

The software is provided "as is", without warranty of any kind, express or implied. In no event shall the authors or copyright holders be liable for any claim, damages or other liability arising from, out of, or in connection with the software or the use or other dealings in the software.

This license terminates automatically upon breach. Upon termination, you must cease all use and destroy all copies of the software.

To obtain commercial terms, contact: theoutervoid@outlook.com

FILE: Makefile
Kind: text
Size: 185
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
.PHONY: install test lint fmt gen-readme

install:
pip install -e .[dev]

test:
pytest

lint:
ruff check .

fmt:
ruff format .

gen-readme:
python scripts/generate_command_reference.py

FILE: NOTICE
Kind: text
Size: 88
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
BLUX Quantum
Copyright (c) 2024 BLUX

This product includes software developed by BLUX.

FILE: README.md
Kind: text
Size: 3789
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
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

FILE: ROLE.md
Kind: text
Size: 450
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# BLUX Quantum Role

BLUX Quantum is a dispatcher-only activator. It builds request envelopes, routes to cA,
calls Guard, and forwards receipts to Lite. It does not enforce permissions, decide
outcomes, or execute tools directly; it only dispatches and surfaces what will happen.

Non-capabilities: execution, enforcement, tokens, doctrine, discernment.

Routing chain: request → discernment_report → guard_receipt → lite execute (or dry-run).

FILE: blux_quantum/__init__.py
Kind: text
Size: 331
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""BLUX Quantum package initialization."""
from importlib.metadata import PackageNotFoundError, version

__all__ = ["__version__"]

try:  # pragma: no cover - fallback for editable installs
    __version__ = version("blux-quantum")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"

FILE: blux_quantum/audit.py
Kind: text
Size: 2119
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Append-only JSONL audit logging for bluxq commands."""
from __future__ import annotations

import getpass
import hashlib
import json
import os
import socket
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def audit_log_path() -> Path:
    """Return the audit log path (configurable via BLUXQ_HOME/XDG_CONFIG_HOME)."""

    base_home = os.environ.get("BLUXQ_HOME") or os.environ.get("XDG_CONFIG_HOME")
    if base_home:
        return Path(base_home) / "blux-quantum" / "logs" / "audit.jsonl"
    return Path.home() / ".config" / "blux-quantum" / "logs" / "audit.jsonl"


def _last_line_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        last_line = path.read_text(encoding="utf-8").splitlines()[-1]
    except (OSError, IndexError):
        return None
    if not last_line:
        return None
    return hashlib.sha256(last_line.encode("utf-8")).hexdigest()


def append_event(event: Dict[str, Any]) -> Path:
    """Append an audit event to the JSONL log and return the path."""

    path = audit_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    event.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    event.setdefault("user", getpass.getuser())
    event.setdefault("host", socket.gethostname())
    event.setdefault("cwd", str(Path.cwd()))
    event.setdefault("trace_id", uuid.uuid4().hex)
    event.setdefault("prev_audit_sha256", _last_line_hash(path))
    with path.open("a", encoding="utf-8") as handle:
        json.dump(event, handle, ensure_ascii=False)
        handle.write("\n")
    return path


def audit_command(cmd: str, args: Dict[str, Any] | None, outcome: str, duration_ms: int, trace_id: str) -> None:
    """Helper to write a structured audit event for a CLI command."""

    payload: Dict[str, Any] = {
        "cmd": cmd,
        "args": args or {},
        "outcome": outcome,
        "duration_ms": duration_ms,
        "trace_id": trace_id,
    }
    append_event(payload)


__all__ = ["append_event", "audit_command", "audit_log_path"]

FILE: blux_quantum/cli.py
Kind: text
Size: 11058
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""BLUX Quantum router CLI."""
from __future__ import annotations

import json
import os
import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import typer

from .audit import audit_command
from .envelope import (
    DISCERNMENT_SCHEMA,
    GUARD_RECEIPT_SCHEMA,
    EnvelopeSource,
    REQUEST_SCHEMA,
    create_envelope,
)
from .environment import detect_environment

app = typer.Typer(help="BLUX Quantum — dispatcher-only activator")

ALLOW_DECISIONS = {"ALLOW", "WARN"}


class RouterError(RuntimeError):
    pass


@dataclass
class ChainResult:
    trace_id: str
    artifacts: list[Path]
    request: Dict[str, Any]
    discernment_report: Dict[str, Any] | None = None
    guard_receipt: Dict[str, Any] | None = None
    lite_receipt: Dict[str, Any] | None = None
    execution_manifest: str | None = None


def _source(component: str) -> EnvelopeSource:
    instance = os.environ.get("BLUXQ_INSTANCE") or os.environ.get("HOSTNAME") or "local"
    return EnvelopeSource(repo="blux-quantum", component=component, instance=instance)


def _default_out_dir() -> Path:
    env = detect_environment()
    out_dir = env.config_dir / "artifacts" / "router"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def _emit_json(payload: Dict[str, Any]) -> None:
    typer.echo(json.dumps(payload, indent=2))


def _persist_artifacts(envelopes: list[Dict[str, Any]], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[Path] = []
    for index, envelope in enumerate(envelopes, start=1):
        name = f"{index:02d}-{envelope['type']}-{envelope['trace_id']}.json"
        path = out_dir / name
        path.write_text(json.dumps(envelope, indent=2), encoding="utf-8")
        artifacts.append(path)
    return artifacts


def _invoke_component(component: str, envelope: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if component == "ca":
            result = subprocess.run(
                ["blux-ca"],
                input=json.dumps(envelope),
                text=True,
                capture_output=True,
                check=True,
            )
        elif component == "guard":
            result = subprocess.run(
                ["blux-guard"],
                input=json.dumps(envelope),
                text=True,
                capture_output=True,
                check=True,
            )
        elif component == "lite":
            result = subprocess.run(
                ["blux-lite"],
                input=json.dumps(envelope),
                text=True,
                capture_output=True,
                check=True,
            )
        else:
            raise RouterError(f"Unknown component '{component}'")
    except FileNotFoundError as exc:
        raise RouterError(f"Missing component command: {component}") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or "component execution failed"
        raise RouterError(message) from exc
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RouterError("Component output was not JSON") from exc


def _extract_decision(report: Dict[str, Any]) -> tuple[str | None, float | None, str | None]:
    payload = report.get("payload") if isinstance(report, dict) else None
    if not isinstance(payload, dict):
        return None, None, None
    band = payload.get("decision_band") or payload.get("band")
    score = payload.get("decision_score") or payload.get("score")
    manifest = payload.get("execution_manifest")
    return band, score, manifest


def _extract_receipt_decision(receipt: Dict[str, Any]) -> str | None:
    payload = receipt.get("payload") if isinstance(receipt, dict) else None
    if not isinstance(payload, dict):
        return None
    return payload.get("decision")


def _assert_uuid(value: str, label: str) -> None:
    try:
        uuid.UUID(value)
    except (ValueError, TypeError) as exc:
        raise RouterError(f"{label} must be a UUID") from exc


def _validate_envelope(envelope: Dict[str, Any], expected_type: str | None = None) -> Dict[str, Any]:
    if expected_type and envelope.get("type") != expected_type:
        raise RouterError(f"Expected {expected_type} envelope")
    for field in ("trace_id", "span_id", "timestamp", "source", "payload"):
        if field not in envelope:
            raise RouterError(f"Envelope missing {field}")
    _assert_uuid(envelope.get("trace_id"), "trace_id")
    _assert_uuid(envelope.get("span_id"), "span_id")
    source = envelope.get("source")
    if not isinstance(source, dict) or not {"repo", "component", "instance"}.issubset(source.keys()):
        raise RouterError("Envelope source must include repo, component, and instance")
    if envelope.get("type") == "discernment_report" and not envelope.get("payload_schema"):
        envelope["payload_schema"] = DISCERNMENT_SCHEMA
    if envelope.get("type") == "guard_receipt" and not envelope.get("payload_schema"):
        envelope["payload_schema"] = GUARD_RECEIPT_SCHEMA
    return envelope


def _emit_audit_preview(result: ChainResult) -> None:
    band, score, manifest = _extract_decision(result.discernment_report or {})
    receipt_decision = _extract_receipt_decision(result.guard_receipt or {})
    preview = {
        "trace_id": result.trace_id,
        "artifacts": [str(path) for path in result.artifacts],
        "decision_band": band,
        "decision_score": score,
        "receipt_decision": receipt_decision,
        "execution_manifest": manifest or result.execution_manifest,
    }
    _emit_json({"audit_preview": preview})


def _build_request(task: str, trace_id: str) -> Dict[str, Any]:
    return create_envelope(
        "request",
        {"text": task},
        source=_source("quantum"),
        trace_id=trace_id,
        payload_schema=REQUEST_SCHEMA,
    )


def _build_guard_request(
    request: Dict[str, Any],
    report: Dict[str, Any],
    trace_id: str,
) -> Dict[str, Any]:
    return create_envelope(
        "guard_request",
        {"request": request, "discernment_report": report},
        source=_source("quantum"),
        trace_id=trace_id,
    )


def _build_lite_request(
    request: Dict[str, Any],
    receipt: Dict[str, Any],
    trace_id: str,
) -> Dict[str, Any]:
    return create_envelope(
        "lite_request",
        {"request": request, "guard_receipt": receipt},
        source=_source("quantum"),
        trace_id=trace_id,
    )


def _route_chain(task: str, include_lite: bool, out_dir: Path) -> ChainResult:
    trace_id = str(uuid.uuid4())
    request = _build_request(task, trace_id)
    envelopes: list[Dict[str, Any]] = [request]

    report = _validate_envelope(_invoke_component("ca", request), expected_type="discernment_report")
    envelopes.append(report)
    guard_request = _build_guard_request(request, report, trace_id)
    envelopes.append(guard_request)
    guard_receipt = _validate_envelope(_invoke_component("guard", guard_request), expected_type="guard_receipt")
    envelopes.append(guard_receipt)

    if include_lite:
        if not guard_receipt:
            raise RouterError("Guard receipt required before invoking Lite")
        decision = _extract_receipt_decision(guard_receipt)
        if decision == "REQUIRE_CONFIRM":
            artifacts = _persist_artifacts(envelopes, out_dir)
            result = ChainResult(trace_id=trace_id, artifacts=artifacts, request=request, discernment_report=report, guard_receipt=guard_receipt)
            _emit_audit_preview(result)
            raise typer.Exit(code=2)
        if decision == "BLOCK":
            artifacts = _persist_artifacts(envelopes, out_dir)
            result = ChainResult(trace_id=trace_id, artifacts=artifacts, request=request, discernment_report=report, guard_receipt=guard_receipt)
            _emit_audit_preview(result)
            raise typer.Exit(code=3)
        if decision and decision not in ALLOW_DECISIONS:
            raise RouterError(f"Unsupported receipt decision: {decision}")
        lite_request = _build_lite_request(request, guard_receipt, trace_id)
        envelopes.append(lite_request)
        lite_receipt = _validate_envelope(_invoke_component("lite", lite_request))
        envelopes.append(lite_receipt)
    else:
        lite_receipt = None

    artifacts = _persist_artifacts(envelopes, out_dir)
    return ChainResult(
        trace_id=trace_id,
        artifacts=artifacts,
        request=request,
        discernment_report=report,
        guard_receipt=guard_receipt,
        lite_receipt=lite_receipt,
    )


def _audit(cmd: str, args: Dict[str, Any], outcome: str) -> None:
    audit_command(cmd, args, outcome, 0, str(uuid.uuid4()))


@app.command("request")
def request(task: str = typer.Argument(..., help="Request text"), out_dir: Path | None = typer.Option(None, "--out-dir")) -> None:
    """Create a request envelope."""

    trace_id = str(uuid.uuid4())
    envelope = _build_request(task, trace_id)
    _emit_json(envelope)
    artifacts = _persist_artifacts([envelope], out_dir or _default_out_dir())
    _emit_json({"trace_id": trace_id, "artifacts": [str(path) for path in artifacts]})
    _audit("request", {"task": task}, "ok")


@app.command("inspect")
def inspect(artifact: Path = typer.Argument(..., help="Artifact JSON path")) -> None:
    """Print a stored artifact."""

    payload = json.loads(artifact.read_text(encoding="utf-8"))
    _emit_json(payload)
    _audit("inspect", {"artifact": str(artifact)}, "ok")


@app.command("dry-run")
def dry_run(task: str = typer.Argument(..., help="Request text"), out_dir: Path | None = typer.Option(None, "--out-dir")) -> None:
    """Route through cA and Guard without invoking Lite."""
    try:
        result = _route_chain(task, include_lite=False, out_dir=out_dir or _default_out_dir())
    except RouterError as exc:
        _audit("dry-run", {"task": task}, "error")
        raise typer.Exit(code=1, message=str(exc))
    for envelope in [result.request, result.discernment_report, result.guard_receipt]:
        if envelope:
            _emit_json(envelope)
    _emit_audit_preview(result)
    _audit("dry-run", {"task": task}, "ok")


@app.command("run")
def run(task: str = typer.Argument(..., help="Request text"), out_dir: Path | None = typer.Option(None, "--out-dir")) -> None:
    """Route through cA, Guard, and Lite with receipt enforcement."""

    try:
        result = _route_chain(task, include_lite=True, out_dir=out_dir or _default_out_dir())
    except RouterError as exc:
        _audit("run", {"task": task}, "error")
        raise typer.Exit(code=1, message=str(exc))
    for envelope in [
        result.request,
        result.discernment_report,
        result.guard_receipt,
        result.lite_receipt,
    ]:
        if envelope:
            _emit_json(envelope)
    _emit_audit_preview(result)
    _audit("run", {"task": task}, "ok")


if __name__ == "__main__":  # pragma: no cover
    app()

FILE: blux_quantum/config.py
Kind: text
Size: 2015
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Configuration loading utilities for BLUX Quantum."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml

BLUXQ_HOME_ENV = "BLUXQ_HOME"
CONFIG_FILENAME = "config.yaml"
DEFAULT_NAMESPACE = "blux-quantum"


def _default_config_dir() -> Path:
    base = os.environ.get(BLUXQ_HOME_ENV)
    if base:
        return Path(base).expanduser().resolve()
    return Path.home() / ".config" / DEFAULT_NAMESPACE


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
            if not isinstance(data, dict):
                return {}
            return data
    except (OSError, yaml.YAMLError):
        return {}


def _merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = _merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Load configuration using the documented search order."""
    config: Dict[str, Any] = {}

    env_config = {
        key[7:].lower(): value
        for key, value in os.environ.items()
        if key.startswith("BLUXQ_") and key not in {BLUXQ_HOME_ENV}
    }
    if env_config:
        config = _merge_dicts(config, env_config)

    user_config_dir = _default_config_dir()
    config = _merge_dicts(config, _load_yaml(user_config_dir / CONFIG_FILENAME))

    local_config = Path.cwd() / CONFIG_FILENAME
    config = _merge_dicts(config, _load_yaml(local_config))

    if extra:
        config = _merge_dicts(config, extra)

    return config


__all__ = ["load_config", "BLUXQ_HOME_ENV", "CONFIG_FILENAME"]

FILE: blux_quantum/diagnostics.py
Kind: text
Size: 5608
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Diagnostics utilities surfaced via the CLI."""
from __future__ import annotations

import importlib
import json
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from rich.table import Table

from .environment import detect_environment
from .plugins.quantum_framework.loader import discover_plugins
from .stability import stability_status
from .telemetry import telemetry_status


def _command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def _check_writable(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        sentinel = path / ".write_test"
        sentinel.write_text("ok", encoding="utf-8")
        sentinel.unlink(missing_ok=True)
        return True
    except OSError:
        return False


def collect_diagnostics() -> Dict[str, Any]:
    env = detect_environment()
    plugins = discover_plugins()
    telemetry = telemetry_status()

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": env.as_dict(),
        "plugins": [plugin.__dict__ for plugin in plugins],
        "telemetry": telemetry,
        "stability": stability_status(),
        "executables": {
            "python": _command_exists("python"),
            "python3": _command_exists("python3"),
            "pip": _command_exists("pip"),
            "ssh": _command_exists("ssh"),
            "sqlite3": _command_exists("sqlite3"),
        },
    }


def render_diagnostics_table(payload: Dict[str, Any]) -> Table:
    table = Table(title="BLUX Quantum Diagnostics", show_lines=True)
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Details", style="magenta")

    environment = payload.get("environment", {})
    env_lines = [f"{key}: {value}" for key, value in environment.items()]
    table.add_row("Environment", "\n".join(env_lines))

    execs = payload.get("executables", {})
    exec_lines = [f"{key}: {'yes' if value else 'no'}" for key, value in execs.items()]
    table.add_row("Executables", "\n".join(exec_lines))

    telemetry = payload.get("telemetry", {})
    telemetry_lines = [f"{key}: {value}" for key, value in telemetry.items()]
    table.add_row("Telemetry", "\n".join(telemetry_lines))

    stability = payload.get("stability", {})
    stability_lines = [f"{key}: {value}" for key, value in stability.items()]
    table.add_row("Stability", "\n".join(stability_lines))

    plugins: List[Dict[str, Any]] = payload.get("plugins", [])
    if not plugins:
        table.add_row("Plugins", "None detected")
    else:
        plugin_lines = [f"{plugin['name']}: {'loaded' if plugin['loaded'] else 'error'}" for plugin in plugins]
        table.add_row("Plugins", "\n".join(plugin_lines))

    checks = payload.get("checks", [])
    if checks:
        check_lines = [
            f"{check['name']}: {'ok' if check['ok'] else 'warn'} ({check['detail']})"
            for check in checks
        ]
        table.add_row("Checks", "\n".join(check_lines))

    return table


def diagnose() -> Dict[str, Any]:
    return collect_diagnostics()


def doctor() -> Dict[str, Any]:
    payload = collect_diagnostics()
    recommendations: List[str] = []
    checks: List[Dict[str, Any]] = []

    execs = payload.get("executables", {})
    for binary, available in execs.items():
        if not available:
            recommendations.append(f"Install '{binary}' via your package manager for richer features.")

    env = detect_environment()
    python_ok = sys.version_info >= (3, 9)
    checks.append(
        {
            "name": "python_version",
            "ok": python_ok,
            "detail": f"running {platform.python_version()} (requires >=3.9)",
        }
    )
    if not python_ok:
        recommendations.append("Upgrade Python to >=3.9 for full support.")

    config_ok = _check_writable(env.config_dir)
    checks.append(
        {
            "name": "config_dir",
            "ok": config_ok,
            "detail": f"{env.config_dir}",
        }
    )
    if not config_ok:
        recommendations.append(f"Config directory is not writable: {env.config_dir}")

    imports_ok = True
    import_errors: list[str] = []
    for module in ["blux_quantum", "blux_quantum.cli"]:
        try:
            importlib.import_module(module)
        except Exception as exc:  # pragma: no cover - defensive
            imports_ok = False
            import_errors.append(f"{module}: {exc}")
    checks.append(
        {
            "name": "core_imports",
            "ok": imports_ok,
            "detail": "; ".join(import_errors) if import_errors else "ok",
        }
    )
    if not imports_ok:
        recommendations.append("Core modules failed to import; check installation.")

    telemetry = payload.get("telemetry", {})
    if not telemetry.get("enabled", False):
        recommendations.append("Telemetry disabled — insights may be limited.")

    plugins = payload.get("plugins", [])
    if not any(plugin.get("loaded") for plugin in plugins):
        recommendations.append("No plugins loaded. Install extras or check entry-points.")

    checks.append(
        {
            "name": "plugins",
            "ok": any(plugin.get("loaded") for plugin in plugins),
            "detail": f"{len(plugins)} discovered",
        }
    )

    payload["recommendations"] = recommendations
    payload["recommendations_json"] = json.dumps(recommendations)
    payload["checks"] = checks
    return payload


__all__ = ["diagnose", "doctor", "render_diagnostics_table"]

FILE: blux_quantum/dispatch.py
Kind: text
Size: 125
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Dispatcher alias for the BLUX Quantum CLI."""
from __future__ import annotations

from .cli import app

__all__ = ["app"]

FILE: blux_quantum/envelope.py
Kind: text
Size: 2090
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Phase 0 envelope helpers for BLUX Quantum."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import os
import socket
import uuid
from typing import Any, Dict


ENVELOPE_SCHEMA = "blux://contracts/envelope.schema.json"
REQUEST_SCHEMA = "blux://contracts/request.schema.json"
DISCERNMENT_SCHEMA = "blux://contracts/discernment_report.schema.json"
GUARD_RECEIPT_SCHEMA = "blux://contracts/guard_receipt.schema.json"

PAYLOAD_SCHEMAS = {
    "request": REQUEST_SCHEMA,
    "discernment_report": DISCERNMENT_SCHEMA,
    "guard_receipt": GUARD_RECEIPT_SCHEMA,
}


@dataclass(frozen=True)
class EnvelopeSource:
    repo: str
    component: str
    instance: str

    def as_dict(self) -> Dict[str, str]:
        return {"repo": self.repo, "component": self.component, "instance": self.instance}


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_instance() -> str:
    return os.environ.get("BLUXQ_INSTANCE") or socket.gethostname()


def create_envelope(
    envelope_type: str,
    payload: Dict[str, Any],
    *,
    source: EnvelopeSource,
    trace_id: str | None = None,
    span_id: str | None = None,
    payload_schema: str | None = None,
) -> Dict[str, Any]:
    """Create a Phase 0 envelope payload."""

    if "capability_ref" in payload and not isinstance(payload["capability_ref"], str):
        raise ValueError("capability_ref must be a string")
    resolved_payload_schema = payload_schema or PAYLOAD_SCHEMAS.get(envelope_type)
    return {
        "schema": ENVELOPE_SCHEMA,
        "envelope_id": str(uuid.uuid4()),
        "type": envelope_type,
        "timestamp": _utc_timestamp(),
        "source": source.as_dict(),
        "trace_id": trace_id or str(uuid.uuid4()),
        "span_id": span_id or str(uuid.uuid4()),
        "payload_schema": resolved_payload_schema,
        "payload": payload,
    }


__all__ = [
    "ENVELOPE_SCHEMA",
    "REQUEST_SCHEMA",
    "DISCERNMENT_SCHEMA",
    "GUARD_RECEIPT_SCHEMA",
    "EnvelopeSource",
    "create_envelope",
]

FILE: blux_quantum/environment.py
Kind: text
Size: 2825
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Runtime environment detection helpers for BLUX Quantum."""
from __future__ import annotations

import os
import platform
import shutil
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict


@dataclass(frozen=True)
class EnvironmentSummary:
    """A structured summary about the execution environment."""

    os_family: str
    os_release: str
    python: str
    architecture: str
    shell: str
    term: str
    is_termux: bool
    is_wsl: bool
    is_macos: bool
    is_debian: bool
    config_dir: Path

    def as_dict(self) -> Dict[str, str | bool]:
        return {
            "os_family": self.os_family,
            "os_release": self.os_release,
            "python": self.python,
            "architecture": self.architecture,
            "shell": self.shell,
            "term": self.term,
            "is_termux": self.is_termux,
            "is_wsl": self.is_wsl,
            "is_macos": self.is_macos,
            "is_debian": self.is_debian,
            "config_dir": str(self.config_dir),
        }


def _detect_termux() -> bool:
    return "com.termux" in os.environ.get("PREFIX", "") or Path("/data/data/com.termux").exists()


def _detect_wsl() -> bool:
    try:
        with open("/proc/version", "r", encoding="utf-8") as handle:
            return "Microsoft" in handle.read()
    except OSError:
        return False


def _detect_shell() -> str:
    shell = os.environ.get("SHELL") or os.environ.get("COMSPEC")
    if not shell:
        return "unknown"
    return Path(shell).name


def _detect_term() -> str:
    term = os.environ.get("TERM") or os.environ.get("WT_SESSION")
    return term or "unknown"


def _config_dir() -> Path:
    xdg_home = os.environ.get("BLUXQ_HOME") or os.environ.get("XDG_CONFIG_HOME")
    if xdg_home:
        return Path(xdg_home) / "blux-quantum"
    return Path.home() / ".config" / "blux-quantum"


@lru_cache(maxsize=1)
def detect_environment() -> EnvironmentSummary:
    """Collect operating-system facts for banner/diagnostics output."""

    os_family = platform.system()
    os_release = platform.release()
    is_macos = os_family.lower() == "darwin"
    is_termux = _detect_termux()
    is_wsl = _detect_wsl()
    is_debian = shutil.which("apt") is not None and os.path.exists("/etc/debian_version")

    return EnvironmentSummary(
        os_family=os_family,
        os_release=os_release,
        python=f"{platform.python_version()} ({sys.executable})",
        architecture=" ".join(platform.architecture()),
        shell=_detect_shell(),
        term=_detect_term(),
        is_termux=is_termux,
        is_wsl=is_wsl,
        is_macos=is_macos,
        is_debian=is_debian,
        config_dir=_config_dir(),
    )


__all__ = ["EnvironmentSummary", "detect_environment"]

FILE: blux_quantum/orchestrator.py
Kind: text
Size: 3042
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Quantum task orchestration primitives for CLI commands."""
from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence

from .plugins.quantum_framework.loader import PluginInfo, discover_plugins


class OrchestrationError(RuntimeError):
    """Raised when routing or evaluation fails."""


@dataclass
class RouteDecision:
    task: str
    route: str
    confidence: float
    reasoning: str
    plugin_candidates: Sequence[str]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "route": self.route,
            "confidence": round(self.confidence, 2),
            "reasoning": self.reasoning,
            "plugin_candidates": list(self.plugin_candidates),
        }


def _plugin_candidates(task: str, plugins: Iterable[PluginInfo]) -> List[str]:
    candidates: List[str] = []
    lowered = task.lower()
    for plugin in plugins:
        if not plugin.loaded:
            continue
        if plugin.name in lowered:
            candidates.append(plugin.name)
        elif any(keyword in lowered for keyword in plugin.name.split("-")):
            candidates.append(plugin.name)
    return candidates


def route_task(task: str, context: Dict[str, Any] | None = None) -> RouteDecision:
    if not task.strip():
        raise OrchestrationError("Task description required for routing")

    plugins = discover_plugins()
    loaded_plugins = [plugin for plugin in plugins if plugin.loaded]
    if not loaded_plugins:
        raise OrchestrationError("No plugins available to route task")

    candidates = _plugin_candidates(task, loaded_plugins)
    if not candidates:
        candidates = [loaded_plugins[0].name]

    preferred = candidates[0]
    confidence = 0.6 + 0.4 * random.random()
    reasoning = "Matched plugin keyword" if candidates else "Defaulted to first available plugin"
    if context:
        reasoning += f"; context keys: {', '.join(sorted(context.keys()))}"

    return RouteDecision(task=task, route=preferred, confidence=confidence, reasoning=reasoning, plugin_candidates=candidates)


def evaluate_task(task: str, result: Dict[str, Any] | None = None) -> Dict[str, Any]:
    if not task.strip():
        raise OrchestrationError("Task description required for evaluation")

    result_payload = result or {}
    score = 0.8 if result_payload else 0.5
    feedback = "Result received" if result_payload else "No result payload provided"

    return {
        "task": task,
        "score": round(score, 2),
        "feedback": feedback,
        "result_echo": result_payload,
    }


def parse_context(context: str | None) -> Dict[str, Any]:
    if not context:
        return {}
    try:
        return json.loads(context)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise OrchestrationError(f"Invalid JSON context: {exc}") from exc


__all__ = ["OrchestrationError", "RouteDecision", "route_task", "evaluate_task", "parse_context"]

FILE: blux_quantum/plugins/__init__.py
Kind: text
Size: 186
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Plugin subsystem for BLUX Quantum."""
from .quantum_framework.loader import PluginInfo, discover_plugins, mount_plugins

__all__ = ["PluginInfo", "discover_plugins", "mount_plugins"]

FILE: blux_quantum/plugins/loader.py
Kind: text
Size: 419
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Compatibility wrapper for the relocated plugin loader."""
from __future__ import annotations

import warnings

from .quantum_framework.loader import PluginInfo, discover_plugins, mount_plugins

warnings.warn(
    "blux_quantum.plugins.loader is deprecated; use blux_quantum.plugins.quantum_framework.loader",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["PluginInfo", "discover_plugins", "mount_plugins"]

FILE: blux_quantum/plugins/quantum_framework/__init__.py
Kind: text
Size: 170
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Quantum framework plugin namespace."""

from .loader import PluginInfo, discover_plugins, mount_plugins

__all__ = ["PluginInfo", "discover_plugins", "mount_plugins"]

FILE: blux_quantum/plugins/quantum_framework/loader.py
Kind: text
Size: 2781
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Plugin discovery for the Quantum framework namespace."""
from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import List

import typer
from importlib import metadata
from rich import print

DEFAULT_PLUGINS: dict[str, str] = {}


@dataclass
class PluginInfo:
    name: str
    app_factory: str
    loaded: bool
    error: str | None = None


def _iter_entry_points() -> List[metadata.EntryPoint]:
    entries: List[metadata.EntryPoint] = []
    try:
        entry_points = metadata.entry_points()
    except Exception:  # pragma: no cover - defensive fallback
        entry_points = ()
    if hasattr(entry_points, "select"):
        entries.extend(list(entry_points.select(group="blux.plugins")))
    else:
        entries.extend(list(entry_points.get("blux.plugins", [])))  # type: ignore[attr-defined]

    if not entries:
        for name, value in DEFAULT_PLUGINS.items():
            entries.append(metadata.EntryPoint(name=name, value=value, group="blux.plugins"))
    return entries


def _resolve_plugin(entry: metadata.EntryPoint) -> typer.Typer:
    module, _, attr = entry.value.partition(":")
    module_obj = importlib.import_module(module)
    plugin_obj = getattr(module_obj, attr) if attr else module_obj
    plugin_app = plugin_obj() if callable(plugin_obj) else plugin_obj
    if not isinstance(plugin_app, typer.Typer):
        raise TypeError("Plugin app must be a Typer application")
    return plugin_app


def discover_plugins() -> List[PluginInfo]:
    plugins: List[PluginInfo] = []
    for entry in _iter_entry_points():
        target = entry.value
        try:
            _resolve_plugin(entry)
            plugins.append(PluginInfo(name=entry.name, app_factory=target, loaded=True))
        except Exception as exc:  # pragma: no cover - defensive
            print(f"[blux] plugin '{entry.name}' failed to load: {exc}")
            plugins.append(
                PluginInfo(name=entry.name, app_factory=target, loaded=False, error=str(exc))
            )
    return plugins


def mount_plugins(app: typer.Typer) -> List[PluginInfo]:
    results: List[PluginInfo] = []
    for entry in _iter_entry_points():
        target = entry.value
        try:
            plugin_app = _resolve_plugin(entry)
            app.add_typer(plugin_app, name=entry.name)
            results.append(PluginInfo(name=entry.name, app_factory=target, loaded=True))
        except Exception as exc:  # pragma: no cover - defensive
            print(f"[blux] plugin '{entry.name}' failed to mount: {exc}")
            results.append(
                PluginInfo(name=entry.name, app_factory=target, loaded=False, error=str(exc))
            )
    return results


__all__ = ["PluginInfo", "discover_plugins", "mount_plugins"]

FILE: blux_quantum/stability.py
Kind: text
Size: 876
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Stability mode helpers for BLUX Quantum."""
from __future__ import annotations

import threading
from typing import Dict

from .telemetry import record_event

_lock = threading.Lock()
_enabled = False


def enable_stability(metadata: Dict[str, str] | None = None) -> bool:
    """Enable stability mode."""
    global _enabled
    with _lock:
        _enabled = True
    record_event("stability.enable", metadata or {})
    return _enabled


def disable_stability(metadata: Dict[str, str] | None = None) -> bool:
    """Disable stability mode."""
    global _enabled
    with _lock:
        _enabled = False
    record_event("stability.disable", metadata or {})
    return _enabled


def stability_status() -> Dict[str, bool]:
    with _lock:
        status = _enabled
    return {"enabled": status}


__all__ = ["enable_stability", "disable_stability", "stability_status"]

FILE: blux_quantum/telemetry.py
Kind: text
Size: 3651
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Best-effort telemetry writer for BLUX Quantum."""
from __future__ import annotations

import json
import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from prometheus_client import CollectorRegistry, Counter

from .config import BLUXQ_HOME_ENV, load_config

TELEMETRY_ENV = "BLUXQ_TELEMETRY"
TELEMETRY_WARN_ENV = "BLUXQ_TELEMETRY_WARN"
_LOG_DIR_NAME = "logs"
_JSONL_NAME = "audit.jsonl"
_SQLITE_NAME = "telemetry.db"

_registry = CollectorRegistry()
_events_counter = Counter(
    "bluxq_events_total",
    "Number of telemetry events recorded by BLUX Quantum.",
    ["event"],
    registry=_registry,
)
_warned_lock = threading.Lock()
_warned = False


def _telemetry_disabled() -> bool:
    return os.environ.get(TELEMETRY_ENV, "on").lower() in {"0", "false", "off"}


def _should_warn() -> bool:
    global _warned
    mode = os.environ.get(TELEMETRY_WARN_ENV, "never").lower()
    if mode not in {"once", "always"}:
        return False
    if mode == "always":
        return True
    with _warned_lock:
        if not _warned:
            _warned = True
            return True
    return False


def _log_dir() -> Path:
    config_dir = Path(os.environ.get(BLUXQ_HOME_ENV) or Path.home() / ".config" / "blux-quantum")
    return config_dir / _LOG_DIR_NAME


def telemetry_status() -> Dict[str, Any]:
    log_dir = _log_dir()
    jsonl_path = log_dir / _JSONL_NAME
    sqlite_path = log_dir / _SQLITE_NAME
    return {
        "enabled": not _telemetry_disabled(),
        "log_path": str(jsonl_path),
        "sqlite_path": str(sqlite_path),
    }


def _ensure_log_dir(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError:
        if _should_warn():
            print("[bluxq] telemetry log directory unavailable; continuing without persistence")


def _write_jsonl(path: Path, payload: Dict[str, Any]) -> None:
    try:
        with path.open("a", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False)
            handle.write("\n")
    except OSError:
        if _should_warn():
            print("[bluxq] telemetry JSONL write failed; continuing")


def _write_sqlite(path: Path, payload: Dict[str, Any]) -> None:
    try:
        conn = sqlite3.connect(path)
        try:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS events (timestamp TEXT, name TEXT, payload TEXT)"
            )
            conn.execute(
                "INSERT INTO events (timestamp, name, payload) VALUES (?, ?, ?)",
                (payload["timestamp"], payload["event"], json.dumps(payload.get("payload", {}))),
            )
            conn.commit()
        finally:
            conn.close()
    except sqlite3.Error:
        if _should_warn():
            print("[bluxq] telemetry SQLite write failed; continuing")


def record_event(event: str, payload: Dict[str, Any] | None = None) -> bool:
    if _telemetry_disabled():
        return False

    timestamp = datetime.now(timezone.utc).isoformat()
    entry = {
        "timestamp": timestamp,
        "event": event,
        "payload": payload or {},
        "config": load_config(),
    }

    log_dir = _log_dir()
    _ensure_log_dir(log_dir)

    jsonl_path = log_dir / _JSONL_NAME
    sqlite_path = log_dir / _SQLITE_NAME

    _write_jsonl(jsonl_path, entry)
    _write_sqlite(sqlite_path, entry)

    try:
        _events_counter.labels(event=event).inc()
    except ValueError:
        _events_counter.labels(event="unknown").inc()

    return True


__all__ = ["record_event", "telemetry_status", "_registry"]

FILE: blux_quantum/tui.py
Kind: text
Size: 1539
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Textual TUI entrypoint for `bq tui`."""
from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header, Static

from .diagnostics import collect_diagnostics


class QuantumDashboard(App):
    CSS_PATH = None
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:  # pragma: no cover - UI code
        yield Header(show_clock=True)
        self._summary = Static(id="summary")
        yield Container(self._summary)
        yield Footer()

    def on_mount(self) -> None:  # pragma: no cover - UI code
        self.refresh_summary()

    def action_refresh(self) -> None:  # pragma: no cover - UI code
        self.refresh_summary()

    def refresh_summary(self) -> None:  # pragma: no cover - UI code
        diag = collect_diagnostics()
        lines = ["BLUX Quantum — Live Diagnostics", ""]
        env = diag.get("environment", {})
        for key, value in env.items():
            lines.append(f"{key}: {value}")
        lines.append("")
        lines.append("Plugins:")
        for plugin in diag.get("plugins", []):
            status = "loaded" if plugin.get("loaded") else f"error ({plugin.get('error', 'unknown')})"
            lines.append(f"- {plugin.get('name')}: {status}")
        self._summary.update("\n".join(lines))


def run() -> None:
    QuantumDashboard().run()  # pragma: no cover - UI code


__all__ = ["run", "QuantumDashboard"]

FILE: bq/__init__.py
Kind: text
Size: 113
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Lightweight namespace for the BLUX Quantum CLI shim."""
from __future__ import annotations

__all__ = ["cli"]

FILE: bq/cli.py
Kind: text
Size: 1012
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Standalone shim for the BLUX Quantum CLI with optional security plugin."""
from __future__ import annotations

import os
import pathlib
from typing import Any

from blux_quantum.cli import app as _app


def _mount_optional_fsp(app: Any) -> None:
    """Mount the optional bq-fsp plugin if it is importable."""
    try:
        import bq_fsp.cli as fsp_cli
    except ImportError:  # pragma: no cover - optional dependency
        return
    register = getattr(fsp_cli, "register", None)
    if callable(register):
        register(app)


def default_fsp_log() -> str:
    """Resolve the default JSONL log path for bq-fsp output."""
    override = os.environ.get("FSP_LOG")
    if override:
        return override
    path = pathlib.Path.home() / ".config" / "blux-lite-gold" / "logs" / "fsp.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


app = _app

# Mount optional security scanner as `bq fsp` if installed.
_mount_optional_fsp(app)


__all__ = ["app", "default_fsp_log"]

FILE: bq_fsp/README.md
Kind: text
Size: 405
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# bq-fsp — Find Suspicious Patterns

Fast regex/heuristic scanner for security patterns in code. Part of BLUX Quantum.

## Usage
```bash
bq fsp scan .                     # table view
bq fsp scan . --staged -f jsonl  # append to default JSONL log
bq fsp scan . -f sarif -o out.sarif
```

**Default log path:** `~/.config/blux-lite-gold/logs/fsp.jsonl`

Install plugin: `pip install bq-fsp`

_(( • ))_

FILE: bq_fsp/__init__.py
Kind: text
Size: 156
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""bq-fsp plugin package."""
from __future__ import annotations

__all__ = ["__version__", "__author__"]

__version__ = "0.1.0"
__author__ = "BLUX Quantum"

FILE: bq_fsp/cli.py
Kind: text
Size: 4258
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Typer entry-point for the bq-fsp plugin."""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

import typer
from rich.console import Console
from rich.table import Table

from .rules import load_rules
from .sarif import to_sarif
from .scanner import Finding, scan

console = Console()
app = typer.Typer(name="bq-fsp", help="BLUX Quantum — Find Suspicious Patterns")


def _default_log_path() -> str | None:
    try:
        from bq.cli import default_fsp_log
    except Exception:  # pragma: no cover - optional shim missing
        return None
    return default_fsp_log()


def _dump_jsonl(findings: Sequence[Finding], destination: str | None) -> None:
    target = destination or _default_log_path()
    if target is None:
        sink = sys.stdout
        for finding in findings:
            sink.write(json.dumps(asdict(finding)) + "\n")
        return

    path = Path(target)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as sink:
        for finding in findings:
            sink.write(json.dumps(asdict(finding)) + "\n")


def _dump_table(findings: Sequence[Finding]) -> None:
    table = Table(title=f"bq-fsp findings ({len(findings)})")
    table.add_column("SEV", style="bold red")
    table.add_column("RULE", style="cyan")
    table.add_column("FILE", style="magenta")
    table.add_column("LINE", justify="right")
    table.add_column("SNIPPET")
    table.add_column("ID", style="green")

    for finding in findings:
        table.add_row(
            finding.severity,
            finding.rule_id,
            finding.file,
            str(finding.line),
            finding.match,
            finding.hash,
        )

    console.print(table)


def _dump_sarif(findings: Sequence[Finding], destination: str | None) -> None:
    payload = to_sarif(findings)
    data = json.dumps(payload, indent=2)
    if destination:
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(data, encoding="utf-8")
    else:
        typer.echo(data)


@app.command("scan")
def cmd_scan(
    path: str = typer.Argument(".", help="Repository root to scan."),
    staged: bool = typer.Option(False, "--staged", help="Scan staged files only."),
    rules: str | None = typer.Option(None, "--rules", "-r", help="Override rules YAML."),
    fmt: str = typer.Option("table", "--format", "-f", help="Output format: table|jsonl|sarif."),
    out: str | None = typer.Option(None, "--out", "-o", help="Optional output path."),
) -> None:
    """Scan a path for suspicious patterns."""

    try:
        rule_set = load_rules(rules)
    except Exception as exc:
        console.print(f"[red]Failed to load rules: {exc}[/red]")
        raise typer.Exit(code=2)

    findings = scan(path, rule_set, only_staged=staged)
    findings_seq = list(findings)

    format_mode = fmt.lower()
    if format_mode == "table":
        _dump_table(findings_seq)
    elif format_mode == "jsonl":
        _dump_jsonl(findings_seq, out)
    elif format_mode == "sarif":
        _dump_sarif(findings_seq, out)
    else:  # pragma: no cover - guarded by Typer choice but kept defensive
        raise typer.BadParameter("format must be table, jsonl, or sarif")

    raise typer.Exit(code=0 if not findings_seq else 1)


@app.command("semgrep")
def cmd_semgrep(
    path: str = typer.Argument(".", help="Repository root to scan with Semgrep."),
    config: str = typer.Option("p/ci", "--config", "-c", help="Semgrep configuration"),
) -> None:
    """Thin wrapper around Semgrep for parity with bq-fsp."""

    try:
        exit_code = subprocess.call(["semgrep", "--config", config, path])
    except FileNotFoundError:
        console.print("[red]Semgrep is not installed.[/red]")
        raise typer.Exit(code=2)

    raise typer.Exit(code=exit_code)


def register(bq_app) -> None:
    """Register the plugin with the BLUX Quantum CLI."""

    fsp_app = typer.Typer(name="fsp", help="Find Suspicious Patterns")
    fsp_app.command("scan")(cmd_scan)
    fsp_app.command("semgrep")(cmd_semgrep)
    bq_app.add_typer(fsp_app, name="fsp")


__all__ = ["app", "register"]

FILE: bq_fsp/ignore.py
Kind: text
Size: 2035
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Ignore rules for the bq-fsp scanner."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

try:  # pragma: no cover - optional dependency branch
    from pathspec import PathSpec
except ImportError:  # pragma: no cover - fallback implementation
    PathSpec = None  # type: ignore[assignment]

DEFAULT_IGNORES = (
    ".git/",
    ".venv/",
    "venv/",
    "node_modules/",
    "dist/",
    "build/",
    "__pycache__/",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.pdf",
    "*.mp4",
    "*.zip",
    "*.tar",
    "*.gz",
    "*.bz2",
)


@dataclass
class _FallbackSpec:
    patterns: tuple[str, ...]

    def match_file(self, filename: str) -> bool:  # pragma: no cover - simple fallback
        for pattern in self.patterns:
            if pattern.endswith("/") and filename.startswith(pattern.rstrip("/")):
                return True
            if pattern.startswith("*") and filename.endswith(pattern.lstrip("*")):
                return True
        return False


def _build_spec(patterns: Iterable[str]):
    if PathSpec is None:
        return _FallbackSpec(tuple(patterns))
    return PathSpec.from_lines("gitwildmatch", patterns)


def load_spec(repo_root: str):
    """Load ignore specification merging defaults with repository .gitignore."""

    patterns = list(DEFAULT_IGNORES)
    gitignore_path = f"{repo_root}/.gitignore"
    try:
        with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    except FileNotFoundError:
        pass
    return _build_spec(patterns)


def should_skip(spec, root: str, relpath: str) -> bool:
    """Check if a path should be skipped according to the ignore spec."""

    if hasattr(spec, "match_file"):
        return bool(spec.match_file(relpath))
    return False


__all__ = ["DEFAULT_IGNORES", "load_spec", "should_skip"]

FILE: bq_fsp/pyproject.toml
Kind: text
Size: 527
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
[build-system]
requires = ["setuptools>=67", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "bq-fsp"
version = "0.1.0"
description = "BLUX Quantum: Find Suspicious Patterns"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "typer>=0.12",
    "rich>=13.7",
    "pathspec>=0.12",
    "regex>=2024.5",
    "ruamel.yaml>=0.18"
]

[project.optional-dependencies]
dev = ["pytest", "black", "mypy"]

[project.scripts]
"bq-fsp" = "bq_fsp.cli:app"

[tool.bq.plugin]
entry = "bq_fsp.cli:register"

FILE: bq_fsp/rules.py
Kind: text
Size: 3265
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Rule definitions for the bq-fsp scanner."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:  # pragma: no cover - optional dependency branch
    import regex as _regex
except ImportError:  # pragma: no cover - fallback for environments without `regex`
    import re as _regex

try:  # pragma: no cover - optional dependency branch
    from ruamel.yaml import YAML
except ImportError:  # pragma: no cover - fallback to PyYAML if available
    YAML = None  # type: ignore[assignment]
    try:
        import yaml as _pyyaml
    except ImportError:  # pragma: no cover - ultimate fallback
        _pyyaml = None  # type: ignore[assignment]
else:
    _yaml_loader = YAML(typ="safe")
    _pyyaml = None


@dataclass(frozen=True)
class Rule:
    """Single suspicious pattern rule."""

    id: str
    pattern: _regex.Pattern[str]
    message: str
    severity: str
    languages: tuple[str, ...] | None = None


_DEFAULT_RULES = """
rules:
  - id: net-exfil
    message: "Outbound network/exfil call"
    severity: HIGH
    regex: "(curl |wget |nc |netcat|socket|requests\\.post|urllib|smtplib|sendmail|scp |ssh |ftp |telnet)"
  - id: shell-exec
    message: "Shell/Process execution"
    severity: HIGH
    regex: "(eval\\(|exec\\(|os\\.system\\(|subprocess\\.(Popen|run)|popen\\()"
  - id: secrets
    message: "Secrets/keys marker"
    severity: HIGH
    regex: "(AKIA|ssh-rsa|-----BEGIN (RSA |EC |)PRIVATE KEY-----|api[_-]?key|access[_-]?token|password)"
  - id: base64-blob
    message: "Suspicious base64-like blob"
    severity: MEDIUM
    regex: "(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{60,}={0,2}(?![A-Za-z0-9+/])"
  - id: obfuscation
    message: "Possible obfuscation / self-modifying code"
    severity: MEDIUM
    regex: "(marshal\\.loads|zlib\\.decompress|lzma\\.decompress|compile\\()"
"""


def _load_yaml_text(text: str) -> dict[str, object]:
    if YAML is not None:
        return _yaml_loader.load(text) or {}
    if _pyyaml is not None:
        return _pyyaml.safe_load(text) or {}
    raise RuntimeError("No YAML loader available for bq-fsp rules")


def _load_yaml_file(path: Path) -> dict[str, object]:
    return _load_yaml_text(path.read_text(encoding="utf-8"))


def load_rules(path: str | Path | None = None) -> list[Rule]:
    """Load rule definitions from YAML or the built-in defaults."""

    data: dict[str, Iterable[dict[str, object]]]
    if path:
        data = _load_yaml_file(Path(path))  # type: ignore[assignment]
    else:
        data = _load_yaml_text(_DEFAULT_RULES)

    rules: list[Rule] = []
    for raw in data.get("rules", []) or []:
        rule_id = str(raw.get("id"))
        pattern = _regex.compile(str(raw.get("regex", "")))
        message = str(raw.get("message", ""))
        severity = str(raw.get("severity", "MEDIUM")).upper()
        languages = raw.get("languages")
        lang_tuple = tuple(str(item) for item in languages) if languages else None
        rules.append(
            Rule(
                id=rule_id,
                pattern=pattern,
                message=message,
                severity=severity,
                languages=lang_tuple,
            )
        )
    return rules


__all__ = ["Rule", "load_rules"]

FILE: bq_fsp/sarif.py
Kind: text
Size: 1698
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""SARIF helpers for bq-fsp."""
from __future__ import annotations

from typing import Iterable

from .scanner import Finding


def to_sarif(findings: Iterable[Finding], tool_name: str = "bq-fsp", version: str = "0.1.0") -> dict:
    """Convert findings into a SARIF 2.1.0 document."""

    rules_meta: dict[str, dict] = {}
    results: list[dict] = []

    for finding in findings:
        rules_meta.setdefault(
            finding.rule_id,
            {
                "id": finding.rule_id,
                "shortDescription": {"text": finding.message},
            },
        )
        results.append(
            {
                "ruleId": finding.rule_id,
                "message": {"text": finding.message},
                "level": "error" if finding.severity.upper() == "HIGH" else "warning",
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": finding.file},
                            "region": {"startLine": finding.line},
                        }
                    }
                ],
                "fingerprints": {"sha1": finding.hash},
            }
        )

    return {
        "version": "2.1.0",
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": tool_name,
                        "version": version,
                        "rules": list(rules_meta.values()),
                    }
                },
                "results": results,
            }
        ],
    }


__all__ = ["to_sarif"]

FILE: bq_fsp/scanner.py
Kind: text
Size: 3224
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Core scanning utilities for bq-fsp."""
from __future__ import annotations

import hashlib
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .ignore import load_spec, should_skip
from .rules import Rule, load_rules

_TEXT_EXTENSIONS = {
    ".py",
    ".sh",
    ".js",
    ".ts",
    ".go",
    ".rb",
    ".rs",
    ".c",
    ".cpp",
    ".java",
    ".php",
    ".ps1",
    ".yaml",
    ".yml",
    ".toml",
    ".json",
    ".cfg",
    ".ini",
    ".md",
    ".txt",
}


@dataclass(slots=True)
class Finding:
    """Single suspicious pattern match."""

    rule_id: str
    message: str
    severity: str
    file: str
    line: int
    match: str
    hash: str


def _iter_staged_files() -> Iterable[str]:
    try:
        output = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):  # pragma: no cover - git missing
        return []
    for entry in output.decode().splitlines():
        if entry and Path(entry).is_file():
            yield entry


def iter_files(root: str, only_staged: bool = False) -> Iterable[str]:
    """Yield candidate files for scanning."""

    if only_staged:
        yield from _iter_staged_files()
        return

    spec = load_spec(root)
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), root)
            if should_skip(spec, root, rel):
                continue
            if Path(name).suffix.lower() in _TEXT_EXTENSIONS:
                yield rel


def scan(root: str = ".", rules: list[Rule] | None = None, only_staged: bool = False) -> list[Finding]:
    """Scan a repository path and return suspicious findings."""

    base = Path(root)
    rule_set = rules or load_rules()
    findings: list[Finding] = []

    for rel in iter_files(str(base), only_staged=only_staged):
        file_path = base / rel
        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
                for lineno, line in enumerate(handle, start=1):
                    for rule in rule_set:
                        match = rule.pattern.search(line)
                        if not match:
                            continue
                        fingerprint = hashlib.sha1(
                            f"{rel}:{lineno}:{match.group(0)}".encode("utf-8"),
                        ).hexdigest()[:12]
                        findings.append(
                            Finding(
                                rule_id=rule.id,
                                message=rule.message,
                                severity=rule.severity,
                                file=str(rel),
                                line=lineno,
                                match=match.group(0)[:200],
                                hash=fingerprint,
                            )
                        )
        except OSError:  # pragma: no cover - permission/encoding errors
            continue

    return findings


__all__ = ["Finding", "scan", "iter_files"]

FILE: docs/ARCHITECTURE.md
Kind: text
Size: 937
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# Architecture

## Core CLI
- Built with [Typer](https://typer.tiangolo.com/) providing the `blux` command.
- Commands implement request creation, routing, and audit previews.

## Plugin Loader
- Discovers entry points published under `blux.plugins`.
- Mounts Typer applications dynamically beneath the root CLI namespace.

## Telemetry Subsystem
- Writes JSONL events and mirrors to SQLite for durability.
- Exposes Prometheus metrics via an in-process registry for external exporters.
- Controlled through `BLUXQ_TELEMETRY` and `BLUXQ_TELEMETRY_WARN` environment variables.

## Configuration
- Supports layered configuration: environment variables, user config directory, and local project files.
- YAML-based configuration merged with dictionary semantics.

## Ecosystem Map
- Guard and Lite extend the ecosystem alongside cA.
- Additional products can publish entry points to join the command surface without modifying the core CLI.

FILE: docs/CONFIGURATION.md
Kind: text
Size: 641
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
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

FILE: docs/INSTALL.md
Kind: text
Size: 748
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
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
Enable Typer auto-completion by exporting `_BLUX_COMPLETE`:
```bash
eval "$(blux --install-completion)"
```

## Termux Notes
- Install Python via `pkg install python`.
- Use `pip install --user blux-quantum` and ensure `$HOME/.local/bin` is on PATH.

## PowerShell Alias
- Run `scripts/demo_install_alias.ps1` to register a convenience alias for `blux`.

## Telemetry Controls
- Disable telemetry with `BLUXQ_TELEMETRY=off`.
- Surface one-time warnings with `BLUXQ_TELEMETRY_WARN=once`.

FILE: docs/INTEGRATIONS.md
Kind: text
Size: 837
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# Integrations

## Plugin Contract
External packages expose Typer apps via the `blux.plugins` entry-point group.

```toml
[project.entry-points."blux.plugins"]
guard = "blux_guard.cli:get_app"
```

## cA
- cA emits discernment reports for incoming requests.
- Ensure the `blux-ca` command is available on PATH.

## Guard
- Guard executes receipt generation for routed requests.
- Quantum forwards discernment reports to Guard and persists the receipt artifacts.
- Ensure the `blux-guard` command is available on PATH.

## Lite
- Lite executes approved tasks after Guard returns an ALLOW/WARN receipt.
- Quantum forwards Guard receipts and captures Lite receipts.
- Ensure the `blux-lite` command is available on PATH.

## Future Plugins
- `blux-ca`, `blux-guard`, and `blux-lite` can register entry points without patching the core CLI.

FILE: docs/OPERATIONS.md
Kind: text
Size: 561
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
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

FILE: docs/PHYSICS.md
Kind: text
Size: 844
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# BLUX Quantum Physics (Phase 9)

## Invariants
- Quantum remains dispatcher-only: dispatch CLI exposes preview + routing only (no execution surfaces).
- Guard receipts are required for any routing that targets Lite.
- Phase 0 envelopes always include `trace_id`, `span_id`, `timestamp`, `source`, and `payload_schema`.
- Audit previews always include `trace_id`, artifact paths, decision band/score, receipt decision, and execution manifest (if known).
- Dispatch preview output always includes a `trace_id` for observability.
- Plugin discovery uses the canonical `blux.plugins` entry-point group or bundled defaults.

## Violations (must never happen)
- Emitting envelopes without a `trace_id` in dispatch outputs.
- Routing to Lite without a guard receipt requirement.
- Expanding Quantum into an execution runtime instead of a dispatcher.

FILE: docs/ROADMAP.md
Kind: text
Size: 605
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# Roadmap

## Near Term
- Integrate real Guard/Lite/Doctrine packages as optional extras.
- Provide remote telemetry forwarding via HTTPS gateway with opt-in consent.
- Harden stability mode with service-specific quiesce adapters.

## Mid Term
- Add Textual-based TUI dashboards for runtime oversight.
- Offer configuration linting and schema validation.
- Expand CI to run security scanners and dependency review automation.

## Long Term
- Release signed binaries for Windows and macOS.
- Introduce plugin marketplace discovery within `blux`.
- Support distributed command execution via BLUX Commander.

FILE: docs/ROLE.md
Kind: text
Size: 1002
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# BLUX Quantum Role

BLUX Quantum is the dispatcher-only front door for the BLUX constellation. It provides
routing, visibility, and preview surfaces for requests, and it forwards receipts from
downstream systems without making decisions locally.

Routing chain:
`request` → `discernment_report` (cA) → `guard_receipt` (Guard) → `lite` execute (or dry-run).

## Allowed responsibilities
- Build and emit request/receipt envelopes for routing visibility.
- Route tasks to the appropriate constellation component without enforcing outcomes.
- Surface previews of what will happen, including required receipt dependencies.
- Report audit previews, artifact locations, and routing summaries.

## Prohibited responsibilities
- Making policy, ethics, or permission decisions.
- Executing non-BLUX tools, commands, or subprocesses locally.
- Issuing, minting, signing, or verifying tokens.
- Performing Guard or Lite enforcement actions locally.
- Providing doctrine, discernment, or enforcement logic.

FILE: docs/SECURITY.md
Kind: text
Size: 805
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
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

FILE: docs/TROUBLESHOOTING.md
Kind: text
Size: 736
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
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

FILE: docs/fsp.md
Kind: text
Size: 352
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# bq fsp — Find Suspicious Patterns

**Purpose:** fast, local static scans for exfil, shell exec, secrets, and obfuscation.

```bash
bq fsp scan .
bq fsp scan . --staged -f jsonl
bq fsp scan . -f sarif -o out.sarif
```

Exit codes: 0 clean, 1 findings, 2 error / plugin missing.  
Default path: `~/.config/blux-lite-gold/logs/fsp.jsonl`

_(( • ))_

FILE: docs/index.md
Kind: text
Size: 290
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
# BLUX Quantum

Welcome to the BLUX Quantum operator platform. This site documents the enterprise CLI, its plugin architecture, telemetry considerations, and operational runbooks. Quantum does not decide outcomes or execute tools directly; it only dispatches and surfaces what will happen.

FILE: mkdocs.yml
Kind: text
Size: 465
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
site_name: BLUX Quantum
site_description: Unified Operator CLI for the BLUX ecosystem
nav:
  - Overview: index.md
  - Architecture: ARCHITECTURE.md
  - Install: INSTALL.md
  - Operations: OPERATIONS.md
  - Security: SECURITY.md
  - FSP Scanner: fsp.md
  - Configuration: CONFIGURATION.md
  - Troubleshooting: TROUBLESHOOTING.md
  - Roadmap: ROADMAP.md
  - Integrations: INTEGRATIONS.md
theme:
  name: material
repo_url: https://github.com/blux-systems/blux-quantum

FILE: mypy.ini
Kind: text
Size: 81
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
[mypy]
python_version = 3.9
ignore_missing_imports = True
strict_optional = True

FILE: pyproject.toml
Kind: text
Size: 1278
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
[build-system]
requires = ["setuptools>=67", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "blux-quantum"
version = "0.1.0"
description = "BLUX Quantum — Dispatcher-only activator (blux) for the BLUX ecosystem"
readme = "README.md"
requires-python = ">=3.9"
license = { text = "Apache-2.0" }
authors = [{ name = "BLUX", email = "ops@blux.systems" }]
keywords = ["cli", "security", "observability", "tui", "blux"]
classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: Apache Software License",
  "Environment :: Console",
  "Intended Audience :: Developers",
  "Topic :: Security",
]
dependencies = [
  "typer>=0.12.3",
  "rich>=13.7.0",
  "textual>=0.62.0",
  "psutil>=5.9.8",
  "pyyaml>=6.0.1",
  "sqlite-utils>=3.36",
  "prometheus-client>=0.20.0",
]

[project.optional-dependencies]
dev = ["pytest", "mypy", "ruff", "pre-commit", "mkdocs-material"]

[project.scripts]
blux = "blux_quantum.cli:app"
bluxq = "blux_quantum.cli:app"

[tool.ruff]
target-version = "py39"
line-length = 100
select = ["E", "F", "I", "UP", "B", "A"]
ignore = ["B905"]

[tool.setuptools]
license-files = ["LICENSE", "LICENSE-APACHE", "LICENSE-COMMERCIAL", "NOTICE"]

[tool.setuptools.packages.find]
include = ["blux_quantum*", "bq*", "bq_fsp*"]

FILE: pytest.ini
Kind: text
Size: 54
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
[pytest]
addopts = -ra
python_files = tests/test_*.py

FILE: scripts/bluxq
Kind: text
Size: 100
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
#!/usr/bin/env sh
# Compatibility wrapper for the BLUX Quantum CLI.

exec "$(dirname "$0")/bq" "$@"

FILE: scripts/bq
Kind: text
Size: 117
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
#!/usr/bin/env sh
# Lightweight wrapper to launch the BLUX Quantum Typer app.

exec python3 -m blux_quantum.cli "$@"

FILE: scripts/demo_install_alias.ps1
Kind: text
Size: 260
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
Param(
    [string]$AliasName = "bluxq",
    [string]$Target = "bluxq"
)

Write-Host "Registering PowerShell alias '$AliasName' for '$Target'"
New-Alias -Name $AliasName -Value $Target -Force
Write-Host "Alias registered. Add to your profile for persistence."

FILE: scripts/gen_filetree.py
Kind: text
Size: 984
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Generate a repository file tree."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

IGNORED = {".git", "__pycache__", "dist", "build", ".mypy_cache", ".pytest_cache", "site"}


def iter_directory(path: Path, prefix: str = "") -> Iterable[str]:
    entries = sorted(p for p in path.iterdir() if p.name not in IGNORED)
    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        yield f"{prefix}{connector}{entry.name}"
        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            yield from iter_directory(entry, prefix + extension)


def build_tree(root: Path | None = None) -> str:
    root = (root or Path.cwd()).resolve()
    lines = [root.name or str(root)]
    lines.extend(iter_directory(root))
    return "\n".join(lines)


def main() -> None:
    print(build_tree())


if __name__ == "__main__":
    main()

FILE: scripts/generate_command_reference.py
Kind: text
Size: 3981
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Generate the README command reference from the real Typer surface."""
from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List, Tuple

from typer.testing import CliRunner

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from blux_quantum.cli import app

MARKER_START = "<!-- BEGIN AUTO-GENERATED COMMANDS -->"
MARKER_END = "<!-- END AUTO-GENERATED COMMANDS -->"


def _run_help(args: Iterable[str], home: Path) -> str:
    env = os.environ.copy()
    env.setdefault("BLUXQ_HOME", str(home))
    env.setdefault("BLUXQ_BANNER", "off")
    result = CliRunner().invoke(app, [*args, "--help"], env=env, prog_name="blux")
    return result.stdout.strip()


def _extract_usage(help_text: str) -> str | None:
    for line in help_text.splitlines():
        if line.strip().startswith("Usage:"):
            usage = line.strip().replace("Usage:", "").strip()
            return usage.replace("python -m blux_quantum.cli", "blux")
    return None


def _extract_commands(help_text: str) -> List[Tuple[str, str]]:
    commands: List[Tuple[str, str]] = []
    capture = False
    for line in help_text.splitlines():
        if "Commands" in line:
            capture = True
            continue
        if not capture:
            continue
        if line.strip().startswith("╰"):
            break

        clean = line.strip().strip("│").strip()
        if not clean:
            continue
        match = re.match(r"([\w-]+)\s*(.*)", clean)
        if match:
            name, desc = match.groups()
            if name:
                commands.append((name.strip(), desc.strip()))
    return commands


def _render_reference(home: Path) -> str:
    root_help = _run_help([], home)
    top_level_commands = _extract_commands(root_help)

    lines: List[str] = [MARKER_START, "", "_Generated via `python scripts/generate_command_reference.py`._", ""]

    for name, desc in top_level_commands:
        description = desc or "No description provided."
        help_text = _run_help([name], home)
        usage = _extract_usage(help_text) or f"blux {name}"
        subcommands = _extract_commands(help_text)
        lines.append(f"- `blux {name}` — {description}")
        lines.append(f"  - Example: `{usage}`")
        if subcommands:
            lines.append("  - Subcommands:")
            for sub_name, sub_desc in subcommands:
                sub_description = sub_desc or "No description provided."
                sub_help = _run_help([name, sub_name], home)
                sub_usage = _extract_usage(sub_help) or f"blux {name} {sub_name}"
                lines.append(f"    - `blux {name} {sub_name}` — {sub_description}")
                lines.append(f"      - Example: `{sub_usage}`")
        lines.append("")

    lines.append(MARKER_END)
    return "\n".join(lines) + "\n"


def _rewrite_readme(readme_path: Path, block: str) -> None:
    content = readme_path.read_text(encoding="utf-8")
    if MARKER_START not in content or MARKER_END not in content:
        raise SystemExit("README is missing the auto-generated command markers")
    start = content.index(MARKER_START)
    end = content.index(MARKER_END) + len(MARKER_END)
    new_content = content[:start] + block + content[end:]
    readme_path.write_text(new_content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate README command reference")
    parser.add_argument("--readme", type=Path, default=Path(__file__).resolve().parent.parent / "README.md")
    parser.add_argument("--stdout", action="store_true", help="Print the block instead of writing")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        block = _render_reference(Path(tmpdir))

    if args.stdout:
        sys.stdout.write(block)
        return

    _rewrite_readme(args.readme, block)

if __name__ == "__main__":
    main()

FILE: scripts/physics_check.sh
Kind: text
Size: 1353
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

forbidden_regex='ethic|morality|discern|posture|illusion|therapy|safety policy|harm'

for file in $(git ls-files); do
  case "$file" in
    LICENSE*|scripts/physics_check.sh) continue ;;
  esac
  if rg -n -i -e "$forbidden_regex" "$file" >/dev/null; then
    echo "Forbidden content detected in $file"
    rg -n -i -e "$forbidden_regex" "$file"
    exit 1
  fi
done

for file in $(git ls-files); do
  case "$file" in
    scripts/physics_check.sh) continue ;;
  esac
  hits="$(rg -n -e 'subprocess\\.run\\(|os\\.system\\(' "$file" || true)"
  if [[ -n "$hits" ]]; then
    if echo "$hits" | rg -v 'blux-guard|blux-lite|blux-reg' >/dev/null; then
      echo "Direct tool execution detected in $file"
      echo "$hits"
      exit 1
    fi
  fi
done

expected_phase0_hash="8e13b0236fdfb573ba6db9c6f5de6ed3d154b0f6885f1d30d3294fbc2aa13657"
actual_phase0_hash="$(python - <<'PY'
import hashlib
from pathlib import Path

path = Path("blux_quantum/envelope.py")
print(hashlib.sha256(path.read_bytes()).hexdigest())
PY
)"
if [[ "$actual_phase0_hash" != "$expected_phase0_hash" ]]; then
  echo "Phase 0 contract schema mismatch in blux_quantum/envelope.py"
  echo "expected=$expected_phase0_hash"
  echo "actual=$actual_phase0_hash"
  exit 1
fi

FILE: scripts/physics_checks.py
Kind: text
Size: 3285
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Physics checks for BLUX Quantum guardrails."""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
CODE_DIRS = [ROOT / "blux_quantum"]

POLICY_KEYWORDS = {"policy", "policies", "ethic", "ethics", "doctrine"}
TOKEN_KEYWORDS = {"token", "tokens", "jwt", "signature", "sign", "verify", "mint"}
ALLOWED_COMMANDS = {"blux-ca", "blux-guard", "blux-lite"}


def _iter_python_files() -> Iterable[Path]:
    for base in CODE_DIRS:
        if base.is_dir():
            yield from base.rglob("*.py")


def _file_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _scan_keywords(keyword_set: set[str]) -> list[str]:
    violations: list[str] = []
    for path in _iter_python_files():
        text = _file_text(path).lower()
        for keyword in keyword_set:
            pattern = re.compile(rf"\\b{re.escape(keyword)}\\b")
            if pattern.search(text):
                violations.append(f"{path.relative_to(ROOT)}: contains '{keyword}'")
    return violations


def _scan_contract_copying() -> list[str]:
    violations: list[str] = []
    for path in ROOT.rglob("*.schema.json"):
        violations.append(f"{path.relative_to(ROOT)}: schema file present")
    for path in ROOT.rglob("contracts"):
        if path.is_dir():
            violations.append(f"{path.relative_to(ROOT)}: contracts directory present")
    return violations


def _scan_subprocess_usage() -> list[str]:
    violations: list[str] = []
    for path in _iter_python_files():
        tree = ast.parse(_file_text(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
                    if func.value.id == "subprocess" and func.attr in {"run", "Popen", "call"}:
                        if not node.args:
                            violations.append(f"{path.relative_to(ROOT)}:{node.lineno}: subprocess call without args")
                            continue
                        arg = node.args[0]
                        cmd = None
                        if isinstance(arg, ast.List) and arg.elts and isinstance(arg.elts[0], ast.Constant):
                            cmd = arg.elts[0].value
                        elif isinstance(arg, ast.Tuple) and arg.elts and isinstance(arg.elts[0], ast.Constant):
                            cmd = arg.elts[0].value
                        if cmd not in ALLOWED_COMMANDS:
                            violations.append(
                                f"{path.relative_to(ROOT)}:{node.lineno}: subprocess command '{cmd}' not allowed"
                            )
    return violations


def main() -> int:
    failures: list[str] = []

    failures.extend(_scan_keywords(POLICY_KEYWORDS))
    failures.extend(_scan_keywords(TOKEN_KEYWORDS))
    failures.extend(_scan_contract_copying())
    failures.extend(_scan_subprocess_usage())

    if failures:
        print("Physics guardrails violated:")
        for item in failures:
            print(f"- {item}")
        return 1
    print("Physics guardrails ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())

FILE: scripts/physics_tests.sh
Kind: text
Size: 150
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

python scripts/physics_checks.py

FILE: scripts/update_readme_filetree.py
Kind: text
Size: 1192
Last modified: 2026-01-21T07:57:01.751602Z

CONTENT:
"""Update README file tree section."""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from gen_filetree import build_tree

MARKER_BEGIN = "<!-- FILETREE:BEGIN -->"
MARKER_END = "<!-- FILETREE:END -->"


def update_readme(readme_path: Path) -> None:
    content = readme_path.read_text(encoding="utf-8")
    if MARKER_BEGIN not in content or MARKER_END not in content:
        raise SystemExit("Markers not found in README")

    tree = build_tree(readme_path.parent)
    snippet = (
        f"{MARKER_BEGIN}\n"
        "<!-- generated; do not edit manually -->\n"
        "<details><summary><strong>Repository File Tree</strong> (click to expand)</summary>\n\n"
        "```text\n"
        f"{tree}\n"
        "```\n\n"
        "</details>\n"
        f"{MARKER_END}"
    )

    start = content.index(MARKER_BEGIN)
    end = content.index(MARKER_END) + len(MARKER_END)
    updated = content[:start] + snippet + content[end:]
    readme_path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    update_readme(Path("README.md"))

FILE: tests/conftest.py
Kind: text
Size: 223
Last modified: 2026-01-21T07:57:01.755602Z

CONTENT:
"""Test configuration for BLUX Quantum."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

FILE: tests/test_cli.py
Kind: text
Size: 4032
Last modified: 2026-01-21T07:57:01.755602Z

CONTENT:
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from typer.testing import CliRunner

from blux_quantum import cli
from blux_quantum.audit import audit_log_path


def _env(tmp_path: Path) -> dict[str, str]:
    return {"BLUXQ_HOME": str(tmp_path)}


def _extract_json_objects(text: str) -> list[Any]:
    decoder = json.JSONDecoder()
    index = 0
    objects: list[Any] = []
    while index < len(text):
        if text[index].isspace():
            index += 1
            continue
        try:
            obj, end = decoder.raw_decode(text, index)
        except json.JSONDecodeError:
            index += 1
            continue
        objects.append(obj)
        index = end
    return objects


def _write_component_stub(
    tmp_path: Path,
    name: str,
    envelope_type: str,
    payload: dict[str, Any],
    payload_schema: str,
) -> Path:
    script_path = tmp_path / name
    script = f"""#!/usr/bin/env python3
import json
import sys
import uuid
from datetime import datetime, timezone

payload = {json.dumps(payload)}
request = json.load(sys.stdin)
trace_id = request.get("trace_id") or str(uuid.uuid4())
response = {{
    "schema": "blux://contracts/envelope.schema.json",
    "envelope_id": str(uuid.uuid4()),
    "type": "{envelope_type}",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "source": {{"repo": "{name}", "component": "{name}", "instance": "test"}},
    "trace_id": trace_id,
    "span_id": str(uuid.uuid4()),
    "payload_schema": "{payload_schema}",
    "payload": payload,
}}
print(json.dumps(response))
"""
    script_path.write_text(script, encoding="utf-8")
    script_path.chmod(0o755)
    return script_path


def _with_component_bins(tmp_path: Path) -> dict[str, str]:
    _write_component_stub(
        tmp_path,
        "blux-ca",
        "discernment_report",
        {"decision_band": "ALLOW", "decision_score": 0.9, "execution_manifest": "plans/exec.json"},
        "blux://contracts/discernment_report.schema.json",
    )
    _write_component_stub(
        tmp_path,
        "blux-guard",
        "guard_receipt",
        {"decision": "ALLOW"},
        "blux://contracts/guard_receipt.schema.json",
    )
    _write_component_stub(
        tmp_path,
        "blux-lite",
        "lite_receipt",
        {"status": "queued"},
        "blux://contracts/lite_receipt.schema.json",
    )
    env = _env(tmp_path)
    env["PATH"] = f"{tmp_path}{os.pathsep}{env.get('PATH', '')}"
    return env


def test_command_tree(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["--help"], env=_env(tmp_path))
    assert result.exit_code == 0
    assert "request" in result.stdout
    assert "inspect" in result.stdout
    assert "dry-run" in result.stdout
    assert "run" in result.stdout


def test_audit_written(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["request", "hello"], env=_env(tmp_path))
    assert result.exit_code == 0
    log = audit_log_path()
    assert log.exists()
    event = json.loads(log.read_text(encoding="utf-8").splitlines()[-1])
    assert event["cmd"] == "request"


def test_dry_run_outputs_audit_preview(tmp_path: Path) -> None:
    runner = CliRunner()
    env = _with_component_bins(tmp_path)
    result = runner.invoke(cli.app, ["dry-run", "hello"], env=env)
    assert result.exit_code == 0
    objects = _extract_json_objects(result.stdout)
    preview = objects[-1]["audit_preview"]
    assert preview["trace_id"]
    assert preview["decision_band"] == "ALLOW"
    assert preview["receipt_decision"] == "ALLOW"


def test_run_outputs_lite_receipt(tmp_path: Path) -> None:
    runner = CliRunner()
    env = _with_component_bins(tmp_path)
    result = runner.invoke(cli.app, ["run", "hello"], env=env)
    assert result.exit_code == 0
    objects = _extract_json_objects(result.stdout)
    types = [obj.get("type") for obj in objects if isinstance(obj, dict) and "type" in obj]
    assert "lite_receipt" in types

FILE: tests/test_physics.py
Kind: text
Size: 1776
Last modified: 2026-01-21T07:57:01.755602Z

CONTENT:
from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from blux_quantum import cli
from blux_quantum.envelope import EnvelopeSource, create_envelope


def _env(tmp_path: Path) -> dict[str, str]:
    return {"BLUXQ_HOME": str(tmp_path)}


def _extract_json_objects(text: str) -> list[object]:
    decoder = json.JSONDecoder()
    index = 0
    objects: list[object] = []
    while index < len(text):
        if text[index].isspace():
            index += 1
            continue
        try:
            obj, end = decoder.raw_decode(text, index)
        except json.JSONDecodeError:
            index += 1
            continue
        objects.append(obj)
        index = end
    return objects


def test_envelope_contract_fields() -> None:
    envelope = create_envelope(
        "guard_receipt",
        {"decision": "ALLOW"},
        source=EnvelopeSource(repo="blux-quantum", component="guard", instance="test"),
    )
    assert envelope["schema"]
    assert envelope["type"] == "guard_receipt"
    assert isinstance(envelope["trace_id"], str)
    assert isinstance(envelope["span_id"], str)
    assert isinstance(envelope["timestamp"], str)
    assert set(envelope["source"].keys()) == {"repo", "component", "instance"}
    assert envelope["payload"] == {"decision": "ALLOW"}


def test_request_outputs_trace_id(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["request", "task.txt"], env=_env(tmp_path))
    assert result.exit_code == 0
    objects = _extract_json_objects(result.stdout)
    envelope = objects[0]
    assert isinstance(envelope["trace_id"], str)
    assert envelope["trace_id"]
    assert envelope["payload_schema"] == "blux://contracts/request.schema.json"

FILE: tests/test_plugins.py
Kind: text
Size: 229
Last modified: 2026-01-21T07:57:01.755602Z

CONTENT:
from __future__ import annotations

from blux_quantum.plugins.quantum_framework.loader import discover_plugins


def test_plugin_discovery_executes() -> None:
    plugins = discover_plugins()
    assert isinstance(plugins, list)

FILE: tests/test_reference_generator.py
Kind: text
Size: 793
Last modified: 2026-01-21T07:57:01.755602Z

CONTENT:
from __future__ import annotations

import sys
from subprocess import check_call


def test_command_reference_generator(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(
        "\n".join(
            [
                "Intro", 
                "<!-- BEGIN AUTO-GENERATED COMMANDS -->", 
                "placeholder", 
                "<!-- END AUTO-GENERATED COMMANDS -->", 
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    check_call([sys.executable, "scripts/generate_command_reference.py", "--readme", str(readme)])

    content = readme.read_text(encoding="utf-8")
    assert "blux request" in content
    assert "_Generated via" in content
    lines = {line.strip() for line in content.splitlines()}
    assert "placeholder" not in lines

FILE: tests/test_role_contract.py
Kind: text
Size: 626
Last modified: 2026-01-21T07:57:01.755602Z

CONTENT:
from __future__ import annotations

from pathlib import Path


def _read_repo_file(name: str) -> str:
    return (Path(__file__).resolve().parents[1] / name).read_text(encoding="utf-8")


def test_role_contract_statement() -> None:
    text = _read_repo_file("ROLE.md").lower()
    assert "dispatcher-only" in text
    assert "does not" in text
    assert "decisions" in text
    assert "execute" in text


def test_readme_dispatch_only_statement() -> None:
    text = _read_repo_file("README.md").lower()
    assert "dispatcher-only" in text
    assert "does not decide outcomes" in text
    assert "only dispatches" in text

FILE: tests/test_telemetry.py
Kind: text
Size: 719
Last modified: 2026-01-21T07:57:01.755602Z

CONTENT:
from __future__ import annotations

from pathlib import Path

from blux_quantum.telemetry import record_event, telemetry_status


def test_record_event_respects_env_off(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("BLUXQ_HOME", str(tmp_path))
    monkeypatch.setenv("BLUXQ_TELEMETRY", "off")
    assert record_event("test.off") is False


def test_record_event_writes_files(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("BLUXQ_HOME", str(tmp_path))
    monkeypatch.delenv("BLUXQ_TELEMETRY", raising=False)
    assert record_event("test.on", {"value": 1}) is True
    status = telemetry_status()
    assert Path(status["log_path"]).exists()
    assert Path(status["sqlite_path"]).exists()

## 4) Workflow Inventory (index only)
.github/workflows/ci.yml — pull_request, push

## 5) Search Index (raw results)

subprocess:
blux_quantum/cli.py
bq_fsp/cli.py
bq_fsp/rules.py
bq_fsp/scanner.py
docs/ROLE.md
scripts/physics_check.sh
scripts/physics_checks.py
tests/test_reference_generator.py

os.system:
none

exec(:
none

spawn:
none

shell:
blux_quantum/environment.py
bq_fsp/rules.py
docs/fsp.md

child_process:
none

policy:
README.md
docs/ROLE.md
scripts/physics_check.sh
scripts/physics_checks.py

ethic:
docs/ROLE.md
scripts/physics_check.sh
scripts/physics_checks.py

enforce:
README.md
ROLE.md
blux_quantum/cli.py
docs/ROLE.md

guard:
README.md
ROLE.md
blux_quantum/cli.py
blux_quantum/envelope.py
bq_fsp/cli.py
docs/CONFIGURATION.md
docs/INTEGRATIONS.md
docs/PHYSICS.md
docs/ROLE.md
scripts/physics_check.sh
scripts/physics_checks.py
tests/test_cli.py
tests/test_physics.py

receipt:
README.md
ROLE.md
blux_quantum/cli.py
blux_quantum/envelope.py
docs/INTEGRATIONS.md
docs/OPERATIONS.md
docs/PHYSICS.md
docs/ROLE.md
tests/test_cli.py
tests/test_physics.py

token:
ROLE.md
bq_fsp/rules.py
docs/ROLE.md
scripts/physics_checks.py

signature:
README.md
scripts/physics_checks.py

verify:
docs/ROLE.md
scripts/physics_checks.py

capability:
blux_quantum/envelope.py

key_id:
none

contract:
LICENSE-APACHE
blux_quantum/envelope.py
scripts/physics_check.sh
scripts/physics_checks.py
tests/test_cli.py
tests/test_physics.py
tests/test_role_contract.py

schema:
blux_quantum/cli.py
blux_quantum/envelope.py
bq_fsp/sarif.py
docs/PHYSICS.md
docs/ROADMAP.md
scripts/physics_check.sh
scripts/physics_checks.py
tests/test_cli.py
tests/test_physics.py

$schema:
bq_fsp/sarif.py

json-schema:
none

router:
README.md
blux_quantum/cli.py

orchestr:
blux_quantum/orchestrator.py

execute:
LICENSE-APACHE
README.md
ROLE.md
blux_quantum/telemetry.py
docs/INTEGRATIONS.md
docs/ROLE.md
docs/SECURITY.md
docs/index.md
tests/test_plugins.py
tests/test_role_contract.py

command:
Makefile
README.md
blux_quantum/audit.py
blux_quantum/cli.py
blux_quantum/diagnostics.py
blux_quantum/orchestrator.py
bq_fsp/cli.py
docs/ARCHITECTURE.md
docs/INTEGRATIONS.md
docs/ROADMAP.md
docs/ROLE.md
docs/TROUBLESHOOTING.md
scripts/generate_command_reference.py
scripts/physics_checks.py
tests/test_cli.py
tests/test_reference_generator.py

## 6) Notes
none
