# Der Datensatz

Dieses Verzeichnis dokumentiert die erzeugten Daten unter `data/`. Die Beschreibung aller Tabellen und Spalten steht je Stufe im Data Dictionary, zum Beispiel [data-dictionary-S.md](data-dictionary-S.md).

## Schichten

| Schicht | Ordner | Für wen | Inhalt |
|---|---|---|---|
| curated | `data/curated/<Stufe>/` | Teilnehmer | Harmonisierte Tabellen mit lesbaren IDs (`PTR-`, `VTR-`, `ANT-`), Rest-Unschärfe bleibt bewusst erhalten |
| raw | `data/raw/<Stufe>/` | Teilnehmer | Die verschmutzten Rohextrakte der Quellsysteme: HAPO und VERA (Host, ISO-8859-1) sowie MINT (JSON Lines) |
| migration | `data/migration/<Stufe>/` | Teilnehmer | Kreuzreferenzen zwischen Quell-IDs und curated-IDs, Feldmapping, Migrationslog der Wellen 2025 |
| truth | `data/truth/<Stufe>/` | Dozenten | Latente Wahrheit (Kündigungsneigung, Betrugsneigung, echte Gesundheitswerte), Labels, Protokoll der Datenqualitäts-Injektionen |

Jede Tabelle liegt als Parquet (kanonisch) und als CSV (UTF-8 mit BOM, Komma, ISO-Datum) vor. Das Manifest `data/manifest_<Stufe>.json` führt Zeilenzahlen und SHA-256-Hashes aller Dateien.

## Stufen

| Stufe | Partner | Verträge | Zweck |
|---|---|---|---|
| S | 1'000 | rund 1'500 | Handouts, Datei-Upload in LLM-Werkzeuge, 90-Minuten-Module |
| M | 50'000 | 75'000 | Analytics und Machine Learning |
| L | 250'000 | 375'000 | Performance-Demos |

Stufe S ist ein echter Teilbaum der grösseren Stufen: gleiche IDs, gleiche Wahrheit.

## Die zwei Systemwelten in den Rohdaten

Die Altsysteme exportieren Fixed-width-Dateien mit Satzartbeschreibung und Semikolon-CSV mit zweistelligen Jahreszahlen. Namen stehen in Grossbuchstaben ohne Umlaute, Beträge in Rappen oder Cent, Datumsfelder als Ganzzahl mit Platzhaltern wie 00000000. Dieselbe Person existiert in HAPO (Haftpflicht) und VERA (Leben) mit verschiedenen Nummern und teils abweichender Schreibweise. Migrierte Verträge tragen den undokumentierten Stornogrund ZZ.

MINT exportiert JSON Lines mit drei Schema-Versionen, je nach Erstellungsdatum. Migrierte Sätze enthalten die Altsystem-Codes unübersetzt im Feld `legacyAttributes`. Dazu kommen Registrierungsdubletten, Testdaten, Freitextberufe und gemischte Zeitzonen.

Welche Abweichung wo eingebaut wurde, steht für Dozenten in `truth/dq_injektionen` mit Originalwert.

## Personas in den Daten

Die zehn Kunden-Personas belegen die Partner-IDs 1 bis 10, ihre Bezugspersonen die IDs 11 bis 20, ihre Verträge die Vertrags-IDs unter 2000. Storylines wie der Fall Pieper (VTR-00000801) oder der Betrugsfall Grimm (VTR-00000901) sind damit in den Tabellen auffindbar.

## Reproduzierbarkeit

```bash
uv run pfefferminzia generate --stufe S
uv run python scripts/build_data_dictionary.py S
```

Jeder Lauf mit demselben Master-Seed liefert identische curated-Tabellen.
