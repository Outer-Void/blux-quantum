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
