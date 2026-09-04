# Pfefferminzia – Fachplanung Sparte Leben (CH/DE)

Status: Planungsdokument (keine Daten), Version 0.1, Stand 2026-09-03
Geltungsbereich: ausschliesslich Lebensversicherung (Einzelleben) der fiktiven Pfefferminzia AG / Pfefferminzia Versicherungen AG
Zweck: fachliche Grundlage für den synthetischen Lehr-Datensatz und die KI-Use-Cases des Executive-Kurses

---

## 0. Rahmen und Annahmen

### 0.1 Unternehmensfiktion (Leben-relevanter Ausschnitt)

| Aspekt | Pfefferminz (Altgesellschaft) | Minzia (KI-Start-up) | Pfefferminzia (Merger) |
|---|---|---|---|
| Gründung / Historie | 1898, klassischer Lebensversicherer, Sitz Zürich, deutsche Niederlassung seit 1962 (Köln) | 2019, digitaler Risikoleben-Anbieter (Insurtech), CH und DE | Merger per 01.01.2025, gemeinsame Marke ab 01.07.2025 |
| Bestand Leben | ca. 180'000 Verträge CH, ca. 240'000 Verträge DE; überwiegend gemischte Leben und Renten, viele Altverträge (ab 1985) | ca. 25'000 Risikoleben-Verträge (ab 2020), volldigitaler Antrag, automatisierte Risikoprüfung | ca. 445'000 Verträge, davon ca. 60 % Altbestand mit alten Tarifgenerationen |
| Bestandssystem | "PALAS" (Pfefferminz Altbestands-Leben-Administrations-System, Host-basiert, seit 1989), Codes numerisch, Datumsformat JJJJMMTT, Geschlecht 1/2 | "mint-core" (Cloud, JSON-API, ISO-Datum, Geschlecht M/F/D) | beide Systeme parallel, Migration läuft bis 2027 → bewusste Heterogenität im Datensatz |
| Aufsicht | FINMA (CH, VAG), BaFin (DE, VAG DE) | FINMA, BaFin | FINMA (Hauptsitz), BaFin (Niederlassung DE) |
| Vertragsrecht | VVG CH (revidiert per 01.01.2022) / VVG DE (Reform 2008) | dito | dito, Altverträge mit Bedingungen der jeweiligen Vertragsgeneration |

### 0.2 Grundsätze für den Datensatz

- Alles synthetisch: keine realen Personen, keine realen Adressen, keine realen Arztpraxen. Namen, Adressen, IBANs, AHV-/Steuer-IDs werden mit Generatoren erzeugt und gültigkeitsgeprüft (Prüfziffern), aber nie aus realen Quellen übernommen.
- Gesundheitsdaten (besondere Kategorie nach DSGVO Art. 9 / besonders schützenswerte Personendaten nach DSG CH Art. 5 lit. c) werden auf Ebene ICD-10-Kapitel/-Gruppe plus Freitext dargestellt, mit bewusst eingebauten Widersprüchen zwischen Fragebogen, Arztbericht und Leistungsakte (siehe Kap. 7).
- Zwei Rechtsräume, zwei Währungen (CHF/EUR), zwei Bestandssysteme, mehrere Tarifgenerationen: die Heterogenität ist gewollt und ist der zentrale Lernstoff für Dokumentextraktion, RAG und Datenqualität.
- Mengengerüst-Empfehlung für den Kurs: 2'000–5'000 Verträge (nicht 445'000), davon ca. 55 % Altbestand Pfefferminz, 45 % Neugeschäft; je Vertrag 3–12 Dokumente; 5–8 % der Verträge mit Leistungsfall.

---

## 1. Produktportfolio Leben

### 1.1 Empfehlung: drei Kernprodukte plus ein Zusatzbaustein plus Altbestand

| Nr. | Produkt (Marke) | Sparte / Typ | Neugeschäft | Altbestand | Primärer KI-Use-Case |
|---|---|---|---|---|---|
| P1 | **Pfefferminzia RisikoLeben** (CH: "Todesfallrisiko", DE: "Risikolebensversicherung") | Reine Todesfallversicherung, Einzel- oder verbundene Leben, konstante oder fallende Summe | ja (Kernprodukt, digital, Minzia-Erbe) | ja, aus Minzia-Bestand ab 2020 und Pfefferminz "PR"-Tarife ab 1995 | Underwriting-Assistenz mit Gesundheitsfragen, Betrugserkennung im Todesfall |
| P2 | **Pfefferminzia Vorsorge** (CH: gemischte Leben Säule 3a/3b, DE: klassische Kapital-LV nur Altbestand) | Kapitalbildende gemischte Lebensversicherung (Tod + Erleben), klassisch mit Garantiezins, ab 2012 optional fondsgebunden mit Garantie | CH ja (3a und 3b); DE nein (seit 2018 geschlossen, nur Bestand) | ja, grosser Altbestand "Pfefferminz Kapital" (PK-Tarife 1985–2012) | RAG über Bedingungswerke (Tarifgenerationen), Rückkaufsberechnung, Storno-Vorhersage |
| P3 | **Pfefferminzia RentePlus** (DE Schwerpunkt; CH als 3a-Auszahlungsvariante) | Aufgeschobene Rentenversicherung, klassisch oder fondsgebunden mit Beitragsgarantie, Kapitalwahlrecht, Rentengarantiezeit | DE ja (Schicht 3, private Rente); CH nur als Umwandlungsoption bei Ablauf von P2 | ja, "Pfefferminz Rente" PR-Tarife ab 2000 | Churn-Vorhersage (Beitragsfreistellung, Rückkauf), Standmitteilungs-Extraktion, Leistungsfall Erleben/Verrentung |
| Z1 | **Zusatzbaustein Erwerbsunfähigkeit** (CH: EU-Rente und Prämienbefreiung; DE: Berufsunfähigkeits-Zusatzversicherung BUZ) | Zusatzversicherung zu P1, P2, P3 | ja (zu P1 und P3) | ja (an vielen PK-Altverträgen als Prämienbefreiung) | Leistungsfallprüfung EU/BU mit Arztberichten, Dokumentextraktion, Betrugserkennung |

Bewusst **nicht** aufgenommen (Begründung):

| Produkt | Begründung des Ausschlusses |
|---|---|
| Riester-Rente (DE) | Zulagen, Förderlogik, ZfA-Meldungen, Wohn-Riester: zu viel regulatorische Komplexität ohne didaktischen Mehrwert für die KI-Use-Cases. Als "Bestand bei Drittanbieter" allenfalls in Kundenkorrespondenz erwähnbar. |
| Basisrente / Rürup (DE) | Nur als optionale Tarifvariante von P3 ("RentePlus Basis") erwähnen, wenn Steuerthemen didaktisch gewünscht sind; nicht als eigenes Produkt. |
| Selbstständige BU (SBU, DE) | Eigenständiger BU-Markt ist umfangreich; als Zusatzbaustein Z1 bleibt der Leistungsprozess abbildbar, ohne einen eigenen Tarif zu pflegen. |
| Kollektivleben / BVG (CH) | Andere Rechtswelt (BVG, Sammelstiftungen); würde die Sparte verdoppeln. |
| Sterbegeld, Pflegerente, Dread Disease | Nischen; allenfalls als "exotischer Altvertrag" in 1–2 Fällen für Stolpersteine. |
| Fondspolicen ohne Garantie (reine Unit-linked) | Nur als Variante von P2/P3 ab 2012, nicht als eigenes Produkt; Fondsdaten synthetisch minimal (3–5 fiktive Fonds). |

### 1.2 Produktsteckbriefe

#### P1 Pfefferminzia RisikoLeben

| Merkmal | Schweiz | Deutschland |
|---|---|---|
| Zielgruppe | Familien mit Hypothek (Amortisation), Selbständige, Konkubinatspartner, Firmen (Keyperson) | Familien, Immobilienfinanzierer, Existenzgründer, Über-Kreuz-Verträge bei Ehepaaren |
| Versicherungssumme | CHF 50'000 – 2'000'000; typisch 250'000 – 500'000 | EUR 25'000 – 2'000'000; typisch 150'000 – 300'000 |
| Summenverlauf | konstant, linear fallend, annuitätisch fallend (Hypothek) | konstant, linear fallend, annuitätisch fallend |
| Laufzeit | 5 – 35 Jahre, Endalter max. 70 (Altbestand 65) | 5 – 40 Jahre, Endalter max. 75 (Altbestand 65/70) |
| Eintrittsalter | 18 – 60 | 18 – 65 |
| Prämie (Beispiel 30 J., Nichtraucher, 20 J. Laufzeit) | CHF 500'000: ca. CHF 45 – 65 / Monat; Raucher ca. Faktor 1.8 – 2.2 | EUR 300'000: Zahlbeitrag ca. EUR 18 – 28 / Monat (Tarifbeitrag ca. 35 – 50, Differenz = Überschussverrechnung); Raucher ca. Faktor 2 |
| Tarifmerkmale | Geschlecht (CH kein Unisex-Zwang), Raucherstatus, Alter, Laufzeit, Summe, Beruf (Berufsgruppe 1–4), BMI, Hobby-Risiken | Unisex seit 21.12.2012 (Altverträge geschlechtsabhängig), Raucherstatus, Berufsgruppe, Alter, Laufzeit, Summe |
| Rechtliche Besonderheiten | Anzeigepflicht Art. 4–8 VVG CH; Rücktritt/Kündigung des Versicherers innert 4 Wochen ab Kenntnis der Verletzung; Kausalitätserfordernis (Art. 6 Abs. 3); Bezugsrecht widerruflich/unwiderruflich (Art. 76–77); Beitrags- und Konkursprivileg (Art. 79–81) | Anzeigepflicht §§ 19–22 VVG DE; Rücktritt/Kündigung/Vertragsanpassung; Fristen 5 Jahre, 10 Jahre bei Vorsatz/Arglist; Widerruf 30 Tage (§ 152); Einwilligung der versicherten Person (§ 150 Abs. 2); Suizidklausel 3 Jahre (§ 161) |
| Steuer | Todesfallleistung einkommensteuerfrei; Erbschaftssteuer kantonal (Ehegatten meist befreit); bei 3b Stempelabgabe nur auf Einmalprämien (2.5 %), bei laufenden Prämien keine | Todesfallleistung einkommensteuerfrei; Erbschaftsteuer, wenn VN = versicherte Person und Bezugsberechtigter ≠ VN (daher Über-Kreuz-Gestaltung); Beiträge nur begrenzt als Vorsorgeaufwendungen absetzbar |
| Überschussbeteiligung | Prämienrabatt (Sofortverrechnung) oder Todesfallbonus; jährlich deklariert | Überschussverwendung "Beitragsverrechnung" (Zahlbeitrag < Tarifbeitrag) oder "Todesfallbonus"; § 153 VVG |
| Garantiezins | irrelevant (kein Sparanteil), aber Rechnungszins in Tarifkalkulation | irrelevant für Leistung; Rechnungszins in Kalkulation (2025: 1.0 %) |
| Optionen | Nachversicherungsgarantie (Heirat, Geburt, Hauskauf: +50 %, max. CHF 250'000, ohne Gesundheitsprüfung); vorgezogene Todesfallleistung bei terminaler Erkrankung (Prognose < 12 Monate) | Nachversicherungsgarantie; vorgezogene Todesfallleistung; Verlängerungsoption ohne Gesundheitsprüfung |

#### P2 Pfefferminzia Vorsorge (gemischte Lebensversicherung) inkl. Altbestand "Pfefferminz Kapital"

| Merkmal | Schweiz | Deutschland (nur Altbestand) |
|---|---|---|
| Zielgruppe | Vorsorgesparer 25–55, Säule 3a (gebunden) oder 3b (frei); Selbständige ohne Pensionskasse (grosse 3a) | ehemals Sparer mit Steuerprivileg (Verträge vor 2005) und Mittelstand (Beitragsverträge 1985–2012) |
| Versicherungssumme (Erlebensfall = Todesfallsumme, klassisch) | CHF 30'000 – 500'000; typisch 80'000 – 200'000 | EUR 10'000 – 250'000; typisch 25'000 – 80'000; DM-Verträge umgerechnet mit 1.95583 → "krumme" Summen (z. B. EUR 25'564.59) |
| Laufzeit | bis Alter 60–65 (3a: Ablauf frühestens 5 Jahre vor Referenzalter 65, spätestens 5 Jahre danach bei Erwerbstätigkeit) | 12 – 40 Jahre, Ablauf typisch Alter 60/65 |
| Prämie | 3a: max. CHF 7'258 p. a. (2025, mit Pensionskasse) bzw. 20 % Nettoerwerbseinkommen, max. CHF 36'288 (ohne PK); 3b frei; typisch CHF 200 – 600 / Monat | EUR 50 – 300 / Monat oder Einmalbeitrag EUR 10'000 – 100'000 |
| Garantie-/technischer Zins nach Tarifgeneration | siehe Tab. 1.3 (FINMA-Höchstzinssatz, historisch 3.5 % → 0.25 %, seit 2024 wieder leicht steigend) | siehe Tab. 1.3 (Höchstrechnungszins DeckRV: 4.0 % (1994–2000) → 0.25 % (2022–2024) → 1.0 % (ab 2025)) |
| Überschussbeteiligung | jährlicher Überschussanteil gemäss Überschussplan (Zins-, Risiko-, Kostenüberschuss), Schlussüberschuss; kein Legal-Quote-Zwang im Einzelleben (nur Kollektiv BVG 90 %), aber FINMA-Aufsicht über Überschussfonds | MindZV: mind. 90 % Kapitalanlageergebnis, 90 % Risikoergebnis, 50 % übriges Ergebnis; laufende Überschüsse (verzinsliche Ansammlung / Bonussumme), Schlussüberschuss, Beteiligung an Bewertungsreserven (§ 153 Abs. 3) |
| Steuer | 3a: Prämien vom steuerbaren Einkommen abziehbar, Auszahlung separat zu reduziertem Satz besteuert; 3b: Kapitalauszahlung steuerfrei bei Alter ≥ 60, Laufzeit ≥ 5 J., Abschluss vor 66, Einmalprämien mit 2.5 % Stempelabgabe | Abschluss vor 2005: Auszahlung steuerfrei bei ≥ 12 Jahren, ≥ 5 Jahre laufende Beitragszahlung, Todesfallschutz ≥ 60 %; Abschluss ab 2005: Halbeinkünfteverfahren bei ≥ 12 Jahren und Alter ≥ 60 (Abschluss ab 2012: ≥ 62), ab 04/2009 Mindesttodesfallschutz 50 % |
| Bezugsrecht | 3a: gesetzlich vorgegebene Reihenfolge (Art. 2 BVV 3: Ehegatte/eingetragener Partner, dann Nachkommen/unterstützte Personen/Lebenspartner ab 5 Jahren, dann Eltern, Geschwister, übrige Erben), nur eingeschränkt änderbar; 3b: frei | frei (§ 159 VVG), widerruflich/unwiderruflich; im Zweifel Erben |
| Rückkauf | Art. 90 VVG: Anspruch auf Rückkauf/Umwandlung nach 3 Jahren Prämienzahlung; 3a nur bei gesetzlichen Vorbezugsgründen (Wohneigentum, Selbständigkeit, Auswanderung, PK-Einkauf, IV-Rente) | § 169 VVG: Rückkaufswert = Deckungskapital ./. Stornoabzug; Abschlusskosten bei Verträgen ab 2008 auf 5 Jahre verteilt; Altverträge gezillmert (in den ersten Jahren Rückkaufswert nahe 0) |
| Zusatzbausteine | Prämienbefreiung bei EU (typisch 3 Monate Wartefrist), EU-Rente, Unfalltod-Zusatz (verdoppelte Summe) | Beitragsbefreiung bei BU, BUZ-Rente, Unfallzusatzversicherung |

#### P3 Pfefferminzia RentePlus (aufgeschobene Rentenversicherung)

| Merkmal | Schweiz | Deutschland |
|---|---|---|
| Rolle im Portfolio | nur Auszahlungsoption (Umwandlung des Erlebensfallkapitals aus P2 in Leibrente; "Rentenoption") | eigenständiges Kernprodukt Schicht 3 |
| Zielgruppe | Pensionierte 60–70 mit 3b-Kapital | Berufstätige 25–55 (Aufschubdauer 10–40 J.), Ältere mit Einmalbeitrag (Sofortrente oder kurze Aufschubzeit) |
| Beitrag | Einmalprämie CHF 50'000 – 1'000'000 | laufend EUR 50 – 500 / Monat; Einmalbeitrag EUR 10'000 – 250'000 |
| Rentenbeginn | Alter 60 – 70 | Alter 62 – 67 (flexibler Abruf ab 62, Verschiebung bis 75) |
| Garantien | garantierte Rente pro CHF 10'000 Kapital; Rentengarantiezeit 5/10/15 Jahre oder Kapitalrückgewähr | garantierte Mindestrente, garantierter Rentenfaktor (z. B. 26.50 pro 10'000 EUR Fondsguthaben), Kapitalwahlrecht bis 3 Monate vor Beginn, Rentengarantiezeit 10 Jahre, Beitragsrückgewähr im Todesfall vor Rentenbeginn |
| Sterbetafel | Generationentafel des Versicherers (an ERM/ERF 20xx angelehnt), geschlechtsabhängig | DAV 2004 R (Renten), Altbestand DAV 1994 R; Unisex ab 12/2012 |
| Steuer | Leibrente aus 3b: 40 % der Rente steuerbar (Pauschale, Reform in Diskussion) | Ertragsanteilbesteuerung (§ 22 EStG, z. B. 18 % bei Rentenbeginn 65); bei Kapitalwahl Halbeinkünfteverfahren |
| Fondsgebundene Variante | ab 2019 "RentePlus Invest" mit Beitragsgarantie 80–100 % | ab 2012 "Pfefferminz Rente Invest", ab 2019 "RentePlus Invest" (3–5 fiktive Fonds, Ablaufmanagement) |
| Überschüsse | Überschussrente (dynamisch/konstant) | Überschussverwendung: "dynamische Überschussrente", "konstante Überschussrente", "teildynamisch"; in der Aufschubzeit verzinsliche Ansammlung oder Fondsanlage |

#### Z1 Zusatzbaustein Erwerbsunfähigkeit / Berufsunfähigkeit

| Merkmal | Schweiz (Erwerbsunfähigkeit) | Deutschland (Berufsunfähigkeit, BUZ) |
|---|---|---|
| Leistungsart | EU-Rente CHF 500 – 5'000 / Monat und/oder Prämienbefreiung des Hauptvertrags | BU-Rente EUR 500 – 3'000 / Monat und/oder Beitragsbefreiung |
| Definition | Erwerbsunfähigkeit (Unfähigkeit, eine zumutbare Erwerbstätigkeit auszuüben; Bezug auf allgemeinen Arbeitsmarkt, in Anlehnung an IV); Teilgrade 25/40/50/60/70 % | Berufsunfähigkeit ≥ 50 % im zuletzt ausgeübten Beruf für voraussichtlich ≥ 6 Monate (§ 172 VVG); Verzicht auf abstrakte Verweisung (Neuverträge), Altverträge mit abstrakter Verweisung (Stolperstein) |
| Wartefrist | 3, 6, 12 oder 24 Monate (24 Monate koordiniert mit IV-Rentenbeginn) | keine Wartefrist, aber 6-Monats-Prognose; rückwirkende Leistung ab Beginn |
| Leistungsdauer | bis Endalter 60/65 | bis Endalter 60/63/65/67 |
| Koordination | Überentschädigungsgrenze 90 % des Erwerbsausfalls unter Anrechnung IV, UVG, BVG | keine Anrechnung; Nachprüfungsverfahren (§ 174 VVG) |
| Prämie | ca. 2 – 5 % der versicherten Jahresrente, stark berufsabhängig | EUR 30 – 150 / Monat; Berufsgruppen 1+ (Akademiker) bis 5 (Handwerk mit Risiko) |
| Typische Leistungsursachen (Verteilung im Datensatz) | psychisch 35 %, Bewegungsapparat 25 %, Krebs 15 %, Herz-Kreislauf 8 %, Unfall 8 %, sonstige 9 % | analog |

### 1.3 Tarifgenerationen (Altbestand und Neugeschäft)

Die Bezeichnungen und CH-Zinssätze sind fiktiv-plausibel; DE-Höchstrechnungszinsen entsprechen der DeckRV.

| Tarifgeneration (Code) | Verkaufszeitraum | Produkte | Rechnungszins DE | Techn. Zins CH | Sterbetafel DE / CH | Bedingungswerk | Besonderheiten / Stolpersteine |
|---|---|---|---|---|---|---|---|
| PK-85 | 1985 – 06/1994 | gemischte Leben | 3.5 % | 3.5 % | Sterbetafel 1986 M/F / SM/SF 1978 | AVB Pfefferminz 1985 (DE: VVG a. F., § 5a-Modell noch nicht) | teilweise DM-Summen, Papierakte nur gescannt, Bezugsrecht oft "gesetzliche Erben", Prämienbefreiung als Klausel im Antrag statt Baustein |
| PK-95 | 07/1994 – 06/2000 | gemischte Leben, Risiko (PR-95) | 4.0 % | 3.5 % | DAV 1994 T / SM/SF 1988 | AVB 1994, DE Policenmodell (§ 5a VVG a. F.) → "ewiges Widerspruchsrecht" Diskussion | höchste Garantien, hoher Rückkaufsanreiz für Kunden gering, für Versicherer teuer; Steuerprivileg DE (12 Jahre) |
| PK-2000 | 07/2000 – 12/2003 | gemischte Leben, Rente (PR-2000) | 3.25 % | 3.0 % | DAV 1994 T / DAV 1994 R | AVB 2000 | Y2K-Migration in PALAS (Datumsfelder mit 2-stelligem Jahr in Altfeldern) |
| PK-2004 | 01/2004 – 12/2007 | gemischte Leben, Rente | 2.75 % | 2.5 % | DAV 2004 R | AVB 2004; DE letzte Verträge vor Alterseinkünftegesetz (Abschluss bis 31.12.2004 steuerprivilegiert) | Dezember-2004-Welle: viele Abschlüsse mit Rückdatierung; Zuordnungsfehler Abschlussdatum vs. Versicherungsbeginn |
| PK/PR-2008 | 01/2008 – 12/2011 | gemischte Leben, Rente, Risiko | 2.25 % | 2.0 % | DAV 2008 T | AVB 2008 (VVG-Reform DE: Rückkaufswert § 169, Abschlusskostenverteilung, Beratungsprotokoll) | BUZ mit abstrakter Verweisung noch verbreitet; Beratungsprotokolle als neue Dokumentart |
| PL-2012 | 01/2012 – 12/2014 | Rente, Vorsorge (CH 3a), Risiko | 1.75 % | 1.5 % | DAV 2008 T, Unisex ab 21.12.2012 | AVB 2012 | Unisex-Umstellung DE mitten in der Generation → zwei Kalkulationsbasen unter einem Tarifcode (Suffix -U) |
| PL-2015 | 01/2015 – 12/2016 | Rente, Vorsorge | 1.25 % | 1.0 % | DAV 2008 T | AVB 2015 | Niedrigzins, erste Überschussdeklarationen nahe null |
| PL-2017 | 01/2017 – 12/2021 | Rente, Vorsorge, Risiko | 0.9 % | 0.25 % | DAV 2008 T | AVB 2017; CH: neues VVG ab 2022 rückwirkend teils anwendbar | DE geschlossene Kapital-LV ab 2018; CH Prämienzahlungsdauer 3a mit IV-Klauseln |
| MZ-R-2020 | 03/2020 – 12/2024 | Risiko (Minzia digital) | 0.9 % / ab 2022 0.25 % | 0.25 % | DAV 2008 T | AVB Minzia 2020 (kurz, digital, "Klartext") | vollständig digitale Antragsstrecke, Gesundheitsfragen als JSON, keine Unterschrift sondern E-Signatur; abweichende Formulierungen zu Pfefferminz-AVB (z. B. Nachversicherungsgarantie) |
| PZ-2025 | ab 07/2025 | alle Neuprodukte Pfefferminzia | 1.0 % | 0.5 % | DAV 2008 T / DAV 2004 R | AVB Pfefferminzia 2025 (harmonisiert CH/DE mit Länderanhang) | Referenz-Bedingungswerk für RAG; Migration der MZ-Tarife auf PZ-Codes |

---

## 2. Lebenszyklus eines Lebensversicherungsvertrags

### 2.1 Phasenübersicht

| Phase | Auslöser | Kernaktivitäten | Ergebnis / Status | Typische Dauer |
|---|---|---|---|---|
| A. Beratung und Angebot | Kundenanfrage, Vermittler, Online-Rechner | Bedarfsanalyse, Offerte, Beratungsprotokoll (DE § 61/62 VVG; CH Informationspflicht Art. 3 VVG) | Offerte (gültig 4–8 Wochen) | Tage |
| B. Antrag inkl. Gesundheitserklärung | unterschriebener/elektronischer Antrag | Antragsaufnahme, Gesundheitsfragen, Identifikation (GwG DE / GwG CH ab Einmalprämie ≥ CHF 15'000 bzw. EUR 15'000), Einwilligung versicherte Person, Schweigepflichtentbindung | Status "Antrag eingegangen" | 1–3 Tage |
| C. Risikoprüfung (Underwriting) | Antrag vollständig | medizinische, finanzielle, berufliche Prüfung; ggf. Nachfragen, Arztbericht, Untersuchung, Labor; Entscheidung normal / Zuschlag / Ausschluss / Zurückstellung / Ablehnung; Rückfrage-Schleifen | Votum + ggf. Gegenofferte | digital: Minuten bis 2 Tage; mit Arztbericht: 2–8 Wochen |
| D. Policierung | Annahme, ggf. Annahme der Gegenofferte durch Kunde | Police/Versicherungsschein, AVB, Produktinformationsblatt, Erstprämie einziehen; DE Widerrufsfrist 30 Tage; CH Widerrufsrecht 14 Tage (Art. 2a VVG) | Status "in Kraft" | 1–5 Tage |
| E. Bestandsphase | jährlich, ereignisgetrieben | Prämieninkasso, Mahnwesen, Dynamik, Standmitteilung, Überschussmitteilung, Adress-/Bank-/Bezugsrechtsänderungen, Nachversicherung, Abtretung/Verpfändung, Tarifwechsel, Auskünfte | Status "in Kraft", "gemahnt", "ruhend" | Jahrzehnte |
| F. Vertragsänderungen mit Wertwirkung | Kundenwunsch, Zahlungsschwierigkeit | Beitragsfreistellung (DE § 165, CH Art. 90 Abs. 1 Umwandlung), Teilrückkauf, Summenreduktion, Laufzeitverlängerung, Wiederinkraftsetzung nach Beitragsfreistellung (mit Gesundheitsprüfung) | Status "beitragsfrei", "reduziert" | Tage bis Wochen |
| G. Rückkauf / Kündigung | Kündigung durch VN | Rückkaufswertberechnung, Stornoabzug, Steuerbescheinigung (DE Kapitalertragsteuer bei Verträgen ab 2005; CH 3a nur mit Vorbezugsgrund), Auszahlung | Status "storniert / zurückgekauft" | 2–6 Wochen |
| H. Ablauf / Erleben | Ablaufdatum erreicht | Vorankündigung (3–6 Monate), Optionen (Auszahlung, Verrentung, Verlängerung), Auszahlung inkl. Schlussüberschuss | Status "abgelaufen" | 4–8 Wochen |
| I. Leistungsfall Tod / EU / BU | Meldung | siehe Kap. 3 | Status "Leistungsfall offen / reguliert / abgelehnt" | 1 Woche – 6 Monate |
| J. Rentenbezug | Rentenbeginn | Lebensbescheinigung jährlich, Rentenanpassung, Todesfall im Rentenbezug (Garantiezeit) | Status "Rentenbezug" | Jahre |

### 2.2 Dokumente und Datenelemente je Phase

| Phase | Entstehende Dokumente (unstrukturiert) | Entstehende / geänderte Datenelemente (strukturiert) |
|---|---|---|
| A. Beratung | Offerte, Beratungsprotokoll (DE), Kundeninformation nach Art. 3 VVG (CH), Produktinformationsblatt (DE: Basisinformationsblatt für Versicherungsanlageprodukte bei P2/P3) | Offerten-ID, Vermittler-ID, Produkt, Summe, Laufzeit, Prämie, Beratungsdatum, Kanal |
| B. Antrag | Antragsformular (Papier gescannt oder digital), Gesundheitsfragebogen, Einwilligungserklärungen (Datenschutz, Schweigepflichtentbindung, versicherte Person), Ausweiskopie, ggf. Finanzfragebogen, Vermittlerbericht | Partnerstammdaten (VN, VP, BB), Antragsdatum, Rollenzuordnung, Gesundheitsantworten (strukturiert), Raucherstatus, BMI, Beruf, Einkommen, Zahlungsweg, Bezugsrecht |
| C. Risikoprüfung | Ärztliches Zeugnis / Attest, Hausarztbericht, Facharztbericht, Laborbefund, Rückfragen-Korrespondenz, Underwriting-Votum (intern), Gegenofferte, Rückversicherer-Anfrage (fakultativ bei grossen Summen) | UW-Entscheid, Risikoklasse, Zuschlag (% / ‰), Ausschlussklauseln (Codes + Text), Zurückstellungsdatum, Ablehnungsgrund, Prüfer, Dauer, Rückversicherungsanteil |
| D. Policierung | Police / Versicherungsschein, AVB der Tarifgeneration, Tarifbestimmungen, Nachtrag bei Zuschlag/Ausschluss, Begleitschreiben, Widerrufsbelehrung, SEPA-Mandat / LSV-Ermächtigung | Policennummer, Versicherungsbeginn, Ablauf, Tarifcode, Summe, Prämie brutto/netto, Zahlweise, Status, Dynamik-Kennzeichen |
| E. Bestand | jährliche Standmitteilung (DE § 155 VVG), Überschussmitteilung, Dynamik-Ankündigung, Mahnungen (1./2. Mahnung, qualifizierte Mahnung § 38 VVG DE / Art. 20 VVG CH), Adressänderung, Bezugsrechtsänderung, Abtretungsanzeige, Verpfändung (Bank), Bescheinigungen (Steuer 3a, Vorsorgebescheinigung) | Deckungskapital, Rückkaufswert, Überschussguthaben, Dynamik-Historie, Zahlungshistorie, Mahnstufe, Bezugsrechts-Historie, Abtretungsvermerk |
| F. Änderungen | Antrag auf Beitragsfreistellung, Berechnung beitragsfreie Summe, Nachtrag, Wiederinkraftsetzungsantrag mit Kurz-Gesundheitserklärung | neue beitragsfreie Summe, Änderungsdatum, Änderungsgrund, Änderungshistorie |
| G. Rückkauf | Kündigungsschreiben, Rückkaufsberechnung, Steuerbescheinigung, Auszahlungsbestätigung, Rückgewinnungsschreiben (Retention) | Kündigungsdatum, Rückkaufswert, Stornoabzug, Steuerabzug, Auszahlungsdatum, Stornogrund (Kundenangabe), Retention-Ergebnis |
| H. Ablauf | Ablaufankündigung, Optionsschreiben, Ablaufabrechnung, Lebensbescheinigung | Ablaufleistung garantiert / Überschuss / Schlussüberschuss / Bewertungsreserven; Option gewählt |
| I. Leistungsfall | siehe Kap. 3 und 4 | siehe Kap. 5.6 |
| J. Rentenbezug | Rentenbescheid, jährliche Rentenanpassungsmitteilung, Lebensbescheinigung, Steuerbescheinigung (Rentenbezugsmitteilung DE) | Rentenhöhe, Anpassungshistorie, Lebensnachweis-Datum |

### 2.3 Underwriting-Entscheidungen (Phase C) im Detail

| Entscheidung | Code | Bedeutung | Anteil im Datensatz (Empfehlung) | Folge im Vertrag |
|---|---|---|---|---|
| Normale Annahme | N | Antrag zu Tarifbedingungen | 78 % | keine Änderung |
| Annahme mit Zuschlag | Z | Risikozuschlag in % der Risikoprämie (25–300 %) oder ‰ der Summe (Berufs-/Hobbyrisiken) | 10 % | Nachtrag, erhöhte Prämie, Kunde muss Gegenofferte annehmen |
| Annahme mit Ausschluss | A | Ausschlussklausel (nur bei Z1 EU/BU sinnvoll; bei reinem Todesfall selten, z. B. Ausschluss bestimmter Extremsportarten) | 4 % | Nachtrag mit Klauseltext |
| Zurückstellung | R | Entscheidung um 6–24 Monate vertagt (z. B. laufende Abklärung, kürzliche Operation) | 3 % | kein Vertrag, Wiedervorlage |
| Ablehnung | X | kein Versicherungsschutz (z. B. metastasierender Tumor, schwere Herzinsuffizienz, hohe Summe ohne finanziellen Bedarf) | 3 % | Ablehnungsschreiben (ohne detaillierte medizinische Begründung an VN; Begründung ggf. an Arzt) |
| Rückversicherung fakultativ | RV | Summe über Selbstbehalt (z. B. > CHF/EUR 1 Mio) → Rückversicherer-Votum | 2 % (überlappend) | RV-Anteil im Vertrag |

---

## 3. Leistungsfallprozess

### 3.1 Phasen des Leistungsfalls Tod

| Phase | Aktivitäten | Nachweise / Dokumente | Sollzeit |
|---|---|---|---|
| 1. Meldung | Eingang per Brief, Telefon, Portal, Vermittler; Erfassung Leistungsfall; Prämienstopp; Sperre Bezugsrechtsänderung | Todesfallmeldung (formlos oder Formular) | 1–2 Tage |
| 2. Formelle Prüfung | Vertragsstatus (in Kraft? gemahnt? ruhend?), versicherte Person = Verstorbener?, Deckungsprüfung, Wartefristen (Suizid), Verjährung (CH 5 Jahre Art. 46 VVG; DE 3 Jahre § 195 BGB ab Kenntnis) | Sterbeurkunde (CH: Todesschein/Todesurkunde des Zivilstandsamts; DE: Sterbeurkunde Standesamt), Police im Original oder Verlusterklärung, Ausweis des Anspruchstellers | 2–5 Tage |
| 3. Materielle Prüfung | Todesursache; bei Tod innerhalb Anzeigepflichtfrist (CH: Rücktrittsrecht auch nach Todesfall bei Anzeigepflichtverletzung, DE: 5 bzw. 10 Jahre) → Nachprüfung der Gesundheitsangaben; Einholung Arztberichte über Schweigepflichtentbindung; Prüfung Ausschlüsse (Suizid in Wartefrist, Kriegsereignisse, Tötung durch Bezugsberechtigten) | Ärztliche Todesbescheinigung mit Todesursache (DE: vertraulicher Teil nur mit Einwilligung; CH: Todesbescheinigung), Arztberichte, Krankenhausentlassungsberichte, Krankenkassen-Auszug, Obduktionsbericht, Polizeibericht bei unnatürlichem Tod | 1–10 Wochen |
| 4. Bezugsrechtsprüfung | Bezugsrechtsklausel in aktueller Fassung, Widerrufe, Abtretungen/Verpfändungen (Bank geht vor), Erbschein/Erbbescheinigung wenn "Erben" oder keine Bezugsberechtigung, Minderjährige (Beistand/KESB bzw. Familiengericht), Ausland (Apostille), 3a-Reihenfolge nach BVV 3 | Bezugsrechtserklärungen (Historie), Erbschein (DE) / Erbbescheinigung (CH), Ehe-/Geburtsurkunden, Vollmachten, Abtretungsurkunden | 1 Woche – 6 Monate |
| 5. Leistungsberechnung | Versicherungssumme + Überschussguthaben + Schlussüberschuss (klassisch) bzw. max(Summe, Fondswert) (fondsgebunden); Abzug offener Prämien; Zinsen bei Verzug (DE § 14 VVG Abschlagszahlung) | Leistungsabrechnung | 1–3 Tage |
| 6. Auszahlung und Abschluss | Auszahlung per Überweisung (GwG-Prüfung bei Barauszahlungswunsch, PEP-Check), Steuerbescheinigung, Erbschaftssteuermeldung (DE § 33 ErbStG: Anzeige an Finanzamt; CH: kantonale Meldepflicht), Vertragsschliessung | Auszahlungsbestätigung, Meldung Finanzamt | 2–5 Tage |

### 3.2 Phasen des Leistungsfalls Erwerbsunfähigkeit / Berufsunfähigkeit (Z1)

| Phase | Aktivitäten | Nachweise | Sollzeit |
|---|---|---|---|
| 1. Meldung | Leistungsantrag EU/BU, Erhebung der Erwerbsbiographie | Leistungsantrag-Formular (12–20 Seiten), Tätigkeitsbeschreibung, Arbeitgeberbescheinigung | 1 Woche |
| 2. Medizinische Prüfung | Diagnose, Verlauf, Behandlung, Prognose; Vergleich mit Gesundheitsangaben im Antrag (Anzeigepflicht); Gutachten bei Unklarheit | Arztberichte, Facharztberichte, Reha-Bericht, IV-Verfügung (CH) / Rentenbescheid DRV (DE), unabhängiges Gutachten | 6–16 Wochen |
| 3. Berufliche / wirtschaftliche Prüfung | Grad der Erwerbs-/Berufsunfähigkeit, Verweisung (DE nur konkret bei Neuverträgen; abstrakt bei Altverträgen), Überentschädigung (CH), Wartefristbeginn | Lohnabrechnungen, Steuererklärung (Selbständige), Stellenbeschreibung | 2–6 Wochen |
| 4. Entscheid | Anerkennung (befristet/unbefristet, Teilgrad), Ablehnung, Kulanz, Vergleich (Einmalzahlung) | Leistungsentscheid, Anerkenntnis (DE § 173 VVG, befristet max. 1 Jahr) | 1 Woche |
| 5. Laufende Leistung und Nachprüfung | monatliche Rente, Prämienbefreiung, jährliche/zweijährliche Nachprüfung, Wiedereingliederung, Einstellung | Nachprüfungsfragebogen, aktuelle Arztberichte | fortlaufend |

### 3.3 Leistungsfall Erleben / Ablauf

| Schritt | Inhalt | Dokument |
|---|---|---|
| Vorankündigung 6 Monate vor Ablauf | Ablaufleistung (garantiert + Überschuss + Schlussüberschuss + Bewertungsreserven DE), Optionen | Ablaufschreiben |
| Optionswahl | Kapital, Rente (P3), Verlängerung (mit/ohne neue Gesundheitsprüfung), Teilverrentung | Optionsformular |
| Nachweise | Lebensnachweis (Ausweis, ggf. Lebensbescheinigung Gemeinde), Bankverbindung, Police, DE: Steuer-ID, CH: 3a-Auszahlungsgrund | Ablaufabrechnung, Steuerbescheinigung |
| Durchlaufzeit | 2–4 Wochen nach Eingang vollständiger Unterlagen | |

### 3.4 Durchlaufzeiten (Zielwerte und Datensatz-Verteilung)

| Fallart | Median | 90 %-Quantil | Langläufer (>180 Tage), Anteil |
|---|---|---|---|
| Tod, Vertrag > 5 Jahre, Bezugsrecht namentlich | 8 Arbeitstage | 20 Arbeitstage | 1 % |
| Tod, Vertrag < 5 Jahre (Nachprüfung Anzeigepflicht) | 45 Tage | 120 Tage | 8 % |
| Tod, Bezugsrecht "Erben" ohne Erbschein | 90 Tage | 240 Tage | 20 % |
| Tod im Ausland / unnatürlicher Tod | 120 Tage | 365 Tage | 30 % |
| EU/BU Erstprüfung | 110 Tage | 240 Tage | 15 % |
| Erleben | 15 Tage | 40 Tage | 0.5 % |
| Rückkauf | 12 Tage | 30 Tage | 0 % |

### 3.5 Betrugsmuster (für Betrugserkennungs-Use-Case)

| Muster | Beschreibung | Indikatoren im Datensatz | Empfohlener Anteil (der Leistungsfälle) |
|---|---|---|---|
| Verschwiegene Vorerkrankung | Diagnose vor Antrag (z. B. Diabetes, Depression, Tumor) im Fragebogen verneint; Tod/EU innerhalb 2–3 Jahren | Diskrepanz Fragebogen vs. Arztbericht (Erstdiagnosedatum < Antragsdatum), Medikamentenliste, Krankenkassen-Auszug | 6 % |
| Fingierter Todesfall | Sterbeurkunde aus Ausland, kein Leichnam, kurze Vertragsdauer, hohe Summe, Bezugsberechtigter Ehepartner, Kontakt nur über Anwalt | Sterbeurkunde mit Formatabweichungen, fehlende Apostille, Prämienzahlung läuft vom Konto des "Verstorbenen" weiter | 1 % |
| Mehrfachversicherung kurz vor Tod | mehrere Risikoleben-Anträge bei verschiedenen Versicherern innerhalb weniger Monate, Summen ohne erkennbaren Bedarf | Frage "weitere Lebensversicherungen beantragt?" verneint, Hinweis-Informationssystem (DE HIS) Treffer, Summe > 10× Jahreseinkommen | 1.5 % |
| Bezugsrechtsänderung unter Einfluss | Änderung wenige Wochen vor Tod auf Pflegeperson/neue Bekanntschaft, Unterschrift abweichend | Bezugsrechtsänderung < 90 Tage vor Tod, Unterschriftenvergleich, Demenzdiagnose im Arztbericht | 1 % |
| Simulierte / aggravierte BU/EU | Angaben zur Arbeitsunfähigkeit widersprechen Social-Media/Nebenerwerb; Gutachten ohne objektiven Befund | Gutachten-Widersprüche, laufende Selbständigkeit (Handelsregister), Nachprüfung nicht beantwortet | 3 % (der EU/BU-Fälle) |
| Vermittlerbetrug | Vermittler fingiert Anträge (Provisionsbetrug), Stornierung nach Provisionshaftungszeit; Unterschriften kopiert | Häufung identischer Handschrift, E-Mail-Adressen des Vermittlers als Kundenkontakt, Storno-Cluster nach 12/60 Monaten | 1 % (der Verträge eines Vermittlers) |
| Geldwäsche | Einmalprämie hoch, Rückkauf nach kurzer Zeit auf Drittkonto, Zahlung aus Drittstaat | Einmalprämie ≥ 100'000, Rückkauf < 12 Monate, Auszahlungskonto ≠ Einzahlungskonto | 0.5 % |
| Identitätsbetrug im Antrag | versicherte Person existiert nicht oder ist eine andere Person (z. B. gesunder Bruder bei Untersuchung) | Untersuchungsbefund passt nicht zu Alter/BMI aus Antrag, Ausweiskopie unscharf | 0.5 % |

### 3.6 Kulanzfälle (bewusst einbauen)

| Kulanzsituation | Regelungslage | Typische Entscheidung Pfefferminzia |
|---|---|---|
| Tod während Mahnverfahren (Prämie 6 Wochen offen, qualifizierte Mahnung zugestellt) | DE § 38 VVG: Leistungsfreiheit bei Verzug nach Fristablauf; CH Art. 20 VVG: Ruhen der Leistungspflicht nach Mahnfrist | Kulanz bei erstem Verzug und Nachzahlung durch Hinterbliebene, Vermerk "Kulanz K1" |
| Suizid 2 Wochen nach Ablauf der 3-Jahres-Frist / 3 Wochen davor | DE § 161 VVG 3 Jahre (Ausnahme bei krankhafter Störung); CH AVB-abhängig (1–3 Jahre) | Prüfung "Zustand krankhafter Störung der Geistestätigkeit" anhand Arztberichten; teilweise Kulanz (Rückkaufswert statt Summe) |
| Anzeigepflichtverletzung ohne Kausalität | CH Art. 6 Abs. 3 VVG: Leistungspflicht bleibt, wenn verschwiegene Tatsache den Eintritt nicht beeinflusst hat; DE § 21 Abs. 2: bei Kündigung/Rücktritt Leistung, wenn nicht kausal | Leistung mit Vertragsanpassung ex tunc (Zuschlag) |
| Verjährte Ansprüche | CH 5 Jahre ab Ereignis (Art. 46 VVG rev.); DE 3 Jahre ab Kenntnis | Kulanz bei entschuldbarer Unkenntnis (Police erst im Nachlass gefunden) |
| Bezugsrecht widersprüchlich (Testament vs. Police) | Bezugsrecht der Police geht vor (CH Art. 78 VVG, DE § 159/160 VVG), Testament nur schuldrechtlich | Auszahlung an Bezugsberechtigten laut Police; Hinweis an Erben |
| Wiederinkraftsetzung nach Verzug mit unentdeckter Erkrankung | Gesundheitserklärung bei Wiederinkraftsetzung fehlt/unvollständig | Kulanzleistung reduziert |

---

## 4. Dokumenttypen (unstrukturiert)

Legende Format: PDF-T = digital erzeugtes PDF mit Textebene; PDF-S = Scan (Bild, OCR nötig); DOCX; E-Mail; JSON (digitale Antragsstrecke Minzia); HS = handschriftlich (Scan).

| Nr. | Dokumenttyp | Inhalt (Kernelemente) | Umfang | Format | Sprache/Varianten | Phase |
|---|---|---|---|---|---|---|
| D01 | Offerte / Angebot | Produkt, Summe, Laufzeit, Prämie brutto/netto, Beispielrechnung (garantiert / Überschuss-Szenarien), Gültigkeit | 2–6 S. | PDF-T | DE, CH-DE (ss statt ß, CHF), FR/IT für CH optional (5–10 %) | A |
| D02 | Beratungsprotokoll / Beratungsdokumentation | Bedarf, Wünsche, Empfehlung, Begründung, Verzichtserklärung; DE § 61/62 VVG; CH Art. 3 Info | 2–4 S. | PDF-S, teils HS | DE/CH | A |
| D03 | Antragsformular Leben | VN, VP, BB, Produkt, Summe, Laufzeit, Zahlweise, Bezugsrecht, Vorversicherungen, Beruf, Einkommen, Unterschriften | 4–8 S. | PDF-S (Altbestand), PDF-T, JSON (Minzia) | 4 Formulargenerationen (1985, 1995, 2008, 2020) | B |
| D04 | Gesundheitsfragebogen | 12–25 Fragen (Grösse/Gewicht, Rauchen, Alkohol, Krankheiten 5/10 Jahre, Medikamente, Klinikaufenthalte, Arbeitsunfähigkeit, HIV-Test, Familienanamnese, Sport), Freitextfelder, Arztadresse | 2–4 S. | PDF-S/HS (alt), JSON/PDF-T (neu) | Fragenkatalog unterscheidet sich je Generation → Stolperstein | B |
| D05 | Einwilligungen (Datenschutz, Schweigepflichtentbindung, Einwilligung versicherte Person, GwG-Identifikation) | Erklärungstext, Unterschrift, Datum | 1–2 S. | PDF-S | DE: § 213 VVG-Einwilligung; CH: DSG | B |
| D06 | Ärztliches Zeugnis / Attest (Hausarzt) | Anamnese, Befund, Diagnosen mit ICD-10, Medikation, Laborwerte, Prognose, Arztstempel | 2–4 S. | PDF-S, teils HS | Arztjargon, Abkürzungen (RR, BZ, HbA1c, Z. n.) | C, I |
| D07 | Grosser Untersuchungsbericht (Vertrauensarzt) | strukturierte Untersuchung (Herz, Lunge, Blutdruck, EKG, Urin, Labor), Summenabhängig | 4–8 S. | PDF-S | | C |
| D08 | Laborbefund | Blutbild, Lipide, Leberwerte, HbA1c, Kreatinin, Cotinin, HIV, Referenzbereiche | 1–3 S. | PDF-T/PDF-S | Tabellen, Einheiten mmol/l vs. mg/dl (CH vs. DE) | C, I |
| D09 | Facharztbericht / Klinikentlassungsbericht | Diagnosen, Verlauf, Therapie, Empfehlung | 2–10 S. | PDF-S | | C, I |
| D10 | Underwriting-Votum (intern) | Entscheid, Begründung, verwendete Richtlinie/Tabelle, Zuschlag, Ausschluss, Prüfer, Datum, RV-Hinweis | 1–2 S. | PDF-T / DOCX | intern, teils Stichworte | C |
| D11 | Gegenofferte / Annahmeerklärung mit Zuschlag | neue Prämie, Zuschlagsbegründung (allgemein), Ausschlusstext, Annahmefrist | 1–2 S. | PDF-T | | C/D |
| D12 | Ablehnungsschreiben | Ablehnung ohne medizinische Details, Hinweis auf Arztauskunft | 1 S. | PDF-T | | C |
| D13 | Police / Versicherungsschein | Policennummer, Parteien, Tarif, Summe, Beginn/Ablauf, Prämie, Zahlweise, Bezugsrecht, Überschussverwendung, Klauseln, Dynamik; DE: Widerrufsbelehrung | 2–5 S. | PDF-S (alt, mit Firmenlogo "Pfefferminz"), PDF-T (neu) | Layout 5 Generationen | D |
| D14 | Nachtrag zur Police | Änderungsinhalt (Zuschlag, Ausschluss, Bezugsrecht, Summe, Beitragsfreistellung, Dynamik-Erhöhung) | 1–2 S. | PDF-T/S | | D, E, F |
| D15 | AVB (Allgemeine Versicherungsbedingungen) | siehe Kap. 6.1 | 12–40 S. | PDF-T | je Tarifgeneration + Land | D |
| D16 | Tarifbestimmungen / Besondere Bedingungen (Zusatzbausteine) | siehe Kap. 6.2 | 4–15 S. | PDF-T | | D |
| D17 | Produktinformationsblatt / Basisinformationsblatt (DE), Kundeninformation (CH) | Kurzübersicht Produkt, Kosten, Risiken | 2–4 S. | PDF-T | ab 2008 DE, ab 2018 BIB | D |
| D18 | Jährliche Standmitteilung (DE § 155 VVG) / Vorsorgeausweis-Brief (CH) | Deckungskapital, Rückkaufswert, beitragsfreie Summe, Überschussguthaben, Ablaufprognose, garantierte Leistungen | 2–4 S. | PDF-T (ab 2008), PDF-S (davor) | Layout je Generation | E |
| D19 | Überschussmitteilung / Deklaration | zugeteilter Überschuss, Zinssatz, Schlussüberschussanwartschaft | 1–2 S. | PDF-T | | E |
| D20 | Dynamik-Ankündigung / Erhöhungsnachtrag | Erhöhungssatz, neue Summe/Prämie, Widerspruchsfrist | 1–2 S. | PDF-T | DE 3–5 % oder Inflationsdynamik | E |
| D21 | Mahnung (1. Mahnung, qualifizierte Mahnung, Ruhen/Kündigung) | Rückstand, Frist, Rechtsfolgen (§ 38 VVG DE / Art. 20 VVG CH) | 1 S. | PDF-T | | E |
| D22 | Bezugsrechtsänderung (Kundenschreiben + Bestätigung) | alte/neue Bezugsberechtigte, widerruflich/unwiderruflich, Quoten, Unterschrift VN (und VP bei DE?) | 1–2 S. | HS, E-Mail, PDF-T | oft unklar formuliert → Stolperstein | E |
| D23 | Abtretungs-/Verpfändungsanzeige (Bank) | Abtretung der Ansprüche an Bank, Kreditnummer | 1–2 S. | PDF-S | | E |
| D24 | Beitragsfreistellungs-/Änderungsantrag und Berechnung | Wunsch, Berechnung beitragsfreie Summe, Hinweise | 1–3 S. | PDF-T, HS | | F |
| D25 | Kündigungsschreiben und Rückkaufsberechnung | Kündigung durch VN (formlos, oft E-Mail); Berechnung: Deckungskapital, Stornoabzug, Überschuss, Steuer, Auszahlungsbetrag | 1–3 S. | E-Mail, HS, PDF-T | | G |
| D26 | Steuerbescheinigung (DE Kapitalertragsteuer, CH 3a-Bescheinigung, Rentenbezugsmitteilung) | steuerpflichtiger Ertrag, Abzüge | 1 S. | PDF-T | | G, H, J |
| D27 | Ablaufankündigung / Optionsschreiben / Ablaufabrechnung | Ablaufleistung, Optionen, Fristen | 1–3 S. | PDF-T | | H |
| D28 | Leistungsantrag Todesfall | Angaben Verstorbener, Todesdatum/-ort/-ursache, Anspruchsteller, Bankverbindung, Erklärungen | 2–4 S. | PDF-S/HS | | I |
| D29 | Sterbeurkunde / Todesschein | Standesamt/Zivilstandsamt, Name, Geburtsdatum, Todesdatum/-ort, Registernummer | 1 S. | PDF-S | DE (Standesamt), CH (Zivilstandsamt, kantonale Layouts), Ausland mit Übersetzung/Apostille | I |
| D30 | Ärztliche Todesbescheinigung (Todesursache) | Todesart (natürlich/nicht natürlich/ungeklärt), Grundleiden, unmittelbare Todesursache, ICD-10 | 1–2 S. | PDF-S/HS | DE vertraulicher Teil; CH Todesbescheinigung | I |
| D31 | Erbschein (DE) / Erbbescheinigung (CH) | Erben mit Quoten, Nachlassgericht/Behörde | 1–2 S. | PDF-S | | I |
| D32 | Leistungsantrag EU/BU | Beruf, Tätigkeit (Stunden, Tätigkeiten in %), Erkrankung, Ärzte, Arbeitgeber, IV/DRV-Antrag, Einkommen | 10–20 S. | PDF-S/HS | umfangreich, Freitext | I |
| D33 | Gutachten (medizinisch) | Fragestellung, Anamnese, Befund, Beurteilung, Grad EU/BU, Prognose | 8–25 S. | PDF-T/S | | I |
| D34 | IV-Verfügung (CH) / Rentenbescheid DRV (DE) | IV-Grad, Rentenbeginn, Berechnung | 3–8 S. | PDF-S | | I |
| D35 | Leistungsentscheid (Anerkennung / Ablehnung / Teilanerkennung / Vergleich) | Begründung, Rechtsgrundlage (AVB-§), Betrag, Beginn, Nachprüfungsvorbehalt, Rechtsbehelf | 2–4 S. | PDF-T | | I |
| D36 | Korrespondenz mit Hinterbliebenen / Anspruchstellern | Nachfragen, Unterlagenanforderung, Zwischenbescheid, emotional gefärbte Kundenschreiben, Rückfragen zu Bezugsrecht | 0.5–2 S. je Schreiben, Threads 2–10 Schreiben | E-Mail, HS, PDF-T | | I |
| D37 | Beschwerdebrief / Ombudsstellen-Eingabe | Beschwerdegrund (Dauer, Ablehnung, Rückkaufswert, Überschusshöhe, Beratung), Forderung, Fristsetzung; Antwort des Versicherers; Ombudsmann-Schreiben (DE Versicherungsombudsmann e. V., CH Ombudsman Privatversicherung) | 1–4 S. | HS, E-Mail, PDF-T | Ton von sachlich bis wütend | E, G, I |
| D38 | Vermittlerkorrespondenz / Maklerschreiben | Vermittlungsauftrag, Nachfragen, Courtage | 1–2 S. | E-Mail | | B–I |
| D39 | Interne Aktennotiz / Telefonnotiz | Gesprächsinhalt, Vereinbarungen | 0.3–1 S. | Freitext (System) | Stichworte, Abkürzungen | alle |
| D40 | Rückversicherer-Korrespondenz (fakultativ) | Anfrage, Votum, Anteil | 1–2 S. | PDF-T/E-Mail | Englisch teilweise | C, I |
| D41 | Lebensbescheinigung (Rentenbezug) | Bestätigung Gemeinde/Notar, Datum | 1 S. | PDF-S | jährlich | J |
| D42 | Migrationsprotokoll / Datenblatt PALAS-Auszug | Host-Ausdruck mit Codes, Feldkürzeln, fixen Spalten | 1–3 S. | Text (fixed width) | didaktisch für Legacy-Extraktion | E |

Empfohlene Dokumentmengen pro Vertrag: Neugeschäft P1 (digital) 4–6 Dokumente; Altvertrag P2 mit 25 Jahren Laufzeit 10–25 Dokumente (Standmitteilungen nicht jedes Jahr generieren, sondern 3–5 Stichjahre); Leistungsfall Tod +5–10; Leistungsfall EU/BU +8–15.

---

## 5. Datenelemente (strukturiert)

### 5.1 Entitätenmodell (Überblick)

```
Partner (1..n Rollen) ──< Vertragsrolle >── Vertrag ──< Deckung/Baustein
                                             │            │
                                             ├──< Bezugsrecht (Historie)
                                             ├──< Risikoprüfung ──< Gesundheitsangabe
                                             ├──< Vertragsereignis (Historie)
                                             ├──< Zahlung (Prämie, Auszahlung)
                                             ├──< Wertstand (jährlich)
                                             └──< Leistungsfall ──< Leistungsdokument / Nachweis
Tarif (Stammdaten) ──< Vertrag
Vermittler ──< Vertrag
Dokument (Metadaten) ──> Vertrag / Leistungsfall / Partner
```

### 5.2 Vertrag

| Feld | Typ | Wertebereich | Beispiel | CH/DE-Hinweis |
|---|---|---|---|---|
| policen_nr | string | PALAS: 9-stellig numerisch "L" + Land + Nr (z. B. LCH0012345678); mint-core: UUID-ähnlich "MZ-2021-000123"; PZ: "PZ-CH-2025-00001" | LCH0018834712 | Nummernkreise pro System → Stolperstein Zusammenführung |
| land | enum | CH, DE | CH | |
| system_quelle | enum | PALAS, MINTCORE, PZ | PALAS | |
| produkt_code | enum | P1, P2, P3 | P2 | |
| tarif_code | string | siehe Tab. 1.3 (PK-95, PL-2012-U, MZ-R-2020, …) | PK-95 | Suffix -U Unisex DE |
| tarifgeneration_jahr | int | 1985–2025 | 1995 | |
| variante | enum | KLASSISCH, FONDS_GARANTIE, FONDS | KLASSISCH | |
| vorsorgeform | enum | 3A, 3B, PRIVAT, BASIS | 3A | nur CH: 3A/3B; DE: PRIVAT/BASIS |
| antragsdatum | date | | 1995-03-14 | |
| versicherungsbeginn | date | | 1995-04-01 | häufig Monatsanfang; Rückdatierung DE Dez. 2004 |
| ablaufdatum | date | | 2030-04-01 | |
| laufzeit_jahre | int | 5–45 | 35 | |
| status | enum | ANTRAG, IN_KRAFT, GEMAHNT, RUHEND, BEITRAGSFREI, STORNIERT, ABGELAUFEN, LEISTUNGSFALL, RENTENBEZUG, ABGELEHNT | IN_KRAFT | PALAS: numerische Statuscodes 01–12 |
| status_seit | date | | 2019-01-01 | |
| waehrung | enum | CHF, EUR, DEM (Altbestand vor Umstellung, historisch) | CHF | DE-Verträge vor 1999: Ursprungswährung DEM, umgestellt 2002 |
| versicherungssumme_tod | decimal | 10'000–2'000'000 | 150000.00 | krumme DM-Umrechnungen |
| versicherungssumme_erleben | decimal | 0 oder = Tod (klassisch gemischt) | 150000.00 | |
| summenverlauf | enum | KONSTANT, LINEAR_FALLEND, ANNUITAET | KONSTANT | |
| praemie_tarif | decimal | | 412.50 | DE: Tarifbeitrag |
| praemie_zahl | decimal | | 355.00 | DE: Zahlbeitrag nach Überschussverrechnung |
| zahlweise | enum | MONATLICH, VIERTELJ, HALBJ, JAEHRLICH, EINMAL | JAEHRLICH | Ratenzuschlag DE 2–5 % |
| zahlungsweg | enum | LSV, SEPA, RECHNUNG, ESR/QR | SEPA | CH: LSV+/QR-Rechnung; DE: SEPA |
| dynamik_art | enum | KEINE, PROZENT, INFLATION, GEHALT | PROZENT | |
| dynamik_satz | decimal | 0–10 % | 3.0 | |
| dynamik_widersprueche | int | 0–3 | 2 | nach 3 Widersprüchen in Folge erlischt Dynamik (DE typisch) |
| ueberschussverwendung | enum | VERRECHNUNG, ANSAMMLUNG, BONUS, FONDS, TODESFALLBONUS | ANSAMMLUNG | |
| garantiezins | decimal | 0.25–4.0 % | 4.0 | |
| deckungskapital_aktuell | decimal | | 98450.20 | |
| rueckkaufswert_aktuell | decimal | | 96120.00 | |
| ueberschussguthaben | decimal | | 12340.15 | |
| beitragsfreie_summe | decimal | | 121000.00 | |
| abtretung_kz | bool | | false | |
| abtretung_glaeubiger | string | | Kantonalbank Muster | |
| rv_anteil_pct | decimal | 0–80 | 0 | |
| vermittler_id | string | | VM-0417 | |
| vertriebskanal | enum | AUSSENDIENST, MAKLER, BANK, ONLINE, DIREKT | MAKLER | |
| erstellt_am / geaendert_am | timestamp | | | PALAS ohne Zeitzone |

### 5.3 Partner und Rollen

| Feld | Typ | Wertebereich | Beispiel | CH/DE-Hinweis |
|---|---|---|---|---|
| partner_id | string | | PT-000123 | über beide Systeme vereinheitlicht, mit Dubletten (Stolperstein) |
| rolle | enum | VN (Versicherungsnehmer), VP (versicherte Person), BB (Bezugsberechtigter), ZAHLER, ANSPRUCHSTELLER, VERMITTLER, GLAEUBIGER | VN | VN = VP in 85 %; Über-Kreuz (VN ≠ VP) DE 10 % |
| anrede / geschlecht | enum | M, W, D, UNBEKANNT; PALAS 1/2 | W | DE Unisex-Tarif trotzdem Geschlecht erfasst |
| name, vorname | string | synthetisch (Namensgenerator, regionale Verteilung CH-DE/FR/IT, DE) | Aebischer, Ruth | Umlaute, ß vs. ss, Doppelnamen |
| geburtsdatum | date | 1930–2007 | 1968-07-22 | Alter bei Antrag 18–65 |
| geburtsort_land | string | | CH | |
| nationalitaet | string ISO | | CH, DE, IT, TR, … | |
| zivilstand | enum | LEDIG, VERHEIRATET, EINGETR_PARTNERSCHAFT, GESCHIEDEN, VERWITWET | VERHEIRATET | Änderungen relevant für 3a-Bezugsrecht |
| adresse (strasse, plz, ort, land) | struct | synthetische Adressen; CH 4-stellige PLZ, DE 5-stellige | 8004 Zürich / 50667 Köln | Adresshistorie mit Umzügen |
| ahv_nr / steuer_id | string | CH 756.XXXX.XXXX.XX (Prüfziffer gültig, synthetisch); DE Steuer-ID 11-stellig | 756.1234.5678.97 | Format-Erkennung |
| sozialversicherungs_nr_de | string | optional für BU-Koordination | | |
| beruf | string + code | Freitext + Berufsgruppe 1–5 | Elektromonteur / BG 3 | Freitext variiert (Elektriker, Elektromonteur, Elektroinstallateur) |
| erwerbsstatus | enum | ANGESTELLT, SELBSTAENDIG, NICHT_ERWERBSTAETIG, PENSIONIERT, STUDENT | ANGESTELLT | |
| jahreseinkommen | decimal | | 92000 | für Summenplausibilität |
| raucher_status | enum | NIE, EX (> 12 Monate), RAUCHER; Menge/Tag | EX | Wechsel im Zeitverlauf |
| groesse_cm / gewicht_kg / bmi | int / decimal | | 178 / 92 / 29.0 | Messwerte im Fragebogen vs. Arztbericht abweichend |
| kontakt (email, telefon) | string | synthetisch | | |
| sprache | enum | DE, FR, IT, EN | DE | CH-Korrespondenz FR/IT 5–10 % |
| pep_kz / sanktionslisten_check | bool / date | | false | GwG |
| todesdatum | date | | | nur bei Leistungsfall |
| datenschutz_einwilligung_datum | date | | | |

### 5.4 Bezugsrecht (Historie)

| Feld | Typ | Wertebereich | Beispiel | Hinweis |
|---|---|---|---|---|
| bezugsrecht_id | string | | BR-000451-03 | laufende Nummer je Vertrag (Version) |
| gueltig_von / gueltig_bis | date | | 2012-05-01 / offen | |
| leistungsart | enum | TOD, ERLEBEN, RENTE | TOD | getrennte Bezugsrechte für Tod und Erleben |
| bezugsart | enum | NAMENTLICH, EHEGATTE, KINDER, GESETZL_ERBEN, 3A_GESETZLICH, VN_SELBST, GLAEUBIGER | NAMENTLICH | "Ehegatte" ohne Namen → wer ist bei Scheidung gemeint? (DE BGH: der zum Zeitpunkt der Erklärung; Stolperstein) |
| widerruflich | bool | | true | unwiderruflich nur mit Zustimmung BB änderbar |
| quote_pct | decimal | Summe je Leistungsart = 100 | 50 | Quoten fehlen oft in Altverträgen |
| begünstigte_partner_id | string | | PT-000987 | |
| freitext_original | string | wörtlicher Text der Erklärung | "meine Frau und die Kinder zu gleichen Teilen" | Extraktions-Übung |
| quelle_dokument_id | string | | DOC-… | |
| erfasst_durch | string | | | |

### 5.5 Risikoprüfung und Gesundheitsangaben

| Feld | Typ | Wertebereich | Beispiel | Hinweis |
|---|---|---|---|---|
| rp_id | string | | RP-2021-04455 | |
| rp_datum_start / _ende | date | | | Dauer = Kennzahl |
| rp_art | enum | GESUNDHEITSFRAGEN, AERZTL_ZEUGNIS, GROSSE_UNTERSUCHUNG, LABOR, FINANZ, TELE_UW | GESUNDHEITSFRAGEN | summenabhängig (Kap. 6.3) |
| entscheid | enum | N, Z, A, R, X | Z | Kap. 2.3 |
| zuschlag_pct | int | 0, 25, 50, 75, 100, 150, 200, 300 | 50 | in % der Risikoprämie |
| zuschlag_promille | decimal | 0–10 ‰ Summe p. a. | 2.0 | Berufs-/Sportzuschlag |
| ausschluss_codes | list | z. B. EX-WS (Wirbelsäule), EX-PSY, EX-MOTO, EX-KLETTER | [EX-WS] | mit Klauseltext |
| zurueckstellung_bis | date | | | |
| ablehnungsgrund_code | enum | MED, FIN, BERUF, MORAL, SUMME | MED | |
| prüfer_id / prüfstufe | string / enum | AUTOMAT, SACHBEARBEITER, ARZT, RV | AUTOMAT | Minzia: 70 % automatisch |
| regelwerk_version | string | z. B. ARL-2020-v3 (Annahmerichtlinie) | | RAG-Bezug |
| begründung_freitext | string | intern | "BMI 31, Hypertonie medikamentös eingestellt, RR 140/90; Tabelle B3 → +50 %" | |
| rv_votum | enum | ZUSTIMMUNG, MIT_AUFLAGE, ABLEHNUNG | | |

Gesundheitsangabe (1..n je Risikoprüfung, aus Fragebogen D04):

| Feld | Typ | Wertebereich | Beispiel | Hinweis |
|---|---|---|---|---|
| frage_nr / frage_text_version | string | Fragenkatalog je Formulargeneration | F07 / GF-2020 | Fragen nicht 1:1 zwischen Generationen mappbar |
| antwort_jn | bool | | true | |
| diagnose_icd10_gruppe | string | dreistellig, keine Vollcodes (Datensparsamkeit) | I10 (Hypertonie), E11 (Diabetes Typ 2), F32 (Depression), C50 (Mammakarzinom), M54 (Rückenschmerz), J45 (Asthma) | Auswahl von ca. 40 Diagnosen mit Häufigkeitsverteilung |
| diagnose_freitext | string | Kundenformulierung | "Bluthochdruck, Tabletten" | uneinheitlich, Tippfehler |
| erstdiagnose_datum | date (Monat/Jahr) | | 2018-03 | Abgleich mit Antragsdatum |
| behandlung_status | enum | ABGESCHLOSSEN, LAUFEND, KONTROLLE | LAUFEND | |
| medikation | string | generische Wirkstoffnamen | Ramipril 5 mg | |
| arzt_id (synthetisch) | string | | ARZT-0112 | Praxisnamen fiktiv |
| arbeitsunfaehigkeit_tage_5j | int | | 0 | |
| quelle | enum | FRAGEBOGEN, ARZTBERICHT, LABOR, LEISTUNGSAKTE | FRAGEBOGEN | mehrere Quellen → Widersprüche |
| sensitivitaet | enum | GESUNDHEIT (immer) | | Kennzeichnung für Zugriffssteuerung im Kurs |

Datenschutz-Hinweise für die synthetische Darstellung von Gesundheitsdaten:

| Massnahme | Beschreibung |
|---|---|
| Keine Echtpersonen | Gesundheitsprofile werden aus einer Diagnose-Bibliothek (ca. 40 Diagnosen, altersabhängige Prävalenzen) zufällig kombiniert; keine Realdaten, keine echten Arztnamen oder Praxisadressen |
| Codierung auf Gruppenebene | ICD-10 dreistellig; keine seltenen Erkrankungen (< 1:10'000), die in Kombination mit Alter/Ort re-identifizierend wirken könnten |
| Trennung von Identität und Gesundheit | Gesundheitsangaben tragen nur rp_id, nicht direkt partner_id; Verknüpfung über Vertrag (simuliert Pseudonymisierung) |
| Kennzeichnung | Feld sensitivitaet und Dokument-Tag "GESUNDHEIT"; Übung: Zugriffsregeln für KI-Systeme (wer darf was sehen), Löschfristen (DE: 10 Jahre nach Vertragsende; CH: 10 Jahre gemäss OR Aufbewahrung) |
| Datensparsamkeit in Freitext | Arztberichte enthalten nur das für Underwriting Nötige; bewusst 10 % "übervollständige" Berichte als Stolperstein (Zweckbindung) |
| Klarer Hinweis im Datensatz | jedes Dokument mit Fusszeile "Synthetische Lehrdaten – fiktiv" |

### 5.6 Tarif (Stammdaten)

| Feld | Typ | Wertebereich | Beispiel |
|---|---|---|---|
| tarif_code | string | Tab. 1.3 | PL-2012-U |
| produkt | enum | P1, P2, P3, Z1 | P2 |
| land | enum | CH, DE | DE |
| verkauf_von / _bis | date | | 2012-01-01 / 2014-12-31 |
| rechnungszins | decimal | | 1.75 |
| sterbetafel | string | | DAV 2008 T |
| unisex | bool | | true |
| avb_version | string | | AVB-DE-2012 |
| tarifbestimmung_version | string | | TB-DE-P2-2012 |
| abschlusskosten_promille | decimal | 25–40 ‰ Beitragssumme | 40 |
| verwaltungskosten_pct | decimal | 2–6 % Prämie | 4.0 |
| stornoabzug_regel | string | | "1 % des Deckungskapitals, max. 250" |
| mindestsumme / hoechstsumme | decimal | | 10000 / 2000000 |
| eintrittsalter_min / _max | int | | 18 / 65 |
| endalter_max | int | | 75 |
| ueberschusssystem | string | | Bonussumme |
| suizidfrist_jahre | int | 1–3 | 3 |
| berufsgruppen_faktor | json | BG1–BG5 → Faktor | {"BG1":1.0,"BG3":1.4} |

### 5.7 Leistungsfall

| Feld | Typ | Wertebereich | Beispiel | Hinweis |
|---|---|---|---|---|
| lf_id | string | | LF-2024-01877 | |
| policen_nr | string | | | |
| leistungsart | enum | TOD, EU, BU, PRAEMIENBEFREIUNG, ERLEBEN, VORGEZOGEN_TERMINAL, RENTE_TOD_GARANTIEZEIT | TOD | |
| ereignisdatum | date | | 2024-02-11 | Tod, EU-Beginn |
| meldedatum | date | | 2024-02-20 | Meldeverzug als Feature |
| meldekanal | enum | BRIEF, PORTAL, TELEFON, VERMITTLER, EMAIL | | |
| anspruchsteller_partner_id | string | | | |
| todesursache_icd10_gruppe | string | I21, C34, V89 (Verkehr), X60–X84 (Suizid), R99 (ungeklärt) | I21 | |
| todesart | enum | NATUERLICH, UNFALL, SUIZID, GEWALT, UNGEKLAERT | NATUERLICH | |
| todesort_land | string | | CH | Ausland → Apostille |
| vertragsalter_bei_ereignis_monate | int | | 22 | < 36/60 Monate → Nachprüfung |
| anzeigepflicht_prüfung | enum | NICHT_NOETIG, DURCHGEFUEHRT_OK, VERLETZUNG_KAUSAL, VERLETZUNG_NICHT_KAUSAL | | |
| eu_grad_pct | int | 0–100 | 70 | |
| wartefrist_ende | date | | | |
| status | enum | GEMELDET, UNTERLAGEN_OFFEN, PRÜFUNG, ENTSCHEID, AUSGEZAHLT, ABGELEHNT, TEILWEISE, KULANZ, VERGLEICH, RECHTSSTREIT | | |
| entscheid_datum | date | | | |
| entscheid_grund_code | enum | REGULAER, ANZEIGEPFLICHT, SUIZIDFRIST, VERZUG, VERJAEHRT, KEIN_BEZUGSRECHT, BETRUG, KULANZ_K1..K4 | | |
| leistung_garantiert / ueberschuss / schlussueberschuss / gesamt | decimal | | 150000 / 12340 / 8000 / 170340 | |
| abzuege (offene Prämien, Darlehen) | decimal | | | |
| auszahlung_datum | date | | | |
| durchlaufzeit_tage | int | | 41 | |
| betrugsverdacht_kz / betrugsindikatoren | bool / list | Kap. 3.5 | [DISKREPANZ_DIAGNOSE, KURZE_LAUFZEIT] | Labels für Trainings-/Testdaten, im Kursdatensatz teilweise "verborgen" |
| betrug_bestaetigt | bool | Ground Truth | | |
| beschwerde_kz / ombudsstelle_kz | bool | | | |
| sachbearbeiter_id | string | | | |
| dokumente_vollstaendig_am | date | | | |

### 5.8 Zahlungen und Wertstände

| Feld | Typ | Wertebereich | Beispiel | Hinweis |
|---|---|---|---|---|
| zahlung_id | string | | | |
| policen_nr | string | | | |
| zahlungsart | enum | PRAEMIE, DYNAMIK_PRAEMIE, NACHZAHLUNG, RUECKKAUF, ABLAUF, TODESFALL, RENTE, EU_RENTE, RUECKERSTATTUNG, STORNOGEBUEHR | PRAEMIE | |
| faelligkeit / zahldatum | date | | | Verzugstage = Feature für Churn |
| betrag / waehrung | decimal / enum | | 355.00 CHF | |
| richtung | enum | EIN, AUS | EIN | |
| zahlungsstatus | enum | OFFEN, BEZAHLT, GEMAHNT_1, GEMAHNT_2, RUECKLASTSCHRIFT, STORNIERT | | Rücklastschriften-Häufung → Churn |
| konto_iban_masked | string | synthetisch, letzte 4 Stellen | CH93 **** 1234 | |
| konto_inhaber_partner_id | string | | | Zahler ≠ VN → Hinweis |
| Wertstand: stichtag, deckungskapital, rueckkaufswert, ueberschuss, fondswert, garantierte_ablaufleistung, prognose_ablauf_1/2/3 | decimal | jährlich | | Basis für Standmitteilung D18 |

### 5.9 Vertragsereignis (Historie) und Churn-Features

| Feld | Typ | Wertebereich | Hinweis |
|---|---|---|---|
| ereignis_typ | enum | ANTRAG, POLICIERUNG, DYNAMIK_ERHOEHUNG, DYNAMIK_WIDERSPRUCH, ADRESSAENDERUNG, BANKAENDERUNG, BEZUGSRECHTSAENDERUNG, MAHNUNG, RUECKLASTSCHRIFT, BEITRAGSFREISTELLUNG, TEILRUECKKAUF, DARLEHEN, ABTRETUNG, AUSKUNFT_RUECKKAUFSWERT, BESCHWERDE, KUENDIGUNG, WIDERRUF_KUENDIGUNG, ABLAUF, LEISTUNGSFALL, VERMITTLERWECHSEL | Auskunftsanfrage Rückkaufswert = starker Churn-Prädiktor |
| ereignis_datum | date | | |
| kanal | enum | | |
| freitext | string | | |
| Abgeleitete Churn-Features (Empfehlung) | | Vertragsalter, Zahlweise, Verzugstage 12 M., Dynamik-Widersprüche, Anzahl Auskunftsanfragen, Vermittlerwechsel, Zinsdifferenz Garantiezins vs. Markt, Rückkaufswert/Beitragssumme, Alter VN, Beschwerde, Bankwechsel, Scheidung | Ziel: Storno innerhalb 12 Monaten (Anteil 4–7 % p. a.; Altverträge mit 4 % Garantie < 1 %) |

---

## 6. Regelwerke Leben

### 6.1 Allgemeine Versicherungsbedingungen (AVB)

Je Tarifgeneration und Land eine Fassung (empfohlen: 5 Generationen × 2 Länder = 10 AVB-Dokumente, wovon 3 vollständig ausformuliert und 7 als Varianten mit gezielten Abweichungen).

| Abschnitt | Inhalt | Umfang | CH-Besonderheit | DE-Besonderheit |
|---|---|---|---|---|
| § 1 Vertragsgrundlagen | Parteien, Police, Antrag, Rangfolge der Dokumente | 0.5 S. | Verweis VVG CH, Kundeninformation Art. 3 | Verweis VVG DE, Produktinformationsblatt |
| § 2 Versicherte Leistungen | Todesfall, Erleben, Rente, Kapitalwahlrecht, Rentengarantie | 1–2 S. | | |
| § 3 Beginn und Ende des Schutzes, vorläufige Deckung | Beginn, vorläufiger Versicherungsschutz (Unfalltod bis Policierung), Ende | 0.5 S. | | Widerrufsrecht 30 Tage § 152 |
| § 4 Anzeigepflicht | Fragen, Folgen der Verletzung, Fristen | 1 S. | Art. 4–8 VVG: Rücktritt/Kündigung 4 Wochen ab Kenntnis, Kausalität | §§ 19–22: 5 Jahre / 10 Jahre bei Arglist, Belehrungserfordernis |
| § 5 Ausschlüsse | Suizid (Wartefrist), Krieg, innere Unruhen, Kernenergie, Tötung durch Bezugsberechtigten, Extremsport (Altverträge: Flugrisiko!) | 1 S. | Suizidfrist AVB 1–3 J. (PK-85: 1 Jahr, ab PL-2012: 3 Jahre) | § 161: 3 Jahre gesetzlich |
| § 6 Prämien | Fälligkeit, Zahlweise, Ratenzuschläge, Verzug, Mahnung, Ruhen | 1 S. | Art. 20 VVG: Mahnung mit 14-Tage-Frist, Ruhen | § 37/38 VVG: Erst-/Folgeprämie, qualifizierte Mahnung 2 Wochen |
| § 7 Überschussbeteiligung | Grundsätze, Quellen, Verwendung, Schlussüberschuss | 1–2 S. | Überschussplan, jährliche Deklaration | § 153 VVG, MindZV, Bewertungsreserven (ab 2008) |
| § 8 Beitragsfreistellung, Rückkauf, Kündigung | Voraussetzungen, Berechnung, Stornoabzug, Mindestwerte | 1–2 S. | Art. 90 VVG (Umwandlung/Rückkauf nach 3 Jahren); 3a Vorbezugsgründe | § 165, § 169 (Rückkaufswert = Deckungskapital, Abschlusskosten 5 Jahre), § 168 Kündigung |
| § 9 Bezugsrecht, Abtretung, Verpfändung | Einräumung, Widerruf, Form, Ausland | 1 S. | Art. 76–78, 3a Art. 2 BVV 3 | §§ 159–160, Anzeige an Versicherer § 13 |
| § 10 Leistungsfall | Anzeige, Nachweise, Fälligkeit, Auszahlung, Verzug | 1 S. | Art. 38–41 VVG; Fälligkeit 4 Wochen nach Unterlagen | § 14 VVG, Abschlagszahlung |
| § 11 Dynamik | Erhöhung, Widerspruch, Erlöschen | 0.5 S. | | |
| § 12 Nachversicherungsgarantie / Optionen | Ereignisse, Fristen, Limiten | 0.5 S. | unterschiedlich zwischen Minzia-AVB und Pfefferminz-AVB | |
| § 13 Verjährung, Gerichtsstand, anwendbares Recht, Ombudsstelle | | 0.5 S. | 5 Jahre (rev. VVG), Ombudsman Privatversicherung | 3 Jahre BGB, Versicherungsombudsmann |
| § 14 Datenschutz, Mitteilungen, Sprache | | 0.5 S. | DSG CH | DSGVO, § 213 VVG |
| Anhang | Tabelle beitragsfreie Summen / Rückkaufswerte (Altbestand), Glossar | 2–10 S. | | |

Umfang gesamt: PK-85/95: 12–16 Seiten, eng gesetzt, juristische Sprache; PL-2012/2017: 25–35 Seiten (Transparenzpflichten); MZ-R-2020: 8–10 Seiten "Klartext" mit Beispielen; PZ-2025: 30–40 Seiten mit Länderanhang CH/DE.

### 6.2 Tarifbestimmungen und Besondere Bedingungen

| Regelwerk | Gliederung | Umfang |
|---|---|---|
| Tarifbestimmungen je Produkt/Generation | 1. Rechnungsgrundlagen (Zins, Tafel, Kosten) 2. Eintrittsalter, Laufzeiten, Summengrenzen 3. Prämienberechnung (Formeln vereinfacht, Beispiele) 4. Ratenzuschläge 5. Berufsgruppen und Faktoren 6. Raucher/Nichtraucher-Definition (12 Monate, inkl. E-Zigaretten ab 2017) 7. Dynamik-Regeln 8. Rückkaufs- und Umwandlungstabellen 9. Überschussverwendung je Tarif | 6–15 S. |
| Besondere Bedingungen EU/BU (Z1) | 1. Begriff EU/BU (Definition, Grad, Prognosezeitraum) 2. Wartefrist 3. Anerkenntnis, Befristung 4. Nachprüfung 5. Mitwirkungspflichten 6. Verweisung (abstrakt bis 2008 DE, konkret ab 2008) 7. Koordination/Überentschädigung (CH) 8. Ausschlüsse 9. Ende | 6–10 S. |
| Besondere Bedingungen Fondsgebunden | Fondsauswahl, Switch, Shift, Ablaufmanagement, Garantieniveau, Kosten | 6–8 S. |
| Besondere Bedingungen Nachversicherungsgarantie / Vorgezogene Todesfallleistung | Ereignisse, Fristen, Höchstbeträge, Nachweise | 2–3 S. |
| Besondere Bedingungen Säule 3a (CH) | BVV-3-Konformität, Bezugsrecht, Auszahlungsgründe, Bescheinigungen, Meldung an Steuerbehörde | 3–4 S. |

### 6.3 Risikoprüfungsrichtlinien (Annahmerichtlinien, ARL)

Interne Richtlinie, Versionen ARL-2008, ARL-2015, ARL-2020 (Minzia, automatisiert, Regel-Codes) und ARL-2025 (harmonisiert). Umfang 40–80 Seiten. Gliederung:

| Kapitel | Inhalt | Umfang |
|---|---|---|
| 1. Grundsätze | Zweck, Antiselektion, Gleichbehandlung, Diskriminierungsverbot (Gentests: CH GUMG-Verbot bei Summen < CHF 400'000 Tod / < CHF 40'000 Rente; DE GenDG-Verbot bis EUR 300'000 / 30'000 Jahresrente), Datenschutz | 3 S. |
| 2. Prüfumfang nach Summe und Alter | Tabelle (siehe unten) | 2 S. |
| 3. Medizinische Prüfung: Bewertungssystem | Punktesystem (Debits/Credits): Summe der Zuschlagspunkte → Risikoklasse | 3 S. |
| 4. Tabelle Grösse/Gewicht (BMI) | siehe unten | 2 S. |
| 5. Rauchen / Nikotin | Definition, Cotinin-Test ab Summe X, Raucher-Tarif vs. Zuschlag, E-Zigaretten, Snus (CH) | 1 S. |
| 6. Blutdruck / Herz-Kreislauf | Tabellen RR-Werte × Alter × Behandlung; KHK, Herzinfarkt (Zeit seit Ereignis), Herzinsuffizienz (Ablehnung ab NYHA III) | 5 S. |
| 7. Stoffwechsel | Diabetes Typ 1/2 (HbA1c, Dauer, Komplikationen), Schilddrüse, Adipositas | 4 S. |
| 8. Tumorerkrankungen | je Tumorart: Zurückstellung (1–5 Jahre nach Therapieende), dann Zuschlag degressiv, Ablehnung bei Metastasen | 8 S. |
| 9. Psychische Erkrankungen | Depression (leicht: normal nach 1 Jahr Remission; mittel: +50–100 %; Klinik/Suizidversuch: Zurückstellung 2–5 J. / Ablehnung bei EU), Angst, Sucht (Alkohol: Abstinenz ≥ 3 J.), Burnout | 5 S. |
| 10. Bewegungsapparat | Bandscheibe, Arthrose, Rheuma → v. a. Ausschlussklauseln EU/BU | 3 S. |
| 11. Neurologie, Atemwege, Verdauung, Niere, Infektionen (HIV: Annahme mit Zuschlag bei stabiler Therapie ab ARL-2015; davor Ablehnung → Stolperstein Altbestand) | | 8 S. |
| 12. Berufsrisiken | Berufsgruppen 1–5, Sonderberufe (Pilot, Taucher, Sprengmeister, Militär), Selbständige | 3 S. |
| 13. Freizeitrisiken | Tauchen, Klettern, Motorsport, Fallschirm, Bergsteigen > 4'000 m: Zuschlag ‰ oder Ausschluss | 2 S. |
| 14. Auslandsaufenthalt / Nationalität | Aufenthalt in Risikoländern | 1 S. |
| 15. Finanzielle Prüfung | Summe vs. Einkommen (Faktor 10–20× Jahreseinkommen je Alter), Keyperson, Kreditabsicherung, Geldwäsche | 2 S. |
| 16. Entscheidungskompetenzen | Automat (Regel-Engine) bis Klasse 2 und Summe X; Sachbearbeiter; Gesellschaftsarzt; Rückversicherer | 1 S. |
| 17. Kommunikation | Formulierungen für Gegenofferten, Ablehnungen (keine Diagnosen im Kundenschreiben), Arztauskunft | 2 S. |
| Anhang | Fragebogen-Mapping über Generationen, ICD-10-Kurzliste, Rechenbeispiele | 5 S. |

Prüfumfang nach Versicherungssumme (Todesfall, Alter < 50; ab 50 eine Stufe strenger):

| Summe (CHF/EUR) | Prüfung |
|---|---|
| bis 300'000 | Gesundheitsfragen (Fragebogen) |
| 300'001 – 750'000 | Fragebogen + ärztliches Zeugnis Hausarzt |
| 750'001 – 1'500'000 | + grosse Untersuchung Vertrauensarzt + Labor (inkl. HIV, Cotinin, HbA1c, Lipide) |
| über 1'500'000 | + EKG (Belastung ab 45), Finanzfragebogen, Rückversicherung |
| EU/BU-Rente > 2'500 / Monat | + Facharztbericht bei Vorerkrankungen, Berufsnachweis |

BMI-Tabelle (Auszug; Zuschläge in % der Risikoprämie Todesfall; EU/BU eine Stufe strenger):

| BMI | Alter 18–39 | Alter 40–59 | Alter 60+ | Bemerkung |
|---|---|---|---|---|
| < 17.0 | +50 % / Rückfrage | +50 % | +75 % | Untergewicht: Abklärung Essstörung, Tumor |
| 17.0 – 18.4 | +25 % | +25 % | +50 % | |
| 18.5 – 27.9 | normal | normal | normal | |
| 28.0 – 29.9 | normal | normal | +25 % | |
| 30.0 – 32.9 | +25 % | +25 % | +50 % | ARL-2008: bereits +50 % (Stolperstein Generationen) |
| 33.0 – 35.9 | +50 % | +75 % | +100 % | + Rückfrage Blutdruck, Blutzucker |
| 36.0 – 39.9 | +100 % | +150 % | +200 % | ärztliches Zeugnis obligatorisch |
| 40.0 – 44.9 | +200 % | +250 % | Ablehnung | EU/BU: Ablehnung |
| ≥ 45.0 | Ablehnung | Ablehnung | Ablehnung | |

Rauchen:

| Status | Todesfall | EU/BU |
|---|---|---|
| Nie / Ex > 12 Monate | Nichtrauchertarif | Nichtrauchertarif |
| Ex 1–12 Monate | Rauchertarif | Rauchertarif |
| Raucher ≤ 10/Tag | Rauchertarif (Faktor 1.8–2.2) | Rauchertarif |
| Raucher > 20/Tag | Rauchertarif + 25 % | Rauchertarif + 50 % |
| Nikotin falsch angegeben (Cotinin positiv) | Anzeigepflichtverletzung; Neubewertung, ggf. Ablehnung | dito |

Vorerkrankungen (Auszug der Referenztabelle, ca. 40 Einträge geplant):

| Diagnose (ICD-10) | Todesfall | EU/BU | Zurückstellung | Nachweis |
|---|---|---|---|---|
| Hypertonie, medikamentös eingestellt, RR < 140/90 (I10) | normal bis +25 % | +25 % | – | Fragebogen, ggf. Arztwerte |
| Hypertonie unbehandelt RR ≥ 160/100 | +50 – 100 % | +100 % oder Ausschluss | bis Einstellung | Arztzeugnis |
| Diabetes Typ 2, HbA1c < 7, keine Komplikationen (E11) | +50 – 100 % | +100 – 150 % oder Ablehnung | – | Labor |
| Diabetes Typ 1 (E10) | +100 – 200 % (alters- und dauerabhängig) | Ablehnung (Alt-ARL) / +200 % (ARL-2025) | – | Facharzt |
| Depression, einmalige Episode, remittiert > 1 Jahr (F32) | normal | +50 % oder Ausschluss psychisch | – | Fragebogen |
| Depression, rezidivierend, stationär (F33) | +50 – 100 % | Ablehnung oder Ausschluss | 2 Jahre nach Klinik | Facharzt |
| Suizidversuch | Zurückstellung 3 Jahre, dann +100 % | Ablehnung | 3–5 J. | Facharzt |
| Mammakarzinom Stadium I, Therapie abgeschlossen (C50) | Zurückstellung 2 J., dann +100 % degressiv über 5 J. | Zurückstellung 5 J. | 2–5 J. | Onkologiebericht |
| Melanom in situ (D03) | normal nach 1 Jahr | normal nach 1 Jahr | 1 J. | Histologie |
| Asthma leicht (J45) | normal | normal bis +25 % | – | |
| Bandscheibenvorfall mit OP (M51) | normal | Ausschluss Wirbelsäule oder +50 % | 6 Monate nach OP | Arztbericht |
| Alkoholabhängigkeit, abstinent ≥ 3 J. (F10) | +100 % | Ablehnung / +200 % nach 5 J. | – | Facharzt |
| HIV-Infektion unter Therapie, Viruslast nicht nachweisbar (B24) | ARL-2008: Ablehnung; ARL-2015+: +100 – 200 % | Ablehnung / Einzelfall | – | Facharzt, Labor |
| Herzinfarkt vor > 2 Jahren, EF > 50 % (I21/I25) | +100 – 200 % | Ablehnung | 1 J. | Kardiologe |
| Epilepsie, anfallsfrei > 2 J. (G40) | +25 – 50 % | +50 % / Ausschluss | – | Neurologe |
| Schwangerschaft | normal (ausser Komplikationen) | Zurückstellung bis 3 Monate nach Geburt für EU | – | |

### 6.4 Leistungsprüfungsrichtlinien (LPR)

Interne Richtlinie, Version LPR-2016 (Pfefferminz) und LPR-2025 (harmonisiert), Umfang 30–50 Seiten:

| Kapitel | Inhalt |
|---|---|
| 1. Grundsätze | Zügigkeit, Fairness, Beweislast (Anspruchsteller für Eintritt, Versicherer für Ausschluss), Kulanzkompetenzen (K1 bis CHF/EUR 10'000 Sachbearbeiter, K2 bis 50'000 Teamleiter, K3 bis 250'000 Leiter Leistung, K4 Geschäftsleitung) |
| 2. Todesfall: Standardprozess | Checkliste Unterlagen, Prüfschritte, Sollzeiten, Abschlagszahlung |
| 3. Todesfall: Sonderfälle | Tod < 3/5 Jahre nach Abschluss oder Wiederinkraftsetzung (obligatorische Nachprüfung Anzeigepflicht), Suizid, Tod im Ausland, Verschollenheit (CH: Verschollenerklärung Art. 35 ZGB; DE: Verschollenheitsgesetz), Tod während Mahnung, Tötung durch Bezugsberechtigten, Tod im Rentenbezug |
| 4. Bezugsrechtsprüfung | Entscheidungsbaum: namentlich → Ehegatte (Scheidung?) → Kinder (welche? adoptiert? nachgeboren?) → Erben (Erbschein) → 3a-Kaskade; Minderjährige; Abtretung geht vor; Auslandsdokumente |
| 5. Anzeigepflichtverletzung | Prüfschema: verschwiegene Tatsache? gefragt? erheblich? Frist? Kausalität? Verschuldensgrad (DE: vorsätzlich/grob fahrlässig/leicht fahrlässig → Rücktritt/Kündigung/Anpassung)? Rechtsfolge; Musterschreiben |
| 6. EU/BU-Prüfung | Berufsbild erheben, medizinische Befunde, Grad-Bemessung (Tätigkeitsanteile), Verweisung, Befristung, Nachprüfung, Wiedereingliederung, Vergleiche |
| 7. Betrugsindikatoren (Red Flags) | Liste mit Gewichtung (Kap. 3.5), Eskalation an Special Investigation, HIS-Abfrage (DE), Zusammenarbeit mit Strafverfolgung |
| 8. Kommunikation | Tonalität gegenüber Hinterbliebenen, Fristen für Zwischenbescheide (alle 14 Tage), Beschwerdeprozess, Ombudsstelle |
| 9. Steuer und Meldungen | Erbschaftssteuer-Anzeige DE, kantonale Meldungen CH, Rentenbezugsmitteilung, 3a-Meldung |
| Anhang | Checklisten, Musterschreiben, Entscheidungsbäume, Fristentabelle CH/DE |

### 6.5 Überschussregelungen

| Element | Inhalt | Umfang / Form |
|---|---|---|
| Überschussdeklaration (jährlich, je Land, je Tarifgruppe) | laufender Zinsüberschuss (Gesamtverzinsung = Garantie + Überschuss, z. B. 2025: DE 2.6 % gesamt, CH 2.0 %), Risikoüberschuss (% der Risikoprämie, z. B. 30 % Risikoleben), Kostenüberschuss, Schlussüberschuss (% des Deckungskapitals je Laufzeitjahr), Bewertungsreserven (DE) | 4–8 S., Tabellen nach Tarifgeneration; Historie 2005–2025 als Zeitreihe (fallend von 4.5 % auf 1.5 % und leichter Anstieg ab 2024) |
| Überschussplan / Grundsätze | Quellen, Verteilungsschlüssel, Zuweisungsverfahren (verzinsliche Ansammlung, Bonussumme, Beitragsverrechnung, Fondsanlage), Behandlung bei Rückkauf/Beitragsfreistellung/Leistungsfall | 6–10 S. |
| Überschussmitteilung an Kunden (D19) | individueller Anteil, Kontostand Überschussguthaben | 1–2 S. |
| Rechtsrahmen | DE: § 153 VVG, MindZV (90/90/50), § 139 VAG Rückstellung für Beitragsrückerstattung; CH: FINMA-Rundschreiben Überschussbeteiligung, Überschussfonds, Art. 36 VAG-Transparenz; Legal Quote 90 % nur BVG-Kollektiv | Verweis im Regelwerk |

---

## 7. Didaktik: bewusst eingebaute Stolpersteine

| Nr. | Stolperstein | Beschreibung im Datensatz | Betroffene Use-Cases | Empfohlene Häufigkeit |
|---|---|---|---|---|
| S01 | Unklare Bezugsrechte | "meine Ehefrau" ohne Namen, Scheidung nach Erklärung; "die Kinder" bei Patchwork; Quoten fehlen; Testament widerspricht Police; 3a-Kaskade übersteuert namentliches Bezugsrecht; unwiderrufliches Bezugsrecht ohne Zustimmung geändert | Leistungsfallprüfung, RAG (AVB § 9), Dokumentextraktion | 15 % der Todesfälle |
| S02 | Altverträge mit abweichenden Bedingungen | Suizidfrist 1 Jahr (PK-85) vs. 3 Jahre; abstrakte Verweisung BUZ-2000; Flugrisiko-Ausschluss 1985; Nachversicherungsgarantie nur in Minzia-AVB; Rückkaufswert-Tabellen statt Formel | RAG über Bedingungswerke, Rückkaufsberechnung, Leistungsprüfung | 30 % der Verträge sind PK-85/95/2000 |
| S03 | Widersprüchliche Gesundheitsangaben | Fragebogen "keine Erkrankungen", Arztbericht mit Hypertonie seit 2016; Gewicht 85 kg im Antrag, 98 kg beim Vertrauensarzt 3 Wochen später; Nichtraucher laut Antrag, Cotinin positiv; Erstdiagnosedatum vor Antrag nur in Klinikbericht in der Leistungsakte | Underwriting-Assistenz, Betrugserkennung, Leistungsfall Anzeigepflicht | 12 % der Risikoprüfungen, 25 % der frühen Leistungsfälle |
| S04 | Fragebogen-Generationen | Frage "Waren Sie in den letzten 5 Jahren in ärztlicher Behandlung?" (1995) vs. "in den letzten 10 Jahren wegen folgender Erkrankungen…" (2020); Antwort ist formal korrekt, aber nach neuem Katalog Anzeigepflichtverletzung → keine Verletzung nach altem | Underwriting, Leistungsprüfung, RAG | strukturell |
| S05 | Zwei Bestandssysteme | Geschlecht 1/2 vs. M/F/D; Datum JJJJMMTT vs. ISO; Statuscodes 01–12 vs. Klartext; Tarifcodes PK-95 vs. Migrationscode "PZ-L-M95"; Beträge in Rappen/Cent (Integer) vs. Dezimal; Umlaute in PALAS als "AE/OE/UE" | Datenintegration, Churn-Modell (Feature-Engineering), Extraktion aus PALAS-Auszügen (D42) | strukturell |
| S06 | Währungen und DM-Erbe | DEM-Summen umgerechnet (EUR 25'564.59), CHF-Verträge mit Rappenrundung 0.05, DE-Verträge mit Ratenzuschlag → Prämie in Dokument ≠ Prämie in Datenbank | Extraktion, Plausibilisierung | 20 % der DE-Altverträge |
| S07 | Unisex-Bruch DE 2012 | gleicher Tarifcode, zwei Kalkulationen; Prämienvergleich "warum zahlt Frau X mehr als Herr Y" | Kundenservice-Bot, RAG | alle PL-2012 |
| S08 | CH-Geschlechtertarif vs. DE-Unisex | Cross-Border-Kunde zieht von Köln nach Zürich: Vertrag bleibt DE-Recht; Frage nach "Umstellung" | RAG, Kundenservice | 2 % |
| S09 | Brutto-/Netto-Prämie (Tarif- vs. Zahlbeitrag) | Dokumente nennen mal Tarifbeitrag, mal Zahlbeitrag; Überschussverrechnung ändert sich jährlich | Extraktion, Churn-Features | alle DE P1 |
| S10 | Verzug und Leistungsfall | Tod 3 Tage nach Ablauf der qualifizierten Mahnfrist; Zustellnachweis fehlt; Nachzahlung durch Witwe am Todestag | Leistungsprüfung, Kulanzentscheid | 3 % der Todesfälle |
| S11 | Fingierter Tod mit "guten" Dokumenten | Sterbeurkunde aus Drittstaat mit Apostille, aber Prämien laufen weiter vom Konto des Verstorbenen; Bezugsberechtigter wechselt 2 Monate vor Tod | Betrugserkennung | 1 % |
| S12 | Legitime Sonderfälle, die wie Betrug aussehen | Tod nach 4 Monaten durch Unfall (keine Anzeigepflichtverletzung); Mehrfachversicherung wegen Hausbau plausibel; Ausland-Tod im Urlaub | Betrugserkennung (False Positives) | 3 % |
| S13 | Widerspruch Todesbescheinigung vs. Sterbeurkunde | Datum weicht um 1 Tag ab (Tod um Mitternacht), Namensschreibweise (Müller/Mueller), Geburtsdatum-Zahlendreher | Extraktion, Matching | 5 % |
| S14 | Verjährung und Verschollenheit | Police erst 7 Jahre nach Tod im Nachlass gefunden; Vermisster im Bergunfall ohne Leichnam | Leistungsprüfung, RAG | 0.5 % |
| S15 | EU vs. BU vs. IV-Koordination | CH: IV-Grad 40 %, Vertrag verlangt 25 % → Teilrente, Überentschädigung; DE: DRV-Rente abgelehnt, BU trotzdem anerkannt (andere Definition) | Leistungsprüfung | 20 % der EU/BU-Fälle |
| S16 | Berufsbild-Freitext | "Bauführer" vs. "Polier" vs. "Projektleiter Bau" → unterschiedliche Berufsgruppen und Verweisungslogik | Underwriting, BU-Prüfung | strukturell |
| S17 | Dynamik-Kette | Summe nach 15 Dynamikerhöhungen; Kunde bestreitet eine Erhöhung; Nachträge teils fehlen | Extraktion, Rückkaufsberechnung | 10 % P2 |
| S18 | Abtretung an Bank vergessen | Verpfändung 2009 nie gelöscht; Todesfall 2024, Bank meldet Kredit längst getilgt | Leistungsprüfung, Bezugsrecht | 2 % |
| S19 | Beschwerde mit Halbwissen | Kunde zitiert Standmitteilung falsch, verwechselt Rückkaufswert und beitragsfreie Summe; fordert "Garantiezins 4 % auf alles" | Kundenservice-Bot, RAG, Sentiment | 5 % der Verträge mit Beschwerde |
| S20 | Mehrsprachigkeit | CH-Dokumente FR/IT (Sterbeurkunde Tessin, Arztbericht Lausanne), Ausland-Dokumente EN/TR mit Übersetzung | Extraktion | 7 % CH |
| S21 | OCR-Qualität und Handschrift | Antrag 1995 handschriftlich, Arztstempel über Text, Faxkopien; Ziffernverwechslung 1/7, 0/6 | Extraktion | 40 % Altbestand-Dokumente in schlechter Qualität |
| S22 | Hidden Labels | Betrugs- und Kulanz-Labels nur in separater Ground-Truth-Tabelle; Datensatz für Teilnehmende ohne Labels | Betrugserkennung, Evaluation | strukturell |
| S23 | Datenschutz-Fallen | Arztbericht enthält Angaben zu Familienangehörigen (nicht versichert); Gentest-Ergebnis im Bericht (Verwendung verboten); KI-Prompt könnte Gesundheitsdaten an falsche Rolle ausgeben | Governance-Diskussion, Underwriting | 3 % |
| S24 | Storno-Prädiktoren mit Störsignal | Rückkaufswert-Auskunft, dann doch kein Storno (Scheidungsverfahren, Hypothek); Bankwechsel wegen Bankfusion (kein Churn) | Churn-Vorhersage | strukturell |
| S25 | Regelwerksversion vs. Vertragsdatum | Underwriting 2019 nach ARL-2015, Leistungsprüfung 2025 nach LPR-2025 mit Verweis auf ARL-2025 (strenger/lockerer) → welche Version gilt? | RAG, Leistungsprüfung | 10 % |

### 7.1 Zuordnung Use-Case → benötigte Bausteine

| KI-Use-Case | Produkte | Dokumente | Strukturierte Daten | Regelwerke | Zentrale Stolpersteine |
|---|---|---|---|---|---|
| Underwriting-Assistenz mit Gesundheitsfragen | P1, Z1 | D03, D04, D06, D07, D08, D10, D11 | Risikoprüfung, Gesundheitsangabe, Partner | ARL (BMI, Rauchen, Vorerkrankungen), Tarifbestimmungen | S03, S04, S16, S23, S25 |
| Dokumentextraktion | alle | D03, D13, D18, D22, D29, D30, D32, D42 | Vertrag, Bezugsrecht, Leistungsfall | – | S05, S06, S13, S20, S21 |
| Storno-/Churn-Vorhersage | P2, P3 | D21, D25, D37 | Vertragsereignis, Zahlung, Wertstand | Überschussdeklaration | S09, S17, S24 |
| RAG über Bedingungswerke | alle | D15, D16, D17 (5 Generationen × 2 Länder) | Tarif | AVB, Tarifbestimmungen, Überschussregelungen | S02, S07, S08, S19, S25 |
| Leistungsfallprüfung | P1, P2, Z1 | D28–D36 | Leistungsfall, Bezugsrecht | LPR | S01, S10, S14, S15, S18 |
| Betrugserkennung | P1, Z1 | D28–D34, D36 | Leistungsfall, Zahlung, Risikoprüfung | LPR Kap. 7 | S11, S12, S22 |

---

## 8. Umsetzungsempfehlungen (Mengengerüst und Reihenfolge)

| Schritt | Inhalt | Ergebnis |
|---|---|---|
| 1 | Tarif-Stammdaten und Regelwerke (AVB PK-95, PL-2012, MZ-R-2020, PZ-2025 vollständig; übrige als Delta), ARL-2020/2025, LPR-2025, Überschussdeklarations-Zeitreihe | Grundlage für RAG und für konsistente Datengenerierung |
| 2 | Partner-Generator (CH/DE, Sprachen, Dubletten) und Vertragsgenerator (2'000–5'000 Verträge, Verteilung: P1 40 %, P2 35 %, P3 20 %, Z1 als Baustein bei 25 %) | Strukturierte Basistabellen |
| 3 | Ereignis- und Zahlungshistorie (Dynamik, Mahnungen, Änderungen, Stornos) mit Churn-Ground-Truth | Zeitreihen für Churn |
| 4 | Risikoprüfungen mit Diagnose-Bibliothek, inkl. Widersprüche (S03) und Generationen-Mapping (S04) | Underwriting-Fälle |
| 5 | Leistungsfälle (5–8 % der Verträge; Tod 60 %, EU/BU 25 %, Erleben 15 %) mit Betrugs-/Kulanz-Labels in separater Ground-Truth | Leistungs- und Betrugsfälle |
| 6 | Dokumentgenerierung aus Vorlagen je Generation (Text → PDF-T; Teil davon → Bild/Scan-Simulation mit Rauschen, Handschrift-Fonts, FR/IT-Anteil) | Unstrukturierter Korpus |
| 7 | Validierung: Konsistenzprüfung Dokument ↔ Daten, gewollte Inkonsistenzen protokolliert; fachliches Review der Regelwerke (Plausibilität CH/DE) | Freigabe für Kurs |

Offene fachliche Entscheidungen für die Auftraggeber:

1. Soll die DE-Kapital-LV wirklich nur als Bestand geführt werden (Empfehlung: ja, Neugeschäft DE über P3)?
2. Basisrente als Variante von P3 aufnehmen (steuerliche Stolpersteine) oder weglassen (Empfehlung: weglassen)?
3. Anteil FR/IT-Dokumente in CH (Empfehlung: 7 %; 0 % falls Kurs ausschliesslich deutschsprachig arbeiten soll)?
4. Fondsgebundene Varianten mit realistischen Fondskursen (synthetische Zeitreihen) oder nur Garantiewert?
5. Umfang des Altbestands (Empfehlung 55 %) und ältestes Jahr (Empfehlung 1985).
