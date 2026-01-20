# Architecture

## Core CLI
- Built with [Typer](https://typer.tiangolo.com/) providing the `blux` command.
- Commands implement request creation, routing, and audit previews.

## Plugin Loader
- Discovers entry points published under `blux.plugins`.
- Mounts Typer applications dynamically beneath the root CLI namespace.

## Telemetry Subsystem
- Writes JSONL events and mirrors to SQLite for durability.
- Exposes Prometheus metrics via an in-process registry for external exporters.
- Controlled through `BLUXQ_TELEMETRY` and `BLUXQ_TELEMETRY_WARN` environment variables.

## Configuration
- Supports layered configuration: environment variables, user config directory, and local project files.
- YAML-based configuration merged with dictionary semantics.

## Ecosystem Map
- Guard and Lite extend the ecosystem alongside cA.
- Additional products can publish entry points to join the command surface without modifying the core CLI.
