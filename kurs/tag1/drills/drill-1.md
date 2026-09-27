# Drill 1 · Bestand verstehen

Tag 1 «AI Augmentation», Montag 28. September 2026. Zeitbox 75 Minuten: 10 Input · 55 Übung · 10 Debrief.

## Deine Rolle

Du bist Dr. Lena Mbatha-Keller, Chief Data & AI Officer der Pfefferminzia-Gruppe. Die CEO will in der nächsten Sitzung des
Verwaltungsrats zeigen, dass die Gruppe ihre Daten ein Jahr nach der Fusion im Griff hat. Du
lieferst die Grundlage: Was haben wir im Bestand, wo verlieren wir Kunden, wo drückt der
Altbestand?

## Lernziel

Du lässt Claude einen unbekannten Datenbestand erkunden und daraus ein Werkzeug bauen, das du im
Browser bedienst. Du lenkst Auswertungen in Geschäftssprache («nur aktive Verträge», «getrennt nach
Herkunft»), verlangst zu jeder Zahl die Definition und rechnest mindestens eine Zahl nach. Du
entscheidest, welche drei Aussagen vor den Verwaltungsrat kommen.

## Mission

Baue dein Cockpit mit dem Reiter «Bestand»: Kennzahl-Kacheln, Übersicht der Tabellen, Filter nach
Sparte, Markt und Herkunft, die Stornoquote 2019 bis 2025 als Zeitreihe und eine Ampel für die
Garantiezinsen der Lebensversicherung. Schreibe dazu eine Management-Summary mit drei Kernaussagen.
Sie ist die Grundlage für deine Präsentation am Ende des Tages.

## Zeitbox

| Teil | Dauer | Was passiert |
|---|---|---|
| Input | 10 Min. | Vorführung: vom ersten Satz zum Cockpit im Browser; was eine Definition ist und warum sie zählt |
| Übung | 55 Min. | Etappen 1 bis 4, allein oder mit deinem Peer. Richtwert: 8 · 17 · 15 · 15 Minuten. Die Rückfrage-Runde und die Kanäle im Storno-Diagramm sind Kür (unten unter «Für Schnelle») |
| Debrief | 10 Min. | Welche Definition, welche Kernaussagen, welche Zahl habt ihr nachgerechnet? |

## Vorher kurz einstellen

Claude-App, Reiter **Code**, Modell **Sonnet 5**, Modus **Auto**, Ordner **«Pfefferminzia»** (nicht
der Arbeitsordner darüber). Am besten eine neue Sitzung beginnen. Aus Drill 0 brauchst du nichts.

## Dialog in vier Etappen

Schreib nicht alle Fragen auf einmal. Nach jeder Antwort prüfst oder entscheidest **du** etwas,
bevor es weitergeht.

| Etappe | Du schreibst Claude | Dann prüfst du |
|---|---|---|
| **1 · Überblick** | «Ich bin Chief Data & AI Officer und soll dem Verwaltungsrat zeigen, was wir ein Jahr nach der Fusion im Bestand haben. Verschaff dir einen Überblick über alle Datentabellen – bereinigte Tabellen, Rohdaten der Altsysteme, Migrationsbrücken – mit Zeilenzahl und je einem Satz, wozu sie dient. Schlag mir dann fünf Kennzahlen zum Bestand am Stichtag vor, je mit Wert und Definition. Noch keine Webseite.» | Prüfen: Stammen die Zahlen aus dem Übungsdatensatz (rund 1'000 Kunden, knapp 1'500 Verträge) und nicht aus dem Firmenprofil? Hat jede Kennzahl eine Definition? Dann **entscheiden** und Claude sagen, wie gezählt wird, zum Beispiel: «Fürs Cockpit gilt: Kunden sind Versicherungsnehmer mit aktivem Vertrag. Prämie heisst Jahresprämie brutto, also was der Kunde zahlt, in Franken umgerechnet mit unserem Konzernkurs 2025, den Euro-Betrag daneben.» |
| **2 · Cockpit anlegen** | «Lege mein Cockpit an mit dem Reiter ‹Bestand›: oben Kacheln mit den Kennzahlen, die wir eben festgelegt haben, jede mit ihrer Definition; darunter der aktive Bestand nach Sparte, Markt und Herkunft in Verträgen und Jahresprämie; unten eine sortierbare Übersicht der bereinigten Tabellen, Migrationsbrücken und Rohdaten mit Namen in Worten, Zeilen, Spalten und Zweck in einem Satz. Eine Filterleiste für Sparte, Markt und Herkunft soll auf alle Zahlen wirken. Öffne das Cockpit im Browser.» | Im Browser selbst klicken: Markt auf «Deutschland» stellen. Ändern sich die Kacheln und der Bestand nach Sparte, Markt und Herkunft? Eine Kachel mit Etappe 1 vergleichen. Siehst du Filter und alle Kacheln, ohne zu scrollen? Dann eine Verbesserung verlangen, die **du** willst, zum Beispiel: «Die Definitionen in den Kacheln sind zu lang: eine kurze Zeile, der Rest beim Überfahren.» Oder: «Die Tabellenübersicht soll nach Zeilenzahl sortiert starten.» |
| **3 · Wo verlieren wir Kunden?** | «Wo verlieren wir Kunden? Berechne die Stornoquote für jedes Jahr von 2019 bis 2025, getrennt nach Herkunft Pfefferminz und Minzia und nach Vertriebskanal, und nenne zuerst deine Definition. Prüfe dann in der Lebensversicherung, welche Tarifgenerationen 2025 einen Garantiezins über der Gesamtverzinsung haben und wie viele aktive Verträge und wie viel Jahresprämie daran hängen. Zeig mir beides als Tabelle, noch nichts ins Cockpit.» | Definition prüfen: Wer zählt als Storno, wer nicht? Was steht im Nenner? Hat Minzia vor 2021 Lücken statt Nullen? Nachhaken: «Ist das ein Minzia-Effekt oder ein Effekt des Direktkanals? Vergleiche nur die Direktkunden beider Herkünfte.» Erst wenn du den Zahlen traust, freigeben: «Übernimm beides in den Reiter ‹Bestand›: eine Kachel ‹Stornoquote 2025›; die Stornoquote als Liniendiagramm mit Prozentachse und je einer Linie für Gesamtbestand, Pfefferminz und Minzia, die Werte an der Gesamtlinie und am Ende jeder Linie, alle anderen beim Überfahren, Jahre mit weniger als 20 Verträgen als Lücke; die Tarifgenerationen als Ampel je Generation und Markt, mit Farbe und Wort, rot heisst Garantiezins über der Gesamtverzinsung, die Regel für Gelb sichtbar darüber. Die Filter sollen auch hier wirken.» Danach «Deutschland» wählen: Ändern sich Kachel und Gesamtlinie, und behält jede Linie ihre Farbe? Kannst du jede Zahl lesen? Sonst: «Die Beschriftungen überdecken sich, räum das Diagramm auf.» Die Kanäle als eigene Linien sind Kür (unten). |
| **4 · Drei Kernaussagen** | «Schreib mir eine Management-Summary für den Verwaltungsrat mit genau drei Kernaussagen zum Bestand ein Jahr nach der Fusion. Jede Kernaussage als ganzer Satz, der sagt, worauf der Verwaltungsrat achten oder reagieren sollte (keine reine Grössenangabe), belegt mit einer Zahl samt Definition und Quelle in Worten. Hänge die Stornoquoten 2019 bis 2025 für den Gesamtbestand, Pfefferminz und Minzia als kleine Tabelle mit Zähler und Nenner an, damit ich später ein Diagramm daraus bauen kann. Leg sie in meinen Ergebnissen ab und zeig sie mir hier.» | Eine Zahl nachrechnen lassen: «Rechne mir die Stornoquote von Minzia 2025 vor: wer im Zähler, wer im Nenner, wer nicht mitzählt, je mit Anzahl.» Dann **entscheiden**: Welche Aussage würdest du vor dem Verwaltungsrat vertreten, welche nicht? Mindestens eine Kernaussage selbst umformulieren oder ersetzen lassen, zum Beispiel: «Ersetze die schwächste Aussage durch eine zur Frage, woran unsere Prämie hängt.» Danach prüfen lassen: «Belegt jede Zahl genau das, was ihr Satz behauptet, und zeigen die drei Aussagen drei verschiedene Dinge? Sag mir zuerst je Aussage, was hält und was nicht, dann korrigiere.» |

## Fertig, wenn

- dein Cockpit im Browser öffnet und der Reiter «Bestand» Kacheln, Filterleiste, Bestand nach
  Sparte, Markt und Herkunft, Tabellenübersicht, Storno-Zeitreihe und Garantiezins-Ampel zeigt,
- der Filter «Deutschland» Kacheln **und** Stornokurve verändert,
- du die Definition der Stornoquote in eigenen Worten erklären kannst,
- du eine Zahl selbst nachgerechnet oder dir hast vorrechnen lassen, mit Zähler und Nenner,
- die Management-Summary mit drei Kernaussagen in deinen Ergebnissen liegt und mindestens eine
  Aussage deine eigene Entscheidung trägt.

## Hinweise, nacheinander

Nimm den nächsten Hinweis erst, wenn du ihn brauchst.

1. **Das Cockpit öffnet nicht oder zeigt keine Diagramme?** Frag: «Öffne mein Cockpit im Browser.»
   Bleiben die Diagramme leer: «Zeichne die Diagramme ohne externe Bibliotheken, damit das Cockpit
   auch ohne Internet läuft.»
2. **Die Filter wirken nicht auf die Stornoquote, oder die Quote springt seltsam?** Frag: «Die
   Filter sollen die Stornoquote neu berechnen: verlorene Verträge und Bestand am Jahresanfang
   getrennt zusammenzählen und erst dann teilen, nicht Quoten mitteln.»
3. **Deine Zahlen weichen von denen deines Peers ab, oder ein Reiter ist kaputt?** Frag: «Zeig
   mir deine Definition und rechne mir 2025 vor.» Unterschiede kommen fast immer aus der Definition
   (Nenner, Abläufe, Widerrufe) oder aus der Währung. Ist der Reiter kaputt: «Baue den Reiter
   ‹Bestand› neu, lass alles andere unverändert.»

## Für Schnelle

**Kür zuerst: die Rückfrage-Runde.** Stell Claude zwei oder drei Fragen, die ein Verwaltungsrat zu
deiner Management-Summary stellen würde, zum Beispiel: «Sind die Quoten vergleichbar, wenn Minzia erst
seit 2021 Kunden hat und der Bestand klein ist?» Prüfe, ob jede Antwort mit einer Zahl aus unseren
Tabellen belegt ist. Die Antworten bleiben im Chat; die Summary änderst du nur, wenn eine Aussage
dadurch nicht mehr hält.

Danach, wenn noch Zeit bleibt, **eines** von diesen:

- **Kanäle im Diagramm:** «Mach das Storno-Diagramm umschaltbar zwischen Herkunft und Kanal, feste Farbe je Kanal, Werte wie bisher.» Dann auf «Kanal» umschalten: Kannst du jede Zahl lesen? Beachte: «Direkt» mischt Pfefferminz- und Minzia-Kunden.
- **Vertiefen:** «Warum verlieren wir 2025 mehr Kunden? Zerlege den Anstieg nach Sparte, Markt,
  Herkunft und Stornogrund und sag mir, welche Gruppe den grössten Beitrag leistet.» Oder: «Zeig
  mir in einem Diagramm, woher der heutige Bestand kommt: Herkunft, ursprüngliches System, Status.»
- **Vorausbauen (Drill 2):** «Stell mir die Chronologie des Beschwerdefalls Pieper zusammen, mit
  Datum, Ereignis und Quelle je Zeile. Noch kein Reiter und kein Schreiben.» Die Akte baust du in
  Drill 2.

## Drei Arbeitsweisen

| Weg | Wenn du … | So bittest du Claude |
|---|---|---|
| Geführt | lieber Schritt für Schritt vorgehst | «Erkläre mir jeden Schritt, bevor du ihn machst, und warte auf mein Okay.» |
| Bauend | die Etappen zügig schaffst | Eigene Kacheln, Diagramme und Fragen verlangen; jede Zahl mit Definition und Quelle. |
| Vorausbauend | vor der Zeit fertig bist | Die Vorausbau-Aufgabe oben; das Ergebnis ist ein Vorsprung, kein Muss. |

Alle Personen, Firmen und Zahlen in Pfefferminzia sind erfunden. Verwende keine echten Kundendaten.
