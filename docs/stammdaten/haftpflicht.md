---
dokument_id: DOC-STAMM-HP
titel: Stammdaten Haftpflicht – Erläuterung für Dozenten
typ: unternehmen
sparte: HP
markt: GRUPPE
sprache: de-CH
version: "1.0"
gueltig_ab: 2026-09-03
gueltig_bis: null
tarifgeneration: null
quelle_system: null
absender: Projektteam Pfefferminzia-Datensatz
vertraulichkeit: intern
erzeugt_am: 2026-09-03
---

# Stammdaten Haftpflicht – Erläuterung für Dozenten

Dieses Dokument erklärt, was in `data/reference/hp/` steckt, welche fachlichen Entscheidungen dahinterstehen und wo die didaktischen Fallen liegen. Das Data Dictionary mit allen Spalten steht in `data/reference/hp/README.md`.

## 1. Was die Stammdaten leisten

Die Haftpflicht-Stammdaten sind das Regelwerk, aus dem der Generator später Verträge, Schäden, Zahlungen und Dokumente ableitet. Sie beantworten fünf Fragen:

1. **Was wird verkauft?** Drei Produkte (Privat-, Betriebs-, Berufshaftpflicht) mit Bausteinen, Deckungssummen, Selbstbehalten und vier Bedingungsgenerationen.
2. **Wer wird versichert?** Branchenklassen für Betriebe, Berufsgruppen für Freiberufler, Tarifzonen für den Wohn- oder Betriebsort.
3. **Was kostet es?** Eine nachrechenbare Tarifformel mit allen Faktoren.
4. **Was passiert?** Schadenarten mit Häufigkeit, Höhe, Dauer und Saisonalität; Lebenszyklusraten für Neugeschäft, Storno, Nachträge und Mahnungen; Betrugsmuster.
5. **Wer darf was?** Vollmachtsstufen, Ablehnungsgründe, Statusmodelle in drei Systemwelten.

## 2. Produkte und Generationen

| Produkt | Marktname | Rolle im Datensatz |
|---|---|---|
| Privathaftpflicht | PrivatPlus | Massengeschäft, kleine Schäden, höchstes Betrugspotenzial, einziges Produkt von Minzia (MZ-DIRECT) |
| Betriebshaftpflicht | BusinessProtect | Underwriting nach Branchenklasse, Bearbeitungsschäden im Handwerk, Regress |
| Berufshaftpflicht | ProfessionalShield | Wenige, grosse, langlaufende Vermögensschäden; Claims-made gegen Verstossprinzip |

Die vier Generationen sind die wichtigste fachliche Konstruktion: **HP-KLASSIK** (bis 2012), **HP-MODERN** (2013 bis 2020), **MZ-DIRECT** (Minzia, 2021 bis 2024, nur Privathaftpflicht) und **PM-2025** (Pfefferminzia ab Closing). Dasselbe Schadenereignis ist je nach Generation unterschiedlich gedeckt, etwa Gefälligkeitsschäden, Obhutsschäden oder Schlüsselverlust. Die Datei `ablehnungsgruende.csv` verweist deshalb je Generation auf unterschiedliche Bedingungsziffern. Das ist die Grundlage für die RAG-Übung mit widersprüchlichen Bedingungsversionen.

## 3. Tarifierung

Die Formel in `tarifformel.md` ist multiplikativ und in Excel nachrechenbar. Drei bewusste Eigenschaften:

- **Generationsfaktor:** Altverträge sind günstiger, weil Pfefferminz nie alle Bestände auf den aktuellen Tarif gehoben hat. Die Prämienharmonisierung 2025 ist eine der Ursachen für den Storno-Anstieg bei Ex-Pfefferminz-Kunden.
- **Tarifzonen:** Die Zone eines Orts steht in den Geo-Referenzen. In der Lebensversicherung dient dieselbe Zone als historischer Bias-Faktor; in der Haftpflicht ist sie ein legitimer Regionalfaktor. Der Kontrast eignet sich für die Diskussion, wann ein Merkmal fachlich begründet und wann diskriminierend ist.
- **Abweichungen:** Drei bis fünf Prozent der Verträge weichen vom Tarif ab. Sie sind in der Ground Truth markiert und dienen Anomalie-Übungen.

## 4. Schäden

`schadenarten.csv` enthält je Produkt und Markt die Anteile der Schadenarten sowie Lognormal-Parameter für den Gesamtaufwand. Median, Mittelwert und Quantile aus Planung 01 §4.4.3 sind daraus rekonstruierbar. Zwei Punkte für Dozenten:

- Die **Trennung von Deckungsprüfung und Haftungsprüfung** ist die konzeptionelle Kernbotschaft der Sparte. Ablehnungsgründe sind deshalb nach `deckung` und `haftung` getrennt; im Datenmodell erhalten beide eigene Statusfelder.
- **Nullschäden** (gemeldet, aber ohne Zahlung) machen je nach Schadenart 10 bis 55 Prozent aus. Modelle, die nur auf Zahlungen trainieren, unterschätzen den Aufwand der Sachbearbeitung. Das ist ein Lernmoment für Analytics-Übungen.

Die Saisonalitätsprofile (Wintersport, Bausaison, Heizperiode, Jahresendmeldungen bei Claims-made) erzeugen erkennbare Muster in Zeitreihen.

## 5. Betrug

Neun Betrugsmuster (F1 bis F9) mit strukturierten und dokumentbasierten Signalen. Wichtig für die Betrugserkennungs-Übung: **ehrliche Fälle tragen bewusst einzelne Betrugssignale** (Wochenendschaden, Meldung ohne Zeugen, Geschädigter aus dem Bekanntenkreis). Ein Modell, das auf diesen Signalen naiv trainiert, produziert viele False Positives. Die Diskussion über Kosten falscher Verdächtigungen gegenüber Kunden gehört zur Übung.

## 6. Systemwelten

`status_codes.csv` führt jeden Status in drei Kodierungen: curated (lesbar), HAPO und SILAS (Altsysteme, numerisch oder kryptisch, teils undokumentiert), MINT (drei Schema-Versionen mit Drift). Dozenten sollten die Teilnehmer den undokumentierten Stornocode im Altsystem selbst entdecken lassen; er ist in der Ground Truth erklärt.

## 7. Kompetenzen und Governance

`vollmachtsstufen.csv` legt fest, was Automatik, Sachbearbeitung, Teamleitung, Abteilungsleitung und Geschäftsleitung entscheiden dürfen. Zwei Regeln sind für die KI-Governance-Übung zentral: **Ablehnungen werden nie automatisch entschieden**, und Fast-Track-Zahlungen der Automatik setzen einen Betrugsscore unter 0.3 voraus. Im Datensatz verletzen ein bis zwei Prozent der Zahlungen die Vollmachtsstufe; das ist die Audit-Übung.

## 8. Konkretisierte Annahmen

Planung 01 nennt vielfach Spannen. Die Stammdaten wählen feste Werte, dokumentiert im Data Dictionary. Abweichungen von der Planung: Risikoklassen 1 bis 5 statt 1 bis 6; NOGA- und WZ-Codes sind auf vierstelliger Ebene identisch, weil beide auf NACE Rev. 2 beruhen; Schlüsselverlust ist keine eigene Schadenart, sondern liefert nur die Sublimit-Verteilung.

## 9. Offene Punkte für Welle 4 und 5

- Die Bedingungswerke selbst (AVB CH, AHB DE je Generation) entstehen in Welle 4; die Ziffernverweise in `ablehnungsgruende.csv` sind dafür verbindlich.
- Die Verteilungsparameter sind vor der Erzeugung der Stufe M gegen die Kennzahlen-Masterdatei zu prüfen, damit Schadenquoten und Combined Ratio zusammenpassen.

---

Pfefferminzia ist ein frei erfundenes Unternehmen für Lehrzwecke. Alle Personen, Firmen, Adressen, Verträge, Schäden, Kennzahlen und Ereignisse sind synthetisch erzeugt. Ähnlichkeiten mit real existierenden Personen, Unternehmen oder Marken, insbesondere mit gleichnamigen Medien oder Dienstleistern, sind unbeabsichtigt und nicht intendiert. Rechtliche und regulatorische Aussagen sind vereinfacht, Stand 2026, und ersetzen keine Rechtsberatung. Teile dieses Materials wurden mit Unterstützung von KI erzeugt.
