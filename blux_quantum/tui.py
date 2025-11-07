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
