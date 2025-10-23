"""Example BLUX Guard plugin."""
from __future__ import annotations

import typer
from rich import print

app = typer.Typer(help="Example BLUX Guard integration.")


@app.command()
def status() -> None:
    """Show guard status."""
    print({"guard": "ok", "checks": ["identity", "runtime"]})


@app.command()
def ping(target: str = "control-plane") -> None:
    """Send a ping to the guard service."""
    print(f"[guard] ping {target} acknowledged")


def get_app() -> typer.Typer:
    return app
