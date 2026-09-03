---
dokument_id: DOC-STAMM-LV
titel: Stammdaten Leben – Erläuterung für Dozenten
typ: unternehmen
sparte: LV
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

# Stammdaten Leben – Erläuterung für Dozenten

Dieses Dokument erklärt, was in `data/reference/lv/` steckt, welche fachlichen Entscheidungen dahinterstehen und wo die didaktischen Fallen liegen. Das Data Dictionary mit allen Spalten steht in `data/reference/lv/README.md`.

## 1. Was die Stammdaten leisten

Die Lebensversicherung ist die Sparte mit dem längsten Gedächtnis: Verträge aus dem Jahr 1985 laufen am Stichtag 2025 noch. Die Stammdaten müssen deshalb zehn Tarifgenerationen mit ihren jeweils eigenen Rechnungszinsen, Sterbetafeln, Bedingungen, Fragebögen und Annahmerichtlinien tragen. Sie beantworten:

1. **Was wird verkauft und was wurde früher verkauft?** Vier Produkte, wobei die gemischte Lebensversicherung in Deutschland nur noch als Altbestand existiert.
2. **Wie wird geprüft?** Gesundheitsfragebogen in fünf Versionen, Diagnose-Bibliothek, Annahmerichtlinien mit BMI-, Raucher- und Berufsgruppentabellen.
3. **Was kostet es und was ist es wert?** Tarifformel, Sterbetafeln, Überschussparameter, Rückkaufregeln.
4. **Was passiert im Leistungsfall?** Leistungsarten mit Nachweisen und Durchlaufzeiten, Betrugsmuster, Kulanzfälle.
5. **Wie sieht es in den Systemen aus?** Status- und Entscheidungscodes in VERA, SILAS und MINT.

## 2. Tarifgenerationen als Rückgrat

Die zehn Generationen von PK-85 bis PZ-2025 bilden die historischen Höchstrechnungszinsen in Deutschland ab (4.0 Prozent bis 0.25 Prozent, ab 2025 wieder 1.0 Prozent), den Unisex-Bruch am 21. Dezember 2012 und die Ablösung alter Sterbetafeln. Jede Generation verweist auf eigene Bedingungswerke, Fragebogenversionen und Annahmerichtlinien.

Für Dozenten wichtig: Dieselbe Frage („Ist ein Suizid im zweiten Vertragsjahr gedeckt?", „Wie hoch ist der Rückkaufswert nach drei Jahren?") hat je nach Generation eine andere Antwort. Das ist die Grundlage der RAG-Übung mit widersprüchlichen Bedingungsversionen und der Grund, warum jedes Dokument einen Metadaten-Header mit Generation und Gültigkeit trägt.

## 3. Risikoprüfung und die eingebauten Bias-Fallen

`annahmerichtlinie_tabellen.yaml` enthält den historischen Bias bewusst und markiert ihn mit `didaktik_falle: true`. Drei Fallen sind zentral für den Use Case zur Risikoprüfung mit historischem Bias:

- **Tarifzonen-Zuschlag bis 2019:** Pfefferminz erhob in ländlichen Zonen einen Zuschlag, in deutschen Grossstadtquartieren mit hohem Ausländeranteil einen weiteren. Die Zone ist dieselbe, die in der Haftpflicht als legitimer Regionalfaktor dient. Ein Modell, das auf den Underwriting-Entscheidungen bis 2019 trainiert, lernt diesen Zuschlag als Muster.
- **Nationalitätsfaktor bis 2007:** In den ältesten Verträgen als Zuschlagscode sichtbar, seit der Richtlinie 2008 gestrichen. Er erlaubt die Diskussion, wie lange gestrichene Regeln in Daten nachwirken.
- **Geschlechtsabhängige Prämien in Deutschland bis 2012:** Für Neugeschäft unzulässig, in der Schweiz weiterhin erlaubt. Ein Modell muss den Markt und das Abschlussdatum kennen, um korrekt zu urteilen.

Dazu kommen Generationenunterschiede in der medizinischen Bewertung (BMI 30 bis 32.9 in alten Richtlinien strenger; HIV bis 2014 Ablehnung, danach Zuschlag). Diese Unterschiede sind in `diagnose_bibliothek.csv` in der Spalte für Richtlinienabweichungen hinterlegt.

Die Kompetenzregel „Ablehnungen und Zurückstellungen nie automatisch" gilt in beiden Sparten. Die Minzia-Engine entscheidet nur positive Fälle bis Risikoklasse 2 und protokolliert alles; zehn Prozent werden manuell nachgeprüft. Für die Governance-Übung ist die Risikoprüfung Leben das Hochrisikosystem nach EU AI Act Anhang III.

## 4. Gesundheitsdaten

Gesundheitsfragen sind Ja/Nein-Fragen mit Freitext. Diagnosen kommen aus einer Bibliothek auf ICD-10-Gruppenebene mit drei Freitextvarianten je Diagnose, darunter eine mit Tippfehlern. Der Generator zieht Diagnosen unabhängig von Identitätsmerkmalen. Trotzdem sollen Teilnehmer diese Daten als besondere Kategorie behandeln: Die Übung zum Detektor für personenbezogene und Gesundheitsdaten baut darauf auf, dass Diagnosen auch in E-Mail-Betreffzeilen und Aktennotizen auftauchen.

## 5. Tarif, Überschuss, Rückkauf

Die Tarifformel in `tarifformel.md` ist eine in Excel nachvollziehbare Näherung: Risikoprämie mit der Sterbewahrscheinlichkeit am mittleren Alter, annuitätische Sparprämie mit dem Rechnungszins, Kostenzuschläge je Generation. Sie ist keine aktuarielle Kalkulation, aber innerhalb der Richtwerte der Planung.

`ueberschuss_parameter.csv` zeigt, warum Hochzinsgenerationen ein Problem sind: Bei PK-95 mit 4.0 Prozent Garantie liegt die Gesamtverzinsung seit Jahren darunter, der Zinsüberschuss ist null. Das ist Stoff für Analytics-Übungen zur Bestandsstruktur.

Die Rückkaufparameter machen die Zillmerung greifbar: Altverträge haben in den ersten zwei Jahren einen Rückkaufswert nahe null. Kundenbeschwerden darüber sind Teil des Korpus.

## 6. Leistungsfall, Betrug, Kulanz

`leistungsarten.csv` unterscheidet Standardfälle von Frühfällen (Tod innerhalb der ersten Jahre mit obligatorischer Nachprüfung der Anzeigepflicht), Auslandsfällen und Verschollenheit. `betrugsmuster.csv` gibt jedem Muster einen **False-Positive-Zwilling**: einen legitimen Fall mit denselben Signalen. `kulanzfaelle.csv` beschreibt Situationen, in denen die Regelungslage in der Schweiz und in Deutschland verschieden ist und die Entscheidung von der Kulanzstufe abhängt.

Die sichtbaren Betrugslabels sind unvollständig: nur aufgedeckte Fälle sind markiert, die Aufdeckungsquote steht je Muster in der Tabelle. Die vollständige Wahrheit liegt in der Ground Truth. Ein Modell, das auf sichtbaren Labels trainiert, reproduziert die Aufdeckungspraxis, nicht den Betrug.

## 7. Konkretisierte Annahmen und Abweichungen von der Planung

Feste Werte statt Spannen sind im Data Dictionary dokumentiert. Bewusste Vereinfachungen: drei statt zehn Sterbetafeln (Zuordnung je Generation), Risikoprämie mit mittlerem Alter, keine Fondskurse (Entscheidung E12), keine Basisrente und kein Riester (E06). Die Rückkaufstabellen der Altgenerationen sind Setzungen.

## 8. Offene Punkte für Welle 3 und 4

- Die ausformulierten Regelwerke (AVB je Generation, Annahmerichtlinien ARL-2008 bis ARL-2025, Leistungsprüfungsrichtlinie) entstehen in Welle 4 aus diesen Tabellen.
- Die Zielanteile der Underwriting-Entscheidungen sind vor Erzeugung der Stufe M gegen die Kennzahlen-Masterdatei abzugleichen.

---

Pfefferminzia ist ein frei erfundenes Unternehmen für Lehrzwecke. Alle Personen, Firmen, Adressen, Verträge, Schäden, Kennzahlen und Ereignisse sind synthetisch erzeugt. Ähnlichkeiten mit real existierenden Personen, Unternehmen oder Marken, insbesondere mit gleichnamigen Medien oder Dienstleistern, sind unbeabsichtigt und nicht intendiert. Rechtliche und regulatorische Aussagen sind vereinfacht, Stand 2026, und ersetzen keine Rechtsberatung. Teile dieses Materials wurden mit Unterstützung von KI erzeugt.
