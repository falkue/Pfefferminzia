"""Pydantic-Modelle fuer ``config/generator.yaml``.

Die Konfiguration ist die einzige Quelle fuer Seeds, Stichtage, Mengengeruest, Pfade und
Fallenparameter. Kennzahlen des Unternehmens stehen ausschliesslich in
``data/reference/kennzahlen_master.yaml`` und werden hier bewusst nicht modelliert.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from pfefferminzia.paths import default_config_path, find_project_root

Stufe = Literal["S", "M", "L"]
STUFEN: tuple[Stufe, ...] = ("S", "M", "L")


class SeedConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    master: int = Field(default=20250101, ge=0, lt=2**63)


class ZeitConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    stichtag: date = date(2025, 12, 31)
    closing: date = date(2025, 1, 1)
    altsystem_snapshot: date = date(2024, 12, 31)
    bewegungsdaten_von: date = date(2016, 1, 1)
    bewegungsdaten_bis: date = date(2025, 12, 31)
    finanzhistorie_von: date = date(2019, 1, 1)
    vertragsbeginn_leben_ab: date = date(1985, 1, 1)
    vertragsbeginn_haftpflicht_ab: date = date(2001, 1, 1)
    minzia_ab: date = date(2019, 1, 1)
    geburtsjahr_von: int = 1930
    geburtsjahr_bis: int = 2007

    @model_validator(mode="after")
    def _plausibel(self) -> ZeitConfig:
        if self.altsystem_snapshot >= self.closing:
            raise ValueError("altsystem_snapshot muss vor closing liegen")
        if self.closing > self.stichtag:
            raise ValueError("closing darf nicht nach stichtag liegen")
        if self.bewegungsdaten_von > self.bewegungsdaten_bis:
            raise ValueError("bewegungsdaten_von > bewegungsdaten_bis")
        if self.geburtsjahr_von > self.geburtsjahr_bis:
            raise ValueError("geburtsjahr_von > geburtsjahr_bis")
        return self


class MarktConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    anteil_ch: float = Field(default=0.47, ge=0, le=1)
    anteil_de: float = Field(default=0.53, ge=0, le=1)
    sprache_ch: dict[str, float] = Field(default_factory=lambda: {"de": 0.70, "fr": 0.23, "it": 0.07})
    dokumente_hp_ch: dict[str, float] = Field(default_factory=lambda: {"fr": 0.15, "it": 0.05})
    anteil_korrespondenz_en: float = Field(default=0.03, ge=0, le=1)

    @model_validator(mode="after")
    def _summen(self) -> MarktConfig:
        if abs(self.anteil_ch + self.anteil_de - 1.0) > 1e-6:
            raise ValueError("anteil_ch + anteil_de muss 1.0 ergeben")
        if abs(sum(self.sprache_ch.values()) - 1.0) > 1e-6:
            raise ValueError("sprache_ch muss sich zu 1.0 summieren")
        return self


class StufeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    faktor: float = Field(gt=0)
    dokumente_rendern: Literal["alle", "stichprobe", "keine"] = "stichprobe"
    formate: list[Literal["parquet", "csv", "sqlite", "xlsx"]] = Field(
        default_factory=lambda: ["parquet", "csv"]
    )
    mengen: dict[str, int] = Field(default_factory=dict)

    @field_validator("mengen")
    @classmethod
    def _nicht_negativ(cls, v: dict[str, int]) -> dict[str, int]:
        for k, n in v.items():
            if n < 0:
                raise ValueError(f"Menge {k} darf nicht negativ sein")
        return v

    def menge(self, name: str, default: int | None = None) -> int:
        if name in self.mengen:
            return self.mengen[name]
        if default is None:
            raise KeyError(f"Menge '{name}' ist fuer diese Stufe nicht konfiguriert")
        return default


class PfadeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reference: Path = Path("data/reference")
    raw: Path = Path("data/raw")
    curated: Path = Path("data/curated")
    truth: Path = Path("data/truth")
    sample: Path = Path("data/sample")
    documents: Path = Path("data/documents")
    communications: Path = Path("data/communications")
    llm_cache: Path = Path("data/cache/llm")
    manifest: Path = Path("data/manifest.json")
    templates: Path = Path("templates")
    prompts: Path = Path("prompts")

    def absolut(self, root: Path) -> PfadeConfig:
        """Liefert eine Kopie mit absoluten Pfaden relativ zu ``root``."""
        werte = {k: (root / v if not Path(v).is_absolute() else Path(v)) for k, v in self}
        return PfadeConfig(**werte)


class FallenConfig(BaseModel):
    """Schalter (bool) und Staerkeparameter (0–1) der didaktischen Fallen.

    Weitere Fallen duerfen ohne Modellaenderung ergaenzt werden (``extra="allow"``).
    """

    model_config = ConfigDict(extra="allow")
    underwriting_bias: float = Field(default=0.6, ge=0, le=1)
    leakage: bool = True
    avb_versionskonflikt: bool = True
    gesundheitsdaten_freitext: float = Field(default=0.15, ge=0, le=1)
    drift: bool = True
    prompt_injection: float = Field(default=0.01, ge=0, le=1)
    survivorship_bias: bool = True
    rueckschlussrisiko: bool = True
    mandatsueberschreitung: float = Field(default=0.015, ge=0, le=1)
    legitime_betrugsmuster: bool = True
    tarifabweichung: float = Field(default=0.04, ge=0, le=1)
    chatbot_nur_minzia_avb: bool = True
    betrugsflag_sichtbar_bis: date = date(2022, 12, 31)
    saubere_variante: bool = False

    def aktiv(self, name: str) -> bool:
        """True, wenn die Falle eingeschaltet ist (bool True oder Staerke > 0) und keine saubere Variante laeuft."""
        if self.saubere_variante:
            return False
        wert = getattr(self, name, None)
        if wert is None and self.model_extra:
            wert = self.model_extra.get(name)
        if isinstance(wert, bool):
            return wert
        if isinstance(wert, int | float):
            return wert > 0
        return False

    def staerke(self, name: str) -> float:
        if not self.aktiv(name):
            return 0.0
        wert = getattr(self, name, None)
        if wert is None and self.model_extra:
            wert = self.model_extra.get(name)
        if isinstance(wert, bool):
            return 1.0 if wert else 0.0
        return float(wert or 0.0)


class DqConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    aktiv: bool = True
    raten: dict[str, float] = Field(default_factory=dict)

    @field_validator("raten")
    @classmethod
    def _bereich(cls, v: dict[str, float]) -> dict[str, float]:
        for k, r in v.items():
            if not 0 <= r <= 1:
                raise ValueError(f"DQ-Rate {k} muss zwischen 0 und 1 liegen")
        return v


class LlmConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    modus: Literal["cached", "refresh", "template"] = "cached"
    modell: str = "platzhalter"
    prompt_version: str = "0.1"
    temperatur: float = Field(default=0.7, ge=0, le=2)
    cache_pfad: Path = Path("data/cache/llm")


class ExportConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    csv_bom: bool = True
    csv_zeilenende: str = "\n"
    parquet_kompression: Literal["snappy", "zstd", "gzip", "none"] = "snappy"
    parquet_ohne_zeitstempel: bool = True


class GeneratorConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "0.1.0"
    schema_version: str = "0.1.0"
    seed: SeedConfig = Field(default_factory=SeedConfig)
    zeit: ZeitConfig = Field(default_factory=ZeitConfig)
    markt: MarktConfig = Field(default_factory=MarktConfig)
    stufen: dict[Stufe, StufeConfig]
    pfade: PfadeConfig = Field(default_factory=PfadeConfig)
    fallen: FallenConfig = Field(default_factory=FallenConfig)
    dq: DqConfig = Field(default_factory=DqConfig)
    llm: LlmConfig = Field(default_factory=LlmConfig)
    export: ExportConfig = Field(default_factory=ExportConfig)

    @field_validator("stufen")
    @classmethod
    def _alle_stufen(cls, v: dict[Stufe, StufeConfig]) -> dict[Stufe, StufeConfig]:
        fehlend = [s for s in STUFEN if s not in v]
        if fehlend:
            raise ValueError(f"Stufen fehlen in der Konfiguration: {fehlend}")
        return v

    @model_validator(mode="after")
    def _teilbaum(self) -> GeneratorConfig:
        """S ⊂ M ⊂ L: Mengen duerfen mit der Stufe nicht sinken (ausser Rendering-Mengen)."""
        ausnahmen = {"dokumente_gerendert", "interaktionen_gerendert"}
        for kleiner, groesser in (("S", "M"), ("M", "L")):
            a, b = self.stufen[kleiner].mengen, self.stufen[groesser].mengen
            for k, n in a.items():
                if k in ausnahmen or k not in b:
                    continue
                if b[k] < n:
                    raise ValueError(f"Menge {k}: Stufe {groesser} ({b[k]}) < Stufe {kleiner} ({n})")
        return self

    @property
    def master_seed(self) -> int:
        return self.seed.master

    def stufe(self, name: str) -> StufeConfig:
        if name not in self.stufen:
            raise KeyError(f"Unbekannte Stufe '{name}', erlaubt: {list(self.stufen)}")
        return self.stufen[name]  # type: ignore[index]


def load_config(path: Path | str | None = None, root: Path | None = None) -> GeneratorConfig:
    """Laedt und validiert die Generator-Konfiguration."""
    root = root or find_project_root()
    cfg_path = Path(path) if path else default_config_path(root)
    if not cfg_path.exists():
        raise FileNotFoundError(f"Konfiguration nicht gefunden: {cfg_path}")
    with cfg_path.open("r", encoding="utf-8") as fh:
        daten = yaml.safe_load(fh) or {}
    return GeneratorConfig.model_validate(daten)
