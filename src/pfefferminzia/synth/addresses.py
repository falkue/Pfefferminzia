"""Adressen: reale PLZ/Orte aus ``geo/orte_*.csv``, ausschliesslich generierte Strassennamen."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

HAUSNUMMER_MAX = 180


@dataclass
class Ort:
    plz: str
    ort: str
    land: str
    region: str  # Kanton (CH) oder Bundesland-Kuerzel (DE)
    sprachregion: str  # de | fr | it
    tarifzone: str
    urbanitaet: str


@dataclass
class Adresse:
    strasse: str
    hausnummer: str
    plz: str
    ort: str
    land: str
    region: str
    sprache: str
    tarifzone: str

    def zeile(self) -> str:
        """Eine Zeile im Landesformat: ``Ahornweg 12, 4600 Olten`` bzw. ``Ahornweg 12, 10115 Berlin``."""
        return f"{self.strasse} {self.hausnummer}, {self.plz} {self.ort}"

    def block(self) -> str:
        return f"{self.strasse} {self.hausnummer}\n{self.plz} {self.ort}" + ("" if self.land == "CH" else "")


class AddressSynth:
    def __init__(self, orte_ch: pd.DataFrame, orte_de: pd.DataFrame, strassen: pd.DataFrame):
        self.orte = {"CH": orte_ch.reset_index(drop=True), "DE": orte_de.reset_index(drop=True)}
        for land, df in self.orte.items():
            fehlt = {"plz", "ort", "gewicht", "tarifzone", "urbanitaet"} - set(df.columns)
            if fehlt:
                raise ValueError(f"orte_{land.lower()}.csv: Spalten fehlen: {sorted(fehlt)}")
        if not {"strasse", "sprache", "typ"} <= set(strassen.columns):
            raise ValueError("strassennamen.csv: Spalten strasse, sprache, typ erwartet")
        self.strassen = strassen.reset_index(drop=True)

    def ort(self, rng: np.random.Generator, land: str, sprachregion: str | None = None,
            region: str | None = None) -> Ort:
        df = self.orte[land]
        if sprachregion and "sprachregion" in df.columns:
            df2 = df[df["sprachregion"] == sprachregion]
            df = df2 if not df2.empty else df
        if region:
            spalte = "kanton" if land == "CH" else "bundesland_kuerzel"
            df2 = df[df[spalte] == region]
            df = df2 if not df2.empty else df
        g = df["gewicht"].to_numpy(dtype=float)
        z = df.iloc[rng.choice(len(df), p=g / g.sum())]
        return Ort(
            plz=str(z["plz"]), ort=str(z["ort"]), land=land,
            region=str(z["kanton"] if land == "CH" else z["bundesland_kuerzel"]),
            sprachregion=str(z.get("sprachregion", "de")), tarifzone=str(z["tarifzone"]),
            urbanitaet=str(z["urbanitaet"]),
        )

    def strasse(self, rng: np.random.Generator, sprache: str) -> str:
        df = self.strassen[self.strassen["sprache"] == sprache]
        if df.empty:
            raise ValueError(f"Keine Strassennamen fuer Sprache {sprache!r}")
        return str(df.iloc[rng.integers(0, len(df))]["strasse"])

    @staticmethod
    def hausnummer(rng: np.random.Generator) -> str:
        n = int(rng.integers(1, HAUSNUMMER_MAX + 1))
        if rng.random() < 0.08:
            return f"{n}{'abc'[int(rng.integers(0, 3))]}"
        return str(n)

    def adresse(self, rng: np.random.Generator, land: str, sprachregion: str | None = None,
                region: str | None = None) -> Adresse:
        o = self.ort(rng, land, sprachregion, region)
        strassen_sprache = {"CH": {"de": "de-CH", "fr": "fr", "it": "it"}, "DE": {"de": "de-DE"}}[land].get(
            o.sprachregion, "de-CH" if land == "CH" else "de-DE"
        )
        return Adresse(
            strasse=self.strasse(rng, strassen_sprache), hausnummer=self.hausnummer(rng),
            plz=o.plz, ort=o.ort, land=land, region=o.region, sprache=o.sprachregion, tarifzone=o.tarifzone,
        )


def geo_versatz(rng: np.random.Generator, lat: float, lon: float, max_km: float = 1.5) -> tuple[float, float]:
    """Koordinaten = Ortsmittelpunkt + Zufallsversatz <= max_km, gerundet auf 3 Dezimalstellen."""
    r = max_km * np.sqrt(rng.random())
    w = rng.random() * 2 * np.pi
    dlat = r * np.cos(w) / 111.0
    dlon = r * np.sin(w) / (111.0 * max(np.cos(np.radians(lat)), 0.2))
    return round(lat + dlat, 3), round(lon + dlon, 3)
