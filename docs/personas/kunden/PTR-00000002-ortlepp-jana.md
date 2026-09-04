---
dokument_id: PTR-00000002
titel: Kunden-Persona Jana Ortlepp
typ: persona
sparte: GRUPPE
markt: DE
sprache: de-CH
version: "1.0"
gueltig_ab: 2025-12-31
gueltig_bis: null
tarifgeneration: null
quelle_system: MINT
absender: Pfefferminzia Versicherungen AG
vertraulichkeit: vertraulich
erzeugt_am: 2026-09-03
---

# Jana Ortlepp – Privatkundin DE, digital

## Steckbrief

| Merkmal | Wert |
|---|---|
| Partner-ID | PTR-00000002 |
| Name | Jana Ortlepp |
| Geburtsdatum | 22.08.1996 |
| Adresse | Holunderstieg 12, 04277 Leipzig (seit 09/2021; vorher bei den Eltern in 04600 Altenburg) |
| Bundesland / Land | Sachsen / DE |
| Sprache | de-DE |
| Beruf | UX-Designerin in einer Digitalagentur, seit 2021 Berufseinsteigerin |
| Familienstand | ledig |
| Vertriebskanal | Direkt / App (ehemals minzia.direct, seit 2025 Pfefferminzia App) |
| Quellsystem und Alt-ID | MINT 7c1f3a2e-9b4d-4e6a-8f21-5d3c0a9b7e14 (Nutzerkonto seit 15.03.2021) |
| Telefon | +49 152 28817 302 (mobil) |

## Vertragsübersicht

| Vertrag | Produkt | Tarifgeneration | Beginn | Prämie | Währung | Alt-ID | Bemerkung |
|---|---|---|---|---|---|---|---|
| (storniert) | PrivatPlus Single (Privathaftpflicht DE, Deckung EUR 10 Mio.) | MZ-DIRECT | 15.03.2021 | 58.80 p. a. | EUR | MINT policy 2d8e5f10-3a7b-4c9d-9e02-b61f4a8c2d75 | Widerruf am 24.03.2021 innerhalb 14 Tagen (noch über Eltern familienversichert) |
| VTR-00000201 | PrivatPlus Single (Privathaftpflicht DE, Deckung EUR 10 Mio., Baustein Schlüsselverlust) | MZ-DIRECT | 01.09.2021 | 58.80 p. a., ab 2024 63.60 | EUR | MINT policy a4b7c2d9-1e3f-4a5b-8c6d-7e8f9a0b1c2d | Neuabschluss nach Auszug; Migration auf Pfefferminzia App 04/2025 |
| VTR-00000202 | RisikoLeben DE, EUR 200'000, 30 Jahre, Nichtraucherin | PZ-2025 | 01.10.2025 | 175.20 p. a. (14.60 monatlich, Zahlbeitrag) | EUR | MINT policy e9f0a1b2-c3d4-4e5f-9a6b-7c8d9e0f1a2b | Volldigitaler Antrag, automatisierte Risikoprüfung ohne Erschwerung |

## Ereignisgeschichte (2016–2025)

| Datum | Ereignis | Bezug |
|---|---|---|
| 2021-03-15 | Digitaler Antrag Privathaftpflicht über minzia.direct nach Vergleichsportal; Chat mit dem Minzia-Assistenten («Brauche ich das, wenn ich noch bei meinen Eltern wohne?») | Chat-Transkript INT-00000201 |
| 2021-03-24 | Widerruf per E-Mail (Formulierung aus Vorlage im Internet), Bestätigung automatisch am selben Tag, Beitragsrückerstattung EUR 1.45 | Widerrufsschreiben, INT-00000202 |
| 2021-09-01 | Neuabschluss nach Umzug nach Leipzig; Antrag in 6 Minuten; E-Signatur | VTR-00000201 |
| 2023-02-07 | Schlüsselverlust Mietwohnung, Schliessanlage ersetzt, EUR 780; Meldung per App, Foto der Rechnung, automatische Zahlung am 2023-02-09 | SCH-00000210 |
| 2024-01 | Beitragsanpassung MZ-DIRECT (Indexierung); Push-Nachricht, keine Reaktion | Vertragsversion |
| 2024-11-18 | Chat-Frage: «Bin ich im Urlaub in Portugal versichert?»; Assistent antwortet korrekt aus Minzia-AVB (weltweit 1 Jahr) | Chat-Transkript INT-00000230 |
| 2025-04-14 | E-Mail zur Umstellung minzia.direct auf Pfefferminzia App; Jana fragt per Chat, ob sich die Bedingungen ändern (Antwort: nein, MZ-DIRECT gilt weiter) | INT-00000241 |
| 2025-09-08 | Chat: «Ich hab jetzt eine Wohnung gekauft, brauche ich eine Risikoleben?»; Assistent erklärt Produkt, verweist auf digitalen Antrag | INT-00000255 |
| 2025-09-09 | Digitaler Antrag RisikoLeben: Gesundheitsfragen als Ja/Nein plus Freitext («vor 2 Jahren Physio wegen Rückenschmerzen, seither nichts»); automatische Annahme | ANT-00000221 |
| 2025-09-30 | Police per App; Jana bewertet den Prozess in der App mit 4 Sternen («Freitextfeld war unklar») | Dokument |
| 2025-11-03 | Chat-Frage nach Steuerbescheinigung; Assistent liefert falsche Aussage (verwechselt Risikoleben mit Rentenversicherung); Jana meldet «Das stimmt nicht»; Ticket an Data & AI Office | INT-00000262, Fehlerprotokoll |

## Rolle im Datensatz

- **UC-11 RAG / Chatbot:** mehrere Chat-Transkripte mit korrekten und einer falschen Antwort; Bedingungen der Generation MZ-DIRECT gelten nach der Migration weiter (Metadaten-Falle F5).
- **UC-04 Antragsextraktion:** volldigitaler Antrag mit Gesundheitsfragen im JSON-Format (MINT), Freitext mit Gesundheitsbezug (UC-18 PII- und Gesundheitsdaten).
- **Widerrufs-Storyline:** Widerruf innerhalb 14 Tagen (§ 8 VVG DE, vereinfachte Darstellung) und Neuabschluss; in MINT zwei Policen mit demselben Nutzerkonto, davon eine storniert; für UC-02 Storno ist die erste Police kein «echter» Storno (Label-Falle).
- **UC-08 Dubletten:** nur in MINT vorhanden, kein HAPO-Satz; Adresse der Eltern in der ersten Police.
- **Drift:** typische Minzia-Kundin (jung, digital, DE) als Kontrast zum Pfefferminz-Bestand.

## Kommunikationsstil

Schnell, informell, chatgewohnt. Jana schreibt in Kleinschreibung, mit Abkürzungen («lg», «kp»), gelegentlich einem Emoji, stellt direkte Fragen und erwartet Antworten in Minuten. Sie duzt den Assistenten und siezt Menschen, wenn sie bemerkt, dass ein Mensch antwortet. E-Mails schreibt sie nur, wenn es die App verlangt (Widerruf), dann formell nach Vorlage: «Hiermit widerrufe ich …». Typische Formulierungen: «kurze frage», «passt, danke», «das stimmt nicht, oder?».

---

Fiktives Lehrbeispiel. Alle Daten synthetisch. Keine Verbindung zu realen Personen, Unternehmen oder Marken.
