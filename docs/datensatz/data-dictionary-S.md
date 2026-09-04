# Data Dictionary Stufe S

Erzeugt aus `data/manifest_S.json` durch `scripts/build_data_dictionary.py`. Stichtag 2025-12-31, Master-Seed 20250101, Version 0.1.0.

Schichten: `curated` (harmonisiert, fuer Teilnehmer), `truth` (latente Wahrheit und Labels, nur Dozenten), `migration` (Kreuzreferenzen, Feldmapping, Migrationslog), `raw` (Rohextrakte der Quellsysteme, siehe unten).

## Tabellen

| Tabelle | Zeilen | Spalten | Beschreibung |
|---|---|---|---|
| curated/agentur | 12 | 11 | Vertriebsorganisationen: Exklusivagenturen, Makler, Banken, Portale, Direkt |
| curated/antrag | 1610 | 17 | Antraege inkl. abgelehnter und zurueckgezogener; Underwriting-Entscheid, Angaben zu BMI und Rauchen |
| curated/deckung | 2208 | 9 | Deckungen je Vertrag: Hauptdeckung, Bausteine, Zusatzversicherungen |
| curated/dokument | 37 | 20 |  |
| curated/interaktion | 62 | 18 |  |
| curated/mitarbeiter | 60 | 20 | Mitarbeitende inkl. der 14 Personas; Herkunft Pfefferminz/Minzia/neu/extern |
| curated/org_einheit | 69 | 10 | Organisationseinheiten der Gruppe (drei Ebenen) |
| curated/partner | 1000 | 30 | Partner: natuerliche und juristische Personen (Kunden, Mitversicherte, Beguenstigte, Inhaber) |
| curated/partner_adresse | 1250 | 13 | Adressen mit Historie (Umzuege); genau eine aktuelle Adresse je Partner |
| curated/partner_beziehung | 458 | 4 | Beziehungen: Ehepartner, Kinder, Inhaber, Kontaktpersonen (von -> zu) |
| curated/partner_firma | 62 | 6 | Firmenmerkmale juristischer Personen: Branche (NACE), Risikoklasse, Umsatz, Mitarbeitende |
| curated/partner_kontakt | 1876 | 5 | Kontaktkanaele (E-Mail, Telefon, Mobil), nur Fiktionsbereiche |
| curated/produkt | 7 | 5 | Produktkatalog beider Sparten |
| curated/risiko_objekt | 1481 | 19 | Risikoobjekt je Vertrag: Haushalt, Betrieb, Beruf oder versicherte Person |
| curated/schaden | 16 | 29 |  |
| curated/schaden_position | 58 | 8 |  |
| curated/tarifgeneration | 14 | 9 | Bedingungs- und Tarifgenerationen mit Gueltigkeit |
| curated/vermittler | 40 | 14 | Vermittlerpersonen mit Agenturzuordnung, Alt- und Neunummer |
| curated/vertrag | 1481 | 35 | Vertraege beider Sparten mit Status, Praemie, Kanal, Quellsystem, Migrationsdatum |
| curated/vertrag_partner_rolle | 3425 | 4 | Rollen der Partner am Vertrag: VN, mitversichert, versicherte Person, beguenstigt |
| migration/feld_mapping | 42 | 9 | Feldweise Abbildung Quellsystem -> curated mit Transformationsregeln und DQ-Bezug |
| migration/migrationslog | 1821 | 8 | Simuliertes Log der Migrationswellen 2025 (OK/WARN/ERROR) |
| migration/partner_xref | 1766 | 8 | Kreuzreferenz Partner: curated-ID zu Quell-IDs in HAPO, VERA, MINT mit Match-Methode und Score |
| migration/vertrag_xref | 2304 | 8 | Kreuzreferenz Vertraege: curated-ID zu Quell-IDs |
| truth/dq_injektionen | 1223 | 7 | Protokoll aller injizierten Datenqualitaetsprobleme mit Originalwert (nur Dozenten) |
| truth/partner_latent | 1000 | 10 | Latente Wahrheit je Partner: Kuendigungsneigung, Betrugsneigung, BMI, Raucher, Todesdatum (nur Dozenten) |
| truth/schaden_latent | 16 | 4 |  |
| truth/vertrag_latent | 1481 | 11 | Latente Wahrheit je Vertrag: Tarifpraemie, Abweichung, Kuendigung in 12 Monaten, Bias-Anwendung (nur Dozenten) |

### curated/agentur

Vertriebsorganisationen: Exklusivagenturen, Makler, Banken, Portale, Direkt

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| agentur_id | str | AGT-0001 | 0 |
| name | str | Aare-Bank AG | 0 |
| typ | str | BANK | 0 |
| kanal | str | bank | 0 |
| land | str | CH | 0 |
| plz | str | 1066 | 0 |
| ort | str | Epalinges | 0 |
| region | str | VD | 0 |
| agenturnummer | str | 0001 | 0 |
| seit | object | 2016-01-01 | 0 |
| herkunft | str | pfefferminz | 0 |

### curated/antrag

Antraege inkl. abgelehnter und zurueckgezogener; Underwriting-Entscheid, Angaben zu BMI und Rauchen

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| antrag_id | str | ANT-00000101 | 0 |
| vertrag_id | str | VTR-00000101 | 129 |
| produkt_id | str | HP-PRIV | 0 |
| antragsteller_id | str | PTR-00000001 | 0 |
| markt | str | CH | 0 |
| tarifgeneration_id | str | HP-MODERN | 0 |
| kanal | str | agentur | 0 |
| eingang | object | 2016-02-08 | 0 |
| entscheid_am | object | 2016-02-15 | 0 |
| gewuenschter_beginn | object | 2016-03-01 | 0 |
| status | str | ANGENOMMEN | 0 |
| uw_entscheid_code | str | N | 0 |
| uw_zuschlag_pct | float64 | 0.0 | 0 |
| uw_automatisiert | bool | False | 0 |
| bmi_angabe | float64 | 22.0 | 998 |
| raucher_angabe | object | False | 998 |
| sparte | str | HP | 0 |

### curated/deckung

Deckungen je Vertrag: Hauptdeckung, Bausteine, Zusatzversicherungen

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| deckung_id | str | DEK-00000101-01 | 0 |
| vertrag_id | str | VTR-00000101 | 0 |
| deckungsart | str | HAUPTDECKUNG | 0 |
| baustein | str | BS-AUSFALL | 1481 |
| summe | float64 | 10000000.0 | 611 |
| selbstbehalt | float64 | 200.0 | 1298 |
| selbstbehalt_typ | str | fix | 1298 |
| gueltig_von | object | 2016-03-01 | 0 |
| gueltig_bis | object | 2021-03-24 | 1545 |

### curated/dokument



| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| dokument_id | str | DOK-00000101 | 0 |
| dokument_typ | str | BERATUNGSPROTOKOLL | 0 |
| richtung | str | INTERN | 0 |
| format | str | MD | 0 |
| ist_gerendert | bool | True | 0 |
| ocr_qualitaet | str | GUT | 0 |
| seiten | int64 | 2 | 0 |
| titel | str | Beratungsdokumentation Risikoleben Ehepa | 0 |
| absender | str | Generalagentur Luzern | 0 |
| empfaenger | str | Akte | 0 |
| partner_id | str | PTR-00000001 | 0 |
| vertrag_id | str | VTR-00000102 | 23 |
| schaden_id | str | SCH-00000118 | 22 |
| antrag_id | str | ANT-00000602 | 29 |
| interaktion_id | object |  | 37 |
| erstellt_am | object | 2018-05-14 | 0 |
| quellsystem | str | DOKU | 0 |
| datei_pfad | str | data/documents/S/personas/PTR-00000001/D | 0 |
| text_body | str | Anlass: Geplante Hypothekaraufnahme fuer | 0 |
| ist_persona_fall | bool | True | 0 |

### curated/interaktion



| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| interaktion_id | str | INT-00000412 | 0 |
| kanal | str | APP | 0 |
| richtung | str | EINGEHEND | 0 |
| zeitpunkt | datetime64[us] | 2025-05-18 09:14:00 | 0 |
| dauer_sekunden | object |  | 62 |
| partner_id | str | PTR-00000001 | 0 |
| mitarbeiter_id | str | MIT-00013 | 17 |
| vermittler_id | str | VRM-00017 | 45 |
| bezug_typ | str | SCHADEN | 0 |
| bezug_id | str | SCH-00000118 | 4 |
| thread_id | str | TH-00000118 | 0 |
| betreff | str | Schadenmeldung E-Bike Nachbar | 0 |
| zusammenfassung | object |  | 62 |
| sprache | str | de | 0 |
| sentiment_agent | str | neutral | 26 |
| datei_pfad | str | data/documents/S/personas/PTR-00000001/I | 0 |
| text_body | str | Guten Tag

Gestern Nachmittag hat unser  | 0 |
| ist_persona_fall | bool | True | 0 |

### curated/mitarbeiter

Mitarbeitende inkl. der 14 Personas; Herkunft Pfefferminz/Minzia/neu/extern

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| mitarbeiter_id | str | MIT-00001 | 0 |
| personalnummer | str | 10007 | 20 |
| vorname | str | Beatrice | 0 |
| nachname | str | Hauenstein | 0 |
| geschlecht | str | W | 0 |
| geburtsjahr | int64 | 1971 | 0 |
| rolle | str | CEO und Vorsitzende der Geschäftsleitung | 0 |
| org_einheit_id | str | ORG-001 | 0 |
| org_kuerzel | str | GL | 0 |
| standort | str | Olten | 0 |
| land | str | CH | 0 |
| herkunft | str | pfefferminz | 0 |
| eintritt | object | 2021-01-01 | 0 |
| austritt | object | 2025-09-01 | 57 |
| sprache | str | de-CH | 0 |
| ki_haltung | str | treibend | 0 |
| email | str | beatrice.hauenstein@pfefferminzia.exampl | 0 |
| kompetenzstufe | int64 | 4 | 0 |
| ist_persona | bool | True | 0 |
| mint_handle | str | beatrice.hauenstein | 0 |

### curated/org_einheit

Organisationseinheiten der Gruppe (drei Ebenen)

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| org_einheit_id | str | ORG-000 | 0 |
| kuerzel | str | VR | 0 |
| name | str | Verwaltungsrat Pfefferminzia Holding AG | 0 |
| uebergeordnet_id | str | ORG-000 | 1 |
| ebene | int64 | 0 | 0 |
| standort | str | Olten | 0 |
| land | str | CH | 0 |
| fte | int64 | 0 | 0 |
| herkunft | str | gemischt | 0 |
| leitung_rolle | str | Präsidentin des Verwaltungsrats | 0 |

### curated/partner

Partner: natuerliche und juristische Personen (Kunden, Mitversicherte, Beguenstigte, Inhaber)

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| partner_id | str | PTR-00000001 | 0 |
| partner_typ | str | NATUERLICH | 0 |
| anrede | str | Frau | 0 |
| titel | str | Dr. med. | 989 |
| vorname | str | Simone | 62 |
| nachname | str | Niederberger | 62 |
| firmenname | str | Schreinerei Kaufmann + Söhne GmbH | 938 |
| rechtsform | str | GmbH | 938 |
| uid_hrb_nummer | str | CHE-499.480.349 | 938 |
| geburtsdatum | object | 1984-03-14 | 0 |
| geschlecht | str | W | 0 |
| nationalitaet | str | CH | 0 |
| zivilstand | str | VERHEIRATET | 0 |
| beruf_code | str | B18 | 62 |
| beruf_text | str | Physiotherapeutin | 62 |
| beruf_selbstaendig | object | False | 62 |
| sprache | str | de | 0 |
| land_wohnsitz | str | CH | 0 |
| kundensegment | str | PRIVAT | 0 |
| kunde_seit | object | 2016-03-01 | 241 |
| status | str | AKTIV | 0 |
| todesdatum | object | 2019-02-14 | 998 |
| datenschutz_werbung_ok | bool | True | 0 |
| datenschutz_ki_ok | bool | True | 0 |
| herkunft | str | pfefferminz | 0 |
| quellsystem_primaer | str | HAPO | 0 |
| haushalt_id | str | HH-000001 | 59 |
| ist_persona | bool | True | 0 |
| erstellt_am | datetime64[us] | 2016-03-01 09:00:00 | 0 |
| geaendert_am | datetime64[us] | 2016-03-01 09:00:00 | 0 |

### curated/partner_adresse

Adressen mit Historie (Umzuege); genau eine aktuelle Adresse je Partner

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| adresse_id | str | ADR-00000001 | 0 |
| partner_id | str | PTR-00000001 | 0 |
| adresse_typ | str | WOHNSITZ | 0 |
| strasse | str | Rebhaldenweg | 0 |
| hausnummer | str | 7 | 0 |
| plz | str | 6004 | 0 |
| ort | str | Luzern | 0 |
| region | str | LU | 0 |
| land | str | CH | 0 |
| tarifzone | str | 1 | 0 |
| gueltig_von | object | 2023-06-01 | 0 |
| gueltig_bis | object | 2023-05-31 | 1000 |
| ist_aktuell | bool | True | 0 |

### curated/partner_beziehung

Beziehungen: Ehepartner, Kinder, Inhaber, Kontaktpersonen (von -> zu)

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| partner_id_von | str | PTR-00000011 | 0 |
| partner_id_zu | str | PTR-00000001 | 0 |
| beziehung | str | EHEPARTNER | 0 |
| seit | object | 2010-01-01 | 249 |

### curated/partner_firma

Firmenmerkmale juristischer Personen: Branche (NACE), Risikoklasse, Umsatz, Mitarbeitende

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| partner_id | str | PTR-00000003 | 0 |
| branche_id | str | BK-008 | 0 |
| nace_code | str | 43.32 | 0 |
| risikoklasse | float64 | 3.0 | 0 |
| mitarbeitende | float64 | 14.0 | 0 |
| umsatz | float64 | 2600000.0 | 0 |

### curated/partner_kontakt

Kontaktkanaele (E-Mail, Telefon, Mobil), nur Fiktionsbereiche

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| kontakt_id | str | KON-00000001 | 0 |
| partner_id | str | PTR-00000001 | 0 |
| kontakt_typ | str | EMAIL | 0 |
| wert | str | simone.niederberger@mail.example | 0 |
| ist_primaer | bool | True | 0 |

### curated/produkt

Produktkatalog beider Sparten

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| produkt_id | str | HP-PRIV | 0 |
| marktname | str | PrivatPlus | 0 |
| sparte | str | HP | 0 |
| maerkte | str | CH;DE | 0 |
| status | str | aktiv | 0 |

### curated/risiko_objekt

Risikoobjekt je Vertrag: Haushalt, Betrieb, Beruf oder versicherte Person

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| risiko_objekt_id | str | RIS-00000101 | 0 |
| vertrag_id | str | VTR-00000101 | 0 |
| risiko_typ | str | HAUSHALT | 0 |
| personen | float64 | 4.0 | 714 |
| hund | object | False | 714 |
| personenkreis | str | familie | 714 |
| branche_id | str | BK-008 | 1355 |
| nace_code | str | 43.32 | 1355 |
| risikoklasse | float64 | 3.0 | 1355 |
| umsatz | float64 | 2600000.0 | 1355 |
| mitarbeitende | float64 | 14.0 | 1355 |
| bemessungsgrundlage | float64 | 1092000.0 | 1338 |
| berufsgruppe | str | BG-ARCH | 1464 |
| untergruppe | str | architekt | 1464 |
| versicherte_person_id | str | PTR-00000001 | 910 |
| eintrittsalter | float64 | 35.0 | 911 |
| raucher_angabe | object | False | 910 |
| bmi_angabe | float64 | 22.0 | 910 |
| summenverlauf | object |  | 1481 |

### curated/schaden



| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| schaden_id | str | SCH-00000110 | 0 |
| schadennummer_anzeige | str | S2019/001001 | 0 |
| vertrag_id | str | VTR-00000101 | 0 |
| partner_id | str | PTR-00000001 | 0 |
| sparte | str | HP | 0 |
| art | str | HP_PERSONEN | 0 |
| ursache_code | str | SKI_KOLLISION | 0 |
| schadendatum | object | 2019-02-16 | 0 |
| meldedatum | object | 2019-02-18 | 0 |
| erfassungsdatum | object | 2019-02-18 | 0 |
| meldekanal | str | VERMITTLER | 0 |
| schadenort_plz | str | 3818 | 0 |
| schadenort_land | str | CH | 0 |
| beschreibung_kurz | str | Reto Niederberger kollidiert auf der Pis | 0 |
| status | str | GESCHLOSSEN | 0 |
| status_seit | object | 2019-06-04 | 0 |
| reserve_aktuell | float64 | 0.0 | 0 |
| bezahlt_total | float64 | 4180.0 | 0 |
| regress_total | float64 | 0.0 | 0 |
| waehrung | str | CHF | 0 |
| deckung_geprueft | bool | True | 0 |
| deckung_ergebnis | str | GEDECKT | 0 |
| ablehnungsgrund_code | str | ARGLIST | 15 |
| sachbearbeiter_id | str | MIT-00008 | 4 |
| org_einheit_id | str | ORG-042 | 4 |
| geschaedigter_text | str | Dritte (Skifahrerin, Bern) | 1 |
| betrugsverdacht_sichtbar | str | KEIN | 0 |
| quellsystem | str | SILAS | 0 |
| ist_persona_fall | bool | True | 0 |

### curated/schaden_position



| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| position_id | str | SCH-00000110-01 | 0 |
| schaden_id | str | SCH-00000110 | 0 |
| art | str | RESERVE | 0 |
| betrag | float64 | 5000.0 | 0 |
| waehrung | str | CHF | 0 |
| datum | object | 2019-02-19 | 0 |
| empfaenger | str | Geschaedigte | 34 |
| beschreibung | str | Erstreserve Personenschaden leicht | 0 |

### curated/tarifgeneration

Bedingungs- und Tarifgenerationen mit Gueltigkeit

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| tarifgeneration_id | str | HP-KLASSIK | 0 |
| sparte | str | HP | 0 |
| bezeichnung | str | Pfefferminz Klassik | 0 |
| herkunft | str | pfefferminz | 0 |
| gueltig_ab | object | 2001-01-01 | 0 |
| gueltig_bis | object | 2012-12-31 | 2 |
| produkte | str | HP-PRIV;HP-BETR;HP-BERUF | 0 |
| maerkte | str | CH;DE | 0 |
| anteil_bestand_pct | float64 | 8.0 | 0 |

### curated/vermittler

Vermittlerpersonen mit Agenturzuordnung, Alt- und Neunummer

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| vermittler_id | str | VRM-00001 | 0 |
| agentur_id | str | AGT-0004 | 0 |
| vorname | str | Ralf | 0 |
| nachname | str | Möller | 0 |
| geschlecht | str | M | 0 |
| geburtsjahr | int64 | 1985 | 0 |
| markt | str | DE | 0 |
| kanal | str | direkt | 0 |
| vermittlernummer_alt | str | 80193 | 0 |
| vermittlernummer | str | 93662 | 0 |
| aktiv_seit | object | 2016-01-01 | 0 |
| aktiv_bis | object | 2019-12-31 | 38 |
| quellsystem | str | MINT | 0 |
| leistungsgewicht | float64 | 0.6614974773058789 | 0 |

### curated/vertrag

Vertraege beider Sparten mit Status, Praemie, Kanal, Quellsystem, Migrationsdatum

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| vertrag_id | str | VTR-00000101 | 0 |
| policennummer_anzeige | object |  | 1481 |
| produkt_id | str | HP-PRIV | 0 |
| sparte | str | HP | 0 |
| tarifgeneration_id | str | HP-MODERN | 0 |
| markt | str | CH | 0 |
| waehrung | str | CHF | 0 |
| versicherungsnehmer_id | str | PTR-00000001 | 0 |
| vermittler_id | str | VRM-00011 | 0 |
| kanal | str | agentur | 0 |
| sachbearbeiter_id | str | MIT-00008 | 0 |
| antrag_id | str | ANT-00000101 | 0 |
| beginn | object | 2016-03-01 | 0 |
| ablauf | object | 2032-05-01 | 910 |
| laufzeit_jahre | float64 | 13.0 | 910 |
| hauptfaelligkeit | object | 2016-03-01 | 0 |
| zahlungsweise | str | VIERTELJAEHRLICH | 0 |
| zahlungsart | str | LASTSCHRIFT | 0 |
| jahrespraemie_netto | float64 | 160.0 | 0 |
| jahrespraemie_brutto | float64 | 168.0 | 0 |
| einmalpraemie | float64 | 150000.0 | 1416 |
| versicherungssumme | float64 | 10000000.0 | 0 |
| status | str | AKTIV | 0 |
| status_seit | object | 2016-03-01 | 0 |
| storno_datum | object | 2021-03-24 | 1009 |
| storno_grund_code | str | K13 | 1009 |
| kuendigungsfrist_monate | float64 | 3.0 | 571 |
| naechste_kuendigungsmoeglichkeit | object | 2026-03-01 | 837 |
| risikoklasse_uw | str | NORMAL | 0 |
| mahnstufe_aktuell | int64 | 0 | 0 |
| herkunft | str | pfefferminz | 0 |
| quellsystem | str | HAPO | 0 |
| migriert_am | object | 2025-05-15 | 658 |
| erstellt_am | object | 2016-02-20 | 0 |
| bemerkung | str | Familie, Hund | 1459 |

### curated/vertrag_partner_rolle

Rollen der Partner am Vertrag: VN, mitversichert, versicherte Person, beguenstigt

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| vertrag_id | str | VTR-00000101 | 0 |
| partner_id | str | PTR-00000001 | 409 |
| rolle | str | VERSICHERUNGSNEHMER | 0 |
| anteil_pct | float64 | 50.0 | 2723 |

### migration/feld_mapping

Feldweise Abbildung Quellsystem -> curated mit Transformationsregeln und DQ-Bezug

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| ziel_tabelle | str | partner | 0 |
| ziel_feld | str | partner_id | 0 |
| quellsystem | str | HAPO | 0 |
| quell_tabelle | str | PARTNER | 0 |
| quell_feld | str | PARTNR | 0 |
| transformation | str | xref (Dedup ueber Name+Geburtsdatum+PLZ, | 0 |
| wertemapping | str |  | 0 |
| dq_regel | str | DQ-01;DQ-02 | 0 |
| bemerkung | str | Dubletten behalten match_score in partne | 0 |

### migration/migrationslog

Simuliertes Log der Migrationswellen 2025 (OK/WARN/ERROR)

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| welle | str | HP-2025-Q2 | 0 |
| objekttyp | str | PARTNER | 0 |
| quellsystem | str | HAPO | 0 |
| quell_id | str | 20000001 | 0 |
| ziel_id | str | PTR-00000001 | 0 |
| zeitpunkt | object | 2025-05-15 | 0 |
| ergebnis | str | OK | 0 |
| meldung | str | Partner uebernommen | 0 |

### migration/partner_xref

Kreuzreferenz Partner: curated-ID zu Quell-IDs in HAPO, VERA, MINT mit Match-Methode und Score

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| curated_id | str | PTR-00000001 | 0 |
| quellsystem | str | HAPO | 0 |
| quell_id | str | 20000001 | 0 |
| match_methode | str | MIGRATIONSLOG | 0 |
| match_score | float64 | 1.0 | 0 |
| gueltig_von | object | 2016-03-01 | 241 |
| gueltig_bis | object | 2025-05-15 | 768 |
| bemerkung | str |  | 0 |

### migration/vertrag_xref

Kreuzreferenz Vertraege: curated-ID zu Quell-IDs

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| curated_id | str | VTR-00000101 | 0 |
| quellsystem | str | HAPO | 0 |
| quell_id | str | 40.000.001-3 | 0 |
| match_methode | str | MIGRATIONSLOG | 0 |
| match_score | float64 | 1.0 | 0 |
| gueltig_von | object | 2016-03-01 | 0 |
| gueltig_bis | object | 2025-05-15 | 1481 |
| bemerkung | str | Migrationsstorno ZZ im Altsystem | 0 |

### truth/dq_injektionen

Protokoll aller injizierten Datenqualitaetsprobleme mit Originalwert (nur Dozenten)

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| quellsystem | str | HAPO | 0 |
| tabelle | str | PARTNER | 0 |
| quell_id | str | 20000002 | 0 |
| feld | str | ADR3 | 0 |
| dq_regel | str | DQ-27 | 0 |
| original | str | 5600 LENZBURG | 2 |
| injiziert | str | 5600 LENZBURX | 0 |

### truth/partner_latent

Latente Wahrheit je Partner: Kuendigungsneigung, Betrugsneigung, BMI, Raucher, Todesdatum (nur Dozenten)

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| partner_id | str | PTR-00000001 | 0 |
| kuendigungsneigung | float64 | 0.15 | 0 |
| betrugsneigung | float64 | 0.01 | 0 |
| preissensitivitaet | float64 | 0.4 | 0 |
| digitalaffinitaet | float64 | 0.3 | 0 |
| bmi | float64 | 23.0 | 62 |
| raucher | object | False | 62 |
| gesundheit_score | float64 | 0.85 | 62 |
| todesdatum | object | 2019-02-14 | 998 |
| hund | bool | False | 0 |

### truth/schaden_latent



| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| schaden_id | str | SCH-00000110 | 0 |
| betrug_wahr | bool | False | 0 |
| betrugsmuster | str | F7/F1/F2 | 12 |
| bemerkung | str | Persona-Fall, siehe docs/personas/kunden | 0 |

### truth/vertrag_latent

Latente Wahrheit je Vertrag: Tarifpraemie, Abweichung, Kuendigung in 12 Monaten, Bias-Anwendung (nur Dozenten)

| Spalte | Typ | Beispiel | Nullwerte |
|---|---|---|---|
| vertrag_id | str | VTR-00000101 | 0 |
| praemie_tarif_brutto | float64 | 188.79 | 0 |
| tarifabweichung_pct | float64 | -11.01 | 0 |
| kuendigt_in_12m | bool | False | 0 |
| kuendigungsgrund_latent | str | K13 | 891 |
| uw_entscheid | str | N | 0 |
| uw_zuschlag_pct | float64 | 0.0 | 0 |
| uw_bias_angewendet | bool | False | 0 |
| uw_automatisiert | bool | False | 0 |
| bmi_wahr | float64 | 23.0 | 131 |
| raucher_wahr | object | False | 131 |

## Rohdaten (raw)

| Datei | Beschreibung |
|---|---|
| data/documents/S/personas/PTR-00000001/DOK-00000101_beratungsprotokoll.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000001/DOK-00000102_beratungsprotokoll.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000001/DOK-00000103_kostenvoranschlag.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000001/DOK-00000104_schadenmeldung.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000001/INT-00000412_app.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000001/INT-00000413_chat.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000001/INT-00000414_chat.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000001/INT-00000415_app.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000001/INT-00000517_app.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000001/INT-00000518_app.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000002/DOK-00000201_antrag.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000002/DOK-00000202_rechnung.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000002/INT-00000201_chat.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000002/INT-00000202.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000002/INT-00000203.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000002/INT-00000230_chat.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000002/INT-00000241_chat.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000002/INT-00000255_chat.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000002/INT-00000262_chat.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000003/DOK-00000301_gutachten.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000003/DOK-00000302_korrespondenz.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000003/DOK-00000303_vergleich.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000003/DOK-00000304_aktennotiz.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000003/INT-00000318.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000003/INT-00000319_telefon.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000003/INT-00000325.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000003/INT-00000326.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000003/INT-00000340.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000004/DOK-00000401_betriebsbeschreibung.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000004/DOK-00000402_beratungsprotokoll.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000004/DOK-00000403_nachtrag.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000004/DOK-00000404_umsatzmeldung.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000004/INT-00000419.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000004/INT-00000420.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000004/INT-00000431_telefon.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000005/DOK-00000501_standmitteilung.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000005/DOK-00000502_ablaufabrechnung.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000005/DOK-00000503_offerte.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000005/DOK-00000504_schadenmeldung.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000005/INT-00000501_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000005/INT-00000502_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000005/INT-00000505_telefon.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000005/INT-00000512_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000005/INT-00000513_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000006/DOK-00000601_antrag.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000006/DOK-00000602_arztbericht.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000006/DOK-00000603_gegenofferte.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000006/DOK-00000604_erklaerungsschreiben.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000006/INT-00000631.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000006/INT-00000632.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000006/INT-00000633.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000006/INT-00000640.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000006/INT-00000641.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000007/DOK-00000701_beratungsprotokoll.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000007/DOK-00000702_kuendigungsbestaetigung.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000007/INT-00000701_chat.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000007/INT-00000705_chat.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000007/INT-00000706_telefon.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000007/INT-00000709_app.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000007/INT-00000714.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000007/INT-00000715.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000007/INT-00000720_app.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000007/INT-00000721_chat.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/DOK-00000801_nachtrag.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/DOK-00000802_beratungsprotokoll.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/DOK-00000803_arztrechnung.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/DOK-00000804_memo.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/DOK-00000805_aufsichtskorrespondenz.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/INT-00000801_telefon.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/INT-00000802_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/INT-00000803_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/INT-00000804.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/INT-00000805_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/INT-00000806.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/INT-00000807.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/INT-00000808_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/INT-00000809_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/INT-00000811_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/INT-00000823_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000008/INT-00000824_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000009/DOK-00000901_rechnung.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000009/DOK-00000902_rechnung.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000009/DOK-00000903_foto.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000009/DOK-00000904_betrugspruefungsbericht.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000009/INT-00000918_portal.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000009/INT-00000919.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000009/INT-00000925_telefon.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000009/INT-00000930_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000009/INT-00000931_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000009/INT-00000932_brief.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000010/DOK-00001001_formular_mittelherkunft.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000010/DOK-00001002_aktennotiz.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000010/DOK-00001003_beratungsprotokoll.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000010/DOK-00001004_rueckkaufstabelle.md | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000010/INT-00001001.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000010/INT-00001004.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000010/INT-00001005.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000010/INT-00001010.eml | ; JSON Lines, UTF-8 |
| data/documents/S/personas/PTR-00000010/INT-00001012.eml | ; JSON Lines, UTF-8 |
| data/raw/S/mint/customers.jsonl | MINT-Kunden als JSON Lines (Schema v1 bis v3); JSON Lines, UTF-8 |
| data/raw/S/mint/policies.jsonl | MINT-Policen als JSON Lines; JSON Lines, UTF-8 |
| data/raw/S/pvs/HAPO_PARTNER.csv | Partnerstamm Haftpflicht-Altsystem HAPO; Semikolon-CSV, ISO-8859-1, Datum DD.MM.YY |
| data/raw/S/pvs/HAPO_PARTNER.txt | Partnerstamm Haftpflicht-Altsystem HAPO; Fixed-width, ISO-8859-1 |
| data/raw/S/pvs/HAPO_PARTNER_SATZART.txt | Partnerstamm Haftpflicht-Altsystem HAPO; Satzartbeschreibung (Feldpositionen) |
| data/raw/S/pvs/HAPO_VERTRAG.csv | Vertraege HAPO; Semikolon-CSV, ISO-8859-1, Datum DD.MM.YY |
| data/raw/S/pvs/HAPO_VERTRAG.txt | Vertraege HAPO; Fixed-width, ISO-8859-1 |
| data/raw/S/pvs/HAPO_VERTRAG_SATZART.txt | Vertraege HAPO; Satzartbeschreibung (Feldpositionen) |
| data/raw/S/pvs/VERA_PARTNER.csv | Partnerstamm Leben-Altsystem VERA; Semikolon-CSV, ISO-8859-1, Datum DD.MM.YY |
| data/raw/S/pvs/VERA_PARTNER.txt | Partnerstamm Leben-Altsystem VERA; Fixed-width, ISO-8859-1 |
| data/raw/S/pvs/VERA_PARTNER_SATZART.txt | Partnerstamm Leben-Altsystem VERA; Satzartbeschreibung (Feldpositionen) |
| data/raw/S/pvs/VERA_VERTRAG.csv | Vertraege VERA; Semikolon-CSV, ISO-8859-1, Datum DD.MM.YY |
| data/raw/S/pvs/VERA_VERTRAG.txt | Vertraege VERA; Fixed-width, ISO-8859-1 |
| data/raw/S/pvs/VERA_VERTRAG_SATZART.txt | Vertraege VERA; Satzartbeschreibung (Feldpositionen) |
