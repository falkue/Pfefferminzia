# Drill 2 · Die Kundenakte

Tag 1 «AI Augmentation», Montag 28. September 2026. Zeitbox 60 Minuten: 10 Input · 40 Übung · 10 Debrief.

## Deine Rolle

Du bist Aylin Demirci, Teamleiterin Schaden Haftpflicht Deutschland der Pfefferminzia in Leipzig. Im März 2025
hat unser System den Haftpflichtschaden von Hans-Georg Pieper aus Dresden automatisch abgelehnt,
obwohl sein Hund seit Jahren versichert war. Herr Pieper hat sich zweimal beschwert, den
Versicherungsombudsmann eingeschaltet und die Aufsicht angerufen. Der Fall ist abgeschlossen, aber er
kommt wieder: Die Geschäftsleitung will wissen, was genau passiert ist und ob wir mit einer
KI-Assistenz schneller und besser geantwortet hätten.

## Lernziel

Du lässt Claude viele Quellen zu einem Fall zusammenführen: Tabellen, Briefe, Telefonnotizen,
E-Mails, interne Memos. Du bekommst jede Aussage mit Quelle und unterscheidest, was belegt ist und
was nur vermutet. Du lässt Schreiben im richtigen Ton entwerfen und prüfst sie gegen die Akte. Du
erlebst: Die KI liefert Chronologie und Entwurf in Minuten, die Verantwortung für jeden Satz bleibt
bei dir.

## Mission

Baue in deinem Cockpit den Reiter «Akte»: der Fall Pieper als klickbarer Zeitstrahl, bei dem jedes
Ereignis das Originaldokument zeigt, gefiltert nach Beteiligten. Spiele dann den entscheidenden Tag
nach: Entwirf den Brief an Herrn Pieper, wie er am 17. April 2025 hätte rausgehen sollen, und lass ihn
Satz für Satz gegen die Akte prüfen, mit Ampel. Die Stellungnahme an den Versicherungsombudsmann und
die Ampel im Cockpit sind Kür für Schnelle.

## Zeitbox

| Teil | Dauer | Was passiert |
|---|---|---|
| Input | 10 Min. | Der Fall in zwei Minuten; Vorführung: von einem Satz zur Chronologie; belegt, vermutet, nicht belegt |
| Übung | 40 Min. | Etappen 1 bis 4, allein oder mit deinem Peer. Richtwert: 8 · 14 · 9 · 9 Minuten. In Etappe 2 arbeitet Claude rund zehn Minuten am Stück; lies in der Zeit den Ablehnungsbrief und die Ursache noch einmal |
| Debrief | 10 Min. | Welche Behauptung war nicht belegt? Wer unterschreibt? Was heisst der Fall für die Automation? |

## Vorher kurz einstellen

Claude-App, Reiter **Code**, Modell **Sonnet 5**, Modus **Auto**, Ordner **«Pfefferminzia»**. Am
besten eine **neue Sitzung** beginnen. Dein Cockpit aus Drill 1 bleibt, der neue Reiter kommt dazu.
Hast du Drill 1 nicht abgeschlossen, sag Claude zuerst: «Lade den Stand nach Drill 1.» Claude legt dann
das Cockpit mit dem Reiter «Bestand» in deine Ergebnisse und zeigt dir, was jetzt da ist.

## Dialog in vier Etappen

Schreib nicht alle Fragen auf einmal. Nach jeder Antwort prüfst oder entscheidest **du** etwas,
bevor es weitergeht.

| Etappe | Du schreibst Claude | Dann prüfst du |
|---|---|---|
| **1 · Akte und Chronologie** | «Ich bin Teamleiterin Schaden Haftpflicht Deutschland. Es geht um die Beschwerde von Hans-Georg Pieper aus Dresden. Stell mir seine Akte zusammen: Stammdaten, Vertrag mit Deckungen, den Schaden mit allen Zahlungen und Reserven, alle Kontakte und alle Dokumente seiner Fallakte einschliesslich der E-Mails, dazu die Einträge zur Migration seines Vertrags. Lies jedes Dokument vollständig. Erstelle daraus eine Chronologie als Tabelle mit Datum, Ereignis, Beteiligten und Quelle mit Kennung, vom Vertragsbeginn bis heute, und sag mir, wie viele Dokumente du gelesen hast. Noch keine Webseite.» | Prüfen: Stehen die internen E-Mails drin? Hat jede Zeile eine Quelle? Ein Dokument selbst lesen: «Zeig mir den Ablehnungsbrief vom März im Wortlaut.» Dann nachhaken: «Was war die Ursache der Ablehnung? Trenne, was in den Daten und Dokumenten belegt ist, von dem, was du vermutest, und nenne die Regel unserer Kompetenzordnung, die verletzt wurde, in der Fassung, die an diesem Tag galt.» **Entscheiden** (für dich und den Debrief, du musst es Claude nicht schicken): War es ein Datenfehler, ein Regelfehler oder ein Prozessfehler, und was davon würdest du der Geschäftsleitung zuerst nennen? |
| **2 · Reiter «Akte»** | «Ergänze mein Cockpit um den Reiter ‹Akte› für den Fall Pieper. Oben eine Zeile mit Kunde, Vertrag, Versicherungsschein und Schaden, darunter wenige Kacheln zum Fall, jede mit ihrer Definition, zum Beispiel Schadentag, Tage bis zur Zahlung, bezahlter Betrag, Zahl der Dokumente. Darunter die Chronologie als klickbarer Zeitstrahl: Ein Klick auf ein Ereignis zeigt daneben das Dokument, den Brief, die E-Mail oder die Notiz im Volltext, bei jedem Dokument mit Art, Datum, Absender und Empfänger. Jede Gruppe von Beteiligten in eigener Farbe mit Legende und als Filter: alle, Kunde, Schadenabteilung, intern und IT, Ombudsmann, Aufsicht; ein Ereignis gehört zu jeder Gruppe, die es schreibt oder bekommt. Der Reiter ‹Bestand› bleibt unverändert. Sieh dir einen Screenshot an und öffne das Cockpit im Browser.» | Im Browser selbst klicken: ein Ereignis im März 2025, einen Brief des Kunden und eine interne E-Mail öffnen. Erscheint der ganze Text, stehen Absender und Empfänger da? Filter «Ombudsmann» wählen: Bleiben nur Anfrage und Stellungnahme? Filter «Schadenabteilung»: Sind der Ablehnungsbrief und der Brief vom 17. April dabei? Überdecken sich Beschriftungen im Frühjahr 2025? Einmal auf «Bestand» wechseln: Funktioniert er noch? Stimmt etwas nicht, sag Claude genau, was du siehst (siehe Hinweise 1 und 2); sonst gleich weiter zu Etappe 3. Eigene Verbesserungen sind Kür. |
| **3 · Der Brief vom 17. April** | «Spielen wir den 17. April 2025 nach. Entwirf den Brief an Herrn Pieper, wie er an diesem Tag hätte rausgehen sollen: Antwort auf seine beiden Beschwerden, jede mit ihrem Datum genannt, Regulierung, Entschuldigung auch dafür, dass wir die Frist nicht gehalten haben, die er uns in seiner ersten Beschwerde gesetzt hat, eine verständliche Erklärung, wer über seinen Schaden entschieden hat, ein Programm oder ein Mensch, und was sich ab sofort ändert. Beachte seinen Ton in den bisherigen Briefen und die Textbausteine unserer Beschwerderichtlinie; keine Diagnosen, keine internen Systemnamen, keine Schuldzuweisung an Kollegen, höchstens eine Seite. Verwende nur, was am 17. April 2025 bekannt war, und nenne nur als erledigt, was an diesem Tag schon erledigt war; alles andere heisst ‹veranlasst›. Rechne jede Frist, die du nennst, mit Anfang und Ende nach. Ausser den Textbausteinen übernimmst du keine Sätze aus dem Brief, der damals tatsächlich rausging. Leg den Brief in meinen Ergebnissen ab und schreib ihn mir hier vollständig in den Chat.» | Den Brief lesen, als wärst du Herr Pieper: Fühlst du dich ernst genommen? Beantwortet er deine Frage, wer den Ablehnungsbrief geschrieben hat? Steht irgendwo ein Systemname, ein Paragraf oder eine Diagnose? **Entscheiden:** Wer unterschreibt? Dann mindestens einen Satz selbst streichen oder ändern lassen, in derselben Eingabe mit der Unterschrift, zum Beispiel: «Streiche den Satz über … und sag stattdessen … Den Brief unterschreibe ich als Teamleiterin.» |
| **4 · Faktencheck** | «Geh meinen Brief, so wie er jetzt in meinen Ergebnissen liegt, Satz für Satz durch und prüfe jede Tatsachenbehauptung gegen die Akte, also gegen Tabellen und Dokumente, nicht gegen deine eigene Chronologie. Jede Aussage mit Datum, Betrag, Zahl oder etwas Erledigtem bekommt eine Zeile, die den Satz aus meinem Brief wörtlich zitiert. Stufe jede ein als belegt (grün), vermutet (gelb) oder nicht belegt (rot) und nenne die Quelle in Worten mit Kennung. Prüfe auch, ob etwas am 17. April 2025 schon bekannt oder schon erledigt war, ob etwas fehlt, das an diesem Tag bekannt war und hineingehört, und ob ein Satz fast wörtlich aus dem Brief stammt, der damals rausging. Ändere den Brief dabei nicht. Zeig mir die Prüfung hier als Tabelle mit Ampel, die Regel der Ampel darüber, und leg sie in meinen Ergebnissen ab.» | Stichprobe: Drei Aussagen aus Claudes Prüftabelle in deinem Brief suchen. Stehen sie dort wörtlich so? Fehlt ein Satz deines Briefs mit Datum, Betrag oder «erledigt»? Dann jede gelbe und rote Zeile ansehen und **entscheiden:** streichen, belegen oder umformulieren; mindestens eine änderst du. Ist alles grün, frag: «Welche Aussage ist am schwächsten belegt?» und entscheide, ob sie bleibt. Dann: «Korrigiere den Brief so: … und mach die Prüfung neu.» Zum Schluss: Würdest du den Brief so unterschreiben? |

## Fertig, wenn

- der Reiter «Akte» im Browser öffnet, der Zeitstrahl klickbar ist und ein Klick den Volltext eines
  Dokuments zeigt, auch einer E-Mail,
- der Filter nach Beteiligten wirkt und der Reiter «Bestand» weiter funktioniert,
- du die Ursache in zwei Sätzen erklären kannst und weisst, welche Regel verletzt wurde,
- der Brief an Herrn Pieper in deinen Ergebnissen liegt,
- die Faktencheck-Tabelle mit Ampel vorliegt (im Chat und in deinen Ergebnissen) und du mindestens
  eine Aussage aufgrund der Prüfung geändert oder gestrichen hast.

## Hinweise, nacheinander

Nimm den nächsten Hinweis erst, wenn du ihn brauchst.

1. **Ein Klick zeigt keinen Text, oder der Zeitstrahl bleibt leer?** Frag: «Nimm die vollständigen
   Texte aller Dokumente der Fallakte, auch der E-Mails, in die Daten des Reiters auf, damit das
   Cockpit ohne Server und ohne Internet läuft.» **Fehlen Absender oder Empfänger, oder stehen Zeichen
   wie # und \*\* im Text?** Frag: «Zeige bei jedem Dokument Art, Datum, Absender und Empfänger in
   Worten und den Text formatiert. Prüfe es an einem Brief, einer E-Mail und der Telefonnotiz.»
2. **Die Ereignisse im Frühjahr 2025 überdecken sich, oder der Zeitstrahl ist fast leer?** Frag:
   «Zeige die Jahre vor 2025 gestaucht und 2025 nach Monaten, oder stelle den Zeitstrahl senkrecht
   dar. Keine Beschriftung darf eine andere überdecken; sieh dir nach dem Bauen einen Screenshot an.»
3. **Der Brief klingt nach Anwalt, oder die Prüfung findet nur «belegt»?** Frag: «Schreib den Brief
   in kurzen Sätzen, so wie du es Herrn Pieper am Telefon sagen würdest, ohne Paragrafen.» Für die
   Prüfung: «Prüfe gegen die Tabellen und Originaldokumente, nicht gegen deine Chronologie. Welche
   Aussage stammt nur aus der Kundengeschichte oder war am Datum noch nicht bekannt?» **Steht in der
   Prüfung ein Satz, den du in deinem Brief nicht findest?** Frag: «Mach die Prüfung neu, und zwar an
   meinem Brief, wie er jetzt abgelegt ist; zitiere jeden Satz wörtlich daraus.» **Zeigt Claude den
   Brief nicht im Chat?** Frag: «Schreib mir den ganzen Brief hier in die Antwort.» Ist ein Reiter
   kaputt: «Baue den Reiter ‹Akte› neu, lass ‹Bestand› unverändert.»

## Für Schnelle (Kür)

Wähle, was dich interessiert; jede Kür dauert fünf bis zehn Minuten.

- **Ampel im Cockpit:** «Nimm die Prüfung als Tabelle mit Ampel in den Reiter ‹Akte› auf, die Regel
  der Ampel sichtbar darüber, und zeige darunter meinen Brief als formatierte Vorschau, so wie er auf
  Papier aussähe.»
- **Stellungnahme an den Ombudsmann:** «Entwirf die Stellungnahme an den Versicherungsombudsmann zu
  den vier Punkten seiner Anfrage, Stand 8. Mai 2025, einschliesslich unserer Versäumnisse bei der
  ersten Beschwerde, aller Massnahmen, die bis dahin beschlossen waren, und dessen, was wir tun, damit
  die weiteren Migrationen den Fehler nicht wiederholen; sachlich, mit Datum und Aktenzeichen, als
  Entwurf zur Freigabe durch die Compliance. Verwende nur, was am 8. Mai 2025 bekannt war; erledigt
  heisst nur, was an diesem Tag erledigt war, alles andere ‹veranlasst›. Rechne jede Frist nach.
  Ausser den Textbausteinen übernimmst du keine Sätze aus der Stellungnahme, die damals rausging. Leg
  sie in meinen Ergebnissen ab und schreib sie mir hier vollständig in den Chat.» Danach mit dem
  Prompt aus Etappe 4 prüfen lassen («meine Stellungnahme» statt «meinen Brief», Datum 8. Mai 2025).
- **Wendepunkte:** «Markiere die drei Wendepunkte des Falls im Zeitstrahl und zeige, wie viele Tage
  zwischen Ablehnung und Zahlung lagen.»
- **Vergleich mit dem Original:** «Leg meinen Brief neben den Brief, der am 17. April 2025
  tatsächlich rausging. Was ist bei mir besser, was fehlt?»
- **Vertiefen:** «War Herr Pieper ein Einzelfall? Wie viele Verträge in unserem Datensatz haben
  dieselbe Migrationswarnung, wie viele davon laufen noch, und hatte einer davon einen Schaden?» Oder
  ein zweiter Fall mit derselben Methode: «Stell mir die Akte der Transportlogistik Grimm zusammen.
  Was rechtfertigt die Ablehnung des letzten Schadens und die Kündigung, und was antworten wir dem
  Anwalt? Trenne Belegtes von Vermutetem.»
- **Vorausbauen (Drill 3):** «Stell mir den Antrag von Dr. Farid Nazari zusammen und erkläre mir,
  nach welcher Regel unserer Annahmerichtlinie er einen Zuschlag bekam. Entwirf dann zwei Sätze an
  ihn, die den Zuschlag erklären, ohne eine Diagnose zu nennen. Noch kein Reiter.» Die Entscheidungs-
  vorlagen baust du in Drill 3.

## Drei Arbeitsweisen

| Weg | Wenn du … | So bittest du Claude |
|---|---|---|
| Geführt | lieber Schritt für Schritt vorgehst | «Erkläre mir jeden Schritt, bevor du ihn machst, und warte auf mein Okay.» |
| Bauend | die Etappen zügig schaffst | Eigene Kacheln, Filter und Prüffragen verlangen; jede Aussage mit Quelle. |
| Vorausbauend | vor der Zeit fertig bist | Die Vorausbau-Aufgabe oben; das Ergebnis ist ein Vorsprung, kein Muss. |

Alle Personen, Firmen und Zahlen in Pfefferminzia sind erfunden. Verwende keine echten Kundendaten.
