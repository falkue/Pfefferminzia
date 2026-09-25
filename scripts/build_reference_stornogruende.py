"""Erzeugt ``data/reference/stornogruende.csv``: Bedeutung der Stornogründe K01 bis K17 aus der Vertragstabelle.

Aufruf: ``uv run python scripts/build_reference_stornogruende.py``

Quelle ist die Liste ``STORNO_GRUENDE`` des Generators. Die Spalte ``zaehlt_als_storno`` folgt der verbindlichen
Stornoquote in der CLAUDE.md: nicht mitgezählt werden K07 (Tod des Versicherungsnehmers), K13 (Widerruf in der Frist),
K15 (Ablauf/Erleben) und K16 (Leistungsfall Tod). Der Migrationsstorno ZZ steht nur in den Rohdaten der Altsysteme.
"""

from __future__ import annotations

import csv
from pathlib import Path

from pfefferminzia.synth.referenz_intern import STORNO_GRUENDE

ROOT = Path(__file__).resolve().parents[1]
ZIEL = ROOT / "data" / "reference" / "stornogruende.csv"
NICHT_GEZAEHLT = {"K07", "K13", "K15", "K16"}
STATUS_DE = {"GEKUENDIGT_VN": "vom Kunden gekündigt", "GEKUENDIGT_VU": "vom Versicherer gekündigt", "STORNIERT": "storniert",
             "RUECKKAUF": "zurückgekauft", "ABGELAUFEN": "abgelaufen", "LEISTUNG_ERBRACHT": "Leistung erbracht"}


def main() -> None:
    with ZIEL.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["storno_grund_code", "bezeichnung", "vertragsstatus", "vertragsstatus_de", "zaehlt_als_storno"])
        for code, bezeichnung, status, _gewicht in STORNO_GRUENDE:
            w.writerow([code, bezeichnung, status, STATUS_DE[status], "NEIN" if code in NICHT_GEZAEHLT else "JA"])
        w.writerow(["ZZ", "Migrationsabschluss (nur Rohdaten HAPO/VERA, kein Storno)", "", "", "NEIN"])
    print(ZIEL.relative_to(ROOT), len(STORNO_GRUENDE) + 1, "Codes")


if __name__ == "__main__":
    main()
