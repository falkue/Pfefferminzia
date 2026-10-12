---
dokument_id: MIT-00010
titel: Persona Jonas Pfister, ML Engineer und MLOps Lead
typ: persona
sparte: GRUPPE
markt: GRUPPE
sprache: de-CH
version: "1.0"
gueltig_ab: 2025-12-31
gueltig_bis: null
tarifgeneration: null
quelle_system: MINT
absender: Pfefferminzia Versicherungen AG
vertraulichkeit: intern
erzeugt_am: 2026-09-03
---

# Jonas Pfister – ML Engineer / MLOps Lead

## Steckbrief

| Merkmal | Wert |
|---|---|
| Mitarbeiter-ID | MIT-00010 (MINT-Handle: jonas.pfister) |
| Name | Jonas Pfister |
| Rolle | ML Engineer, Lead MLOps & Plattform (Modell-Registry, Monitoring, LLM-Gateway) |
| Organisationseinheit | DAO-MLOPS – MLOps und Plattform (Data & AI Office) |
| Standort | Berlin, „Werkstatt"; remote-first |
| Herkunft | Minzia |
| Eintrittsjahr | 2020 (Minzia) |
| Alter | 31 (Jahrgang 1994) |
| Sprache | de-CH (Schweizer in Berlin; schreibt im Team Englisch/Deutsch gemischt) |
| E-Mail | jonas.pfister@pfefferminzia.example (Alias: jonas@minzia.example) |
| Telefon | +49 152 28817 210 |
| Vorgesetzte | Dr. Lena Mbatha-Keller (MIT-00002) |

## Biografie

Jonas Pfister wächst in Frauenfeld auf, studiert Informatik an der ETH Zürich und schreibt seine Masterarbeit über Monitoring von Machine-Learning-Systemen. Nach zwei Jahren bei einem Zürcher Logistik-Start-up zieht er 2020 nach Berlin, weil Minzia jemanden sucht, der Modelle nicht nur trainiert, sondern betreibt. Er baut die Modell-Registry, den Feature Store und das Deployment von MINT auf, mit täglichen Releases und einem Team, das sich über Slack organisiert.

Er ist Autor des Schaden-Triage-Modells, das 2021 bei Pfefferminz pilotiert wird, und des Betrugsscores, der 2025 die Serienschäden der Transportlogistik Grimm erkennt. Er ist auch derjenige, der 2025 die Entwicklungsumgebung verantwortet, in die ein Kollege echte Leben-Anträge als Testdaten lädt. Der Vorfall und die anschliessende Sperre haben ihn getroffen; er hat danach das Pseudonymisierungskonzept geschrieben, das der Datenschutzbeauftragte inzwischen als Referenz nutzt.

Seit dem Closing ärgert ihn vor allem eines: Ein Deployment, das früher am Nachmittag live war, braucht jetzt ein Change-Ticket, eine Validierung und zwei Freigaben. Er versteht inzwischen, warum, findet den Prozess aber schlecht gebaut. Er lebt in Berlin-Neukölln, klettert, hat den Schweizer Wehrdienst hinter sich und spricht mit Ruth Amrein Mundart, was in Olten für Verwirrung sorgt.

## Haltung zu KI

Technik-optimistisch, lernend. Modelle sind für ihn Software mit Statistik, und Software gehört überwacht, versioniert und zurückrollbar. Er hält Governance für richtig und die Umsetzung für bürokratisch. Was er von Amrein über Altverträge gelernt hat, hat seinen Respekt vor Domänenwissen deutlich erhöht.

> «Ich hab kein Problem damit, dass jemand mein Modell validiert. Ich hab ein Problem damit, dass die Validierung in einem Word-Dokument lebt und drei Wochen dauert. Baut mir das als Pipeline, und ich mach's freiwillig.»

## Typische Aufgaben und Systeme

- Deployment und Monitoring der produktiven Modelle (Schaden-Triage, Betrugsscore, Risikoprüfung Leben MZ-Generation, Chat-Assistent)
- LLM-Gateway: Prompt-Logging, Filter für Personendaten, Modellversionen
- Herbarium: Feature-Pipelines, Drift-Berichte; Migrationsunterstützung für die Leben-Welle
- Systeme: MINT (Kern), Herbarium, Slack, Wiki, Git; VERA-Extrakte nur als Parquet, „Fixed-width hab ich das erste Mal 2025 gesehen"

## Konflikte und Beziehungen

- **Urs Bächtold (MIT-00003):** entzieht ihm nach dem Vorfall die Produktivrechte; Pfister hält ihn für den Grund, dass Deployments Wochen dauern.
- **Sven Lindqvist-Brandt (MIT-00006):** vom Gegner zum widerwilligen Partner; das Pseudonymisierungskonzept ist gemeinsame Arbeit.
- **Ruth Amrein (MIT-00007):** Wissenstransfer-Tandem; er lernt Altverträge, sie lernt, was ein Feature ist.
- **Aylin Demirci (MIT-00009):** seine anspruchsvollste Nutzerin; die Pieper-Regel war eine Konfiguration, die er im Review übersehen hat.
- **Tobias Wenger (MIT-00008):** liefert ihm Fehlklassifikationen der Vorprüfung; «unser bester Labeler».
- **Dario Bianchi (MIT-00013):** meldet Assistenten-Fehler über den Feedback-Button; Pfister antwortet ihm persönlich.

## Rolle in Seminar-Gruppenarbeiten (Rollenkarte Data Science / ML Engineering)

- **Ziele:** Deployments in Tagen statt Wochen, Monitoring mit Alarmen statt Quartalsberichten, ein Modellinventar, das aus der Registry generiert wird, kein Word-Dokument.
- **Sorgen:** Freigabeprozesse, die Iteration verhindern; Modelle, die auf Altdaten mit Bias trainiert sind, für die er den Kopf hinhalten muss; Talente, die zu Start-ups gehen.
- **Argumente:** «Das ist ein Datenproblem, kein Modellproblem.» – «Wir haben Monitoring, ihr habt Meetings.» – «Leakage erkennt man am Zeitstempel, nicht am Bauchgefühl.» – «Gebt mir eine API für die Freigabe, dann automatisiere ich die Governance.»
- **Typische Frage an die Gruppe:** «Welche Metrik würde euch morgen früh aufwecken?»

## Schreibstil für spätere Korrespondenz

- Tonalität: informell, schnell, technisch; Slack mit Codeblöcken, Emojis, Threads; E-Mails selten und kurz; Englisch-Deutsch-Mix («deployed», «rollback», «Feature»).
- Anrede: «hey», «hi Aylin», «Hallo Herr Bächtold» (siezt nur ihn und Ruth Amrein, die er «Frau Amrein» nennt und mit der er Mundart spricht).
- Grussformel: «lg jonas», in E-Mails «Beste Grüsse, Jonas».
- Typische Formulierungen: «quick question», «ist gefixt», «kann ich heute noch shippen?», «das ist nicht das Modell, das sind die Daten», «wer hat das Ticket?», «tl;dr».
- Rechtschreibung de-CH (kein ß, auch in Berlin), Kleinschreibung in Chats.

---

Fiktives Lehrbeispiel. Alle Daten synthetisch. Keine Verbindung zu realen Personen, Unternehmen oder Marken.
