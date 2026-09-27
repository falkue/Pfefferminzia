# Einstieg für Teilnehmende

Willkommen bei Pfefferminzia, einem frei erfundenen Versicherer, an dem du Arbeiten mit KI-Unterstützung übst. Alles hier ist synthetisch: Personen, Firmen, Verträge, Schäden, Zahlen.

## In der Claude Desktop-App (so arbeiten wir im Kurs)

Du arbeitest im Kurs nur in der Claude Desktop-App, im Reiter «Code». Ein Terminal brauchst du nicht, ein GitHub-Konto auch nicht.

1. **App einstellen:** Claude Desktop öffnen, Reiter «Code», Modell Sonnet 5, Modus Auto.
2. **Arbeitsstand holen:** einen leeren Ordner wählen und Claude bitten: «Lade den Arbeitsstand von github.com/falkue/Pfefferminzia, Zweig teilnehmer, in diesen Ordner.» Du lädst nur herunter und arbeitest danach lokal auf deinem Rechner; nichts wird hochgeladen. Ohne Claude geht es auch im Browser: auf GitHub den Zweig `teilnehmer` wählen, «Code» → «Download ZIP», entpacken.
3. **Ordner als Projekt öffnen:** im Reiter «Code» den Ordner mit dem Arbeitsstand wählen (meist `Pfefferminzia`). Claude liest die Datei `CLAUDE.md` und kennt damit den Datensatz. Braucht Claude für eine Auswertung Python, richtet es das im Projekt selbst ein; du musst dafür nichts installieren.
4. **Erste Frage stellen**, zum Beispiel: «Erkläre mir, was in diesem Datensatz steckt, und zeige mir die fünf grössten Tabellen.»

## Wo was liegt

- **`kurs/tag1/`** ist das Material für Tag 1: `notizbuch/` (Notizbuch einer Teamleiterin als Obsidian-Vault), `antragseingang/` (drei Anträge für die Risikoprüfung Leben), `praesentation/` (Auftrag, Vorlage und Regeln für die Management-Präsentation).
- **`meine-ergebnisse/`** nimmt deine Ergebnisse auf; Claude legt den Ordner beim ersten Ergebnis an. Dort entstehen dein Cockpit `cockpit.html` (eine Seite mit Reitern, die von Übung zu Übung wächst), Berichte und Schreiben sowie der Foliensatz `praesentation.html`. Notizen zum Notizbuch legt Claude unter `kurs/tag1/notizbuch/Vorbereitung/` ab.
- **Lösungen und Dozentenmaterial liegen nicht in diesem Zweig.** Du findest hier den Datensatz, die Unterlagen des Unternehmens und das Kursmaterial, aber keine Musterlösungen.

## Die Geschichte in einem Absatz

Die Pfefferminz Versicherung, 1924 in Olten gegründet, hat am 1. Januar 2025 das Berliner KI-Start-up Minzia übernommen. Seither heisst die Gruppe Pfefferminzia. Sie verkauft Haftpflicht- und Lebensversicherungen in der Schweiz und in Deutschland. Der Bestand kommt aus zwei Welten: den Host-Systemen HAPO und VERA aus Olten und der Cloud-Plattform MINT aus Berlin. Beide wurden 2025 zusammengeführt, mit allen Nebenwirkungen, die eine Fusion in den Daten hinterlässt.

## Was du findest

| Ordner | Inhalt |
|---|---|
| `data/curated/S/csv/` | Die bereinigten Tabellen: Partner, Verträge, Anträge, Deckungen, Organisation |
| `data/raw/S/` | Die Rohdaten der drei Systeme, so wie sie ein Migrationsprojekt vorfindet |
| `data/migration/S/` | Zuordnung zwischen Rohdaten und bereinigten Tabellen, Migrationslog |
| `docs/datensatz/` | Data Dictionary: was in welcher Tabelle steht |
| `docs/personas/` | Die Menschen hinter den Daten: Mitarbeitende und Kunden mit ihren Geschichten |
| `docs/unternehmen/` | Wer Pfefferminzia ist: Profil, Geschichte, Organisation, Systeme |
| `docs/regelwerke/` | Annahmerichtlinie Leben, Kompetenzordnung, Beschwerderichtlinie |
| `data/documents/S/personas/` | Die Fallakten der Kunden-Personas: Briefe, E-Mails, Notizen, Berichte |
| `data/documents/S/tarife/` | Tarifblätter je Tarifgeneration und Markt als Markdown und PDF |
| `kurs/tag1/` | Material für Tag 1: Notizbuch einer Teamleiterin (Obsidian), Antragseingang Risikoprüfung Leben, Auftrag und Vorlage für die Präsentation |
| `meine-ergebnisse/` | Deine eigenen Ergebnisse: Cockpit, Berichte, Schreiben, Präsentation (legt Claude beim ersten Ergebnis an) |

## Ein paar Fragen zum Warmwerden

- Wie viele Kunden leben in der Schweiz, wie viele in Deutschland?
- Welche Verträge hat Simone Niederberger, und in welchen Systemen taucht sie auf?
- Warum haben so viele Verträge im Altsystem den Stornogrund ZZ?
- Welche Tarifgeneration der Lebensversicherung hat den höchsten Garantiezins, und wie viele Verträge gehören dazu?

## Für Fortgeschrittene: im Terminal

Im Kurs nicht nötig. Wer lieber im Terminal arbeitet:

```bash
git clone -b teilnehmer https://github.com/falkue/Pfefferminzia
cd Pfefferminzia
claude
```

## Hinweis

Pfefferminzia ist ein frei erfundenes Unternehmen für Lehrzwecke. Ähnlichkeiten mit real existierenden Personen, Unternehmen oder Marken, insbesondere mit gleichnamigen Medien oder Dienstleistern, sind unbeabsichtigt. Rechtliche Aussagen sind vereinfacht und ersetzen keine Rechtsberatung.
