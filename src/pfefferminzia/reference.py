"""Loader fuer Referenzdaten unter ``data/reference/`` (CSV und YAML) mit Caching.

Der Loader kennt die vereinbarten Dateien (Katalog ``REFERENZEN``), setzt aber keine davon voraus:
fehlende Dateien fuehren erst beim Zugriff zu einer ``ReferenzFehltError`` mit klarem Hinweis,
welche Datei von welchem Team erwartet wird.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

# Spalten, die immer als Text gelesen werden (fuehrende Nullen, Codes)
TEXT_SPALTEN: frozenset[str] = frozenset(
    {"plz", "plz_von", "plz_bis", "code", "kanton", "bundesland_kuerzel", "tarifzone", "org_einheit_id",
     "parent_id", "standort_id", "system_id", "persona_id", "mitarbeiter_id", "partner_id"}
)


class ReferenzFehltError(FileNotFoundError):
    """Eine erwartete Referenzdatei ist (noch) nicht vorhanden."""


@dataclass(frozen=True)
class ReferenzEintrag:
    schluessel: str
    relpfad: str
    art: str  # csv | yaml | glob
    team: str
    pflicht_ab_stufe: str  # Pipeline-Stufe, ab der die Datei benoetigt wird
    beschreibung: str


REFERENZEN: dict[str, ReferenzEintrag] = {
    e.schluessel: e
    for e in [
        # Welle 0, dieses Team
        ReferenzEintrag("geo.orte_ch", "geo/orte_ch.csv", "csv", "Generator", "partner",
                        "Schweizer Orte mit PLZ, Kanton, Sprachregion, Gewicht, Tarifzone"),
        ReferenzEintrag("geo.orte_de", "geo/orte_de.csv", "csv", "Generator", "partner",
                        "Deutsche Orte mit PLZ, Bundesland, Gewicht, Tarifzone"),
        ReferenzEintrag("geo.strassennamen", "geo/strassennamen.csv", "csv", "Generator", "partner",
                        "Generierte, fiktive Strassennamen je Sprache"),
        ReferenzEintrag("namen.vornamen", "namen/vornamen.csv", "csv", "Generator", "partner",
                        "Vornamen mit Geschlecht, Sprachraum und Dekadengewichten"),
        ReferenzEintrag("namen.nachnamen", "namen/nachnamen.csv", "csv", "Generator", "partner",
                        "Nachnamen mit Sprachraum und Gewicht"),
        ReferenzEintrag("namen.firmennamen_bausteine", "namen/firmennamen_bausteine.csv", "csv",
                        "Generator", "partner", "Bausteine fuer fiktive KMU-Namen"),
        ReferenzEintrag("namen.blocklist", "namen/blocklist.csv", "csv", "Generator", "validate",
                        "Blocklist realer Personen und Firmen"),
        # Welle 0, andere Teams (Pfade werden hier nicht angefasst)
        ReferenzEintrag("kennzahlen_master", "kennzahlen_master.yaml", "yaml", "Unternehmen",
                        "organisation", "Kennzahlen-Masterdatei (einzige Quelle aller Zahlen)"),
        ReferenzEintrag("organisationseinheiten", "organisationseinheiten.csv", "csv", "Unternehmen",
                        "organisation", "Organisationseinheiten (3 Ebenen)"),
        ReferenzEintrag("standorte", "standorte.csv", "csv", "Unternehmen", "organisation",
                        "Standorte der Gruppe"),
        ReferenzEintrag("systeme", "systeme.csv", "csv", "Unternehmen", "organisation",
                        "IT-Systeme VERA, HAPO, SILAS, DOKU, MINT, Herbarium"),
        ReferenzEintrag("personas", "personas_*.csv", "glob", "Unternehmen", "organisation",
                        "Persona-Rollenkarten (Mitarbeiter, Kunden)"),
        ReferenzEintrag("hp", "hp/", "dir", "Haftpflicht", "vertrag",
                        "Produkt-, Tarif- und Kodierungsreferenzen Haftpflicht"),
        ReferenzEintrag("lv", "lv/", "dir", "Leben", "vertrag",
                        "Produkt-, Tarif- und Kodierungsreferenzen Leben"),
    ]
}


@dataclass
class ReferenzStatus:
    schluessel: str
    pfad: Path
    vorhanden: bool
    zeilen: int | None
    team: str
    pflicht_ab_stufe: str
    hinweis: str = ""


class ReferenceLoader:
    """Laedt CSV/YAML aus ``data/reference/`` und cacht die Ergebnisse im Speicher."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self._cache: dict[str, Any] = {}

    # -- Pfade -----------------------------------------------------------------
    def pfad(self, schluessel_oder_relpfad: str) -> Path:
        eintrag = REFERENZEN.get(schluessel_oder_relpfad)
        rel = eintrag.relpfad if eintrag else schluessel_oder_relpfad
        return self.root / rel

    def vorhanden(self, schluessel_oder_relpfad: str) -> bool:
        p = self.pfad(schluessel_oder_relpfad)
        if "*" in p.name:
            return any(p.parent.glob(p.name))
        return p.exists()

    def _fehlt(self, schluessel: str, pfad: Path) -> ReferenzFehltError:
        eintrag = REFERENZEN.get(schluessel)
        if eintrag:
            return ReferenzFehltError(
                f"Referenzdatei fehlt: {pfad} (Schluessel '{schluessel}', Team {eintrag.team}, "
                f"benoetigt ab Stufe '{eintrag.pflicht_ab_stufe}': {eintrag.beschreibung})"
            )
        return ReferenzFehltError(f"Referenzdatei fehlt: {pfad}")

    # -- Laden -----------------------------------------------------------------
    def csv(self, schluessel_oder_relpfad: str, **kwargs) -> pd.DataFrame:
        """Liest eine CSV (UTF-8, optional BOM) als DataFrame; Textspalten bleiben Text."""
        pfad = self.pfad(schluessel_oder_relpfad)
        key = f"csv:{pfad}"
        if key in self._cache:
            return self._cache[key]
        if not pfad.exists():
            raise self._fehlt(schluessel_oder_relpfad, pfad)
        kopf = pd.read_csv(pfad, encoding="utf-8-sig", nrows=0).columns
        dtype = {c: "string" for c in kopf if c in TEXT_SPALTEN}
        dtype.update(kwargs.pop("dtype", {}) or {})
        df = pd.read_csv(pfad, encoding="utf-8-sig", dtype=dtype, keep_default_na=True, **kwargs)
        self._cache[key] = df
        return df

    def yaml(self, schluessel_oder_relpfad: str) -> dict[str, Any]:
        pfad = self.pfad(schluessel_oder_relpfad)
        key = f"yaml:{pfad}"
        if key in self._cache:
            return self._cache[key]
        if not pfad.exists():
            raise self._fehlt(schluessel_oder_relpfad, pfad)
        with pfad.open("r", encoding="utf-8") as fh:
            daten = yaml.safe_load(fh) or {}
        if not isinstance(daten, dict):
            raise ValueError(f"YAML-Referenz {pfad} muss ein Mapping auf oberster Ebene sein")
        self._cache[key] = daten
        return daten

    def glob(self, schluessel_oder_muster: str) -> dict[str, pd.DataFrame]:
        """Laedt alle CSVs eines Musters (z. B. ``personas_*.csv``) als Dict Dateiname -> DataFrame."""
        p = self.pfad(schluessel_oder_muster)
        dateien = sorted(p.parent.glob(p.name))
        if not dateien:
            raise self._fehlt(schluessel_oder_muster, p)
        return {d.stem: self.csv(d.relative_to(self.root).as_posix()) for d in dateien}

    def verzeichnis(self, schluessel_oder_relpfad: str) -> dict[str, pd.DataFrame]:
        """Laedt alle CSVs eines Unterordners (z. B. ``hp/``)."""
        p = self.pfad(schluessel_oder_relpfad)
        if not p.is_dir():
            raise self._fehlt(schluessel_oder_relpfad, p)
        return {d.stem: self.csv(d.relative_to(self.root).as_posix()) for d in sorted(p.glob("*.csv"))}

    def load(self, schluessel: str) -> Any:
        """Laedt einen Katalogeintrag passend zu seiner Art."""
        eintrag = REFERENZEN[schluessel]
        if eintrag.art == "csv":
            return self.csv(schluessel)
        if eintrag.art == "yaml":
            return self.yaml(schluessel)
        if eintrag.art == "glob":
            return self.glob(schluessel)
        if eintrag.art == "dir":
            return self.verzeichnis(schluessel)
        raise ValueError(f"Unbekannte Art {eintrag.art}")

    def leeren(self) -> None:
        self._cache.clear()

    # -- Pruefung --------------------------------------------------------------
    def status(self) -> list[ReferenzStatus]:
        """Status aller Katalogeintraege (vorhanden, Zeilenzahl, Hinweis)."""
        out: list[ReferenzStatus] = []
        for e in REFERENZEN.values():
            pfad = self.pfad(e.schluessel)
            vorhanden = self.vorhanden(e.schluessel) if e.art != "dir" else pfad.is_dir()
            zeilen: int | None = None
            hinweis = ""
            if vorhanden:
                try:
                    daten = self.load(e.schluessel)
                    if isinstance(daten, pd.DataFrame):
                        zeilen = len(daten)
                    elif isinstance(daten, dict):
                        zeilen = len(daten)
                except Exception as exc:  # noqa: BLE001 – Status soll nie abbrechen
                    hinweis = f"Fehler beim Laden: {exc}"
            else:
                hinweis = f"fehlt (Team {e.team}, benoetigt ab Stufe {e.pflicht_ab_stufe})"
            out.append(ReferenzStatus(e.schluessel, pfad, vorhanden, zeilen, e.team,
                                      e.pflicht_ab_stufe, hinweis))
        return out
