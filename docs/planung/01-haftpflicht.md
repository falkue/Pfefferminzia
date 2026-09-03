# Pfefferminzia – Fachplanung Haftpflichtsparte (CH/DE)

**Zweck:** Fachliche Grundlage für einen synthetischen Lehr-Datensatz (Verträge, Schäden, Dokumente, Regelwerke) des fiktiven Versicherers *Pfefferminzia* (Merger Altversicherer *Pfefferminz* + KI-Start-up *Minzia*). Der Datensatz soll Executive-Teilnehmenden ermöglichen, KI-Use-Cases (Schadenklassifikation, Betrugserkennung, Dokumentextraktion, RAG über Bedingungswerke, Underwriting-Assistenz) hands-on durchzuspielen.

**Geltungsbereich dieses Dokuments:** ausschliesslich Haftpflicht (nicht Leben). Märkte Schweiz (CHF, VVG CH) und Deutschland (EUR, VVG DE). Es werden keine Daten erzeugt, nur geplant.

**Hinweis zur Fiktion:** Alle Prämien-, Häufigkeits- und Schadenhöhenangaben sind marktnahe Richtwerte, keine Tarifdaten realer Versicherer. Sie dienen der Plausibilität, nicht der Nachbildung eines konkreten Anbieters.

---

## Inhalt

1. Rahmen und Grundannahmen
2. Produktportfolio Haftpflicht
3. Lebenszyklus eines Haftpflichtvertrags
4. Schadenprozess Haftpflicht
5. Dokumenttypen (unstrukturiert)
6. Datenelemente (strukturiert)
7. Regelwerke
8. Didaktik: Stolpersteine und bewusste Unschärfen
9. Empfohlene Mengengerüste und nächste Schritte

---

## 1. Rahmen und Grundannahmen

### 1.1 Fiktive Unternehmensstruktur (Haftpflicht-relevant)

| Aspekt | Annahme | Didaktischer Nutzen |
|---|---|---|
| Rechtsträger CH | Pfefferminzia Versicherungen AG, Sitz Zürich, FINMA-beaufsichtigt | Eigene Policennummernlogik, CHF, Schweizer Bedingungswerke |
| Rechtsträger DE | Pfefferminzia Versicherung AG, Sitz Köln, BaFin-beaufsichtigt | EUR, AHB-basierte Bedingungen, deutsches VVG |
| Historie | Pfefferminz (gegr. 1911) betreibt Haftpflicht seit Jahrzehnten; Minzia (gegr. 2019) bringt Digitalvertrieb und ML-Modelle ein | Erklärt Altbestände mit alten Bedingungsgenerationen, Legacy-Nummernkreise, Medienbrüche |
| Bestandsgrösse (Vorschlag) | CH: 60'000 Privat-, 8'000 Betriebs-, 2'000 Berufshaftpflichtverträge; DE: 150'000 Privat-, 20'000 Betriebs-, 5'000 Berufshaftpflichtverträge | Ausreichend für Statistik, dennoch synthetisch handhabbar (Datensatz kann als Stichprobe von 1–5 % generiert werden) |
| Vertriebswege | CH: Eigene Aussendienst-Agenturen, Broker, Online; DE: Ausschliesslichkeitsvertreter, Makler, Vergleichsportale, Online | Unterschiedliche Datenqualität je Kanal (Portalanträge sind strukturiert, Broker-Anträge kommen als PDF/E-Mail) |
| Systemlandschaft | Altsystem "PFEFFER/400" (Pfefferminz, Bestand/Schaden, seit 1998) und Neusystem "MINT" (Minzia, cloudbasiert, seit 2021); Migration teilweise | Erklärt Feldnamen-Inkonsistenzen, Dubletten, unterschiedliche Codelisten |

### 1.2 Rechtsgrundlagen im Überblick

| Thema | Schweiz | Deutschland |
|---|---|---|
| Versicherungsvertrag | VVG (SR 221.229.1), revidiert per 1.1.2022 (u. a. Art. 2a Widerrufsrecht, Art. 35a ordentliches Kündigungsrecht nach 3 Jahren, Art. 60 Abs. 1bis direktes Forderungsrecht bei obligatorischen Haftpflichtversicherungen) | VVG 2008, insb. §§ 100–112 VVG (Haftpflichtversicherung), §§ 113–124 VVG (Pflichtversicherung), § 19 ff. Anzeigepflicht, § 28 Obliegenheiten, § 38 Folgeprämie, § 86 Forderungsübergang |
| Aufsicht | VAG, FINMA; AVO | VAG, BaFin; Solvency II |
| Haftungsgrundlagen | OR Art. 41 (Verschuldenshaftung), Art. 55 (Geschäftsherr), Art. 56 (Tierhalter), Art. 58 (Werkeigentümer), Art. 97 ff. (Vertragshaftung); PrHG (Produktehaftpflicht); Art. 333 ZGB (Familienhaupt) | BGB § 823 (unerlaubte Handlung), § 831 (Verrichtungsgehilfe), § 832 (Aufsichtspflicht), § 833 (Tierhalter), § 836 ff. (Gebäude), § 280 ff. (Vertragspflichtverletzung); ProdHaftG; UmweltHG |
| Verjährung Haftpflichtansprüche | OR Art. 60: 3 Jahre relativ / 10 Jahre absolut (20 Jahre bei Personenschäden, seit 2020) | BGB § 195/199: 3 Jahre ab Kenntnis, max. 10/30 Jahre |
| Datenschutz | DSG (revidiert 1.9.2023) | DSGVO, BDSG |
| Vermittlung | Art. 40 ff. VAG (Vermittlerregister, Informationspflicht) | IDD, § 34d GewO, §§ 60–65 VVG (Beratungs- und Dokumentationspflicht) |
| Vorvertragliche Information | Art. 3 VVG (Informationspflicht des Versicherers) | § 7 VVG, VVG-InfoV (Produktinformationsblatt), IPID |
| Pflichtversicherungen (Auswahl) | Anwälte (BGFA Art. 12 lit. f, min. CHF 1 Mio.), Hundehalter in einzelnen Kantonen, diverse Berufe kantonal | Rechtsanwälte (§ 51 BRAO, min. EUR 250'000), Steuerberater (§ 67 StBerG, min. EUR 250'000), Ärzte (Berufsordnungen), Hundehalter in mehreren Bundesländern (z. B. Berlin, Hamburg, Niedersachsen, Sachsen-Anhalt, Thüringen, Schleswig-Holstein) |

### 1.3 Zentrale fachliche Unterschiede CH vs. DE (für Datenmodell und Dokumente relevant)

| Merkmal | Schweiz | Deutschland |
|---|---|---|
| Währung / Zahlenformat | CHF, Tausendertrennzeichen Apostroph (5'000'000), Dezimalpunkt in Systemen, Komma in Briefen | EUR, Tausenderpunkt (5.000.000), Dezimalkomma |
| Deckungssumme Privathaftpflicht | Meist CHF 5 Mio. (Standard), Optionen 10 Mio.; einheitlich für Personen- und Sachschäden; reine Vermögensschäden teils sublimitiert | Pauschal 5 / 10 / 20 / 50 Mio. EUR für Personen- und Sachschäden; Vermögensschäden oft sublimitiert (z. B. 100'000–500'000 EUR) oder pauschal mitversichert |
| Selbstbehalt Privathaftpflicht | Üblich CHF 200 pro Ereignis (Varianten 0/100/200/500) | Üblich EUR 0; Option 150 oder 250 EUR gegen Rabatt |
| Vertragsdauer | Mehrjahresverträge (3–5 Jahre) üblich, ordentliche Kündigung nach 3 Jahren (Art. 35a VVG); stillschweigende Verlängerung jeweils 1 Jahr | Regel 1 Jahr mit stillschweigender Verlängerung; bei Verbrauchern max. 3 Jahre Bindung (§ 11 Abs. 4 VVG); Kündigungsfrist 3 Monate |
| Mahnverfahren bei Prämienverzug | Art. 20 VVG: schriftliche Mahnung mit 14-tägiger Frist; danach Deckungsunterbruch ("Haftung ruht") | § 38 VVG: qualifizierte Mahnung mit 2-Wochen-Frist, Leistungsfreiheit und Kündigungsrecht |
| Kündigung im Schadenfall | Art. 42 VVG: beide Seiten nach Leistung, VN innert 14 Tagen nach Kenntnis, Versicherer bei Auszahlung | § 111 VVG: beide Seiten innert 1 Monat nach Anerkennung/Ablehnung/Anweisung zur Rechtsstreitigkeit |
| Beratungsdokumentation | Keine Protokollpflicht wie DE; Vermittler-Informationspflicht (Art. 45 VAG) | Beratungsprotokoll nach §§ 61–62 VVG bei Vermittlung, § 6 VVG beim Versicherer |
| Widerruf | 14 Tage (Art. 2a VVG, seit 2022) | 14 Tage (§ 8 VVG) |
| Anzeigepflichtverletzung | Art. 6 VVG: Kündigungsrecht innert 4 Wochen nach Kenntnis; Leistungsfreiheit bei Kausalität | § 19 ff. VVG: Rücktritt/Kündigung/Vertragsanpassung je nach Verschuldensgrad, 1-Monats-Frist |
| Direktanspruch Geschädigter | Grundsätzlich nein; Ausnahme obligatorische Haftpflicht (Art. 60 Abs. 1bis VVG) | Grundsätzlich nein; Ausnahme Pflichtversicherung (§ 115 VVG), ansonsten Pfandrecht § 108 VVG |
| Sozialversicherungsregress | UVG/AHV/IV-Regress nach ATSG Art. 72 ff., Subrogation im Zeitpunkt des Ereignisses | § 116 SGB X: Forderungsübergang auf Sozialversicherungsträger |
| Mehrwertsteuer | 8.1 % (seit 2024); relevant bei Sachschadenregulierung | 19 % / 7 % |
| Adressen | PLZ 4-stellig, Kanton; Strasse mit "strasse" (kein ß) | PLZ 5-stellig, Bundesland; "Straße" |
| Personennamen / Sprache | Mehrsprachigkeit: Dokumente in DE, FR, IT (Empfehlung: DE als Hauptsprache, 15 % FR, 5 % IT für Realismus) | Deutsch |

---

## 2. Produktportfolio Haftpflicht

### 2.1 Empfehlung: Drei Kernprodukte plus Bausteine

Ein handhabbares, aber realistisches Portfolio umfasst drei eigenständige Produkte. Weitere Deckungen (Tierhalter, Bauherren, Gewässerschaden/Öltank) werden als *Bausteine* innerhalb der Privathaftpflicht bzw. Betriebshaftpflicht modelliert. Das ist marktüblich (insbesondere in CH), reduziert die Produktanzahl und erzeugt trotzdem interessante Deckungsgrenzfälle.

| Nr. | Produkt (Markenname) | Kürzel | Zielgruppe | Warum im Lehrdatensatz |
|---|---|---|---|---|
| P1 | Pfefferminzia Privathaftpflicht ("PrivatPlus") | PHV | Privatpersonen, Einzelpersonen/Familien, CH+DE | Massengeschäft: hohe Stückzahlen, viele Kleinschäden, viel Betrugspotenzial, standardisierte Dokumente, ideal für Klassifikation/Betrugserkennung |
| P2 | Pfefferminzia Betriebshaftpflicht ("BusinessProtect") | BHV | KMU bis ca. 50 Mitarbeitende: Handwerk, Gastronomie, Handel, Dienstleistung, Kleinproduktion | Underwriting mit Branchenklassifikation, heterogene Risiken, Produkt-/Umweltbausteine, komplexere Schäden, gut für UW-Assistenz und RAG |
| P3 | Pfefferminzia Berufshaftpflicht ("ProfessionalShield") | BeHV | Freie Berufe mit Vermögensschadenrisiko: Architekten/Ingenieure, Treuhänder/Steuerberater, IT-Dienstleister/Softwareentwickler, Unternehmensberater | Wenige, aber grosse und langlaufende Schäden (long tail), Anwaltskorrespondenz, Claims-made-Problematik (DE), Abwehrkosten, gut für Dokumentextraktion und Haftungsprüfung |
| B1 | Baustein Tierhalter (Hunde, Pferde) | – | In PHV; in CH Hunde/Katzen standardmässig inkl., Pferde als Zusatz; in DE Hundehalter als Zusatzbaustein (Pflicht in einigen Bundesländern) | Regionale Pflichtversicherung als Regelwerk-Frage |
| B2 | Baustein Bauherrenhaftpflicht | – | In PHV bis Bausumme (CH: CHF 100'000; DE: EUR 50'000) inkl., darüber Einzelvertrag (nicht modelliert) | Deckungsgrenzfall Bausumme |
| B3 | Baustein Gewässerschaden / Öltank | – | PHV: Heizöltank bis 5'000 l (DE) bzw. in CH Gebäudehaftpflicht-Baustein; BHV: Umwelthaftpflicht-Baustein | Grenzfall Umwelt vs. Sachschaden |
| B4 | Baustein Produkthaftpflicht (nur BHV) | – | Produzierende KMU, Gastronomie (Lebensmittel) | Rückruf vs. Produkthaftung als Abgrenzung |
| B5 | Baustein Gebäudehaftpflicht (Hauseigentümer) | – | In PHV für selbstbewohnte Ein-/Zweifamilienhäuser inkl.; vermietete Objekte als Zusatz | CH-typischer Werkeigentümer-Fall (Art. 58 OR) |

Nicht modelliert (bewusst): Motorfahrzeughaftpflicht (eigene Sparte, andere Regelwerke), Vermögensschadenhaftpflicht für Anwälte/Notare (zu speziell), D&O, Cyber, Jagdhaftpflicht, Veranstalterhaftpflicht. Diese können in Dokumenten als "nicht versichert, bitte Sparte X kontaktieren" auftauchen (Stolperstein).

### 2.2 P1 – Privathaftpflicht ("PrivatPlus")

| Merkmal | Schweiz | Deutschland |
|---|---|---|
| Versicherte Personen | Einzelperson oder Familie/Haushalt (Ehe-/Lebenspartner, Kinder bis 25 in Ausbildung im gleichen Haushalt, Au-pair, Haushalthilfen) | Single oder Familie (Ehe-/Lebenspartner, unverheiratete Kinder bis Abschluss der Erstausbildung, auch auswärts; deliktunfähige Kinder als Option mitversichert) |
| Deckungssumme | CHF 5 Mio. (Standard), CHF 10 Mio. (Option); Vermögensschäden (reine) sublimitiert CHF 100'000 | EUR 5 / 10 / 20 / 50 Mio. pauschal Personen-/Sachschäden; Vermögensschäden EUR 100'000 (Basis) / 500'000 (Premium); Mietsachschäden EUR 1 Mio. (Basis) bis Deckungssumme |
| Selbstbehalt | CHF 200 pro Ereignis (Standard); Varianten 0 / 500; bei grobfahrlässig verursachten Schäden ggf. Kürzung statt SB | EUR 0 (Standard); Option EUR 150 (ca. 15 % Rabatt) |
| Jahresprämie (Richtwert) | Einzelperson CHF 80–140; Familie CHF 110–220; mit Haustierhalter +CHF 0 (inkl.); Pferdehalter +CHF 150–300; Gebäudehaftpflicht +CHF 60–120; Variante 10 Mio. +15 % | Single EUR 45–90; Familie EUR 65–140; Hundehalter +EUR 40–90 (je nach Rasse/Bundesland); Pferdehalter +EUR 100–200; Öltank +EUR 25–50; 50 Mio. +10 % |
| Tarifmerkmale | Personenkreis (Einzel/Familie), Deckungssumme, Selbstbehalt, Bausteine, Wohnort (Kanton/PLZ-Region, gering), Vertragsdauer (Mehrjahresrabatt 3/5 Jahre), Bündelrabatt Hausrat, Zahlweise | Personenkreis, Deckungssumme, Selbstbehalt, Bausteine, Berufsgruppe (öffentlicher Dienst-Rabatt), Vorschäden (Anzahl in 5 Jahren), Zahlweise, Laufzeit (3 Jahre = Rabatt), Beamtenrabatt |
| Typische Einschlüsse | Familienhaupt-Haftung (Art. 333 ZGB), Mieterschäden (Mietsachschäden an Wohnung), Obhutsschäden (gemietete/geliehene bewegliche Sachen bis CHF 2'000–5'000), Gefälligkeitsschäden (bis CHF 5'000–10'000), Hunde/Katzen, Modellflug bis 30 kg (CH-Typik), Velos/E-Bikes bis 25 km/h, Bauherren bis CHF 100'000 Bausumme, Weltdeckung | Mietsachschäden, Schlüsselverlust (bis EUR 30'000–100'000), Gefälligkeitsschäden, Ausfalldeckung (Forderungsausfall ab EUR 2'500), deliktunfähige Kinder, Drohnen bis 5 kg (Pflicht nach LuftVG beachten), Internet-/Datenschäden, Ehrenamt, Bauherren bis EUR 50'000, Auslandaufenthalt weltweit bis 5 Jahre (EU unbegrenzt), Photovoltaik auf eigenem Haus |
| Typische Ausschlüsse | Vorsatz, Motorfahrzeuge (MFH), Schäden an eigenen Sachen, Berufs-/Gewerbetätigkeit, Halter von Motorbooten/Luftfahrzeugen, Bussen, Schäden unter mitversicherten Personen (Familienangehörige), Asbest, Kernenergie, Schäden aus Übertragung von Krankheiten (teilweise), Vertragserfüllung | Vorsatz, Kfz/Luft-/Wasserfahrzeuge, Schäden an eigenen/geliehenen Sachen (soweit nicht eingeschlossen), Angehörigen-Schäden (mitversicherte Personen untereinander), berufliche Tätigkeit, Jagd, Sportarten mit erhöhtem Risiko (Boxen, Ringen), Kernenergie, Asbest, gentechnisch veränderte Organismen, Ansprüche aus Vertragserfüllung, Umweltschäden über Baustein hinaus |
| Rechtsgrundlage | VVG CH, AVB PHV Pfefferminzia CH (Ausgabe 2022) + Altbedingungen Pfefferminz (Ausgabe 2012, 2017) | VVG DE, AHB (GDV-Muster) + BBR Privathaftpflicht Pfefferminzia (Fassung 2023) + Altbedingungen Pfefferminz (AHB 2008, BBR 2015) |
| Marktpraxis | Häufig im Bündel mit Hausratversicherung; Selbstbehalt Standard; Vermittlung über Agenten; Wechselquote niedrig wegen Mehrjahresverträgen | Preiswettbewerb über Vergleichsportale; jährliche Kündigungswelle zum 1.1.; hohe Deckungssummen mit geringem Preisunterschied; "Best-Leistungs-Garantie" als Marketingmerkmal |

### 2.3 P2 – Betriebshaftpflicht ("BusinessProtect")

| Merkmal | Schweiz | Deutschland |
|---|---|---|
| Zielgruppe | KMU 1–50 Mitarbeitende, Lohnsumme bis CHF 5 Mio. oder Umsatz bis CHF 10 Mio.; Branchen: Handwerk (Sanitär, Elektro, Maler, Schreiner), Gastronomie, Detailhandel, Dienstleistungen (Reinigung, Coiffeur, Fitness), Kleinproduktion | Analog: Handwerk, Gastronomie, Einzelhandel, Dienstleistung, kleine Produktionsbetriebe; Umsatz bis EUR 10 Mio., bis 50 Beschäftigte |
| Versicherte Risiken | Betriebs-, Produkte-, Umwelthaftpflicht (Baustein), Anlage-/Gebäudehaftpflicht, Bauherren (bis Bausumme), Werbung/Kommunikation, Arbeitgeberhaftpflicht (Regress UVG-Versicherer), Obhutsschäden (bearbeitete Sachen bis Sublimit) | Betriebs-, Produkthaftpflicht (inkl. erweiterte Produkthaftpflicht optional), Umwelthaftpflicht-Basis (UHV) + Umweltschaden (USV nach USchadG), Tätigkeitsschäden (Bearbeitungsschäden), Mietsachschäden Gebäude, Schlüsselverlust, Be-/Entladeschäden, Vermögensschäden, Datenschutzverletzungen |
| Deckungssumme | CHF 5 Mio. (Standard) / 10 Mio.; Sublimits: Obhut/Bearbeitung CHF 100'000–500'000, reine Vermögensschäden CHF 100'000–250'000, Umwelt CHF 1–5 Mio.; Jahresmaximum = 2 × Deckungssumme | EUR 3 / 5 / 10 Mio. pauschal; Vermögensschäden EUR 100'000–500'000; Tätigkeitsschäden EUR 100'000–1 Mio.; Mietsachschäden EUR 1 Mio.; Jahreshöchstleistung 2-fach |
| Selbstbehalt | CHF 500 (Standard), CHF 1'000–5'000 (Option); bei Bearbeitungsschäden 10 % min. CHF 1'000 | EUR 250–1'000 (Standard 500) je Schadenfall Sachschaden; Tätigkeitsschäden 10 % min. EUR 1'000; Personenschäden meist ohne SB |
| Jahresprämie (Richtwert) | CHF 400–6'000; Bemessung: Lohnsumme (CHF 2–8 ‰ je Branche) oder Umsatz; Mindestprämie CHF 350 | EUR 250–5'000; Bemessung: Umsatz (0.5–4 ‰) oder Personenzahl (Handwerk: EUR 80–300 pro Person); Mindestprämie EUR 200 |
| Tarifmerkmale | Branchencode (Pfefferminzia-Risikoklasse 1–6 auf Basis NOGA 2008), Lohnsumme/Umsatz, Mitarbeitendenzahl, Deckungssumme, Selbstbehalt, Bausteine, Vorschäden (3 Jahre), Auslandanteil, Subunternehmer-Anteil | Betriebsart (Klassifikation nach GDV-Betriebsartenverzeichnis / WZ 2008), Umsatz, Lohn-/Gehaltssumme, Beschäftigte, Deckungssumme, SB, Bausteine, Vorschäden (5 Jahre), Export USA/Kanada (Zuschlag/Ausschluss) |
| Besonderheiten | Regress UVG-Versicherer (SUVA) bei Arbeitsunfällen mit grober Fahrlässigkeit; Werkeigentümerhaftung; Baustein "Sachen in Obhut/bearbeitete Sachen" ist Hauptschadentreiber im Handwerk | Trennung Haftpflicht/Betriebsschliessung; USV-Baustein; "Nachhaftung" nach Betriebsaufgabe; GDV-Klausel-Systematik; Regress Berufsgenossenschaft (§ 110 SGB VII) |
| Typische Ausschlüsse | Vorsatz, Erfüllungsansprüche, Mängelbeseitigung am eigenen Werk, Motorfahrzeuge, Asbest, reine Vermögensschäden aus Beratung (BeHV), Rückrufkosten (ausser Baustein), Bussen, Vertragsstrafen, Datenverlust (ausser Baustein) | Vorsatz, Erfüllungsansprüche, Nachbesserung, Kfz, Asbest, Beratungsfehler mit reinen Vermögensschäden (Berufshaftpflicht), Rückruf (ausser Baustein), Vertragsstrafen, Sachschäden an hergestellten/gelieferten Produkten, USA/Kanada-Risiko ohne Zuschlag |
| Rechtsgrundlage | VVG CH, AVB BHV Pfefferminzia CH 2022; Branchenzusatzbedingungen (ZB) für Handwerk/Gastro/Handel | AHB 2016 (GDV-Muster) + BBR Betriebshaftpflicht Pfefferminzia 2023 + Betriebsbeschreibung |

### 2.4 P3 – Berufshaftpflicht ("ProfessionalShield")

| Merkmal | Schweiz | Deutschland |
|---|---|---|
| Zielgruppe (4 Berufsgruppen) | (a) Architekten/Bauingenieure (SIA-Verträge), (b) Treuhänder/Steuerberater/Revisoren (EXPERTsuisse, TREUHAND SUISSE), (c) IT-Dienstleister/Softwareentwickler, (d) Unternehmens-/Managementberater | (a) Architekten/Ingenieure (Pflicht nach Landesbauordnungen/Architektengesetzen), (b) Steuerberater (Pflicht § 67 StBerG, min. EUR 250'000 je Fall), (c) IT-Dienstleister, (d) Unternehmensberater |
| Charakter | Vermögensschadenhaftpflicht (reine Vermögensschäden), kombiniert mit Betriebshaftpflicht-Grunddeckung für Personen-/Sachschäden aus dem Bürobetrieb | Vermögensschaden-Haftpflicht (VH) + Büro-Betriebshaftpflicht |
| Deckungssumme | CHF 1 / 2 / 5 Mio. für Vermögensschäden; CHF 5 Mio. für Personen-/Sachschäden; Jahresmaximum 2-fach | EUR 250'000 / 500'000 / 1 Mio. / 2 Mio. für Vermögensschäden (Steuerberater min. 250'000, Architekten je LBO meist 1.5 Mio. Personen / 250'000–300'000 Sach); Personen-/Sachschäden EUR 3–5 Mio. |
| Selbstbehalt | CHF 1'000–5'000 pro Fall (Standard CHF 2'000); bei IT 10 % min. CHF 2'500 | EUR 1'000–5'000 (Standard EUR 2'500); Steuerberater oft EUR 1'000 |
| Jahresprämie (Richtwert) | Architekten CHF 1'500–15'000 (nach Honorarsumme, 5–12 ‰); Treuhänder CHF 800–6'000; IT CHF 900–8'000 (nach Umsatz, 3–8 ‰); Berater CHF 700–5'000 | Architekten EUR 900–12'000; Steuerberater EUR 500–4'000; IT EUR 600–6'000; Berater EUR 500–4'000 |
| Deckungsprinzip (zentraler Stolperstein) | Verstossprinzip (Schadenverursachung/Pflichtverletzung während Vertragsdauer) mit Nachhaftung 5 Jahre; teils Claims-made-Variante für IT | Verstossprinzip Standard bei Architekten/Steuerberatern (Nachhaftung 5 Jahre); Claims-made bei IT-/Beratern mit Rückwärtsdeckung ab definiertem Datum und Nachmeldefrist 3 Jahre |
| Tarifmerkmale | Berufsgruppe, Honorar-/Umsatzsumme, Anzahl Berufsträger/Mitarbeitende, Deckungssumme, SB, Tätigkeitsschwerpunkte (z. B. Bauleitung ja/nein, Revisionstätigkeit ja/nein), Vorschäden 5 Jahre, Auslandtätigkeit, Zertifizierungen (ISO 27001 Rabatt bei IT) | Analog; zusätzlich Kammermitgliedschaft, Anteil öffentlicher Auftraggeber, Projektgrössen (max. Bausumme), Datenschutz-Zertifikate |
| Typische Ausschlüsse | Vorsatz, wissentliche Pflichtverletzung, Erfüllungsansprüche (Nachbesserung), Honorarstreitigkeiten, Kostenüberschreitungen bei Bauprojekten (ausser Baustein), Bussen, Garantiezusagen, Termingarantien, Schäden aus Insolvenz, Asbest, IT: Datenverlust ohne Backup-Konzept, Cyber-Erpressung | Vorsatz, wissentliche Pflichtverletzung, Kostenüberschreitungen/Bausummenüberschreitungen, Honorarstreit, Termingarantien, Insolvenz, Geldbussen, Tätigkeiten ausserhalb der Berufsordnung, USA/Kanada |
| Rechtsgrundlage | VVG CH, AVB BeHV Pfefferminzia CH 2022; Besondere Bedingungen je Berufsgruppe | VVG DE, AVB-Vermögen (GDV-Muster AVB-V) + BBR je Berufsgruppe; AHB für Bürobetrieb |
| Marktpraxis | Broker-dominiert, individuelle Offerten, Fragebogen "Risikoerhebung" mit 3–6 Seiten | Makler-dominiert, Berufsverbands-Rahmenverträge (Gruppenverträge) als Konkurrenz, Fragebogen "Risikofragebogen" |

### 2.5 Produktgenerationen (für Realismus)

| Generation | Zeitraum | Bezeichnung in Daten | Merkmale | Anteil im Bestand (Vorschlag) |
|---|---|---|---|---|
| Pfefferminz Klassik | bis 2012 | `PFM-K` | Alte AVB (CH 2005 / DE AHB 2008), tiefere Deckungssummen (CH 3 Mio., DE 3 Mio.), keine Gefälligkeitsschäden, keine Ausfalldeckung | 8 % (Altbestand, nur PHV/BHV) |
| Pfefferminz Modern | 2013–2020 | `PFM-M` | AVB 2012/2017 (CH), BBR 2015 (DE); Deckungssumme CH 5 Mio., DE 5–10 Mio.; Bausteine eingeführt | 45 % |
| Pfefferminzia | ab 2021 | `PFZ-2021` / `PFZ-2023` | Neue AVB 2022 (CH) / BBR 2023 (DE), digitale Antragstrecke, Online-Schadenmeldung, höhere Sublimits, Best-Leistungs-Garantie (DE) | 47 % |

Der Bedingungsmix erlaubt RAG-Aufgaben wie "Welche AVB gilt für diesen Vertrag?" und Deckungsprüfungen, bei denen die Bedingungsgeneration das Ergebnis ändert (z. B. Gefälligkeitsschaden unter PFM-K nicht gedeckt).

---

## 3. Lebenszyklus eines Haftpflichtvertrags

### 3.1 Phasenübersicht

```
Anfrage/Offerte → Antrag → Risikoprüfung (UW) → Policierung → Inkasso → Laufender Vertrag
      (Änderung/Nachtrag ↔ Erneuerung/Indexierung ↔ Mahnung) → Beendigung (Kündigung/Storno/Aufhebung) → Nachbearbeitung (Nachhaftung, Rückerstattung)
```

### 3.2 Phasen mit Dokumenten und Datenelementen

| Phase | Auslöser / Akteure | Aktivitäten | Entstehende Dokumente | Zentrale Datenelemente | CH/DE-Besonderheiten |
|---|---|---|---|---|---|
| 1. Anfrage / Offerte | Kunde, Vermittler, Portal | Bedarfsermittlung, Tarifberechnung, Offertstellung, ggf. mehrere Varianten | Offerte/Angebot (PDF), Vorvertragliche Kundeninformation (CH Art. 3 VVG), Produktinformationsblatt + IPID (DE), Beratungsprotokoll (DE), E-Mail-Korrespondenz | Offertnummer, Offertdatum, Gültigkeit (30 Tage), Produkt, Varianten (Deckungssumme, SB), Prämie brutto/netto, Vermittler-ID, Kanal | DE: Beratungsprotokoll Pflicht bei Vermittlung; CH: Kundeninformation vor Antrag; Portalofferten strukturiert, Broker-Offerten frei formatiert |
| 2. Antrag | Kunde unterschreibt (physisch/e-Signatur/Click) | Antragsdaten erfassen, Risikofragen beantworten, Vorversicherung/Vorschäden angeben, Zahlungsmodalität wählen | Antragsformular (PDF ausgefüllt, teils handschriftlich), Risikofragebogen (BHV/BeHV), Betriebsbeschreibung (BHV), Vollmacht Vermittler, SEPA-Lastschriftmandat (DE) / LSV-Ermächtigung (CH), Ausweiskopie (selten), Vorversicherungsnachweis | Antragsnummer, Antragsdatum, Unterschriftsdatum, VN-Stammdaten, Risikoangaben, Antworten auf Risikofragen (Ja/Nein + Freitext), gewünschter Beginn, Vorversicherer, Vorschäden (Anzahl, Jahr, Höhe), Zahlweise | DE: Belehrung über Folgen der Anzeigepflichtverletzung (§ 19 Abs. 5 VVG) muss auf Antrag; CH: Art. 4/6 VVG Fragen "schriftlich oder in anderer Textform" |
| 3. Risikoprüfung (Underwriting) | Underwriter (bei Abweichung von Vollmachtsstufe 0) oder automatischer Regelentscheid | Prüfung Zeichnungsrichtlinien, Vorschäden, Bonität (DE: Schufa-Auskunft bei BHV; CH: Betreibungsauskunft), Sanktionsprüfung, Branchenklasse, Rückfragen | UW-Entscheid (intern), Rückfrage-E-Mail an Vermittler, Ablehnungsschreiben, Annahme mit Auflagen (Zuschlag, Ausschlussklausel), Auskunft Vorversicherer (DE: Anfrage Vorschäden), Bonitätsauskunft | UW-Status (angenommen/mit Auflagen/abgelehnt/rückgefragt), UW-Entscheidungsdatum, Underwriter-ID, Vollmachtsstufe, Zuschlag %, Ausschlussklausel-Code, Begründung Freitext, Risikoscore (MINT-Modell) | DE: Datenaustausch über HIS (Hinweis- und Informationssystem) bei Haftpflicht-Vorschäden; CH: kein zentrales HIS, aber Vorversicherer-Anfrage |
| 4. Policierung | Bestandssystem | Vertragserstellung, Policennummer, Versicherungsschein drucken/versenden, Dokumentenmappe zusammenstellen | Police/Versicherungsschein (PDF), AVB/AHB + BBR/Besondere Bedingungen (PDF), Deckungsbestätigung (Kurzform, z. B. für Vermieter), Begleitschreiben, Prämienrechnung | Policennummer, Vertragsbeginn, Ablauf/Hauptfälligkeit, Laufzeit, Verlängerungsklausel, Bedingungsgeneration, Deckungsbausteine, Prämie, Zahlweise, Rechnungsnummer, Fälligkeitsdatum | CH: Police gilt als Vertragsurkunde; Einwände gegen Policeninhalt innert 4 Wochen (Art. 12 VVG alt, seit 2022 aufgehoben, aber Praxis "Genehmigungsfiktion" in Altdokumenten); DE: Versicherungsschein § 3 VVG, Billigungsklausel § 5 VVG (Abweichungen gelten als genehmigt nach 1 Monat mit Hinweis) |
| 5. Inkasso | Buchhaltung, Zahlungsdienstleister | Rechnung, Zahlungseingang, Zuordnung, Mahnwesen, Rückerstattung | Prämienrechnung (PDF/E-Rechnung/QR-Rechnung CH), Zahlungsbestätigung, 1. Zahlungserinnerung, Mahnung (qualifiziert), Deckungsunterbruch-Mitteilung (CH), Rücklastschrift-Info (DE), Inkassoübergabe | Rechnungsnummer, Rechnungsbetrag, Fälligkeit, Zahlungsdatum, Zahlungsart, Offener Saldo, Mahnstufe (0–3), Mahndatum, Deckungsunterbruch ab/bis, Verzugszinsen, Inkassogebühr | CH: QR-Rechnung, Art. 20 VVG Mahnung mit 14 Tagen, Haftung ruht ab Fristablauf, Betreibung; DE: § 38 VVG Mahnung mit 2 Wochen, Leistungsfreiheit, Kündigungsrecht, SEPA-Rücklastschrift-Gebühren |
| 6. Laufender Vertrag: Änderung/Nachtrag | Kunde, Vermittler, System | Adressänderung, Namensänderung, Heirat (Einzel → Familie), Umzug (CH ↔ Kanton, DE ↔ Bundesland mit Hundehalterpflicht), Baustein-Zugang/-Abgang, Deckungssummenerhöhung, Lohnsummen-/Umsatzmeldung (BHV/BeHV jährlich), Betriebsänderung (Branche, Rechtsform), Vermittlerwechsel | Änderungsantrag (E-Mail, Formular, Telefonnotiz), Nachtrag/Nachtragspolice (PDF), Nachtragsrechnung/Gutschrift, Umsatz-/Lohnsummenmeldung (Formular), Bestätigungsschreiben, Maklerwechsel-Mitteilung mit Vollmacht | Nachtragsnummer, Nachtragsdatum, Wirksamkeitsdatum, Änderungsgrund (Codeliste), Alte/Neue Werte (Delta), Prämienänderung pro rata, Bearbeiter-ID | BHV: jährliche Lohnsummen-/Umsatzabrechnung mit Nachprämie (CH: "Prämienabrechnung", DE: "Beitragsregulierung"); Gefahrerhöhung: CH Art. 28 ff. VVG, DE §§ 23–27 VVG |
| 7. Laufender Vertrag: Erneuerung / Anpassung | Hauptfälligkeit | Automatische Verlängerung, Prämienanpassung (Indexierung, Tarifanpassung), Bedingungsumstellung (Migration Altbestand), Rabattprüfung | Erneuerungsrechnung, Anpassungsschreiben (mit Hinweis Kündigungsrecht bei Prämienerhöhung), Bedingungsumstellungsangebot, Erinnerungsschreiben an Vermittler | Verlängerungsdatum, Anpassungsgrund, Prämie alt/neu, Kündigungsrecht ja/nein, Frist, Bedingungsgeneration alt/neu | CH: bei Prämienerhöhung Kündigungsrecht (Art. 35a/AVB); DE: § 40 VVG Kündigungsrecht bei Prämienerhöhung, 1 Monat |
| 8. Beendigung | Kunde, Versicherer, Gesetz | Ordentliche Kündigung, Kündigung im Schadenfall, Kündigung wegen Prämienverzug, Rücktritt/Kündigung wegen Anzeigepflichtverletzung, Aufhebung im gegenseitigen Einvernehmen (Wegzug ins Ausland, Tod, Betriebsaufgabe, Doppelversicherung), Widerruf, Storno rückwirkend (Nichtzustandekommen), Nachversicherung Todesfall | Kündigungsschreiben VN (Brief/E-Mail/Portal, oft formlos), Kündigungsbestätigung, Kündigung Versicherer (eingeschrieben), Aufhebungsvereinbarung, Rückerstattungsabrechnung, Widerrufserklärung, Storno-Mitteilung, Nachhaftungsbestätigung (BeHV), Bestätigung Vorversicherungszeit/Schadenfreiheit (für neuen Versicherer) | Beendigungsdatum, Beendigungsgrund (Codeliste), Kündigende Partei, Kündigungseingang, Fristwahrung ja/nein, Rückprämie, Nachhaftung bis, Storno-Typ | CH: Kündigung nach Ablauf 3. Jahr (Art. 35a), Kündigung im Schadenfall (Art. 42), Frist 3 Monate; formlos, aber schriftlich (Textform seit 2022); DE: Kündigung 3 Monate vor Ablauf, § 111 im Schadenfall 1 Monat, § 11 Abs. 4 nach 3 Jahren; Textform genügt |
| 9. Nachbearbeitung | System | Nachhaftung (BeHV, Verstossprinzip 5 Jahre), Archivierung (10 Jahre CH OR 958f, DE HGB § 257), Löschung nach DSG/DSGVO, Reaktivierung bei Rücknahme der Kündigung | Rücknahme-Bestätigung, Archivierungsvermerk | Archivdatum, Löschfrist, Reaktivierungsdatum | |

### 3.3 Vertragsstatus-Modell (Vorschlag)

| Statuscode | Bezeichnung | Beschreibung | Folgestatus |
|---|---|---|---|
| `OFF` | Offerte | Angebot erstellt, nicht angenommen | `ANT`, `OFV` (verfallen) |
| `ANT` | Antrag | Antrag eingegangen, in Prüfung | `AKT`, `ABG` (abgelehnt), `RUE` (Rückfrage) |
| `AKT` | Aktiv | Deckung besteht | `SUS`, `GEK`, `STO`, `ABL` |
| `SUS` | Suspendiert (Deckungsunterbruch) | CH: Haftung ruht nach Mahnung; DE: Leistungsfreiheit | `AKT` (nach Zahlung), `GEK` |
| `GEK` | Gekündigt (wirksam zu Datum) | Kündigung liegt vor, Vertrag läuft bis Beendigungsdatum | `BEE` |
| `BEE` | Beendet | Vertrag abgelaufen/beendet | `NAC` (Nachhaftung) |
| `STO` | Storniert | Rückwirkend aufgehoben (Widerruf, Nichtzustandekommen, Rücktritt) | – |
| `NAC` | Nachhaftung | Nur BeHV: Meldung von Verstössen aus Vertragszeit noch möglich | `BEE` |
| `MIG` | In Migration | Altsystem-Vertrag noch nicht vollständig in MINT | `AKT` |

### 3.4 Typische Ereignisverteilung pro Jahr (für Synthese)

| Ereignis | PHV | BHV | BeHV | Kommentar |
|---|---|---|---|---|
| Neugeschäft (Anteil Bestand) | 8–12 % | 10–15 % | 10–15 % | DE PHV höherer Wechsel als CH |
| Storno/Kündigung (Anteil Bestand) | CH 5–7 %, DE 9–13 % | 8–12 % | 8–12 % | DE-Portal-Kunden wechseln häufiger |
| Nachträge (pro Vertrag) | 0.15 | 0.6 | 0.4 | BHV: jährliche Umsatzmeldung |
| Mahnstufe ≥ 1 | 6–9 % | 8–12 % | 4–6 % | |
| Deckungsunterbruch/Suspension | 1–2 % | 2–3 % | 0.5–1 % | Ergibt Deckungsstreitfälle bei Schäden |
| Kündigung im Schadenfall (durch Versicherer) | 0.2 % | 0.5 % | 0.3 % | Bei auffälligen Schadenverläufen |
| Anzeigepflichtverletzung festgestellt | 0.1 % | 0.4 % | 0.5 % | Meist erst im Schadenfall entdeckt |

---

## 4. Schadenprozess Haftpflicht

### 4.1 Grundprinzip der Haftpflichtversicherung (für Teilnehmende ohne Fachhintergrund)

Der Versicherer erbringt zwei Leistungen: (1) Befriedigung *berechtigter* Ansprüche Dritter gegen den Versicherungsnehmer (Zahlung) und (2) Abwehr *unberechtigter* Ansprüche (passive Rechtsschutzfunktion, inkl. Anwalts- und Gerichtskosten, in CH über Deckungssumme hinaus, in DE innerhalb der Deckungssumme bei Pflichtversicherungen sonst darüber je nach Bedingung). Damit hat jeder Schaden zwei Prüfdimensionen: **Deckung** (Vertragsverhältnis VN–Versicherer) und **Haftung** (Rechtsverhältnis VN–Geschädigter). Beide müssen im Datenmodell getrennt abgebildet werden. Das ist der wichtigste konzeptionelle Unterschied zu Sach- oder Lebensversicherung und eine zentrale didaktische Botschaft.

### 4.2 Prozessphasen

| Phase | Aktivitäten | Beteiligte | Dokumente (Input/Output) | Datenelemente | Typische Durchlaufzeit |
|---|---|---|---|---|---|
| 1. Meldung (FNOL) | Schaden wird gemeldet: durch VN (Telefon, Portal, App, E-Mail, Vermittler), durch Geschädigten direkt (Anspruchsschreiben), durch Anwalt des Geschädigten, durch Sozialversicherer (Regress) | VN, Geschädigter, Vermittler, Anwalt, Sozialversicherer, Contact Center | Schadenmeldung (Formular/Portal/E-Mail/Telefonnotiz), Anspruchsschreiben Dritter, Fotos, erste Belege | Meldedatum, Meldekanal, Melder-Typ, Schadendatum (behauptet), Schadenort, Kurzbeschreibung Freitext, Geschädigter (Name, Kontakt), Schadenart grob | 0–90 Tage nach Ereignis (Median 6 Tage PHV; BeHV Median 4 Monate) |
| 2. Erfassung / Triage | Schadennummer vergeben, Vertrag zuordnen, Schadenart und -sparte klassifizieren, Erstreserve setzen, Zuteilung an Sachbearbeiter/Team nach Komplexität (Fast Track / Standard / Komplex / Grossschaden), Betrugsindikatoren prüfen (Minzia-Modell) | Schadenerfassung, ML-Klassifikator | Schadenanlage (Systemeintrag), Eingangsbestätigung an VN/Geschädigten, Aufforderung zur Einreichung fehlender Unterlagen | Schadennummer, Vertragsnummer, Schadenart (Personen/Sach/Vermögen/gemischt), Schadenursache-Code, Komplexitätsklasse, Erstreserve, Sachbearbeiter-ID, Betrugsscore, Prioritätsflag | 1–3 Tage |
| 3. Deckungsprüfung | Vertrag zum Schadendatum aktiv? Prämie bezahlt (kein Deckungsunterbruch)? Schaden im versicherten Risiko (privat vs. beruflich, Baustein vorhanden)? Ausschluss anwendbar? Obliegenheiten erfüllt (rechtzeitige Meldung, kein Anerkenntnis)? Bedingungsgeneration? Selbstbehalt? Sublimit? | Sachbearbeiter, Deckungsjurist bei Zweifel | Deckungsprüfungsnotiz (intern), Deckungszusage/-vorbehalt/-ablehnung an VN, Rückfragen an VN | Deckungsstatus (gedeckt / teilweise / Vorbehalt / abgelehnt), Ablehnungsgrund-Code, geprüfte AVB-Ziffer, Selbstbehalt, anwendbares Sublimit | 1–14 Tage |
| 4. Haftungsprüfung | Haftet der VN dem Grunde nach? Verschulden, Widerrechtlichkeit, Kausalität, Schaden; Mitverschulden des Geschädigten (Quote); Haftungsgrundlage (OR 41 / BGB 823 usw.); Anspruchshöhe plausibel (Zeitwert vs. Neuwert, Abzug neu für alt, Schmerzensgeld/Genugtuung)? | Sachbearbeiter, Jurist, externer Anwalt, Sachverständiger | Stellungnahme VN (Sachverhaltsschilderung), Zeugenaussagen, Polizeirapport, Gutachten, Anwaltsschreiben, internes Haftungsmemo, Schreiben an Geschädigten (Anerkennung/Teilanerkennung/Ablehnung mit Begründung) | Haftungsstatus (bejaht / verneint / strittig / Quote), Haftungsquote %, Haftungsgrundlage-Code, Mitverschulden %, Haftungsbegründung Freitext | 7–180 Tage |
| 5. Regulierung | Zahlung an Geschädigten (direkt) oder an VN (Erstattung), Vergleich, Teilzahlung, Abschlagszahlung (Personenschaden), Sachverständigenkosten, Anwaltskosten (eigene/gegnerische), Gerichtskosten; Abwehr: Prozessführung im Namen VN | Sachbearbeiter, Buchhaltung, Anwalt | Zahlungsavis, Vergleichsvereinbarung, Abfindungserklärung, Rechnung Geschädigter/Handwerker, Kostenvoranschlag, Reparaturrechnung, Arztrechnungen, Verdienstausfallnachweis, Klageschrift, Urteil | Zahlungen (Betrag, Datum, Empfänger, Zahlungsart, Kostenart), Reserveänderungen, Vergleichsbetrag, Abfindung ja/nein, Prozessstatus | Sach: 14–60 Tage; Personen: 6 Monate bis 10 Jahre |
| 6. Regress | Rückgriff auf Dritte (Mitverursacher, Hersteller, Subunternehmer, Haftpflichtversicherer des Mitverursachers), Regress gegen VN bei Vorsatz/Obliegenheitsverletzung (DE: § 116 VVG bei Pflichtversicherung), Aktivregress: Forderungsübergang (CH Art. 72 VVG / DE § 86 VVG). Passivregress: Sozialversicherer (SUVA/UVG, Berufsgenossenschaft, Krankenkasse) fordert vom Haftpflichtversicherer | Regress-Spezialist, Anwalt | Regressforderung (eingehend, von Sozialversicherer/anderem Versicherer), Regressschreiben (ausgehend), Teilungsabkommen-Abrechnung (DE: Teilungsabkommen mit Krankenkassen), Regressvereinbarung | Regressart (aktiv/passiv), Regressgegner, Forderungsbetrag, Regressquote, eingegangener Betrag, Regressstatus | 3 Monate bis 3 Jahre |
| 7. Abschluss | Reserve auflösen, Schaden schliessen, Kündigungsrecht prüfen, Bonus/Malus-Wirkung (BHV Vorschäden), Wiedereröffnung möglich (Nachforderung) | Sachbearbeiter | Abschlussschreiben, interne Schliessungsnotiz, Kündigung im Schadenfall (selten) | Schliessungsdatum, Schliessungsgrund (bezahlt / abgelehnt / zurückgezogen / verjährt / ohne Zahlung), Gesamtaufwand (Zahlungen + Kosten), Wiedereröffnungszähler | 0–30 Tage nach letzter Zahlung |

### 4.3 Schadenstatus-Modell (Vorschlag)

| Statuscode | Bezeichnung | Kommentar |
|---|---|---|
| `GEM` | Gemeldet | Eingegangen, noch nicht erfasst |
| `ERF` | Erfasst | Schadennummer vergeben, Erstreserve gesetzt |
| `DPR` | In Deckungsprüfung | |
| `DVB` | Deckung mit Vorbehalt | Bearbeitung läuft unter Vorbehalt (Reservation of Rights) |
| `HPR` | In Haftungsprüfung | |
| `REG` | In Regulierung | Zahlungen laufen |
| `ABW` | In Abwehr | Anspruch wird bestritten, ggf. Prozess |
| `RGS` | Regress laufend | Schaden geschlossen gegenüber Geschädigtem, Regress offen |
| `ABG` | Abgelehnt | Deckung oder Haftung verneint, Mitteilung versandt |
| `GES` | Geschlossen | Abgeschlossen |
| `WIE` | Wiedereröffnet | Nach Schliessung erneut geöffnet |

### 4.4 Schadenarten und typische Verteilungen

#### 4.4.1 Schadenarten nach Produkt (Anteil an Schadenanzahl)

| Schadenart | PHV CH | PHV DE | BHV | BeHV | Beispiele |
|---|---|---|---|---|---|
| Sachschaden Dritter (bewegliche Sachen) | 55 % | 52 % | 30 % | 2 % | Smartphone/Laptop eines Freundes beschädigt, Brille zerbrochen, Rotwein auf Teppich, Velo umgestossen, Kind zerkratzt Auto |
| Sachschaden Immobilie / Mietsache | 18 % | 20 % | 15 % | 1 % | Wasserschaden in Mietwohnung (überlaufende Badewanne), Parkettschaden, Brand durch Kerze, Schlüsselverlust (DE) |
| Bearbeitungs-/Obhutsschaden (BHV) | – | – | 25 % | – | Handwerker beschädigt Kundenwohnung, Malerflecken auf Möbeln, Sanitär-Installateur verursacht Wasserschaden |
| Personenschaden leicht (ambulant, < 30 Tage AU) | 12 % | 12 % | 12 % | – | Sturz durch nicht gestreuten Weg, Hundebiss, Kollision Velo–Fussgänger, Ski-Kollision |
| Personenschaden schwer (stationär, Dauerschaden) | 2 % | 2 % | 3 % | – | Schwere Ski-Kollision mit Invalidität, Sturz von Leiter beim Nachbar, Gastro: schwere Lebensmittelvergiftung |
| Reiner Vermögensschaden | 3 % | 4 % | 8 % | 85 % | Falsche Steuererklärung (Nachzahlung Zinsen/Bussen), Planungsfehler (Mehrkosten Bau), Softwarefehler (Betriebsunterbruch beim Kunden), Fehlberatung |
| Produktschaden | – | – | 5 % | – | Fremdkörper im Lebensmittel, fehlerhafte Komponente verursacht Folgeschaden |
| Umwelt-/Gewässerschaden | 1 % | 1 % | 2 % | – | Heizöl läuft aus Tank, Chemikalien im Abfluss |
| Tierhalter (Sach/Person) | 9 % (in PHV) | 9 % (Baustein) | – | – | Hund beisst Jogger, Pferd tritt Auto, Hund zerbeisst Sofa des Gastgebers |
| Gemischt (Person + Sache) | in obigen enthalten | | | | Velo-Kollision mit Personenschaden und Sachschaden |

Hinweis: Summe je Spalte ≈ 100 % (Tierhalter bei PHV überlappt mit Sach-/Personenschäden; für die Synthese als eigene Ursache-Dimension führen, nicht als Schadenart).

#### 4.4.2 Schadenfrequenz (Anzahl gemeldete Schäden pro Vertrag und Jahr)

| Produkt | CH | DE | Bemerkung |
|---|---|---|---|
| PHV Einzelperson | 4–5 % | 4–5 % | |
| PHV Familie | 7–10 % | 8–11 % | Kinder erhöhen Frequenz deutlich |
| PHV mit Hund | +3 Prozentpunkte | +4 Prozentpunkte | |
| BHV Handwerk | 20–35 % | 20–35 % | Bearbeitungsschäden treiben |
| BHV Gastronomie | 12–18 % | 12–18 % | |
| BHV Handel/Dienstleistung | 6–10 % | 6–10 % | |
| BeHV Architekten/Ingenieure | 8–12 % | 8–12 % | Viele Meldungen "vorsorglich" ohne Zahlung |
| BeHV Treuhand/Steuer | 5–8 % | 6–9 % | |
| BeHV IT | 4–6 % | 4–6 % | |
| BeHV Berater | 2–4 % | 2–4 % | |

#### 4.4.3 Schadenhöhenverteilung (Gesamtaufwand inkl. Kosten, geschlossene Schäden)

Empfohlene Modellierung: Lognormalverteilung je Schadenart mit Pareto-Tail für die obersten 1–2 %. Nullschäden (gemeldet, aber ohne Zahlung: Ablehnung, Rückzug, unter Selbstbehalt) als separater Anteil.

| Produkt / Schadenart | Anteil Nullschäden | Median | Mittelwert | 90 %-Quantil | 99 %-Quantil | Maximum (Datensatz) | Verteilungsparameter (Lognormal μ, σ des positiven Teils) |
|---|---|---|---|---|---|---|---|
| PHV Sachschaden beweglich (CHF/EUR) | 20 % | 450 | 800 | 1'800 | 6'000 | 25'000 | μ=6.1, σ=0.9 |
| PHV Sachschaden Immobilie/Mietsache | 15 % | 1'800 | 3'500 | 8'000 | 30'000 | 150'000 | μ=7.5, σ=1.0 |
| PHV Personenschaden leicht | 25 % | 1'200 | 2'500 | 6'000 | 20'000 | 60'000 | μ=7.1, σ=1.0 |
| PHV Personenschaden schwer | 10 % | 45'000 | 180'000 | 450'000 | 2'500'000 | 5'000'000 (CH) / 8'000'000 (DE) | μ=10.7, σ=1.3 |
| PHV reiner Vermögensschaden | 40 % | 900 | 2'500 | 6'000 | 25'000 | 100'000 | μ=6.8, σ=1.2 |
| PHV Tierhalter | 20 % | 600 | 2'200 | 4'500 | 40'000 | 300'000 | μ=6.4, σ=1.2 |
| BHV Bearbeitungsschaden | 15 % | 2'200 | 4'800 | 12'000 | 45'000 | 250'000 | μ=7.7, σ=1.0 |
| BHV Sachschaden Dritter | 15 % | 1'500 | 4'000 | 9'000 | 50'000 | 400'000 | μ=7.3, σ=1.1 |
| BHV Personenschaden | 20 % | 3'000 | 25'000 | 40'000 | 500'000 | 4'000'000 | μ=8.0, σ=1.6 |
| BHV Produktschaden | 30 % | 4'000 | 18'000 | 40'000 | 300'000 | 1'500'000 | μ=8.3, σ=1.4 |
| BHV Umweltschaden | 25 % | 12'000 | 35'000 | 90'000 | 400'000 | 1'200'000 | μ=9.4, σ=1.1 |
| BeHV Vermögensschaden Architekten | 45 % | 18'000 | 55'000 | 150'000 | 800'000 | 2'000'000 | μ=9.8, σ=1.2 |
| BeHV Vermögensschaden Treuhand/Steuer | 40 % | 9'000 | 30'000 | 80'000 | 400'000 | 1'000'000 | μ=9.1, σ=1.2 |
| BeHV Vermögensschaden IT | 50 % | 15'000 | 60'000 | 180'000 | 900'000 | 2'000'000 | μ=9.6, σ=1.3 |
| BeHV Vermögensschaden Berater | 55 % | 12'000 | 40'000 | 120'000 | 600'000 | 1'500'000 | μ=9.4, σ=1.2 |

Zusätzliche Verteilungsannahmen:

| Grösse | Annahme |
|---|---|
| Anteil Kosten (Anwalt, Gutachter, Gericht) am Gesamtaufwand | PHV 5 %, BHV 12 %, BeHV 35 % |
| Abwehrquote (Ansprüche vollständig abgewehrt) | PHV 15 %, BHV 20 %, BeHV 45 % |
| Haftungsquote < 100 % (Mitverschulden) | PHV 12 % der Schäden, BHV 18 %, BeHV 25 %; typische Quoten 50 %, 2/3, 75 % |
| Abwicklungsdauer (Meldung bis Schliessung) | PHV Sach Median 35 Tage; PHV Person leicht 120 Tage; Person schwer 3–8 Jahre; BHV Median 90 Tage; BeHV Median 14 Monate |
| Reserveentwicklung | Erstreserve pauschal nach Schadenart (PHV Sach 800, Person 5'000; BeHV 25'000); 30 % der Schäden mit mind. einer Reserveanpassung; Grossschäden mit 3–8 Anpassungen |
| Meldeverzug > 30 Tage | PHV 15 %, BHV 25 %, BeHV 60 % |
| Wiedereröffnung | 3 % (PHV), 5 % (BHV), 8 % (BeHV) |
| Regress erfolgreich (aktiv) | 4 % der BHV-Schäden, 2 % PHV; Rückfluss 30–70 % des Aufwands |
| Passivregress (Sozialversicherer als Melder) | 20 % der Personenschäden |
| Selbstbehalt-Abzug | Bei Zahlung an Geschädigten: Versicherer zahlt voll, fordert SB vom VN zurück (CH-Praxis) oder zahlt abzüglich SB an VN (bei Erstattung) |

#### 4.4.4 Zeitliche Muster (für Realismus)

| Muster | Beschreibung |
|---|---|
| Saisonalität PHV | Winter: Ski-Kollisionen (Jan–Mär, CH stärker), Glatteis-Stürze (Dez–Feb); Sommer: Velo/E-Bike, Grillunfälle, Ferien-Mietsachschäden (Jul–Aug); Dezember: Kerzenbrände |
| Saisonalität BHV | Baugewerbe Frühling–Herbst; Gastronomie Dezember (Weihnachtsessen); Heizungsbauer Herbst |
| Wochentag | Meldungen Mo–Fr; Ereignisse überproportional Sa/So (PHV) |
| Meldehäufung Jahresende | BeHV: Meldungen vor Vertragsablauf (Claims-made) |
| Grossereignisse | Optional 1–2 Kumulereignisse (z. B. Unwetter: Baustellenabsperrung stürzt auf parkierte Autos; Lebensmittelvergiftung bei Firmenanlass mit 20 Geschädigten) |

### 4.5 Betrugsmuster (synthetisch nachbildbar)

Grundannahme: 3–6 % der PHV-Schäden mit Betrugsverdacht (Marktschätzungen liegen zwischen 5 und 10 % über alle Sparten); davon 40 % bestätigt. BHV 2–3 %, BeHV < 1 %. Muster sollen sowohl über strukturierte Daten (Timing, Beträge, Beziehungen) als auch über Dokumente (Formulierungen, Widersprüche) erkennbar sein.

| Nr. | Muster | Beschreibung | Erkennbare Signale (strukturiert) | Erkennbare Signale (Dokumente) | Häufigkeit (Anteil an Betrugsfällen) |
|---|---|---|---|---|---|
| F1 | Gefälligkeitsschaden / Freundschaftsdienst | Eigener Schaden wird als Haftpflichtschaden eines Freundes/Verwandten deklariert ("Mein Kollege hat mein Handy fallen lassen") | Geschädigter mit gleicher Adresse oder gleichem Nachnamen wie VN; Geschädigter ist selbst VN bei Pfefferminzia mit eigenem Schaden kurz davor; hochwertiges Gerät, kurz vor Ende Garantie; Schaden am Wochenende | Schilderung vage, keine Zeugen; Rechnung des Geräts auf Geschädigten, aber Kaufdatum lange her; identische Formulierung in Meldung VN und Bestätigung Geschädigter (copy-paste) | 30 % |
| F2 | Rückdatierung / Schaden vor Vertragsbeginn | Schaden ereignete sich vor Vertragsbeginn oder während Deckungsunterbruch; Schadendatum wird verschoben | Schadendatum ≤ 14 Tage nach Vertragsbeginn; Schadendatum genau nach Ende der Suspension; Kostenvoranschlag datiert vor Schadendatum | Widersprüchliche Datumsangaben zwischen Meldung, Rechnung, Foto-Metadaten; Handwerkerrechnung mit Auftragsdatum vor Schadendatum | 15 % |
| F3 | Überhöhte Forderung / Wertsteigerung | Tatsächlicher Schaden, aber Neuwert statt Zeitwert, zusätzliche nicht betroffene Gegenstände, Fantasiepreise | Forderung > 90 %-Quantil der Schadenart; Anzahl Positionen hoch; Kostenvoranschlag ohne Firmenangaben; Betrag glatt (z. B. 2'000.00) | Mehrere Positionen ohne Belege; Rechnung ohne MwSt-Nummer/UID; Preis über Marktpreis; nachgeschobene Positionen im zweiten Schreiben | 20 % |
| F4 | Mehrfachmeldung / Doppelversicherung | Gleicher Schaden bei zwei Versicherern (Haftpflicht + eigene Hausrat/Elektronikversicherung) oder zweimal bei Pfefferminzia unter zwei Verträgen | Gleicher Geschädigter/Gegenstand in zwei Schäden; identische Fotos (Hash); Meldung unter altem und neuem Vertrag nach Migration | Identische Fotos, identische Rechnung; Hinweis des Geschädigten "hab ich auch bei meiner Versicherung gemeldet" | 8 % |
| F5 | Serientäter / Netzwerk | VN meldet 3+ Schäden in 24 Monaten, oft mit wechselnden Geschädigten aus einem Bekanntenkreis; Geschädigter tritt in mehreren Schäden verschiedener VN auf | Schadenanzahl pro VN hoch; Geschädigter-Identität in > 1 Schaden; gleiche IBAN in mehreren Schäden; gleiche Werkstatt/Reparaturfirma | Wiederkehrende Formulierungen, gleiche Handschrift auf Formularen, gleiche E-Mail-Domain | 10 % |
| F6 | Verschleierung Vorsatz / Eigenschaden | Vorsätzliche Beschädigung (Streit, Wut) als Unfall gemeldet; oder eigene Sache als fremde deklariert | Ereignis "Streit", Polizeirapport mit Vorsatz, Zeitpunkt nachts | Polizeirapport widerspricht Meldung ("im Streit geworfen" vs. "versehentlich gestossen"); Zeugenaussage abweichend | 7 % |
| F7 | Kollusion mit Dienstleister | Handwerker/Werkstatt stellt überhöhte oder fiktive Rechnung, teilt mit VN/Geschädigtem | Gleiche Dienstleister-UID/USt-IdNr. in überdurchschnittlich vielen Schäden; Rechnungsbetrag stets knapp unter Vollmachtsgrenze (z. B. 4'900 bei Grenze 5'000) | Rechnungslayout inkonsistent, fehlende Adressdaten, Rechnungsnummern nicht fortlaufend | 5 % |
| F8 | Fingierter Personenschaden | Übertriebene Verletzung (HWS-Schleudertrauma nach Bagatellkollision), Arbeitsunfähigkeit ohne objektiven Befund | AU-Dauer lang bei geringem Sachschaden; Arzt wechselt; keine Erstbehandlung am Unfalltag | Arztzeugnis ohne Befund, Anwalt eingeschaltet vor Erstbehandlung, Forderung für "Haushaltsschaden" ohne Nachweis | 3 % |
| F9 | Falsche Risikoangaben (Antragsbetrug, BHV/BeHV) | Umsatz/Lohnsumme zu tief angegeben, Tätigkeit verschwiegen (z. B. Dachdeckerarbeiten bei "Malerbetrieb") | Schaden aus nicht deklarierter Tätigkeit; Umsatzmeldung deutlich unter Handelsregister-/Bilanzdaten | Schadenschilderung nennt Tätigkeit, die nicht in Betriebsbeschreibung steht | 2 % (aber didaktisch wertvoll: Anzeigepflicht) |

Für Betrugserkennungs-Übungen sollte der Datensatz ein Label `betrug_status` (kein Verdacht / Verdacht / bestätigt / ausgeräumt) führen, das den Teilnehmenden nur in einem Trainingsanteil sichtbar ist. Wichtig: auch "ehrliche" Schäden müssen einzelne Betrugssignale aufweisen (z. B. glatte Beträge, Meldung kurz nach Vertragsbeginn), damit Modelle nicht triviale Regeln lernen (False-Positive-Diskussion).

---

## 5. Dokumenttypen (unstrukturiert)

### 5.1 Übersicht und Klassifikation

Jedes Dokument sollte im Datensatz mit Metadaten versehen sein: `dokument_id`, `dokument_typ` (Codeliste unten), `format`, `sprache` (de/fr/it), `land`, `erstelldatum`, `eingangsdatum`, `absender_typ`, `bezug` (Vertrag/Schaden/Offerte), `seitenzahl`, `qualitaet` (sauber / gescannt / handschriftlich / Foto-von-Dokument), `system_herkunft` (PFEFFER/400 / MINT / Posteingang / Portal). Für Extraktionsübungen sollte ein Teil der Dokumente ein Ground-Truth-JSON mit den enthaltenen Feldern haben.

### 5.2 Vertragsdokumente

| Code | Dokumenttyp | Inhalt | Typische Länge | Format | Varianten / Bemerkungen |
|---|---|---|---|---|---|
| `V01` | Offerte / Angebot | Kopf mit Offertnummer, Kundendaten, Produkt, Varianten-Tabelle (Deckungssumme, SB, Prämie), Gültigkeit, Vermittlerangaben, Hinweis auf AVB und Kundeninformation | 2–4 Seiten | PDF (Systemdruck) | CH: mit "Kundeninformation nach Art. 3 VVG" als Anhang; DE: mit IPID; Broker-Offerten teils als E-Mail-Text |
| `V02` | Antrag / Antragsformular | Personalien VN, mitversicherte Personen, Adresse, Produkt, Deckungsvarianten, Bausteine, Vorversicherung, Vorschäden (5 Jahre), Risikofragen, Zahlweise/Bankverbindung, Datenschutzhinweis, Unterschriften, Belehrung (DE § 19 Abs. 5 VVG) | PHV 2–3 Seiten; BHV 4–6 Seiten; BeHV 6–10 Seiten | PDF-Formular (digital ausgefüllt), gescanntes Papierformular (teils handschriftlich), Portal-Export (JSON + PDF) | 25 % gescannt, davon 10 % handschriftlich mit schlechter Lesbarkeit; Stolperstein: Vorschäden-Feld leer statt "keine" |
| `V03` | Betriebsbeschreibung / Risikofragebogen (BHV/BeHV) | Tätigkeitsbeschreibung Freitext, Branchenzuordnung, Umsatz/Lohnsumme, Mitarbeitende, Subunternehmer, Auslandanteil, Produkte, Maschinen, Qualitätsmanagement, bisherige Schäden, spezifische Fragen (Asbest, Sprengarbeiten, USA-Export) | 3–8 Seiten | PDF-Formular, Word-Dokument (Broker), E-Mail | Freitext ist Basis für UW-Assistenz-Übungen (Klassifikation Branchencode aus Text) |
| `V04` | Beratungsprotokoll (DE) / Beratungsdokumentation | Anlass, Wünsche und Bedürfnisse des Kunden, Empfehlung mit Begründung, Verzicht auf Beratung (falls), Unterschriften | 1–3 Seiten | PDF, teils handschriftlich | Nur DE; CH: nur bei Broker-Mandaten "Beratungsdokumentation" freiwillig |
| `V05` | Produktinformationsblatt / IPID (DE) / Kundeninformation (CH) | Was ist versichert, was nicht, Einschränkungen, Pflichten, Zahlung, Beginn/Ende, Kündigung | IPID 2 Seiten; Kundeninformation CH 2–4 Seiten; Produktinformationsblatt DE 3–5 Seiten | PDF | Standardisiertes Layout; gut für Vergleich mit AVB (Widersprüche einbauen: IPID nennt Sublimit, das in alter AVB-Generation anders ist) |
| `V06` | Police / Versicherungsschein | Policennummer, VN, Adresse, versicherte Personen/Betrieb, Produkt und Bedingungsgeneration, Deckungssummen, Sublimits, Selbstbehalt, Bausteine, Laufzeit, Prämie (netto, Stempelsteuer CH 5 % / Versicherungsteuer DE 19 %, brutto), Zahlweise, Klauseln, Hinweis auf AVB | 2–5 Seiten (BeHV bis 8) | PDF Systemdruck; Altbestand: Scan der Papierpolice (PFEFFER/400-Layout, monospace) | Zwei Layouts (Alt/Neu) mit unterschiedlicher Feldanordnung; Altpolicen ohne Sublimit-Tabelle |
| `V07` | Allgemeine Versicherungsbedingungen (AVB CH / AHB DE) | Siehe Kapitel 7 | CH PHV 12–18 Seiten; BHV 20–30; BeHV 18–25; DE AHB 12–16 + BBR 15–30 | PDF, mehrspaltig, Ziffern-Gliederung | Pro Generation eine Version; FR/IT-Übersetzungen für CH (mind. FR) |
| `V08` | Besondere Bedingungen / Zusatzbedingungen / Klauseln | Bausteinbedingungen (Tierhalter, Bauherren, Öltank, Produkt, Umwelt), Berufsgruppen-Bedingungen, individuelle Klauseln (Ausschluss bestimmter Tätigkeiten, Zuschlagsvereinbarung) | 1–6 Seiten je Baustein | PDF | Klausel-Codes (z. B. `KL-CH-017 Ausschluss Dachdeckerarbeiten`) auf Police referenziert |
| `V09` | Nachtrag / Nachtragspolice | Nachtragsnummer, Wirksamkeitsdatum, Änderungsgrund, Tabelle "bisher / neu", Prämienänderung, Hinweis "übrige Bestimmungen unverändert" | 1–3 Seiten | PDF | Kette von Nachträgen ermöglicht "Welcher Zustand galt am Schadendatum?"-Aufgaben |
| `V10` | Deckungsbestätigung / Versicherungsbestätigung | Kurzbestätigung für Dritte (Vermieter, Auftraggeber, Bauherr, Behörde bei Hundehalterpflicht) | 1 Seite | PDF, Brief | DE: "Versicherungsbestätigung für Bauamt/Kammer"; CH: "Versicherungsnachweis" |
| `V11` | Prämienrechnung / Beitragsrechnung | Rechnungsnummer, Periode, Prämie netto, Steuer/Stempelabgabe, brutto, Fälligkeit, Zahlungsinformation | 1–2 Seiten | PDF; CH mit QR-Zahlteil; DE mit SEPA-Hinweis oder Überweisungsdaten | Ratenzahlung: Teilrechnungen mit Ratenzuschlag 3–5 % |
| `V12` | Zahlungserinnerung / Mahnung | Stufe 1 (freundlich), Stufe 2 (qualifizierte Mahnung mit Rechtsfolgen: CH Art. 20 VVG, DE § 38 VVG), Stufe 3 (Inkasso/Betreibungsandrohung) | 1 Seite | PDF, Brief (eingeschrieben bei Stufe 2 CH) | Rechtsfolgenbelehrung muss exakt sein; Stolperstein: fehlerhafte Mahnung (falsche Frist) → Deckungsunterbruch unwirksam |
| `V13` | Mitteilung Deckungsunterbruch / Leistungsfreiheit | Hinweis, dass Deckung ruht ab Datum; Wiederinkraftsetzung nach Zahlung | 1 Seite | Brief | CH-typisch; DE: Kündigung nach § 38 Abs. 3 VVG |
| `V14` | Kündigungsschreiben VN | Formlos: "Hiermit kündige ich meine Haftpflichtversicherung Nr. ... per ..." – oft ohne Policennummer, mit falschem Datum, mit Begründung (Wechsel, Preis, Wegzug, Tod) | 0.5–1 Seite | Brief (gescannt, handschriftlich 20 %), E-Mail, Portal-Formular, Fax (Altbestand) | Häufige Fehler: Frist verpasst, Vertrag nicht eindeutig, Unterschrift fehlt |
| `V15` | Kündigungsbestätigung / Kündigungsablehnung | Bestätigung Beendigungsdatum oder Hinweis auf Fristversäumnis mit nächstmöglichem Termin | 1 Seite | PDF Brief | |
| `V16` | Kündigung durch Versicherer | Kündigung im Schadenfall, wegen Prämienverzug, wegen Anzeigepflichtverletzung (mit Begründung, Rechtsgrundlage) | 1–2 Seiten | Brief eingeschrieben | Rechtsgrundlagen-Zitat prüfen (RAG-Aufgabe) |
| `V17` | Aufhebungsvereinbarung / Storno-Mitteilung | Einvernehmliche Aufhebung (Wegzug, Tod, Doppelversicherung), Rückerstattung | 1 Seite | Brief | |
| `V18` | Vollmacht / Maklervollmacht / Maklermandat | VN bevollmächtigt Vermittler zur Vertretung; Umfang (Korrespondenz, Kündigung, Schadenmeldung) | 1–2 Seiten | PDF, Scan | DE: Maklervollmacht; CH: Brokermandat mit Courtage-Vereinbarung |
| `V19` | Umsatz-/Lohnsummenmeldung (BHV/BeHV) | Jahresmeldung Umsatz/Lohnsumme/Honorare je Sparte; oft mit Bilanzauszug | 1–2 Seiten | Formular, E-Mail, Excel-Anhang | Stolperstein: Meldung abweichend von HR-Daten |
| `V20` | Korrespondenz allgemein (Vertrag) | E-Mails, Briefe: Fragen zu Deckung ("Ist mein E-Bike versichert?"), Adressänderung, Beschwerden, Auskunftsbegehren (DSG/DSGVO), Anfrage Ombudsstelle | 0.5–2 Seiten | E-Mail (mit Threads), Brief | Deckungsanfragen sind ideale RAG-Testfälle |
| `V21` | Vorversicherer-Auskunft / Schadenfreiheitsbescheinigung | Bestätigung Vorversicherungszeit, Schäden der letzten 5 Jahre | 1 Seite | Brief, PDF | DE: HIS-Auskunft; CH: direkte Anfrage |
| `V22` | Bonitäts-/Sanktionsprüfung (intern) | Betreibungsauskunft (CH), Schufa (DE), Sanktionslisten-Treffer | 1–3 Seiten | PDF | Nur intern, nie an Kunden |

### 5.3 Schadendokumente

| Code | Dokumenttyp | Inhalt | Typische Länge | Format | Varianten / Bemerkungen |
|---|---|---|---|---|---|
| `S01` | Schadenmeldung VN (Formular) | Policennummer, VN, Schadendatum/-zeit/-ort, Ereignisbeschreibung Freitext, Geschädigter (Name, Adresse, Kontakt), Art des Schadens, geschätzte Höhe, Zeugen, Polizei ja/nein, Verschuldensfrage ("Wer ist Ihrer Meinung nach schuld?"), Unterschrift | 2–3 Seiten | PDF-Formular, gescannt (30 % handschriftlich), Portal-Formular (strukturiert + Freitext), App (Foto + Kurztext) | Herzstück für Klassifikation; Freitext 50–400 Wörter; Qualität variiert stark |
| `S02` | Schadenmeldung per E-Mail / Telefonnotiz | Unstrukturierte Erstmeldung: "Guten Tag, mir ist gestern beim Kollegen ..."; Telefonnotiz vom Contact Center in Stichworten mit Abkürzungen | 0.3–1 Seite | E-Mail, interner Notiztext | Telefonnotizen mit Tippfehlern, Abkürzungen (VN, GS, SD, "lt. VN") |
| `S03` | Anspruchsschreiben Geschädigter (Schadenanzeige Dritter) | Geschädigter schildert Ereignis, macht Forderung geltend, Frist zur Stellungnahme, Bankverbindung, Beilagen | 1–2 Seiten | Brief (gescannt), E-Mail | Ton von höflich bis aggressiv; Forderung teils ohne Belege; Stolperstein: Geschädigter schreibt direkt an Versicherer ohne dass VN gemeldet hat |
| `S04` | Anwaltsschreiben Geschädigtenvertreter | Vollmachtsanzeige, Sachverhalt, Haftungsgrundlage (OR 41 / BGB 823 zitiert), Schadenspositionen (Sachschaden, Heilungskosten, Erwerbsausfall, Genugtuung/Schmerzensgeld, Haushaltsschaden, Anwaltskosten), Fristsetzung, Verjährungsverzicht-Forderung | 2–6 Seiten | PDF/Brief mit Kanzleibriefkopf | Juristische Sprache; CH: "Genugtuung", DE: "Schmerzensgeld"; Extraktionsziel: Positionen-Tabelle |
| `S05` | Stellungnahme VN / Sachverhaltsschilderung | Antwort des VN auf Rückfragen: detaillierte Schilderung, eigene Sicht zur Schuldfrage, Angaben zu Zeugen | 0.5–2 Seiten | E-Mail, Brief, Formular | Widersprüche zur Erstmeldung bewusst einbauen |
| `S06` | Fotos | Beschädigte Sache, Schadenort, Verletzung, Dokumente abfotografiert | 1–10 Bilder | JPEG/HEIC, mit/ohne EXIF (Datum, GPS) | EXIF-Datum vs. behauptetes Schadendatum als Betrugssignal; Bildqualität variabel; im Lehrdatensatz ggf. synthetisch/generiert oder Platzhalter mit Metadaten |
| `S07` | Kostenvoranschlag / Offerte Reparatur | Handwerker/Werkstatt/Fachgeschäft: Positionen, Stundenansätze, Material, MwSt, Firmenangaben (UID CH / USt-IdNr DE) | 1–2 Seiten | PDF, Scan, Foto | Layout je Firma unterschiedlich; Extraktionsziel: Total, Positionen, Datum, Firma |
| `S08` | Rechnung / Quittung | Reparaturrechnung, Ersatzkauf-Beleg (Kassenzettel), Arztrechnung, Apothekenquittung, Reinigungsrechnung | 1 Seite | PDF, Scan, Foto (Kassenzettel ausgeblichen) | Kaufbelege für Zeitwertberechnung (Kaufdatum, Preis) |
| `S09` | Gutachten Sachverständiger (Sach) | Auftrag, Besichtigungsdatum, Objektbeschreibung, Schadenursache, Schadenumfang, Reparaturkosten vs. Zeitwert, Abzug neu für alt, Fotos, Zusammenfassung | 5–20 Seiten | PDF | Bau-/Wasserschaden-Gutachten, Elektronik-Gutachten, Kfz-Gutachten (Fremdfahrzeug beschädigt) |
| `S10` | Medizinisches Gutachten / Arztbericht / Arztzeugnis | Diagnose (ICD-10), Behandlungsverlauf, Arbeitsunfähigkeit (% und Dauer), Prognose, Dauerschaden, Kausalitätsbeurteilung | Arztzeugnis 1 Seite; Bericht 2–5 Seiten; Gutachten 10–40 Seiten | PDF, Scan | Sensible Daten: im Datensatz mit fiktiven Diagnosen; CH: Unfallmeldung UVG als Beilage; DE: Durchgangsarztbericht (bei Arbeitsunfall) |
| `S11` | Polizeirapport / Unfallprotokoll | Ereignis, Beteiligte, Zeugen, Sachverhalt aus Polizeisicht, Bussen, Verzeigung | 2–6 Seiten | PDF (gescannt, teils geschwärzt) | CH: "Polizeirapport" kantonal; DE: "Unfallaufnahme", "Ermittlungsakte" (Akteneinsicht über Anwalt); Widerspruch zu Meldung möglich |
| `S12` | Zeugenaussage / Bestätigung Dritter | Kurzschreiben von Zeugen; Bestätigung des Geschädigten über Hergang | 0.5–1 Seite | E-Mail, handschriftlich | F1-Betrug: identischer Wortlaut wie Meldung |
| `S13` | Deckungszusage / Deckungsvorbehalt / Deckungsablehnung (an VN) | Bezug auf Schaden und Police, Ergebnis der Deckungsprüfung, AVB-Ziffer zitiert, Selbstbehalt, weiteres Vorgehen; bei Ablehnung Begründung und Rechtsmittelhinweis (Ombudsstelle) | 1–2 Seiten | PDF Brief | Ablehnungsgründe: Ausschluss (beruflich, Vorsatz, eigene Sache, Angehörige), kein Vertrag, Deckungsunterbruch, verspätete Meldung |
| `S14` | Schreiben an Geschädigten (Haftung) | Anerkennung dem Grunde nach, Teilanerkennung mit Quote, Ablehnung mit Begründung (kein Verschulden, Mitverschulden, Verjährung), Zahlungsankündigung, Bitte um Unterlagen | 1–2 Seiten | PDF Brief | "Ohne Anerkennung einer Rechtspflicht" (Kulanz) als Sonderfall |
| `S15` | Vergleichsvereinbarung / Abfindungserklärung | Parteien, Schadenereignis, Vergleichsbetrag, Saldoklausel ("per Saldo aller Ansprüche"), Vorbehalt Nachforderung bei Personenschaden (Verschlimmerung), Unterschriften | 1–3 Seiten | PDF, unterschrieben gescannt | DE: "Abfindungserklärung"; CH: "Saldovereinbarung" |
| `S16` | Zahlungsavis / Zahlungsmitteilung | Betrag, Empfänger, IBAN, Verwendungszweck, Abzug Selbstbehalt, Zeitwertberechnung | 1 Seite | PDF Brief | Verknüpfung zu Zahlungsdaten |
| `S17` | Regressforderung eingehend | Sozialversicherer (SUVA/Krankenkasse/AHV-IV in CH; Berufsgenossenschaft/Krankenkasse/DRV in DE) oder anderer Versicherer fordert Leistungen zurück; Aufstellung Leistungen, Rechtsgrundlage (ATSG Art. 72 / SGB X § 116), Zahlungsfrist | 2–5 Seiten | Brief, PDF mit Leistungsaufstellung (Tabelle) | Tabellenextraktion; DE: Teilungsabkommen-Abrechnung (pauschale Quote) |
| `S18` | Regressschreiben ausgehend | Pfefferminzia fordert von Drittem/dessen Versicherer Anteil zurück | 1–2 Seiten | PDF Brief | |
| `S19` | Interne Schadennotiz / Aktennotiz / Bearbeitungsjournal | Chronologische Einträge des Sachbearbeiters: Telefonate, Einschätzungen, Reserveänderungen, To-dos; Kürzel und Fachjargon ("Hftg. dem Grunde nach bejaht, Quote 2/3, Res. auf 12k erhöht") | 0.2–3 Seiten kumuliert | Systemtext (Journal), Word-Notiz | Sehr wertvoll für Summarization-Übungen; enthält subjektive Einschätzungen und Betrugsverdacht-Vermerke |
| `S20` | Interne Haftungs-/Deckungsbeurteilung (Memo) | Strukturiertes juristisches Memo: Sachverhalt, Deckung, Haftung, Quantum, Empfehlung, Vollmachtsstufe | 1–4 Seiten | Word/PDF | Bei komplexen/grossen Schäden; Vorlage für Zusammenfassungs- und Entscheidungs-Assistenz |
| `S21` | Reserveprotokoll / Grossschadenmeldung | Bei Reserve > Schwelle (CH 100'000 / DE 100'000): Meldung an Grossschadenkomitee/Rückversicherer mit Sachverhalt, Reservebegründung, Prognose | 1–3 Seiten | PDF Formular | |
| `S22` | Klageschrift / Klageantwort / Urteil | Prozessdokumente bei Abwehr: Rechtsbegehren, Sachverhalt, Beweismittel, Urteil mit Erwägungen | 10–40 Seiten | PDF | Nur wenige (5–10) im Datensatz, z. B. gekürzt; CH: Bezirksgericht/Kantonsgericht; DE: Amtsgericht/Landgericht |
| `S23` | Anwaltsrechnung / Gutachterrechnung (Kosten) | Honorarnote nach Stunden/Tarif (DE: RVG-Gebühren; CH: Stundenansatz oder kantonaler Tarif), Spesen, MwSt | 1–2 Seiten | PDF | Kostenart-Klassifikation |
| `S24` | Betrugsprüfungsbericht (intern) | Verdachtsmomente, durchgeführte Abklärungen (Recherche, Befragung, Detektiv), Ergebnis, Empfehlung (Ablehnung, Strafanzeige, Zahlung) | 2–6 Seiten | PDF/Word | Nur bei bestätigten/ausgeräumten Verdachtsfällen |
| `S25` | Beschwerde / Ombudsstelle | VN oder Geschädigter beschwert sich über Ablehnung/Verzögerung; Anfrage der Ombudsstelle (CH: Ombudsman der Privatversicherung; DE: Versicherungsombudsmann e.V.) | 1–3 Seiten | Brief, E-Mail | Sentiment-/Eskalationsanalyse |
| `S26` | Abschlussschreiben | Mitteilung an VN: Schaden abgeschlossen, Gesamtaufwand, Auswirkungen (Selbstbehalt eingefordert, Kündigungsrecht) | 1 Seite | PDF Brief | |
| `S27` | Schadenmeldung an Rückversicherer | Bei Grossschäden über Priorität (z. B. CHF/EUR 1 Mio.) | 1–2 Seiten | PDF Formular | Optional |

### 5.4 Dokumentmengen (Vorschlag pro 1'000 Schäden bzw. Verträge)

| Bezug | Dokumenttyp | Anzahl pro 1'000 | Hinweis |
|---|---|---|---|
| Vertrag | V02 Antrag | 1'000 | 1 pro Vertrag |
| Vertrag | V06 Police | 1'000 + Nachtragspolicen | |
| Vertrag | V09 Nachtrag | 300 (PHV) / 1'200 (BHV) | |
| Vertrag | V11 Rechnung | 1'000–4'000 | Je nach Zahlweise und Laufzeit |
| Vertrag | V12 Mahnung | 80–120 | |
| Vertrag | V14 Kündigung VN | 60–130 | |
| Vertrag | V20 Korrespondenz | 400 | |
| Schaden | S01/S02 Meldung | 1'000 | Mix 45 % Formular, 30 % Portal, 25 % E-Mail/Telefon |
| Schaden | S03 Anspruchsschreiben | 700 | |
| Schaden | S04 Anwaltsschreiben | 120 (PHV) / 250 (BHV) / 800 (BeHV) | |
| Schaden | S06 Fotos | 2'500 | |
| Schaden | S07/S08 KV/Rechnung | 1'400 | |
| Schaden | S09 Sachgutachten | 60 | |
| Schaden | S10 Arztbericht | 140 | Bei Personenschäden |
| Schaden | S11 Polizeirapport | 50 | |
| Schaden | S13 Deckungsentscheid | 1'000 | |
| Schaden | S14 Haftungsschreiben | 900 | |
| Schaden | S15 Vergleich | 80 | |
| Schaden | S17 Regressforderung | 60 | |
| Schaden | S19 Aktennotiz | 1'000 (Journal je Schaden, 3–25 Einträge) | |
| Schaden | S20 Memo | 40 | |
| Schaden | S24 Betrugsbericht | 15 | |

---

## 6. Datenelemente (strukturiert)

Legende: Typ (str = Text, int, dec = Dezimal, date, datetime, bool, enum = Codeliste, fk = Fremdschlüssel). Spalte "CH/DE": *beide* (identisch), *CH*, *DE*, *variiert* (Feld existiert in beiden, Wertebereich unterschiedlich).

### 6.1 Entität `versicherungsnehmer` (Partner)

| Feld | Typ | Wertebereich / Codeliste | Beispiel | CH/DE |
|---|---|---|---|---|
| `partner_id` | str (PK) | `P-CH-000123456` / `P-DE-000123456`; Altbestand: 8-stellig numerisch aus PFEFFER/400 | `P-CH-000481223` | variiert (Präfix) |
| `partner_typ` | enum | `natuerlich`, `juristisch` | `natuerlich` | beide |
| `anrede` | enum | `Herr`, `Frau`, `Firma`, `keine`, `Divers` (DE) | `Frau` | variiert |
| `vorname` | str | | `Corinne` | beide |
| `nachname` / `firmenname` | str | | `Brunner-Aeschlimann` | beide |
| `geburtsdatum` | date | 1930–2008 (VN volljährig) | `1979-04-12` | beide |
| `geschlecht` | enum | `m`, `w`, `d`, `unbekannt` | `w` | beide |
| `nationalitaet` | str (ISO 3166) | | `CH`, `DE`, `IT`, `TR` | beide |
| `sprache_korrespondenz` | enum | `de`, `fr`, `it`, `en` | `fr` | variiert (DE: nur `de`, `en`) |
| `strasse` | str | | `Bahnhofstrasse 17` / `Kölner Straße 17` | variiert (Schreibweise) |
| `plz` | str | CH 4-stellig (1000–9658), DE 5-stellig (01067–99998) | `8400` / `50667` | variiert |
| `ort` | str | | `Winterthur` / `Köln` | beide |
| `kanton` / `bundesland` | enum | CH: 26 Kantonskürzel; DE: 16 Bundesländer | `ZH` / `NW` | variiert |
| `land` | enum | `CH`, `DE`, `LI`, `AT`, andere | `CH` | beide |
| `email` | str | | `c.brunner@example.ch` | beide |
| `telefon` | str | +41 / +49 | `+41 52 000 00 00` | variiert |
| `zivilstand` | enum | `ledig`, `verheiratet`, `eingetragene_partnerschaft`, `geschieden`, `verwitwet`, `konkubinat` | `verheiratet` | beide |
| `beruf` | str | Freitext / ISCO-Code | `Pflegefachfrau` | beide |
| `berufsgruppe_tarif` | enum | `normal`, `oeffentlicher_dienst`, `student`, `rentner` | `oeffentlicher_dienst` | DE (Rabattmerkmal), CH kaum |
| `rechtsform` | enum (juristisch) | CH: `AG`, `GmbH`, `Einzelfirma`, `Kollektivgesellschaft`, `Verein`, `Stiftung`; DE: `GmbH`, `UG`, `AG`, `e.K.`, `GbR`, `OHG`, `KG`, `e.V.` | `GmbH` | variiert |
| `uid` / `handelsregisternummer` | str | CH: `CHE-123.456.789`; DE: `HRB 12345` + Registergericht | `CHE-104.556.221` | variiert |
| `ust_id` | str | DE: `DE123456789`; CH: UID mit MWST-Suffix | `DE812345678` | variiert |
| `branche_code` | str | CH: NOGA 2008 (6-stellig); DE: WZ 2008 (5-stellig) | `432200` (Sanitär) / `43.22.0` | variiert |
| `kunde_seit` | date | 1985–heute | `2009-11-01` | beide |
| `kundensegment` | enum | `standard`, `premium`, `jung`, `kmu`, `freier_beruf` | `kmu` | beide |
| `vermittler_id` | fk | Vermittlerstamm | `VM-CH-0412` | beide |
| `kanal_erstkontakt` | enum | `agentur`, `broker`, `online`, `portal`, `telefon`, `bestand_pfefferminz` | `broker` | beide |
| `datenschutz_einwilligung_marketing` | bool | | `false` | beide |
| `bonitaet_status` | enum | `ok`, `betreibung` (CH), `negativmerkmal` (DE), `unbekannt` | `ok` | variiert |
| `sanktionspruefung_datum` | date | | `2024-02-01` | beide |
| `partner_status` | enum | `aktiv`, `inaktiv`, `verstorben`, `dublette` | `aktiv` | beide |
| `dublette_von` | fk | Verweis auf führenden Partner | `P-CH-000381777` | beide (Stolperstein Migration) |
| `system_herkunft` | enum | `PFEFFER400`, `MINT` | `PFEFFER400` | beide |

### 6.2 Entität `vertrag`

| Feld | Typ | Wertebereich / Codeliste | Beispiel | CH/DE |
|---|---|---|---|---|
| `vertrag_id` / `policennummer` | str (PK) | Neu: `H-CH-2023-0004521` / `H-DE-2023-0004521`; Alt: `40.123.456-7` (PFEFFER/400) | `H-CH-2022-0018834` | variiert |
| `policennummer_alt` | str | Altsystemnummer bei migrierten Verträgen | `40.987.112-3` | beide |
| `partner_id` | fk | | | beide |
| `produkt_code` | enum | `PHV`, `BHV`, `BEHV` | `PHV` | beide |
| `produktgeneration` | enum | `PFM-K`, `PFM-M`, `PFZ-2021`, `PFZ-2023` | `PFM-M` | beide |
| `bedingungen_version` | str | z. B. `AVB-PHV-CH-2017-01`, `AHB-2008/BBR-PHV-DE-2015` | `AVB-PHV-CH-2017-01` | variiert |
| `land` | enum | `CH`, `DE` | | beide |
| `waehrung` | enum | `CHF`, `EUR` | | variiert |
| `vertragsbeginn` | date | 1995–heute | `2017-04-01` | beide |
| `vertragsablauf` / `hauptfaelligkeit` | date | | `2027-04-01` | beide |
| `laufzeit_jahre` | int | CH: 1, 3, 5; DE: 1, 3 | `5` | variiert |
| `verlaengerung_stillschweigend` | bool | | `true` | beide |
| `kuendigungsfrist_monate` | int | 3 | `3` | beide |
| `vertragsstatus` | enum | siehe 3.3 | `AKT` | beide |
| `status_seit` | date | | | beide |
| `beendigungsdatum` | date | | | beide |
| `beendigungsgrund` | enum | `kuendigung_vn`, `kuendigung_vr_schaden`, `kuendigung_vr_praemie`, `kuendigung_vr_anzeigepflicht`, `ruecktritt`, `widerruf`, `aufhebung_einvernehmlich`, `tod`, `wegzug`, `betriebsaufgabe`, `doppelversicherung`, `ersatz_neuvertrag` | `kuendigung_vn` | beide |
| `personenkreis` | enum (PHV) | `einzel`, `familie`, `paar` (DE) | `familie` | variiert |
| `deckungssumme_personen_sach` | dec | CH: 3'000'000 (alt), 5'000'000, 10'000'000; DE: 3, 5, 10, 20, 50 Mio. | `5000000` | variiert |
| `deckungssumme_vermoegen` | dec | CH: 100'000–5'000'000; DE: 100'000–2'000'000 | `100000` | variiert |
| `jahresmaximum_faktor` | int | 1, 2 | `2` | beide |
| `selbstbehalt` | dec | CH: 0, 100, 200, 500, 1'000, 2'000, 5'000; DE: 0, 150, 250, 500, 1'000, 2'500, 5'000 | `200` | variiert |
| `selbstbehalt_typ` | enum | `fix`, `prozent_min` (z. B. 10 % min. 1'000) | `fix` | beide |
| `bausteine` | list[enum] | `tierhalter_hund`, `tierhalter_pferd`, `bauherr`, `oeltank`, `gebaeude`, `produkt`, `umwelt`, `rueckruf`, `ausfalldeckung` (DE), `schluesselverlust_erweitert` (DE), `deliktunfaehige_kinder` (DE), `drohne`, `it_datenschutz` | `["tierhalter_hund","gebaeude"]` | variiert |
| `klauseln` | list[str] | Klausel-Codes | `["KL-CH-017"]` | beide |
| `praemie_netto_jahr` | dec | | `168.40` | beide |
| `steuer_satz` | dec | CH Stempelabgabe 5 % (Haftpflicht); DE Versicherungsteuer 19 % | `0.05` / `0.19` | variiert |
| `praemie_brutto_jahr` | dec | | `176.80` | beide |
| `zahlweise` | enum | `jaehrlich`, `halbjaehrlich`, `vierteljaehrlich`, `monatlich` | `jaehrlich` | beide |
| `ratenzuschlag_pct` | dec | 0, 2, 3, 5 | `0` | beide |
| `zahlungsart` | enum | `rechnung`, `lsv` (CH), `ebill` (CH), `sepa_lastschrift` (DE), `kreditkarte` | `rechnung` | variiert |
| `iban` | str | CH: `CH..` 21 Zeichen; DE: `DE..` 22 Zeichen | `CH93 0076 2011 6238 5295 7` | variiert |
| `vermittler_id` | fk | | | beide |
| `vermittler_typ` | enum | `agentur`, `broker`, `makler`, `portal`, `direkt` | | variiert |
| `courtage_pct` | dec | 10–20 % | `15` | beide |
| `vorversicherer` | str | | `Zürich`, `Allianz`, `keine` | beide |
| `vorschaeden_anzahl_antrag` | int | 0–5 | `1` | beide |
| `vorschaeden_freitext_antrag` | str | | `2019 Wasserschaden Mietwohnung ca. 3'000` | beide |
| `anzeigepflicht_belehrung` | bool | | `true` | DE (Pflichtfeld), CH optional |
| `beratungsprotokoll_vorhanden` | bool | | `true` | DE |
| `underwriting_status` | enum | `automatisch`, `manuell_angenommen`, `mit_auflagen`, `abgelehnt` | `automatisch` | beide |
| `underwriting_zuschlag_pct` | dec | 0–100 | `0` | beide |
| `risikoscore_mint` | dec | 0.0–1.0 (nur Verträge ab 2021) | `0.23` | beide |
| `buendelrabatt_pct` | dec | 0–15 | `10` | beide |
| `mahnstufe_aktuell` | int | 0–3 | `0` | beide |
| `deckungsunterbruch_von` / `_bis` | date | | | beide |
| `nachhaftung_bis` | date | BeHV | | beide |
| `deckungsprinzip` | enum (BeHV) | `verstoss`, `claims_made` | `verstoss` | beide |
| `rueckwaertsdeckung_ab` | date (BeHV claims-made) | | | beide |
| `erstellt_am`, `geaendert_am` | datetime | | | beide |
| `system_herkunft` | enum | `PFEFFER400`, `MINT` | | beide |
| `migriert_am` | date | | `2022-09-15` | beide |

### 6.3 Entität `risiko` (produktspezifische Risikodaten, 1:n zu Vertrag)

| Feld | Typ | Wertebereich / Codeliste | Beispiel | CH/DE | Produkt |
|---|---|---|---|---|---|
| `risiko_id` | str (PK) | | `R-0012345` | beide | alle |
| `vertrag_id` | fk | | | beide | alle |
| `risiko_typ` | enum | `haushalt`, `betrieb`, `beruf`, `tier`, `gebaeude`, `bauvorhaben`, `oeltank` | | beide | alle |
| `mitversicherte_personen` | list[obj] | Name, Geburtsdatum, Beziehung (`partner`, `kind`, `hausangestellte`, `au_pair`) | | beide | PHV |
| `anzahl_kinder` | int | 0–6 | `2` | beide | PHV |
| `wohnsituation` | enum | `miete`, `eigentum_wohnung`, `eigentum_haus` | `miete` | beide | PHV |
| `tierart` | enum | `hund`, `katze`, `pferd`, `sonstiges` | `hund` | beide | PHV/B1 |
| `hunderasse` | str | | `Labrador Retriever`, `Rottweiler` | beide | B1 |
| `listenhund` | bool | DE: nach Landesrecht; CH: kantonale Listen | `false` | variiert | B1 |
| `hundehalter_pflicht` | bool | Abgeleitet aus Bundesland/Kanton | `true` | variiert | B1 |
| `gebaeude_typ` | enum | `efh`, `zfh`, `mfh`, `ferienhaus` | | beide | B5 |
| `gebaeude_vermietet` | bool | | | beide | B5 |
| `oeltank_liter` | int | 500–20'000 | `3000` | beide | B3 |
| `bausumme` | dec | ≤ 100'000 (CH) / ≤ 50'000 (DE) im Baustein | `80000` | variiert | B2 |
| `betriebsart_text` | str | Freitext aus Antrag | `Sanitär- und Heizungsinstallationen, Kundendienst` | beide | BHV |
| `branche_code` | str | NOGA / WZ | | variiert | BHV |
| `risikoklasse_pfz` | int | 1–6 | `4` | beide | BHV/BeHV |
| `umsatz_jahr` | dec | 50'000–10'000'000 | `1450000` | beide | BHV/BeHV |
| `lohnsumme_jahr` | dec | | `680000` | beide | BHV |
| `anzahl_mitarbeitende` | dec (FTE) | 0.5–50 | `7.5` | beide | BHV/BeHV |
| `anzahl_berufstraeger` | int | 1–15 | `2` | beide | BeHV |
| `honorarsumme_jahr` | dec | | `420000` | beide | BeHV |
| `berufsgruppe` | enum | `architekt`, `bauingenieur`, `treuhaender`, `steuerberater`, `revisor`, `it_dienstleister`, `softwareentwickler`, `unternehmensberater` | `architekt` | beide | BeHV |
| `taetigkeitsschwerpunkte` | list[enum] | z. B. `bauleitung`, `planung`, `revision`, `lohnbuchhaltung`, `softwareentwicklung`, `hosting`, `beratung_mna` | | beide | BeHV |
| `subunternehmer_anteil_pct` | dec | 0–80 | `20` | beide | BHV |
| `auslandanteil_pct` | dec | 0–50 | `5` | beide | BHV/BeHV |
| `export_usa_kanada` | bool | | `false` | beide | BHV |
| `produkte_beschreibung` | str | | | beide | B4 |
| `umsatz_gemeldet_jahr` | dec | Jährliche Meldung; Abweichung zu `umsatz_jahr` als Stolperstein | | beide | BHV/BeHV |
| `umsatz_meldung_datum` | date | | | beide | BHV/BeHV |
| `zertifizierungen` | list[str] | `ISO9001`, `ISO27001`, `SIA-Mitglied`, `Kammermitglied` | | beide | BHV/BeHV |
| `risiko_gueltig_von` / `_bis` | date | Versionierung über Nachträge | | beide | alle |

### 6.4 Entität `nachtrag`

| Feld | Typ | Wertebereich | Beispiel | CH/DE |
|---|---|---|---|---|
| `nachtrag_id` | str (PK) | `vertrag_id` + laufende Nummer | `H-CH-2022-0018834-N03` | beide |
| `vertrag_id` | fk | | | beide |
| `nachtrag_nr` | int | 1–20 | `3` | beide |
| `wirksam_ab` | date | | `2024-07-01` | beide |
| `erstellt_am` | date | | `2024-07-12` (rückwirkend möglich) | beide |
| `aenderungsgrund` | enum | `adresse`, `personenkreis`, `deckungssumme`, `selbstbehalt`, `baustein_zugang`, `baustein_abgang`, `umsatz_anpassung`, `betriebsaenderung`, `vermittlerwechsel`, `zahlweise`, `bedingungsumstellung`, `praemienanpassung`, `klausel` | `baustein_zugang` | beide |
| `aenderung_json` | json | Delta alt/neu | `{"bausteine": {"alt": [], "neu": ["tierhalter_hund"]}}` | beide |
| `praemie_delta_jahr` | dec | | `+62.00` | beide |
| `pro_rata_betrag` | dec | | `+31.00` | beide |
| `ausloeser` | enum | `kunde`, `vermittler`, `versicherer`, `system` | | beide |

### 6.5 Entität `schaden`

| Feld | Typ | Wertebereich / Codeliste | Beispiel | CH/DE |
|---|---|---|---|---|
| `schaden_id` | str (PK) | `S-CH-2024-0031277` / `S-DE-...`; Alt: `24/031277` | `S-CH-2024-0031277` | variiert |
| `vertrag_id` | fk | Kann leer sein (Meldung ohne zuordenbaren Vertrag) | | beide |
| `partner_id_vn` | fk | | | beide |
| `produkt_code` | enum | | | beide |
| `schadendatum` | date | Behauptet; kann unsicher sein | `2024-02-17` | beide |
| `schadendatum_unsicher` | bool | | `false` | beide |
| `schadenzeit` | time | optional | `15:30` | beide |
| `meldedatum` | date | | `2024-02-21` | beide |
| `meldeverzug_tage` | int | berechnet | `4` | beide |
| `erfassungsdatum` | date | | `2024-02-22` | beide |
| `meldekanal` | enum | `portal`, `app`, `email`, `telefon`, `brief`, `vermittler`, `geschaedigter_direkt`, `anwalt`, `sozialversicherer` | `portal` | beide |
| `melder_typ` | enum | `vn`, `mitversicherte_person`, `vermittler`, `geschaedigter`, `anwalt_geschaedigter`, `sozialversicherer`, `anderer_versicherer` | `vn` | beide |
| `schadenort_plz` / `_ort` / `_land` | str | | `3800 Interlaken CH` | beide |
| `schadenart` | enum | `sach_beweglich`, `sach_immobilie`, `sach_mietsache`, `bearbeitung_obhut`, `person_leicht`, `person_schwer`, `vermoegen_rein`, `produkt`, `umwelt`, `gemischt` | `sach_beweglich` | beide |
| `schadenursache` | enum | ca. 40 Codes: `fallenlassen`, `umstossen`, `fluessigkeit`, `wasser_ueberlauf`, `brand_kerze`, `tier_biss`, `tier_sonstig`, `sturz_glaette`, `kollision_ski`, `kollision_velo`, `kind_spiel`, `schluesselverlust`, `handwerk_bearbeitung`, `montage_fehler`, `planungsfehler`, `beratungsfehler`, `berechnungsfehler`, `software_fehler`, `datenverlust`, `fristversaeumnis`, `lebensmittel`, `produktfehler`, `oel_austritt`, `sonstiges` | `fallenlassen` | beide |
| `beschreibung_kurz` | str | 1 Satz, vom Sachbearbeiter | `Smartphone des Kollegen beim Wandern fallen gelassen` | beide |
| `beschreibung_vn_freitext` | str | Originaltext der Meldung, 50–400 Wörter | | beide |
| `beschaedigte_sache` | str | | `iPhone 14 Pro` | beide |
| `beschaedigte_sache_kaufdatum` | date | | `2022-11-03` | beide |
| `beschaedigte_sache_neupreis` | dec | | `1299.00` | beide |
| `verletzungsart` | enum (Person) | `prellung`, `fraktur`, `schnittwunde`, `biss`, `hws`, `schaedel_hirn`, `sonstiges` | | beide |
| `arbeitsunfaehigkeit_tage` | int | | `12` | beide |
| `invaliditaetsgrad_pct` | dec | 0–100 | | beide |
| `geschaedigter_partner_id` | fk | Geschädigte werden als Partner geführt (auch wenn keine Kunden) | `P-CH-G-000771` | beide |
| `geschaedigter_typ` | enum | `privatperson`, `firma`, `oeffentliche_hand`, `sozialversicherer`, `mitversicherte_person` (Ausschluss!) | `privatperson` | beide |
| `geschaedigter_beziehung_vn` | enum | `fremd`, `bekannt`, `freund`, `verwandt`, `nachbar`, `kunde`, `arbeitgeber`, `vermieter`, `unbekannt` | `freund` | beide |
| `geschaedigter_gleiche_adresse` | bool | berechnet | `false` | beide |
| `geschaedigter_anwalt` | bool | | `false` | beide |
| `zeugen_vorhanden` | bool | | | beide |
| `polizei_involviert` | bool | | | beide |
| `polizeirapport_nr` | str | | | beide |
| `schadenstatus` | enum | siehe 4.3 | `GES` | beide |
| `status_seit` | date | | | beide |
| `komplexitaetsklasse` | enum | `fast_track`, `standard`, `komplex`, `grossschaden` | `fast_track` | beide |
| `sachbearbeiter_id` | str | | `SB-CH-044` | beide |
| `team` | enum | `phv_ch`, `phv_de`, `bhv_ch`, `bhv_de`, `behv`, `personenschaden`, `gross`, `regress`, `betrug` | | beide |
| `deckungsstatus` | enum | `offen`, `gedeckt`, `teilweise`, `vorbehalt`, `abgelehnt` | `gedeckt` | beide |
| `deckungsablehnungsgrund` | enum | `kein_vertrag`, `vertrag_nicht_aktiv`, `deckungsunterbruch`, `ausschluss_beruflich`, `ausschluss_vorsatz`, `ausschluss_eigene_sache`, `ausschluss_angehoerige`, `ausschluss_mfz`, `ausschluss_erfuellung`, `nicht_versicherte_taetigkeit`, `baustein_fehlt`, `obliegenheit_verletzt`, `verspaetete_meldung`, `unter_selbstbehalt`, `anzeigepflicht`, `sonstiges` | | beide |
| `avb_ziffer_referenz` | str | Zitierte Bedingungsziffer | `AVB PHV CH 2017 Ziff. B4.3` | variiert |
| `haftungsstatus` | enum | `offen`, `bejaht`, `teilweise`, `verneint`, `strittig`, `kulanz` | `bejaht` | beide |
| `haftungsquote_pct` | dec | 0–100 | `100` | beide |
| `haftungsgrundlage` | enum | CH: `OR41`, `OR55`, `OR56`, `OR58`, `OR97`, `ZGB333`, `PrHG`; DE: `BGB823`, `BGB831`, `BGB832`, `BGB833`, `BGB836`, `BGB280`, `ProdHaftG`, `UmweltHG` | `OR41` / `BGB823` | variiert |
| `mitverschulden_pct` | dec | 0–100 | `0` | beide |
| `erstreserve` | dec | | `800` | beide |
| `reserve_aktuell` | dec | | `0` | beide |
| `reserve_kosten` | dec | | | beide |
| `bezahlt_entschaedigung` | dec | Summe Zahlungen an Geschädigte/VN | `612.00` | beide |
| `bezahlt_kosten` | dec | Anwalt, Gutachter, Gericht | `0` | beide |
| `gesamtaufwand` | dec | bezahlt + Reserve | `612.00` | beide |
| `forderung_geschaedigter` | dec | Ursprünglich geltend gemacht | `1299.00` | beide |
| `zeitwert_berechnet` | dec | | `812.00` | beide |
| `selbstbehalt_angewendet` | dec | | `200` | beide |
| `selbstbehalt_eingefordert` | bool | | `true` | beide |
| `sublimit_angewendet` | str | | `obhut_5000` | beide |
| `regress_status` | enum | `keiner`, `aktiv_offen`, `aktiv_erfolgreich`, `aktiv_erfolglos`, `passiv_offen`, `passiv_bezahlt` | `keiner` | beide |
| `regress_betrag` | dec | | | beide |
| `betrugsscore_mint` | dec | 0.0–1.0 | `0.71` | beide |
| `betrugsindikatoren` | list[enum] | `F1`…`F9` + Detailcodes (`gleiche_adresse`, `kurz_nach_beginn`, `glatter_betrag`, `foto_datum_abweichend`, `wiederholter_geschaedigter`, `neuwert_forderung`, `keine_belege`) | `["gleiche_adresse","kurz_nach_beginn"]` | beide |
| `betrug_status` | enum (Label) | `kein_verdacht`, `verdacht`, `bestaetigt`, `ausgeraeumt` | `verdacht` | beide |
| `betrug_muster` | enum | `F1`…`F9`, `null` | `F1` | beide |
| `kuendigung_im_schadenfall` | enum | `keine`, `durch_vn`, `durch_vr` | `keine` | beide |
| `schliessungsdatum` | date | | `2024-04-02` | beide |
| `schliessungsgrund` | enum | `bezahlt`, `abgelehnt_deckung`, `abgelehnt_haftung`, `abgewehrt`, `zurueckgezogen`, `verjaehrt`, `unter_sb`, `vergleich`, `urteil` | `bezahlt` | beide |
| `wiedereroeffnung_anzahl` | int | 0–3 | `0` | beide |
| `abwicklungsdauer_tage` | int | berechnet | `45` | beide |
| `grossschaden_flag` | bool | Reserve > 100'000 | `false` | beide |
| `rueckversicherung_gemeldet` | bool | | `false` | beide |
| `system_herkunft` | enum | | `MINT` | beide |

### 6.6 Entität `schaden_beteiligte` (1:n)

| Feld | Typ | Wertebereich | Beispiel |
|---|---|---|---|
| `beteiligung_id` | str (PK) | | |
| `schaden_id` | fk | | |
| `partner_id` | fk | | |
| `rolle` | enum | `geschaedigter`, `verursacher_mitversichert`, `zeuge`, `anwalt_geschaedigter`, `anwalt_vn`, `gutachter`, `arzt`, `werkstatt`, `sozialversicherer`, `anderer_versicherer`, `polizei`, `regressgegner` |
| `iban` | str | Zahlungsempfänger; Wiederverwendung über Schäden = Signal |
| `vollmacht_vorhanden` | bool | |

### 6.7 Entität `zahlung` (Schaden- und Prämienzahlungen)

| Feld | Typ | Wertebereich / Codeliste | Beispiel | CH/DE |
|---|---|---|---|---|
| `zahlung_id` | str (PK) | | `Z-2024-00912233` | beide |
| `bezug_typ` | enum | `schaden`, `praemie`, `regress`, `rueckerstattung`, `selbstbehalt` | `schaden` | beide |
| `bezug_id` | fk | `schaden_id` oder `vertrag_id`/Rechnungsnr. | | beide |
| `richtung` | enum | `ausgang`, `eingang` | `ausgang` | beide |
| `betrag` | dec | | `612.00` | beide |
| `waehrung` | enum | `CHF`, `EUR` | | variiert |
| `kostenart` | enum (Schaden) | `entschaedigung_sach`, `entschaedigung_person_heilung`, `entschaedigung_person_erwerbsausfall`, `genugtuung_schmerzensgeld`, `haushaltsschaden`, `entschaedigung_vermoegen`, `anwalt_eigen`, `anwalt_gegner`, `gutachter`, `gericht`, `regress_eingang`, `selbstbehalt_eingang`, `abschlag`, `vergleich`, `kulanz` | `entschaedigung_sach` | variiert (Bezeichnung) |
| `empfaenger_partner_id` | fk | | | beide |
| `empfaenger_typ` | enum | `geschaedigter`, `vn`, `anwalt`, `gutachter`, `werkstatt`, `sozialversicherer`, `gericht` | `geschaedigter` | beide |
| `iban_empfaenger` | str | | | variiert |
| `zahlungsdatum` | date | | `2024-03-28` | beide |
| `valutadatum` | date | | | beide |
| `zahlungsart` | enum | `ueberweisung`, `sepa`, `lsv`, `scheck` (Altbestand DE), `verrechnung` | | variiert |
| `verwendungszweck` | str | | `Schaden S-CH-2024-0031277 / Zeitwert iPhone abzgl. SB` | beide |
| `freigabe_stufe` | int | 0–4 (Vollmachtsstufe, siehe 7.6) | `0` | beide |
| `freigegeben_von` | str | | `SB-CH-044` | beide |
| `storniert` | bool | | `false` | beide |
| `praemien_periode_von` / `_bis` | date (Prämie) | | | beide |
| `mahnstufe_bei_zahlung` | int (Prämie) | 0–3 | `1` | beide |
| `rechnung_nr` | str (Prämie) | | `RE-CH-2024-0442112` | beide |
| `faelligkeit` | date (Prämie) | | | beide |
| `verzugstage` | int (Prämie) | | `23` | beide |

### 6.8 Entität `reserve_historie`

| Feld | Typ | Beispiel |
|---|---|---|
| `schaden_id` | fk | |
| `datum` | date | `2024-03-01` |
| `reserve_entschaedigung_neu` | dec | `12000` |
| `reserve_kosten_neu` | dec | `2500` |
| `grund` | enum: `erstreserve`, `gutachten`, `anwaltsforderung`, `arztbericht`, `vergleich`, `zahlung`, `schliessung`, `wiedereroeffnung`, `periodische_pruefung` | `anwaltsforderung` |
| `bearbeiter_id` | str | |
| `kommentar` | str | `Forderung RA Meier CHF 18'500, Quote 2/3 erwartet` |

### 6.9 Entität `dokument` (Metadaten)

| Feld | Typ | Wertebereich | Beispiel |
|---|---|---|---|
| `dokument_id` | str (PK) | | `D-2024-01188273` |
| `dokument_typ` | enum | `V01`…`V22`, `S01`…`S27` | `S04` |
| `bezug_typ` / `bezug_id` | enum/fk | `vertrag`, `schaden`, `offerte`, `partner` | |
| `richtung` | enum | `eingang`, `ausgang`, `intern` | `eingang` |
| `absender_typ` | enum | `vn`, `geschaedigter`, `anwalt`, `vermittler`, `sozialversicherer`, `gutachter`, `arzt`, `polizei`, `versicherer`, `system` | `anwalt` |
| `format` | enum | `pdf_text`, `pdf_scan`, `pdf_handschrift`, `email`, `foto_jpeg`, `docx`, `xlsx`, `txt_journal` | `pdf_text` |
| `sprache` | enum | `de`, `fr`, `it`, `en` | `de` |
| `seiten` | int | | `4` |
| `erstelldatum` | date | Im Dokument | `2024-03-11` |
| `eingangsdatum` | date | Posteingang | `2024-03-14` |
| `ocr_qualitaet` | dec | 0.0–1.0 | `0.87` |
| `ground_truth_json` | json | Extraktionsfelder (nur Teilmenge) | `{"forderung_total": 18500, "positionen": [...]}` |
| `enthaelt_widerspruch_zu` | fk (didaktisch) | Verweis auf Dokument mit widersprüchlicher Angabe | `D-2024-01188201` |
| `system_herkunft` | enum | `PFEFFER400_ARCHIV`, `MINT_DMS`, `POSTEINGANG`, `PORTAL` | |

### 6.10 Referenz-/Stammdaten

| Tabelle | Inhalt | Umfang |
|---|---|---|
| `vermittler` | ID, Name, Typ, Land, Region, Courtagesatz, aktiv seit, Bewertung (Datenqualität) | 150 CH, 400 DE |
| `sachbearbeiter` | ID, Name, Team, Vollmachtsstufe, Standort | 60 |
| `branchen` | NOGA/WZ-Code, Bezeichnung, Pfefferminzia-Risikoklasse, Prämiensatz ‰, UW-Regel (automatisch / manuell / abgelehnt) | 120 Einträge |
| `plz_regionen` | PLZ, Ort, Kanton/Bundesland, Tarifzone, Hundehalterpflicht (Bundesland/Kanton), Sprache (CH) | CH ~4'000, DE ~8'000 (oder Stichprobe) |
| `bedingungen` | Version, Produkt, Land, gültig von/bis, PDF-Referenz, Sublimit-Tabelle als JSON | 12–16 Versionen |
| `klauseln` | Code, Text, Typ (Ausschluss/Einschluss/Zuschlag), Produkt | 40 |
| `codelisten` | Alle Enums mit Bezeichnung DE/FR/IT und Alt-Code (PFEFFER/400) | |

---

## 7. Regelwerke

Alle Regelwerke sollen als eigenständige Dokumente (PDF + Markdown-Quelle) vorliegen, mit eindeutiger Versionierung und Ziffern-Gliederung, damit RAG-Systeme präzise zitieren können ("AVB PHV CH 2022, Ziff. B3.2"). Für jede Bedingungsgeneration braucht es eine eigene Version; die inhaltlichen Unterschiede zwischen Generationen müssen dokumentiert (Änderungsverzeichnis) und in den Vertragsdaten referenziert sein.

### 7.1 Allgemeine Versicherungsbedingungen (AVB CH) – Gliederung

Empfohlene Struktur für die drei CH-Produkte (Ausgabe 2022; Altversionen 2005/2012/2017 mit gleicher Grundgliederung, aber abweichenden Inhalten):

| Teil | Abschnitt | Inhalt | Umfang (Seiten) | Didaktische Anker |
|---|---|---|---|---|
| A | Allgemeine Bestimmungen | A1 Vertragsgrundlagen, A2 Örtlicher Geltungsbereich (weltweit / Europa), A3 Zeitlicher Geltungsbereich (Schadenverursachungsprinzip bzw. Verstossprinzip bei BeHV; Nachhaftung), A4 Beginn und Dauer, stillschweigende Verlängerung, Kündigung (ordentlich nach 3 Jahren gemäss Art. 35a VVG, im Schadenfall, bei Prämienänderung), A5 Prämie, Fälligkeit, Zahlungsverzug (Art. 20 VVG), Rückerstattung, A6 Anzeigepflicht und Gefahrsänderung, A7 Obliegenheiten im Schadenfall (unverzügliche Meldung, kein Anerkenntnis, Mitwirkung, Prozessführung durch Versicherer), A8 Folgen bei Verletzung, A9 Selbstbehalt, A10 Sanktionsklausel, A11 Datenschutz, A12 Mitteilungen, A13 Gerichtsstand, A14 Broker-Klausel | 4–5 | Kündigungsrecht nach 3 Jahren fehlt in Altversionen (vor 2022) |
| B | Versicherte Personen und Eigenschaften | B1 Versicherungsnehmer, B2 Mitversicherte Personen (Familie, Haushalt), B3 Versicherte Eigenschaften (Privatperson, Familienhaupt, Mieter, Hauseigentümer, Tierhalter, Bauherr, Sportler, Velofahrer …) bzw. Betriebsbeschreibung (BHV) bzw. berufliche Tätigkeit (BeHV) | 2–3 | Grenze privat/beruflich (Nebenerwerb bis CHF 10'000 Jahresumsatz mitversichert in PFZ-2021, nicht in PFM-M) |
| C | Versicherte Leistungen und Deckungsumfang | C1 Gegenstand (Haftpflicht für Personen-, Sach- und daraus folgende Vermögensschäden), C2 Reine Vermögensschäden (sublimitiert), C3 Abwehr unberechtigter Ansprüche, C4 Deckungssumme und Jahresmaximum, C5 Sublimits (Obhutsschäden, Gefälligkeitsschäden, Mietsachschäden, Schlüsselverlust, Umwelt), C6 Schadenverhütungskosten, C7 Kosten (Anwalt, Gericht, Expertise) | 3–4 | Sublimit-Tabelle als strukturierter Anhang |
| D | Einschränkungen und Ausschlüsse | D1 Vorsatz und grobe Fahrlässigkeit (Kürzungsrecht), D2 Ansprüche mitversicherter Personen untereinander, D3 Schäden an eigenen, gemieteten, geliehenen Sachen (soweit nicht eingeschlossen), D4 Motorfahrzeuge, Luft- und Wasserfahrzeuge, D5 Berufliche/gewerbliche Tätigkeit (PHV), D6 Erfüllungsansprüche, Mängel am eigenen Werk (BHV/BeHV), D7 Vertragliche Haftungserweiterungen, D8 Bussen, Vertragsstrafen, Strafverfolgungskosten, D9 Umwelt (ausserhalb Baustein), D10 Asbest, Kernenergie, Krankheitsübertragung, Genetisch veränderte Organismen, Elektromagnetische Felder, D11 Krieg, Terror, Unruhen, D12 Rückruf (ausser Baustein), D13 Datenverlust/Cyber (ausser Baustein), D14 USA/Kanada (BHV/BeHV) | 3–4 | Krankheitsübertragung: in PFM-M ausgeschlossen, in PFZ-2021 bis CHF 1 Mio. eingeschlossen (Pandemieerfahrung) |
| E | Schadenfall | E1 Meldung, E2 Mitwirkung, E3 Schadenregulierung, Verhandlungsführung, E4 Direktzahlung an Geschädigte, E5 Selbstbehalt-Einforderung, E6 Regress (Art. 72 VVG), E7 Vergleich, Prozess, E8 Verjährung | 2 | Frist "unverzüglich, spätestens innert 30 Tagen" (PFZ) vs. "sofort" (PFM-K) |
| F | Glossar / Definitionen | Personenschaden, Sachschaden, Vermögensschaden, Ereignis, Serienschaden, Obhut, Gefälligkeit, Familienhaupt, Zeitwert, Neuwert | 1–2 | Serienschadenklausel: mehrere Schäden aus gleicher Ursache = 1 Ereignis (1 Selbstbehalt, 1 Deckungssumme) |
| Anhang | Sublimit-Tabelle je Generation; Übersicht Bausteine; Kundeninformation Art. 3 VVG | 2–3 | |

Gesamtumfang: PHV 14–18 Seiten, BHV 22–30 Seiten, BeHV 18–25 Seiten. Sprachen: DE verbindlich, FR-Übersetzung für Realismus (mind. für PHV), IT optional. Fassung 2022 in geschlechtsneutraler Sprache, Altversionen nicht (Stilunterschied als Datierungshinweis).

### 7.2 Allgemeine Haftpflichtbedingungen (AHB DE) und Besondere Bedingungen (BBR)

DE folgt der GDV-Systematik: AHB als Grundlage (produktübergreifend), Besondere Bedingungen und Risikobeschreibungen (BBR) je Produkt, dazu Klauseln. Pfefferminzia DE verwendet "AHB 2016 (Pfefferminzia-Fassung)" für Neugeschäft ab 2016 und "AHB 2008" im Altbestand.

| Dokument | Gliederung | Umfang | Didaktische Anker |
|---|---|---|---|
| AHB (Pfefferminzia-Fassung 2016) | Abschnitt A1 Umfang des Versicherungsschutzes: 1 Gegenstand der Versicherung, 2 Vermögensschäden/Abhandenkommen von Sachen, 3 Versichertes Risiko (inkl. Erhöhungen und Erweiterungen, Vorsorgeversicherung), 4 Vorsorgeversicherung, 5 Leistungen der Versicherung, 6 Begrenzung der Leistungen (Versicherungssumme, Jahreshöchstersatzleistung, Serienschaden, Selbstbeteiligung), 7 Ausschlüsse (Vorsatz, Vertragserfüllung, Angehörige, Kfz, Umwelt, Asbest, Gentechnik, Kernenergie, Krieg, Strahlen, Sachen in Obhut, Tätigkeitsschäden, Erzeugnisse); Abschnitt A2 Beginn/Dauer/Ende: 8 Beginn, 9 Beitrag/Fälligkeit, 10 Folgebeitrag, 11 Lastschrift, 12 Teilzahlung/Verzug, 13 Beitragsregulierung, 14 Beitragsangleichung, 15 Dauer und Ende, 16 Wegfall des versicherten Risikos, 17 Kündigung nach Beitragsangleichung, 18 Kündigung nach Versicherungsfall, 19 Kündigung nach Veräusserung, 20 Kündigung nach Risikoerhöhung, 21 Mehrfachversicherung; Abschnitt A3 Obliegenheiten: 22 Vorvertragliche Anzeigepflichten, 23 Obliegenheiten vor Eintritt, 24 Obliegenheiten nach Eintritt, 25 Rechtsfolgen; Abschnitt A4 Weitere Bestimmungen: 26 Mitversicherte Personen, 27 Abtretungsverbot, 28 Anzeigen/Willenserklärungen, 29 Verjährung, 30 Zuständiges Gericht, 31 Anzuwendendes Recht | 14–18 Seiten | Nummerierung AHB 2008 vs. 2016 weicht ab (Ziff. 7.6 Kfz in 2008 vs. 7.4 in 2016) – RAG muss Version beachten |
| BBR Privathaftpflicht (Basis / Komfort / Premium, Fassung 2023) | 1 Versichertes Risiko (Privatperson; Familienhaupt; Wohnung/Haus; Tierhalter zahm; Hundehalter als Zusatz; Radfahrer; Sport; Waffen; Bauherr bis 50'000/100'000; Photovoltaik; Drohnen; Ehrenamt; Internet), 2 Mitversicherte Personen (Partner, Kinder, Haushaltshilfen), 3 Deckungserweiterungen (Mietsachschäden, Schlüsselverlust, Gefälligkeitsschäden, Sachschäden an geliehenen Sachen, Deliktunfähige Kinder, Ausfalldeckung, Auslandsaufenthalt, Neuwertentschädigung bis 500 EUR, Vermögensschäden), 4 Besondere Ausschlüsse (Jagd, gefährliche Sportarten, Gewerbe), 5 Best-Leistungs-Garantie (Premium), 6 Innovationsklausel, 7 Sublimit-Tabelle (Basis/Komfort/Premium) | 15–25 Seiten | Drei Tarifstufen mit unterschiedlichen Sublimits: gleiche Ereignisse, unterschiedliche Ergebnisse |
| BBR Betriebshaftpflicht (Fassung 2023) + Betriebsbeschreibung | 1 Versichertes Risiko (Betriebsbeschreibung als Vertragsbestandteil), 2 Mitversicherte Personen/Betriebsangehörige, 3 Deckungserweiterungen (Tätigkeitsschäden, Be-/Entladeschäden, Mietsachschäden, Schlüsselverlust, Abwasserschäden, Vermögensschäden, Datenschutz, Auslandsschäden EU/weltweit ohne USA), 4 Produkthaftpflicht (Grund- und erweiterte Produkthaftpflicht nach GDV-Modell: Verbindungs-/Vermischungs-/Verarbeitungsschäden, Aus-/Einbaukosten, Prüf-/Sortierkosten), 5 Umwelthaftpflicht-Basis + Umweltschadensversicherung (USV), 6 Besondere Ausschlüsse, 7 Beitragsregulierung (jährliche Umsatz-/Lohnsummenmeldung), 8 Klauselverzeichnis | 25–35 Seiten | Tätigkeitsschaden vs. Erfüllungsanspruch als Kernabgrenzung |
| AVB Vermögensschaden-Haftpflicht (BeHV) + BBR je Berufsgruppe | Teil A Allgemein (nach GDV AVB-V): § 1 Gegenstand, § 2 Vorsorge, § 3 Versicherungsfall/Verstoss, § 4 Ausschlüsse (wissentliche Pflichtverletzung, Kostenüberschreitung, Erfüllung), § 5 Versicherungssumme/Selbstbehalt/Serienschaden, § 6 Nachhaftung, § 7 Rückwärtsdeckung; Teil B BBR: Architekten/Ingenieure (Objektversicherung optional, Bauleitung, Mitversicherung Personen-/Sachschäden 1.5 Mio./250'000), Steuerberater (Pflichtdeckung § 67 StBerG, Jahreshöchstleistung 4-fach), IT (Claims-made, Datenverlust, Nacherfüllung ausgeschlossen, Cyber-Abgrenzung), Unternehmensberater | 18–28 Seiten | Verstoss vs. Claims-made: gleicher Fehler, andere Deckung je nach Vertragsjahr |
| Klauselblatt (CH und DE) | 40 nummerierte Klauseln: Einschluss/Ausschluss bestimmter Tätigkeiten (Dachdecker, Abbruch, Sprengen, Gerüstbau), Subunternehmer-Klausel, USA/Kanada-Ausschluss, Rückrufkosten-Einschluss, Mitversicherung Ehegatte im Betrieb, Regressverzicht gegenüber Arbeitnehmenden, Leasing-Klausel, Baustellenklausel, Silo-Klausel (Landwirtschaft, nicht gezeichnet) | 6–10 Seiten | Klausel auf Police referenziert, Text nur im Klauselblatt |

### 7.3 Zeichnungsrichtlinien (Underwriting Guidelines)

| Kapitel | Inhalt | Umfang |
|---|---|---|
| 1 Zweck, Geltungsbereich, Rollen | Verbindlichkeit für Aussendienst, Broker-Desk, UW-Team; Verhältnis zu Vollmachtsregelung; Eskalation | 1 Seite |
| 2 Zielrisiken und Ausschlussrisiken (Risikoappetit) | Positivliste Branchen (BHV) mit Risikoklasse 1–6; Negativliste (nicht gezeichnet: Sprengbetriebe, Feuerwerk, Chemie > 20 MA, Sicherheitsdienste, Vermittlung von Finanzprodukten, Medizinaltechnik-Hersteller, Kernkraft, Luftfahrt, Reedereien, Bergbau, Tabak, Waffen); Graubereich mit Pflicht-UW (Dachdecker, Gerüstbau, Abbruch, Kinderbetreuung, Fitness mit Trainerpflicht, Gastronomie mit Catering, Tätowierer) | 3–4 Seiten |
| 3 Annahmeregeln PHV | Automatische Annahme wenn: Alter 18–85, Wohnsitz CH/DE, max. 2 Vorschäden in 5 Jahren mit Summe < 5'000, keine Vorversicherer-Kündigung, keine Listenhunde ohne Nachweis, keine Betreibung/Negativmerkmal. Manuelle Prüfung: 3+ Vorschäden, Listenhund, Pferde > 2, Bausumme > Baustein-Limit, Ferienhaus im Ausland, Nebenerwerb > Grenze. Ablehnung: 5+ Vorschäden, Betrugsvermerk, Sanktionstreffer | 2–3 Seiten |
| 4 Annahmeregeln BHV | Branchenklasse (1–4 automatisch bis Umsatz 3 Mio.; 5 manuell; 6 nur mit Genehmigung Leitung UW); Umsatz/Lohnsumme; Vorschäden (Schadenquote 3 Jahre > 80 % → Zuschlag; > 120 % → Ablehnung oder Sanierung); Subunternehmer > 30 % → Klausel; Export USA/Kanada → Ausschluss oder Zuschlag 25 %; Betriebsbeschreibung muss vollständig sein (Tätigkeitsabgrenzung); Bonität | 4–5 Seiten |
| 5 Annahmeregeln BeHV | Berufsgruppe muss auf Positivliste; Nachweis Berufsqualifikation/Kammer; Umsatz > 5 Mio. → Rückversicherung; Vorschäden; Tätigkeitsschwerpunkte (Bauleitung Zuschlag 30 %; Revision Zuschlag 20 %; IT mit Hosting Zuschlag 25 %); Claims-made-Umstellung: Rückwärtsdeckung nur mit Erklärung "keine bekannten Verstösse" | 3–4 Seiten |
| 6 Tarifabweichungen | Rabatte (Bündel, Mehrjahr, Schadenfreiheit, Zertifizierung) max. kumuliert 25 %; Zuschläge (Vorschäden, Risikoklasse, Tätigkeit); Abweichung > 15 % nur Stufe 2 | 1–2 Seiten |
| 7 Deckungssummen und Sublimits | Zulässige Kombinationen; Sublimit-Erhöhungen nur mit UW-Freigabe; Maximalkapazität (CH 10 Mio., DE 50 Mio. PHV / 10 Mio. BHV, darüber Rückversicherung) | 1 Seite |
| 8 Sanktions-, Bonitäts- und Betrugsprüfung | Pflichtprüfungen, Quellen, Umgang mit Treffern | 1–2 Seiten |
| 9 Dokumentationspflichten | UW-Entscheid mit Begründung; Rückfragen; Frist 5 Arbeitstage; Auflagen auf Police | 1 Seite |
| 10 Bestandssanierung und Erneuerung | Kündigung/Anpassung bei Schadenquote > 150 %; Umstellung Altbedingungen; Pflicht-Review Risikoklasse 5–6 jährlich | 1–2 Seiten |
| Anhang | Branchen-Risikoklassen-Tabelle (NOGA/WZ → Klasse → Prämiensatz ‰ → UW-Regel), Listenhunde je Kanton/Bundesland, Checkliste Betriebsbeschreibung, Fragenkatalog BeHV | 6–10 Seiten |

Gesamtumfang ca. 25–35 Seiten, je eine Version CH und DE (80 % identisch, Unterschiede: Branchencodes, Bonitätsquellen, Hundehalterpflicht, Deckungssummen).

### 7.4 Schadenregulierungsrichtlinien

| Kapitel | Inhalt | Umfang |
|---|---|---|
| 1 Grundsätze | Zügig, fair, rechtskonform; Gleichbehandlung; Kulanzrahmen; Kommunikation mit Geschädigten (kein Direktanspruch, aber Direktzahlung); Datenschutz | 1–2 Seiten |
| 2 Schadenerfassung und Triage | Pflichtfelder; Fristen (Erfassung 2 AT, Eingangsbestätigung 3 AT); Komplexitätsklassen und Zuteilung (Fast Track: Sachschaden < 2'000, klare Deckung, kein Personenschaden, kein Betrugssignal → Regulierung innert 5 AT ohne Belegprüfung bis 500); Grossschadendefinition | 2 Seiten |
| 3 Deckungsprüfung | Prüfreihenfolge (Vertrag → Prämie → Risiko → Ausschluss → Obliegenheit → Sublimit/SB); Deckungsvorbehalt (Reservation of Rights) wann und wie; Ablehnungsschreiben-Standards mit Rechtsmittelhinweis; Entscheidungsbefugnis | 2–3 Seiten |
| 4 Haftungsprüfung | Prüfschema (Schaden, Widerrechtlichkeit, Kausalität, Verschulden/Haftungsgrund); Mitverschulden-Quoten (Richttabellen: Ski-Kollision FIS-Regeln, Velo/Fussgänger, Hundebiss mit Provokation); Beweislast; Kulanz bis 1'000 ohne Haftungsprüfung bei langjährigen Kunden; Sozialversicherungsregress-Koordination | 3–4 Seiten |
| 5 Schadenbemessung Sachschaden | Zeitwert (Abschreibungstabellen: Elektronik 20 %/Jahr, Möbel 10 %, Brillen 15 %, Kleidung 25 %, Fahrräder 10 %; Neuwert in DE-Premium bis 500 EUR), Reparatur vs. Ersatz (Reparatur bis 100 % Zeitwert), Mehrwertsteuer (nur bei tatsächlichem Ersatz DE § 249 BGB; CH bei Privaten inkl.), Wertminderung, Nutzungsausfall, Gutachterpflicht ab 5'000 (Sach) / 10'000 (Bau) | 3 Seiten |
| 6 Schadenbemessung Personenschaden | Heilungskosten (Koordination mit Kranken-/Unfallversicherung), Erwerbsausfall (Lohnausweis/Gehaltsabrechnung, Berechnung), Haushaltsschaden (CH: SAKE-Tabellen; DE: Tabellenwerke), Genugtuung/Schmerzensgeld (CH: Richtwerte nach Hütte/Landolt; DE: Schmerzensgeldtabellen Hacks/ADAC), Abschlagszahlungen, Rentenfälle, Kapitalisierung, medizinische Begutachtung, Fallmanagement | 3–4 Seiten |
| 7 Schadenbemessung Vermögensschaden (BeHV) | Kausalität (hypothetischer Verlauf), Sowieso-Kosten (Bau), Vorteilsanrechnung, Steuerschaden bei Steuerberatern (Zins, Busse nicht versichert), Abgrenzung Nachbesserung | 2 Seiten |
| 8 Reservierung | Erstreserve-Tabelle je Schadenart; Anpassungspflicht bei neuen Informationen; Grossschadenmeldung > 100'000; Reserve-Review alle 6 Monate; Kostenreserve separat | 1–2 Seiten |
| 9 Abwehr und Prozessführung | Wann Anwalt beauftragen (Forderung > 20'000, Anwalt auf Gegenseite, strittige Haftung), Anwaltspanel, Kostenkontrolle, Vergleichsbefugnis, Prozessrisiko-Bewertung | 2 Seiten |
| 10 Regress | Prüfpflicht bei jedem Schaden > 5'000; Regressgegner; Teilungsabkommen (DE); Regressverzicht gegenüber Arbeitnehmenden; Regress gegen VN bei Vorsatz | 1–2 Seiten |
| 11 Betrugsprävention | Indikatorenliste (Red Flags), Pflicht zur Weiterleitung an Team Betrug bei Score > 0.6 oder 2+ Indikatoren, Abklärungsmassnahmen (Rückfrage, Belege, Besichtigung, Detektiv nur mit Genehmigung Stufe 3), Umgang mit Verdacht in Kommunikation (keine Vorverurteilung), Strafanzeige-Kriterien | 2–3 Seiten |
| 12 Kommunikation und Fristen | Service-Level: Eingangsbestätigung 3 AT, Deckungsentscheid 10 AT, Zahlung 5 AT nach Freigabe; Sprache; Eskalation; Beschwerdemanagement; Ombudsstelle | 1–2 Seiten |
| 13 Schliessung und Wiedereröffnung | Schliessungskriterien; Kündigungsrecht prüfen; Selbstbehalt einfordern; Nachforderung | 1 Seite |
| Anhang | Abschreibungstabellen, Genugtuungs-/Schmerzensgeldrichtwerte (fiktiv, aber plausibel), Musterbriefe (Deckungszusage, Ablehnung, Anerkennung, Teilanerkennung), Red-Flag-Liste, Erstreserve-Tabelle | 8–12 Seiten |

Gesamtumfang ca. 35–45 Seiten; eine gemeinsame Version mit CH/DE-Abschnitten (klar markiert), um länderspezifische RAG-Fragen zu ermöglichen ("Gilt die Neuwertregel auch in der Schweiz?").

### 7.5 Tarifierungsregeln (Tarifhandbuch)

| Kapitel | Inhalt | Umfang |
|---|---|---|
| 1 Tarifstruktur | Grundprämie × Faktoren + Bausteinprämien − Rabatte + Zuschläge; Mindestprämie; Rundung; Stempelabgabe (CH 5 %) / Versicherungsteuer (DE 19 %); Ratenzuschlag | 1–2 Seiten |
| 2 Tarif PHV | Grundprämie je Personenkreis (Einzel/Familie/Paar) × Deckungssummenfaktor (CH 5 Mio. = 1.00, 10 Mio. = 1.15; DE 5 = 1.00, 10 = 1.05, 20 = 1.10, 50 = 1.18) × Selbstbehaltfaktor (CH 0 = 1.20, 200 = 1.00, 500 = 0.85; DE 0 = 1.00, 150 = 0.85) × Regionalfaktor (CH: Stadt/Land 1.05/0.98; DE: 3 Zonen) × Vorschadenfaktor (0 = 0.95, 1 = 1.00, 2 = 1.15, 3+ = 1.40) + Bausteine (Hund CH 0 / DE 40–90 nach Rasse und Bundesland; Pferd; Bauherr; Öltank; Gebäude) − Bündelrabatt 10 % − Mehrjahresrabatt CH (3 J. 5 %, 5 J. 10 %) − Berufsgruppenrabatt DE (ÖD 10 %) | 3–4 Seiten inkl. Tabellen |
| 3 Tarif BHV | Prämiensatz ‰ je Risikoklasse (1: 1.5 ‰, 2: 2.5 ‰, 3: 4 ‰, 4: 6 ‰, 5: 9 ‰, 6: 14 ‰) auf Lohnsumme (CH) bzw. Umsatz (DE, 0.4–4 ‰) oder pro Kopf (Handwerk DE); Mindestprämie; Deckungssummenfaktor; SB-Faktor; Bausteine (Produkt +15 %, Umwelt +10 %, Rückruf +20 %, IT/Datenschutz +8 %); Zuschläge (USA +25 %, Subunternehmer > 30 % +10 %, Vorschäden nach Schadenquote); Rabatte (Zertifizierung 5 %, Schadenfreiheit 3 J. 10 %) | 4–5 Seiten |
| 4 Tarif BeHV | Prämiensatz ‰ auf Honorar-/Umsatzsumme je Berufsgruppe (Architekt 8 ‰, Bauingenieur 7 ‰, Treuhand 5 ‰, Steuerberater DE 4 ‰, IT 5 ‰, Berater 4 ‰) × Deckungssummenfaktor × SB-Faktor × Tätigkeitsfaktor (Bauleitung 1.3, Revision 1.2, Hosting 1.25) × Vorschadenfaktor; Mindestprämie; Objektzuschläge | 3 Seiten |
| 5 Beitragsregulierung / Prämienabrechnung | Vorläufige Prämie auf Basis Vorjahreswerte, Nachabrechnung nach Meldung; Schätzung bei Nichtmeldung (+20 %) | 1 Seite |
| 6 Indexierung und Tarifanpassung | Jährliche Anpassung nach Schadenindex; Ankündigungspflicht; Kündigungsrecht | 1 Seite |
| 7 Vermittlervergütung | Courtage/Provision je Kanal (Agentur 12 %, Broker 15–18 %, Portal 8 %, Direkt 0) | 1 Seite |
| Anhang | Beispielrechnungen (10 Fälle), Rasse-/Listenhund-Tabelle, Regionalzonen, Risikoklassen-Tabelle (Verweis UW) | 4–6 Seiten |

Gesamtumfang ca. 20–25 Seiten je Land. Tarifregeln müssen mit den erzeugten Vertragsprämien konsistent sein (Prämie in Daten = Tarif ± Rundung), damit "Prämie nachrechnen"-Aufgaben lösbar sind; bewusst 3–5 % der Verträge mit Abweichungen (manuelle Rabatte, Altbestand) für Anomalie-Übungen.

### 7.6 Vollmachtsregelung (Kompetenzordnung)

| Stufe | Rolle | Underwriting-Kompetenz | Schaden-Kompetenz (Zahlung / Reserve je Schaden) | Kulanz | Besonderes |
|---|---|---|---|---|---|
| 0 | Automatik (Regelwerk / MINT-Modell) | Annahme nach UW-Regeln Kapitel 3–5 ohne Abweichung | Fast-Track-Zahlungen bis CHF/EUR 1'000 bei Deckung klar und Betrugsscore < 0.3 | keine | Jede Automatik-Entscheidung muss protokolliert und stichprobengeprüft werden (10 %) |
| 1 | Sachbearbeiter/in Vertrag bzw. Schaden | Tarifabweichung bis 10 %; Bausteine; keine Risikoklasse 5–6 | Zahlung bis 10'000; Reserve bis 25'000; Deckungsablehnung PHV Standardfälle | bis 500 | Vier-Augen-Prinzip ab 5'000 |
| 2 | Senior-Sachbearbeiter/in, Teamleitung | Tarifabweichung bis 25 %; Risikoklasse 5; Ausschlussklauseln; Annahme mit Auflagen | Zahlung bis 50'000; Reserve bis 100'000; Deckungsablehnung alle Produkte; Anwaltsbeauftragung; Vergleiche bis 50'000 | bis 2'000 | Grossschadenmeldung an Stufe 3 |
| 3 | Leitung Underwriting / Leitung Schaden | Risikoklasse 6; Abweichung > 25 %; Sonderdeckungen; Kündigung Bestand | Zahlung bis 250'000; Reserve bis 1'000'000; Vergleiche bis 250'000; Detektiveinsatz; Strafanzeige | bis 10'000 | Rückversicherungsmeldung |
| 4 | Geschäftsleitung / Schadenkomitee | Kapazität über Rückversicherungsgrenze; Ablehnung Negativliste-Ausnahmen | Unbegrenzt; Prozessführung vor Obergerichten; Grundsatzentscheide | unbegrenzt | Protokoll Schadenkomitee |

Ergänzende Regeln: Stellvertretung, Interessenkonflikt (eigene Verträge, Verwandte), Vollmacht Vermittler (Agenturen: Policierung PHV Standard im Rahmen Stufe 0; Broker: keine Zeichnungsvollmacht), Kompetenz-Überschreitung als Compliance-Fall. Umfang 4–6 Seiten. Im Datensatz: `freigabe_stufe` in Zahlungen muss mit Betrag konsistent sein; bewusst 1–2 % Fälle mit Verletzung (Betrag knapp über Stufe, aber von niedrigerer Stufe freigegeben) als Audit-Übung.

### 7.7 Übersicht Regelwerke und Versionen

| Regelwerk | CH | DE | Versionen | Umfang gesamt |
|---|---|---|---|---|
| AVB / AHB | AVB PHV, BHV, BeHV | AHB + BBR PHV, BHV; AVB-V + BBR BeHV | 2005/2008, 2012/2015, 2017, 2022/2023 | ~200 Seiten |
| Besondere Bedingungen / Bausteine / Klauseln | Bausteinbedingungen, Klauselblatt | BBR-Bausteine, Klauselblatt | je 2 Versionen | ~40 Seiten |
| Zeichnungsrichtlinien | 1 Version 2023 | 1 Version 2023 | 1 (+ Altversion 2018 optional) | ~35 Seiten je Land |
| Schadenregulierungsrichtlinien | Gemeinsam mit Länderabschnitten | | 1 Version 2024 | ~45 Seiten |
| Tarifhandbuch | CH | DE | 2022, 2024 | ~25 Seiten je Land |
| Vollmachtsregelung | Gemeinsam | | 1 Version 2023 | ~6 Seiten |
| Kundeninformation / IPID / Produktinformationsblatt | CH Art. 3 VVG | DE IPID + PIB | je Produkt | ~30 Seiten |
| Prozesshandbuch Schaden (optional) | Gemeinsam | | 1 | ~20 Seiten |

---

## 8. Didaktik: Stolpersteine und bewusste Unschärfen

Ziel: Die Use-Cases sollen nicht an sauberen Lehrbuchdaten scheitern oder trivial werden. Jeder Stolperstein ist einem Use-Case zugeordnet, hat eine geplante Häufigkeit und eine Auflösung (Ground Truth), damit Lernende Ergebnisse überprüfen können.

### 8.1 Stolpersteine in Verträgen und Underwriting

| Nr. | Stolperstein | Beschreibung | Häufigkeit | Use-Case | Auflösung / Ground Truth |
|---|---|---|---|---|---|
| U1 | Widerspruch Antrag vs. Police | Antrag nennt Familie, Police Einzelperson (Erfassungsfehler); Antrag mit Hund, Police ohne Baustein | 2 % der Verträge | Dokumentextraktion, Datenqualität | Feld `police_abweichung_von_antrag` mit Erklärung; Rechtsfolge (CH: Police massgebend, wenn nicht beanstandet; DE: § 5 VVG Billigungsklausel) |
| U2 | Vorschäden verschwiegen | Antrag "keine Vorschäden", aber Vorversicherer-Auskunft oder eigener Altbestand zeigt 2 Schäden | 1.5 % | UW-Assistenz, Betrug | Label `anzeigepflicht_verletzt`; im Schadenfall Rechtsfolge (Kürzung/Rücktritt) |
| U3 | Betriebsbeschreibung unscharf | "Allgemeine Bauarbeiten" ohne Angabe Dachdecken/Gerüstbau; Schaden aus Dacharbeit | 5 % der BHV | UW-Assistenz, Deckungsprüfung | Korrekter Branchencode und UW-Entscheid als Ground Truth |
| U4 | Umsatzmeldung abweichend | Gemeldeter Umsatz 40 % unter Vorjahr, während Mitarbeitendenzahl steigt | 3 % der BHV | Anomalieerkennung | Flag mit korrektem Umsatz |
| U5 | Dubletten Partner | Gleiche Person unter zwei Partner-IDs (Alt- und Neusystem; Schreibvariante "Müller"/"Mueller", Umzug) | 3 % der Partner | Entity Resolution | `dublette_von` |
| U6 | Verträge in Migration | Alt-Policennummer und neue Nummer parallel, Bedingungsversion im Altsystem anders als in MINT | 4 % der Verträge (PFM-K/M) | Datenqualität, RAG (welche AVB gilt?) | `bedingungen_version` verbindlich, Notiz zur Migration |
| U7 | Fehlerhafte Mahnung | Mahnung mit falscher Frist (10 statt 14 Tage) oder ohne Rechtsfolgenbelehrung → Deckungsunterbruch unwirksam; Schaden fällt in "Unterbruch" | 0.5 % | RAG, Deckungsprüfung | Juristische Auflösung: Deckung besteht |
| U8 | Kündigung unklar | Kündigungsschreiben ohne Policennummer, Kunde hat 3 Verträge (PHV, Hausrat, Motorfahrzeug); Kündigung per E-Mail an Vermittler statt Versicherer; Frist um 2 Tage verpasst | 15 % der Kündigungen | Klassifikation, Extraktion | Zuordnung und Fristbewertung als Ground Truth |
| U9 | Sprachmix CH | Antrag DE, Police DE, Korrespondenz FR, Schadenmeldung IT | 10 % der CH-Verträge | Mehrsprachige Extraktion | |
| U10 | Prämie stimmt nicht mit Tarif überein | Manueller Rabatt ohne Dokumentation, Altbestand-Tarif | 3–5 % | Anomalieerkennung, Tarifprüfung | Erklärung im Feld `praemie_abweichung_grund` (teils leer = echter Fehler) |
| U11 | Nebenerwerb in PHV | VN betreibt Etsy-Shop / Coaching nebenbei; Schaden bei Kunde | 1 % PHV | Deckungsprüfung (Generationen-abhängig) | PFZ-2021: bis CHF 10'000 Umsatz gedeckt; PFM-M: nicht gedeckt |
| U12 | Listenhund ohne Nachweis | Hund als "Mischling" deklariert, Schaden-Polizeirapport nennt "Amstaff-Mix" | 0.3 % | Betrug, Anzeigepflicht | |
| U13 | Wohnsitzwechsel DE-Bundesland | Umzug von Bayern (keine Hundehalterpflicht) nach Berlin (Pflicht) ohne Nachtrag | 0.5 % | Regelprüfung | |
| U14 | Vertragsdauer und Kündigungsrecht CH | 5-Jahres-Vertrag von 2020, Kunde kündigt 2023 unter Berufung auf Art. 35a VVG (gilt für Altverträge? Übergangsrecht) | 0.3 % | RAG (juristische Nuance) | Auflösung: Art. 35a gilt seit 1.1.2022 auch für bestehende Verträge (Übergangsbestimmung) |

### 8.2 Stolpersteine in Schäden

| Nr. | Stolperstein | Beschreibung | Häufigkeit | Use-Case | Auflösung |
|---|---|---|---|---|---|
| S1 | Unvollständige Meldung | Schadenmeldung ohne Schadendatum, ohne Geschädigten-Adresse, ohne Betrag; Freitext "Siehe Anhang" ohne Anhang | 15 % der Meldungen | Extraktion, Vollständigkeitsprüfung | Liste fehlender Pflichtfelder |
| S2 | Widersprüchliche Angaben zwischen Dokumenten | Meldung: Schaden 12.3.; Rechnung: Reparatur 10.3.; Foto-EXIF: 8.3.; Geschädigter: "Mitte März" | 8 % | Betrug, Extraktion, Reasoning | `enthaelt_widerspruch_zu`, Erklärung (Tippfehler vs. Betrug) |
| S3 | Falsche Sparte | Meldung "Kollision beim Ausparken mit Mietauto" (Motorfahrzeug → nicht PHV); Meldung "Handy selbst fallen gelassen" (Eigenschaden); Meldung "Einbruch" (Hausrat) | 6 % der Meldungen | Klassifikation, Triage | Korrekte Sparte + Ablehnungsgrund |
| S4 | Geschädigter = mitversicherte Person | Kind beschädigt Laptop des Vaters; Ehefrau verletzt beim Sturz über Kabel des Mannes | 3 % | Deckungsprüfung | Ausschluss Angehörige (mit Ausnahme Personenschäden in DE-Premium-Tarif ab 2023) |
| S5 | Grenzfall privat/beruflich | Lehrerin beschädigt Schul-Beamer; IT-Freelancer löscht Daten beim Nachbarn "als Gefallen"; Handwerker verursacht Schaden bei privater Nachbarschaftshilfe | 3 % | Deckungsprüfung, RAG | Auflösung je Bedingungsgeneration und Land |
| S6 | Grenzfall Obhut/Gefälligkeit | Geliehenes E-Bike gestürzt (Obhutsschaden, Sublimit); Beim Umzug helfen und Fernseher fallen lassen (Gefälligkeit, Sublimit, in PFM-K ausgeschlossen) | 5 % | Deckungsprüfung | Sublimit-Anwendung |
| S7 | Meldeverzug | Schaden 14 Monate nach Ereignis gemeldet, Geschädigter hat Anwalt; VN hat bereits Schuld schriftlich anerkannt | 4 % | Obliegenheitsprüfung, RAG | Rechtsfolge: Leistungskürzung nur bei Kausalität (CH Art. 38/45 VVG, DE § 28 VVG) |
| S8 | Deckungsunterbruch am Schadentag | Schaden während Suspension (Prämienverzug); Zahlung ging 1 Tag nach Schaden ein | 1 % | Deckungsprüfung | Nicht gedeckt (CH Art. 20 Abs. 3 VVG), mit U7 als Gegenfall |
| S9 | Bedingungsgeneration ändert Ergebnis | Identisches Ereignis (Schlüsselverlust, Krankheitsübertragung, Gefälligkeit, Drohne) unter PFM-K / PFM-M / PFZ | 5 % gezielt konstruiert | RAG, Deckungsprüfung | Tabelle mit Ergebnis je Generation |
| S10 | Sublimit und Selbstbehalt kombiniert | Obhutsschaden 6'500 bei Sublimit 5'000 und SB 200 → Zahlung 4'800 | 5 % | Berechnung | Rechenweg dokumentiert |
| S11 | Mitverschulden strittig | Ski-Kollision: beide Seiten geben dem anderen die Schuld; Zeugen widersprüchlich; FIS-Regeln | 3 % der Personenschäden | Haftungsprüfung, Summarization | Quote mit Begründung |
| S12 | Serienschaden | Handwerker verwendet fehlerhaftes Dichtmaterial bei 8 Kunden → 8 Meldungen, 1 Ereignis (1 SB, 1 Deckungssumme) | 2 Fälle | Verknüpfung, Aggregation | Serienschaden-ID |
| S13 | Passivregress ohne VN-Meldung | SUVA/Berufsgenossenschaft meldet Regress; VN hat nie gemeldet, weiss nichts | 2 % der Personenschäden | Triage, Vertragszuordnung | Vertrag über Name/Adresse suchen (Entity Resolution) |
| S14 | Geschädigter schreibt direkt, kein Vertrag findbar | Anspruchsschreiben nennt "Ihr Versicherter Herr X"; drei Partner mit dem Namen; einer ohne aktiven PHV | 2 % | Entity Resolution | |
| S15 | Anwaltsschreiben mit überhöhten Positionen | Forderung enthält nicht ersatzfähige Positionen (eigene Zeit des Geschädigten, Ärger, pauschale Unkosten), falsche Rechtsgrundlage (BGB in CH-Fall) | 30 % der Anwaltsschreiben | Extraktion, Prüfung | Position-für-Position-Bewertung |
| S16 | Medizinische Kausalität | HWS-Beschwerden 6 Monate nach Bagatellsturz; Vorerkrankung | 1 % | Personenschaden-Bewertung | Gutachten mit Teilkausalität |
| S17 | Zeitwert vs. Neuwert | Geschädigter fordert Neupreis, Rechnung von 2019; DE-Premium: Neuwert bis 500 EUR | 20 % der Sachschäden | Berechnung, RAG | Abschreibungstabelle |
| S18 | Reserve nie angepasst | Grossschaden mit Erstreserve 5'000, Anwaltsforderung 180'000, Reserve erst nach 8 Monaten erhöht | 1 % | Anomalie, Prozess-Mining | |
| S19 | Kulanzzahlung ohne Haftung | "Ohne Anerkennung einer Rechtspflicht" bei langjährigem Kunden trotz klarem Ausschluss | 2 % | Klassifikation (Kulanz erkennen), Compliance | Flag `kulanz` |
| S20 | Vollmachtsverletzung | Zahlung 12'000 von Stufe 1 freigegeben | 1 % der Zahlungen > 10'000 | Audit | |
| S21 | Fast-Track fälschlich | Automatisch bezahlter Schaden mit nachträglich erkanntem Betrugsmuster F1 | 0.5 % | Betrug (Modell-Evaluation) | |
| S22 | Journal mit Fachjargon und Abkürzungen | "GS meldet sich tel., will Neuwert. Erkl. ZW-Regel. GS ungehalten. RA angekündigt. Res. belassen." | alle Journale | Summarization, Sentiment | Lange Klartext-Version als Referenz für Stichprobe |
| S23 | OCR-Fehler und Handschrift | Beträge "1'2OO" statt "1'200", Datum "12.O3.24" | 10 % der Scans | Extraktion (Robustheit) | Ground Truth |
| S24 | Länderverwechslung | DE-Anwalt zitiert BGB, Schaden aber in CH mit CH-Vertrag; Betrag in EUR gefordert bei CHF-Vertrag | 1 % | RAG, Reasoning | Anwendbares Recht: Deliktsort/Vertrag |
| S25 | Ereignis vs. Meldung im Grenzjahr (BeHV) | Fehler 2021 (Vertrag Verstossprinzip), Anspruch 2024 (neuer Vertrag Claims-made, Rückwärtsdeckung ab 2022) → Deckungslücke oder Nachhaftung? | 5 Fälle | RAG, Reasoning | Auflösung: Nachhaftung Altvertrag |

### 8.3 Bewusste Unschärfen in Regelwerken

| Nr. | Unschärfe | Zweck |
|---|---|---|
| R1 | AVB-Ziffer für Gefälligkeitsschäden in PFZ-2021 nennt "bis CHF 10'000", Sublimit-Tabelle im Anhang "CHF 5'000" | RAG muss Widerspruch erkennen und Vorrangregel (Police > Besondere Bedingungen > AVB) anwenden |
| R2 | IPID (DE) formuliert "Schlüsselverlust mitversichert", BBR Basis-Tarif schliesst beruflich genutzte Schlüssel aus | Marketing-Kurzfassung vs. Bedingungsdetail |
| R3 | Schadenrichtlinie sagt "Gutachter ab 5'000", Vollmachtsregelung erwähnt Gutachterauftrag erst ab Stufe 2 (Zahlung bis 50'000), Praxis in Journalen: Gutachter ab 3'000 | Regel vs. gelebte Praxis |
| R4 | Zeichnungsrichtlinie CH und DE verwenden unterschiedliche Risikoklassen für gleiche Branche (Gastronomie CH 3, DE 4) | Länderunterschied ist gewollt; Frage "ist das ein Fehler?" |
| R5 | Altbedingungen enthalten Verweise auf aufgehobene Gesetzesartikel (Art. 12 VVG alt) | Historische Korrektheit; RAG muss Gültigkeit einordnen |
| R6 | Tarifhandbuch 2022 vs. 2024: Änderung Selbstbehaltfaktor, in Daten beide Generationen | Prämie nachrechnen erfordert Versionswahl |
| R7 | Zwei Klauseln mit ähnlicher Bezeichnung (`KL-CH-017 Ausschluss Dachdeckerarbeiten` vs. `KL-CH-071 Einschluss Dacharbeiten bis 3 m Höhe`) | Verwechslungsgefahr, präzises Retrieval nötig |
| R8 | Glossar definiert "Obhut" leicht anders als Bausteinbedingung "Sachen in Obhut" | Definitionskonflikte |

### 8.4 Zuordnung Stolpersteine zu Kurs-Use-Cases

| Use-Case | Primäre Stolpersteine | Empfohlener Datenausschnitt |
|---|---|---|
| Schadenklassifikation (Schadenart, Sparte, Komplexität) | S1, S3, S4, S5, S22, S23 | 2'000 Meldungen (S01/S02) mit Labels |
| Betrugserkennung | F1–F9, S2, S21, U2, U12 | 5'000 Schäden strukturiert + 500 mit Dokumenten, Label teilweise verdeckt |
| Dokumentextraktion | V02, V06, V14, S04, S07, S08, S17 mit Ground Truth; S23 | 300 Dokumente je Typ, Mix sauber/gescannt |
| RAG über Bedingungswerke | S5, S6, S9, S25, U7, U11, U14, R1–R8 | Alle Regelwerke + 100 Deckungsfragen mit Musterantwort und Zitat |
| Underwriting-Assistenz | U2, U3, U4, U10, U11, V03 | 500 Anträge BHV/BeHV mit UW-Entscheid |
| Schaden-Summarization / Next-Best-Action | S11, S18, S22, S19 | 200 Schadenakten mit Journal + Dokumenten |
| Entity Resolution / Datenqualität | U5, U6, S13, S14 | Partner- und Vertragsstamm mit Dubletten |
| Prozess-Mining / SLA | S18, Statushistorie, Fristen | Statusverlauf aller Schäden |

### 8.5 Didaktische Leitplanken

| Leitplanke | Begründung |
|---|---|
| Jeder Stolperstein hat eine dokumentierte Auflösung (Ground Truth + Begründung mit Regelwerkverweis) | Teilnehmende müssen Modelloutputs prüfen können; Kursleitung braucht Musterlösungen |
| Basisrate der Stolpersteine realistisch (nicht mehr als 20–25 % der Fälle "besonders") | Sonst lernen Modelle und Teilnehmende, dass alles verdächtig ist |
| Ehrliche Fälle enthalten einzelne Betrugssignale | False-Positive-Diskussion (Fairness, Kundenerlebnis) |
| Keine echten Personen, Firmen, Adressen (nur Strassennamen und Orte real); Namen aus generierten Listen; Firmen mit erkennbar fiktiven Namen | DSG/DSGVO, Reputationsschutz |
| Medizinische Daten fiktiv, aber ICD-konform; keine hochsensiblen Diagnosen (Psychiatrie, HIV) | Sensibilität im Kurskontext |
| Beträge und Verteilungen marktnah, aber nicht auf einen realen Versicherer rückführbar | Kein Wettbewerbsbezug |
| Sprachliche Vielfalt (Registerwechsel, Dialektspuren "isch", Tippfehler, Anglizismen bei IT-Kunden) | Realismus für NLP |
| Zeitraum Daten: 2015–2025, mit Schwerpunkt 2021–2025 (Post-Merger) | Migrationsartefakte und Bedingungsgenerationen abbildbar |

---

## 9. Empfohlene Mengengerüste und nächste Schritte

### 9.1 Mengengerüst Lehrdatensatz (Stichprobe aus fiktivem Bestand)

| Objekt | CH | DE | Total | Bemerkung |
|---|---|---|---|---|
| Partner (VN) | 3'000 | 5'000 | 8'000 | + 6'000 Geschädigte/Dritte |
| Verträge PHV | 2'400 | 4'200 | 6'600 | inkl. 12 % beendet |
| Verträge BHV | 500 | 700 | 1'200 | |
| Verträge BeHV | 150 | 250 | 400 | |
| Nachträge | 1'500 | 2'500 | 4'000 | |
| Schäden (2018–2025) | 1'800 | 3'200 | 5'000 | davon 220 Betrugsverdacht, 90 bestätigt |
| Zahlungen (Schaden) | 3'000 | 5'500 | 8'500 | |
| Zahlungen (Prämie) | 15'000 | 25'000 | 40'000 | |
| Dokumente (alle Typen) | 12'000 | 20'000 | 32'000 | davon 3'000 mit Ground-Truth-JSON |
| Regelwerke | 14 | 16 | 30 Dokumente | ~450 Seiten |
| Deckungsfragen mit Musterantwort (RAG-Evaluation) | 50 | 50 | 100 | |

### 9.2 Priorisierung für die Umsetzung

| Priorität | Arbeitspaket | Abhängigkeit |
|---|---|---|
| 1 | Codelisten und Datenmodell finalisieren (Kapitel 6) | – |
| 2 | Regelwerke schreiben: AVB/AHB je Generation, Sublimit-Tabellen, Schadenrichtlinie (Kapitel 7) | 1 |
| 3 | Tarifhandbuch und Prämienformel implementieren (Kapitel 7.5), damit Vertragsdaten konsistent sind | 1 |
| 4 | Vertrags- und Partnerstamm generieren inkl. Nachträge, Status, Migrationsartefakte | 1–3 |
| 5 | Schäden generieren (Verteilungen Kapitel 4.4), Betrugsmuster injizieren (4.5), Stolpersteine injizieren (8) | 2–4 |
| 6 | Dokumente generieren (Vorlagen je Typ, Kapitel 5) mit Ground Truth; Scan-/OCR-Degradation | 4–5 |
| 7 | Deckungsfragen-Katalog und Musterlösungen für RAG-Evaluation | 2, 5 |
| 8 | Qualitätssicherung: Konsistenzprüfungen (Prämie = Tarif, Zahlung ≤ Deckungssumme, Status-Reihenfolge, Vollmachtsstufe) mit dokumentierten Ausnahmen | 4–6 |
| 9 | Kurs-Dossier: Use-Case-Beschreibungen, Datenausschnitte, Lösungsskizzen (Kapitel 8.4) | 7–8 |

### 9.3 Offene Entscheidungen

| Frage | Optionen | Empfehlung |
|---|---|---|
| Fotos real generieren oder Platzhalter mit Metadaten? | (a) generierte Bilder, (b) Platzhalter + EXIF-JSON | (b) für erste Version; Bilder nur für 50 Showcase-Fälle |
| Französisch/Italienisch in CH-Dokumenten? | (a) nur DE, (b) 15 % FR / 5 % IT | (b), aber nur für PHV-Dokumenttypen S01–S03, V14, V20 |
| Eigene Anwalts-/Gutachtertexte oder Vorlagen mit Variablen? | (a) Vorlagen, (b) LLM-generiert mit Vorlagen-Constraints | (b) für Realismus, mit Review |
| Abbildung Motorfahrzeug-Haftpflicht? | (a) nein, (b) nur als "Fehlmeldung" | (b): Meldungen erscheinen, werden abgelehnt/weitergeleitet |
| Verknüpfung zur Lebensparte? | Gemeinsamer Partnerstamm (Kunde hat PHV und Leben) | Ja, gemeinsamer Partnerstamm; Cross-Selling-Signale als Bonus-Use-Case |
