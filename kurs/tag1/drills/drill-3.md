# Drill 3 · Underwriting mit Assistenz

Tag 1 «AI Augmentation», Montag 28. September 2026. Zeitbox 60 Minuten: 15 Input · 35 Übung · 10 Debrief.

## Deine Rolle

Du arbeitest in der Risikoprüfung Leben der Pfefferminzia. Auf deinem Tisch liegen drei Anträge auf
Risikolebensversicherung. Einer ist schon entschieden, kommt aber zurück: Dr. Farid Nazari, Arzt in
München, 1.2 Millionen Euro, hat einen Zuschlag bekommen und will wissen, ob «ein Algorithmus» über
ihn entschieden hat. Zwei sind neu aus dem Dezember: Katrin Brandes aus Hannover und Bruno Pedrazzini
aus Lugano. Du sollst alle drei nach unserer Annahmerichtlinie bewerten und dafür sorgen, dass die
nächste Vorlage nicht wieder eine Stunde dauert.

## Lernziel

Du gibst Claude ein Regelwerk als Grundlage und verlangst Ergebnisse in fester Struktur, jede
Bewertung mit Paragraf. Du erkennst, wo eine Regel eine Spanne lässt und wo ein Mensch entscheiden
muss. Wenn du schnell bist, lässt du als Kür ein Kundenschreiben entwerfen, das den Entscheid
erklärt, ohne Gesundheitsdaten zu verraten. Und du hältst deine Arbeitsweise als **eigenen Skill** fest: eine Anweisung an Claude, die
beim nächsten Antrag von selbst greift, auch in einer neuen Sitzung.

## Mission

Erstelle drei Entscheidungsvorlagen nach der Annahmerichtlinie und baue im Cockpit den Reiter
«Underwriting»: die Anträge als Liste, je Antrag der Regelpfad vom Prüfumfang bis zur Kompetenz, rot
markiert, wo ein Mensch entscheidet. Lege
zum Schluss deinen Skill «Entscheidungsvorlage Leben» an und teste ihn in einer neuen Sitzung mit
einem einzigen Satz an einem vierten Antrag. Als Kür beantwortest du Dr. Nazaris Fragen in einem
Brief ohne Diagnose.

## Zeitbox

| Teil | Dauer | Was passiert |
|---|---|---|
| Input | 15 Min. | Dr. Nazaris Frage «Hat ein Algorithmus entschieden?»; die Richtlinie in fünf Minuten; was ein Skill ist |
| Übung | 35 Min. | Etappen 1 bis 3, allein oder mit deinem Peer. Richtwert: 7 · 17 · 11 Minuten. In Etappe 2 arbeitet Claude rund zehn Minuten am Stück; lies in der Zeit die erste fertige Vorlage. Der Brief an Dr. Nazari ist Kür (unten unter «Für Schnelle») |
| Debrief | 10 Min. | Wer hat entschieden, Claude oder du? Was hat der Skill verändert? Was darf ein Makler lesen? |

## Vorher kurz einstellen

Claude-App, Reiter **Code**, Modell **Sonnet 5**, Modus **Auto**, Ordner **«Pfefferminzia»**. Am
besten eine **neue Sitzung** beginnen. Dein Cockpit aus Drill 1 und 2 bleibt, der neue Reiter kommt
dazu. Hast du Drill 2 nicht abgeschlossen, sag Claude zuerst: «Lade den Stand nach Drill 2.» Claude
legt dann das Cockpit mit den Reitern «Bestand» und «Akte» in deine Ergebnisse.

## Dialog in drei Etappen

Schreib nicht alle Fragen auf einmal. Nach jeder Antwort prüfst oder entscheidest **du** etwas,
bevor es weitergeht.

| Etappe | Du schreibst Claude | Dann prüfst du |
|---|---|---|
| **1 · Regeln und Anträge** | «Ich arbeite in der Risikoprüfung Leben. Lies unsere Annahmerichtlinie Leben und die Kompetenzordnung vollständig. Erkläre mir in höchstens zehn Sätzen, jeder mit Paragraf, wie ein Antrag auf Risikoleben geprüft wird: welcher Prüfumfang bei welcher Summe und welchem Alter, wie Gewicht, Nikotin, Beruf, Vorerkrankungen und Freizeitrisiken bewertet werden, wie aus den Zuschlägen eine Risikoklasse wird und wer entscheidet, ein System oder ein Mensch. Stell mir dann drei Anträge in einer Tabelle nebeneinander: den Antrag von Dr. Farid Nazari vom März 2025 mit seiner ganzen Fallakte und die neuen Anträge von Katrin Brandes und Bruno Pedrazzini aus dem Antragseingang; je Summe, Alter bei Antragseingang, Grösse und Gewicht, Nikotin, Vorerkrankungen, Freizeit und vorliegende Unterlagen. Noch keine Bewertung und keine Webseite.» | Prüfen: Kommen die Kombination der Zuschläge und die Entscheidungskompetenzen vor, mit Paragraf? Stimmt das Alter? Selbst nachlesen: «Zeig mir die Tabelle zum Bluthochdruck im Wortlaut.» **Entscheiden:** Welcher der drei Anträge ist für dich der heikelste, und worauf willst du bei ihm achten? |
| **2 · Vorlagen und Reiter** | «Erstelle für jeden der drei Anträge eine Entscheidungsvorlage nach unserer Annahmerichtlinie, jede als eigene Datei in meinen Ergebnissen, mit genau diesen Abschnitten: Antrag in Kürze; Prüfumfang und vorliegende Unterlagen; Bewertung Schritt für Schritt (Gewicht, Nikotin, Beruf, Vorerkrankungen, Freizeit), je mit Paragraf und Zuschlag in Prozent; Gesamtzuschlag und Risikoklasse; wer entscheidet, System oder Mensch, und auf welcher Stufe; Empfehlung; offene Rückfragen; was nicht in die Entscheidung einfliessen darf. Lässt die Richtlinie eine Spanne oder muss ein Mensch wählen, nenne die Möglichkeiten, schlage einen Wert vor, begründe ihn und markiere die Wahl als offen, bis ich entscheide. Entscheide bei Dr. Nazari mit dem Stand vom 28. Mai 2025 und vergleiche erst am Schluss mit dem damaligen Entscheid. Ergänze danach mein Cockpit um den Reiter ‹Underwriting›: links die Anträge mit Summe, Risikoklasse und Empfehlung (die Liste wächst mit jedem neuen Antrag); ein Klick zeigt rechts den Regelpfad als Schrittfolge vom Prüfumfang bis zur Kompetenz, jeder Schritt mit Angabe, Paragraf und Ergebnis, der Schritt, an dem ein Mensch entscheiden muss, rot markiert mit ‹Hier entscheidet ein Mensch›, darunter die ganze Vorlage. Die anderen Reiter bleiben unverändert. Öffne das Cockpit zum Schluss im Browser.» | Claude braucht dafür rund zehn Minuten. Lies in der Zeit die erste Vorlage, sobald sie in deinen Ergebnissen liegt. Einen Zuschlag selbst nachrechnen: Passen Gesamtzuschlag und Risikoklasse zur Tabelle der Richtlinie? Im Browser alle drei Anträge anklicken: Ist bei jedem der rote Punkt da? Nachhaken, wo es hakt, etwa: «Warum zählt der Rauchertarif bei Frau Brandes nicht zum Gesamtzuschlag?» oder «Spielen Staatsangehörigkeit oder Wohnort von Herrn Pedrazzini eine Rolle?» **Entscheiden** (eine der beiden Fragen genügt, die andere ist Kür): Gehst du bei Dr. Nazari mit dem Wert in der Spanne mit? Oder: Brauchst du für Herrn Pedrazzini noch den Vertrauensarzt, oder reicht, was vorliegt? Sag es Claude: «Übernimm meine Entscheidung … in Vorlage und Reiter, mit Vermerk ‹entschieden durch mich›. Lösche jeden Satz, der ihr jetzt widerspricht oder sie noch offen nennt, ganz (nicht durchstreichen), und zeig mir die Stelle.» |
| **3 · Dein Skill** | «Halte fest, wie bei uns eine gute Entscheidungsvorlage Leben entsteht, als Skill ‹Entscheidungsvorlage Leben› in diesem Projekt, den du künftig von selbst benutzt, sobald jemand eine Entscheidungsvorlage oder ein Kundenschreiben zu einem Antrag auf Lebensversicherung verlangt. Hinein gehören: welche Quellen du liest; die Prüfschritte in fester Reihenfolge mit Paragrafen; wie Zuschläge nach der Richtlinie zusammengezählt werden, mit allen Ausnahmen, und was nicht mitzählt; wer entscheiden darf; was nie in eine Entscheidung einfliessen darf; was nie in ein Kundenschreiben gehört; die Gliederung der Vorlage und wo sie abgelegt wird; dass jeder neue Antrag im Reiter ‹Underwriting› dazukommt. Nimm auf, was ich heute entschieden und korrigiert habe, aber als allgemeine Regel für jeden künftigen Antrag, ohne Namen, Werte oder Ergebnisse unserer drei Anträge. Erkläre mir den Skill danach in einfachen Worten.» | Den Skill (Claudes Arbeitsanleitung) überfliegen, vor allem das Zusammenzählen und wer entscheidet: Fehlt eine Regel, die dir wichtig ist? Eine selbst ergänzen lassen, zum Beispiel: «Jede Vorlage endet mit der Zeile ‹Entscheid durch: …, Datum: …›. Name und Datum stehen dort nur, wenn ein Mensch im Gespräch selbst entschieden hat, sonst steht ‹offen›.» Dann eine **neue Sitzung** beginnen und nur einen Satz schreiben: «Entscheidungsvorlage für den Antrag von Lea Hartwig.» Prüfen: Zeigt Claude an, dass es den Skill benutzt? Hat die Vorlage dieselbe Gliederung? Steht Frau Hartwig im Reiter, und wo in ihrem Regelpfad entscheidet ein Mensch? **Entscheiden:** Dürfte ein Antrag wie ihrer künftig automatisch angenommen werden? |

## Fertig, wenn

- drei Entscheidungsvorlagen in deinen Ergebnissen liegen, jede mit Paragrafen, Gesamtzuschlag,
  Risikoklasse, Kompetenz und Empfehlung, und du bei mindestens einer selbst entschieden hast und
  das mit «entschieden durch mich» in Vorlage und Reiter steht,
- der Reiter «Underwriting» im Browser öffnet, ein Klick auf einen der drei Anträge den Regelpfad mit
  dem roten Punkt «Hier entscheidet ein Mensch» und die Vorlage zeigt, und «Bestand» und «Akte» weiter
  funktionieren,
- dein Skill «Entscheidungsvorlage Leben» angelegt ist und in einer neuen Sitzung aus einem Satz die
  Vorlage für Lea Hartwig entstanden ist.

## Hinweise, nacheinander

Nimm den nächsten Hinweis erst, wenn du ihn brauchst.

1. **Claude findet die neuen Anträge nicht oder fragt nach einem Ordner?** Sag: «Die neuen Anträge
   liegen im Kursmaterial von Tag 1 im Antragseingang.» **Fehlen in der Zusammenfassung Kombination
   oder Kompetenz?** Frag: «Lies die Richtlinie noch einmal ganz, auch die Paragrafen zur Kombination
   der Zuschläge und zu den Entscheidungskompetenzen, und zeig mir, wo sie bei unseren drei Anträgen
   greifen.»
2. **Gesamtzuschlag oder Risikoklasse wirken falsch?** Frag: «Rechne den Gesamtzuschlag noch einmal
   vor: Nur Prozentzuschläge zählen, der Rauchertarif ist ein eigener Tarif, Übergewicht wird nur
   einmal bewertet. Zeig mir die Zeile der Tabelle, die zur Risikoklasse passt.» **Ein Klick im Reiter
   zeigt nichts?** Frag: «Nimm Regelpfad und Volltext der Vorlagen in die Daten des Reiters auf, damit
   das Cockpit ohne Server läuft.»
3. **Der Skill greift in der neuen Sitzung nicht?** Schreib: «Nutze den Skill Entscheidungsvorlage
   Leben für den Antrag von Lea Hartwig.» Ist ein Reiter kaputt: «Baue den Reiter ‹Underwriting› neu,
   lass ‹Bestand› und ‹Akte› unverändert.»

## Für Schnelle

**Kür zuerst: Brief an Dr. Nazari.** Mach sie, wenn dein Skill steht und noch Zeit bleibt.

| Kür | Du schreibst Claude | Dann prüfst du |
|---|---|---|
| **Kür · Brief an Dr. Nazari** | «Dr. Nazari hat am 2. Juni 2025 per E-Mail vier Fragen zu seinem Zuschlag gestellt. Entwirf die Antwort als Brief an ihn, wie sie am 16. Juni 2025 hätte rausgehen sollen: seine vier Fragen der Reihe nach beantwortet, nummeriert wie in seiner E-Mail; Entscheid und Zuschlag; wie entschieden wurde und von wem, System oder Mensch; welche Unterlagen verarbeitet wurden; wann und wie er eine Nachprüfung verlangen kann. Halte die Kommunikationsregel unserer Annahmerichtlinie ein: keine Diagnose, kein Medikament, keine Messwerte, auch nicht umschrieben; medizinische Einzelheiten nur auf seinen Wunsch und auf dem Weg, den die Richtlinie vorsieht. Präzise und sachlich, er ist selbst Arzt; höchstens anderthalb Seiten. Formuliere eigene Sätze und schreib die Schreiben aus seiner Akte nicht ab. Prüfe den Entwurf dann Satz für Satz: Verrät ein Satz etwas über seine Gesundheit, auch indirekt? Zeig die Prüfung als Tabelle mit Satz, Gesundheitsbezug und Ampel, nimm Brief und Prüfung als Vorschau in den Reiter ‹Underwriting› auf und zeig mir den Brief hier.» | Den Brief lesen, als wärst du sein Makler: Weisst du danach, woran Dr. Nazari leidet? Ist seine Frage «Hat ein Algorithmus entschieden?» klar beantwortet? Mindestens einen Satz ändern oder streichen lassen: «Ersetze den Satz über … durch …» **Entscheiden:** Wer unterschreibt, und geht der Brief direkt an ihn oder über den Makler? |

Verrät der Brief etwas über die Gesundheit? Frag: «Ersetze jede Aussage über seine Gesundheit durch den
Verweis auf seine Angaben im Antrag und die ärztlichen Unterlagen, ohne sie zu nennen.» Fertig ist die
Kür, wenn der Brief seine vier Fragen beantwortet, keine Diagnose, kein Medikament und keinen Messwert
enthält und die Prüfung mit Ampel im Reiter steht.

Danach, wenn noch Zeit bleibt, **eines** von beiden. Oder frag nach, was in Etappe 1 keinen Platz hatte:
«Was darf nach unseren Regeln ein System allein entscheiden, und was nie? Prüf deine Antwort an unseren
drei Anträgen, auch am Prüfumfang nach Alter.»

- **Vertiefen:** «Entwirf für Herrn Pedrazzini das Schreiben zu unserem Entscheid: ohne Diagnose,
  mit dem Weg zur ärztlichen Auskunft über seinen Hausarzt und seinem Recht, die Entscheidung von
  einem Menschen überprüfen zu lassen. Prüfe es danach selbst auf Gesundheitsangaben.» Oder frag
  deinen Skill in einer neuen Sitzung nach einem Antrag, der ihn fordert: «Entscheidungsvorlage für
  den Antrag von Bruno Pedrazzini, diesmal mit halber Summe.» Ändert sich das Ergebnis?
- **Vorausbauen (Drill 4):** Lade Obsidian von **obsidian.md** herunter und installiere es. Frag dann:
  «Im Kursmaterial liegt das Arbeitsnotizbuch von Aylin Demirci. Sag mir den vollständigen Ordnerpfad,
  damit ich es in Obsidian öffnen kann, und wie viele Notizen es hat. Noch keine neue Notiz.»

## Drei Arbeitsweisen

| Weg | Wenn du … | So bittest du Claude |
|---|---|---|
| Geführt | lieber Schritt für Schritt vorgehst | «Erkläre mir jeden Prüfschritt, bevor du ihn machst, und warte auf mein Okay.» |
| Bauend | die Etappen zügig schaffst | Eigene Prüfschritte, Kacheln oder Regeln für den Skill verlangen; jede Bewertung mit Paragraf. |
| Vorausbauend | vor der Zeit fertig bist | Die Vorausbau-Aufgabe oben; das Ergebnis ist ein Vorsprung, kein Muss. |

Alle Personen, Firmen und Zahlen in Pfefferminzia sind erfunden. Gesundheitsangaben sind auch im
Planspiel besondere Personendaten: Verwende keine echten Gesundheits- oder Kundendaten.
