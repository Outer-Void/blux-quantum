# Architecture

## Core CLI
- Built with [Typer](https://typer.tiangolo.com/) providing the `bluxq` command.
- Commands implement health checks, stability toggles, telemetry triggers, and plugin enumeration.

## Plugin Loader
- Discovers entry points published under `blux.plugins`.
- Provides built-in examples for Guard, Lite, and Doctrine modules.
- Mounts Typer applications dynamically beneath the root CLI namespace.

## Telemetry Subsystem
- Writes JSONL events and mirrors to SQLite for durability.
- Exposes Prometheus metrics via an in-process registry for external exporters.
- Controlled through `BLUXQ_TELEMETRY` and `BLUXQ_TELEMETRY_WARN` environment variables.

## Configuration
- Supports layered configuration: environment variables, user config directory, and local project files.
- YAML-based configuration merged with dictionary semantics.

## Stability Mode
- Provides enable/disable hooks that emit telemetry events.
- Designed for future integration with Guard/Commander quiesce and lockdown features.

## Ecosystem Map
- Guard, Lite, Doctrine examples showcase how ecosystem services extend `bluxq`.
- Additional products can publish entry points to join the command surface without modifying the core CLI.
