# Planung 05 – Übergreifende Regelwerke und Unternehmenskontext „Pfefferminzia"

**Status:** Planungsdokument (keine ausformulierten Artefakte), Stand 3. September 2026
**Arbeitspaket:** Unternehmensprofil, Merger-Narrativ, übergreifende Regelwerke, CH/DE-Regulierungsvergleich, Meldewesen, Personas, rechtliche Hinweise zum Datensatz
**Schnittstellen:** AP Sparten-Fachinhalte (AVB, Zeichnungsrichtlinien), AP Datenarchitektur, AP Use Cases

---

## 0. Leitplanken und Konventionen für alle Artefakte

| Thema | Festlegung | Begründung |
|---|---|---|
| Datensatz-Stichtag („heute" im Datensatz) | **30. Juni 2026**; Historie ab Gründung 1924, Detaildaten ab Geschäftsjahr 2023 | Ein fixer Stichtag verhindert Widersprüche zwischen Reports, Memos, Protokollen |
| Merger-Zeitachse | Beteiligung 2023 → Signing 05/2024 → Closing/rechtliche Fusion 01.01.2025 → Rebranding 01.01.2025 → Integrationsphase bis 2027 | Dataset-„Gegenwart" liegt 18 Monate nach Closing: Integrationsschmerzen sind sichtbar, aber nicht abgeschlossen |
| Zentrale Zahlenwahrheit | **Eine Kennzahlen-Masterdatei** (`kennzahlen-master.csv/xlsx`) aus der alle Berichte, Pressemitteilungen, Protokolle und Dashboards ihre Zahlen ziehen | Zusammenfassungs- und Analytics-Use-Cases scheitern sofort an inkonsistenten Zahlen |
| Sprachvarianten | Jedes Dokument trägt ein Metadatum `locale: de-CH` oder `de-DE`; CH-Dokumente konsequent ohne ß, DE-Dokumente mit ß | Sichtbare Marktunterschiede, Testfall für Sprachmodelle |
| Fiktionalität | Fiktive Domain `pfefferminzia.example` (RFC 2606), keine realen Adressen/Telefonnummern/IBAN, kein Bezug auf reale Firmen, siehe Kap. 7 | Rechtliche Absicherung, Verwechslungsschutz |
| Dokument-Metadaten | Jedes Artefakt: `doc_id`, `titel`, `typ`, `absender_rolle`, `datum`, `locale`, `vertraulichkeit` (öffentlich/intern/vertraulich/streng vertraulich), `version`, `gilt_fuer` (CH/DE/Gruppe), `quelle_kennzahlen` | Ermöglicht RAG-Filterung, Berechtigungs-Use-Cases, Versionierungs-Use-Cases |
| Regulatorische Zitate | Immer mit Gesetz + Artikel/Paragraph und dem Hinweis „vereinfachte Darstellung, Stand 2026"; im Datensatz nur als Verweis, nie als Wiedergabe längerer Gesetzestexte | Keine Urheberrechts-/Aktualitätsrisiken, gleichzeitig realistischer Ton |

---

## 1. Unternehmensprofil Pfefferminzia

### 1.1 Eckdaten (Vorschlag)

| Merkmal | Pfefferminz (Altversicherer) | Minzia (KI-Start-up) | Pfefferminzia (fusioniert) |
|---|---|---|---|
| Gründung | 1924 als „Pfefferminz Versicherungs-Genossenschaft" in Olten (SO) – Haftpflicht- und Sterbekasse für Gewerbetreibende; 1961 Lebensversicherung; 1998 Umwandlung in AG; 2006 Markteintritt Deutschland | 2019 in Berlin als „Minzia Technologies GmbH" – Gründerteam aus Aktuarin, ML-Ingenieur und Ex-Schadensachbearbeiter; Produkt: KI-gestützte Risikoprüfung und Schadenautomatisierung als SaaS für Versicherer, ab 2021 eigener digitaler Haftpflicht-Direktvertrieb unter der App „minzia.direct" (als Assekuradeur, d.h. ohne eigene Risikoträgerschaft) | Closing 01.01.2025; Marke „Pfefferminzia" seit 01.01.2025 |
| Rechtsform / Struktur | Pfefferminz Holding AG (CH) mit Pfefferminz Versicherung AG (Schaden/Haftpflicht) und Pfefferminz Leben AG | GmbH, Series-B-finanziert (zwei fiktive VC-Fonds) | **Pfefferminzia Holding AG**, Olten (CH), FINMA-Gruppenaufsicht; Töchter siehe 1.2 |
| Sitz / Standorte | Hauptsitz Olten; Regionaldirektionen Bern, Zürich, St. Gallen, Lausanne (Romandie – im Datensatz nur erwähnt, nicht ausgearbeitet); Deutschland-Niederlassung Leipzig (seit 2006) | Berlin (Hauptsitz), kleines Team in Zürich (2022) | Konzernsitz Olten; Deutschland-Hub Leipzig; Tech-Hub Berlin; siehe 1.4 |
| Bruttoprämien (GJ 2025) | CHF 1'640 Mio. | Vermittelte Prämien EUR 38 Mio. (kein eigenes Risiko) | **CHF 2'060 Mio.** (Details 1.3) |
| Mitarbeitende (FTE, 30.06.2026) | 2'150 | 185 (davon 120 Tech/Data) | **2'410** (nach Abgängen, Doppelfunktionen, Neueinstellungen) |
| Kundinnen/Kunden | 1,25 Mio. Verträge, ca. 980'000 Kundenbeziehungen | 62'000 Nutzerkonten, 41'000 aktive Policen | **ca. 1,05 Mio. Kundenbeziehungen**, 1,36 Mio. Verträge |
| Marktposition (fiktiv) | „Nummer 7–9" im Schweizer Haftpflichtmarkt, „Nummer 6" bei Risikoleben CH; in DE Nischenanbieter (Rang >25) | Insurtech mit hohem Bekanntheitsgrad bei Unter-35-Jährigen in DE | Mittelgrosser, überregional tätiger Versicherer – bewusst *nicht* Top-3 |
| Rating (fiktiv) | „A-" einer fiktiven Ratingagentur „Nordstern Rating" | – | „A-", Ausblick stabil |

### 1.2 Gruppenstruktur und Aufsicht (regulatorisch plausibel)

| Gesellschaft | Sitz | Geschäft | Aufsicht | Bemerkung / Lehrwert |
|---|---|---|---|---|
| Pfefferminzia Holding AG | Olten CH | Konzernholding | FINMA (Gruppenaufsicht, Art. 64 ff. VAG CH) | Verwaltungsrat, Konzernfunktionen |
| Pfefferminzia Versicherung AG | Olten CH | Schadenversicherer: Privat- und Betriebshaftpflicht CH | FINMA (VAG CH, SST) | Führt die **Niederlassung Deutschland (Leipzig)** für Haftpflicht auf Basis des Direktversicherungsabkommens CH–EU (Schadenversicherung); BaFin beaufsichtigt die Niederlassung (§§ 61 ff. VAG DE), „Hauptbevollmächtigte/r" als Rolle |
| Pfefferminzia Leben AG | Olten CH | Risiko-, Kapital-, Rentenversicherung CH (Säule 3a/3b) | FINMA (SST, gebundenes Vermögen, verantwortlicher Aktuar) | Tarifierung teilweise geschlechtsabhängig (CH zulässig) – bewusster Kontrast zu DE (Unisex) |
| Pfefferminzia Lebensversicherung Deutschland AG | Leipzig DE | Risiko-, Kapital-, Rentenversicherung DE | BaFin (VAG DE / Solvency II, SFCR, ORSA) | Eigene deutsche Tochter, weil das CH–EU-Abkommen Lebensversicherung nicht abdeckt – wichtiger Lernpunkt „warum zwei Aufsichtsregime" |
| Minzia Technologies GmbH | Berlin DE | Konzerninterne IT-/KI-Dienstleisterin, Betreiberin der Plattform „MINT", Assekuradeur-Lizenz ruhend seit 2025 | Keine Versicherungsaufsicht, aber **gruppeninternes Outsourcing** (FINMA-RS 2018/3; § 32 VAG DE; DORA für DE-Tochter) | Träger der Outsourcing-, Datenschutz- und KI-Governance-Fallstudien |
| Pfefferminzia Service AG | Olten CH | Shared Services (HR, Finanzen, Einkauf) | – | Kostenumlage, intra-group SLA |

### 1.3 Prämien- und Bestandsmix (GJ 2025, Masterdatei-Basis)

| Segment | Markt | Bruttoprämien | Verträge | Combined Ratio / Marge | Vertriebsmix |
|---|---|---|---|---|---|
| Privathaftpflicht | CH | CHF 210 Mio. | 520'000 | CR 91 % | Agenturen 45 %, Makler 10 %, Direkt/Online 35 %, Bank 10 % |
| Betriebshaftpflicht (KMU) | CH | CHF 190 Mio. | 68'000 | CR 96 % | Makler 55 %, Agenturen 40 %, Direkt 5 % |
| Privathaftpflicht | DE | EUR 165 Mio. | 410'000 | CR 94 % | Direkt/Online 55 % (Minzia-Erbe), Makler 30 %, Bank 15 % |
| Betriebshaftpflicht | DE | EUR 120 Mio. | 39'000 | CR 99 % | Makler 75 %, Direkt 25 % |
| Risikoleben | CH | CHF 240 Mio. | 145'000 | Neugeschäftsmarge 3,1 % | Agenturen 50 %, Makler 25 %, Bank 20 %, Direkt 5 % |
| Kapital-/Rentenversicherung (3a/3b) | CH | CHF 690 Mio. | 118'000 | Neugeschäftsmarge 1,8 % | Agenturen 55 %, Bank 30 %, Makler 15 % |
| Risikoleben | DE | EUR 95 Mio. | 72'000 | Neugeschäftsmarge 2,4 % | Makler 50 %, Direkt 35 %, Bank 15 % |
| Kapital-/Rentenversicherung (Basis-/Privatrente) | DE | EUR 310 Mio. | 63'000 | Neugeschäftsmarge 1,1 % | Makler 60 %, Bank 35 %, Direkt 5 % |

Hinweis: Umrechnung im Datensatz mit fixem Planungskurs 1 EUR = 0,94 CHF (Planungsannahme, in der Masterdatei dokumentieren).

### 1.4 Standorte

| Standort | Funktion | Mitarbeitende | Herkunft | Kultur-Marker im Datensatz |
|---|---|---|---|---|
| Olten (CH) – „Haus Aarequai" (fiktive Adresse: Aarequai 12, 4600 Olten) | Konzernsitz, GL, Aktuariat, Underwriting Leben CH, Schaden CH, Compliance, Risk, IT-Betrieb Altsysteme | 1'050 | Pfefferminz | Hierarchisch, Präsenzkultur, „Olten-Zeit" für Sitzungen |
| Leipzig (DE) – „Minzhof" (fiktiv: Kohlrabizirkus-Str. 7, 04103 Leipzig) | Deutschland-Hub: Niederlassung Haftpflicht, Leben-Tochter, Kundenservice DE, Vertriebsleitung DE | 620 | Pfefferminz (seit 2006) | Vermittelnd zwischen den Welten, sieht sich als „Brücke" |
| Berlin (DE) – „Werkstatt" (fiktiv: Mariendorfer Damm 300, 12107 Berlin) | Data & AI Office, MINT-Plattform, Direktvertrieb/Online, Produktdesign digital | 260 | Minzia | Remote-first, Slack, Englisch/Deutsch gemischt, kein Dresscode |
| Zürich (CH) | Regionaldirektion, Makler-Desk, kleines Data-Science-Team (ex-Minzia CH) | 190 | gemischt | Erster Ort, wo beide Kulturen physisch zusammensitzen |
| Bern, St. Gallen (CH) | Regionaldirektionen, Agenturbetreuung | je ca. 80 | Pfefferminz | Vertriebsnah |
| Lausanne (CH) | Regionaldirektion Romandie – **nur erwähnt** | 60 | Pfefferminz | Hinweis auf Mehrsprachigkeit (nicht ausgearbeitet) |
| Agenturnetz | 96 Ausschliesslichkeitsagenturen CH, 38 in DE (selbständige Handelsvertreter) | ca. 900 externe Personen | Pfefferminz | Skeptisch gegenüber Direktvertrieb aus Berlin |

### 1.5 Vertriebswege

| Kanal | CH | DE | Konflikte / Storylines |
|---|---|---|---|
| Ausschliesslichkeitsagenturen (gebundene Vermittler) | 96 Agenturen, Kernkanal Leben; FINMA-Registrierung als gebundene Vermittler | 38 Agenturen (Handelsvertreter § 84 HGB, IHK-Register § 34d GewO) | Angst vor Kannibalisierung durch Online; Provisionsdiskussion |
| Makler / Broker | ca. 400 aktive Makler, Makler-Desk Zürich; Broker-Portal „PfeffMakler" (Altsystem-Anbindung) | ca. 1'200 Makler, Pool-Anbindungen; § 60 ff. VVG DE | Makler fordern API-Anbindung – MINT liefert, Altsystem bremst |
| Direkt/Online | Website + App (ehemals minzia.direct, jetzt „Pfefferminzia App") | Kernkanal Haftpflicht DE | Chatbot-Use-Cases, dunkle Muster vermeiden (Compliance) |
| Bancassurance | Kooperation mit fiktiver „Aare-Bank AG" (Regionalbank) | Kooperation mit fiktiver „Sächsische Genossenschaftskasse eG" | Datenteilung/Datenschutz, Beratungsdokumentation durch Bankberater |
| Firmenkunden-Desk | Betriebshaftpflicht KMU über Verbände (fiktiver „Gewerbeverband Mittelland") | Über Makler-Pools | Zeichnungskompetenzen (Kompetenzordnung) |

### 1.6 Organigramm (Gruppe, Stand 30.06.2026)

**Verwaltungsrat (Holding, CH):** 7 Mitglieder; Präsidentin (ex-Pfefferminz, Juristin), Vizepräsident (Minzia-Mitgründer, Vertreter der Alt-Investoren), Ausschüsse: Audit & Risk, Nomination & Compensation, **Technology & AI Committee** (neu 2025). Die DE-Tochter Leben hat einen eigenen **Aufsichtsrat** (3 Mitglieder), die DE-Niederlassung eine/n **Hauptbevollmächtigte/n**.

**Geschäftsleitung (Group Executive Board):**

| Rolle | Herkunft | Verantwortung | Bemerkung |
|---|---|---|---|
| CEO | Pfefferminz (seit 2021) | Gesamtleitung, Strategie 2030 | Treiber des Mergers, „Brückenbauer"-Rhetorik |
| CFO | Pfefferminz | Finanzen, Rechnungslegung, Kapitalanlagen, Investor Relations | Skeptisch bzgl. KI-ROI |
| CRO | extern (2024 rekrutiert) | Risikomanagement, SST/Solvency II, ORSA, Modellrisiko | Neutral, verlangt Nachweise |
| COO | Pfefferminz | Betrieb Schaden/Leistung, Kundenservice, Prozesse | Prozesshandbuch-Owner |
| Chief Underwriting Officer | Pfefferminz | Underwriting Haftpflicht und Leben, Aktuariat Tarifierung | Owner der Zeichnungsrichtlinien (mit Sparten-AP abstimmen) |
| Chief Sales Officer | Pfefferminz (DE-Vertriebschef) | Alle Vertriebswege CH/DE | Agenturlobby |
| **Chief Data & AI Officer (CDAO)** | Minzia (Mitgründerin) | Data & AI Office, MINT-Plattform, Datenplattform, KI-Governance operativ | Zentrale Figur der Use Cases |
| CIO | Pfefferminz | IT-Betrieb, Altsysteme, Informationssicherheit, Migration | Spannungsfeld zu CDAO |
| General Counsel & Chief Compliance Officer | Pfefferminz | Legal, Compliance, Datenschutz (fachlich), Geldwäscherei-Fachstelle | Owner Compliance-Handbuch |
| Chief People Officer | extern (2025) | HR, Kultur, Integration | Owner Kulturumfrage |

**Abteilungen (2. Ebene) und Schlüsselfunktionen:**

| Bereich | Einheiten | Rollen (Auswahl) | Regulatorischer Anker |
|---|---|---|---|
| Risikomanagement | Risk Controlling, Modellvalidierung, ORSA/SST-Team, **Modellrisiko & KI-Validierung** (neu) | Head Risk, Modellvalidator/in | Schlüsselfunktion (Art. 22 VAG CH; § 26 VAG DE) |
| Compliance | Regulatory Compliance, Geldwäscherei-Fachstelle, Beschwerdestelle, **AI Compliance Officer** (neu) | Compliance Officer CH, Compliance Officer DE | Schlüsselfunktion (§ 29 VAG DE; FINMA-RS 2017/2) |
| Interne Revision | Gruppenrevision inkl. IT-Audit | Leiter/in IR, berichtet an VR-Audit-Committee | Schlüsselfunktion |
| Aktuariat | Verantwortlicher Aktuar CH (Art. 23 VAG CH), Versicherungsmathematische Funktion DE (§ 31 VAG DE), Reservierung, Tarifierung | Chefaktuar/in Leben, Aktuar/in Nichtleben | Schlüsselfunktion |
| Datenschutz | Datenschutzbeauftragte/r Gruppe (CH: Datenschutzberater/in nach Art. 10 DSG), Datenschutzbeauftragte/r DE (Art. 37 DSGVO, § 38 BDSG) | DSB CH, DSB DE | DSG / DSGVO |
| **Data & AI Office** (Minzia) | Data Science, ML Engineering, MLOps/Plattform, Data Governance & Datenqualität, **AI Governance & Ethics**, Data Product Owner je Sparte | Head of AI Governance, ML Lead Leben, ML Lead Haftpflicht, Data Steward Bestand, Prompt-/LLM-Engineer | KI-Governance-Richtlinie, EU AI Act (DE), FINMA-Aufsichtsmitteilung 08/2024 (CH) |
| IT (CIO) | Betrieb Altsysteme, Infrastruktur/Cloud, Informationssicherheit (CISO), Migration Office | CISO, Leiter/in Bestandsführung IT | ISMS, DORA (DE), FINMA-Cyber-Meldepflicht |
| Schaden/Leistung (COO) | Schaden Haftpflicht CH/DE, Leistungsprüfung Leben CH/DE, Betrugsabwehr (Special Investigation Unit), Regress | Schadenleiter/in, Leistungsprüfer/in, Betrugsermittler/in | Prozesshandbuch |
| Underwriting (CUO) | Risikoprüfung Leben (medizinisch), Underwriting Betriebshaftpflicht, Produktmanagement | Senior Underwriter, medizinischer Berater (Vertragsarzt) | Zeichnungsrichtlinien (Sparten-AP) |
| Vertrieb (CSO) | Agenturvertrieb CH, Agenturvertrieb DE, Maklerservice, Direkt/Online, Bancassurance | Agenturleiter/in, Maklerbetreuer/in | Vermittlerrecht |
| Kundenservice | Contact Center Olten und Leipzig, Bestandsverwaltung, Beschwerdebearbeitung 1st Level | Teamleiter/in Service | Beschwerderichtlinie |
| Finanzen (CFO) | Rechnungslegung, Controlling, Kapitalanlage, Steuern (Stempelabgabe/VersSt), Reporting | Controller/in | Meldewesen |
| Legal | Vertragsrecht, Vermittlerverträge, Litigation, Ombudsfälle | Syndikus | – |
| HR & Kultur (CPO) | HR CH, HR DE, Integrationsbüro, Lernen & Entwicklung | Integration Lead | Kulturumfrage |
| Kommunikation | Interne Kommunikation, Presse, Marketing | Pressesprecher/in | Pressemitteilungen, Newsletter |

### 1.7 IT-Landschaft (Altsystem vs. Neusystem)

| System (fiktiver Name) | Herkunft | Technologie / Alter | Funktion | Rolle in Use Cases |
|---|---|---|---|---|
| **VERA** (Versicherungs-Rechnungs-Anwendung) | Pfefferminz, 1994 | Host-basierte Bestandsführung (COBOL, relationale Host-DB), Batch nächtlich | Bestand Leben CH und DE (getrennte Mandanten), Prämienrechnung, Inkasso | Datenqualität, Legacy-Extraktion, Doku-Lücken (Wissen in Köpfen) |
| **SILAS** (Schaden-Informations- und Leistungs-Abwicklungs-System) | Pfefferminz, 2004 | Java-Client/Server, eigene Workflow-Engine | Schaden Haftpflicht CH/DE, Leistungsfälle Leben | Schadenautomatisierung, Betrugserkennung, Dokumentenklassifikation |
| **PfeffMakler** | Pfefferminz, 2011 | Web-Portal, Anbindung über nächtliche Schnittstellen | Makler-/Agenturportal | API-Modernisierung |
| **DOKU-Archiv** | Pfefferminz, 2008 | Dokumentenmanagement, gescannte Post (TIFF/PDF), OCR unvollständig | Alle Korrespondenz | RAG-Quelle, OCR-Qualität als Realitätsfaktor |
| **MINT** (Minzia Intelligence & Technology Platform) | Minzia, 2020 | Cloud-native (Container, Event-Streaming), Microservices, Feature Store, Modell-Registry, LLM-Gateway | Digitale Antragsstrecke Haftpflicht, KI-Risikoprüfung, Schaden-Triage, Chat-Assistent | Neusystem, alle produktiven KI-Modelle |
| **Herbarium** (Datenplattform) | gemischt, 2025 | Lakehouse, tägliche Replikation aus VERA/SILAS, Data Catalog, Datenqualitätsregeln | Analytische Daten, Reporting, Modelltraining | Datenarchitektur-AP: Single Source für Analytics |
| **KOMPASS** | Pfefferminz, 2016 | Standard-Finanz-/Reporting-Suite (fiktiv) | Rechnungslegung, Solvenz-Reporting | Meldewesen |
| Kollaboration | zwei Welten: E-Mail/Sitzungsprotokolle (Olten) vs. Chat/Wiki (Berlin) | – | – | Kulturunterschied, Wissensfragmentierung |

Migrationsstand 30.06.2026: Haftpflicht DE Neugeschäft läuft vollständig auf MINT; Haftpflicht CH Neugeschäft zu 60 % auf MINT; Leben-Bestand komplett auf VERA („Migration Leben" ist Roadmap-Meilenstein 2027/28). Zwei Kundennummernkreise (VERA 8-stellig, MINT UUID) mit Mapping-Tabelle – bewusst als Datenqualitätsproblem angelegt.

---

## 2. Merger-Narrativ als Dokumente

### 2.1 Storyline (Kurzfassung für alle Autorinnen und Autoren)

1. **2019–2022:** Minzia wächst als KI-SaaS und Assekuradeur, gewinnt Pfefferminz 2021 als Pilotkunden für Schaden-Triage.
2. **2023:** Pfefferminz übernimmt 30 % an Minzia; Minzias Investoren wollen Exit. Pfefferminz steht unter Kostendruck (CR Betriebshaftpflicht DE >100 %, Storno Leben steigt).
3. **05/2024:** Signing „Zusammenschluss" – formal eine Übernahme durch Pfefferminz (Aktientausch + Cash), kommunikativ als „Merger of Equals" verkauft. Neue Marke Pfefferminzia.
4. **01.01.2025:** Closing. CDAO tritt in die GL ein. Technology & AI Committee im VR.
5. **2025:** Integrations-Roadmap „Wurzeln & Flügel"; erste Reibungen: Agenturen vs. Direktvertrieb, CIO vs. CDAO, Datenschutz-Vorfall bei Testdaten-Nutzung, FINMA-Rückfrage zu KI-Governance.
6. **H1 2026:** Erste produktive KI-Use-Cases mit messbarem Effekt; Kulturumfrage zeigt Spaltung; Strategie 2030 verabschiedet; Beschwerdefall wegen automatisierter Ablehnung; Betrugsfall aufgedeckt durch Modell.
7. **Offene Konflikte (für Kursteilnehmende zum Bearbeiten):** Migration Leben, EU-AI-Act-Einstufung der Risikoprüfung Leben, Outsourcing-Setup Minzia Technologies, Rollenklärung CIO/CDAO, Provisionsmodell.

### 2.2 Dokumentenliste

| # | Dokument | Zweck im Datensatz | Länge | Ton | Absender | Locale | Vertraulichkeit |
|---|---|---|---|---|---|---|---|
| M01 | Unternehmensgeschichte „100 Jahre Pfefferminz – und ein Neuanfang" | Grundwissen, RAG-Quelle für „Wer sind wir"-Fragen, Zeitleiste | 4–6 Seiten | Erzählend, leicht nostalgisch | Kommunikation | de-CH | öffentlich |
| M02 | Zusammenfassung Fusionsvertrag (Term Sheet für interne Verwendung) | Struktur der Transaktion, Governance-Zusagen (Sitz CDAO in GL, Standortgarantie Berlin bis 2028, Earn-out an Minzia-Gründer bei KI-KPIs) | 3 Seiten, Tabellen | Juristisch-nüchtern | General Counsel | de-CH | vertraulich |
| M03 | Strategie 2030 „Wurzeln & Flügel" | Ziele: CR <93 %, 40 % Neugeschäft digital, 30 % Prozessautomatisierung, KI-Governance als Wettbewerbsvorteil; Leitplanken | 12–15 Seiten inkl. KPI-Baum | Visionär, aber mit Zahlen | CEO/GL | de-CH | intern |
| M04 | VR-Protokolle (6 Stück: 03/2024, 09/2024, 12/2024, 03/2025, 09/2025, 03/2026) | Entscheidungswege, Konflikte, Beschlüsse zu KI-Investitionen, FINMA-Rückfrage, Genehmigung KI-Richtlinie | je 3–5 Seiten | Formell, Beschlussformat | VR-Sekretariat | de-CH | streng vertraulich |
| M05 | GL-Protokolle (8 Stück, monatlich ausgewählt 2025/26) | Operative Konflikte (Migration, Provision, Datenschutz-Vorfall) | je 2–3 Seiten | Formell, Traktandenliste | GL-Assistenz | de-CH | vertraulich |
| M06 | Interne Memos (12–15 Stück) | z. B. CIO an GL „Risiken Parallelbetrieb VERA/MINT"; CDAO an GL „Modellinventar"; CRO „Modellrisiko KI"; DSB „Testdaten-Vorfall"; CSO „Provisionsmodell Direktkanal"; Compliance „EU AI Act Betroffenheitsanalyse" | je 1–3 Seiten | Sachlich bis pointiert; Berliner Memos informeller | verschiedene | gemischt | intern/vertraulich |
| M07 | Mitarbeiter-Newsletter „Minzblatt" (10 Ausgaben, quartalsweise + Sonderausgaben) | Integrationskommunikation, Erfolge, Personalien, FAQ | je 2–3 Seiten | Warm, motivierend, teils beschönigend | Interne Kommunikation | de-CH mit DE-Rubrik | intern |
| M08 | Pressemitteilungen (8 Stück: Beteiligung 2023, Signing, Closing/neue Marke, Geschäftszahlen 2024 und 2025, neue CDAO, Launch KI-Schadenassistent, Rating bestätigt) | Öffentliches Narrativ vs. interne Realität | je 1–2 Seiten | PR-Sprache | Pressestelle | de-CH und de-DE (Doppelfassung) | öffentlich |
| M09 | Integrations-Roadmap 2025–2028 | Workstreams (Marke, Vertrieb, IT-Migration, Daten, Kultur, Regulatorik), Meilensteine, Ampelstatus | 8 Seiten + Gantt-Tabelle | Projektsprache | Integration Office (CPO/COO) | de-CH | intern |
| M10 | KPI-Dashboards (Monatsdaten 01/2024–06/2026 als CSV + 4 Screenshots/Beschreibungen) | Analytics-Use-Cases: CR, Storno, NPS, Bearbeitungszeit, Automatisierungsquote, Beschwerdequote, Modell-KPIs | Tabellen | – | Controlling / Data & AI Office | – | intern |
| M11 | Kulturumfrage 2025 (Ergebnisbericht + Rohdaten anonymisiert, n = 1'830) | Spaltung sichtbar: Vertrauen in KI, Zugehörigkeit, Führung; Freitextkommentare (200 Stück) für NLP-Use-Cases | 10 Seiten + CSV | Neutral-analytisch, Freitexte emotional | CPO / externes Institut (fiktiv) | gemischt | intern |
| M12 | Organigramme (Stand 01/2025 und 06/2026) | Veränderung sichtbar machen | je 1 Seite | – | HR | – | intern |
| M13 | Onboarding-Guide „Willkommen bei Pfefferminzia" | Glossar CH/DE, Systemlandschaft, Ansprechpersonen – ideale RAG-Grundlage | 8 Seiten | Freundlich | HR | de-CH | intern |
| M14 | Town-Hall-Transkript (2 Stück) inkl. Q&A | Ungefilterte Mitarbeiterfragen, Zusammenfassungs-Use-Case | je 6–8 Seiten | Gesprochene Sprache | CEO/CDAO | gemischt | intern |
| M15 | Aktionärsbrief / Geschäftsbericht-Vorwort 2025 | Öffentliche Zahlen konsistent mit Masterdatei | 2 Seiten | Formell | VR-Präsidentin/CEO | de-CH | öffentlich |

Empfehlung: Widersprüche **gezielt** einbauen (z. B. Pressemitteilung „Merger of Equals" vs. Fusionsvertrag „Übernahme", Newsletter-Optimismus vs. Kulturumfrage) und in einer internen Autorendatei (`redaktions-notizen.md`, nicht Teil des Lehrdatensatzes) dokumentieren, damit sie in Use Cases („Finde Inkonsistenzen") auswertbar sind.

---

## 3. Übergreifende Regelwerke (nicht spartenspezifisch)

Für jedes Regelwerk: Gliederung, Umfang, Rolle für KI-Use-Cases. Alle Regelwerke sind Gruppenrichtlinien mit CH/DE-Anhängen, verabschiedet durch GL, KI- und Compliance-Richtlinien zusätzlich vom VR genehmigt. Versionierung: v1.0 Pfefferminz (alt, 2019–2022), v2.0 Pfefferminzia (2025), teils v2.1 (2026) – alte Versionen bewusst mitliefern für Versionsvergleich-Use-Cases.

### 3.1 Übersicht

| # | Regelwerk | Owner | Umfang | Versionen im Datensatz | Primäre Use-Case-Rolle |
|---|---|---|---|---|---|
| R01 | Compliance-Handbuch | GC/CCO | 35–45 Seiten | v1.0 (2021, Pfefferminz), v2.0 (2025) | RAG-Quelle, Compliance-Check-Referenz, Onboarding-Quiz |
| R02 | Datenschutzrichtlinie (DSG CH / DSGVO DE) | DSB | 25–30 Seiten + Anhänge | v2.0 (2025), v2.1 (2026 nach Vorfall) | Compliance-Check für KI-Use-Cases, DSFA-Templates, Klassifikation von Anfragen |
| R03 | KI-Governance-Richtlinie | CDAO + CRO + CCO | 30–40 Seiten + Modellinventar | v0.9 Minzia „AI Principles" (2022, EN), v1.0 (2025), v1.1 (2026) | Kernreferenz aller KI-Use-Cases; Risikoklassifizierung; Freigabe-Workflow |
| R04 | Geldwäscherei-/AML-Richtlinie Leben | Geldwäscherei-Fachstelle | 20–25 Seiten | v2.0 (2025) | KYC-Automatisierung, Transaktionsmonitoring, Verdachtsmeldung |
| R05 | Beschwerdemanagement-Richtlinie | Compliance (Beschwerdestelle) | 12–15 Seiten | v2.0 (2025) | Beschwerde-Klassifikation, Antwortgenerierung, Fristenüberwachung |
| R06 | Outsourcing-Richtlinie | CRO + CIO | 18–22 Seiten + Outsourcing-Register | v2.0 (2025) | Bewertung von Cloud-/LLM-Anbietern, gruppeninternes Outsourcing Minzia Tech |
| R07 | Informationssicherheitsrichtlinie (ISMS) | CISO | 25–30 Seiten + 8 Unterrichtlinien | v2.0 (2025) | Prompt-Injection-/Datenabfluss-Checks, Berechtigungen für KI-Tools |
| R08 | Vollmachts- und Kompetenzordnung | GC + CFO | 15 Seiten, überwiegend Tabellen | v2.0 (2025) | Entscheidungs-Use-Cases: „Darf X das freigeben?", Human-in-the-loop-Schwellen |
| R09 | Verhaltenskodex (Code of Conduct) | CEO/CPO | 10–12 Seiten | v1.0 (2018), v2.0 (2025) | Ton-/Werte-Referenz für generierte Texte; Ethik-Checks |
| R10 | Prozesshandbuch mit Prozesslandkarte | COO | 40–60 Seiten + Prozessdiagramme (BPMN-Text) | v2.0 (2025), Teilprozesse v2.1 | Process-Mining, Automatisierungspotenzial, Agenten-Workflows |
| R11 | Richtlinie Nutzung generativer KI am Arbeitsplatz (Kurzrichtlinie) | CDAO/CISO | 4 Seiten | v1.0 (2025) | Realistischer Alltagsbezug, Schulungs-Use-Case |
| R12 | Interessenkonflikt- und Geschenkerichtlinie | Compliance | 6 Seiten | v2.0 | Nebenrolle (Vertrieb/Makler) |
| R13 | Richtlinie Produktfreigabe (POG – Product Oversight & Governance) | CUO + Compliance | 10 Seiten | v2.0 | Verbindung zu Sparten-AP; Zielmarkt-Prüfung, KI-Produktfeatures |

### 3.2 R01 Compliance-Handbuch

| Kapitel | Inhalt | Bemerkung |
|---|---|---|
| 1 Zweck, Geltungsbereich, Rollen | Gruppe, CH-Gesellschaften, DE-Tochter, DE-Niederlassung; Compliance-Funktion als Schlüsselfunktion | Three-Lines-Modell |
| 2 Regulatorisches Umfeld | Übersichtstabelle FINMA/BaFin, VAG CH/DE, VVG CH/DE, Vermittlerrecht, DSG/DSGVO, GwG, EU AI Act, DORA (nur DE) | Verweis auf Referenzdokument Kap. 4 |
| 3 Compliance-Risikoanalyse | Jährlich, Methodik, Risikoregister (Auszug) | Tabelle mit 20 Risiken inkl. „KI-Diskriminierung", „automatisierte Einzelentscheidung" |
| 4 Verhaltensregeln | Verweis auf Kodex, Interessenkonflikte, Geschenke, Insiderinformation (Kapitalanlagen) | |
| 5 Kundenschutz | Informations-/Beratungspflichten CH vs. DE, Fair Treatment, Vulnerable Customers, Zielmarkt (POG) | Wichtig für Chatbot-Use-Cases |
| 6 Vermittleraufsicht | Registrierung, Aus-/Weiterbildung, Provisionsoffenlegung (CH Art. 45b VAG), Provisionsdeckel Leben DE | |
| 7 Datenschutz, Geldwäscherei, Sanktionen | Kurzverweise auf R02, R04, Sanktionsscreening | |
| 8 Regulatorische Meldungen und Kontakt mit Aufsicht | Meldepflichten, Ansprechpersonen, Umgang mit Anfragen | Enthält Musterprozess „FINMA-Anfrage zu KI" |
| 9 Whistleblowing | Meldekanal, Schutz | |
| 10 Schulung, Überwachung, Reporting | Compliance-Jahresbericht, Kontrollplan | |
| Anhänge | Kontrollmatrix, Fristenkalender, Glossar CH/DE | Glossar ist RAG-Gold |

### 3.3 R02 Datenschutzrichtlinie

| Kapitel | Inhalt | KI-Bezug |
|---|---|---|
| 1 Grundsätze | Rechtmässigkeit, Zweckbindung, Datenminimierung, Transparenz; CH: DSG (rev. 2023), DE: DSGVO + BDSG | – |
| 2 Rollen | Verantwortliche je Gesellschaft, DSB DE (Pflicht), Datenschutzberater CH (freiwillig, benannt), Auftragsbearbeiter (Minzia Technologies!) | Gruppeninterne Auftragsverarbeitung als Fallstudie |
| 3 Datenkategorien | Besonders schützenswerte Daten: Gesundheitsdaten (Leben-Risikoprüfung, Leistungsfälle), genetische Daten (CH GUMG / DE GenDG – Verbotsschwellen), Betreibungs-/Bonitätsdaten, biometrische Daten (App-Login) | Trainingsdaten-Restriktionen |
| 4 Rechtsgrundlagen je Verarbeitung | Tabelle: Antrag, Underwriting, Schaden, Marketing, Profiling, Betrugsbekämpfung, Modelltraining | Kernreferenz für „Darf das Modell diese Daten nutzen?" |
| 5 Automatisierte Einzelentscheidungen | CH Art. 21 DSG (Informations-/Anhörungspflicht), DE Art. 22 DSGVO (Verbot mit Ausnahmen, § 37 BDSG Versicherungs-Ausnahme bei Leistungserbringung) | Human-in-the-loop-Regeln, direkt in KI-Use-Cases anwendbar |
| 6 Betroffenenrechte | Auskunft, Berichtigung, Löschung, Widerspruch; Fristen (DE 1 Monat, CH 30 Tage) | Use Case: Auskunftsersuchen automatisiert beantworten |
| 7 Datenschutz-Folgenabschätzung | Wann Pflicht; Template; Liste durchgeführter DSFA (inkl. „KI-Risikoprüfung Leben", „Schaden-Triage") | DSFA-Generierungs-Use-Case |
| 8 Datentransfer | CH↔DE-Datenflüsse (Angemessenheit beidseitig), Cloud-Anbieter, LLM-APIs ausserhalb EU/CH | Vendor-Check |
| 9 Aufbewahrung und Löschung | Fristen-Tabelle (10 Jahre Buchhaltung, Verjährung, Leben bis Vertragsende + 10) | Datenarchitektur-AP |
| 10 Vorfälle | Meldung: CH an EDÖB „so rasch als möglich", DE 72 Stunden an Aufsichtsbehörde; interner Prozess | Vorfall „Testdaten 2025" als Fallbeispiel |
| Anhänge | Verarbeitungsverzeichnis (Auszug, 25 Einträge), Informationstexte CH/DE, DSFA-Vorlage, AVV-Muster gruppenintern | |

### 3.4 R03 KI-Governance-Richtlinie

| Kapitel | Inhalt | Bemerkung |
|---|---|---|
| 1 Zweck und Prinzipien | Verantwortung, Transparenz, Fairness, Robustheit, menschliche Aufsicht, Datenschutz-by-Design; Herkunft: Minzia „AI Principles" 2022 (EN, Start-up-Ton) → formalisiert 2025 | Alte Version als Kontrast beilegen |
| 2 Geltungsbereich und Definitionen | KI-System (Definition angelehnt an EU AI Act Art. 3), Modell, Agent, generative KI, Schatten-KI | Glossar |
| 3 Governance-Struktur | VR Technology & AI Committee; GL; **AI Governance Board** (CDAO Vorsitz, CRO, CCO, DSB, CUO, Vertreter Schaden, Ethik-Beisitz); Model Owner, Model Validator (Risk), AI Compliance Officer; Three Lines | RACI-Tabelle |
| 4 Risikoklassifizierung | Vierstufig intern (Gruppe): **Klasse A verboten**, **Klasse B hoch** (Deckungsgleich mit EU AI Act Anhang III inkl. Nr. 5 lit. c „Risikobewertung und Preisbildung bei Lebens-/Krankenversicherung natürlicher Personen"; ebenso Bonitätsprüfung, Personalentscheidungen), **Klasse C begrenzt** (Chatbots, Transparenzpflichten), **Klasse D minimal**. CH: kein AI Act, aber gleiche interne Klassifizierung; FINMA-Aufsichtsmitteilung 08/2024 (Governance, Inventar, Datenqualität, Tests, Erklärbarkeit) als Anker | Diskussionspunkt: Haftpflicht-Pricing ist nicht Anhang III, Leben-Risikoprüfung schon; Betrugserkennung Grenzfall; Zeitplan AI Act Hochrisiko (ursprünglich 08/2026, Verschiebung im Digital-Omnibus-Verfahren – Datum im Datensatz als Variable führen) |
| 5 Lebenszyklus | Idee → Use-Case-Antrag → Risikoklassifizierung → Datenfreigabe (DSB) → Entwicklung → Validierung (Risk) → Freigabe (Board je Klasse) → Betrieb/Monitoring → Re-Validierung → Abschaltung | Formulare als Anhänge; Use Case: „Antrag automatisch vorprüfen" |
| 6 Anforderungen je Klasse | Dokumentation (Model Card), Datenqualität, Bias-Tests (Merkmale: Geschlecht, Alter, Nationalität, Wohnort/PLZ als Proxy), Erklärbarkeit, Human Oversight, Logging, Robustheit, Fallback | Tabelle |
| 7 Generative KI und Agenten | Erlaubte Tools, Prompt-Standards, Halluzinationskontrolle, Kundenkontakt nur mit Kennzeichnung, keine Verbindlichkeitserklärungen durch KI, Vier-Augen bei Ablehnungen | Verknüpft mit R11 |
| 8 Drittanbieter und Outsourcing | Modelle/APIs Dritter; Verknüpfung R06; DORA-IKT-Drittparteienregister (DE) | |
| 9 Vorfälle und Beschwerden | KI-Vorfallmeldung, Kundenbeschwerden über KI-Entscheide (Verknüpfung R05), Meldung an Aufsicht | |
| 10 Schulung und Kultur | Pflichtschulung, AI Literacy (AI Act Art. 4) | |
| Anhang A Modellinventar | 18–25 Einträge: Name, Zweck, Sparte, Markt, Klasse, Owner, Status, letzte Validierung, Datenquellen, Aufsichtsrelevanz | **Zentrales Artefakt** für viele Use Cases |
| Anhang B Model-Card-Vorlage, C Bias-Testprotokoll, D Use-Case-Antragsformular | | |

### 3.5 R04 Geldwäscherei-/AML-Richtlinie Leben

| Kapitel | Inhalt | CH | DE |
|---|---|---|---|
| 1 Rechtsgrundlagen | – | GwG CH, GwV-FINMA, Reglement SRO-SVV (Selbstregulierung Versicherer), Lebensversicherer als Finanzintermediär | GwG DE, Lebensversicherer als Verpflichtete, BaFin-Auslegungs- und Anwendungshinweise, FIU |
| 2 Betroffene Produkte | Rückkaufsfähige Kapital-/Rentenversicherungen, Einmalprämien, Säule 3b; Risikoleben und 3a mit tiefem Risiko | Schwellenwerte je Land tabellarisch (im Datensatz als „Richtlinienwerte", nicht als Gesetzeszitate) | |
| 3 Kundenidentifikation und wirtschaftlich Berechtigte | Verfahren, Dokumente, Video-Ident, PEP-Prüfung, Sanktionslisten | Formular A (SRO-SVV-Logik) | Transparenzregister-Abgleich |
| 4 Risikoklassifizierung Kunden | Risikofaktoren, erhöhte Sorgfalt | | |
| 5 Transaktionsmonitoring | Regeln: Einmalprämien, Prämienzahler ≠ VN, frühe Rückkäufe, Drittstaaten-Zahlungen | Use Case: Regelwerk vs. ML-Scoring | |
| 6 Verdachtsmeldung | MROS (CH) vs. FIU (DE), Fristen, Tipping-off-Verbot | | |
| 7 Dokumentation, Schulung, Kontrollen | Aufbewahrung 10 Jahre | | |
| Anhang | Fallbeispiele (3), Eskalationsmatrix, Kunden-Persona „Einmalprämie aus Drittstaat" | | |

### 3.6 R05 Beschwerdemanagement-Richtlinie

| Kapitel | Inhalt | Bemerkung |
|---|---|---|
| 1 Definition Beschwerde | Weite Definition (jede Unzufriedenheitsäusserung), Abgrenzung Anfrage/Einwand | Klassifikations-Use-Case |
| 2 Grundlagen | DE: BaFin-Mindestanforderungen Beschwerdebearbeitung (Sammelverfügung/Rundschreiben), EIOPA-Leitlinien, Versicherungsombudsmann; CH: FINMA-Erwartung faires Beschwerdemanagement, Ombudsstelle Privatversicherung | |
| 3 Organisation | Beschwerdestelle zentral, 1st Level Service, Eskalation, Ombudsfälle Legal | |
| 4 Prozess und Fristen | Eingangsbestätigung 5 Arbeitstage, Antwort 15 Arbeitstage (interne Zielwerte), Verlängerung mit Zwischenbescheid | Fristenüberwachung |
| 5 Sonderfälle | Beschwerden über automatisierte Entscheidungen (Recht auf menschliche Überprüfung), Beschwerden über Vermittler, Datenschutzbeschwerden | KI-Anbindung R03 |
| 6 Root-Cause-Analyse und Reporting | Quartalsstatistik, Kategorien-Taxonomie (30 Kategorien), Meldung an BaFin (Beschwerdestatistik), Ursachenbehebung | Taxonomie als CSV |
| Anhänge | Textbausteine CH/DE (mit ß/ss-Unterschied), Eskalationsmatrix, Kategorien | Basis für Antwortgenerierung |

### 3.7 R06 Outsourcing-Richtlinie

| Kapitel | Inhalt | Bemerkung |
|---|---|---|
| 1 Grundlagen | CH: FINMA-RS 2018/3 Outsourcing (wesentliche Funktionen, Inventar, Zugriffsrechte FINMA); DE: § 32 VAG (wichtige Funktionen, Anzeigepflicht), MaGo, **DORA** (IKT-Drittparteienrisiko, Informationsregister) | Unterschiede sichtbar machen |
| 2 Wesentlichkeitsprüfung | Kriterien, Entscheidungsbaum | Use Case: Klassifizierung von Anbietern |
| 3 Gruppeninternes Outsourcing | Minzia Technologies als IT-/KI-Dienstleisterin für CH-Gesellschaften und DE-Tochter: Vertrag, SLA, Weisungsrecht, Prüfrechte | Fallstudie |
| 4 Due Diligence und Vertrag | Mindestinhalte (Prüfrechte, Datenstandort, Subunternehmer, Exit) | Cloud/LLM-API-Anbieter |
| 5 Laufende Überwachung | KPIs, Vorfälle, jährliche Neubewertung | |
| 6 Exit-Strategien | | |
| Anhang | Outsourcing-Register (20 Einträge: Rechenzentrum, Cloud, Druck/Versand, Schadenregulierer extern, LLM-API, Assistance-Dienstleister, Medizinischer Prüfdienst) | Register als CSV |

### 3.8 R07 Informationssicherheitsrichtlinie

| Kapitel / Unterrichtlinie | Inhalt | KI-Bezug |
|---|---|---|
| Leitlinie | Ziele, ISMS-Organisation, Klassifizierung (öffentlich/intern/vertraulich/streng vertraulich) | Klassifizierung steuert, was in Prompts darf |
| U1 Zugriffs- und Berechtigungsmanagement | Rollen, Least Privilege, privilegierte Zugriffe, Agentur-/Maklerzugriffe | Use Case: Berechtigungsanomalien |
| U2 Cloud- und Entwicklungssicherheit | Secure SDLC, MLOps-Sicherheit, Secrets | |
| U3 Umgang mit KI-Tools und Daten | Kein Upload vertraulicher Daten in nicht freigegebene Tools; freigegebene Tool-Liste; Prompt-Injection-Bewusstsein | direkt |
| U4 Vorfallmanagement | Meldung: FINMA (Cyber-Meldepflicht innert 24 h nach Art. 29 Abs. 2 FINMAG, Aufsichtsmitteilung), BaFin/DORA-Meldewesen (schwerwiegende IKT-Vorfälle) | Vorfall-Zusammenfassungs-Use-Case |
| U5 Business Continuity / Resilienz | Notfallpläne VERA-Ausfall, MINT-Ausfall, Cloud-Ausfall | |
| U6 Kryptografie und Datenübertragung | | |
| U7 Physische Sicherheit | Standorte | |
| U8 Lieferanten | Verknüpfung R06 | |

### 3.9 R08 Vollmachts- und Kompetenzordnung

| Bereich | Inhalt | Beispielhafte Schwellen (fiktiv) |
|---|---|---|
| Zeichnungsberechtigung | Kollektivunterschrift zu zweien, Handelsregister-Logik CH, Prokura DE | |
| Underwriting-Kompetenzen | Stufen U1–U5 je Sparte; Verweis auf Zeichnungsrichtlinien (Sparten-AP) | Betriebshaftpflicht: Sachbearbeiter bis CHF 2 Mio. Deckungssumme, Senior bis 10 Mio., Chief UW darüber; Leben: Risikosumme bis 500 k Sachbearbeiter, ärztliche Prüfung ab 1 Mio. |
| Schaden-/Leistungskompetenzen | Reservierung, Zahlung, Ablehnung, Vergleich | Zahlung bis CHF 5'000 automatisiert (MINT), bis 25'000 Sachbearbeiter, bis 250'000 Teamleitung, darüber Schadenleitung + Legal |
| **KI-Entscheidungsgrenzen** | Vollautomatisch nur bei positiven Entscheiden unter Schwelle; jede Ablehnung/Erschwerung durch Mensch; Kulanz nur Mensch | Direkte Grundlage für Agenten-Use-Cases |
| Finanzkompetenzen | Beschaffung, Investitionen, IT-Projekte (KI-Projekte > CHF 500 k via Technology & AI Committee) | |
| Vertragsabschlüsse mit Vermittlern | | |
| Delegation und Stellvertretung | | |

### 3.10 R09 Verhaltenskodex

Gliederung: Werte (Verlässlichkeit – aus Pfefferminz, Neugier – aus Minzia, Fairness, Verantwortung), Umgang mit Kundinnen/Kunden, Umgang untereinander (Diversität, Sprache – „wir duzen uns in Berlin, in Olten entscheidet das Team"), Integrität, Umgang mit Daten und KI (Kurzfassung), Nachhaltigkeit, Meldewege. Ton: nahbar, kurze Sätze. Zweck in Use Cases: Stilreferenz, Ethik-Prüfung generierter Texte, Onboarding.

### 3.11 R10 Prozesshandbuch und Prozesslandkarte

| Ebene | Inhalt |
|---|---|
| Landkarte | Führungsprozesse (Strategie, Risiko, Compliance, Governance) – Kernprozesse (Produktentwicklung, Vertrieb & Beratung, Antrag & Underwriting, Bestandsverwaltung, Schaden/Leistung, Beschwerde) – Unterstützungsprozesse (IT, Daten & KI, HR, Finanzen, Einkauf, Kommunikation) |
| Prozesssteckbriefe (30–40) | Zweck, Input/Output, Rollen (RACI), Systeme (VERA/SILAS/MINT), Kontrollen, KPIs, Automatisierungsgrad (Ist/Ziel), regulatorische Bezüge, Varianten CH/DE |
| Detailprozesse als Text-BPMN (10 ausgewählte) | Antrag Haftpflicht online, Risikoprüfung Leben, Schadenmeldung bis Zahlung, Leistungsfall Todesfall, Beschwerde, Kundendatenänderung, KYC Einmalprämie, Storno/Rückkauf, KI-Use-Case-Freigabe, Datenschutz-Auskunft |
| Rolle | Basis für Process-Mining-Daten (Datenarchitektur-AP liefert Event-Logs), Agenten-Design, Automatisierungspotenzial-Analysen |

### 3.12 R11–R13 Kurzrichtlinien

| Richtlinie | Kerninhalte |
|---|---|
| R11 Nutzung generativer KI am Arbeitsplatz | Erlaubte Tools (interner „Pfefferminzia Assistent" auf MINT-LLM-Gateway), verbotene Eingaben, Kennzeichnungspflicht, Verantwortung bleibt beim Menschen, Beispiele |
| R12 Interessenkonflikte und Geschenke | Schwellen, Register, Vermittlerbezug |
| R13 Produktfreigabe (POG) | Zielmarkt, Produkttest, KI-Features im Produkt (z. B. dynamische Preise) benötigen zusätzliche Freigabe |

---

## 4. Regulatorischer Rahmen CH vs. DE – Referenzdokument (Vergleichstabelle)

Das Referenzdokument „Regulatorischer Rahmen Schweiz–Deutschland" (ca. 20 Seiten, Owner Compliance, Locale de-CH, Stand 2026, mit Hinweis „vereinfachte Darstellung für Schulungszwecke") soll die folgenden Unterschiede tabellarisch enthalten. Alle Angaben sind bei der Ausformulierung nochmals zu prüfen (siehe Spalte „Prüfen").

| Dimension | Schweiz | Deutschland | Sichtbar im Datensatz durch | Prüfen |
|---|---|---|---|---|
| Aufsichtsbehörde | FINMA (Bern); Gruppenaufsicht | BaFin (Bonn/Frankfurt); Niederlassung eines CH-Versicherers: BaFin-Zulassung Niederlassung; Leben: eigene AG | Briefköpfe, Meldeadressaten, Protokolle | – |
| Aufsichtsgesetz | VAG CH (rev. 01.01.2024), AVO, FINMA-Rundschreiben/Aufsichtsmitteilungen | VAG DE (Solvency II-Umsetzung), MaGo, DORA (seit 17.01.2025) | Compliance-Handbuch Kap. 2 | Revisionen |
| Vertragsrecht | VVG CH (rev. 01.01.2022) | VVG DE (2008), VVG-InfoV | AVB (Sparten-AP), Kundenbriefe | – |
| Solvenzregime | Swiss Solvency Test (SST): SST-Quotient, Zielkapital, risikotragendes Kapital; Bericht an FINMA jährlich; Offenlegung „Bericht über die Finanzlage" | Solvency II: SCR, MCR, Solvenzquote; SFCR öffentlich, RSR an BaFin, QRT quartalsweise/jährlich | Solvenzreports (Kap. 5) | – |
| ORSA | FINMA-RS 2016/3 ORSA | § 27 VAG, ORSA-Bericht an BaFin | Risikobericht | – |
| Schlüsselfunktionen | Compliance, Risikomanagement, Interne Revision, verantwortlicher Aktuar | Compliance, Risikomanagement, Interne Revision, Versicherungsmathematische Funktion | Organigramm | – |
| Sprache/Rechtschreibung | Schweizer Hochdeutsch: **ss statt ß**, „Grüsse", Helvetismen (Offerte, Police, Franchise, Rückkaufswert, „allfällig", „Betreibung") | Bundesdeutsch: **ß**, „Versicherungsschein", „Beitrag" (Leben) oder „Prämie", „Selbstbeteiligung", „Mahnverfahren" | Locale-Metadatum, Glossar, Textbausteine | Glossar konsolidieren |
| Zahlen-/Datumsformat | CHF 1'250.00; 3. September 2026 oder 03.09.2026 | 1.250,00 EUR; 03.09.2026 | Reports, Briefe | – |
| Währung | CHF | EUR | Masterdatei mit Kurs | – |
| Anrede/Grussformel | „Freundliche Grüsse", „Sehr geehrte Frau …" | „Mit freundlichen Grüßen" | Korrespondenz | – |
| Adressformat | 4-stellige PLZ, Kantonskürzel optional, Postfach | 5-stellige PLZ | Kundenstammdaten | – |
| Identifikatoren Personen | **AHV-Nummer (756.xxxx.xxxx.xx)** – Verwendung durch Private eingeschränkt (systematische Nutzung nur gesetzlich erlaubt, z. B. BVG/3a-Meldungen) | **Steuer-Identifikationsnummer (11-stellig)** – Leben: Rentenbezugsmitteilung, Kirchensteuerabzug auf Kapitalerträge; Sozialversicherungsnummer nicht verwenden | Datenmodell (Datenarchitektur-AP) mit Feld je Land, Datenschutzrichtlinie | Rechtsgrundlagen AHVG |
| Identifikatoren Firmen | UID (CHE-xxx.xxx.xxx), Handelsregister kantonal | Handelsregisternummer (HRB/HRA), USt-IdNr., Transparenzregister | Firmenkunden-Personas | – |
| Vermittlerrecht | VAG CH Art. 40 ff.: gebunden/ungebunden, FINMA-Register (ungebundene), Aus-/Weiterbildung, Provisionsoffenlegung ungebundene Vermittler | § 34d GewO, IHK-Register, § 59 ff. VVG; Weiterbildung 15 h/Jahr; Provisionsabgabeverbot (§ 48b VAG) | Vermittlerverträge, Compliance-Handbuch | – |
| Beratungs-/Dokumentationspflicht | VVG Art. 3 Informationspflicht; seit 2024 VAG Art. 45: Vermittler müssen Bedürfnisse erfassen und Beratung dokumentieren (Beratungsprotokoll) | § 6 VVG: Beratungs- und Dokumentationspflicht (Beratungsprotokoll) mit Verzichtsmöglichkeit; § 61 VVG Vermittler; § 7 VVG Informationspflichten, Produktinformationsblatt | Beratungsprotokoll-Muster je Land, Use Case „Protokoll-Vollständigkeit prüfen" | Detailanforderungen |
| Widerrufsrecht | VVG Art. 2a: 14 Tage (seit 2022) | § 8 VVG: 14 Tage; **Leben 30 Tage** (§ 152 VVG) | Antragsprozess, Kundenbriefe | – |
| Ordentliche Kündigung | VVG Art. 35a: nach 3 Jahren jährlich mit 3 Monaten Frist (Ausnahme Leben) | § 11 VVG: Verträge >3 Jahre zum Ende des 3. Jahres kündbar, Frist 3 Monate; Leben § 168 VVG jederzeit zum Ende der Versicherungsperiode | AVB, Storno-Prozess | – |
| Kündigung im Schadenfall | VVG Art. 42 | § 92 VVG | Schadenprozess | – |
| Verjährung Ansprüche | VVG Art. 46: 5 Jahre (seit 2022) | § 195 BGB: 3 Jahre (Regelverjährung) | Leistungsprozess | – |
| Steuern auf Prämien | **Stempelabgabe** 5 % auf Haftpflichtprämien; rückkaufsfähige Leben mit Einmalprämie 2,5 %; periodische Lebensprämien befreit | **Versicherungsteuer** 19 % auf Haftpflicht; Lebensversicherung befreit (§ 4 VersStG) | Prämienrechnungen, Finanzreports | Sätze prüfen |
| Datenschutz | DSG (rev. 01.09.2023), EDÖB; Datenschutzberater freiwillig; Meldung Vorfall „so rasch als möglich"; Auskunft 30 Tage; Art. 21 automatisierte Einzelentscheidung (Informationspflicht) | DSGVO + BDSG; DSB Pflicht; Landesdatenschutzbehörde (für Leipzig: Sächsischer Datenschutzbeauftragter); Meldung 72 h; Auskunft 1 Monat; Art. 22 DSGVO + § 37 BDSG (Versicherungsausnahme) | R02, Datenschutzvorfall-Memo | – |
| Gesundheits-/genetische Daten | GUMG: Verbot von Gentest-Anforderung; Nutzung vorbestehender Ergebnisse nur oberhalb Versicherungssumme (Schwelle im Gesetz) | GenDG § 18: analog, Schwelle EUR 300'000 Versicherungssumme bzw. Jahresrente | Zeichnungsrichtlinien Leben (Sparten-AP), KI-Datenfreigabe | Schwellen prüfen |
| Unisex-Tarife | Nicht gesetzlich vorgeschrieben; geschlechtsabhängige Tarifierung Leben zulässig | Pflicht seit 21.12.2012 (EuGH Test-Achats) | Tarifdokumente, Bias-Diskussion | – |
| Höchstrechnungszins Leben | FINMA-Vorgaben/technischer Zinssatz (Aufsicht) | DeckRV: 1,0 % seit 01.01.2025 | Aktuarielle Reports | Werte prüfen |
| Kundenschutz Leben / Sicherung | Gebundenes Vermögen (Art. 17 ff. VAG CH) | Sicherungsvermögen + Sicherungsfonds (gesetzlich) | Compliance-Handbuch | – |
| Geldwäscherei | GwG CH, GwV-FINMA, SRO-SVV; MROS | GwG DE; FIU; Transparenzregister | R04 | – |
| Ombudsstelle | Ombudsstelle Privatversicherung und Suva (Zürich) | Versicherungsombudsmann e.V. (Berlin); BaFin-Beschwerdestelle | R05 | – |
| Beschwerde-Meldung an Aufsicht | Keine standardisierte Statistikmeldung (Erwartung faires Beschwerdemanagement) | Jährliche Beschwerdestatistik an BaFin | Beschwerdereport | Details |
| KI-Regulierung | Kein AI Act; FINMA-Aufsichtsmitteilung 08/2024 (Governance, Inventar, Datenqualität, Tests, Erklärbarkeit); Bundesrat: Ratifikation Europarats-KI-Konvention, sektorielle Regulierung geplant | EU AI Act (2024/1689): Leben-Risikobewertung/Preisbildung = Hochrisiko (Anhang III Nr. 5 lit. c); Transparenzpflichten Chatbots; AI-Literacy; BaFin-Erwartungen zu Algorithmen/KI, EIOPA-Opinion KI-Governance | R03, Modellinventar, Memo AI-Act-Betroffenheit | Zeitplan Hochrisiko-Pflichten |
| IKT-/Cyber-Aufsicht | FINMA Cyber-Meldepflicht (24 h), FINMA-RS Corporate Governance (operationelle Risiken), Outsourcing-RS 2018/3 | DORA (seit 2025): IKT-Risikomanagement, Vorfallmeldung, Drittparteienregister, TLPT | R06, R07 | – |
| Sozialversicherungs-Kontext Leben | Säule 3a (steuerbegünstigt, Maximalbeträge), 3b, BVG | Basisrente („Rürup"), Riester (Auslaufmodell), bAV; § 10 EStG | Produkte (Sparten-AP), Kunden-Personas | – |
| Vertragssprache/Mehrsprachigkeit | DE/FR/IT-Pflicht je nach Kundschaft (im Datensatz nur DE) | DE | Hinweis in Onboarding-Guide | – |
| Gerichtsstand/Recht | Schweizer Recht, Gerichtsstand Wohnsitz VN (Art. 46a VVG) | Deutsches Recht, § 215 VVG | AVB | – |

Empfehlung: Das Referenzdokument zusätzlich als maschinenlesbare Tabelle (`regulatorik-ch-de.csv`) ausliefern, damit Use Cases wie „Prüfe Brief auf Landeskonformität" darauf zugreifen können.

---

## 5. Meldewesen und Reporting – Artefakte

### 5.1 Grundsatz

Jeder Bericht liegt in **zwei Formen** vor: (a) narratives Dokument (PDF/Markdown, 3–20 Seiten) und (b) strukturierte Daten (CSV/Parquet aus der Masterdatei). Zeitreihe: monatlich 01/2024–06/2026, quartalsweise Q1/2024–Q2/2026, jährlich 2023–2025. Alle Berichte tragen die Kennzahlen-Masterdatei-Version als Metadatum.

### 5.2 Berichtsliste

| # | Bericht | Intern/Extern | Frequenz | Adressat | Inhalt (Kennzahlen) | Umfang | Use-Case-Bezug |
|---|---|---|---|---|---|---|---|
| B01 | GL-Quartalsbericht („Quartalsspiegel") | intern | Q | GL, VR | Prämien, Neugeschäft, CR, Storno, Kosten, Personal, Projektampeln, Top-Risiken | 12–15 Seiten + CSV | Zusammenfassung, Q&A über Zeitreihen |
| B02 | Schadenquoten-Report Haftpflicht | intern | M | COO, CUO, Aktuariat | Schadenquote, Kostenquote, CR je Segment/Markt/Kanal, Grossschäden, Reserveentwicklung, Bearbeitungsdauer, Automatisierungsquote, Betrugsverdachtsquote | 6 Seiten + CSV (Segment × Monat) | Analytics, Anomalieerkennung, Trendkommentar generieren |
| B03 | Leben-Bestandsreport | intern | M | CUO, Chefaktuar | Neugeschäft (APE), Storno-/Rückkaufquote, Sterblichkeit A/E, Annahmequote, Erschwerungen, Bearbeitungszeit Risikoprüfung, Anteil KI-vorgeprüft | 6 Seiten + CSV | Analytics, Fairness-Analysen (Annahmequote nach Merkmalen) |
| B04 | Vertriebsreport | intern | M | CSO | Neugeschäft je Kanal/Region/Agentur, Stornofrühindikatoren, Beratungsprotokoll-Vollständigkeit | 5 Seiten + CSV | Vertriebsanalytik |
| B05 | Beschwerdestatistik | intern + extern (DE an BaFin jährlich) | Q, J | Compliance, GL, BaFin | Anzahl je Kategorie/Sparte/Kanal/Land, Bearbeitungsdauer, Ombudsfälle, Root Causes, KI-bezogene Beschwerden | 4 Seiten + CSV + Beschwerde-Einzelfalldaten (anonymisiert, 600 Fälle) | Klassifikation, Zusammenfassung, Trendwarnung |
| B06 | Risikobericht CRO | intern | Q | GL, VR Audit & Risk | Risikolandkarte, Top-10-Risiken, Limitauslastung, Modellrisiko/KI-Risiken, Szenarien | 15 Seiten | Zusammenfassung für VR, Risiko-Q&A |
| B07 | ORSA-Bericht (CH-Gesellschaften, DE-Tochter) | intern + Aufsicht | J | VR, FINMA, BaFin | Gesamtsolvabilitätsbedarf, Szenarien, Kapitalplanung 3 Jahre, Verknüpfung Strategie | 25–30 Seiten (je 1 CH, 1 DE) | Langdokument-Zusammenfassung, Vergleich CH/DE |
| B08 | SST-Bericht (Kurzfassung) und Bericht über die Finanzlage CH | Aufsicht / öffentlich | J | FINMA / Öffentlichkeit | SST-Quotient (z. B. 198 % Leben, 231 % Nichtleben), Zielkapital, risikotragendes Kapital, Marktrisiko, Versicherungsrisiko | 8 + 20 Seiten | Kennzahlenextraktion |
| B09 | SFCR DE-Leben-Tochter und QRT-Auszug | öffentlich / Aufsicht | J, Q | Öffentlichkeit / BaFin | Solvenzquote (z. B. 214 %), SCR-Komponenten, Eigenmittelklassen, versicherungstechnische Rückstellungen | 40 Seiten + CSV-QRT-Auszug | Strukturierte Extraktion |
| B10 | Geschäftsbericht Gruppe 2024, 2025 | öffentlich | J | Aktionäre, Öffentlichkeit | Lagebericht, Zahlen, Corporate Governance, Nachhaltigkeit (Art. 964a ff. OR), Vergütung | 60–80 Seiten | Langdokument-RAG, Konsistenzcheck mit Pressemitteilungen |
| B11 | Compliance-Jahresbericht | intern | J | GL, VR | Risikoanalyse, Vorfälle, Schulungen, Aufsichtskontakte, Massnahmen | 12 Seiten | Zusammenfassung |
| B12 | Datenschutz-Jahresbericht DSB | intern | J | GL | Betroffenenanfragen, Vorfälle, DSFA, Auftragsverarbeiter | 8 Seiten | – |
| B13 | KI-/Modellrisiko-Report (Model Inventory Report) | intern | Q | AI Governance Board, VR Tech & AI Committee | Modelle je Klasse, Validierungsstatus, Performance-Drift, Bias-Kennzahlen, Vorfälle, Human-Override-Quote | 8 Seiten + CSV | Kern für KI-Governance-Use-Cases |
| B14 | IT-/Informationssicherheitsreport | intern | Q | CIO, GL | Verfügbarkeit VERA/SILAS/MINT, Vorfälle, Phishing-Quote, DORA-Meldungen | 5 Seiten + CSV | Vorfall-Zusammenfassung |
| B15 | Internes Revisionsprogramm und 3 Prüfberichte (KI-Governance, Outsourcing Minzia Tech, Schadenprozess DE) | intern | J | Audit Committee | Feststellungen, Massnahmen, Fälligkeiten | je 10 Seiten | Findings-Tracking, Zusammenfassung |
| B16 | Outsourcing-/IKT-Drittparteienregister (DORA-Informationsregister-Logik) | intern + Aufsicht | J | CRO, BaFin | Register-Tabelle | CSV, 20 Einträge | Klassifikation |
| B17 | Aufsichtskorrespondenz (Auswahl: FINMA-Anfrage KI-Governance 2025 mit Antwort; BaFin-Anzeige Outsourcing; BaFin-Rückfrage Beschwerdestatistik) | extern | ad hoc | – | Briefe | 6–8 Dokumente | Antwortentwürfe generieren |
| B18 | Nachhaltigkeits-/ESG-Kurzbericht | öffentlich | J | – | Klimarisiken Kapitalanlage, Sozialkennzahlen | 10 Seiten | Nebenrolle |
| B19 | Monatliches KPI-Dashboard (siehe M10) | intern | M | alle Führungskräfte | 25 Kern-KPIs | CSV + Beschreibung | Dashboard-Q&A |
| B20 | Geldwäscherei-Jahresbericht Leben | intern | J | GL, SRO-SVV / interne Prüfung | Kundenrisikoverteilung, Verdachtsmeldungen (CH/DE getrennt), Schulungen | 6 Seiten | – |

### 5.3 Masterdatei-Kennzahlen (Mindestumfang, Abstimmung mit Datenarchitektur-AP)

| Kennzahlengruppe | Granularität | Beispiele |
|---|---|---|
| Prämien und Bestand | Monat × Gesellschaft × Sparte × Segment × Markt × Kanal | Bruttoprämie, Verträge, Neugeschäft, Storno |
| Schaden | Monat × Segment × Markt | Meldungen, Zahlungen, Reserven, Schadenquote, Grossschäden, Bearbeitungsdauer, Betrugsverdacht |
| Leben | Monat × Produkt × Markt | APE, Annahmequote, Erschwerungen, Rückkäufe, Leistungsfälle, A/E-Sterblichkeit |
| Kunden | Monat × Markt | Kundenzahl, NPS, Beschwerden, Kontaktvolumen je Kanal |
| Finanzen/Solvenz | Quartal × Gesellschaft | Ergebnis, Kosten, Eigenmittel, SST-Quotient, Solvenzquote |
| Personal/Kultur | Quartal × Standort × Herkunft (Pfefferminz/Minzia/neu) | FTE, Fluktuation, Engagement-Index, KI-Vertrauens-Index |
| KI/Modelle | Monat × Modell | Volumen, Automatisierungsquote, Override-Quote, Drift, Bias-Kennzahl, Vorfälle |
| IT | Monat × System | Verfügbarkeit, Vorfälle, Tickets |

---

## 6. Personas

Namenskonvention: fiktive, im DACH-Raum plausible Namen; keine Namen realer Personen aus der Branche, insbesondere keine Namen von Mitarbeitenden des realen Fachmediums „Pfefferminzia" (siehe Kap. 7). Vor Finalisierung Namensabgleich per Websuche (Name + Versicherung).

### 6.1 Mitarbeiter-Personas (14)

| # | Name | Rolle, Standort | Herkunft | Alter | Haltung zu KI | Typische Aufgaben | Storyline-Funktion |
|---|---|---|---|---|---|---|---|
| P01 | Beatrice Hauenstein | CEO, Olten | Pfefferminz (seit 2021, vorher extern) | 54 | Strategisch überzeugt, will Ergebnisse bis 2027 | Strategie 2030, Town Halls, VR-Berichte | Treiberin, Brückenbauerin, Absenderin vieler Memos |
| P02 | Dr. Lena Mbatha-Keller | Chief Data & AI Officer, Berlin | Minzia-Mitgründerin (Aktuarin, Data Science) | 38 | Visionär, ungeduldig gegenüber Governance-Aufwand, lernt Regulatorik zu schätzen | Modellinventar, AI Governance Board, Use-Case-Priorisierung | Zentrale KI-Figur, Konflikt mit CIO, Gegenüber der FINMA-Anfrage |
| P03 | Urs Bächtold | CIO, Olten | Pfefferminz (28 Jahre im Haus) | 58 | Skeptisch-vorsichtig: „VERA läuft seit 30 Jahren ohne Ausfall" | Betrieb Altsysteme, Migration Office, Informationssicherheit | Legacy-Verteidiger mit berechtigten Einwänden |
| P04 | Dr. Konstantin Reber | CRO, Olten | extern (2024, vorher Rückversicherung) | 47 | Nüchtern: „Zeig mir die Validierung" | ORSA/SST, Modellrisiko, Risikobericht | Neutraler Schiedsrichter, verlangt Nachweise |
| P05 | Martina Jost | General Counsel & CCO, Olten | Pfefferminz | 51 | Rechtlich getrieben, sieht AI Act als Chance zur Ordnung | Compliance-Handbuch, KI-Richtlinie mit P02, Aufsichtskontakt | Owner Compliance-Artefakte |
| P06 | Sven Lindqvist-Brandt | Datenschutzbeauftragter Gruppe, Leipzig | Pfefferminz (seit 2016) | 44 | Kritisch-konstruktiv, nach Testdaten-Vorfall verschärft | DSFA, Auskunftsersuchen, Datenfreigaben für Modelle | Bremser aus gutem Grund |
| P07 | Ruth Amrein | Leiterin Leistungsprüfung Leben CH, Olten | Pfefferminz (31 Jahre) | 59 | Ablehnend bis resigniert: „Der Computer kennt die Familie nicht" | Todesfall-/Invaliditätsleistungen, Kulanzentscheide | Wissensträgerin VERA, Pensionierung 2027 → Wissenstransfer-Use-Case |
| P08 | Tobias Wenger | Senior Underwriter Betriebshaftpflicht, Zürich | Pfefferminz | 41 | Pragmatisch, nutzt KI-Vorprüfung gern, misstraut Preismodellen | KMU-Risiken, Makleranfragen, Kompetenzstufe U4 | Beispiel Kompetenzordnung, Makler-Storyline |
| P09 | Aylin Demirci | Teamleiterin Schaden Haftpflicht DE, Leipzig | Pfefferminz DE | 36 | Begeistert, fordert mehr Automatisierung, unterschätzt Risiken | Schaden-Triage mit MINT, Betrugsverdachtsfälle, Beschwerden 2nd Level | Trägerin Schaden- und Betrugsfall-Storylines |
| P10 | Jonas Pfister | ML Engineer / MLOps Lead, Berlin | Minzia | 31 | Technik-optimistisch, genervt von Freigabeprozessen, lernt | Modelle deployen, Monitoring, LLM-Gateway | Realistische Tech-Sicht, Slack-Ton |
| P11 | Isabelle Roth-Fankhauser | Leiterin Agenturvertrieb CH, Bern | Pfefferminz | 49 | Bedroht: Direktkanal kannibalisiert Agenturen | Agenturbetreuung, Provisionsmodell, Beratungsprotokolle | Vertriebskonflikt |
| P12 | Miriam Steinbrecher | Compliance Officer DE / AI Compliance Officer, Leipzig | Pfefferminz DE, neu in KI-Rolle | 33 | Neugierig, überfordert von Tempo, gründlich | EU-AI-Act-Betroffenheit, Beschwerdestelle DE, BaFin-Statistik | Verbindet Beschwerde- und KI-Storyline |
| P13 | Dario Bianchi | Kundenberater Contact Center, Olten | neu (2025) | 26 | Nutzt Assistenten täglich, meldet Fehler | Kundenanfragen, Adressänderungen, Erstkontakt Beschwerden | Frontline-Perspektive, Prompt-Nutzung |
| P14 | Hanna Vollmer | Chief People Officer, Olten/Leipzig | extern (2025) | 45 | Sieht KI als Kulturthema | Kulturumfrage, Integration, Schulung AI Literacy | Owner Kulturartefakte |
| (opt.) P15 | Peter Grünenfelder | Verwaltungsratspräsident-Stv./Minzia-Investorvertreter | Minzia-Seite | 62 | Renditegetrieben, drängt auf Earn-out-KPIs | VR-Sitzungen | Governance-Spannung im VR |

### 6.2 Kunden-Personas (10)

| # | Name | Typ / Markt | Alter / Profil | Produkte | Storyline | Korrespondenzarten |
|---|---|---|---|---|---|---|
| K01 | Familie Niederberger (Simone und Reto) | Privat CH, Luzern | 41/43, zwei Kinder, Eigenheim | Privathaftpflicht CH, Risikoleben (beide), Säule 3a | Schadenfall: Kind beschädigt Nachbars E-Bike; später Erhöhung Risikoleben nach Hauskauf | Schadenmeldung per App, Agenturgespräch, Beratungsprotokoll CH |
| K02 | Jana Ortlepp | Privat DE, Leipzig | 29, Berufseinsteigerin, Online-affin | Privathaftpflicht DE (über App, ex-Minzia), später Risikoleben | Digitaler Antrag, Chatbot-Interaktion, Widerruf innerhalb 14 Tagen und erneuter Abschluss | Chat-Transkripte, E-Mails, Widerrufsschreiben |
| K03 | Schreinerei Kaufmann + Söhne GmbH | Gewerbe CH, Aargau | KMU, 14 Mitarbeitende, Inhaber 57 | Betriebshaftpflicht CH (über Makler), Kollektiv-Risikoleben für Kader | Grossschaden: Wasserschaden bei Kunde CHF 180'000; Regressfrage; Makler fordert schnelle Regulierung | Maklerkorrespondenz, Schadenakte, Gutachten |
| K04 | Bergmann Gebäudetechnik GmbH & Co. KG | Gewerbe DE, Sachsen | 42 Mitarbeitende, Geschäftsführerin 48 | Betriebshaftpflicht DE, bAV-Direktversicherung (Renten) | Underwriting-Fall: Risikoänderung (neuer Geschäftszweig Photovoltaik), Nachtragspflicht, Prämienanpassung; Beratungsprotokoll DE | Makler-E-Mails, Nachtragsdokumente |
| K05 | Elisabeth Vogt-Schnyder | Leben CH, Rentnerin, Solothurn | 71, verwitwet | Kapitalversicherung fällig, Rentenversicherung 3b | Auszahlung Kapital, Leibrentenberatung, Betreuung durch Agentur; Stempelabgabe-Frage | Briefe klassisch, Telefonnotizen |
| K06 | Dr. Farid Nazari | Leben DE, München | 52, selbständiger Arzt | Basisrente, Risikoleben hohe Summe (EUR 1,2 Mio.) | Risikoprüfung mit ärztlichen Unterlagen, GenDG-Grenze, Erschwerung wegen Vorerkrankung; verlangt Erklärung des (KI-gestützten) Entscheids | Ärztliche Fragebögen, Erklärungsschreiben, Anfrage nach Art. 22 DSGVO |
| K07 | Leon Waibel | Leben CH, junger Erwachsener, Zürich | 24, Student, Teilzeit | Säule 3a mit kleinen Beiträgen, Privathaftpflicht | Onboarding volldigital, Beitragspause, Adressänderung, Kündigung Haftpflicht wegen Wechsel | App-Interaktionen, kurze E-Mails, Chat |
| K08 | Hans-Georg Pieper (**Beschwerdeführer**) | Privat DE, Dresden | 63, Frühpensionär | Privathaftpflicht DE | Automatisierte Schadenablehnung (Hundebiss, Ausschluss strittig) ohne menschliche Prüfung; Beschwerde, Eskalation an Ombudsmann und BaFin, Presse-Drohung; Root-Cause führt zu Richtlinienänderung v2.1 | Beschwerdebriefe (scharfer Ton), Ombudsmann-Korrespondenz, interne Eskalations-E-Mails |
| K09 | „Transportlogistik Grimm" e.K. (**Betrugsfall**) | Gewerbe DE, Brandenburg | Einzelunternehmer 39 | Betriebshaftpflicht DE, Privathaftpflicht | Serie inszenierter Drittschäden mit gefälschten Rechnungen; MINT-Betrugsmodell schlägt an, SIU ermittelt, Strafanzeige; Datenschutz- und Fairness-Fragen (Modell nutzt PLZ-Cluster) | Schadenakten, Ermittlungsbericht, Anwaltsschreiben |
| K10 | Nadia Ferreira-Bucher | Leben CH, Einmalprämie (AML-Fall) | 46, Rückkehrerin aus dem Ausland, Basel | Kapitalversicherung mit Einmalprämie CHF 450'000 | KYC: Herkunft der Mittel, PEP-Prüfung (Onkel im Ausland politisch tätig), erhöhte Sorgfalt, am Ende unauffällig | Formulare, Nachfragen, interne AML-Notizen |
| (opt.) K11 | Verein Quartierwerkstatt Olten | Gewerbe/Non-Profit CH | Vereinspräsidentin 35 | Vereinshaftpflicht | Kleine Storyline für Bagatellschaden mit vollautomatischer Zahlung (< CHF 5'000) | App, automatisch generiertes Schreiben |

Empfehlung: pro Persona ein Steckbrief (1 Seite) plus ein „Interaktionsjournal" (chronologische Liste aller Kontakte mit Verweis auf Dokumente), damit Use Cases wie „Fasse die Kundenhistorie zusammen" möglich sind. Personas ausschliesslich mit synthetischen Identifikatoren (siehe 7.3).

---

## 7. Rechtliche Hinweise für den Datensatz selbst

### 7.1 Ergebnis der Namensprüfung (Websuche, 03.09.2026)

| Begriff | Befund | Risiko | Empfehlung |
|---|---|---|---|
| **„Pfefferminzia"** | **Real existent**: „Pfefferminzia" ist seit 2013 ein bekanntes deutsches Fachmedium für Versicherungsvermittler (Website, Printmagazin, Podcast, Plattform für Makler), betrieben von der Pfefferminzia Medien GmbH, Hamburg; zusätzlich existiert eine Pfefferminzia Beteiligungs GmbH. Domains pfefferminzia.de, pfefferminzia.pro und pfefferminzia.versicherung sind belegt. Die Redaktion führt zudem eine KI-Autorenfigur namens „Minzia Kolberg". Eine Marken-Registerprüfung (DPMA, Swissreg, EUIPO) war per Websuche nicht möglich. | **Hoch**: gleiche Branche (Versicherung), identische Schreibweise, Zielgruppe des Kurses (Führungskräfte aus der Versicherungsbranche) kennt das Medium mit hoher Wahrscheinlichkeit; Verwechslungs- und Kennzeichenrisiko (Markenrecht, Namensrecht § 12 BGB / Art. 29 ZGB) nicht ausschliessbar | (1) Registerprüfung DPMAregister, EUIPO eSearch, Swissreg durch Legal veranlassen; (2) **Umbenennung ernsthaft erwägen** – Vorschläge unten; (3) falls der Name beibehalten wird: prominenter Disclaimer inkl. ausdrücklicher Abgrenzung vom Fachmedium, keine Nutzung ähnlicher Logos/Farben (das Medium tritt mit Minz-/Grünmotiven auf), keine .de/.ch/.versicherung-Domains, nur `pfefferminzia.example` |
| **„Minzia"** | Kein Versicherer, keine Versicherungsmarke und kein Start-up dieses Namens gefunden; einziger Treffer die genannte KI-Autorenfigur des Fachmediums | Mittel (wegen Nähe zu „Pfefferminzia") | Als Start-up-Name im Datensatz verwendbar, wenn Gesamtname geändert wird; Persona-Namen dürfen nicht „Kolberg" lauten |
| **„Pfefferminz"** (Altversicherer) | Kein Versicherer, keine AG/GmbH dieses Namens gefunden (generisches Wort) | Niedrig | Verwendbar; Registerprüfung dennoch mitlaufen lassen |

**Alternativvorschläge für den Gesamtnamen** (jeweils vor Verwendung per Websuche und Register zu prüfen): „Menthalis Versicherungen" (Altversicherer „Mentha", Start-up „Thalis"), „Piperita Gruppe" (Mentha piperita = Pfefferminze; „Piper" + „Ita"), „Krauseminz Versicherung" (Altversicherer „Krause", Start-up „Minz.ai"). Damit bleibt die Minz-Metapher (Tradition + Frische) erhalten, die Kollision entfällt. Falls der Kurs den Namen „Pfefferminzia" bereits fest eingeführt hat, ist Variante (3) mit Disclaimer die Mindestlösung; die Entscheidung sollte dokumentiert werden.

### 7.2 Disclaimer-Text (Entwurf, in jedes Artefakt als Fusszeile/Metadatum und einmal als eigenständige Datei `DISCLAIMER.md`)

> **Hinweis zum fiktiven Charakter.** „Pfefferminzia", „Pfefferminz", „Minzia" sowie alle in diesem Datensatz genannten Gesellschaften, Marken, Produkte, Systeme, Standorte, Personen, Kundinnen und Kunden, Vorfälle, Kennzahlen und Dokumente sind frei erfunden und wurden ausschliesslich zu Lehr- und Übungszwecken erstellt. Übereinstimmungen mit real existierenden Unternehmen, Marken, Medien, Behördenentscheidungen oder lebenden bzw. verstorbenen Personen sind unbeabsichtigt und zufällig. Insbesondere besteht keinerlei Verbindung zu gleich- oder ähnlich lautenden realen Unternehmen oder Publikationen der Versicherungsbranche. Regulatorische Angaben (u. a. zu FINMA, BaFin, VAG, VVG, DSG, DSGVO, EU AI Act, DORA, SST, Solvency II) sind vereinfachte, zum Teil bewusst verkürzte Darstellungen mit Stand 2026, dienen nur der Illustration und stellen keine Rechts-, Steuer- oder Aufsichtsberatung dar; für reale Fragestellungen sind die geltenden Rechtsquellen und fachkundige Beratung massgebend. Alle Personendaten sind synthetisch; Identifikatoren (AHV-Nummern, Steuer-IDs, IBAN, Telefonnummern, Adressen, E-Mail-Adressen unter `pfefferminzia.example`) sind konstruiert und gehören keiner realen Person oder Organisation. Die Nutzung erfolgt auf eigene Verantwortung; Gewährleistung und Haftung sind im Rahmen der Lizenz ausgeschlossen.

Kurzfassung (Fusszeile, eine Zeile): „Fiktiver Lehrdatensatz – alle Unternehmen, Personen, Daten und Vorfälle sind erfunden; keine Rechtsberatung; Stand 2026."

Englische Kurzfassung für Metadaten: „Synthetic training dataset. All companies, brands, persons, data and events are fictional; regulatory content is simplified and for educational purposes only; no legal advice."

### 7.3 Massnahmen zur Vermeidung von Verwechslung und Personenbezug

| Bereich | Regel |
|---|---|
| Firmennamen | Keine realen Versicherer, Banken, Makler, Rückversicherer, Ratingagenturen, Beratungsfirmen, Institute; auch Partner (Banken, Verbände) fiktiv und als solche gekennzeichnet; reale Behörden (FINMA, BaFin, EDÖB, Ombudsstellen) dürfen als Institutionen genannt werden, aber ohne fiktive Zitate „im Namen" der Behörde – Aufsichtskorrespondenz im Datensatz mit Kennzeichnung „fiktives Musterschreiben" |
| Personen | Fiktive Namen; Abgleich gegen Branchenpersonen per Websuche; keine Namen von Mitarbeitenden des Fachmediums; keine Fotos realer Personen (falls Avatare: generiert und gekennzeichnet) |
| Adressen | Reale Städte und PLZ erlaubt, Strassen/Hausnummern erfunden oder offensichtlich fiktiv; keine realen Firmenadressen |
| Domains/E-Mail | Ausschliesslich `pfefferminzia.example`, `minzia.example`; keine .de/.ch/.com |
| Telefonnummern | Keine realen Nummern; Muster mit erkennbarem Platzhaltercharakter (z. B. +41 62 000 xx xx, +49 341 000 xxxx); Verwendung vorab prüfen |
| AHV-Nummer / Steuer-ID | Synthetisch mit gültiger Prüfziffer generiert, in Datenarchitektur-AP als „synthetic=true" markiert; Kennzeichnung im Datenkatalog |
| IBAN | Synthetisch mit gültiger Prüfsumme, aber nicht vergebener Bankidentifikation; keine Beispiel-IBAN aus offiziellen Publikationen |
| Logos/Design | Eigenes, einfaches Wort-Bild-Zeichen; keine Anlehnung an reale Insurtechs oder an das Fachmedium |
| Regulatorische Texte | Nur Verweise und Paraphrasen, keine längeren Gesetzes- oder Rundschreiben-Zitate (Urheberrecht bei Aufsichtspublikationen prüfen, amtliche Erlasse sind gemeinfrei, Rundschreiben-Wortlaut trotzdem nicht übernehmen) |
| Reale Ereignisse | Keine Anspielungen auf reale Schadenereignisse, Fusionen, Datenpannen oder Gerichtsverfahren |

### 7.4 Lizenzempfehlung

| Bestandteil | Empfohlene Lizenz | Begründung |
|---|---|---|
| Dokumente, Texte, Personas, Narrative | **CC BY 4.0** (alternativ CC BY-SA 4.0, falls Weiterentwicklungen offen bleiben sollen) | Namensnennung sichert Kontext (Lehrdatensatz), einfache Nachnutzung in Kursen |
| Strukturierte Daten (CSV, Kennzahlen, Event-Logs) | **CC0 1.0** oder CC BY 4.0 | Für Datentabellen ist Attribution unpraktisch; CC0 vereinfacht die Nutzung in Tools |
| Code (Generatoren, Skripte) | MIT oder Apache 2.0 | Standard |
| Zusatzklausel (in LICENSE-Datei) | „Keine Gewährleistung, keine Rechtsberatung, keine Verwendung, die eine Verbindung zu realen Unternehmen suggeriert; keine Nutzung der fiktiven Marken als reale Kennzeichen" | Verstärkt Disclaimer, auch wenn CC-Lizenzen bereits Haftungsausschlüsse enthalten |
| Namensnennungsformat | „Pfefferminzia Lehrdatensatz, © [Kursanbieter], Jahr, CC BY 4.0" | Konsistenz |

Zusätzlich: Dokumentation der Provenienz (welche Artefakte von Menschen, welche von Sprachmodellen erzeugt; EU-AI-Act-Transparenz für KI-generierte Texte ist bei Lehrmaterial sinnvoll), Versionsstand des Datensatzes, Changelog.

---

## 8. Abhängigkeiten, Reihenfolge, offene Punkte

### 8.1 Empfohlene Erstellungsreihenfolge

| Schritt | Artefakt | Grund |
|---|---|---|
| 1 | Namensentscheid (Kap. 7.1) | Steht vor allem anderen; Umbenennung später ist teuer |
| 2 | Kennzahlen-Masterdatei + Zeitachse (Kap. 0, 1.3, 5.3) | Alle Dokumente hängen daran |
| 3 | Unternehmensprofil, Organigramm, Standorte, IT-Landschaft (Kap. 1) | Referenz für alle Autorinnen und Autoren und für Sparten-/Daten-AP |
| 4 | Personas (Kap. 6) | Tragen Korrespondenz und Storylines aller AP |
| 5 | Regulatorik-Referenztabelle CH/DE (Kap. 4) | Sparten-AP braucht sie für AVB und Zeichnungsrichtlinien |
| 6 | Regelwerke R01–R13 (Kap. 3), zuerst R03 KI-Governance und R08 Kompetenzordnung | Use-Case-AP braucht Freigabeschwellen und Klassifizierung früh |
| 7 | Merger-Dokumente (Kap. 2) | Bauen auf Zahlen, Personas, Regelwerken auf |
| 8 | Reports (Kap. 5) | Letzter Schritt, generierbar aus Masterdatei |

### 8.2 Schnittstellen zu anderen Arbeitspaketen

| Thema | Abstimmung mit | Inhalt |
|---|---|---|
| Zeichnungsrichtlinien | Sparten-AP | Kompetenzstufen U1–U5 und KI-Grenzen (R08) müssen mit Sparten-Richtlinien übereinstimmen |
| AVB | Sparten-AP | Widerrufs-/Kündigungsfristen, Sprachvarianten aus Kap. 4 übernehmen |
| Datenmodell | Datenarchitektur-AP | Felder für AHV/Steuer-ID, Locale, Kundennummernkreise VERA/MINT, Vertraulichkeitsklassen, synthetische Identifikatoren, Event-Logs für Prozesse aus R10 |
| Use Cases | Use-Case-AP | Modellinventar (R03 Anhang A) als gemeinsame Liste der KI-Systeme; Beschwerde- und Betrugsfall-Personas als Standardfälle |
| Kulturumfrage-Rohdaten | Datenarchitektur-AP | Freitextgenerierung mit Herkunftsmarker |

### 8.3 Offene Entscheidungen

1. Beibehaltung des Namens „Pfefferminzia" trotz realem Fachmedium (Empfehlung: Umbenennung oder Legal-Freigabe mit Disclaimer).
2. Detaillierungstiefe Romandie (Empfehlung: nur erwähnen).
3. Ob EU-AI-Act-Hochrisiko-Pflichten im Datensatz als „bereits geltend" oder „bevorstehend" dargestellt werden (Empfehlung: Datum als Variable, Memo „Betroffenheitsanalyse" beschreibt beide Szenarien).
4. Ob VR-Protokolle vollständig oder als Auszüge geliefert werden (Empfehlung: Auszüge mit Schwärzungen – realistisch und Use-Case-tauglich).
5. Umfang der englischsprachigen Artefakte aus der Minzia-Welt (Empfehlung: 10–15 % der Berlin-Dokumente in Englisch, um Realität und Mehrsprachigkeits-Use-Cases abzubilden).

---

## Anhang A – Entwurf Modellinventar (R03 Anhang A, Stand 30.06.2026)

Vorschlag für die Einträge; Details (Features, Metriken) mit Use-Case-AP abstimmen. Klassen: A verboten, B hoch, C begrenzt, D minimal (siehe 3.4).

| ID | Modell / KI-System | Sparte / Markt | Zweck | Klasse | Status | Owner | Validierung | Datenquellen | Bemerkung für Storylines |
|---|---|---|---|---|---|---|---|---|---|
| KI-001 | Schaden-Triage Haftpflicht | Haftpflicht CH/DE | Klassifizierung eingehender Schadenmeldungen (Bagatell/Standard/Komplex/Verdacht) | C | produktiv seit 2022 (DE), 2025 (CH) | Schadenleitung | 03/2026 | SILAS, MINT, DOKU-Archiv | Ältestes Minzia-Modell, Grundlage der Kooperation |
| KI-002 | Dunkelverarbeitung Bagatellschäden | Haftpflicht CH/DE | Vollautomatische Prüfung und Zahlung < CHF/EUR 5'000 | C (intern erhöht: „C+", Human-Stichprobe 10 %) | produktiv | Schadenleitung | 03/2026 | SILAS, MINT | Fall K08 (Ablehnung) zeigt Lücke: Ablehnungen wurden fälschlich automatisiert |
| KI-003 | Betrugserkennung Haftpflicht | Haftpflicht DE, Pilot CH | Anomalie-Scoring Schadenfälle | B (intern; AI-Act-Einstufung strittig) | produktiv DE | SIU | 05/2026 mit Auflagen (PLZ-Feature) | SILAS, externe Adressdaten | Fall K09, Fairness-Diskussion |
| KI-004 | Risikoprüfung Leben – Vorprüfung | Leben DE | Automatisierte Annahme bei Standardrisiken, Weiterleitung sonst | **B (AI Act Anhang III 5c)** | Pilot, Freigabe Board 02/2026 mit Auflagen | CUO | 01/2026 | Antragsdaten, Gesundheitsfragen (keine Fremddaten) | Fall K06, DSFA vorhanden, Hochrisiko-Pflichten-Timeline |
| KI-005 | Risikoprüfung Leben – Vorprüfung | Leben CH | wie KI-004 | B (intern, FINMA-Aufsichtsmitteilung) | Pilot | CUO | 01/2026 | VERA-Extrakt, Antragsdaten | FINMA-Anfrage 2025 bezog sich hierauf |
| KI-006 | Pricing-Unterstützung Betriebshaftpflicht | Haftpflicht CH/DE | Tarifvorschlag KMU | C | produktiv seit 2025 | CUO | 12/2025 | Bestandsdaten, Branchencodes | Persona P08 misstraut |
| KI-007 | Stornofrühwarnung Leben | Leben CH/DE | Churn-Score für Bestandsberatung | C | produktiv | CSO | 09/2025 | VERA, Kontaktdaten | Agenturen nutzen Listen; Datenschutz-Zweckbindung geprüft |
| KI-008 | Kunden-Chat-Assistent „Minzi" | alle / CH+DE | Generative Auskunft zu Produkten, Status, FAQ; keine Entscheide | C (Transparenzpflicht) | produktiv seit 04/2026 | Kundenservice | 03/2026 | Wissensbasis (AVB, FAQ, R-Dokumente öffentlich) | Halluzinationsvorfall 05/2026 (falsche Widerrufsfrist DE/CH) |
| KI-009 | Interner Assistent „Pfefferminzia Assistent" | intern | RAG über Regelwerke, Prozesshandbuch, Glossar | D | produktiv | CDAO | 02/2026 | R01–R13, M13 | Basis vieler Kurs-Use-Cases |
| KI-010 | Dokumentenklassifikation Posteingang | intern CH/DE | Klassifikation und Extraktion gescannter Post | D | produktiv | COO | 11/2025 | DOKU-Archiv | OCR-Qualität |
| KI-011 | Beschwerdeklassifikation | intern | Kategorisierung, Dringlichkeit, Fristzuordnung | C | Pilot | Compliance | 04/2026 | Beschwerdedaten | Persona P12 |
| KI-012 | Leistungsprüfung Leben – Dokumentenvorprüfung | Leben CH | Vollständigkeitsprüfung Todesfall-/IV-Unterlagen | C | Pilot | Leistungsprüfung | ausstehend | DOKU-Archiv, VERA | Persona P07 Widerstand |
| KI-013 | AML-Transaktionsscoring | Leben CH/DE | Ergänzung Regelwerk R04 | B (intern) | Konzept | Geldwäscherei-Fachstelle | – | Zahlungsdaten | Fall K10 |
| KI-014 | Sprach-/Tonalitätsprüfung Kundenschreiben | intern | Prüft Briefe auf Locale (ß/ss), Kodex, Verständlichkeit | D | produktiv | Kommunikation | 01/2026 | Textbausteine | Use Case Landeskonformität |
| KI-015 | Beratungsprotokoll-Vollständigkeit | Vertrieb CH/DE | Prüft Protokolle gegen Pflichtinhalte | C | Pilot | CSO/Compliance | 05/2026 | Protokolle Agenturen | Persona P11 |
| KI-016 | Recruiting-Vorselektion | HR | CV-Screening | **B (AI Act Anhang III 4)** | **gestoppt 2025** nach Board-Entscheid | CPO | – | – | Beispiel für Nicht-Freigabe |
| KI-017 | Emotionserkennung im Contact Center | intern | Stimmungsanalyse Anrufe | **A (verboten, Art. 5 AI Act am Arbeitsplatz)** | abgelehnt | – | – | – | Beispiel Klasse A |
| KI-018 | Reserving-Unterstützung Nichtleben | Aktuariat | ML-Ergänzung Chain-Ladder | C | produktiv | Chefaktuar | 12/2025 | SILAS | Modellrisiko-Report |
| KI-019 | Wissenstransfer-Assistent VERA | IT | Code- und Regeldokumentation Altsystem | D | Pilot | CIO | – | VERA-Quellcode | Persona P03/P07, Pensionierungswelle |
| KI-020 | Agenten-Workflow Adressänderung | Kundenservice | Mehrschrittige Automatisierung (Identprüfung, Update VERA+MINT, Bestätigung) | C | Pilot | COO | 06/2026 | VERA, MINT | Agenten-Use-Case, Kundennummern-Mapping |

## Anhang B – Glossar CH/DE (Auszug für das Referenzdokument und den Onboarding-Guide)

| Begriff CH (de-CH) | Begriff DE (de-DE) | Bemerkung |
|---|---|---|
| Police | Versicherungsschein | |
| Prämie | Beitrag (Leben) / Prämie (Haftpflicht) | DE-Leben spricht traditionell von Beiträgen |
| Offerte | Angebot | |
| Selbstbehalt | Selbstbeteiligung | |
| Schadenfall, Schadenmeldung | Schadensfall/Schadenfall, Schadenmeldung | DE Fugen-s uneinheitlich; im Datensatz „Schadenfall" beidseitig, „Schadensersatz" DE vs. „Schadenersatz" CH |
| Betreibung | Mahnverfahren / Zwangsvollstreckung | |
| Versicherungsnehmer/in (VN) | Versicherungsnehmer/in (VN) | gleich |
| Rückkaufswert | Rückkaufswert | gleich |
| Säule 3a / 3b | Basisrente / private Rentenversicherung (3. Schicht) | |
| BVG / Pensionskasse | bAV / Direktversicherung | |
| Ausschliesslichkeitsagentur, gebundener Vermittler | Ausschließlichkeitsvertreter, gebundener Versicherungsvertreter | |
| Broker / ungebundener Vermittler | Versicherungsmakler | |
| Stempelabgabe | Versicherungsteuer | |
| AHV-Nummer | Steuer-ID | vgl. Kap. 4 |
| Verwaltungsrat | Aufsichtsrat (+ Vorstand als Leitungsorgan) | CH: Verwaltungsrat und Geschäftsleitung |
| Geschäftsleitung | Vorstand | |
| Freundliche Grüsse | Mit freundlichen Grüßen | |
| allfällig | etwaig / gegebenenfalls | Helvetismus |
| Traktandum / Traktandenliste | Tagesordnungspunkt / Tagesordnung | Protokolle |
| Verantwortlicher Aktuar | Verantwortlicher Aktuar / Versicherungsmathematische Funktion | |
| SST-Quotient | Solvenzquote (SCR-Bedeckung) | |
| Bericht über die Finanzlage | SFCR | |
| Ombudsstelle Privatversicherung | Versicherungsombudsmann | |
| EDÖB | Datenschutzaufsichtsbehörde (Land) / BfDI | |
| Grossschaden | Großschaden | ss/ß |
| Massnahme | Maßnahme | ss/ß |

## Anhang C – Prüfliste vor Freigabe jedes Artefakts

| Prüfpunkt | Ja/Nein |
|---|---|
| Locale gesetzt und konsequent (ß/ss, Währung, Zahlenformat, Grussformel)? | |
| Alle Zahlen aus der Kennzahlen-Masterdatei (Version referenziert)? | |
| Personas nur aus der Persona-Liste, keine neuen Namen ohne Abgleich? | |
| Keine realen Firmen, Domains, Adressen, Telefonnummern, IBAN? | |
| Regulatorische Aussagen als Paraphrase mit Quelle und „Stand 2026"? | |
| Vertraulichkeitsstufe und Absenderrolle gesetzt? | |
| Disclaimer-Fusszeile vorhanden? | |
| Beabsichtigte Inkonsistenzen in `redaktions-notizen.md` dokumentiert? | |
| Datum innerhalb der Zeitachse (Stichtag 30.06.2026)? | |
| Für KI-Bezug: Modell-ID aus dem Inventar referenziert? | |
