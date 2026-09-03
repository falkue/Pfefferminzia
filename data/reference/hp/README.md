# Referenzdaten Haftpflicht (HP)

Stammdaten und Parameter der Haftpflichtsparte, aus denen der Generator Verträge, Schäden und Dokumente ableitet. Fachliche Quelle: `docs/planung/01-haftpflicht.md`. Erläuterung für Dozenten: `docs/stammdaten/haftpflicht.md`.

Konventionen: CSV in UTF-8 mit Komma und Kopfzeile, Dezimalpunkt, Beträge in Landeswährung mit eigener Spalte `waehrung` oder klarer Spaltenbezeichnung. Listen innerhalb einer Zelle sind mit Semikolon getrennt. Produkte: `HP-PRIV`, `HP-BETR`, `HP-BERUF`. Generationen: `HP-KLASSIK`, `HP-MODERN`, `MZ-DIRECT`, `PM-2025`. Märkte: `CH`, `DE`.

Fünf Dateien werden durch `scripts/build_reference_hp.py` erzeugt (branchenklassen, plz_zonen, schadenarten, dokumenttypen, lebenszyklus_raten); alle anderen sind handgepflegt.

## Übersicht

| Datei | Inhalt | Zeilen | Quelle |
|---|---|---|---|
| produkte.csv | Die drei Produkte mit Marktnamen, Zielgruppe, Einführungsjahren, Systemcodes | 3 | Planung 01 §2 |
| tarifgenerationen.csv | Vier Bedingungsgenerationen mit Gültigkeit, Bedingungswerk-IDs, Kernunterschieden | 4 | §2.5 |
| bausteine.csv | 15 Bausteine mit Sublimits, Zusatzprämien, Verfügbarkeit je Generation | 15 | §2.2 bis 2.4 |
| deckungssummen.csv | Wählbare Deckungssummen je Produkt, Markt und Deckungsart mit Bestandsanteil | 36 | §2 |
| selbstbehalte.csv | Selbstbehalt-Optionen je Produkt und Markt mit Bestandsanteil | 23 | §2 |
| branchenklassen.csv | 87 Branchen (NACE 4-stellig) mit Risikoklasse, Prämiensatz, Zeichnungsstatus | 87 | §2.3, §7.3 |
| berufsgruppen.csv | Vier Berufsgruppen je Markt mit Pflichtversicherung, Mindestdeckung, Sätzen | 8 | §2.4 |
| plz_zonen.csv | Tarifzonen 1 bis 3 je Markt mit Faktoren je Produkt | 6 | §7.5 |
| tarifparameter.yaml | Tarifformel-Parameter je Produkt, Markt, Generation | – | §7.5 |
| tarifformel.md | Erläuterung der Formel mit fünf Beispielen | – | §7.5 |
| schadenarten.csv | 14 Schadenarten je Produkt und Markt mit Anteil, Lognormal-Parametern, Saisonalität | 46 | §4.4 |
| schadenfrequenzen.csv | Jahresschadenfrequenz je Produkt, Personenkreis, Risikoklasse, Berufsgruppe | 23 | §4.4.2 |
| status_codes.csv | Vertrags- und Schadenstatus mit HAPO-, SILAS- und MINT-Codes | ca. 30 | §3.3, §4.3 |
| ablehnungsgruende.csv | Deckungs- und Haftungsablehnungsgründe mit Texten und Bedingungsverweisen je Generation | ca. 30 | §4.2 |
| betrugsmuster.csv | Neun Betrugsmuster F1 bis F9 mit Anteilen, Signalen, Dokumenttypen | 9 | §4.5 |
| dokumenttypen.csv | 49 Dokumenttypen (22 Vertrag, 27 Schaden) mit Format, Umfang, Menge | 49 | §5 |
| vollmachtsstufen.csv | Fünf Kompetenzstufen 0 bis 4 mit Betragsgrenzen | 5 | §7.6 |
| lebenszyklus_raten.csv | Jahresraten je Produkt, Markt, Kanal, Herkunft und Jahr 2016 bis 2025 | 250 | §3.4 |

## Spaltenbeschreibungen

### produkte.csv

| Spalte | Beschreibung |
|---|---|
| kuerzel | Produktkürzel |
| marktname | Verkaufsname (PrivatPlus, BusinessProtect, ProfessionalShield) |
| sparte | HP |
| bezeichnung_de_ch, bezeichnung_de_de | Fachbezeichnung je Sprachvariante |
| zielgruppe | Freitext |
| maerkte | CH;DE |
| einfuehrungsjahr_ch, einfuehrungsjahr_de | Jahr des Marktstarts |
| status | aktiv |
| tarifgenerationen | Verfügbare Generationen |
| alt_kuerzel_planung | Kürzel aus Planung 01 (PHV, BHV, BeHV) |
| hapo_sparte_code, mint_product_code | Codes in den Quellsystemen |
| charakter_datensatz | Rolle im Lehrdatensatz |

### tarifgenerationen.csv

| Spalte | Beschreibung |
|---|---|
| kuerzel, bezeichnung, herkunft | Generation, Name, Pfefferminz oder Minzia |
| gueltig_ab, gueltig_bis | Zeitraum für Neugeschäft |
| neugeschaeft_ausnahme_bis | Verlängerte Neugeschäftsphase für einzelne Kanäle |
| produkte, maerkte | Verfügbarkeit |
| bedingungswerk_ch, bedingungswerk_de | Regelwerk-IDs (RW-HP-AVB-CH-…, RW-HP-AHB-DE-…) |
| revisionen | Zwischenrevisionen innerhalb der Generation |
| tarifhandbuch_version | TH-Version |
| anteil_bestand_pct | Anteil am Stichtagsbestand |
| quellsystem_primaer | HAPO oder MINT |
| kernunterschiede | Fachliche Abweichungen, Grundlage für AVB-Versionskonflikte in RAG-Übungen |

### bausteine.csv

| Spalte | Beschreibung |
|---|---|
| kuerzel, name_de_ch, name_de_de | Baustein |
| produkte, maerkte | Verfügbarkeit |
| standard_inkludiert_ch, standard_inkludiert_de | ja, wenn im Grundtarif enthalten |
| sublimit_regel, sublimit_betrag_ch, sublimit_betrag_de | Begrenzung innerhalb der Deckungssumme |
| zusatzpraemie_regel, zusatzpraemie_typ | fix_pro_tier, fix, prozent |
| zusatzpraemie_ch, zusatzpraemie_de | Betrag in Landeswährung oder Prozent |
| zusatzpraemie_variante_ch, zusatzpraemie_variante_de | Varianten wie Listenhund |
| ab_generation_ch, ab_generation_de, bis_generation | Verfügbarkeit nach Generation |
| anteil_vertraege_ch_pct, anteil_vertraege_de_pct | Anteil der Verträge mit diesem Baustein |
| alt_code_planung, hapo_code, mint_code | Codes; HAPO führt Bausteine teils in überladenen Feldern |
| bemerkung | Hinweise auf Datenqualitätsregeln |

### deckungssummen.csv und selbstbehalte.csv

| Spalte | Beschreibung |
|---|---|
| produkt, markt | |
| deckungsart | personen_sach oder vermoegen (nur deckungssummen) |
| selbstbehalt_typ | fix oder prozent_min (nur selbstbehalte) |
| betrag, waehrung | Betrag in Landeswährung |
| prozent, minimum | Nur bei prozent_min |
| standard | ja bei Standardoption |
| generationen | Verfügbarkeit |
| anteil_bestand_pct | Anteil im Bestand |
| gilt_fuer, bemerkung | |

### branchenklassen.csv

| Spalte | Beschreibung |
|---|---|
| branche_id | BK-001 bis BK-087 |
| bezeichnung_de | |
| noga_code, wz_code | 4-stelliger Code; NOGA 2008 und WZ 2008 beruhen auf NACE Rev. 2 und sind auf dieser Ebene identisch |
| risikoklasse | 1 gering bis 5 hoch |
| grundpraemiensatz_promille | Prämiensatz auf Umsatz (DE-Basis); CH-Sätze auf Lohnsumme in tarifparameter.yaml |
| zeichnungsstatus | annehmbar, zuschlag, referat, abgelehnt |
| anteil_bestand_pct | Anteil am Betriebshaftpflicht-Bestand, Summe rund 100 |
| bemerkung | Zeichnungshinweise |

Konkretisierung: Planung 01 nennt Risikoklassen 1 bis 6; die Stammdaten verwenden durchgängig 1 bis 5, weil schadenfrequenzen.csv und vollmachtsstufen.csv bereits darauf aufbauen.

### berufsgruppen.csv

| Spalte | Beschreibung |
|---|---|
| kuerzel, markt, bezeichnung, untergruppen | BG-ARCH, BG-TREU, BG-IT, BG-BER je Markt |
| pflichtversicherung, rechtsgrundlage_pflicht | Vereinfachte Angabe, zu verifizieren |
| mindestdeckung_vermoegen, mindestdeckung_personen, mindestdeckung_sach, waehrung | |
| praemiensatz_promille, bemessungsgrundlage, untergruppen_saetze_promille | Satz auf Honorar- oder Umsatzsumme |
| grundpraemie_min | Mindestprämie |
| deckungsprinzip_standard | verstoss oder claims_made |
| nachhaftung_jahre, nachmeldefrist_jahre | |
| taetigkeitszuschlaege | Zuschläge in Prozent je Tätigkeit |
| schadenfrequenz_pct, nullschaden_anteil_pct, anteil_bestand_pct | |
| verband_fiktiv, bemerkung | |

### plz_zonen.csv

| Spalte | Beschreibung |
|---|---|
| markt, tarifzone | Zone 1 bis 3; Zuordnung Ort zu Zone in data/reference/geo/orte_*.csv |
| bezeichnung, begruendung | |
| faktor_hp_priv, faktor_hp_betr, faktor_hp_beruf | Multiplikativer Regionalfaktor |

### schadenarten.csv

| Spalte | Beschreibung |
|---|---|
| schadenart_id, bezeichnung | 14 Schadenarten |
| produkt, markt | Eine Zeile je Kombination |
| anteil_pct | Anteil an der Schadenanzahl des Produkts, Summe je Produkt und Markt rund 100 |
| waehrung | CHF oder EUR |
| lognormal_mu, lognormal_sigma | Parameter der Lognormalverteilung des positiven Gesamtaufwands (inkl. Kosten); nominal für CHF und EUR gleich |
| nullschaden_anteil_pct | Gemeldet, aber ohne Zahlung |
| abwehrquote_pct | Ansprüche vollständig abgewehrt |
| abwicklungsdauer_median_tage, abwicklungsdauer_p90_tage | Meldung bis Schliessung |
| saison_jan bis saison_dez | Monatsfaktoren, Mittel 1.0 |

Die Zeile SA-SCHLUESSEL trägt Anteil 0, weil Schlüsselverlust in Planung 01 in den Immobilienschäden enthalten ist; sie liefert nur die Verteilung für das Sublimit.

### schadenfrequenzen.csv

| Spalte | Beschreibung |
|---|---|
| produkt, markt | |
| personenkreis | einzel, paar, familie (HP-PRIV) |
| risikoklasse | 1 bis 5 (HP-BETR) |
| berufsgruppe | BG-… (HP-BERUF) |
| frequenz_pct | Gemeldete Schäden je Vertrag und Jahr |
| zuschlag_hund_prozentpunkte | Zusätzliche Frequenz bei Hundehaltung |

### status_codes.csv

| Spalte | Beschreibung |
|---|---|
| entitaet | vertrag oder schaden |
| code, hauptstatus, bezeichnung, beschreibung, folgestatus | Curated-Status und Übergänge |
| curated_status_planung03 | Bezeichnung in Planung 03 |
| hapo_status, hapo_stornogrund, silas_stat | Legacy-Codes, teils kryptisch und undokumentiert (bewusst, siehe Datenqualitätsregeln) |
| mint_v1, mint_v2, mint_v3_lifecycle_state | MINT-Codes je Schema-Version (Schema-Drift) |

### ablehnungsgruende.csv

| Spalte | Beschreibung |
|---|---|
| typ | deckung oder haftung |
| kuerzel, bezeichnung | |
| text_de_ch, text_de_de | Textbaustein für Ablehnungsschreiben |
| rechtsgrundlage_ch, rechtsgrundlage_de | Vereinfacht |
| avb_ref_ch_<Generation>, ahb_ref_de_<Generation> | Verweis auf die Bedingungsziffer je Generation; unterschiedliche Ziffern sind gewollt (RAG-Übung) |
| bemerkung | Zuordnung zu Stolpersteinen |

### betrugsmuster.csv

| Spalte | Beschreibung |
|---|---|
| kuerzel, name, beschreibung | F1 bis F9 |
| produkte | Betroffene Produkte |
| anteil_an_betrugsfaellen_pct | Verteilung innerhalb der Betrugsfälle |
| anteil_an_schaeden_hp_priv_pct, …_betr_pct, …_beruf_pct | Anteil an allen Schäden des Produkts |
| bestaetigungsquote_pct | Anteil der Verdachtsfälle, die sich bestätigen |
| signale_strukturiert, detailcodes_betrugsindikatoren | Feldnamen und Indikatorcodes für Features |
| signale_dokumente, dokumenttypen | Hinweise in Dokumenten |
| erkennungsschwierigkeit, erkennungsschwierigkeit_score | leicht bis sehr schwer, 1 bis 5 |
| typische_schadenarten, bemerkung | |

### dokumenttypen.csv

| Spalte | Beschreibung |
|---|---|
| code | V01 bis V22, S01 bis S27 |
| name, bereich, phase | Vertrag oder Schaden, Prozessphase |
| format | pdf, scan, eml, json, txt, docx, jpg, xlsx |
| laenge_seiten_typisch | Spanne |
| anzahl_pro_1000 | Dokumente je 1'000 Verträge (Vertrag) bzw. 1'000 Schäden (Schaden) |
| sprache | Mögliche Sprachvarianten |
| quellsystem | HAPO, SILAS, DOKU, MINT |
| ground_truth_json | true, wenn für einen Teil der Dokumente extrahierte Sollwerte mitgeliefert werden |

### vollmachtsstufen.csv

| Spalte | Beschreibung |
|---|---|
| stufe, rolle, rolle_kurz | 0 Automatik bis 4 Geschäftsleitung |
| uw_kompetenz, tarifabweichung_max_pct, risikoklasse_max, zeichnungsstatus_max | Zeichnungskompetenz |
| zahlung_max, reserve_max, vergleich_max, kulanz_max | Betragsgrenzen je Stufe, nominal für CHF und EUR |
| vier_augen_ab | Betrag, ab dem Vier-Augen-Prinzip gilt |
| deckungsablehnung, anwaltsbeauftragung, detektiveinsatz, strafanzeige | Zulässige Entscheidungen |
| besonderes | Regeln, darunter: Ablehnungen nie automatisch |

Im Datensatz verletzen 1 bis 2 Prozent der Zahlungen die Vollmachtsstufe (Audit-Übung).

### lebenszyklus_raten.csv

| Spalte | Beschreibung |
|---|---|
| produkt, markt, kanal | Kanal: agentur, makler, direkt, bank |
| herkunft | alle (bis 2020), pfefferminz oder minzia (ab 2021); Minzia nur HP-PRIV im Direktkanal |
| jahr | 2016 bis 2025 |
| neugeschaeft_rate_pct | Neugeschäft in Prozent des Bestands |
| storno_rate_pct | Kündigung durch Kunden in Prozent des Bestands; 2025 Fusionseffekt bei Ex-Pfefferminz-Kunden |
| nachtrag_rate | Nachträge je Vertrag und Jahr |
| mahn_rate_pct | Anteil Verträge mit mindestens Mahnstufe 1 |
| kuendigung_vu_rate_pct | Kündigung durch den Versicherer |
| bemerkung | |

## Konkretisierte Spannen

Wo Planung 01 Spannen nennt, wurden feste Werte gewählt: Neugeschäft Privat 10 Prozent, Betrieb und Beruf 12.5 Prozent; Storno Privat CH 6, DE 11 Prozent, Betrieb und Beruf 10 Prozent; Mahnquote Privat 7.5, Betrieb 10, Beruf 5 Prozent. Kanalfaktoren und Jahrestrend sind im Erzeugungsskript dokumentiert. Grundprämien und Faktoren in tarifparameter.yaml liegen innerhalb der Richtwerte aus Planung 01 §2.
