---
dokument_id: PTR-00000007
titel: Kunden-Persona Leon Waibel
typ: persona
sparte: GRUPPE
markt: CH
sprache: de-CH
version: "1.0"
gueltig_ab: 2025-12-31
gueltig_bis: null
tarifgeneration: PZ-2025
quelle_system: MINT
absender: Pfefferminzia Versicherungen AG
vertraulichkeit: vertraulich
erzeugt_am: 2026-09-03
---

# Leon Waibel – junger Privatkunde CH, volldigital

## Steckbrief

| Merkmal | Wert |
|---|---|
| Partner-ID | PTR-00000007 |
| Name | Leon Waibel |
| Geburtsdatum | 17.04.2001 |
| Adresse | Farnweg 9, 8004 Zürich (WG, seit 08/2024); vorher Amselgasse 2, 8630 Rüti ZH (Eltern) |
| Kanton / Land | ZH / CH |
| Sprache | de-CH |
| Beruf | Student Wirtschaftsinformatik, Teilzeit 40 Prozent als Werkstudent bei einem IT-Dienstleister |
| Familienstand | ledig |
| Vertriebskanal | Direkt / Pfefferminzia App (Haftpflicht); Säule 3a über die App mit Beratungs-Chat |
| Quellsysteme und Alt-IDs | MINT 4d7c2b19-8e5f-4a3b-9c6d-1e2f3a4b5c6d (Konto seit 03.09.2024); Eltern: HAPO 40377215 (Familienvertrag, Leon bis 2024 mitversichert) |
| Telefon | +41 44 000 64 07 (mobil hinterlegt als Festnetzformat, Datenqualität) |

## Vertragsübersicht

| Vertrag | Produkt | Tarifgeneration | Beginn | Prämie | Währung | Alt-ID | Bemerkung |
|---|---|---|---|---|---|---|---|
| VTR-00000701 | PrivatPlus Einzel, Deckungssumme CHF 5 Mio., Selbstbehalt CHF 200 | PM-2025 | 01.09.2024 | 129.20 p. a. (Alter unter 25, Zone 1, Direktrabatt, papierlos) | CHF | MINT policy 8a9b0c1d-2e3f-4a5b-8c7d-9e0f1a2b3c4d | **Gekündigt per 31.12.2025** wegen Wechsel zum Anbieter des Arbeitgebers (Kollektivrabatt) |
| VTR-00000702 | Vorsorge Säule 3a (gemischte Lebensversicherung), Prämie CHF 150 monatlich, Ablauf Alter 65, Prämienbefreiung bei Erwerbsunfähigkeit | PZ-2025 | 01.02.2025 | 1'800.00 p. a. | CHF | MINT policy c5d6e7f8-9a0b-4c1d-8e2f-3a4b5c6d7e8f | Beitragspause Juli bis September 2025 (Auslandsemester); Gesundheitsfragen alle Nein |

## Ereignisgeschichte (2016–2025)

| Datum | Ereignis | Bezug |
|---|---|---|
| 2016 bis 2024 | Mitversichert im Familienvertrag der Eltern (HAPO); als 19-Jähriger 2020 ein Kleinschaden (Handy einer Kollegin, CHF 380) über den Elternvertrag | SCH-00000710 auf Elternvertrag |
| 2024-09-03 | Konto in der App, Antrag Privathaftpflicht in vier Minuten; Chat-Frage: «Bin ich als WG-Bewohner für die Waschmaschine haftbar?»; Antwort korrekt (Mietsachschaden gedeckt) | INT-00000701 |
| 2024-09-05 | Automatische Policierung; App-Bewertung 5 Sterne | Police |
| 2025-01-20 | Chat: «Was ist Säule 3a und lohnt sich das mit 23?»; Assistent erklärt, verweist auf Beratungs-Chat mit Mensch; Video-Beratung 25 Minuten mit Kundenberater Contact Center Olten | INT-00000705, Beratungsdokumentation CH |
| 2025-02-01 | Abschluss 3a-Police; Gesundheitsfragen alle Nein; automatische Annahme | ANT-00000711, Underwriting N |
| 2025-05-12 | Adressänderung über die App abgelehnt, weil Postleitzahl 8004 mit Ort «Zürich 4» erfasst; zweiter Versuch mit «Zürich» erfolgreich | Datenqualität, INT-00000709 |
| 2025-06-28 | Antrag Beitragspause 3a für Auslandsemester (Juli bis September); genehmigt per App | Vertragsereignis |
| 2025-08-14 | E-Mail-Frage: «Ich bin in Lissabon, gilt meine Haftpflicht hier?»; Antwort aus AVB PM-2025 (weltweit, vorübergehender Aufenthalt bis 12 Monate) | INT-00000714 |
| 2025-10 | Wiederaufnahme Beitragszahlung 3a | Buchung |
| 2025-11-25 | Kündigung Privathaftpflicht per App-Formular auf 31.12.2025 mit Grund «Wechsel Anbieter»; Kündigungsbestätigung automatisch; Rückgewinnungsangebot per Push ignoriert | V14, V15, Churn-Label |
| 2025-12-02 | Chat: «Bleibt meine 3a bestehen, wenn ich die Haftpflicht kündige?»; Antwort korrekt; Assistent erwähnt fälschlich einen «Bündelrabatt», den es für 3a nicht gibt (Halluzination, im Fehlerprotokoll) | INT-00000721 |

## Rolle im Datensatz

- **UC-02 Stornoprognose:** Typischer junger Direktkunde mit kurzer Vertragsdauer und Kündigung; Features: Alter unter 25, Direktkanal, Adressänderung, Beitragspause, keine Schäden; Ground Truth: Kündigungsgrund Preiswettbewerb.
- **UC-11 RAG:** Vier Chat-Transkripte, davon eine Halluzination (Bündelrabatt); Deckungsfrage Ausland als Testfrage.
- **Datenqualität:** Telefonnummer im Festnetzformat, Ortsschreibweise «Zürich 4»; Eltern-Haushalt in HAPO als eigener Partnerstamm.
- **Beratungsdokumentation CH:** Freiwillige Dokumentation der Video-Beratung; Vergleich mit Pflichtprotokoll DE.
- **Onboarding volldigital:** Gegenstück zu Elisabeth Vogt-Schnyder (PTR-00000005).

## Kommunikationsstil

Kurz, direkt, gelegentlich Schweizerdeutsch im Chat («isch das gdeckt?»), sonst Hochdeutsch in Kleinschreibung. Stellt Fragen in einem Satz, erwartet sofortige Antwort, bewertet jede Interaktion. E-Mails nur, wenn die App keinen Chat anbietet, dann ohne Anrede. Typische Formulierungen: «kurz gefragt», «ok merci», «geht das per app?».

---

Fiktives Lehrbeispiel. Alle Daten synthetisch. Keine Verbindung zu realen Personen, Unternehmen oder Marken.
