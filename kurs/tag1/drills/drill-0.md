# Drill 0 · Arbeitsumgebung

Tag 1 «AI Augmentation», Montag 28. September 2026. Zeitbox 30 Minuten: 10 Einführung · 15 Übung · 5 Auswertung.

## Deine Rolle

Du bist Tiago Almeida, Trainee Datenqualität im Data & AI Office der Pfefferminzia, einem
Versicherer, der vor einem Jahr aus einer Fusion entstanden ist. Heute ist dein erster Arbeitstag.
Du richtest deinen Arbeitsplatz ein und lernst den Datenbestand kennen. Deine oberste Chefin,
Dr. Lena Mbatha-Keller (Chief Data & AI Officer), bereitet für den Verwaltungsrat eine Übersicht
zum Bestand vor und fragt dich als Erstes: Wie viele Kunden haben wir in der Schweiz und in
Deutschland, und wie ist gezählt? Deine Antwort legst du ihr als kurze Notiz ab. Ab Drill 1 seid
ihr Lena selbst.

## Lernziel

Du kennst die drei Arbeitsweisen der Claude-App (Chat, Cowork, Code) und weisst, wann du welche
nimmst. Du hast den Kursdatensatz auf deinem Rechner und hast Claude die ersten Fragen dazu
gestellt. Du hast gesehen, dass Claude Dateien liest, selbst nachrechnet und dich vorher um
Erlaubnis fragt, und du hast einmal nachgehakt, wie Claude auf eine Zahl gekommen ist.

## Mission

Hol dir im Code-Bereich der Claude-App den Kursdatensatz Pfefferminzia. Lass dir erklären, was
darin steckt. Stell zwei erste Fragen an die Daten und prüfe bei einer Antwort, wie Claude
gezählt hat. Deine Empfehlung zur Kundenzahl legst du Lena als Notiz ab.

## Zeitbox

| Teil | Dauer | Was passiert |
|---|---|---|
| Einführung | 10 Min. | Rundgang durch Chat, Cowork und Code; Vorführung des ersten Gesprächs, dabei stellst du die App gleich mit ein und holst den Datensatz (Etappe 1); Etappe 2 siehst du in der Vorführung |
| Übung | 15 Min. | Neue Sitzung im Ordner «Pfefferminzia», dann Etappen 3 und 4 (Etappe 1, falls sie in der Einführung nicht geklappt hat), allein oder mit deinem Peer; Etappe 2 selbst stellen, die Ergänzung der Notiz und eigene Zusatzfragen sind Zusatzaufgaben |
| Auswertung | 5 Min. | Was hat Claude getan, woher wusste es das, wo musstest du nachhaken? |

## Vorher kurz einstellen

Das machst du während der Vorführung in der Einführung mit, damit die 15 Minuten Übung direkt mit der neuen
Sitzung und Etappe 3 beginnen. In der Claude-App den Reiter **Code** öffnen. Modell **Sonnet 5**,
Modus **Auto**. Als Ordner einen einfachen Arbeitsordner wählen, zum Beispiel «ai-studio» in deinem
Benutzerordner, ohne Umlaute im Namen und nicht in einem Cloud-Ordner (OneDrive, iCloud). Ein
GitHub-Konto brauchst du nicht. Wenn die Vorführung Etappe 1 zeigt, schickst du denselben Satz in
deiner App ab und erlaubst den Befehl. Klappt es nicht auf Anhieb, machst du in der Übung mit
Etappe 1 und Hinweis 2 weiter. Etappe 2 stellt die Kursleitung danach am Beamer; du liest mit und
prüfst mit.

Öffne dieses Blatt digital (den Link bekommst du von der Kursleitung), kopiere die Eingaben aus der
Tabelle unten und füge sie ein, statt sie abzutippen. Das spart in der Übung zwei bis drei Minuten;
mit Abtippen wird die Übung in 15 Minuten knapp.

## Dialog in vier Etappen

Schreib nicht alle Fragen auf einmal. Nach jeder Antwort prüfst oder entscheidest **du** etwas,
bevor es weitergeht.

| Etappe | Du schreibst Claude | Dann prüfst du |
|---|---|---|
| **1 · Datensatz holen** | «Hol mir den Kursdatensatz Pfefferminzia: nur den Zweig ‹teilnehmer› (einzelner Zweig, --single-branch) aus dem öffentlichen Repository github.com/falkue/Pfefferminzia. Ich habe kein GitHub-Konto und brauche keins. Leg ihn in diesem Ordner ab und sag mir danach in zwei Sätzen, was du gemacht hast und wie der neue Ordner heisst.» | Claude fragt, ob es den Befehl ausführen darf: die Frage lesen und erlauben. Danach eine **neue Sitzung** starten und als Ordner den neuen Ordner «Pfefferminzia» wählen. Erst dort geht es weiter. Hast du den Datensatz schon in der Einführung geholt, beginnst du hier mit der neuen Sitzung. |
| **2 · Orientieren** (Vorführung in der Einführung; selbst stellen ist eine Zusatzaufgabe) | «Lies das Einstiegsblatt für Teilnehmende. Erkläre mir dann in fünf Sätzen und ohne Fachjargon: Wer ist Pfefferminzia – echt oder erfunden – und was verkauft sie wo, woher kommen die Daten, was ist der Stichtag, wie gross ist unser Übungsdatensatz, und was macht ihn für unsere Übungen besonders?» | In der Vorführung mitprüfen: Nennt Claude die Grösse des **Übungsausschnitts** (1'000 Personen und Firmen, knapp 1'500 Verträge) oder die Zahlen des ganzen Unternehmens (über eine Million Verträge)? In der Übung beginnst du nach der neuen Sitzung direkt mit Etappe 3. |
| **3 · Erste Zahl** | «Wie viele unserer Kunden leben in der Schweiz, wie viele in Deutschland? Sag mir dazu, wen du als Kunden gezählt hast und aus welcher Quelle die Zahl stammt.» | Zuschauen, was Claude tut: Es liest, rechnet und fragt um Erlaubnis. Meist nennt Claude schon mehrere Zählweisen mit ihrer Definition. Nur wenn Claude bloss eine Zahl nennt, zuerst nachhaken: «Und wenn nur zählt, wer heute einen laufenden Vertrag hat?» **Dann entscheidest du:** Welche Zählweise empfiehlst du Lena Mbatha-Keller für ihre Unterlage an den Verwaltungsrat? Schreib Claude deine Empfehlung mit einem Satz Begründung und lass sie ablegen, zum Beispiel: «Ich empfehle Lena …, weil … Leg die Zahlen mit allen Zählweisen und meiner Empfehlung als Notiz für Lena in meinen Ergebnissen ab.» Entscheiden wird Lena. In Drill 1 seid ihr sie und findet deine Notiz vor. |
| **4 · Eine Kundin, drei Systeme** | «Welche Verträge hat Simone Niederberger, und in welchen Systemen taucht sie auf? Zeig mir je Vertrag Produkt, Beginn, Status und Jahresprämie.» | Nachhaken: «Woher weisst du, dass das in allen Systemen dieselbe Person ist? Zeig mir, wie sie in jedem System eingetragen ist: Name, Geburtsdatum, Adresse.» Selbst entscheiden, ob dich die Antwort überzeugt, und was dir auffällt. Das sagst du deinem Peer oder bringst es in die Auswertung mit; eine weitere Frage an Claude dazu ist eine Zusatzaufgabe (siehe «Für Schnelle»). |

## Fertig, wenn

- der Ordner «Pfefferminzia» auf deinem Rechner liegt und deine Sitzung in diesem Ordner läuft,
- du weisst, wer Pfefferminzia ist, woher die Daten kommen und welcher Stichtag gilt (Etappe 2 in der Vorführung oder selbst gestellt),
- du eine Zahl zu Kunden in der Schweiz und in Deutschland hast, **weisst, wie sie gezählt ist**, und
  deine Notiz für Lena in deinen Ergebnissen liegt,
- du die Verträge von Simone Niederberger gesehen hast und weisst, in welchen Systemen sie steht.

## Hinweise, nacheinander

Nimm den nächsten Hinweis erst, wenn du ihn brauchst.

1. **Claude kennt den Datensatz nicht oder fragt nach Dateien?** Schau oben in der App, welcher
   Ordner gewählt ist. Es muss der Ordner «Pfefferminzia» sein, nicht dein Arbeitsordner darüber.
   Neue Sitzung, richtigen Ordner wählen, Frage wiederholen.
2. **Das Holen des Datensatzes klappt nicht?** Frag Claude: «Was fehlt auf meinem Rechner, damit
   das Klonen klappt? Nur den nächsten Schritt.» Meist fehlt das Programm Git. Ausweg ohne Git:
   Auf der Seite github.com/falkue/Pfefferminzia den Zweig «teilnehmer» wählen, «Code» und
   «Download ZIP» klicken, entpacken und den entpackten Ordner in Claude wählen.
3. **Die Zahlen wirken seltsam oder widersprechen sich?** Frag: «Zeig mir, wie du gezählt hast:
   welche Tabelle, welcher Filter, welcher Stichtag.» Zahlen aus Firmenprofil und Geschichten
   gelten für das ganze Unternehmen; der Übungsdatensatz ist ein Ausschnitt mit 1'000 Personen und
   Firmen (Kunden, Mitversicherte, Begünstigte).

## Für Schnelle

Hast du Etappe 2 in der Vorführung verpasst, stell sie jetzt selbst. Sonst zuerst, wenn dir in
Etappe 4 etwas aufgefallen ist, **nachfassen**: «Mir fällt … auf. Wie oft kommt das im Datensatz
vor? Nur die Zahl und wie du gezählt hast.»

Dann, wenn du willst, **ergänzt du deine Notiz für Lena**: «Ergänze meine Notiz für Lena um
Simone Niederberger als Beispiel dafür, wie dieselbe Kundin in drei Systemen steht: je System
Name, Geburtsdatum und Adresse, so wie sie eingetragen sind.» Das ist dein eigentliches Fach als
Trainee Datenqualität. Danach wähle **eines** von beiden.

- **Vertiefen:** «Warum haben so viele Verträge in den Altsystemen den Stornogrund ZZ? Stell eine
  Vermutung auf und prüfe sie gegen die Migrationsunterlagen, bevor du antwortest.» Oder:
  «Welche Tarifgeneration der Lebensversicherung hat den höchsten Garantiezins, wie viele Verträge
  gehören dazu, und wie viele davon laufen noch?»
- **Vorausbauen (Drill 1):** «Lena Mbatha-Keller baut diese Woche ein Cockpit zum Bestand für den
  Verwaltungsrat. Welche fünf Kennzahlen sollte es zeigen? Gib mir dazu eine Liste der Tabellen
  mit Zeilenzahl und Zweck, noch keine Webseite.» Das Cockpit baust du in Drill 1.

## Drei Arbeitsweisen

| Weg | Wenn du … | So bittest du Claude |
|---|---|---|
| Geführt | zum ersten Mal mit Claude arbeitest | «Erkläre mir jeden Schritt, bevor du ihn machst, und warte auf mein Okay.» |
| Bauend | die Etappen zügig schaffst | Eigene Fragen an die Daten stellen und jede Zahl mit Definition und Quelle verlangen. |
| Vorausbauend | vor der Zeit fertig bist | Die Vorausbau-Aufgabe oben; das Ergebnis ist ein Vorsprung, kein Muss. |

Alle Personen, Firmen und Zahlen in Pfefferminzia sind erfunden. Verwende keine echten Kundendaten.
