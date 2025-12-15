from __future__ import annotations

import subprocess
import sys


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

    result = subprocess.run(
        [sys.executable, "scripts/generate_command_reference.py", "--readme", str(readme)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.returncode == 0

    content = readme.read_text(encoding="utf-8")
    assert "bluxq version" in content
    assert "_Generated via" in content
    lines = {line.strip() for line in content.splitlines()}
    assert "placeholder" not in lines
