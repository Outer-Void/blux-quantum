"""Lightweight Reg bridge for key gating and signing stubs."""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from pathlib import Path
from typing import Dict, Iterable

from .audit import append_event


def _config_root() -> Path:
    env_home = os.environ.get("BLUXQ_HOME") or os.environ.get("XDG_CONFIG_HOME")
    if env_home:
        return Path(env_home) / "blux-quantum"
    return Path.home() / ".config" / "blux-quantum"


def key_dir() -> Path:
    return _config_root() / "keys"


def _keys() -> Iterable[Path]:
    return key_dir().glob("*.json")


def ensure_key_store() -> Path:
    store = key_dir()
    store.mkdir(parents=True, exist_ok=True)
    return store


def create_key(label: str | None = None) -> Path:
    ensure_key_store()
    key_id = uuid.uuid4().hex
    payload: Dict[str, str] = {"id": key_id, "label": label or "default", "secret": uuid.uuid4().hex}
    path = key_dir() / f"{key_id}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    append_event({"cmd": "reg.key.create", "outcome": "ok", "args": {"id": key_id}})
    return path


def load_keys() -> Dict[str, Dict[str, str]]:
    keys: Dict[str, Dict[str, str]] = {}
    for item in _keys():
        try:
            data = json.loads(item.read_text(encoding="utf-8"))
            keys[data.get("id", item.stem)] = data
        except json.JSONDecodeError:
            continue
    return keys


def has_keys() -> bool:
    return any(True for _ in _keys())


def require_key(action: str) -> None:
    outcome = "allow" if has_keys() else "deny"
    append_event({"cmd": "reg.require", "args": {"action": action}, "outcome": outcome})
    if outcome == "deny":
        raise PermissionError("Reg key required for this action")


def _local_signature(secret: str, content: bytes) -> str:
    return hashlib.sha256(secret.encode("utf-8") + content).hexdigest()


def _load_first_key() -> Dict[str, str] | None:
    keys = load_keys()
    if not keys:
        return None
    key_id = sorted(keys.keys())[0]
    return keys[key_id]


def sign_path(path: Path) -> str:
    key = _load_first_key()
    if not key:
        raise PermissionError("No Reg keys available")
    content = path.read_bytes()
    return _local_signature(key["secret"], content)


def verify_path(path: Path, signature: str) -> bool:
    key = _load_first_key()
    if not key:
        return False
    content = path.read_bytes()
    return _local_signature(key["secret"], content) == signature


__all__ = ["create_key", "ensure_key_store", "has_keys", "key_dir", "load_keys", "require_key", "sign_path", "verify_path"]
