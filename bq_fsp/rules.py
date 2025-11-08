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
