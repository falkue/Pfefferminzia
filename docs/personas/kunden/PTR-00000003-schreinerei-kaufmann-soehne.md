---
dokument_id: PTR-00000003
titel: Kunden-Persona Schreinerei Kaufmann + Söhne GmbH
typ: persona
sparte: GRUPPE
markt: CH
sprache: de-CH
version: "1.0"
gueltig_ab: 2025-12-31
gueltig_bis: null
tarifgeneration: null
quelle_system: HAPO
absender: Pfefferminzia Versicherungen AG
vertraulichkeit: vertraulich
erzeugt_am: 2026-09-03
---

# Schreinerei Kaufmann + Söhne GmbH – Gewerbekundin CH

## Steckbrief

| Merkmal | Wert |
|---|---|
| Partner-ID | PTR-00000003 (juristische Person) |
| Name | Schreinerei Kaufmann + Söhne GmbH |
| Gründung | 01.04.1987 (GmbH seit 2004; UID fiktiv, prüfziffernvalide im Datensatz) |
| Adresse | Sägereiweg 4, 5600 Lenzburg |
| Kanton / Land | AG / CH |
| Sprache | de-CH |
| Branche | Schreinerei, Innenausbau und Küchenbau (NOGA 43.32 Bautischlerei; Nebenbetrieb 16.23) |
| Betrieb | 14 Mitarbeitende, Lohnsumme ca. CHF 1.1 Mio., Umsatz ca. CHF 2.6 Mio. |
| Inhaber / Kontakt | Bruno Kaufmann (PTR-00000012, geb. 05.10.1968, Geschäftsführer, 57); Söhne Marc (Betriebsleiter) und Simon (Projektleiter Küchen) |
| Vertriebskanal | Makler: Broker Mittelland AG, Aarau (VRM-00042) |
| Quellsysteme und Alt-IDs | HAPO 40551207 (als «Kaufmann + Söhne GmbH, Schreinerei»); VERA 30227761 (als «Schreinerei Kaufmann & Soehne GmbH») |
| Telefon | +41 44 000 62 03 |

## Vertragsübersicht

| Vertrag | Produkt | Tarifgeneration | Beginn | Prämie | Währung | Alt-ID | Bemerkung |
|---|---|---|---|---|---|---|---|
| VTR-00000301 | BusinessProtect (Betriebshaftpflicht CH), Deckungssumme CHF 5 Mio., Bausteine Bearbeitungsschäden, Produkthaftpflicht | HP-MODERN | 01.01.2016 | 3'840.00 p. a.; ab 01.01.2025 4'620.00 mit Selbstbehalt CHF 2'000 (Sanierung) | CHF | HAPO 40.551.207-2 | Migriert nach MINT Q2 2025; Makleranfrage Erhöhung auf CHF 10 Mio. (02/2025) mit Sublimit Bearbeitungsschäden CHF 2 Mio. offeriert |
| VTR-00000302 | RisikoLeben Kollektiv Kader (3 versicherte Personen, je CHF 300'000) | PL-2017 | 01.07.2019 | 2'160.00 p. a. | CHF | VERA L-0192466 | VN die GmbH, Begünstigte die Familien der Kader; Migration Leben Q4 2025 |

## Ereignisgeschichte (2016–2025)

| Datum | Ereignis | Bezug |
|---|---|---|
| 2016-01 | Abschluss Betriebshaftpflicht über Makler nach Wechsel vom Vorversicherer (Prämienvergleich) | Offerte, Police |
| 2018-11-05 | Kleinschaden: Kratzer in Parkett beim Küchenmontage, CHF 1'900, reguliert | SCH-00000310, SILAS S2018/003321 |
| 2019-06 | Abschluss Kollektiv-Risikoleben für Kader nach Beratung des Maklers | VTR-00000302 |
| 2021-03 | Betriebsbeschreibung aktualisiert (neue CNC-Anlage, gleiche Branche) | Nachtrag |
| 2024-03-12 | **Grossschaden:** undichter Wasseranschluss nach Küchenmontage in Neubauwohnung Lenzburg; Wasser dringt über Nacht in Wohnung und zwei darunterliegende Wohnungen; Schadenmeldung per Makler 2024-03-13 | SCH-00000318, SILAS S2024/002917 |
| 2024-03-20 | Erstreserve CHF 120'000; Gutachter beauftragt | Schadenposition |
| 2024-05-14 | Gutachten: Schadenhöhe CHF 180'000 (Bauschaden, Mobiliar, Mietausfall); Ursache vermutlich fehlerhafte Armatur (Produktfehler) oder Montage | Gutachten |
| 2024-06 | Makler drängt schriftlich auf schnelle Regulierung (Kunde droht mit Klage); Teilzahlung CHF 95'000 am 2024-09-02 (Freigabe Teamleitung Schaden CH) | Maklerkorrespondenz |
| 2024-08 | Regressprüfung gegenüber Armaturenlieferant eingeleitet | Schaden-Beteiligte |
| 2024-11 | Sanierung durch Underwriting (Tobias Wenger, MIT-00008): Prämie plus 20 Prozent, Selbstbehalt CHF 2'000 | Nachtrag, Kompetenzstufe U4 |
| 2025-02 | Makleranfrage Höherdeckung CHF 10 Mio. wegen Grossprojekt; Offerte mit Sublimit | Offerte |
| 2025-03-18 | Abschluss Schadenfall: Gesamtzahlung CHF 172'400 | Schadenposition |
| 2025-07 | Regress: Lieferant zahlt CHF 40'000 im Vergleich | Buchung |
| 2025-10 | Kollektiv-Risikoleben: Mutation, ein Kader tritt aus, neuer Betriebsleiter (Marc Kaufmann) aufgenommen | Vertragsversion |

## Rolle im Datensatz

- **Grossschaden-Storyline Haftpflicht CH:** Gutachten, Reserveentwicklung (Reserve 120'000 → Ultimate 172'400), Teilzahlung, Regress; Kompetenzstufen (Zahlung über CHF 25'000 durch Teamleitung, Sanierung U4).
- **Survivorship-Bias Reserven (F12):** Fall ist abgeschlossen und trägt ein Ultimate; Vergleichsfall mit offenem Personenschaden fehlt bewusst.
- **Makler-Storyline:** Broker fordert Tempo und API-Anbindung; Korrespondenz über PfeffMakler und E-Mail.
- **UC-08 Dubletten:** Firmenname in HAPO und VERA unterschiedlich geschrieben («+»/«&», «Söhne»/«Soehne»), gleiche UID.
- **UC-11 RAG:** Deckungsfrage Bearbeitungsschäden und Produkthaftpflicht je Generation (HP-MODERN vs. PM-2025).
- **UC-15 Betrug:** Handwerker-Grossschaden als ehrlicher Fall mit einzelnen Betrugssignalen (hohe Summe, Teilzahlung unter Druck, Regress) – bewusstes Gegenbeispiel.

## Kommunikationsstil

Bruno Kaufmann schreibt selten und kurz, meist vom Handy, ohne Anrede und mit Rechtschreibfehlern; er telefoniert lieber mit dem Makler. Die formelle Korrespondenz führt der Makler (Broker Mittelland AG): sachlich, fordernd, mit Fristen («Wir erwarten die Stellungnahme bis …»). Marc Kaufmann übernimmt seit 2025 die Kommunikation per E-Mail, höflich und strukturiert. Gruss des Betriebs: «Freundliche Grüsse, Kaufmann + Söhne». Typische Formulierung (Bruno): «Wann kommt das Geld, der Kunde macht Druck.»

---

Fiktives Lehrbeispiel. Alle Daten synthetisch. Keine Verbindung zu realen Personen, Unternehmen oder Marken.
