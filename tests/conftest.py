from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def config():
    from pfefferminzia.config import load_config

    return load_config(root=ROOT)


@pytest.fixture()
def ctx(tmp_path, monkeypatch):
    """RunContext mit Ausgabepfaden im tmp-Ordner, Referenzen aus dem Projekt."""
    from pfefferminzia.context import RunContext

    c = RunContext.erstellen(stufe="S", root=ROOT)
    c.config.pfade.curated = tmp_path / "curated"
    c.config.pfade.truth = tmp_path / "truth"
    c.config.pfade.raw = tmp_path / "raw"
    c.config.pfade.sample = tmp_path / "sample"
    c.config.pfade.manifest = tmp_path / "manifest.json"
    return c
