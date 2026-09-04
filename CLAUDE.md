# Pfefferminzia – Hinweise für Claude Code

Dieses Repository enthält einen **synthetischen Lehr-Datensatz** eines fiktiven Versicherers (Pfefferminzia, Schweiz und Deutschland, Haftpflicht und Leben) samt dem Generator, der ihn erzeugt. Alle Personen, Firmen, Verträge und Ereignisse sind erfunden.

## Wo was liegt

- `data/curated/S/csv/` – die harmonisierten Tabellen als CSV (auch als Parquet unter `parquet/`). Einstieg für Analysen.
- `data/raw/S/pvs/` – Rohextrakte der Altsysteme HAPO (Haftpflicht) und VERA (Leben): Fixed-width-Text mit Satzartbeschreibung (`*_SATZART.txt`) und Semikolon-CSV, Zeichensatz ISO-8859-1.
- `data/raw/S/mint/` – Rohextrakt der Plattform MINT als JSON Lines (Schema-Versionen v1 bis v3).
- `data/migration/S/csv/` – Kreuzreferenzen Quell-ID zu curated-ID, Feldmapping, Migrationslog.
- `data/truth/S/` – Lösungen (latente Wahrheit, Labels, Protokoll der eingebauten Datenfehler). Nur für Dozenten.
- `data/reference/` – Stammdaten und Referenzen (Produkte, Tarife, Regelwerkstabellen, Personas, Geo- und Namenslisten) mit Data Dictionaries in den README-Dateien.
- `docs/datensatz/data-dictionary-S.md` – Beschreibung aller Tabellen und Spalten.
- `docs/datensatz/dashboard-S.html` – interaktive Datenschau (im Browser öffnen).
- `docs/personas/` – 14 Mitarbeiter- und 10 Kunden-Personas mit Storylines.
- `docs/unternehmen/` – Unternehmensprofil, Geschichte, Zeitachse, Organisation, IT-Landschaft.
- `docs/konventionen.md` – Regeln des Datensatzes: IDs, Sprachen, Formate, Fiktionalität.

## Wichtige Fakten

- Stichtag des Datensatzes: 31. Dezember 2025. Fusion (Closing) am 1. Januar 2025.
- IDs: Partner `PTR-00000001`, Verträge `VTR-00000001`, Anträge `ANT-…`. Die Personas belegen die Partner-IDs 1 bis 20 und die Vertrags-IDs unter 2000.
- Währungen: CH-Verträge in CHF, DE-Verträge in EUR. Beträge in den Rohdaten der Altsysteme stehen in Rappen bzw. Cent.
- Quellsysteme: HAPO und VERA (Pfefferminz, Host), MINT (Minzia, Cloud). Migrierte Verträge tragen im Altsystem den Stornogrund `ZZ`.
- Der Datensatz enthält bewusst Datenqualitätsprobleme (Dubletten, Transliteration, Platzhalterdaten, Schema-Drift). Sie sind gewollt.

## Arbeiten mit den Daten

- Python-Umgebung: `uv sync`, dann `uv run python …`. pandas und pyarrow sind installiert.
- CSV-Dateien unter `curated` sind UTF-8 mit BOM, Komma-getrennt, Datum ISO. Rohdaten der Altsysteme mit `encoding="iso-8859-1"` und Semikolon lesen.
- Den Datensatz neu erzeugen: `uv run pfefferminzia generate --stufe S` (deterministisch, Master-Seed 20250101).
- Datenschau neu bauen: `uv run python scripts/build_dashboard.py S`.

## Regeln

- Keine realen Personen, Firmen oder Adressen erfinden oder einfügen; Domains nur `.example`.
- Ergebnisse von Analysen bitte gegen die Tabellen prüfen, bevor sie berichtet werden.
- Der Ordner `data/truth/` ist die Lösung. Für Übungen nicht verwenden, wenn die Aufgabe es nicht ausdrücklich erlaubt.
