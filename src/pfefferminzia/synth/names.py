"""Namensziehung aus den kuratierten Listen ``data/reference/namen/``.

Vornamen werden nach Geschlecht, Sprachraum und Geburtsjahrzehnt gewichtet (Spalten ``g_1930`` …
``g_2000``), Nachnamen nach Sprachraum und Gewicht. Kombinationen auf der Blocklist werden verworfen.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from pfefferminzia.validate.fiction import Blocklist

DEKADEN = tuple(range(1930, 2010, 10))
SPRACHRAEUME = ("de-CH", "de-DE", "fr", "it", "international")


def dekade(geburtsjahr: int) -> int:
    return int(min(max(geburtsjahr // 10 * 10, DEKADEN[0]), DEKADEN[-1]))


@dataclass
class Person:
    vorname: str
    nachname: str
    geschlecht: str
    sprachraum: str


class NameSynth:
    def __init__(self, vornamen: pd.DataFrame, nachnamen: pd.DataFrame, blocklist: Blocklist | None = None,
                 anteil_international: float = 0.12):
        pflicht_v = {"vorname", "geschlecht", "sprachraum", *[f"g_{d}" for d in DEKADEN]}
        pflicht_n = {"nachname", "sprachraum", "gewicht"}
        if not pflicht_v <= set(vornamen.columns):
            raise ValueError(f"vornamen.csv: Spalten fehlen: {sorted(pflicht_v - set(vornamen.columns))}")
        if not pflicht_n <= set(nachnamen.columns):
            raise ValueError(f"nachnamen.csv: Spalten fehlen: {sorted(pflicht_n - set(nachnamen.columns))}")
        self.vornamen = vornamen.reset_index(drop=True)
        self.nachnamen = nachnamen.reset_index(drop=True)
        self.blocklist = blocklist or Blocklist(None)
        self.anteil_international = anteil_international

    @staticmethod
    def _ziehe(rng: np.random.Generator, df: pd.DataFrame, gewichte: np.ndarray) -> pd.Series:
        g = np.asarray(gewichte, dtype=float)
        if g.sum() <= 0 or len(df) == 0:
            raise ValueError("Keine Kandidaten mit positivem Gewicht")
        idx = rng.choice(len(df), p=g / g.sum())
        return df.iloc[idx]

    def vorname(self, rng: np.random.Generator, geschlecht: str, sprachraum: str, geburtsjahr: int) -> str:
        spalte = f"g_{dekade(geburtsjahr)}"
        kand = self.vornamen[(self.vornamen["geschlecht"].isin([geschlecht, "U"]))
                             & (self.vornamen["sprachraum"] == sprachraum)]
        if kand.empty or kand[spalte].sum() <= 0:
            kand = self.vornamen[self.vornamen["geschlecht"].isin([geschlecht, "U"])]
        return str(self._ziehe(rng, kand, kand[spalte].to_numpy())["vorname"])

    def nachname(self, rng: np.random.Generator, sprachraum: str) -> str:
        kand = self.nachnamen[self.nachnamen["sprachraum"] == sprachraum]
        if kand.empty:
            kand = self.nachnamen
        return str(self._ziehe(rng, kand, kand["gewicht"].to_numpy())["nachname"])

    def sprachraum(self, rng: np.random.Generator, land: str, sprache: str = "de") -> str:
        """Sprachraum des Namens aus Wohnsitzland und Korrespondenzsprache, mit Migrationsanteil."""
        if rng.random() < self.anteil_international:
            return "international"
        if land == "CH":
            return {"de": "de-CH", "fr": "fr", "it": "it"}.get(sprache, "de-CH")
        return "de-DE"

    def person(self, rng: np.random.Generator, geschlecht: str, land: str, geburtsjahr: int,
               sprache: str = "de", max_versuche: int = 20) -> Person:
        """Zieht eine Person; Blocklist-Treffer werden neu gezogen."""
        for _ in range(max_versuche):
            sr = self.sprachraum(rng, land, sprache)
            sr_nach = sr if rng.random() < 0.85 else self.sprachraum(rng, land, sprache)
            v, n = self.vorname(rng, geschlecht, sr, geburtsjahr), self.nachname(rng, sr_nach)
            if not self.blocklist.person_gesperrt(v, n):
                return Person(v, n, geschlecht, sr)
        raise RuntimeError("Blocklist blockiert alle gezogenen Namen – Listen pruefen")


def firmenname(rng: np.random.Generator, bausteine: pd.DataFrame, land: str,
               blocklist: Blocklist | None = None, branche: str | None = None) -> str:
    """Fiktiver KMU-Name ``<Stamm> <Branche> <Rechtsform>`` aus ``firmennamen_bausteine.csv``."""
    b = bausteine
    def pool(art: str, **filt) -> pd.DataFrame:
        k = b[b["art"] == art]
        for sp, wert in filt.items():
            if sp in k.columns and wert is not None:
                k2 = k[(k[sp] == wert) | (k[sp].isna()) | (k[sp] == "")]
                k = k2 if not k2.empty else k
        return k

    for _ in range(20):
        stamm = pool("stamm", land=land)
        br = pool("branche", land=land)
        if branche is not None and "branche" in br.columns:
            br2 = br[br["branche"] == branche]
            br = br2 if not br2.empty else br
        rf = pool("rechtsform", land=land)
        teile = [
            str(stamm.iloc[rng.integers(0, len(stamm))]["wert"]),
            str(br.iloc[rng.integers(0, len(br))]["wert"]),
        ]
        if rng.random() < 0.85:
            teile.append(str(rf.iloc[rng.integers(0, len(rf))]["wert"]))
        name = " ".join(teile)
        if blocklist is None or not blocklist.firma_gesperrt(name):
            return name
    raise RuntimeError("Kein zulaessiger Firmenname gefunden")
