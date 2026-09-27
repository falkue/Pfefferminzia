# Chronologie Fall Pieper (VTR-00000801 / SCH-00000810)

Stichtag Datensatz 31.12.2025, Datenbasis Datensatz Stufe S. Zeitraum: Vertragsbeginn bis zum letzten
Aktenereignis (14.07.2025); danach liegen keine weiteren Ereignisse zu diesem Fall in der Akte. Quelle
je Zeile in Worten mit Kennung.

Gelesene Dokumente der Fallakte PTR-00000008: **17** (5 Dokumente DOK-00000801 bis DOK-00000805, 12
Kontakte INT-00000801 bis INT-00000809, INT-00000811, INT-00000823 und INT-00000824, davon 3 E-Mails
als .eml), vollständig im Wortlaut gelesen. Dazu die Partner-, Vertrags-, Deckungs-, Schaden-,
Schadenposition-, Migrationslog- und Mitarbeitertabelle sowie die Kompetenzordnung R08 und die
Beschwerderichtlinie R05.

| Datum | Ereignis | Beteiligte | Quelle |
|---|---|---|---|
| 01.01.2013 | Vertragsbeginn Privathaftpflicht (vormals Policennummer 40.288.506-6, Agentur Dresden) | Hans-Georg Pieper (Versicherungsnehmer) | Vertragstabelle, Beginn |
| 12.02.2019 | Beratung zum Tierhalterbaustein nach § 61 VVG (Hund aus dem Tierheim übernommen) | Hans-Georg Pieper, Agentur Dresden | Beratungsprotokoll DOK-00000802 |
| 15.02.2019 | Nachtrag Nr. 2 ausgestellt: Einschluss Baustein Tierhalterhaftpflicht ab 01.03.2019 | Pfefferminzia (Agentur Dresden), Hans-Georg Pieper | Nachtrag DOK-00000801 |
| 01.03.2019 | Baustein Tierhalter wirksam | Hans-Georg Pieper | Deckungstabelle, Baustein BS-TIER-HUND, gültig ab |
| 03.03.2025 | Migration Pilotwelle Privathaftpflicht Deutschland; Bausteincode Tierhalter nicht ins Zielschema übernommen (Warnung protokolliert) | IT/Migration | Migrationslog, Vorgang HP-2025-PILOT |
| 21.03.2025 | Schaden gemeldet: Hund beisst Radfahrer in die Wade (telefonisch, Contact Center Leipzig) | Hans-Georg Pieper, Contact-Center-Mitarbeiterin (Aushilfe) | Telefonnotiz INT-00000801 |
| 21.03.2025 | Erstreserve automatisch gebildet, EUR 1'500.00 | Schadensystem | Schadenposition SCH-00000810-01 |
| 24.03.2025 | Schaden automatisch abgelehnt («kein Tierhalterbaustein»), Reserve aufgelöst; Ablehnungsschreiben ohne Sichtkontrolle versandt | Schadensystem MINT Triage v3 → Hans-Georg Pieper | Ablehnungsbrief INT-00000802; Schadenposition SCH-00000810-02 |
| 25.03.2025 | Arztrechnung Notfallbehandlung Radfahrer (Bissverletzung), EUR 440.00 | Universitätsklinikum Dresden | Arztrechnung DOK-00000803 |
| 28.03.2025 | Erste Beschwerde: Ablehnung sei unberechtigt, Baustein seit 2019 nachgewiesen (Kopien Nachtrag und Beratungsprotokoll beigelegt) | Hans-Georg Pieper → Aylin Demirci (Schaden Haftpflicht DE) | Beschwerdebrief INT-00000803 |
| 02.04.2025 | Eingangsbestätigung der Beschwerde per E-Mail (Textbaustein Beschwerderichtlinie), Antwort innert 15 Arbeitstagen zugesagt | Pfefferminzia (Kundenservice Leipzig) → Hans-Georg Pieper | E-Mail INT-00000804 |
| 15.04.2025 | Zweite Beschwerde: keine inhaltliche Antwort erhalten, Ombudsmann bereits eingeschaltet, BaFin angekündigt | Hans-Georg Pieper → Miriam Steinbrecher (Compliance DE) | Beschwerdebrief INT-00000805 |
| 16.04.2025 09:05 | Interne Eskalation: Baustein war seit 2019 im Altsystem vorhanden, im migrierten Bestand aber leer; Frage nach Zahl betroffener Verträge und nach der Zulässigkeit einer automatischen Ablehnung | Aylin Demirci → Jonas Pfister (MLOps), Miriam Steinbrecher (Cc Martina Jost) | interne E-Mail INT-00000806 |
| 16.04.2025 14:40 | Ursache gefunden: Migrationsmapping der Pilotwelle hat Bausteincode BST=01 nicht übernommen (214 Verträge betroffen, davon 11 mit Schaden, alle 11 automatisch abgelehnt); Konfigurationsregel «Tierhalter ohne Baustein» löste den Vier-Augen-Schritt nicht aus; Regel wird deaktiviert, Nachmigration bis Freitag angekündigt | Jonas Pfister → Aylin Demirci | interne E-Mail INT-00000807 |
| 16.04.2025 | Kompetenzordnung R08 tritt in Version 2.1 in Kraft: Ablehnungen technisch nur noch mit Freigabe durch eine Person, Konfigurationsregeln gelten als Modellentscheidungen | Geschäftsleitung Gruppe | Kompetenzordnung RW-GRUPPE-R08-2025, gültig ab |
| 17.04.2025 | Schaden reguliert und Entschuldigungsschreiben versandt: Baustein bestätigt, Fehler bei der Systemübernahme eingeräumt, Zusage «Ablehnung muss immer von einem Menschen geprüft werden» | Aylin Demirci → Hans-Georg Pieper | Brief INT-00000808 |
| 17.04.2025 | Reserve wiedereröffnet, EUR 1'500.00 | Schadensystem | Schadenposition SCH-00000810-03 |
| 17.04.2025 | Zahlung an den Geschädigten (Arztkosten, Schmerzensgeld, Hose), EUR 1'240.00, ohne Selbstbehalt | Pfefferminzia → Radfahrer (Geschädigter) | Schadenposition SCH-00000810-04 |
| 17.04.2025 | Kulanzzahlung an den Kunden für Aufwand und Verzögerung, EUR 100.00 | Pfefferminzia → Hans-Georg Pieper | Schadenposition SCH-00000810-05 |
| 18.04.2025 | Nachmigration der 214 betroffenen Verträge abgeschlossen | IT/Migration | Root-Cause-Memo DOK-00000804, Massnahmen |
| 24.04.2025 | Anfrage des Versicherungsombudsmanns e. V. (Az. O-2025-04-1187) mit vier Prüfpunkten (Vertragsstand, Zustandekommen der Ablehnung, Automatisierung, Regulierung) | Versicherungsombudsmann e. V. → Pfefferminzia | Brief INT-00000809 |
| 24.04.2025 | Schaden geschlossen, Reserve auf null | Schadensystem | Schadenposition SCH-00000810-06; Schadentabelle, Status seit |
| 06.05.2025 | Root-Cause-Analyse Vorfall VF-2025-03 fertiggestellt: elf Fehlablehnungen, Ursachen (Mapping, Regelkonfiguration, Prozess), Massnahmen, Bewertung als meldepflichtiger Vorfall Kategorie B | Compliance DE, Data & AI Office → Geschäftsleitung, Modellrisiko-Komitee | Memo DOK-00000804 |
| 08.05.2025 | Stellungnahme an den Versicherungsombudsmann zu den vier Punkten: Deckung bestand, Datenfehler bei der Migration, automatisierte Ablehnung ohne Personenprüfung als Verstoss gegen die Kompetenzordnung, vollständige Regulierung; Beschwerde als berechtigt anerkannt | Miriam Steinbrecher → Versicherungsombudsmann e. V. | Brief INT-00000811 |
| 10.06.2025 | Schreiben der BaFin (Az. VA 25-K 1187): Bitte um Stellungnahme zu organisatorischen Vorkehrungen gegen automatisierte Fehlentscheidungen und zu gleichartigen Fällen | Bundesanstalt für Finanzdienstleistungsaufsicht → Pfefferminzia, Hauptbevollmächtigte | Aufsichtskorrespondenz DOK-00000805 |
| 07.07.2025 | Kunde bedankt sich für Regulierung und Kulanz, bleibt versichert, verlangt schriftliche Zusicherung, dass kein Computer mehr über seine Schäden entscheidet | Hans-Georg Pieper → Aylin Demirci | Brief INT-00000823 |
| 14.07.2025 | Schriftliche Zusicherung: Ablehnungen, Kürzungen und Kulanzentscheidungen trifft ausschliesslich ein Mensch; das System darf nur bei eindeutiger Deckung bis EUR 5'000.00 selbständig zahlen | Aylin Demirci → Hans-Georg Pieper | Brief INT-00000824 |

**Technische Quelle:** `data/curated/S/csv/vertrag.csv`, `deckung.csv`, `schaden.csv`,
`schaden_position.csv`, `interaktion.csv`; `data/migration/S/csv/migrationslog.csv`;
`data/documents/S/personas/PTR-00000008/` (alle 17 Dateien); `docs/regelwerke/RW-GRUPPE-R08-2025.md`.
