"""ID-Generatoren fuer alle Praefixe aus docs/konventionen.md §4.

curated-IDs sind ueber Generatorlaeufe und Groessenstufen stabil: sie werden aus einer laufenden
Nummer gebildet, nie aus Zufall. Legacy-Formate (VERA, HAPO, SILAS, DOKU) und MINT-UUIDs werden
deterministisch aus Seeds bzw. Nummern abgeleitet.
"""

from __future__ import annotations

import re
import uuid
from typing import Any

from pfefferminzia.seeds import MASTER_SEED, rng_for

# ---------------------------------------------------------------------------
# curated: Praefix + Bindestrich + feste Ziffernzahl
# ---------------------------------------------------------------------------

PRAEFIXE: dict[str, tuple[str, int]] = {
    "partner": ("PTR", 8),
    "vertrag": ("VTR", 8),
    "antrag": ("ANT", 8),
    "schaden": ("SCH", 8),
    "dokument": ("DOK", 8),
    "interaktion": ("INT", 8),
    "mitarbeiter": ("MIT", 5),
    "vermittler": ("VRM", 5),
    "agentur": ("AGT", 4),
}

PRODUKTE: tuple[str, ...] = (
    "HP-PRIV", "HP-BETR", "HP-BERUF", "LV-RISK", "LV-VORS", "LV-RENTE", "LV-EU",
)
TARIFGENERATIONEN_HP: tuple[str, ...] = ("HP-KLASSIK", "HP-MODERN", "MZ-DIRECT", "PM-2025")
TARIFGENERATIONEN_LV: tuple[str, ...] = (
    "PK-85", "PK-95", "PK-2000", "PK-2004", "PK-2007",
    "PL-2012", "PL-2015", "PL-2017", "MZ-2020", "PZ-2025",
)

_ID_RE = re.compile(r"^(?P<praefix>[A-Z]{3})-(?P<nummer>\d+)$")


def curated_id(entitaet: str, nummer: int) -> str:
    """Bildet eine curated-ID, z. B. ``curated_id("partner", 12345) == "PTR-00012345"``."""
    if entitaet not in PRAEFIXE:
        raise KeyError(f"Unbekannte Entitaet '{entitaet}', erlaubt: {sorted(PRAEFIXE)}")
    praefix, breite = PRAEFIXE[entitaet]
    if nummer < 0 or nummer >= 10**breite:
        raise ValueError(f"Nummer {nummer} ausserhalb des Bereichs 0..{10**breite - 1} fuer {praefix}")
    return f"{praefix}-{nummer:0{breite}d}"


def partner_id(n: int) -> str:
    return curated_id("partner", n)


def vertrag_id(n: int) -> str:
    return curated_id("vertrag", n)


def antrag_id(n: int) -> str:
    return curated_id("antrag", n)


def schaden_id(n: int) -> str:
    return curated_id("schaden", n)


def dokument_id(n: int) -> str:
    return curated_id("dokument", n)


def interaktion_id(n: int) -> str:
    return curated_id("interaktion", n)


def mitarbeiter_id(n: int) -> str:
    return curated_id("mitarbeiter", n)


def vermittler_id(n: int) -> str:
    return curated_id("vermittler", n)


def agentur_id(n: int) -> str:
    return curated_id("agentur", n)


def regelwerk_id(sparte: str, typ: str, markt: str, jahr: int) -> str:
    """``RW-HP-AVB-CH-2025``; sparte HP|LV|GRUPPE, markt CH|DE|GRUPPE."""
    if sparte not in {"HP", "LV", "GRUPPE"} or markt not in {"CH", "DE", "GRUPPE"}:
        raise ValueError("sparte muss HP|LV|GRUPPE, markt CH|DE|GRUPPE sein")
    return f"RW-{sparte}-{typ.upper()}-{markt}-{jahr}"


def parse_curated_id(wert: str) -> tuple[str, int]:
    """Zerlegt eine curated-ID in (Praefix, Nummer); ValueError bei falschem Format."""
    m = _ID_RE.match(wert)
    if not m:
        raise ValueError(f"Keine gueltige curated-ID: {wert!r}")
    praefix, nummer = m.group("praefix"), m.group("nummer")
    breiten = {p: b for p, b in PRAEFIXE.values()}
    if praefix not in breiten or len(nummer) != breiten[praefix]:
        raise ValueError(f"Praefix/Breite passt nicht: {wert!r}")
    return praefix, int(nummer)


def is_curated_id(wert: str, entitaet: str | None = None) -> bool:
    try:
        praefix, _ = parse_curated_id(wert)
    except ValueError:
        return False
    return entitaet is None or PRAEFIXE[entitaet][0] == praefix


# ---------------------------------------------------------------------------
# Pruefziffern
# ---------------------------------------------------------------------------

_MOD10_TABELLE = (0, 9, 4, 6, 8, 2, 7, 1, 3, 5)


def modulo10_rekursiv(ziffern: str) -> int:
    """Modulo-10-rekursiv (Schweizer ESR-Verfahren) fuer HAPO-Vertragsnummern."""
    uebertrag = 0
    for z in ziffern:
        if not z.isdigit():
            raise ValueError(f"Nur Ziffern erlaubt: {ziffern!r}")
        uebertrag = _MOD10_TABELLE[(uebertrag + int(z)) % 10]
    return (10 - uebertrag) % 10


# ---------------------------------------------------------------------------
# Legacy: VERA (Leben), HAPO (Haftpflicht), SILAS (Schaden), DOKU (Archiv)
# ---------------------------------------------------------------------------

_VERA_RE = re.compile(r"^L-(\d{7})$")
_HAPO_RE = re.compile(r"^(\d{2})\.(\d{3})\.(\d{3})-(\d)$")
_SILAS_RE = re.compile(r"^S(\d{4})/(\d{6})$")


def vera_vertragsnummer(n: int) -> str:
    """VERA-Vertragsnummer ``L-0098765`` (7 Ziffern)."""
    if not 0 <= n < 10**7:
        raise ValueError("VERA-Nummer muss 0..9999999 sein")
    return f"L-{n:07d}"


def hapo_vertragsnummer(n: int) -> str:
    """HAPO-Vertragsnummer ``40.987.112-3``: 8 Stammziffern in Gruppen 2.3.3 plus Pruefziffer."""
    if not 0 <= n < 10**8:
        raise ValueError("HAPO-Nummer muss 0..99999999 sein")
    stamm = f"{n:08d}"
    pz = modulo10_rekursiv(stamm)
    return f"{stamm[:2]}.{stamm[2:5]}.{stamm[5:8]}-{pz}"


def hapo_vertragsnummer_gueltig(wert: str) -> bool:
    m = _HAPO_RE.match(wert)
    if not m:
        return False
    stamm = "".join(m.groups()[:3])
    return modulo10_rekursiv(stamm) == int(m.group(4))


def silas_schadennummer(jahr: int, n: int) -> str:
    """SILAS-Schadennummer ``S2019/004512`` (Jahr + laufende Nummer, 6-stellig)."""
    if not 1900 <= jahr <= 2099 or not 0 <= n < 10**6:
        raise ValueError("Jahr 1900..2099 und Nummer 0..999999 erwartet")
    return f"S{jahr}/{n:06d}"


def doku_archivnummer(n: int) -> str:
    """DOKU-Archivnummer ``DOKU-0000123456`` (10 Ziffern)."""
    if not 0 <= n < 10**10:
        raise ValueError("DOKU-Nummer muss 0..9999999999 sein")
    return f"DOKU-{n:010d}"


# Eigene Nummernkreise je Altsystem (Konventionen §4: "je System eigener Kreis").
_LEGACY_PARTNER_OFFSET = {"VERA": 10_000_000, "HAPO": 20_000_000}


def legacy_partnernummer(system: str, n: int) -> str:
    """8-stellige numerische Partnernummer je Altsystem (VERA/HAPO), mit fuehrenden Nullen."""
    if system not in _LEGACY_PARTNER_OFFSET:
        raise KeyError("system muss VERA oder HAPO sein")
    if not 0 <= n < 10_000_000:
        raise ValueError("Legacy-Partnernummer muss 0..9999999 sein")
    return f"{_LEGACY_PARTNER_OFFSET[system] + n:08d}"


def personalnummer(n: int) -> str:
    """5-stellige Personalnummer (raw VERA/HAPO)."""
    if not 0 <= n < 10**5:
        raise ValueError("Personalnummer muss 0..99999 sein")
    return f"{n:05d}"


def agenturnummer(n: int) -> str:
    """4-stellige Agenturnummer (raw)."""
    if not 0 <= n < 10**4:
        raise ValueError("Agenturnummer muss 0..9999 sein")
    return f"{n:04d}"


# ---------------------------------------------------------------------------
# MINT: UUID v4, deterministisch aus Seed
# ---------------------------------------------------------------------------


def mint_uuid(modul: str, entity_id: Any, master_seed: int = MASTER_SEED) -> str:
    """Deterministische UUID v4 fuer MINT-Objekte (Variant RFC 4122, Version 4)."""
    rng = rng_for(f"mint.uuid.{modul}", entity_id, master_seed)
    raw = bytes(rng.integers(0, 256, size=16, dtype=np_uint8()))
    return str(uuid.UUID(bytes=raw, version=4))


def np_uint8():
    import numpy as np

    return np.uint8


def mint_policennummer(jahr: int, n: int) -> str:
    """Kundenseitige MINT-Policennummer ``MZ-2021-000123-P``."""
    return f"MZ-{jahr}-{n:06d}-P"


def mint_schadennummer(jahr: int, n: int) -> str:
    """Kundenseitige MINT-Schadennummer ``CLM-2022-0004512``."""
    return f"CLM-{jahr}-{n:07d}"


def mint_email_handle(vorname: str, nachname: str) -> str:
    """Mitarbeiter-Handle in MINT: ``vorname.nachname`` ASCII-normalisiert."""
    from pfefferminzia.synth.identifiers import ascii_handle

    return f"{ascii_handle(vorname)}.{ascii_handle(nachname)}"
