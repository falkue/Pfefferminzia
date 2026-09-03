# Konventionen für alle Artefakte

Diese Regeln gelten für jedes Dokument, jede Tabelle und jeden Code im Pfefferminzia-Datensatz. Sie setzen die Entscheidungen aus [entscheidungen.md](entscheidungen.md) um.

## 1. Fiktionalität und Disclaimer

**Disclaimer (lang, deutsch)** – am Ende jedes Dokuments:

> Pfefferminzia ist ein frei erfundenes Unternehmen für Lehrzwecke. Alle Personen, Firmen, Adressen, Verträge, Schäden, Kennzahlen und Ereignisse sind synthetisch erzeugt. Ähnlichkeiten mit real existierenden Personen, Unternehmen oder Marken, insbesondere mit gleichnamigen Medien oder Dienstleistern, sind unbeabsichtigt und nicht intendiert. Rechtliche und regulatorische Aussagen sind vereinfacht, Stand 2026, und ersetzen keine Rechtsberatung. Teile dieses Materials wurden mit Unterstützung von KI erzeugt.

**Disclaimer (kurz)** – für Fußzeilen, E-Mails, Tabellen-Manifeste:

> Fiktives Lehrbeispiel. Alle Daten synthetisch. Keine Verbindung zu realen Personen, Unternehmen oder Marken.

**Disclaimer (englisch)**:

> Pfefferminzia is a fictional company created for teaching purposes. All persons, companies, addresses, contracts, claims, figures and events are synthetic. Any resemblance to real persons, companies or brands, including media or service providers of the same name, is unintentional. Legal and regulatory statements are simplified, as of 2026, and do not constitute legal advice. Parts of this material were produced with AI assistance.

Weitere Regeln:

- Domains ausschließlich `pfefferminzia.example`, `minzia.example`, `pfefferminz.example`. Keine `.de`, `.ch`, `.com`.
- Postleitzahlen und Orte real, Straßennamen ausschließlich generiert (kein Abgleich mit realen Straßen in diesem Ort).
- Personennamen aus kuratierten Listen, Prominenten-Blocklist beachten.
- Telefonnummern: CH `+41 44 000 xx xx` (Bereich 000 ist nicht vergeben), DE `+49 30 23125 xxx` (offizieller Fiktionsbereich Berlin), Mobil DE `+49 152 28817 xxx` (Fiktionsbereich).
- IBAN, UID (CH), Steuer-ID (DE), AHV-Nummer (CH): prüfziffernvalide, aber fiktive Stammnummern. Bank-Codes nur der fiktiven „Oltener Kantonalbank" (fiktive Clearing-Nummer 99999) und „Spree Volksbank" (fiktive BLZ 99999999).
- Keine Gesichter, keine Kennzeichen, keine realen Logos.

## 2. Unternehmen (verbindliche Eckdaten)

| Merkmal | Wert |
|---|---|
| Name | Pfefferminzia Versicherungen AG (Holding, Olten SO) |
| Kurzname | Pfefferminzia |
| Altgesellschaft | Pfefferminz Versicherung, gegründet 1924 in Olten als Genossenschaft, AG seit 1998, DE-Eintritt 2006 |
| Start-up | Minzia Technologies GmbH, gegründet 2019 in Berlin |
| Closing / neue Marke | 1. Januar 2025 |
| Datensatz-Stichtag („heute") | 31. Dezember 2025 |
| Märkte | Schweiz (CH), Deutschland (DE) |
| Sparten | Haftpflicht (HP), Leben (LV) |
| Systeme Pfefferminz | VERA (Leben-Bestand), HAPO (Haftpflicht-Bestand), SILAS (Schaden/Leistung), DOKU (Archiv) |
| Systeme Minzia | MINT (Kernsystem), Herbarium (Datenplattform) |

Alle weiteren Kennzahlen (Prämien, Mitarbeiter, Kunden, Quoten) kommen ausschließlich aus der Kennzahlen-Masterdatei `data/reference/kennzahlen_master.yaml`. Kein Dokument erfindet eigene Zahlen.

## 3. Sprache

| Variante | Regeln | Verwendung |
|---|---|---|
| de-CH | ss statt ß; CHF; Offerte, Police, Prämie, Versicherungsnehmer; Kanton; „Grüezi"/„Freundliche Grüsse"; Datumsformat 31.12.2025 | Holding-Dokumente, CH-Kundendokumente, CH-Regelwerke |
| de-DE | ß; EUR; Angebot, Versicherungsschein, Beitrag; Bundesland; „Mit freundlichen Grüßen"; Datumsformat 31.12.2025 | DE-Kundendokumente, DE-Regelwerke, Niederlassung/Tochter DE |
| fr-CH / it-CH | Nur in CH-Kundendokumenten Haftpflicht (15 % / 5 %) | Welle 6 |
| en | Nur Data Dictionary (zweisprachig) und Disclaimer | |

Dokumente der Gruppe (Strategie, Richtlinien, Protokolle) sind in de-CH verfasst, weil der Sitz in Olten liegt.

## 4. Identifikatoren

| Entität | Präfix (curated) | Beispiel | raw VERA/HAPO | raw MINT |
|---|---|---|---|---|
| Partner | `PTR-` | `PTR-00012345` | 8-stellig numerisch, je System eigener Kreis | UUID v4 |
| Vertrag | `VTR-` | `VTR-00012345` | `40.987.112-3` (HAPO), `L-0098765` (VERA) | UUID v4 |
| Antrag | `ANT-` | `ANT-00012345` | – | UUID v4 |
| Schaden / Leistungsfall | `SCH-` | `SCH-00012345` | `S2019/004512` (SILAS) | UUID v4 |
| Dokument | `DOK-` | `DOK-00012345` | `DOKU-…` | UUID v4 |
| Interaktion | `INT-` | `INT-00012345` | – | UUID v4 |
| Mitarbeiter | `MIT-` | `MIT-00123` | Personalnummer 5-stellig | E-Mail-Handle |
| Vermittler | `VRM-` | `VRM-00123` | Agenturnummer 4-stellig | UUID v4 |
| Agentur | `AGT-` | `AGT-0012` | | |
| Produkt | Kürzel | `HP-PRIV`, `HP-BETR`, `HP-BERUF`, `LV-RISK`, `LV-VORS`, `LV-RENTE`, `LV-EU` | | |
| Tarifgeneration HP | Kürzel | `HP-KLASSIK` (≤2012), `HP-MODERN` (2013–2020), `MZ-DIRECT` (2021–2024), `PM-2025` (ab 2025) | | |
| Tarifgeneration LV | Kürzel | `PK-85`, `PK-95`, `PK-2000`, `PK-2004`, `PK-2007`, `PL-2012`, `PL-2015`, `PL-2017`, `MZ-2020`, `PZ-2025` | | |
| Regelwerk-Dokument | `RW-` | `RW-HP-AVB-CH-2025` | | |

Alle IDs in `curated` sind über Generatorläufe und Größenstufen stabil.

## 5. Dateiformate

| Inhalt | Format | Regeln |
|---|---|---|
| Referenz- und Stammdaten | CSV (UTF-8, Komma, Header, ISO-Datum `YYYY-MM-DD`) oder YAML für hierarchische Daten | Jede Datei hat eine gleichnamige `.md`-Beschreibung oder einen Eintrag im Data Dictionary |
| Tabellen curated | Parquet kanonisch, CSV und SQLite abgeleitet | Dezimaltrennzeichen Punkt, Beträge als Dezimalzahl mit 2 Stellen, Währung in eigener Spalte |
| Tabellen raw | VERA/HAPO/SILAS: Fixed-width oder Semikolon-CSV, ISO-8859-1; MINT: JSONL, UTF-8 | Bewusst verschmutzt, siehe Datenarchitektur §2 |
| Dokumente | Markdown-Quelle unter `docs/` oder `data/…/documents/`, gerendert nach PDF/DOCX | Metadaten-Header als YAML-Frontmatter |
| E-Mails | EML | |
| Transkripte | JSON | |
| Konfiguration | YAML | |

## 6. Metadaten-Header für Dokumente

Jedes Regelwerk, jedes Unternehmensdokument und jedes gerenderte Kundendokument beginnt mit YAML-Frontmatter:

```yaml
---
dokument_id: RW-HP-AVB-CH-2025
titel: Allgemeine Versicherungsbedingungen Privathaftpflicht
typ: regelwerk            # regelwerk | unternehmen | kunde | schaden | report | persona
sparte: HP                # HP | LV | GRUPPE
markt: CH                 # CH | DE | GRUPPE
sprache: de-CH
version: "2025.1"
gueltig_ab: 2025-01-01
gueltig_bis: null
tarifgeneration: PM-2025  # falls zutreffend
quelle_system: null       # VERA | HAPO | SILAS | DOKU | MINT | null
absender: Pfefferminzia Versicherungen AG
vertraulichkeit: oeffentlich   # oeffentlich | intern | vertraulich
erzeugt_am: 2026-09-03
---
```

Regelwerke verwenden durchnummerierte Paragraphen (`§ 1`, `§ 2` …) mit stabilen Nummern über Versionen hinweg, damit RAG-Antworten zitierfähig sind. Gestrichene Paragraphen bleiben als „§ 7 (aufgehoben)" stehen.

## 7. Seeds und Reproduzierbarkeit

- Master-Seed: `20250101` (Closing-Datum). Konfigurierbar in `config/generator.yaml`.
- Abgeleitete Seeds: `sha256(f"{master_seed}:{modul}:{entity_id}")`, erste 8 Bytes als Integer.
- LLM-generierte Texte werden mit Prompt-Hash im Cache `data/cache/llm/` abgelegt und versioniert.
- Jede Ausgabedatei erhält im Manifest einen SHA-256-Hash.

## 8. Ground Truth

`data/truth/` enthält die latente Wahrheit und alle Labels. Dieser Ordner ist Teil des Repositories, wird aber **nie** in Teilnehmer-Releases gepackt. Sichtbare Tabellen dürfen Labels nur verrauscht und zeitlich beschnitten enthalten.
