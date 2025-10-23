"""Example BLUX Doctrine plugin."""
from __future__ import annotations

import typer
from rich import print

app = typer.Typer(help="Example BLUX Doctrine integration.")


@app.command()
def schema() -> None:
    """Display doctrine schema version."""
    print({"doctrine": "v1", "compliance": "baseline"})


@app.command()
def sync(destination: str = "ledger") -> None:
    """Synchronise doctrine data."""
    print(f"[doctrine] synchronised with {destination}")


def get_app() -> typer.Typer:
    return app
