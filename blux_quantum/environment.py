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
