# Pfefferminzia – Gesamtplan für den synthetischen Lehr-Datensatz

**Stand:** 2026-09-03 · **Status:** Entwurf zur Entscheidung · **Version:** 0.1

Dieses Dokument fasst die fünf Teilplanungen (Haftpflicht, Leben, Datenarchitektur, Use Cases, Regelwerke/Unternehmen) zu einem konsistenten Gesamtbild zusammen. Es benennt zuerst die Entscheidungen, die vor dem Bau getroffen werden müssen, dann die vollständige Artefakt-Landkarte, das Datenmodell, die Didaktik und den Umsetzungsplan. Die Teilplanungen enthalten die Detailtiefe (Feldlisten, Verteilungen, Paragraphenstruktur) und sind in Abschnitt 10 verlinkt.

---

## 1. Zweck und Zielbild

Pfefferminzia ist ein fiktiver Versicherer, der aus der Fusion der traditionellen **Pfefferminz Versicherung** mit dem KI-Start-up **Minzia** entstanden ist. Er bietet **Haftpflicht-** und **Lebensversicherungen** in der **Schweiz und Deutschland** an. Der Datensatz dient einem Executive-Kurs, in dem Führungskräfte aus der Versicherungsbranche KI-Use-Cases praktisch durchspielen.

Der Datensatz muss drei Dinge gleichzeitig leisten:

| Anforderung | Bedeutung für den Bau |
|---|---|
| **Fachlich glaubwürdig** | Produkte, Prozesse, Bedingungswerke und CH/DE-Unterschiede müssen so realistisch sein, dass Branchenprofis sie ernst nehmen. |
| **Didaktisch präpariert** | Der Datensatz enthält bewusst eingebaute Fallen (Bias, Leakage, Versionskonflikte, Datenqualität), deren Auflösung in einem Lösungsheft dokumentiert ist. |
| **Technisch zugänglich** | Teilnehmer arbeiten mit Excel, No-Code-Tools, Python, SQL und LLM-Datei-Upload. Alle Artefakte müssen in mehreren Formaten und Größenstufen vorliegen. |

Das Merger-Narrativ ist nicht Dekoration, sondern **Datenrealität**: zwei Kundenstämme, zwei Systemwelten, zwei Bedingungsgenerationen, eine historisch gewachsene Underwriting-Praxis. Die Teilnehmer schlüpfen in die vakante Rolle des Chief AI & Data Officer und müssen aus dieser Lage heraus KI-Entscheidungen treffen.

---

## 2. Entscheidungsbedarf vor dem Bau

Die Teilplanungen sind an einigen Stellen bewusst unabhängig voneinander entstanden und widersprechen sich. Die folgenden Punkte müssen festgelegt werden, bevor Daten erzeugt werden. Je Punkt ist eine Empfehlung angegeben.

### 2.1 Name des Unternehmens (kritisch)

Die Namensprüfung hat ergeben: **„Pfefferminzia" existiert real.** Es ist seit 2013 ein bekanntes deutsches Fachmedium für Versicherungsvermittler (Pfefferminzia Medien GmbH, Hamburg, mit Portal, Podcast und Maklerplattform). Die Redaktion führt zudem eine KI-Autorenfigur namens „Minzia Kolberg". Die Kurszielgruppe kennt dieses Medium mit hoher Wahrscheinlichkeit.

| Option | Bewertung |
|---|---|
| **A. Umbenennen** (z. B. „Menthalis Versicherungen", „Piperita Gruppe", „Krauseminz Versicherung") | Kollision entfällt, Minz-Metapher bleibt. Empfohlen, wenn der Name im Kurs noch nicht fest eingeführt ist. |
| **B. Beibehalten mit Abgrenzung** | Ausdrücklicher Disclaimer in jedem Artefakt, keine .de/.ch-Domains, nur `pfefferminzia.example`, Markenregisterprüfung (DPMA, Swissreg, EUIPO). Mindestlösung, falls der Name bereits gesetzt ist. |

**Empfehlung:** Option A prüfen, bevor die ersten Dokumente entstehen. Alle Teilplanungen sind namensneutral formuliert; ein späterer Austausch ist per Suchen-und-Ersetzen möglich, wird aber mit jedem erzeugten Dokument teurer.

### 2.2 Kanonische Zeitachse

Die Teams haben drei verschiedene Fusionsdaten verwendet. Vorschlag für eine verbindliche Zeitachse:

| Ereignis | Datum | Begründung |
|---|---|---|
| Gründung Pfefferminz | 1924, Olten (SO), als Genossenschaft | Alt genug für 100-jährige Tradition und Altbestand ab 1985 |
| Lebensversicherung bei Pfefferminz | 1961 | Erlaubt Tarifgenerationen ab PK-85 |
| Umwandlung in AG | 1998 | |
| Markteintritt Deutschland | 2006 | Ausreichend DE-Historie für Altverträge |
| Gründung Minzia | 2019, Berlin | KI-natives Start-up, ab 2021 digitaler Haftpflicht-Direktvertrieb |
| Beteiligung Pfefferminz an Minzia | 2023 | |
| Signing | Mai 2024 | |
| **Closing / Legal Day 1 / neue Marke** | **1. Januar 2025** | |
| PVS-Snapshot für Migration | 31. Dezember 2024 | Altsystem-Datenstand zum Fusionszeitpunkt |
| **Datensatz-Stichtag („heute")** | **31. Dezember 2025** | Sauberes Geschäftsjahresende, vollständiger Jahresbericht 2025, zwölf Monate Integrationsschmerz sichtbar |
| Bewegungsdaten | 2016–2025 (10 Jahre) | Zeitreihen, Saisonalität, Drift durch Fusion |
| Altverträge Leben | ab 1985 (Tarifgeneration PK-85) | |
| Altverträge Haftpflicht | ab 2001 | |

**Alternative:** Stichtag 30. Juni 2026 (Vorschlag des Regelwerk-Teams, 18 Monate nach Closing). Vorteil: mehr Post-Merger-Realität. Nachteil: kein sauberes Jahresende für Reports und Churn-Labels.

### 2.3 Mengengerüst und Größenstufen

Die Fachteams empfehlen kleinere Bestände (Haftpflicht ca. 8'000, Leben 2'000–5'000 Verträge), das Datenarchitektur-Team ein größeres Standardvolumen. Beides lässt sich über Größenstufen vereinen:

| Stufe | Umfang | Zweck | Priorität |
|---|---|---|---|
| **S – Sample** | ca. 1'000 Kunden, ca. 1'500 Verträge, < 20 MB, **alle** Dokumente gerendert | LLM-Datei-Upload, Handouts, 90-Minuten-Module, Live-Demos | **Zuerst bauen** |
| **M – Standard** | ca. 50'000 Partner, 75'000 Verträge, 27'000 Schäden/Leistungsfälle, 6'500 gerenderte Dokumente, 13'000 gerenderte Interaktionen | ML-Use-Cases mit statistisch belastbaren Mengen, Analytics | Version 1 |
| **L – Large** | ×5 gegenüber M, nur Parquet/SQLite | Performance-Demos, optional | Später |

Stufe S ist ein **echter Teilbaum** von Stufe M (gleiche IDs, gleiche Wahrheit), damit Ergebnisse übertragbar bleiben.

Verteilung in Stufe M (Vorschlag): 47 % CH / 53 % DE. Verträge: Privathaftpflicht 38'000, Betriebshaftpflicht 7'000, Risikoleben 11'000, Kapitalleben 12'000, Rente 7'000. Rund 660 echte Betrugsfälle.

### 2.4 Namen der IT-Systeme

Drei Teams haben unterschiedliche Systemnamen verwendet. Vorschlag für die kanonische Systemlandschaft:

| System | Herkunft | Rolle | Technische Charakteristik |
|---|---|---|---|
| **VERA** | Pfefferminz | Bestandsführung Leben (Host, COBOL, seit 1994) | Fixed-width, ISO-8859-1, 8-stellige Nummern, Datum als `YYYYMMDD`-Integer, Beträge in Rappen/Cent, kryptische Codes |
| **HAPO** | Pfefferminz | Bestandsführung Haftpflicht | Wie VERA, eigener Partnerstamm (Dubletten zu VERA) |
| **SILAS** | Pfefferminz | Schaden- und Leistungssystem beider Sparten | Semikolon-CSV-Exporte, überladene Freitextfelder |
| **DOKU** | Pfefferminz | Dokumentenarchiv | Scans ohne Textebene, OCR-Rauschen |
| **MINT** | Minzia | Kernsystem (Cloud, JSONL, UUIDs, ISO-Zeitstempel) | Schema-Drift v1–v3, Zeitzonenmix, Testdaten-Lecks |
| **Herbarium** | Minzia | Datenplattform / Lakehouse | Zielsystem der Migration, `curated`-Schicht |

Migration: zwei Wellen 2025 (Haftpflicht Q2, Leben Q4), dokumentiert in einem simulierten Migrationslog und einer Mapping-Tabelle.

### 2.5 Offene fachliche Entscheidungen

| Nr. | Frage | Empfehlung |
|---|---|---|
| F1 | Kapitalbildende Leben in DE nur als Altbestand oder auch Neugeschäft? | Nur Altbestand („Pfefferminz Kapital"), Neugeschäft DE ausschließlich Risiko und Rente |
| F2 | Basisrente/Riester in DE? | Weglassen, zu viel Regulatorik ohne didaktischen Mehrwert |
| F3 | Anteil französisch- und italienischsprachiger CH-Dokumente? | 15 % FR, 5 % IT in Haftpflicht-Kundendokumenten; Regelwerke nur DE |
| F4 | Schadenfotos generieren? | Platzhalterbilder mit EXIF-Metadaten (Datum, Gerät, GPS) statt generierter Fotos; EXIF trägt die Widersprüche |
| F5 | Gesundheitsfragen im Antrag Leben? | Ja/Nein-Fragen plus Freitext, Diagnosen auf ICD-10-Gruppenebene aus einer Diagnose-Bibliothek |
| F6 | AHV-Nummer und Steuer-ID im Datensatz? | Ja, prüfziffernvalide aber fiktiv; nötig für PII-Detektor-Use-Case |
| F7 | Rückversicherung abbilden? | Nur als Referenztabelle (Verträge, Quoten), keine Bewegungsdaten |
| F8 | Fondskurse für fondsgebundene Leben? | Nicht in Version 1 |
| F9 | Gemeinsamer Partnerstamm über beide Sparten? | Ja in `curated`, getrennt in `raw` (VERA vs. HAPO), das ist die Dubletten-Übung |
| F10 | Zugriffsschutz für Ground Truth? | Separates Release-Paket `truth`, nur Dozenten, Hashes im öffentlichen Manifest |

---

## 3. Produktportfolio (verbindliche Auswahl)

### 3.1 Haftpflicht

| Produkt | Marktname | Zielgruppe | Charakter im Datensatz |
|---|---|---|---|
| Privathaftpflicht | PrivatPlus | Privatpersonen, Familien | Massengeschäft, viele Kleinschäden, höchstes Betrugspotenzial |
| Betriebshaftpflicht | BusinessProtect | KMU nach Branchenklassen (NOGA CH / WZ DE) | Underwriting-Entscheidungen, mittlere Schäden, Regress |
| Berufshaftpflicht | ProfessionalShield | Architekten/Ingenieure, Treuhänder/Steuerberater, IT-Dienstleister, Unternehmensberater | Wenige, große, langlaufende Vermögensschäden, Claims-made vs. Verstoßprinzip |

Bausteine (keine eigenen Produkte): Tierhalter, Bauherren, Öltank/Gewässerschaden, Gebäude, Produkthaftpflicht. Bausteine erzeugen Deckungsgrenzfälle (Sublimits, fehlende Bausteine, Hundehalterpflicht je Kanton/Bundesland).

Bedingungsgenerationen: **Pfefferminz Klassik** (bis 2012), **Pfefferminz Modern** (2013–2020), **Minzia Direct** (2021–2024, nur Privathaftpflicht), **Pfefferminzia** (ab 2025). Dasselbe Schadenereignis ist je nach Generation unterschiedlich gedeckt.

### 3.2 Leben

| Produkt | Marktname | Märkte | Charakter im Datensatz |
|---|---|---|---|
| Risikolebensversicherung | RisikoLeben | CH, DE | Kernprodukt, Minzia-Erbe, volldigitaler Antrag, automatisierte Risikoprüfung |
| Gemischte Lebensversicherung | Vorsorge | CH Neugeschäft (Säule 3a/3b), DE nur Altbestand | Altverträge mit Garantiezins, Rückkauf, Überschuss |
| Aufgeschobene Rente | RentePlus | DE-Schwerpunkt, CH als Auszahlungsoption | Langläufer, Rentenbeginn, Bezugsrecht |
| Erwerbs-/Berufsunfähigkeit | Zusatzbaustein | CH (EU mit IV-Koordination), DE (BUZ) | Leistungsprüfung mit Arztberichten |

Tarifgenerationen: zehn Generationen von **PK-85** bis **PZ-2025** mit historisch korrekten Höchstrechnungszinsen (DE 4,0 % bis 0,25 %, ab 2025 1,0 %), Unisex-Bruch 2012 in DE, DM-umgerechnete Summen in Altverträgen. Rund 55–60 % des Leben-Bestands ist Altbestand.

---

## 4. Artefakt-Landkarte

Die Artefakte sind in acht Gruppen gegliedert. Die Spalte „Use Cases" verweist auf den Katalog in Abschnitt 6. Die Spalte „Detail" verweist auf die Teilplanung.

### 4.1 Gruppe A – Unternehmenskontext und Merger-Narrativ

| Artefakt | Umfang | Zweck | Use Cases | Detail |
|---|---|---|---|---|
| Unternehmensprofil und Eckdaten | 3 Seiten + Kennzahlen-Masterdatei | Single Source of Truth für alle Zahlen in Reports, Memos, Präsentationen | alle | 05 §1 |
| Unternehmensgeschichte Pfefferminz und Minzia | je 3–4 Seiten | Narrativ, Kontext für Kulturkonflikt | Onboarding, Zusammenfassung | 05 §2 |
| Zusammenfassung Fusionsvertrag (Term Sheet) | 3 Seiten | Governance-Zusagen, Earn-out an Minzia-Gründer bei KI-KPIs | Governance | 05 §2 |
| Strategie 2030 „Wurzeln & Flügel" | 12 Seiten | Bewusst naive KI-Annahmen als Diskussionsgrundlage | Governance, Strategie | 05 §2 |
| CEO-Strategie-Memo | 2 Seiten | Auslöser für die Teilnehmerrolle | Einstieg | 04 §4 |
| Board-Präsentation KI-Roadmap | 20 Folien (als Markdown/PDF) | Zusammenfassung, Kritik | Governance | 04 §4 |
| Organigramm mit Rollen | 1 Diagramm + Tabelle | inkl. Data & AI Office, vakante CAIDO-Rolle | alle | 05 §1 |
| Verwaltungsrats- und Geschäftsleitungsprotokolle | 6 VR + 8 GL, je 2–4 Seiten | Widersprüche zwischen öffentlichem und internem Narrativ | Zusammenfassung, RAG | 05 §2 |
| Interne Memos | 12–15, je 1–2 Seiten | Integrationsstreit, Datenqualität, Make-or-buy | RAG, Zusammenfassung | 05 §2 |
| Mitarbeiter-Newsletter „Minzblatt" | 8 Ausgaben | Kulturwandel | Sentiment | 05 §2 |
| Pressemitteilungen | 8, je 1–2 Seiten, de-CH und de-DE | Öffentliches Narrativ | Vergleich intern/extern | 05 §2 |
| Integrations-Roadmap | 4 Seiten + Gantt | Migrationswellen, Systemabschaltungen | Kontext für Datenqualität | 05 §2 |
| Kulturumfrage | n = 1'830, CSV + Auswertung | Haltung zu KI nach Herkunft (Pfefferminz/Minzia) | Analytics, Bias | 05 §2 |
| Town-Hall-Transkripte | 3, je 8–10 Seiten | Zusammenfassung, Sentiment | GenAI | 05 §2 |
| Mitarbeiterinterviews | 30, je 2–3 Seiten | Rückschlussrisiko, Anonymisierung | PII, Zusammenfassung | 04 §4 |
| Fiktiver Aufsichtsbrief (FINMA) | 2 Seiten | Auslöser für KI-Governance-Use-Case | Governance | 04 §4 |
| Persona-Rollenkarten | 14 Mitarbeiter, 10 Kunden | Tragen Korrespondenz und Gruppenarbeit | alle | 05 §6 |

### 4.2 Gruppe B – Regelwerke

**Übergreifend (Gruppe):**

| Regelwerk | Umfang | Rolle für KI-Use-Cases | Detail |
|---|---|---|---|
| KI-Governance-Richtlinie | 15 Seiten + Modellinventar (20 Einträge) | Vierstufige Risikoklassifizierung deckungsgleich mit EU AI Act; Leben-Risikoprüfung als Hochrisiko | UC-19, RAG | 05 §3 |
| Datenschutzrichtlinie (DSG CH / DSGVO DE) | 12 Seiten | Gesundheitsdaten, Art. 21 DSG / Art. 22 DSGVO automatisierte Entscheidungen | UC-18, Compliance-Check | 05 §3 |
| Compliance-Handbuch | 20 Seiten | Referenz für Prüf-Use-Cases | RAG | 05 §3 |
| Kompetenz- und Vollmachtsordnung | 8 Seiten | Explizite KI-Entscheidungsgrenzen: Automatisierung nur bei positiven Entscheiden unter Schwelle, Ablehnungen immer durch Menschen | Audit, Agenten | 05 §3 |
| Geldwäscherei/AML (Leben) | 8 Seiten | Einmalprämien, wirtschaftlich Berechtigte | Anomalie | 05 §3 |
| Beschwerdemanagement-Richtlinie | 6 Seiten | Fristen, Eskalation, Ombudsmann/BaFin | Triage | 05 §3 |
| Outsourcing-Richtlinie | 8 Seiten | Minzia Technologies als gruppeninterner Dienstleister; FINMA-RS 2018/3, § 32 VAG, DORA | Governance | 05 §3 |
| Informationssicherheit, Verhaltenskodex, Prozesslandkarte | je 5–10 Seiten | Kontext, RAG-Korpus | RAG | 05 §3 |
| Regulatorischer Vergleich CH/DE | 30-zeilige Tabelle als Markdown und CSV | Referenz für Konformitätsprüfungen; alle Angaben „vereinfacht, zu verifizieren" | Compliance-Check | 05 §4 |

**Haftpflicht:**

| Regelwerk | Umfang | Besonderheit | Detail |
|---|---|---|---|
| AVB CH (Teile A–F) je Generation | 4 Versionen × ca. 25 Seiten | Bewusst abweichende Klauseln je Generation | 01 §7 |
| AHB/BBR DE nach GDV-Systematik je Generation | 4 Versionen × ca. 30 Seiten | | 01 §7 |
| Besondere Bedingungen je Baustein | je 2–4 Seiten | Sublimits | 01 §7 |
| Zeichnungsrichtlinien | ca. 35 Seiten je Land | Branchenklassen, Ablehnungsgründe | 01 §7 |
| Schadenregulierungsrichtlinie | ca. 45 Seiten, Länderabschnitte | Trennung Deckungsprüfung / Haftungsprüfung | 01 §7 |
| Tarifhandbuch | ca. 25 Seiten je Land, formelbasiert | Prämien nachrechenbar; 3–5 % der Verträge weichen bewusst ab | 01 §7 |
| Vollmachtsregelung Schaden | fünf Stufen | 1–2 % der Zahlungen verletzen die Stufe | 01 §7 |

**Leben:**

| Regelwerk | Umfang | Besonderheit | Detail |
|---|---|---|---|
| AVB je Tarifgeneration und Land | 10 Generationen × 14 Paragraphen | Suizidfrist 1 vs. 3 Jahre, Flugrisiko-Ausschluss 1985, Nachversicherungsgarantie nur Minzia | 02 §6 |
| Tarifbestimmungen | je Generation | Rechnungszins, Sterbetafel, Kosten | 02 §6 |
| Annahmerichtlinien (medizinisch) | ca. 40 Seiten | Konkrete BMI-, Raucher-, Vorerkrankungstabellen mit Zuschlägen | 02 §6 |
| Leistungsprüfungsrichtlinie | ca. 30 Seiten | Kulanzkompetenzen, Nachweise | 02 §6 |
| Überschussregelung | DE MindZV, CH Überschussplan | Standmitteilungen | 02 §6 |

Alle Regelwerke tragen einen **Metadaten-Header** (Dokument-ID, Version, Markt, gültig ab/bis, Sparte, Generation) und eine stabile Paragraphenstruktur, damit RAG-Antworten zitierfähig sind.

### 4.3 Gruppe C – Strukturierte Daten (Kernentitäten)

Rund 30 Tabellen in drei Schichten (siehe Abschnitt 5). Die wichtigsten:

| Entität | Inhalt | Sparte | Detail |
|---|---|---|---|
| Partner, Partnerrolle, Adresse (mit Historie), Beziehung | Kunden, versicherte Personen, Bezugsberechtigte, Geschädigte | beide | 03 §1, 01 §6, 02 §5 |
| Antrag, Risikofrage, Antwort | inkl. Gesundheitsangaben (Leben), Risikoangaben (Haftpflicht) | beide | 02 §5, 01 §6 |
| Risikoprüfung / Underwriting-Entscheidung | normal, Zuschlag, Ausschluss, Zurückstellung, Ablehnung, mit Sachbearbeiter und Zeitstempel | Leben (Haftpflicht Betrieb/Beruf) | 02 §5 |
| Vertrag, Vertragsversion, Deckung, Risikoobjekt | Status, Generation, Prämie, Bausteine, Nachträge | beide | 03 §1 |
| Bezugsrecht (Historie) | widerrufliche/unwiderrufliche Bezugsrechte, Änderungen | Leben | 02 §5 |
| Schaden / Leistungsfall, Schadenposition, Beteiligte, Statushistorie, Reservehistorie | Deckungs- und Haftungsstatus getrennt, Abwehr, Regress | beide | 01 §6, 02 §5 |
| Rechnung, Buchung, Zahlung, Mahnung | Prämien, Leistungen, Rückkäufe, Mahnstufen | beide | 03 §1 |
| Wertstand | Deckungskapital, Rückkaufswert, Überschuss je Stichtag | Leben | 02 §5 |
| Dokument (Metadaten) | Typ, Quelle, Datum, Pfad, OCR-Status | beide | 03 §1 |
| Interaktion, Thread | E-Mail, Anruf, Chat, Brief, Kanal, Sentiment | beide | 03 §1 |
| Aufgabe / Workflow-Schritt | Bearbeitungsschritte, Durchlaufzeiten | beide | 03 §1 |
| Beschwerde | Grund, Eskalation, Ombudsmann | beide | 03 §1 |
| Vermittler, Agentur | Ausschließlichkeit, Makler, Direkt, Bancassurance | beide | 03 §1 |
| Mitarbeiter, Organisationseinheit | Herkunft Pfefferminz/Minzia, Rolle, Kompetenzstufe | beide | 03 §1 |
| Produkt, Tarifgeneration, Deckungsart, Branchenklasse, Diagnose-Bibliothek | Stammdaten | beide | 03 §1 |
| Kennzahlen-Masterdatei | Alle Zahlen für Reports und Narrativ | beide | 05 §5 |
| Kreuzreferenzen, Feldmapping, Migrationslog | Verbindung raw ↔ curated | beide | 03 §2 |

### 4.4 Gruppe D – Unstrukturierte Dokumente

| Bereich | Dokumenttypen | Formate | Detail |
|---|---|---|---|
| Haftpflicht Vertrag | 22 Typen: Antrag, Offerte, Police, Nachtrag, Beratungsprotokoll (nur DE), Kündigung, Mahnung, Prämienrechnung u. a. | Markdown-Quelle → PDF/DOCX, Teil als simulierter Scan | 01 §5 |
| Haftpflicht Schaden | 27 Typen: Schadenmeldung, Schadenanzeige Dritter, Gutachten, Kostenvoranschlag, Anwaltsschreiben, Regressforderung, Ablehnungsschreiben, Fotos (Platzhalter mit EXIF) | PDF, EML, JPG | 01 §5 |
| Leben | 42 Typen: Antrag mit Gesundheitsfragebogen (je Generation), ärztliches Zeugnis, Police, Standmitteilung, Überschussmitteilung, Bezugsrechtsänderung, Rückkaufsberechnung, Leistungsantrag, Sterbeurkunde/Todesbescheinigung, Erbschein, Korrespondenz mit Hinterbliebenen | PDF, Scan mit OCR-Rauschen, Handschrift-Simulation | 02 §4 |
| Beschwerden | Beschwerdebriefe, Ombudsmann-Korrespondenz, BaFin-Anfragen | PDF, EML | 05 §3 |
| Ground-Truth-JSON je Dokument | Extrahierte Sollwerte für einen Teil der Dokumente | JSON | 01 §5 |

Alle Dokumente tragen einen Disclaimer und einen Metadaten-Header. Sprachen: de-CH (ss statt ß, CHF, Schweizer Terminologie), de-DE, in Haftpflicht CH-Kundendokumenten 15 % FR und 5 % IT.

### 4.5 Gruppe E – Kommunikation und Interaktionen

| Artefakt | Umfang (Stufe M) | Besonderheit | Use Cases |
|---|---|---|---|
| E-Mails (EML) | 13'000 gerendert, 300'000 Metadaten | Threads, Anhänge, Prompt-Injection in einzelnen Kundenmails | Triage, Extraktion |
| Anruf-Transkripte (JSON) | Teil der 13'000 | Sprecherwechsel, Emotionen | Zusammenfassung, Sentiment |
| Chat-Protokolle (JSON) | Teil der 13'000 | Minzia-Chatbot kennt nur Minzia-AVB (bewusste Falle) | RAG-Evaluation |
| Deckungsfragen mit Musterantworten | 100 Haftpflicht + 100 Leben | Evaluationsset für RAG | UC-11 |

### 4.6 Gruppe F – Reports und Meldewesen

20 Berichtsartefakte, jeweils als narratives Dokument plus CSV, alle aus der Kennzahlen-Masterdatei gespeist: Quartalsspiegel, Schadenquoten-Report, Leben-Report, Vertriebsreport, Beschwerdestatistik, ORSA-Bericht, SST-Finanzlage (CH), SFCR/QRT (DE), Geschäftsbericht, Modellrisiko-Report, KPI-Dashboards, Aufsichtskorrespondenz. Detail: 05 §5.

### 4.7 Gruppe G – Ground Truth und Lösungsheft (nur Dozenten)

| Artefakt | Inhalt |
|---|---|
| 14 Label-Dateien (L01–L14) | Churn, Betrug, Dublette, Schadenkategorie, Underwriting-Bias-Marker, Extraktions-Sollwerte, PII-Positionen, AI-Act-Klasse, Deckungs-Sollantwort u. a. |
| Latente Wahrheit | Echte Betrugsabsicht, echte Kündigungsneigung, Ursachen; sichtbare Labels sind verrauscht und zeitlich beschnitten |
| DQ-Injektionsprotokoll | Welche der 28 Datenqualitätsregeln wo angewendet wurden |
| Fallenkatalog | 16 Fallen mit Konstruktion, erwartetem naivem Verhalten, Lernmoment, Nachweis |
| Redaktionsnotiz Narrativ | Alle bewusst eingebauten Widersprüche im Merger-Narrativ |
| Referenz-Notebooks | Offline, fixer Seed, Laufzeit < 5 Minuten, Toleranzbänder statt Punktwerte |
| Bewertungsrubriken | „Was hätte man merken müssen"-Listen je Use Case |
| Vorgegebene Train/Test-Splits | Stabil über Generatorläufe |
| „Saubere" Variante ohne Fallen | Kontrollgruppe |

### 4.8 Gruppe H – Generator, Tooling und Bereitstellung

| Artefakt | Inhalt | Detail |
|---|---|---|
| Python-Generator | Zehn Stufen: config → reference → organisation → partner → antrag/vertrag → schaden → finanz → prozess → text → render → legacyify/mintify → export → validate | 03 §5 |
| Seed-Konzept | Master-Seed, entitätsbezogen abgeleitete Seeds, versionierter LLM-Cache; Releases byte-identisch reproduzierbar | 03 §5 |
| Validierungssuite (CI) | Schema, Referenzintegrität, Zeitregeln, bilanzielle Summen, Verteilungen, Label-Signal-Kohärenz, Fiktionalitäts-Blocklists, Referenz-Parser raw → curated ≥ 97 % | 03 §5 |
| Data Dictionary, JSON Schema, Manifest | Generiert, deutsch und englisch | 03 §4 |
| Release-Pakete | `core` (≤ 250 MB), `raw`, `documents` (je Sparte), `communications`, `sample`, `truth` (zugriffsbeschränkt) | 03 §7 |
| Onboarding-Guide für Teilnehmer | Wie lese ich den Datensatz, Glossar CH/DE | 05 Anhang B |

---

## 5. Datenmodell in Kurzfassung

### 5.1 Drei Schichten

| Schicht | Inhalt | Zugriff |
|---|---|---|
| `raw` | Zwei bewusst verschmutzte Quellsysteme: Pfefferminz-Altsysteme (Fixed-width, ISO-8859-1, Codes) und MINT (JSONL, UUIDs, Schema-Drift). Getrennte Partnerstämme. | Teilnehmer |
| `curated` | Harmonisiertes, dokumentiertes Zielmodell mit lesbaren Präfix-IDs (`PTR-00012345`), Feld `quelle` (PF/MZ), Rest-Unschärfe und `dq_flags` | Teilnehmer |
| `truth` | Latente Wahrheit, vollständige Labels, Injektionsprotokolle | Dozenten |

### 5.2 Generierungsprinzip

Der Generator erzeugt zuerst eine **latente wahre Welt** (wer betrügt wirklich, wer wird wirklich kündigen, welche Vorerkrankung liegt wirklich vor) und leitet daraus sowohl die sichtbaren, fehlerbehafteten Beobachtungen als auch die Labels ab. Sichtbare Labels sind verrauscht und zeitlich beschnitten (Betrugsflag nur für vor 2023 geschlossene Fälle), `truth` ist vollständig.

### 5.3 Fiktionalität

Reale Postleitzahlen und Orte, aber ausschließlich generierte Straßennamen. Kuratierte Namenslisten mit Prominenten-Blocklist. Nur `.example`-Domains. Nicht vergebbare Telefonnummern. Prüfziffernvalide, aber fiktive IBAN, UID, AHV-Nummer, Steuer-ID. Keine Gesichter oder Kennzeichen. Disclaimer in jedem Dokument.

---

## 6. Use Cases und Didaktik

### 6.1 Must-have für Version 1

| Nr. | Use Case | KI-Typ | Modul | Zentrale Falle |
|---|---|---|---|---|
| UC-08 | Dublettenerkennung über zwei Kundenstämme | Datenqualität, Matching | 1 Daten verstehen | Zwei Systemwelten, Umlaute, Adressformate |
| UC-02 | Stornoprognose | Klassisches ML | 3 ML | Leakage durch Kündigungsgrund im Feature |
| UC-05 | Risikoprüfung Leben mit historischem Bias | Klassisches ML, Fairness | 3 ML | Bias nach PLZ, Geschlecht (pre-Unisex), Herkunft |
| UC-15 | Betrugserkennung Haftpflicht | Anomalie, Klassifikation | 3 ML | Ehrliche Fälle mit Betrugssignalen |
| UC-04 | Antragsextraktion aus Scans | GenAI Extraktion | 4 GenAI | OCR-Rauschen, Generationen des Fragebogens |
| UC-11 | AVB-Chatbot mit RAG | GenAI RAG | 4 GenAI | Widersprüchliche Bedingungsversionen, Chatbot kennt nur Minzia-AVB |
| UC-18 | PII- und Gesundheitsdaten-Detektor | GenAI Klassifikation | 4 GenAI | Gesundheitsdaten in Freitext, Rückschluss aus Interviews |
| UC-19 | AI-Act/FINMA/BaFin-Risikoklassifizierung des Modellinventars | Governance | 6 Governance | Hochrisiko-Einstufung Leben-Risikoprüfung |

Nice-to-have (16 weitere) in 04 §1, darunter Schadenklassifikation, E-Mail-Triage, Beschwerde-Analyse, Reserveprognose, Agenten-Demo mit Claude Code.

### 6.2 Dramaturgie in sechs Modulen

1. **Daten verstehen und Datenqualität** (UC-08): Zwei Welten, Dubletten, Migrationslog.
2. **Analytics**: Kennzahlen, Schadenquoten, Kulturumfrage.
3. **Klassisches ML** (UC-02, UC-05, UC-15): Leakage, Bias, False Positives.
4. **GenAI und RAG** (UC-04, UC-11, UC-18): Extraktion, Bedingungswerke, Datenschutz.
5. **Agenten**: Live-Demo auf den Dublettendaten.
6. **Governance, Regulatorik, Change** (UC-19): Modellinventar, Kompetenzordnung, Entscheidung als CAIDO.

Leitprinzip: **erst scheitern, dann verstehen.** Jede Übung beginnt mit einem naiv zu guten oder zu schlechten Ergebnis und endet mit einer Management-Entscheidung, nicht mit einem Modell. Rollenkarten (CEO, CFO, CTO, Chief Underwriter, Data Science, Datenschutz) für Gruppenarbeiten.

### 6.3 Fallenkatalog (Auswahl)

| Falle | Konstruktion | Lernmoment |
|---|---|---|
| Underwriting-Bias | Historische Zuschläge korrelieren mit PLZ und Herkunft | Fairness, Art. 21 DSG / Art. 22 DSGVO |
| Leakage | Kündigungsgrund und Rückkaufsdatum als Feature verfügbar | Zeitliche Konsistenz |
| AVB-Versionskonflikt | Gleiche Frage, vier Generationen, vier Antworten | RAG braucht Metadaten |
| Gesundheitsdaten im Freitext | Diagnose in E-Mail-Betreff | Besondere Kategorien |
| Drift | Tarifwechsel 2021 und Fusion 2025 verändern Verteilungen | Modell-Monitoring |
| Prompt-Injection | Kundenmail enthält Anweisung an den Assistenten | Agentensicherheit |
| Survivorship-Bias | Reserven nur für abgeschlossene Fälle | Statistik |
| Rückschlussrisiko | Interview-Anonymisierung scheitert an Rollenkombination | Anonymisierung |
| Agenten-Mandatsüberschreitung | Agent zahlt über Vollmachtsstufe | Kompetenzordnung |
| Legitime Fälle, die wie Betrug aussehen | Dezember-2004-Welle, Serienschäden Handwerker | False Positives |

Vollständig: 04 §5 (16 Fallen), 01 §8 (47 Stolpersteine Haftpflicht), 02 §7 (25 Stolpersteine Leben).

---

## 7. Konventionen

| Thema | Festlegung |
|---|---|
| Sprache | Deutsch; de-CH und de-DE unterscheiden sich in Rechtschreibung (ss/ß), Währung, Terminologie (Offerte/Angebot, Police/Versicherungsschein, Prämie/Beitrag) |
| Formate | Parquet kanonisch; CSV (UTF-8 mit BOM, Komma, ISO-Datum); SQLite mit Views; XLSX-Bundles; JSONL für MINT-raw; Fixed-width/Semikolon-CSV für Altsystem-raw; Markdown → PDF/DOCX für Dokumente; EML; JSON für Transkripte |
| Identifikatoren | curated: lesbare Präfixe (`PTR-`, `VTR-`, `SCH-`, `DOK-`); raw: systemspezifisch |
| Metadaten | `manifest.json`, JSON Schema je Tabelle, Data Dictionary DE/EN |
| Versionierung | SemVer; MAJOR = Schemabruch, MINOR = neue Tabellen/Labels/Text-Refresh, PATCH = Korrekturen |
| Lizenz | CC BY 4.0 für Daten und Texte (keine NC-Klausel, damit Teilnehmer intern weiterarbeiten dürfen), MIT für Generator-Code |
| Disclaimer | Lang-, Kurz- und EN-Fassung in 05 §7; Provenienzhinweis für KI-generierte Inhalte |
| Regulatorische Aussagen | Immer als „vereinfacht, Stand 2026, zu verifizieren" gekennzeichnet; juristische Prüfung vor Kurseinsatz empfohlen |

---

## 8. Umsetzungsplan in Wellen

Abhängigkeiten bestimmen die Reihenfolge. Jede Welle liefert ein testbares Zwischenergebnis.

| Welle | Inhalt | Ergebnis | Abhängig von |
|---|---|---|---|
| **0 Fundament** | Entscheidungen aus Abschnitt 2 (Name, Zeitachse, Systeme, Mengen), Kennzahlen-Masterdatei, Unternehmensprofil, Organigramm, Personas, Stammdaten (Produkte, Generationen, Branchenklassen, Diagnose-Bibliothek), Repository-Struktur, Generator-Skelett mit Seed-Konzept | Konsistente Welt-Definition | – |
| **1 Kundenstamm und Verträge** | Partner, Adressen, Vermittler, Mitarbeiter, Verträge beider Sparten in `curated`; dann `legacyify`/`mintify` nach `raw`; Feldmapping, Migrationslog; Validierungssuite Stufe 1 | UC-08 Dubletten lauffähig (Modul 1) | Welle 0 |
| **2 Bewegungsdaten** | Rechnungen, Buchungen, Mahnungen, Interaktions-Metadaten, Aufgaben, Beschwerden, Vertragsereignisse, Wertstände; Churn-Labels | UC-02 Storno lauffähig (Modul 3) | Welle 1 |
| **3 Underwriting Leben** | Anträge mit Gesundheitsfragen je Generation, Risikoprüfungsentscheidungen mit historischem Bias, Annahmerichtlinien als Dokument | UC-05 lauffähig | Welle 1 |
| **4 Regelwerke und RAG-Korpus** | Alle AVB-Generationen beider Sparten, übergreifende Richtlinien, Regulatorik-Tabelle, 200 Deckungsfragen mit Musterantworten | UC-11 RAG lauffähig (Modul 4) | Welle 0 |
| **5 Schäden und Leistungsfälle** | Schäden Haftpflicht, Leistungsfälle Leben, Positionen, Reserven, Beteiligte, Betrugsmuster, Schadenregulierungsrichtlinie, Vollmachtsverstöße | UC-15 Betrug lauffähig | Welle 2 |
| **6 Dokumente rendern** | Antragsscans, Policen, Schadenmeldungen, Gutachten, Korrespondenz, E-Mails, Transkripte; Ground-Truth-JSON; PII-Labels | UC-04, UC-18 lauffähig | Wellen 3, 5 |
| **7 Narrativ und Governance** | Merger-Dokumente, Protokolle, Memos, Reports aus Masterdatei, Modellinventar, KI-Governance-Richtlinie, Fallenkatalog konsolidiert, Lösungsheft, Referenz-Notebooks, Release-Pakete | UC-19 lauffähig (Modul 6); Version 1.0 | alle |

Empfehlung: **Stufe S zuerst vollständig durch alle Wellen**, dann Stufe M. So entsteht früh ein komplettes, kleines Beispiel, an dem Didaktik und Konsistenz geprüft werden können, bevor teure Mengen erzeugt werden.

---

## 9. Offene Punkte und Risiken

| Nr. | Punkt | Risiko | Vorschlag |
|---|---|---|---|
| R1 | Namenskollision Pfefferminzia | Verwechslung, Kennzeichenrecht | Entscheidung 2.1 vor Welle 0 |
| R2 | Juristische Genauigkeit der Regulatorik | Falsche Rechtsaussagen im Kurs | Alle Angaben markiert; Review durch Legal vor Kurseinsatz |
| R3 | LLM-generierte Texte (Anwaltsschreiben, Gutachten) | Inkonsistenz mit Tabellen | Vorlagen-Constraints, Abgleichstest Dokument ↔ Tabelle in der Validierungssuite |
| R4 | Aufwand Dokumentrendering | Größter Kostenblock | Stufe S vollständig, Stufe M nur Teilmenge rendern (6'500 Dokumente) |
| R5 | Ground-Truth-Leck | Teilnehmer finden Lösungen | Separates Paket `truth`, kein Zugriff über das Teilnehmer-Repository |
| R6 | EU AI Act Hochrisiko-Zeitplan | Fristen ändern sich | Als Variable im Datensatz, nicht als Fakt |
| R7 | Gesundheitsdaten | Auch synthetisch sensibel wirkend | Diagnose-Bibliothek auf Gruppenebene, von Identität getrennt erzeugt, Kennzeichnung |
| R8 | Reproduzierbarkeit LLM-Texte | Neue Modellversionen ändern Texte | Versionierter LLM-Cache im Repository |

---

## 10. Teilplanungen

| Dokument | Inhalt | Umfang |
|---|---|---|
| [01-haftpflicht.md](01-haftpflicht.md) | Produkte, Lebenszyklus, Schadenprozess mit Verteilungen, 49 Dokumenttypen, Feldlisten, Regelwerke, 47 Stolpersteine | 980 Zeilen |
| [02-leben.md](02-leben.md) | Produkte, zehn Tarifgenerationen, Lebenszyklus, Leistungsfall, 42 Dokumenttypen, Feldlisten, Annahmerichtlinien, 25 Stolpersteine | 731 Zeilen |
| [03-datenarchitektur.md](03-datenarchitektur.md) | Entitätsmodell mit ER-Diagramm, zwei Quellsysteme, 28 DQ-Regeln, Mengengerüst, Formate, Generator-Pipeline, Validierung, Fiktionalität, Lizenz | 982 Zeilen |
| [04-use-cases.md](04-use-cases.md) | 24 Use Cases, Artefakt-Register (15 Tabellen, 15 Korpora, 14 Label-Dateien), Matrizen, Dramaturgie, 16 Fallen, Lösungsheft, Lieferplan | 908 Zeilen |
| [05-regelwerke-unternehmen.md](05-regelwerke-unternehmen.md) | Unternehmensprofil, Merger-Dokumente, 13 Gruppenrichtlinien, CH/DE-Vergleich, 20 Reports, 24 Personas, Namensprüfung, Disclaimer | 624 Zeilen |

Die Teilplanungen verwenden teilweise abweichende Zeitachsen, Systemnamen und Mengen. Bei Widersprüchen gilt dieser Gesamtplan.
