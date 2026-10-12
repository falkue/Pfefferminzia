---
dokument_id: PTR-00000008
titel: Kunden-Persona Hans-Georg Pieper (Beschwerdeführer)
typ: persona
sparte: HP
markt: DE
sprache: de-DE
version: "1.0"
gueltig_ab: 2025-12-31
gueltig_bis: null
tarifgeneration: HP-MODERN
quelle_system: HAPO
absender: Pfefferminzia Versicherungen AG
vertraulichkeit: vertraulich
erzeugt_am: 2026-09-03
---

# Hans-Georg Pieper – Privatkunde DE, Beschwerdeführer

## Steckbrief

| Merkmal | Wert |
|---|---|
| Partner-ID | PTR-00000008 |
| Name | Hans-Georg Pieper |
| Geburtsdatum | 02.09.1962 |
| Adresse | Erlensteig 27, 01309 Dresden |
| Bundesland / Land | Sachsen / DE |
| Sprache | de-DE |
| Beruf | Frühpensionär, ehemals Betriebsschlosser; Hundehalter (Schäferhund-Mischling «Rex», kein Listenhund) |
| Familienstand | geschieden, lebt allein |
| Vertriebskanal | Ausschliesslichkeitsagentur Dresden, in den Briefen «Agentur Dresden» (Generalagentur Elbland Petrov, AGT-0005, Vermittlerin Maria José Kim VRM-00023), seit 2025 Betreuung durch Contact Center Leipzig |
| Quellsysteme und Alt-IDs | Partner HAPO 20000005 («PIEPER HANS-GEORG»); MINT 0860b995-c21a-4b5a-9d32-f5dd16da9d7f («Hans-Georg Pieper») |
| Telefon | +49 30 23125 614 (Festnetz) |

## Vertragsübersicht

| Vertrag | Produkt | Tarifgeneration | Beginn | Prämie | Währung | Alt-ID | Bemerkung |
|---|---|---|---|---|---|---|---|
| VTR-00000801 | PrivatPlus Einzel (Privathaftpflicht DE), Deckungssumme EUR 5 Mio., **Baustein Hundehalter seit 01.03.2019** | HP-MODERN | 01.01.2013 | 74.90 p. a. (2013); 131.40 p. a. ab 2019 inkl. Hund | EUR | HAPO 40.288.506-6 | Beratungsprotokoll DE 2019 zum Hundebaustein vorhanden; Prämienzahlung jährlich per Überweisung, zweimal Mahnstufe 1 (2021, 2023) |

## Ereignisgeschichte (2016–2025)

| Datum | Ereignis | Bezug |
|---|---|---|
| 2019-02 | Kunde meldet der Agentur die Anschaffung eines Hundes; Nachtrag Baustein Hundehalter ab 01.03.2019, Beratungsprotokoll DE mit Hinweis auf sächsische Hundehalterpflicht (vereinfacht) | V04, V09 |
| 2021-04 | Mahnung Stufe 1 nach vergessener Überweisung; Zahlung nach 9 Tagen | V12 |
| 2023-06 | Erneut Mahnung Stufe 1; Kunde beschwert sich telefonisch über den «Ton» der Mahnung | V12, INT-00000803 |
| 2025-03-21 | **Schaden:** Hund beisst beim Spaziergang einen Radfahrer in die Wade; Arztkosten (EUR 440), Schmerzensgeld (EUR 700) und Radhose (EUR 100), zusammen EUR 1'240; Meldung über Contact Center Leipzig, Telefonnotiz mit Stichworten «Hund, Biss, Radfahrer, Leine ja» | SCH-00000810, MINT claim |
| 2025-03-24 | **MINT Schaden-Triage v3 lehnt automatisch ab:** Regel «Tierhalter-Baustein» prüft das Feld `bausteine` des am 03.03.2025 in der Pilotwelle migrierten Vertrags; im Migrationsmapping der Pilotwelle wurde der HAPO-Bausteincode BST=01 nicht übernommen (Migrationsartefakt); Ablehnungsschreiben S13 mit Grund «kein Tierhalterbaustein» automatisch versandt, ohne menschliche Prüfung | S13, Regelkonfiguration, **Verstoss gegen Kompetenzordnung R08: Ablehnungen nie automatisch** |
| 2025-03-28 | Erster Beschwerdebrief des Kunden, scharf: Er habe den Baustein seit 2019, Beratungsprotokoll liege vor; fordert Zahlung binnen 14 Tagen und droht mit Presse | S25 |
| 2025-04-02 | Contact Center Leipzig antwortet mit Standardtext («Ihr Anliegen wird geprüft»); interne Weiterleitung an Team Schaden DE | INT-00000804 |
| 2025-04-15 | Zweiter Brief: Kunde wendet sich an den Versicherungsombudsmann und kündigt Beschwerde bei der BaFin an | S25, Ombudsmann-Korrespondenz |
| 2025-04-17 | Teamleiterin Schaden DE (Aylin Demirci, MIT-00009) erkennt den Fehler: Baustein in HAPO vorhanden; Zahlung EUR 1'240 an den Radfahrer, Entschuldigungsschreiben an den Kunden mit Kulanz EUR 100 für Aufwand | S14, S16, Kulanz |
| 2025-04-24 | Ombudsmann-Anfrage trifft ein; Stellungnahme durch Compliance DE (Miriam Steinbrecher, MIT-00012) | Ombudsmann-Korrespondenz |
| 2025-05 | **Root-Cause-Analyse:** 214 Verträge der Pilotwelle (Pieper eingeschlossen) ohne übernommenen Bausteincode, am 18.04. nachmigriert; 11 davon mit automatischer Ablehnung (Pieper eingeschlossen), bis 25.04. reguliert; Mapping vor der Hauptwelle 15.05. korrigiert; Änderung Kompetenzordnung R08 auf Version 2.1: Ablehnungen technisch nur mit Vier-Augen-Freigabe; Modellinventar-Eintrag Triage v3 mit Vorfall | Memo M06, Modellinventar, Vorfall VF-2025-03 |
| 2025-06-10 | BaFin-Beschwerde des Kunden trotz Regulierung eingegangen; Stellungnahme der Niederlassung; Verfahren im September abgeschlossen ohne Massnahme | Aufsichtskorrespondenz |
| 2025-07 | Kunde kündigt nicht, verlangt aber schriftliche Zusicherung, dass «kein Computer mehr über meine Schäden entscheidet»; Antwort mit Verweis auf Vier-Augen-Regel | INT-00000823 |
| 2025-11 | Jahresrechnung 2026 fristgerecht bezahlt, ohne Kommentar | Buchung |

## Kommunikationsstil

Handschriftlich oder mit Schreibmaschine gedruckte Briefe, mit Betreff in Grossbuchstaben («BESCHWERDE – SCHADEN NR. …»), Fristsetzungen, Unterstreichungen, Verweisen auf «mein gutes Recht» und auf Zeitungsberichte. Zitiert Paragraphen unvollständig, ist aber sachlich im Kern richtig. Am Telefon laut, unterbricht, lässt sich durch konkrete Zusagen beruhigen. Typische Formulierungen: «Ich lasse mir das nicht gefallen», «Sie haben das schriftlich», «Wer haftet für Ihren Computer?». Grussformel: «Hochachtungsvoll, H.-G. Pieper».

---

Fiktives Lehrbeispiel. Alle Daten synthetisch. Keine Verbindung zu realen Personen, Unternehmen oder Marken.
