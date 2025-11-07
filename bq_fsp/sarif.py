"""SARIF helpers for bq-fsp."""
from __future__ import annotations

from typing import Iterable

from .scanner import Finding


def to_sarif(findings: Iterable[Finding], tool_name: str = "bq-fsp", version: str = "0.1.0") -> dict:
    """Convert findings into a SARIF 2.1.0 document."""

    rules_meta: dict[str, dict] = {}
    results: list[dict] = []

    for finding in findings:
        rules_meta.setdefault(
            finding.rule_id,
            {
                "id": finding.rule_id,
                "shortDescription": {"text": finding.message},
            },
        )
        results.append(
            {
                "ruleId": finding.rule_id,
                "message": {"text": finding.message},
                "level": "error" if finding.severity.upper() == "HIGH" else "warning",
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": finding.file},
                            "region": {"startLine": finding.line},
                        }
                    }
                ],
                "fingerprints": {"sha1": finding.hash},
            }
        )

    return {
        "version": "2.1.0",
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": tool_name,
                        "version": version,
                        "rules": list(rules_meta.values()),
                    }
                },
                "results": results,
            }
        ],
    }


__all__ = ["to_sarif"]
