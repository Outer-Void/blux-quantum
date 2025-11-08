"""Quantum task orchestration primitives for CLI commands."""
from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence

from .plugins.quantum_framework.loader import PluginInfo, discover_plugins


class OrchestrationError(RuntimeError):
    """Raised when routing or evaluation fails."""


@dataclass
class RouteDecision:
    task: str
    route: str
    confidence: float
    reasoning: str
    plugin_candidates: Sequence[str]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "route": self.route,
            "confidence": round(self.confidence, 2),
            "reasoning": self.reasoning,
            "plugin_candidates": list(self.plugin_candidates),
        }


def _plugin_candidates(task: str, plugins: Iterable[PluginInfo]) -> List[str]:
    candidates: List[str] = []
    lowered = task.lower()
    for plugin in plugins:
        if not plugin.loaded:
            continue
        if plugin.name in lowered:
            candidates.append(plugin.name)
        elif any(keyword in lowered for keyword in plugin.name.split("-")):
            candidates.append(plugin.name)
    return candidates


def route_task(task: str, context: Dict[str, Any] | None = None) -> RouteDecision:
    if not task.strip():
        raise OrchestrationError("Task description required for routing")

    plugins = discover_plugins()
    loaded_plugins = [plugin for plugin in plugins if plugin.loaded]
    if not loaded_plugins:
        raise OrchestrationError("No plugins available to route task")

    candidates = _plugin_candidates(task, loaded_plugins)
    if not candidates:
        candidates = [loaded_plugins[0].name]

    preferred = candidates[0]
    confidence = 0.6 + 0.4 * random.random()
    reasoning = "Matched plugin keyword" if candidates else "Defaulted to first available plugin"
    if context:
        reasoning += f"; context keys: {', '.join(sorted(context.keys()))}"

    return RouteDecision(task=task, route=preferred, confidence=confidence, reasoning=reasoning, plugin_candidates=candidates)


def evaluate_task(task: str, result: Dict[str, Any] | None = None) -> Dict[str, Any]:
    if not task.strip():
        raise OrchestrationError("Task description required for evaluation")

    result_payload = result or {}
    score = 0.8 if result_payload else 0.5
    feedback = "Result received" if result_payload else "No result payload provided"

    return {
        "task": task,
        "score": round(score, 2),
        "feedback": feedback,
        "result_echo": result_payload,
    }


def parse_context(context: str | None) -> Dict[str, Any]:
    if not context:
        return {}
    try:
        return json.loads(context)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise OrchestrationError(f"Invalid JSON context: {exc}") from exc


__all__ = ["OrchestrationError", "RouteDecision", "route_task", "evaluate_task", "parse_context"]
