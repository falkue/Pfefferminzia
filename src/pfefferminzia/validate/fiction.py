"""Fiktionalitaets-Checks: Blocklist, Domains, Telefonnummern (Konventionen §1, Datenarchitektur 6)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pandas as pd

from pfefferminzia.validate.registry import CheckErgebnis, check

if TYPE_CHECKING:
    from pfefferminzia.context import RunContext

ERLAUBTE_DOMAINS = ("pfefferminzia.example", "minzia.example", "pfefferminz.example")
DOMAIN_RE = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
URL_RE = re.compile(r"https?://([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
TELEFON_RE = re.compile(r"\+(?:41|49)[\d\s]{8,16}")
TELEFON_FIKTIV_RE = re.compile(
    r"^(\+41 44 000 \d{2} \d{2}|\+49 30 23125 \d{3}|\+49 152 28817 \d{3})$"
)


def domain_erlaubt(domain: str) -> bool:
    return domain.lower().endswith(".example")


def telefon_fiktiv(nummer: str) -> bool:
    return bool(TELEFON_FIKTIV_RE.match(nummer.strip()))


def _normal(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().lower()


class Blocklist:
    """Blocklist aus ``namen/blocklist.csv``: Personen (Vorname+Nachname) und Firmen."""

    def __init__(self, df: pd.DataFrame | None):
        self.personen: set[tuple[str, str]] = set()
        self.firmen: set[str] = set()
        if df is None or df.empty:
            return
        for _, z in df.iterrows():
            if z.get("typ") == "person":
                self.personen.add((_normal(z.get("vorname", "")), _normal(z.get("nachname", ""))))
            elif z.get("typ") == "firma":
                self.firmen.add(_normal(z.get("name", "")))

    def person_gesperrt(self, vorname: str, nachname: str) -> bool:
        return (_normal(vorname), _normal(nachname)) in self.personen

    def firma_gesperrt(self, name: str) -> bool:
        n = _normal(name)
        return any(f and f in n for f in self.firmen)

    def __len__(self) -> int:
        return len(self.personen) + len(self.firmen)


def lade_blocklist(ctx: RunContext) -> Blocklist | None:
    if ctx.tabellen.has("namen_blocklist", "reference"):
        return Blocklist(ctx.tabellen.get("namen_blocklist", "reference"))
    if ctx.reference.vorhanden("namen.blocklist"):
        return Blocklist(ctx.reference.csv("namen.blocklist"))
    return None


@check("blocklist_personen", "Keine Vorname+Nachname-Kombination aus der Blocklist", klasse="fiktionalitaet",
       reihenfolge=30)
def blocklist_personen(ctx: RunContext, erg: CheckErgebnis) -> None:
    bl = lade_blocklist(ctx)
    if bl is None:
        erg.uebersprungen, erg.grund = True, "Blocklist nicht vorhanden"
        erg.warnung("namen/blocklist.csv fehlt – Check uebersprungen")
        return
    for key, df in ctx.tabellen.alle().items():
        if key.startswith("reference/"):
            continue
        if {"vorname", "nachname"} <= set(df.columns):
            paare = zip(df["vorname"].fillna("").astype(str), df["nachname"].fillna("").astype(str),
                        strict=True)
            treffer = sum(1 for v, n in paare if bl.person_gesperrt(v, n))
            if treffer:
                erg.fehler(f"{treffer} Personen auf der Blocklist", tabelle=key, anzahl=treffer)
        if "firmenname" in df.columns:
            firmen = df["firmenname"].dropna().astype(str)
            n = int(firmen.map(bl.firma_gesperrt).sum())
            if n:
                erg.fehler(f"{n} Firmennamen enthalten gesperrte Marken", tabelle=key, anzahl=n)
    erg.info(f"Blocklist mit {len(bl.personen)} Personen und {len(bl.firmen)} Firmen angewendet")


@check("domains_telefon", "Nur .example-Domains und Fiktions-Telefonnummern", klasse="fiktionalitaet",
       reihenfolge=31)
def domains_telefon(ctx: RunContext, erg: CheckErgebnis) -> None:
    for key, df in ctx.tabellen.alle().items():
        if key.startswith("reference/"):
            continue
        for spalte in df.columns:
            s = df[spalte]
            if not (pd.api.types.is_string_dtype(s) or pd.api.types.is_object_dtype(s)):
                continue
            werte = s.dropna().astype(str)
            if werte.empty:
                continue
            for m in werte.str.extractall(DOMAIN_RE)[0].tolist() + werte.str.extractall(URL_RE)[0].tolist():
                if not domain_erlaubt(m):
                    erg.fehler(f"Nicht-fiktive Domain {m!r}", tabelle=key, spalte=spalte)
            if "telefon" in spalte or "mobil" in spalte or "phone" in spalte:
                schlecht = werte[~werte.map(telefon_fiktiv)]
                if len(schlecht):
                    erg.fehler(f"{len(schlecht)} Telefonnummern ausserhalb der Fiktionsbereiche "
                               f"(z. B. {schlecht.iloc[0]!r})", tabelle=key, spalte=spalte,
                               anzahl=int(len(schlecht)))
