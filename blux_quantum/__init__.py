"""BLUX Quantum package initialization."""
from importlib.metadata import PackageNotFoundError, version

__all__ = ["__version__"]

try:  # pragma: no cover - fallback for editable installs
    __version__ = version("blux-quantum")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"
