# Einstieg für Teilnehmende

Willkommen bei Pfefferminzia, einem frei erfundenen Versicherer, an dem du Arbeiten mit KI-Unterstützung übst. Alles hier ist synthetisch: Personen, Firmen, Verträge, Schäden, Zahlen.

## In der Claude-App (so arbeiten wir im Kurs)

1. **Claude-App öffnen:** Claude Desktop, Reiter «Code», Modell Sonnet 5, Modus Auto.
2. **Arbeitsstand holen:** einen leeren Ordner wählen und Claude bitten: «Lade den Arbeitsstand von github.com/falkue/Pfefferminzia, Zweig teilnehmer, in diesen Ordner.» Ein GitHub-Konto brauchst du nicht: Du lädst nur herunter und arbeitest danach lokal auf deinem Rechner; nichts wird hochgeladen. Ohne Claude geht es auch im Browser: auf GitHub den Zweig `teilnehmer` wählen, «Code» → «Download ZIP», entpacken.
3. **Ordner öffnen:** den Ordner `Pfefferminzia` in der App als Projekt wählen. Claude liest die Datei `CLAUDE.md` und kennt damit den Datensatz.
4. **Erste Frage stellen**, zum Beispiel: «Erkläre mir, was in diesem Datensatz steckt, und zeige mir die fünf grössten Tabellen.»

Deine Ergebnisse legt Claude im Ordner `meine-ergebnisse/` ab (Cockpit, Berichte, Präsentation); Notizen zum Notizbuch kommen in `kurs/tag1/notizbuch/Vorbereitung/`.

## Im Terminal (optional)

```bash
git clone -b teilnehmer https://github.com/falkue/Pfefferminzia
cd Pfefferminzia
uv sync      # nur nötig, wenn du selbst Python-Skripte startest
claude
```

Der Zweig `teilnehmer` enthält den Datensatz ohne Lösungen.

## Die Geschichte in einem Absatz

Die Pfefferminz Versicherung, 1924 in Olten gegründet, hat am 1. Januar 2025 das Berliner KI-Start-up Minzia übernommen. Seither heisst die Gruppe Pfefferminzia. Sie verkauft Haftpflicht- und Lebensversicherungen in der Schweiz und in Deutschland. Der Bestand kommt aus zwei Welten: den Host-Systemen HAPO und VERA aus Olten und der Cloud-Plattform MINT aus Berlin. Beide wurden 2025 zusammengeführt, mit allen Nebenwirkungen, die eine Fusion in den Daten hinterlässt.

## Was du findest

| Ordner | Inhalt |
|---|---|
| `data/curated/S/csv/` | Die bereinigten Tabellen: Partner, Verträge, Anträge, Deckungen, Organisation |
| `data/raw/S/` | Die Rohdaten der drei Systeme, so wie sie ein Migrationsprojekt vorfindet |
| `data/migration/S/` | Zuordnung zwischen Rohdaten und bereinigten Tabellen, Migrationslog |
| `docs/datensatz/` | Data Dictionary und interaktive Datenschau |
| `docs/personas/` | Die Menschen hinter den Daten: Mitarbeitende und Kunden mit ihren Geschichten |
| `docs/unternehmen/` | Wer Pfefferminzia ist: Profil, Geschichte, Organisation, Systeme |
| `docs/regelwerke/` | Annahmerichtlinie Leben, Kompetenzordnung, Beschwerderichtlinie |
| `data/documents/S/personas/` | Die Fallakten der Kunden-Personas: Briefe, E-Mails, Notizen, Berichte |
| `data/documents/S/tarife/` | Tarifblätter je Tarifgeneration und Markt als Markdown und PDF |
| `kurs/tag1/` | Material für Tag 1: Notizbuch einer Teamleiterin (Obsidian), Antragseingang Risikoprüfung Leben, Auftrag und Vorlage für die Präsentation |
| `meine-ergebnisse/` | Deine eigenen Ergebnisse (legt Claude beim ersten Ergebnis an) |

Lösungen der Übungen liegen nicht in diesem Zweig.

## Ein paar Fragen zum Warmwerden

- Wie viele Kunden leben in der Schweiz, wie viele in Deutschland?
- Welche Verträge hat Simone Niederberger, und in welchen Systemen taucht sie auf?
- Warum haben so viele Verträge im Altsystem den Stornogrund ZZ?
- Welche Tarifgeneration der Lebensversicherung hat den höchsten Garantiezins, und wie viele Verträge gehören dazu?

## Hinweis

Pfefferminzia ist ein frei erfundenes Unternehmen für Lehrzwecke. Ähnlichkeiten mit real existierenden Personen, Unternehmen oder Marken, insbesondere mit gleichnamigen Medien oder Dienstleistern, sind unbeabsichtigt. Rechtliche Aussagen sind vereinfacht und ersetzen keine Rechtsberatung.
