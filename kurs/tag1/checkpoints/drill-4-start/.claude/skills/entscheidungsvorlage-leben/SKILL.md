---
name: entscheidungsvorlage-leben
description: Verwenden, sobald jemand eine Entscheidungsvorlage der Risikoprüfung Leben oder ein Kundenschreiben zu einem Antrag auf Lebensversicherung (RisikoLeben, Vorsorge, RentePlus, EU/BU-Baustein) verlangt. Liest Annahmerichtlinie und Kompetenzordnung vollständig, prüft in fester Reihenfolge (Prüfumfang, Gewicht, Nikotin, Beruf, Vorerkrankungen, Freizeit, Kombination/Risikoklasse, Kompetenz), zählt Zuschläge nach der Richtlinie zusammen, sagt System oder Mensch entscheidet, erzeugt die achtteilige Vorlage in meine-ergebnisse und ergänzt den Cockpit-Reiter Underwriting.
---

# Entscheidungsvorlage Leben

Dieser Skill hält fest, wie in diesem Projekt eine Entscheidungsvorlage der Risikoprüfung Leben und, falls verlangt, ein zugehöriges Kundenschreiben entstehen. Er gilt für jeden künftigen Antrag auf RisikoLeben, Vorsorge, RentePlus oder den Zusatzbaustein Erwerbs- und Berufsunfähigkeit, unabhängig von Name, Summe oder Ergebnis des Einzelfalls.

## 1. Quellen, die vollständig gelesen werden, nicht aus dem Gedächtnis zitiert

1. `docs/regelwerke/RW-LV-ARL-2025.md` – Annahmerichtlinie Leben (ARL-2025), ganz lesen, auch wenn nur ein Paragraf gebraucht wird: Tabellenwerte ändern sich zwischen Richtlinien-Versionen und dürfen nicht aus einer früheren Antwort im Gespräch übernommen werden.
2. `docs/regelwerke/RW-GRUPPE-R08-2025.md` – Kompetenzordnung (R08), mindestens § 1, § 4, § 5 und § 8.
3. Die Fallunterlagen des Antrags:
   - bei bestehenden Kunden: alle Dateien unter `data/documents/S/personas/<PTR-…>/`, die sich auf den Antrag beziehen (Antrag, Gesundheitserklärung, Arztzeugnisse, Vertrauensarztbericht, Gegenofferte, Korrespondenz) – vollständig, nicht nur eine Auswahl;
   - bei neuen, noch offenen Anträgen: die Datei unter `kurs/tag1/antragseingang/`.
4. Falls ein Vergleich mit einem bereits getroffenen Entscheid verlangt wird: die bereinigten Tabellen (`antrag.csv`, `vertrag.csv`) und die entsprechenden Dokumente/E-Mails der Fallakte für Datum, Entscheiderinnen und Ergebnis.
5. Bei Bedarf `data/reference/lv/` für Tarifgenerationen- oder Berufsgruppen-Codes.

Am Kopf der Vorlage immer einen Bewertungsstand nennen: entweder das von der Nutzerin oder dem Nutzer vorgegebene Datum, sonst das Datum der jüngsten vorliegenden Unterlage. Nur Unterlagen bis zu diesem Stand verwenden.

## 2. Prüfschritte in fester Reihenfolge

Immer in dieser Reihenfolge prüfen und jeden Schritt mit seinem Paragrafen belegen:

1. **Prüfumfang (§ 2 ARL-2025).** Todesfallsumme in die Stufentabelle einordnen (bis 300'000 / 750'000 / 1'500'000 / darüber) und die dafür verlangten Unterlagen nennen. Ist die versicherte Person bei Antragseingang 55 Jahre oder älter, gilt zwingend die nächststrengere Stufe – diese Alters-Verschärfung nie übersehen. Bei einer EU/BU-Rente über 2'500 je Monat zusätzlich Facharztbericht und Berufsnachweis, Laborumfang wie in § 2 angegeben. Danach abgleichen, welche der verlangten Unterlagen tatsächlich vorliegen.
   - **Liegt eine vorgeschriebene Unterlage nicht vor:** das ausdrücklich festhalten, die Bewertung als vorläufig kennzeichnen und in der Empfehlung nicht auf Annahme, Zuschlag oder Ablehnung schliessen. Die Empfehlung lautet dann, die fehlende Unterlage anzufordern, bevor irgendjemand entscheidet; eine bereits berechnete Risikoklasse dient nur der Einordnung, nicht der Entscheidung.
2. **Gewicht (§ 3).** BMI aus Grösse und Gewicht berechnen (kg / m², eine Nachkommastelle), passende Altersgruppe (18–39, 40–59, 60+) und passende Zieldeckung (Tod oder EU/BU) wählen, Zuschlag oder Ablehnung gemäss Tabelle.
3. **Nikotin (§ 4).** Konsum der letzten 12 Monate inklusive E-Zigaretten (Schweiz zusätzlich Snus) prüfen. Ergibt Nichtraucher- oder Rauchertarif; bei mehr als 20 Zigaretten pro Tag zusätzlich einen Prozentzuschlag.
4. **Beruf (§ 5).** Nur bewerten, wenn eine EU/BU-Zusatzdeckung beantragt ist. Ohne diese Deckung als nicht anwendbar vermerken, nicht einfach weglassen.
5. **Vorerkrankungen (§ 6).** Jede angegebene Diagnose einzeln der ICD-10-Tabelle zuordnen, mit Zuschlag, Zurückstellung, Ablehnung oder Normal sowie der geforderten Nachweisart; bei Hypertonie geht Tabelle 6.1 der allgemeinen Zeile vor. Fehlt der in der Tabelle verlangte Nachweis, das als offenen Punkt vermerken statt den Zuschlag ohne Beleg anzusetzen.
6. **Freizeit (§ 7).** Promillezuschlag auf die Versicherungssumme oder Ausschluss; nicht aufgeführte, ungefährliche Aktivitäten gelten als normal.
7. **Kombination und Risikoklasse (§ 8).** Siehe Abschnitt 3 unten.
8. **Kompetenz (§ 9 ARL-2025, § 4 Kompetenzordnung).** Siehe Abschnitt 4 unten.

## 3. Wie Zuschläge zusammengezählt werden (§ 8)

- Methode: additiv in Prozent. Addiert werden die Prozentzuschläge aus § 3 (Gewicht), § 4 (nur der Teil oberhalb 20 Zigaretten pro Tag), § 5 (nur bei EU/BU-Deckung) und § 6 (bei mehreren Diagnosen alle einzeln addieren).
- **Was nicht in die Prozentsumme einfliesst:**
  - Der Rauchertarif selbst (Faktor 2.0) ist ein eigener Tarif, kein Prozentzuschlag.
  - Freizeitzuschläge nach § 7 werden getrennt in Promille auf die Versicherungssumme erhoben, nie in die Prozentsumme gemischt.
  - Übergewicht wird ausschliesslich nach § 3 bewertet; die ICD-Zeile E66 (Adipositas) daneben nicht zusätzlich ansetzen, das wäre eine Doppelzählung desselben Befunds.
  - Ergebnisse genetischer Untersuchungen fliessen nie ein (§ 1 Nr. 3), auch wenn sie vorliegen.
- Die Summe der Prozentzuschläge ergibt über die Tabelle in § 8 die Risikoklasse 1 (normal) bis 5 (Ablehnung ab 251 %).
- **Lässt eine Tabellenzeile eine Spanne offen** (wie Tabelle 6.1 bei Hypertonie) oder muss aus einem anderen Grund innerhalb eines Rahmens gewählt werden: in der Vorlage die möglichen Werte nennen, dafür- und dagegensprechende Befunde auflisten, einen Wert vorschlagen und begründen, die Wahl aber ausdrücklich als **offen, bis die Nutzerin oder der Nutzer entscheidet** markieren. Nie selbst eine verbindliche Wahl innerhalb einer Spanne treffen.

## 4. Wer entscheiden darf (§ 9 ARL-2025, § 4 und § 5 Kompetenzordnung)

- Automatische Annahme (System): nur Risikoklasse bis 2, Todesfallsumme bis 400'000, EU/BU-Rente bis 2'000 je Monat, ausschliesslich positive Entscheide ohne jede Erschwerung.
- Sachbearbeitung: bis Risikoklasse 3, Summe bis 750'000.
- Gesellschaftsarzt: bis Risikoklasse 4, Summe bis 1'500'000.
- Rückversicherung: ab Summe 1'500'001, zusätzlich bei einer Annahme in Risikoklasse 4.
- **Zuschläge, Ausschlüsse, Zurückstellungen und Ablehnungen werden nie automatisiert entschieden**, unabhängig von der Risikoklasse. Ablehnungen und Zurückstellungen entscheidet immer der Gesellschaftsarzt, über 1'500'000 zusätzlich mit der Rückversicherung. Das gilt gruppenweit: jede ablehnende Entscheidung trifft eine natürliche Person.
- In der Vorlage und im Cockpit-Reiter immer explizit benennen, welche Stufe zuständig ist, und den Schritt, an dem ein Mensch statt eines Systems entscheidet, sichtbar kennzeichnen.

## 5. Was nie in eine Entscheidung einfliessen darf (§ 1)

- Nationalität, Herkunft und der Wohnort als Proxy für Herkunft.
- Ergebnisse genetischer Untersuchungen – dürfen weder verlangt noch verwendet werden, auch wenn sie der antragstellenden Person vorliegen und angeboten werden.
- Das Geschlecht bei Neugeschäft in Deutschland (Unisex-Grundsatz).
- Aufgehobene Altmerkmale (Tarifzonen-Zuschlag, Nationalitätsfaktor) auch nicht bei Nachprüfungen wieder anwenden.
- Diesen Abschnitt als eigenen, festen Punkt „Was nicht in die Entscheidung einfliessen darf" in jede Vorlage aufnehmen, auch wenn im Einzelfall keines der Merkmale genannt wurde.

## 6. Was nie in ein Kundenschreiben gehört

- Keine Diagnosen und keine medizinischen Einzelheiten. Ein Kundenschreiben nennt nur Entscheid, Zuschlag (in Prozent oder als Tarif) und die Möglichkeit einer späteren Nachprüfung (§ 9 Nr. 5). Medizinische Begründungen gehen auf Wunsch an den behandelnden Arzt oder werden dem Gesellschaftsarzt zur persönlichen Erläuterung überlassen.
- Gesundheitsdaten werden getrennt von Vertriebsdaten behandelt und nie in einem an die Kundin oder den Kunden adressierten Schreiben wiedergegeben (§ 1 Nr. 4).
- Für Form und Ablage gelten zusätzlich die allgemeinen Regeln für Kundenschreiben dieses Projekts: Dateiname `meine-ergebnisse/<nachname>-antwort-kunde.md`, keine Frontmatter, nur höchstens eine Zeile „Entwurf, Stand TT.MM.JJJJ, zur Freigabe durch …" über dem eigentlichen Schreiben, deutsches oder Schweizer Zahlen- und Rechtschreibformat je nach Markt, jeder Absatz als eine Zeile, Unterschrift mit Name und Funktion, fehlende Angaben als sichtbarer Platzhalter.

## 7. Gliederung der Entscheidungsvorlage und Ablage

Datei: `meine-ergebnisse/entscheidungsvorlage-<nachname>.md`. Titelzeile mit Name, darunter eine Zeile mit Antrags- und ggf. Partnernummer, Bewertungsstand und Datenbasis. Danach genau diese Abschnitte, in dieser Reihenfolge und mit diesen Überschriften:

1. Antrag in Kürze
2. Prüfumfang und vorliegende Unterlagen
3. Bewertung Schritt für Schritt (Gewicht, Nikotin, Beruf, Vorerkrankungen, Freizeit), je mit Paragraf und Zuschlag in Prozent
4. Gesamtzuschlag und Risikoklasse
5. Wer entscheidet, System oder Mensch, und auf welcher Stufe
6. Empfehlung
7. Offene Rückfragen
8. Was nicht in die Entscheidung einfliessen darf

Einen Abschnitt „Vergleich mit dem damaligen Entscheid" nur anhängen, wenn ausdrücklich ein Vergleich mit einem bereits getroffenen Entscheid verlangt wird, und dann als letzten Abschnitt.

Jede Vorlage endet, nach allen Abschnitten, mit der Zeile:

`Entscheid durch: …, Datum: …`

Name und Datum stehen dort nur, wenn eine Nutzerin oder ein Nutzer im Gespräch selbst entschieden hat (Name und Datum dieser Entscheidung eintragen). Ist noch niemand aus einem Gespräch entschieden – etwa weil die Vorlage gerade erst erstellt wurde oder weil wie in Abschnitt 2 zuerst fehlende Unterlagen angefordert werden müssen –, steht dort „offen". Ein von mir selbst vorgeschlagener oder berechneter Wert füllt diese Zeile nie.

**Trifft die Nutzerin oder der Nutzer im Gespräch eine Entscheidung**, die von einem Vorschlag, einer offenen Spanne oder einer vorläufigen Empfehlung abweicht: in der Vorlage jeden Satz, der dieser Entscheidung jetzt widerspricht oder die Sache noch offen nennt, nicht löschen, sondern mit Markdown-Durchstreichung (`~~Text~~`) sichtbar stehen lassen, und unmittelbar danach die neue Fassung mit dem Vermerk „entschieden durch [Name]" ergänzen. Zugleich die Schlusszeile `Entscheid durch: …, Datum: …` von „offen" auf den Namen und das im Gespräch genannte oder aktuelle Datum setzen. So bleibt nachvollziehbar, was sich geändert hat und warum.

## 8. Cockpit-Reiter «Underwriting»

Jeder neue oder inhaltlich geänderte Antrag kommt in den Reiter Underwriting von `meine-ergebnisse/cockpit.html`:

- Links in die Liste: Antragsteller/in, Antragsnummer, Summe, Risikoklasse, kurze Empfehlung.
- Rechts beim Anklicken: der Regelpfad als nummerierte Schrittfolge in der Reihenfolge aus Abschnitt 2 (Prüfumfang, Gewicht, Nikotin, Beruf, Vorerkrankungen, Freizeit, Kombination und Risikoklasse, Kompetenz), je mit Paragraf und Ergebnis in Worten. Der Schritt, an dem eine natürliche Person statt eines Systems entscheidet, wird rot markiert mit der Marke „Hier entscheidet ein Mensch". Darunter erscheint die vollständige Vorlage aus Abschnitt 7, im selben Cockpit-Format wie der übrige Text (keine rohen `#`, `**`, `~~` oder `---`, Umlaute und echte Sonderzeichen).
- Die Daten entstehen in `meine-ergebnisse/skripte/underwriting.py`: liest die Markdown-Vorlagen aus `meine-ergebnisse/` und den dazugehörigen Regelpfad, schreibt nach `meine-ergebnisse/cockpit-daten/underwriting.js`. Für einen neuen Antrag: einen neuen Eintrag in der Antragsliste und einen neuen Regelpfad im Skript ergänzen, dann das Skript ausführen. Für eine nachträgliche Entscheidung: die betroffenen Regelpfad-Texte ebenso mit `~~…~~` und dem Vermerk „entschieden durch [Name]" aktualisieren.
- Nach jeder Änderung das Skript neu ausführen und die betroffene Stelle im Cockpit per Screenshot prüfen (Bestand und Akte bleiben dabei unverändert).

## 9. Ablauf, wenn dieser Skill greift

1. Auftrag einordnen: Entscheidungsvorlage, Kundenschreiben oder beides verlangt?
2. Quellen aus Abschnitt 1 vollständig lesen.
3. Prüfschritte aus Abschnitt 2 der Reihe nach durchgehen, Zuschläge nach Abschnitt 3 zusammenzählen.
4. Kompetenzstufe nach Abschnitt 4 bestimmen.
5. Abschnitte 5 und 6 nicht vergessen, auch wenn im Einzelfall nichts davon einschlägig scheint.
6. Vorlage nach Abschnitt 7 schreiben und ablegen; Kundenschreiben, falls verlangt, nach den dort verlinkten Regeln.
7. Cockpit-Reiter Underwriting nach Abschnitt 8 ergänzen oder aktualisieren.
8. Bei einer nachträglichen Entscheidung: Durchstreichen statt Löschen, Vermerk „entschieden durch [Name]", Vorlage, Regelpfad und Cockpit-Daten neu abgleichen.
