"""Projektwurzel und Standardpfade.

Die Projektwurzel wird ueber die Umgebungsvariable ``PFEFFERMINZIA_ROOT`` oder durch Suche nach
``pyproject.toml`` ab dem Arbeitsverzeichnis (bzw. ab dem Paketverzeichnis) ermittelt.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT_ENV = "PFEFFERMINZIA_ROOT"
DEFAULT_CONFIG = Path("config") / "generator.yaml"


def find_project_root(start: Path | None = None) -> Path:
    """Ermittelt die Projektwurzel (Ordner mit ``pyproject.toml``)."""
    env = os.environ.get(ROOT_ENV)
    if env:
        return Path(env).resolve()
    candidates = [start or Path.cwd(), Path(__file__).resolve()]
    for base in candidates:
        for folder in [base, *base.parents]:
            if (folder / "pyproject.toml").exists():
                return folder
    return Path.cwd().resolve()


def default_config_path(root: Path | None = None) -> Path:
    return (root or find_project_root()) / DEFAULT_CONFIG
