"""Erzeugt die tabellarischen Leben-Stammdaten, die sich aus Planung 02 formelhaft ableiten lassen.

Aufruf: ``uv run python scripts/build_reference_lv.py``

Erzeugt unter ``data/reference/lv/``: sterbetafel.csv, ueberschuss_parameter.csv, lebenszyklus_raten.csv.
Die uebrigen Dateien des Ordners sind handgepflegt. Deterministisch, ohne Zufall.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LV = ROOT / "data" / "reference" / "lv"

# ---------------------------------------------------------------------------------------------
# Vereinfachte Sterbetafeln (Gompertz-Makeham): qx = a + b * exp(c * alter), Frauen mit Faktor.
# Die Tafelnamen entsprechen der Spalte sterbetafel_vereinfacht in tarifgenerationen.csv.
# Neuere Tafeln liegen tiefer (Langlebigkeit); T1985 enthaelt zusaetzlich einen Sicherheitszuschlag,
# wie er in Tarifen der 1980er ueblich war.
# ---------------------------------------------------------------------------------------------
TAFELN = {
    "T1985": {"a": 0.00035, "b": 0.000032, "c": 0.094, "faktor_w": 0.62, "beschreibung": "Tarifgenerationen PK-85 bis PK-2004"},
    "T2004": {"a": 0.00025, "b": 0.000025, "c": 0.094, "faktor_w": 0.60, "beschreibung": "Tarifgenerationen PK-2007 bis PL-2017"},
    "T2020": {"a": 0.00018, "b": 0.000019, "c": 0.095, "faktor_w": 0.58, "beschreibung": "Tarifgenerationen MZ-2020 und PZ-2025"},
}


def qx(t: dict, alter: int) -> float:
    return t["a"] + t["b"] * math.exp(t["c"] * alter)


def sterbetafel() -> list[list]:
    zeilen = []
    for name, t in TAFELN.items():
        for alter in range(18, 86):
            m = min(qx(t, alter), 0.5)
            w = min(m * t["faktor_w"], 0.5)
            u = (m + w) / 2
            zeilen.append([name, alter, f"{m:.6f}", f"{w:.6f}", f"{u:.6f}", t["beschreibung"]])
    return zeilen


# ---------------------------------------------------------------------------------------------
# Ueberschussparameter je Generation, Markt und Jahr (Planung 02 §6.5):
# Gesamtverzinsung fallend bis 2022/2023, leichter Anstieg ab 2024; 2025: DE 2.6 %, CH 2.0 %.
# Zinsueberschuss = max(0, Gesamtverzinsung - Rechnungszins der Generation).
# ---------------------------------------------------------------------------------------------
GESAMTVERZINSUNG = {
    "DE": {2016: 2.90, 2017: 2.75, 2018: 2.60, 2019: 2.50, 2020: 2.35, 2021: 2.25, 2022: 2.15, 2023: 2.20,
           2024: 2.45, 2025: 2.60},
    "CH": {2016: 2.25, 2017: 2.10, 2018: 2.00, 2019: 1.90, 2020: 1.75, 2021: 1.60, 2022: 1.50, 2023: 1.55,
           2024: 1.80, 2025: 2.00},
}
RECHNUNGSZINS = {  # generation: (DE bis 2021, DE ab 2022, CH)
    "PK-85": (3.5, 3.5, 3.5), "PK-95": (4.0, 4.0, 3.5), "PK-2000": (3.25, 3.25, 3.0), "PK-2004": (2.75, 2.75, 2.5),
    "PK-2007": (2.25, 2.25, 2.0), "PL-2012": (1.75, 1.75, 1.5), "PL-2015": (1.25, 1.25, 1.0),
    "PL-2017": (0.9, 0.25, 0.25), "MZ-2020": (0.25, 0.25, 0.25), "PZ-2025": (1.0, 1.0, 0.5),
}
GENERATION_AB = {"PK-85": 1985, "PK-95": 1994, "PK-2000": 2000, "PK-2004": 2004, "PK-2007": 2007, "PL-2012": 2012,
                 "PL-2015": 2015, "PL-2017": 2017, "MZ-2020": 2020, "PZ-2025": 2025}
RISIKOUEBERSCHUSS = {"DE": 30.0, "CH": 25.0}   # Prozent der Risikopraemie (Risikoleben)


def ueberschuss() -> list[list]:
    zeilen = []
    for gen, (rz_de_alt, rz_de_neu, rz_ch) in RECHNUNGSZINS.items():
        for markt in ("DE", "CH"):
            for jahr in range(2016, 2026):
                if jahr < GENERATION_AB[gen]:
                    continue
                if gen == "MZ-2020" and markt == "CH" and jahr < 2021:
                    continue
                gesamt = GESAMTVERZINSUNG[markt][jahr]
                rz = rz_ch if markt == "CH" else (rz_de_alt if jahr < 2022 else rz_de_neu)
                zins_ueb = max(0.0, round(gesamt - rz, 2))
                # Schlussueberschuss in Prozent des Deckungskapitals bei Ablauf, ueber die Jahre gesunken
                schluss = round(max(0.5, 3.0 - 0.2 * (jahr - 2016)) * (0.8 if markt == "CH" else 1.0), 2)
                kommentar = ""
                if zins_ueb == 0.0 and rz >= gesamt:
                    kommentar = "Garantiezins ueber Gesamtverzinsung: kein Zinsueberschuss (Zinszusatzreserve DE)"
                elif jahr >= 2024:
                    kommentar = "Zinswende: Gesamtverzinsung steigt wieder"
                zeilen.append([gen, markt, jahr, rz, gesamt, zins_ueb, RISIKOUEBERSCHUSS[markt], schluss, kommentar])
    return zeilen


# ---------------------------------------------------------------------------------------------
# Lebenszyklusraten je Produkt x Markt x Kanal x Herkunft x Jahr (Prozent des Bestands je Jahr)
# ---------------------------------------------------------------------------------------------
BASIS = {  # produkt: (neugeschaeft, storno_rueckkauf, beitragsfrei, dynamik_annahme, leistungsfall)
    "LV-RISK": (9.0, 5.0, 0.8, 65.0, 0.25),
    "LV-VORS": (4.0, 3.5, 1.8, 60.0, 1.2),    # Leistungsfall inkl. Ablauf/Erleben
    "LV-RENTE": (6.0, 2.5, 1.5, 62.0, 0.6),
    "LV-EU": (5.0, 4.0, 1.0, 55.0, 0.35),
}
MARKT_FAKTOR = {"CH": (1.0, 0.85, 0.9), "DE": (1.0, 1.15, 1.1)}   # neugeschaeft, storno, beitragsfrei
KANAL_FAKTOR = {"agentur": (1.00, 0.85, 0.95), "makler": (1.10, 1.10, 0.95), "direkt": (1.40, 1.35, 1.10),
                "bank": (0.80, 0.95, 1.00)}
JAHR_TREND_STORNO = {2016: 1.00, 2017: 1.00, 2018: 1.02, 2019: 1.03, 2020: 1.10, 2021: 1.00, 2022: 1.08,
                     2023: 1.15, 2024: 1.05, 2025: 1.12}


def lebenszyklus() -> list[list]:
    zeilen = []
    for produkt, (ng, st, bf, dyn, lf) in BASIS.items():
        for markt, (m_ng, m_st, m_bf) in MARKT_FAKTOR.items():
            if produkt == "LV-VORS" and markt == "DE":
                ng_markt = 0.0   # DE nur Altbestand (Entscheidung E05)
            else:
                ng_markt = ng * m_ng
            for kanal, (k_ng, k_st, k_bf) in KANAL_FAKTOR.items():
                for jahr in range(2016, 2026):
                    herkuenfte = ["alle"] if jahr < 2020 else ["pfefferminz", "minzia"]
                    for herkunft in herkuenfte:
                        if herkunft == "minzia" and not (produkt in ("LV-RISK", "LV-EU") and kanal == "direkt"):
                            continue
                        neug = ng_markt * k_ng * (1.8 if herkunft == "minzia" else 1.0)
                        if jahr == 2020:
                            neug *= 0.85
                        storno = st * m_st * k_st * JAHR_TREND_STORNO[jahr]
                        if herkunft == "minzia":
                            storno *= 1.2
                        if jahr == 2025 and herkunft == "pfefferminz":
                            storno *= 1.25
                        beitragsfrei = bf * m_bf * k_bf * (1.3 if jahr in (2020, 2023) else 1.0)
                        dynamik = dyn - (jahr - 2016) * 0.8 - (8.0 if herkunft == "minzia" else 0.0)
                        leistung = lf * (1.15 if jahr in (2020, 2021) else 1.0)
                        bem = ""
                        if jahr == 2025 and herkunft == "pfefferminz":
                            bem = "Fusionseffekt: Rueckkaufwelle nach Vertriebsumbau und Systemmigration Q4"
                        elif jahr in (2020, 2021):
                            bem = "Pandemiejahre: Uebersterblichkeit, mehr Beitragsfreistellungen"
                        elif jahr == 2023:
                            bem = "Zinsanstieg: Rueckkaeufe zugunsten anderer Anlagen"
                        zeilen.append([produkt, markt, kanal, herkunft, jahr, round(neug, 2), round(storno, 2),
                                       round(beitragsfrei, 2), round(dynamik, 1), round(leistung, 2), bem])
    return zeilen


def schreibe(pfad: Path, spalten: list[str], zeilen: list[list]) -> None:
    with pfad.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(spalten)
        w.writerows(zeilen)
    print(f"{pfad.relative_to(ROOT)}: {len(zeilen)} Zeilen")


def main() -> None:
    LV.mkdir(parents=True, exist_ok=True)
    schreibe(LV / "sterbetafel.csv", ["tafel", "alter", "qx_m", "qx_w", "qx_unisex", "beschreibung"], sterbetafel())
    schreibe(LV / "ueberschuss_parameter.csv",
             ["generation_code", "markt", "jahr", "rechnungszins_pct", "gesamtverzinsung_pct", "zinsueberschuss_pct",
              "risikoueberschuss_pct", "schlussueberschuss_pct", "kommentar"], ueberschuss())
    schreibe(LV / "lebenszyklus_raten.csv",
             ["produkt_code", "markt", "kanal", "herkunft", "jahr", "neugeschaeft_rate_pct", "storno_rueckkauf_rate_pct",
              "beitragsfrei_rate_pct", "dynamik_annahme_rate_pct", "leistungsfall_rate_pct", "bemerkung"],
             lebenszyklus())


if __name__ == "__main__":
    main()
