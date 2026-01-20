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
