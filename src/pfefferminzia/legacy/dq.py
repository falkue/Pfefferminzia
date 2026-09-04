"""Werkzeuge fuer die Datenqualitaets-Injektion (Datenarchitektur 2.2) mit Protokoll in ``truth/dq_injektionen``."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

import numpy as np

TRANSLIT = {"ä": "AE", "ö": "OE", "ü": "UE", "ß": "SS", "é": "E", "è": "E", "ê": "E", "à": "A", "â": "A", "ç": "C", "ô": "O",
            "î": "I", "ï": "I", "û": "U", "ù": "U", "ë": "E", "ñ": "N", "ø": "O", "å": "A", "æ": "AE", "œ": "OE", "ì": "I", "ò": "O"}
MOJIBAKE = {"AE": "Ã¤", "OE": "Ã¶", "UE": "Ã¼", "SS": "ÃŸ"}


@dataclass
class DqProtokoll:
    eintraege: list[dict] = field(default_factory=list)

    def notiere(self, system: str, tabelle: str, quell_id: str, feld: str, regel: str, original, injiziert) -> None:
        self.eintraege.append({"quellsystem": system, "tabelle": tabelle, "quell_id": quell_id, "feld": feld, "dq_regel": regel,
                               "original": None if original is None else str(original), "injiziert": None if injiziert is None else str(injiziert)})


def translit_upper(text: str) -> str:
    """GROSSBUCHSTABEN mit Umlaut-Transliteration (DQ-03), ISO-8859-1-kompatibel."""
    if text is None:
        return ""
    out = []
    for ch in str(text):
        lo = ch.lower()
        if lo in TRANSLIT:
            out.append(TRANSLIT[lo])
        else:
            n = unicodedata.normalize("NFKD", ch)
            out.append("".join(c for c in n if not unicodedata.combining(c)))
    return "".join(out).upper()


def mojibake(text: str, rng: np.random.Generator) -> str:
    """Ersetzt eine transliterierte Umlautgruppe durch eine UTF-8-als-Latin-1-Fehlinterpretation."""
    for k, v in MOJIBAKE.items():
        if k in text and rng.random() < 0.8:
            return text.replace(k, v, 1)
    return text


def fixed(text, breite: int, rechts: bool = False, fuell: str = " ") -> str:
    s = "" if text is None else str(text)
    s = s[:breite]
    return s.rjust(breite, fuell) if rechts else s.ljust(breite, fuell)


def datum_int(d) -> str:
    """YYYYMMDD; None -> 00000000."""
    if d is None or (isinstance(d, float) and np.isnan(d)):
        return "00000000"
    return f"{d.year:04d}{d.month:02d}{d.day:02d}"


def datum_kurz(d) -> str:
    """DD.MM.YY fuer den CSV-Extrakt (zweistelliges Jahr, DQ-05/DQ-14)."""
    if d is None or (isinstance(d, float) and np.isnan(d)):
        return ""
    return f"{d.day:02d}.{d.month:02d}.{d.year % 100:02d}"


def rappen(betrag) -> str:
    if betrag is None or (isinstance(betrag, float) and np.isnan(betrag)):
        return "0"
    return str(int(round(float(betrag) * 100)))


def kuerze_name(vorname: str, nachname: str, rng: np.random.Generator, protokoll: DqProtokoll | None, system: str, pid: str,
                rate_abschnitt: float) -> tuple[str, str, list[str]]:
    """NAME1 = 'NACHNAME VORNAME' (30 Zeichen), NAME2 Zusatz; liefert (name1, name2, regeln)."""
    regeln: list[str] = []
    n1 = translit_upper(f"{nachname} {vorname}".strip())
    n2 = ""
    if len(n1) > 30:
        regeln.append("DQ-04")
        if protokoll:
            protokoll.notiere(system, "PARTNER", pid, "NAME1", "DQ-04", n1, n1[:30])
        n1 = n1[:30]
    elif rng.random() < rate_abschnitt and "-" in nachname:
        # Doppelname nur teilweise erfasst
        regeln.append("DQ-04")
        alt = n1
        n1 = translit_upper(f"{nachname.split('-')[0]} {vorname}")
        n2 = translit_upper(nachname.split("-")[1])
        if protokoll:
            protokoll.notiere(system, "PARTNER", pid, "NAME1", "DQ-04", alt, n1)
    return n1, n2, regeln


def adresse_freitext(strasse: str, hausnummer: str, plz: str, ort: str, rng: np.random.Generator, verrutscht: bool) -> tuple[str, str, str]:
    """ADR1..ADR3: Freitextzeilen; bei verrutscht steht die Hausnummer in ADR2 (DQ-13)."""
    if verrutscht:
        return translit_upper(strasse), translit_upper(str(hausnummer)), translit_upper(f"{plz} {ort}")
    return translit_upper(f"{strasse} {hausnummer}"), "", translit_upper(f"{plz} {ort}")


_WS = re.compile(r"\s+")


def bemerk(text: str, breite: int = 60) -> str:
    return _WS.sub(" ", translit_upper(text))[:breite]
