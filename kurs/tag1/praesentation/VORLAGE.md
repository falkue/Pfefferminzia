# Vorlage «Minze klar» für Präsentationen

`vorlage.html` ist ein Foliensatz mit reveal.js 5 im Pfefferminzia-Design, Format 1280 × 720 Pixel.
Er enthält je einen Baustein jeder Folienart. Für eine Präsentation die Vorlage nach
`meine-ergebnisse/praesentation.html` kopieren und dort arbeiten; die Vorlage selbst bleibt unverändert.

## Regeln

1. **Eine Aussage pro Folie.** Der Titel ist diese Aussage als ganzer Satz mit Verb
   (Action Title): «Wir verlieren vor allem Kunden aus X», nicht «Stornoquote». Eine Zeile,
   höchstens rund 60 Zeichen. Wer nur die Titel liest, kennt die Geschichte. Ausnahme Titelfolie:
   Titel höchstens zwei Zeilen, Untertitel höchstens zwei Zeilen, Gremium und Name zusammen höchstens
   vier Zeilen, Datenstand eine Zeile.
2. **Der Untertitel belegt den Titel** mit der Zahl, die ihn trägt.
3. **Jede Zahl mit Quelle und Definition** in der Quellzeile unten: Tabelle oder Unterlage in
   Worten, Stichtag, was gezählt wird (etwa «aktiv am 31.12.», «Storno ohne Tod, Widerruf,
   Ablauf, geteilt durch den Bestand am 1.1.»). Keine Dateipfade, keine Spaltennamen. Zahlen aus den
   eigenen Ergebnissen oder frisch aus den Tabellen, nie geschätzt; Zahlen für das ganze
   Unternehmen, die sich im Datensatz nicht nachzählen lassen, als solche kennzeichnen.
4. **Mindestschrift 19 px** für Fliesstext, **15 px** für Beschriftungen, Quellen, Achsen.
   Passt ein Text nicht, kürzen, nicht verkleinern. Zu lange Texte markiert die Vorlage rot
   gestrichelt; der rote Kasten oben links listet alle Hinweise. Einzeilig bleiben Rubrik,
   Untertitel, grosse Zahlen, Stichwort und Zahl der Entscheidungsfolie; die Erläuterung unter der
   Zahl rechts darf zwei Zeilen haben. Grosse Beträge runden und Einheiten klein setzen:
   `<small>CHF</small>12.3 <small>Mio.</small>`.
5. **Zahlenformat** Schweiz: 1'513'301, 11.1 %, CHF 1'240.00, EUR getrennt oder mit Kurs
   umgerechnet; Datum TT.MM.JJJJ.
6. **Genau ein Diagramm** pro Präsentation, das die wichtigste Aussage trägt. Werte an den
   Linienenden, Lücken statt 0 bei fehlendem oder zu kleinem Bestand. Reihennamen kurz (rund
   15 Zeichen), Band-Text kürzer als das Band. `einheit: "%"` für Quoten; für Anzahlen oder Beträge
   eine andere Einheit (etwa `"Verträge"`), dann zeigt das Diagramm ganze Zahlen.
7. **Höchstens drei Punkte** auf einer Folie, höchstens drei Beschlüsse auf der Entscheidungsfolie,
   je ein Satz.
8. **Sprechernotizen** zu jeder Folie: Kernsatz, was man zur Zahl sagt, Überleitung, Zeit.
9. Keine eckigen Klammern, kein Hinweis «Beispieldaten», keine leeren Bausteine im fertigen Satz.

## Farben

| Name | Wert | Wofür |
|---|---|---|
| Dunkelgrün | `#173d2c` | Titel, Hauptlinie, Nummern |
| Minze dunkel | `#23774d` | Text und Linien in Minze, hervorgehobene Reihe |
| Minze | `#52b986` | Akzente, Balken, Linien, nie für Text |
| Hellminze | `#d9f1e1` | Band der Titelfolie |
| Fläche hell | `#f3faf5` | hervorgehobene Kachel, Seitenkasten |
| Grau | `#8a9a91` | dritte Linie (etwa Gesamt), Text dazu in `#56665d` |
| Text / gedämpft / Linien | `#1c2a23` / `#56665d` / `#d5e3da` | Fliesstext / Untertitel, Quellen / Trennlinien, Gitter |

Keine weiteren Farben. Rot (`#c0392b`) nur für die Prüfhinweise der Vorlage, nie auf einer Folie.

## Raster

Rand links und rechts 64 px. Rubrik und Logo y = 40, Titel y = 104, Untertitel y = 150,
Linie y = 204, Inhaltsfläche y = 232 bis 616 (1152 × 384), Quelle y = 626, Fusszeile y = 668.
Logo, Fusszeile und Foliennummer setzt die Vorlage selbst; den Text der Fusszeile ändert man
einmal im Attribut `data-fuss`.

## Bausteine

| Baustein | Aufbau | Wofür |
|---|---|---|
| `titel` | Titel, Untertitel, Gremium und Datum, Name und Funktion, Datenstand | immer die erste Folie |
| `kennzahlen` | drei Kacheln, die dritte hervorgehoben; optional Aufteilungsbalken | drei Zahlen zu einer Aussage |
| `diagramm` | D3-Liniendiagramm links (Daten im Block «DIAGRAMM-DATEN»), Einordnung rechts | die wichtigste Aussage |
| `aussage` | bis drei Punkte links, Beleg rechts | Befund mit Belegen, etwa ein Fall |
| `entscheidung` | bis drei Zeilen: Nummer, Stichwort, ein Satz, Zahl rechts | immer die letzte Folie |

Neue Folie: die passende `<section class="folie">` kopieren und Texte ersetzen. Die Kommentare in
`vorlage.html` sagen, was wo steht.

## Zeigen und exportieren

- Im Browser öffnen, mit den Pfeiltasten blättern; Taste **S** öffnet die Sprecheransicht.
- **PDF:** in Chrome Drucken → Als PDF speichern, Ränder keine, Hintergrundgrafiken an; eine Folie
  je Seite. Mit Notizen: `praesentation.html?print-pdf&showNotes=separate-page` öffnen und so
  drucken. Ohne Klicken geht es mit Chrome im Hintergrund (Befehl in den Kommentaren der Vorlage).

*Fiktives Lehrbeispiel. Alle Daten synthetisch. Keine Verbindung zu realen Personen, Unternehmen oder Marken.*
