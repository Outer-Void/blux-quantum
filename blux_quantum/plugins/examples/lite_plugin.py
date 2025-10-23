"""Example BLUX Lite plugin."""
from __future__ import annotations

import typer
from rich import print

app = typer.Typer(help="Example BLUX Lite integration.")


@app.command()
def info() -> None:
    """Display lite module info."""
    print({"lite": "ready", "mode": "developer"})


@app.command()
def activate(profile: str = "default") -> None:
    """Activate a lite profile."""
    print(f"[lite] profile '{profile}' activated")


def get_app() -> typer.Typer:
    return app
