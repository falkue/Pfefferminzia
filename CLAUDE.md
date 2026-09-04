# Pfefferminzia – Hinweise für Claude Code

Dieses Repository enthält einen **synthetischen Lehr-Datensatz** des fiktiven Versicherers Pfefferminzia (Schweiz und Deutschland, Haftpflicht und Leben) samt dem Generator, der ihn erzeugt. Alle Personen, Firmen, Verträge und Ereignisse sind erfunden. Die Nutzerinnen und Nutzer sind Fachleute aus der Versicherungsbranche, meist ohne Programmierkenntnisse. Sie stellen Fragen in Geschäftssprache und nennen selten Dateipfade. Finde die passenden Quellen mit dieser Landkarte selbst, ohne nachzufragen.

## Die Geschichte in drei Sätzen

Die Pfefferminz Versicherung (gegründet 1924 in Olten, Host-Systeme HAPO für Haftpflicht und VERA für Leben) hat am 1. Januar 2025 das Berliner KI-Start-up Minzia (Cloud-Plattform MINT) übernommen. 2025 wurden die Bestände aus HAPO und VERA nach MINT migriert (Haftpflicht am 15. Mai, Leben am 15. November). Stichtag des Datensatzes ist der 31. Dezember 2025. Details: `docs/unternehmen/` (Profil, Geschichte, Zeitachse, Organisation, IT-Landschaft, Standorte).

## Landkarte: Welche Frage, welche Quelle

| Frage betrifft | Quelle |
|---|---|
| Kunden, Firmen, Adressen, Kontakte, Haushalte | `data/curated/S/csv/partner.csv`, `partner_adresse.csv`, `partner_kontakt.csv`, `partner_firma.csv`, `partner_beziehung.csv` |
| Verträge, Prämien, Status, Storno, Kanal, Herkunft | `vertrag.csv` (Schlüssel `vertrag_id`, Kunde über `versicherungsnehmer_id`), Mitversicherte in `vertrag_partner_rolle.csv`, Deckungen in `deckung.csv`, Risikoobjekte in `risiko_objekt.csv` |
| Anträge, Risikoprüfung, Zuschläge, BMI, Raucher | `antrag.csv` (`uw_entscheid_code` A angenommen, Z Zuschlag, X abgelehnt, R Rückstellung; `uw_automatisiert`) |
| Schäden und Leistungsfälle | `schaden.csv`, `schaden_position.csv`; nur die zehn Kunden-Personas haben Schäden |
| Kontakte mit Kunden (Anrufe, Mails, Briefe) | `interaktion.csv` (Volltext in `text_body` oder Datei in `datei_pfad`) |
| Dokumente (Briefe, Policen, Gutachten) | `dokument.csv` und die Dateien unter `data/documents/S/personas/<PTR>/` (Markdown mit Frontmatter, E-Mails als `.eml`) |
| Produkte, Tarifgenerationen, Garantiezins | `produkt.csv`, `tarifgeneration.csv`; Details in `data/reference/lv/tarifgenerationen.csv`, `data/reference/hp/tarifgenerationen.csv`, `data/reference/lv/ueberschuss_parameter.csv` (Gesamtverzinsung); Tarifblätter als Markdown und PDF unter `data/documents/S/tarife/` |
| Vertrieb: Vermittler, Agenturen | `vermittler.csv` (`vermittler_id`, `agentur_id`), `agentur.csv` |
| Mitarbeitende, Organisation | `mitarbeiter.csv`, `org_einheit.csv`; Personas in `docs/personas/mitarbeiter/` |
| Regeln: Annahmerichtlinie Leben, Kompetenzordnung (wer darf was entscheiden), Beschwerderichtlinie mit Textbausteinen | `docs/regelwerke/RW-LV-ARL-2025.md`, `RW-GRUPPE-R08-2025.md`, `RW-GRUPPE-R05-2025.md` |
| Altsysteme, Migration, Dubletten, Stornogrund ZZ | Brücken in `data/migration/S/csv/`: `partner_xref.csv` und `vertrag_xref.csv` (Quell-ID zu curated-ID, Zuordnungsmethode), `feld_mapping.csv` (Bedeutung der Altsystem-Codes), `migrationslog.csv` (OK, WARN, ERROR je Objekt) |
| Rohdaten der Altsysteme, so wie ein Migrationsprojekt sie vorfindet | `data/raw/S/pvs/` (HAPO, VERA: Fixed-width mit `*_SATZART.txt` und Semikolon-CSV, ISO-8859-1), `data/raw/S/mint/` (JSON Lines, Schema v1 bis v3) |
| Bedeutung einer Spalte | `docs/datensatz/data-dictionary-S.md` |
| Codes und Stammdaten (Status, Schadenarten, Bausteine, Berufsgruppen, Sterbetafel) | `data/reference/hp/`, `data/reference/lv/`, jeweils mit README |

Schlüssel: Partner `PTR-00000001`, Vertrag `VTR-00000001`, Antrag `ANT-…`, Schaden `SCH-…`, Interaktion `INT-…`, Dokument `DOK-…`, Vermittler `VRM-…`, Agentur `AGT-…`. Die Personas belegen Partner-IDs 1 bis 20 und Vertrags-IDs unter 2000.

## Die zehn Kunden-Personas

Zu jeder gibt es eine Geschichte in `docs/personas/kunden/` und eine Fallakte unter `data/documents/S/personas/`.

| ID | Name | Worum es geht |
|---|---|---|
| PTR-00000001 | Simone Niederberger | Kundin in HAPO, VERA und MINT zugleich; Dubletten, Doppelname, Adresswechsel |
| PTR-00000002 | Jana Ortlepp | Junge Direktkundin von Minzia; Widerruf in 14 Tagen und Neuabschluss, zwei Policen auf einem MINT-Konto, davon eine storniert, aber kein echter Storno |
| PTR-00000003 | Schreinerei Kaufmann + Söhne GmbH | Grossschaden Betriebshaftpflicht CH: Gutachten, Reserveentwicklung, Teilzahlung, Regress, drängender Makler |
| PTR-00000004 | Bergmann Gebäudetechnik GmbH & Co. KG | Gewerbebetrieb DE; neuer Geschäftszweig ohne Anzeige, erst durch einen Schaden erkannt; Firmenname in drei Schreibweisen |
| PTR-00000005 | Elisabeth Vogt-Schnyder | Altbestand Leben (PK-95) bis zur Rente; Bezugsberechtigter verstorben; drei Altsätze in VERA und HAPO; Kundin ohne E-Mail |
| PTR-00000006 | Dr. Farid Nazari | Risikoleben 1.2 Mio EUR, Zuschlag wegen Bluthochdruck, Erklärung ohne Diagnose |
| PTR-00000007 | Leon Waibel | Junger Direktkunde, kurze Vertragsdauer, Kündigung wegen Preis; Musterfall für Storno-Frühwarnung |
| PTR-00000008 | Hans-Georg Pieper | Schaden automatisch abgelehnt nach Migrationsfehler; Beschwerde, Ombudsmann, BaFin |
| PTR-00000009 | Transportlogistik Grimm e.K. | Betrugsverdacht, Ablehnung und Kündigung, Anwalt |
| PTR-00000010 | Nadia Ferreira-Bucher | Einmalprämie über der Geldwäscherei-Schwelle, Prüfung endet unauffällig; Neukundin nur in MINT; Beratungsfehler des Maklers |

## Wichtige Fakten

- Stichtag 31. Dezember 2025. Closing der Fusion 1. Januar 2025. Snapshot der Altsysteme 31. Dezember 2024.
- Herkunft eines Vertrags: `PFEFFERMINZ` oder `MINZIA`. Quellsystem: `HAPO`, `VERA`, `MINT`.
- Währungen: CH-Verträge in CHF, DE-Verträge in EUR. Beträge in den Rohdaten der Altsysteme stehen in Rappen bzw. Cent.
- Migrierte Verträge tragen im Altsystem-Extrakt Status `S` mit Stornogrund `ZZ`. Das ist kein Kundenstorno, sondern der Migrationsabschluss.
- Stornoquote sinnvoll als: Verträge mit `storno_datum` im Jahr, geteilt durch die im Jahr aktiven Verträge. Nachfragen, wenn die Definition offen ist.
- Der Datensatz enthält bewusst Datenqualitätsprobleme (Dubletten, Transliteration, Platzhalterdaten, Schema-Drift). Sie sind gewollt und Teil der Übungen.

## Arbeiten mit den Daten

- Python: `uv sync`, dann `uv run python …`. pandas, pyarrow und matplotlib sind verfügbar.
- CSV unter `curated` und `migration`: UTF-8 mit BOM, Komma, Datum ISO. Rohdaten der Altsysteme mit `encoding="iso-8859-1"` und Semikolon lesen.
- Zahlen vor dem Berichten gegen die Tabellen prüfen und die Definition nennen (aktiv, Stichtag, Währung).

## Ergebnisse ablegen und zeigen

- Ergebnisse der Nutzerinnen und Nutzer kommen in den Ordner `meine-ergebnisse/` im Projektstamm (anlegen, wenn er fehlt). Nichts im Datensatz selbst verändern.
- Für Visualisierungen bevorzugt **eine einzelne HTML-Datei** mit eingebetteten Daten, die ohne Server im Browser läuft. Diagramme mit Chart.js von `https://cdnjs.cloudflare.com` laden, wenn Internet vorhanden ist; sonst als Inline-SVG oder Canvas zeichnen. Kennzahlen-Kacheln oben, Filter und Sortierung per Klick, Titel und Stichtag sichtbar.
- Fertige HTML-Dateien nach dem Schreiben im Standardbrowser öffnen: `xdg-open` (Linux), `open` (Mac), `start` (Windows).
- Tabellen als CSV, Berichte als Markdown, Diagramme zusätzlich als PNG, wenn ein Bericht sie braucht.
- **Cockpit:** Wenn jemand von «meinem Cockpit» spricht, ist `meine-ergebnisse/cockpit.html` gemeint: eine Seite mit Reitern, die über mehrere Übungen wächst. Neue Sichten kommen als neuer Reiter dazu, bestehende Reiter bleiben unverändert. Daten je Reiter in einer eigenen Datei `meine-ergebnisse/cockpit-daten/<reiter>.js` (eine globale Konstante mit JSON), erzeugt von einem Python-Skript unter `meine-ergebnisse/skripte/`, damit die Seite ohne Server läuft und die Daten nachvollziehbar sind. Kopfzeile mit «Pfefferminzia», Stichtag 31.12.2025 und Reiterleiste. Falls das Cockpit noch nicht existiert, anlegen.

## Regeln

- Keine realen Personen, Firmen oder Adressen erfinden oder einfügen; Domains nur `.example`.
- Der Ordner `data/truth/` ist die Lösung. Für Übungen nicht verwenden, wenn die Aufgabe es nicht ausdrücklich erlaubt.
- Den Datensatz neu erzeugen: `uv run pfefferminzia generate --stufe S` (deterministisch, Master-Seed 20250101). Datenschau: `uv run python scripts/build_dashboard.py S`.
