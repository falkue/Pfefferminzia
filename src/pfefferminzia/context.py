"""Laufkontext des Generators: Konfiguration, Stufe, Pfade, Tabellen-Registry, Manifest."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from pfefferminzia.config import GeneratorConfig, StufeConfig, load_config
from pfefferminzia.manifest import Manifest
from pfefferminzia.paths import find_project_root
from pfefferminzia.reference import ReferenceLoader
from pfefferminzia.seeds import derive_seed, rng_for

log = logging.getLogger("pfefferminzia")


@dataclass
class TabellenRegistry:
    """Tabellen im Speicher, adressiert als ``<layer>/<name>`` (Layer-Default: curated)."""

    _tabellen: dict[str, pd.DataFrame] = field(default_factory=dict)

    @staticmethod
    def _key(name: str, layer: str) -> str:
        return name if "/" in name else f"{layer}/{name}"

    def register(self, name: str, df: pd.DataFrame, layer: str = "curated", ersetzen: bool = False) -> None:
        key = self._key(name, layer)
        if key in self._tabellen and not ersetzen:
            raise KeyError(f"Tabelle {key} ist bereits registriert (ersetzen=True zum Ueberschreiben)")
        self._tabellen[key] = df

    def get(self, name: str, layer: str = "curated") -> pd.DataFrame:
        key = self._key(name, layer)
        if key not in self._tabellen:
            raise KeyError(f"Tabelle {key} nicht registriert; vorhanden: {sorted(self._tabellen)}")
        return self._tabellen[key]

    def has(self, name: str, layer: str = "curated") -> bool:
        return self._key(name, layer) in self._tabellen

    def alle(self, layer: str | None = None) -> dict[str, pd.DataFrame]:
        if layer is None:
            return dict(self._tabellen)
        return {k: v for k, v in self._tabellen.items() if k.startswith(f"{layer}/")}

    def __len__(self) -> int:
        return len(self._tabellen)


@dataclass
class RunContext:
    config: GeneratorConfig
    stufe: str
    root: Path
    tabellen: TabellenRegistry = field(default_factory=TabellenRegistry)
    manifest: Manifest | None = None
    ereignisse: list[dict[str, Any]] = field(default_factory=list)
    _reference: ReferenceLoader | None = None

    # -- Fabrik ----------------------------------------------------------------
    @classmethod
    def erstellen(
        cls, stufe: str = "S", config_pfad: Path | str | None = None, root: Path | None = None
    ) -> RunContext:
        root = Path(root) if root else find_project_root()
        cfg = load_config(config_pfad, root)
        cfg.stufe(stufe)  # validiert die Stufe
        ctx = cls(config=cfg, stufe=stufe, root=root)
        ctx.manifest = Manifest(
            version=cfg.version,
            schema_version=cfg.schema_version,
            scale=stufe,
            stichtag=cfg.zeit.stichtag.isoformat(),
            master_seed=cfg.master_seed,
            config_version=cfg.version,
        )
        return ctx

    # -- Eigenschaften ---------------------------------------------------------
    @property
    def stufe_config(self) -> StufeConfig:
        return self.config.stufe(self.stufe)

    @property
    def master_seed(self) -> int:
        return self.config.master_seed

    @property
    def pfade(self):
        return self.config.pfade.absolut(self.root)

    @property
    def reference(self) -> ReferenceLoader:
        if self._reference is None:
            self._reference = ReferenceLoader(self.pfade.reference)
        return self._reference

    def ausgabe_dir(self, layer: str) -> Path:
        """Ausgabeordner je Schicht; Stufe S schreibt nach ``sample``, sonst ``<layer>/<stufe>``."""
        basis = {
            "curated": self.pfade.curated,
            "raw": self.pfade.raw,
            "truth": self.pfade.truth,
            "sample": self.pfade.sample,
            "reference": self.pfade.reference,
            "migration": self.pfade.migration,
        }[layer]
        return basis / self.stufe

    def menge(self, name: str, default: int | None = None) -> int:
        return self.stufe_config.menge(name, default)

    # -- Zufall ----------------------------------------------------------------
    def seed(self, modul: str, entity_id: Any) -> int:
        return derive_seed(modul, entity_id, self.master_seed)

    def rng(self, modul: str, entity_id: Any) -> np.random.Generator:
        return rng_for(modul, entity_id, self.master_seed)

    # -- Protokoll -------------------------------------------------------------
    def ereignis(self, stufe: str, meldung: str, **daten: Any) -> None:
        self.ereignisse.append({"stufe": stufe, "meldung": meldung, **daten})
        log.info("[%s] %s", stufe, meldung)
