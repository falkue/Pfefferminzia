# Entscheidungsprotokoll

Verbindliche Festlegungen für den Pfefferminzia-Datensatz. Neue Einträge werden unten angefügt. Bei Widersprüchen zu anderen Dokumenten gilt dieses Protokoll.

| Nr. | Datum | Entscheidung | Begründung |
|---|---|---|---|
| E01 | 2026-09-03 | Der Name **Pfefferminzia** bleibt, trotz Kollision mit einem realen Fachmedium. Jedes Artefakt trägt den Abgrenzungs-Disclaimer, Domains nur `pfefferminzia.example`, keine Bezugnahme auf das reale Medium. | Name ist im Kurs eingeführt (Entscheidung des Kursleiters) |
| E02 | 2026-09-03 | Kanonische Zeitachse: Pfefferminz gegründet 1924 in Olten; Leben seit 1961; AG seit 1998; DE-Eintritt 2006; Minzia gegründet 2019 in Berlin; Beteiligung 2023; Signing Mai 2024; **Closing und neue Marke 1. Januar 2025**; Altsystem-Snapshot 31. Dezember 2024; **Datensatz-Stichtag 31. Dezember 2025**; Bewegungsdaten 2016–2025; Altverträge Leben ab 1985, Haftpflicht ab 2001. | Sauberes Geschäftsjahresende, zwölf Monate Integrationsrealität |
| E03 | 2026-09-03 | Größenstufen **S** (ca. 1'000 Kunden, alle Dokumente gerendert), **M** (ca. 50'000 Partner, 75'000 Verträge), **L** (×5). Stufe S ist echter Teilbaum von M. S wird zuerst vollständig gebaut. | Frühes komplettes Beispiel vor teurer Mengenerzeugung |
| E04 | 2026-09-03 | IT-Systeme: Pfefferminz **VERA** (Leben-Bestand, Host), **HAPO** (Haftpflicht-Bestand), **SILAS** (Schaden/Leistung beide Sparten), **DOKU** (Archiv); Minzia **MINT** (Kernsystem) und **Herbarium** (Datenplattform). Migration in zwei Wellen 2025 (Haftpflicht Q2, Leben Q4). | Harmonisierung der Teilplanungen |
| E05 | 2026-09-03 | F1: Kapitalbildende Leben in DE nur als Altbestand („Pfefferminz Kapital"); DE-Neugeschäft nur Risiko und Rente. | Weniger Regulatorik, gleiche Didaktik |
| E06 | 2026-09-03 | F2: Keine Basisrente, kein Riester. | Kein didaktischer Mehrwert |
| E07 | 2026-09-03 | F3: In CH-Kundendokumenten Haftpflicht 15 % FR, 5 % IT; Regelwerke nur Deutsch. | Realismus ohne Übersetzungsaufwand für Regelwerke |
| E08 | 2026-09-03 | F4: Schadenfotos als Platzhalterbilder mit EXIF-Metadaten, keine generierten Fotos. | EXIF trägt die didaktischen Widersprüche |
| E09 | 2026-09-03 | F5: Gesundheitsfragen als Ja/Nein plus Freitext; Diagnosen auf ICD-10-Gruppenebene aus Diagnose-Bibliothek, getrennt von der Identität erzeugt. | Datenschutz-Sensibilität, Extraktions-Use-Case |
| E10 | 2026-09-03 | F6: AHV-Nummer und Steuer-ID enthalten, prüfziffernvalide aber fiktiv. | PII-Detektor-Use-Case |
| E11 | 2026-09-03 | F7: Rückversicherung nur als Referenztabelle. | Kein Bewegungsdatenaufwand |
| E12 | 2026-09-03 | F8: Keine Fondskurse in Version 1. | Scope |
| E13 | 2026-09-03 | F9: Gemeinsamer Partnerstamm in `curated`, getrennte Stämme in `raw` (VERA, HAPO, MINT). | Dubletten-Übung |
| E14 | 2026-09-03 | F10: Ground Truth als separates Release-Paket `truth`, nur Dozenten; Hashes im öffentlichen Manifest. `data/truth/` wird nicht in Teilnehmer-Releases aufgenommen. | Lösungsschutz |
| E15 | 2026-09-03 | Technik: Python 3.12, Paketverwaltung mit `uv`, Generator als Paket `pfefferminzia` unter `src/`, Referenzdaten als CSV/YAML unter `data/reference/`. | Vorhandene Werkzeuge, Reproduzierbarkeit |
| E16 | 2026-09-03 | Lizenz: CC BY 4.0 für Daten und Texte, MIT für Code. | Weiterverwendung durch Teilnehmer intern erlaubt |
