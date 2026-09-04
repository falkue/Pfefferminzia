# Pfefferminzia

Pfefferminzia ist ein fiktiver Versicherungsdienstleister. Dieses Repository enthält alle Unterlagen und Software, die im Rahmen des Aufbaus entstehen.

## Zweck

Pfefferminzia ist ein Lehr-Datensatz für einen Executive-Kurs, in dem Führungskräfte aus der Versicherungsbranche KI-Use-Cases praktisch durchspielen. Das Unternehmen ist aus der Fusion der traditionellen Pfefferminz Versicherung mit dem KI-Start-up Minzia entstanden, bietet Haftpflicht- und Lebensversicherungen an und ist in der Schweiz und Deutschland tätig.

## Struktur

- [docs/START.md](docs/START.md) – Einstieg für Teilnehmende; `CLAUDE.md` – Orientierung für Claude Code
- `docs/planung/` – Planung des Datensatzes. Einstieg: [00-gesamtplan.md](docs/planung/00-gesamtplan.md), darunter fünf Teilplanungen (Haftpflicht, Leben, Datenarchitektur, Use Cases, Regelwerke/Unternehmen)
- [docs/entscheidungen.md](docs/entscheidungen.md) – verbindliches Entscheidungsprotokoll
- [docs/konventionen.md](docs/konventionen.md) – Regeln für alle Artefakte (Fiktionalität, Sprache, IDs, Formate, Metadaten)
- `docs/unternehmen/` – Unternehmensprofil, Geschichte, Zeitachse, Organisation, IT-Landschaft, Standorte
- `docs/personas/` – 14 Mitarbeiter- und 10 Kunden-Personas mit Storylines
- `docs/stammdaten/` – Dozentenerläuterungen zu den Stammdaten Haftpflicht und Leben
- `docs/regelwerke/` – Regelwerke als Dokumente: Annahmerichtlinie Leben, Kompetenzordnung, Beschwerderichtlinie
- `data/reference/` – Stammdaten und Referenzen: Kennzahlen-Masterdatei, Organisation, Standorte, Systeme, Personas, Geo- und Namenslisten, `hp/` und `lv/` mit je einem Data Dictionary
- `src/pfefferminzia/` – Generator (Python, `uv`), siehe [src/README.md](src/README.md)
- `scripts/` – Erzeugungsskripte für Referenzdaten
- `tests/` – Testsuite (`uv run pytest`)
- `data/raw`, `data/curated`, `data/truth`, `data/sample` – erzeugter Datensatz (ab Welle 1)

## Stand

- **Welle 0 (Fundament)** abgeschlossen: Entscheidungen, Konventionen, Unternehmenskontext, Personas, Stammdaten beider Sparten, Generator-Skelett.
- **Welle 1 (Kundenstamm und Verträge)** abgeschlossen: Der Datensatz der Stufe S liegt unter `data/` (siehe [docs/datensatz/data-dictionary-S.md](docs/datensatz/data-dictionary-S.md)).
  - `data/curated/S/` – 16 harmonisierte Tabellen (Partner, Adressen, Kontakte, Beziehungen, Firmen, Organisation, Mitarbeitende, Agenturen, Vermittler, Produkte, Tarifgenerationen, Anträge, Verträge, Deckungen, Risikoobjekte, Rollen) als Parquet und CSV
  - `data/raw/S/pvs/` – Rohextrakte der Altsysteme HAPO und VERA (Fixed-width und Semikolon-CSV, ISO-8859-1, mit Satzartbeschreibung)
  - `data/raw/S/mint/` – Rohextrakt der Minzia-Plattform MINT (JSON Lines, Schema-Versionen v1 bis v3)
  - `data/migration/S/` – Kreuzreferenzen, Feldmapping, Migrationslog
  - `data/documents/S/personas/` – die Fallakten der zehn Kunden-Personas als Briefe, E-Mails, Notizen und Berichte (Markdown und EML)
  - `data/documents/S/tarife/` – 28 Tarifblätter aus den Referenztabellen für Haftpflicht und Leben (Markdown und PDF)
  - `data/truth/S/` – latente Wahrheit, Labels und Protokoll der Datenqualitäts-Injektionen (nur Dozenten, nicht Teil der Teilnehmer-Releases)
- **Teilnehmer-Zweig:** Der Zweig `teilnehmer` enthält denselben Datensatz ohne Lösungen. Teilnehmende klonen mit `git clone -b teilnehmer https://github.com/falkue/Pfefferminzia`. Der Zweig wird mit `scripts/build_teilnehmer_branch.sh` aus `main` neu erzeugt.
- Nächster Schritt ist Welle 2 (Bewegungsdaten: Rechnungen, Buchungen, Mahnungen, Interaktionen, Beschwerden, Churn-Labels) und danach Welle 3 (Underwriting-Akten Leben).

Der Datensatz wird mit `uv run pfefferminzia generate --stufe S` reproduzierbar erzeugt (Master-Seed 20250101).

## Einrichtung

```bash
uv sync
uv run pytest
uv run pfefferminzia reference check
```

## Lizenz

Code (`src/`, `scripts/`, `tests/`): MIT, siehe [LICENSE](LICENSE). Daten und Dokumente (`data/`, `docs/`): CC BY 4.0, siehe [LICENSE-DATA.md](LICENSE-DATA.md).

## Hinweis

Pfefferminzia ist ein frei erfundenes Unternehmen für Lehrzwecke. Alle Personen, Firmen, Adressen, Verträge, Schäden, Kennzahlen und Ereignisse sind synthetisch erzeugt. Ähnlichkeiten mit real existierenden Personen, Unternehmen oder Marken, insbesondere mit gleichnamigen Medien oder Dienstleistern, sind unbeabsichtigt und nicht intendiert. Rechtliche und regulatorische Aussagen sind vereinfacht, Stand 2026, und ersetzen keine Rechtsberatung. Teile dieses Materials wurden mit Unterstützung von KI erzeugt.

Der Ordner `data/truth/` enthält die Lösungen (latente Wahrheit, Labels, Protokoll der eingebauten Datenfehler). Er ist für Dozenten gedacht; Seminarteilnehmer sollten mit den Release-Paketen ohne diesen Ordner arbeiten.
