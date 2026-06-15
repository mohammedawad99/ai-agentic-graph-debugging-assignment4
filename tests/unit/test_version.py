"""Guard: the package version is exposed and starts at 1.00, in sync with pyproject.toml."""

from __future__ import annotations

from pathlib import Path

import tomllib

import ex04_graph_debugger
from ex04_graph_debugger.version import __version__


def test_version_is_one_point_zero_zero() -> None:
    assert __version__ == "1.00"


def test_package_exposes_version() -> None:
    assert ex04_graph_debugger.__version__ == __version__


def test_pyproject_version_matches_package() -> None:
    root = Path(__file__).resolve().parents[2]
    data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["version"] == __version__
