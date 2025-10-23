# Contributing

## Development Workflow
1. Create a virtual environment with Python 3.9+.
2. Install dependencies: `pip install -e .[dev]`.
3. Run format and lint checks: `ruff check .` and `mypy blux_quantum`.
4. Execute tests: `pytest`.

## Commit Guidelines
- Use descriptive commit messages (e.g., `[QUANTUM]` prefix for major changes).
- Include relevant documentation updates for new features.

## Pull Requests
- Ensure CI checks pass before requesting review.
- Update the README file tree via `python scripts/update_readme_filetree.py` when adding files.
- Provide context for telemetry or security-sensitive changes.

## Code Style
- Follow Ruff and Mypy guidance.
- Avoid broad exception handling without logging context.
