# Referenzdaten Leben (LV)

Stammdaten und Parameter der Lebensversicherungssparte, aus denen der Generator Verträge, Risikoprüfungen, Leistungsfälle und Dokumente ableitet. Fachliche Quelle: `docs/planung/02-leben.md`. Erläuterung für Dozenten: `docs/stammdaten/leben.md`.

Konventionen: CSV in UTF-8 mit Komma und Kopfzeile, Dezimalpunkt, Listen innerhalb einer Zelle mit Semikolon. Produkte: `LV-RISK`, `LV-VORS`, `LV-RENTE`, `LV-EU`. Generationen: `PK-85`, `PK-95`, `PK-2000`, `PK-2004`, `PK-2007`, `PL-2012`, `PL-2015`, `PL-2017`, `MZ-2020`, `PZ-2025`. Märkte: `CH`, `DE`.

Drei Dateien werden durch `scripts/build_reference_lv.py` erzeugt (sterbetafel, ueberschuss_parameter, lebenszyklus_raten); alle anderen sind handgepflegt.

## Hinweis zur Sensibilität der Gesundheitsdaten

Die Diagnose-Bibliothek und die Gesundheitsfragen enthalten medizinische Begriffe auf ICD-10-Gruppenebene. Alle späteren Zuordnungen zu Personen sind synthetisch: Der Generator zieht Diagnosen unabhängig von Name, Adresse und Geburtsdatum, es existiert keine reale Person hinter einem Datensatz. Trotzdem gelten die Daten im Seminar als Beispiel für besondere Kategorien personenbezogener Daten (Art. 9 DSGVO, Art. 5 DSG). Tabellen mit Gesundheitsangaben tragen in der Ausgabe das Flag `sensitiv = true` und dürfen nicht mit den Kommunikationsdaten in ein öffentliches Modell geladen werden. Das ist Gegenstand des Use Case UC-18.

## Übersicht

| Datei | Inhalt | Zeilen | Quelle |
|---|---|---|---|
| produkte.csv | Vier Produkte je Markt mit Neugeschäfts- und Altbestandsstatus | 8 | Planung 02 §1 |
| tarifgenerationen.csv | Zehn Generationen mit Rechnungszins, Tafel, Unisex, Bedingungswerk, Rückkaufmethode, Zillmerung, Fragebogenversion | 10 | §1.3 |
| versicherungssummen.csv | Wertebereiche und Bestandsanteile der Summen und Renten je Produkt und Markt | 42 | §1.2 |
| laufzeiten.csv | Laufzeiten, Eintritts- und Endalter, Bestandsanteile | 36 | §1.2 |
| sterbetafel.csv | Drei vereinfachte Tafeln T1985, T2004, T2020, Alter 18 bis 85 | 204 | §6.2 |
| tarifparameter.yaml | Kosten, Risikofaktoren, Unisex-Regeln, produktspezifische Parameter | – | §1.2, §6.2 |
| tarifformel.md | Formel mit drei Beispielen | – | §6.2 |
| gesundheitsfragen.csv | Gesundheitsfragebogen in fünf Versionen GF-1985 bis GF-2025 | 82 | §5.5 |
| diagnose_bibliothek.csv | 115 Diagnosen auf ICD-10-Gruppenebene mit Underwriting-Wirkung und Freitextvarianten | 115 | §6.3 |
| annahmerichtlinie_tabellen.yaml | Prüfumfang, BMI, Rauchen, Berufsgruppen, Freizeit, regionale und herkunftsbezogene Faktoren mit Bias-Markierung, Kompetenzen | – | §6.3 |
| underwriting_entscheidungen.csv | Entscheidungscodes mit VERA- und MINT-Codes und Zielanteilen je Generation und Markt | 120 | §2.3 |
| status_codes.csv | Antrags-, Vertrags- und Leistungsfallstatus mit VERA-, MINT- und SILAS-Codes | 34 | §5.2 |
| leistungsarten.csv | Tod, EU/BU, Erleben, Rückkauf, Rentenbeginn mit Nachweisen und Durchlaufzeiten | 12 | §3 |
| betrugsmuster.csv | Acht Betrugsmuster mit Signalen und False-Positive-Zwillingen | 8 | §3.5 |
| kulanzfaelle.csv | Sechs Kulanzkonstellationen mit Regelungslage CH/DE | 6 | §3.6 |
| ueberschuss_parameter.csv | Gesamtverzinsung, Zins-, Risiko- und Schlussüberschuss je Generation, Markt, Jahr 2016 bis 2025 | 171 | §6.5 |
| rueckkauf_parameter.yaml | Rückkaufmethode, Zillmerung, Stornoabzug, Tabellen für Altgenerationen | – | §1.2, §6.2 |
| dokumenttypen.csv | 42 Dokumenttypen mit Format, Umfang, Mengen, Gesundheitsdaten-Flag | 42 | §4 |
| lebenszyklus_raten.csv | Jahresraten je Produkt, Markt, Kanal, Herkunft und Jahr 2016 bis 2025 | 344 | §2, §8 |

## Spaltenbeschreibungen

### produkte.csv

| Spalte | Beschreibung |
|---|---|
| produkt_code, marktname, marktname_lokal, produkt_typ | RISIKO, GEMISCHT, RENTE, ZUSATZ |
| zielgruppe, markt, waehrung | |
| neugeschaeft, neugeschaeft_von, neugeschaeft_bis | JA/NEIN; LV-VORS in DE nur Altbestand (Entscheidung E05) |
| altbestand, altbestand_marke | Bezeichnung der Altmarke (z. B. Pfefferminz Kapital) |
| einfuehrungsjahr, status, bestandsanteil_pct | |
| primaerer_use_case, bemerkung | |

### tarifgenerationen.csv

| Spalte | Beschreibung |
|---|---|
| generation_code, bezeichnung, gueltig_ab, gueltig_bis, herkunft, produkte | |
| rechnungszins_de_pct, rechnungszins_de_ab_2022_pct | Höchstrechnungszins DE, historisch korrekt; PL-2017 wechselt 2022 auf 0.25 |
| technischer_zins_ch_pct | Technischer Zins CH |
| sterbetafel_de, sterbetafel_ch | Fiktive Tafelbezeichnungen (angelehnt an marktübliche Systematik) |
| sterbetafel_vereinfacht | T1985, T2004, T2020: Schlüssel zu sterbetafel.csv |
| unisex_de, unisex_de_ab, unisex_ch | Unisex-Regel; DE ab 2012-12-21 |
| bedingungswerk_id_ch, bedingungswerk_id_de | RW-LV-AVB-… |
| suizidfrist_jahre_ch, suizidfrist_jahre_de | 1 Jahr in Altgenerationen, 3 Jahre ab PL-2012 |
| flugrisiko_ausschluss, nachversicherungsgarantie | JA/NEIN |
| rueckkauf_methode | TABELLE, FORMEL, ENTFAELLT |
| zillmerung | VOLL_JAHR1, VERTEILT_5J, KEINE |
| verweisung_bu | ABSTRAKT, ABSTRAKT_BIS_2008, KONKRET |
| annahmerichtlinie_version, antragsformular_generation, gesundheitsfragebogen_version | ARL-…, F…, GF-… |
| bestandsanteil_pct, vera_tarifcode, mint_tarifcode, kernunterschiede_bemerkung | |

### versicherungssummen.csv und laufzeiten.csv

| Spalte | Beschreibung |
|---|---|
| produkt_code, markt, waehrung | |
| groesse | VERSICHERUNGSSUMME_TOD, ERLEBENSFALLSUMME, JAHRESRENTE, EU_RENTE_MONAT, EINMALPRAEMIE |
| minimum, maximum, klasse_von, klasse_bis, bestandsanteil_pct | Klassen für die Ziehung |
| typisch, typisch_von, typisch_bis | Kennzeichnung der typischen Klasse |
| laufzeit_min_jahre, laufzeit_max_jahre, eintrittsalter_min, eintrittsalter_max, endalter_max, endalter_max_altbestand | nur laufzeiten.csv |

### sterbetafel.csv

| Spalte | Beschreibung |
|---|---|
| tafel | T1985, T2004, T2020 |
| alter | 18 bis 85 |
| qx_m, qx_w, qx_unisex | Jahres-Sterbewahrscheinlichkeit Mann, Frau, Unisex (Mittel); Gompertz-Makeham, monoton steigend, neuere Tafel tiefer |
| beschreibung | Zugehörige Generationen |

### gesundheitsfragen.csv

| Spalte | Beschreibung |
|---|---|
| frage_id, fragebogen_version, generationen, reihenfolge | |
| frage_text | Wortlaut; ältere Versionen kürzer und anders formuliert |
| antworttyp | JA_NEIN, ZAHL, FREITEXT, AUSWAHL |
| freitext_bei_antwort | Ob bei JA ein Freitext folgt (Entscheidung E09) |
| zeitraum_jahre, themenbereich, icd10_kapitel_bezug | |
| aequivalent_gf_2025 | Zuordnung zur aktuellen Fragebogenversion (Generationen-Mapping) |
| hinweis | |

### diagnose_bibliothek.csv

| Spalte | Beschreibung |
|---|---|
| diagnose_code, icd10_gruppe, icd10_kapitel, bezeichnung_de | Gruppenebene, keine Einzelcodes |
| schweregrad | 1 bis 3 |
| haeufigkeit_antragspopulation_pct, altersschwerpunkt | Ziehungsgewicht |
| uw_wirkung_tod, zuschlag_tod_pct, zuschlag_tod_promille | NORMAL, ZUSCHLAG, AUSSCHLUSS, ZURUECKSTELLUNG, ABLEHNUNG |
| uw_wirkung_eu_bu, zuschlag_eu_bu_pct, ausschluss_code_eu_bu | |
| zurueckstellung_monate, nachweis | |
| freitext_variante_1, freitext_variante_2, freitext_variante_3_tippfehler | Formulierungen, wie Antragsteller schreiben, inkl. Tippfehler |
| relevanz_eu_bu, arl_abweichung_hinweis | Abweichende Bewertung in älteren Richtlinien (z. B. HIV vor ARL-2015) |
| leistungsursache_kategorie, medikation_beispiel | |

### underwriting_entscheidungen.csv

| Spalte | Beschreibung |
|---|---|
| entscheid_code | N normal, Z Zuschlag, A Ausschluss, R Zurückstellung, X Ablehnung |
| bezeichnung, vera_code, mint_code | Codes je System |
| generation_code, markt | Eine Zeile je Kombination |
| zielanteil_pct | Anteil der Entscheidungen |
| automatisierungsquote_pct | Anteil automatischer Entscheide (nur positive, siehe annahmerichtlinie_tabellen.yaml) |
| beschreibung, bemerkung | |

### status_codes.csv

| Spalte | Beschreibung |
|---|---|
| status_typ | ANTRAG, VERTRAG, LEISTUNGSFALL |
| status_code, bezeichnung_de | |
| vera_code, vera_stornogrund, mint_code_v1, mint_code_v2, silas_code | Codes je System und Schema-Version |
| endstatus, zaehlt_als_churn | JA/NEIN |
| beschreibung | |

### leistungsarten.csv

| Spalte | Beschreibung |
|---|---|
| leistungsart_code, bezeichnung_de, produkte, maerkte | TOD, EU_BU, ERLEBEN, RUECKKAUF, RENTENBEGINN mit Fallvarianten |
| fallvariante, ausloeser | STANDARD, FRUEH (unter 3 bzw. 5 Jahren), AUSLAND, VERSCHOLLEN … |
| nachweise_dokumenttypen | Codes aus dokumenttypen.csv |
| durchlaufzeit_median_tage, durchlaufzeit_p90_tage, langlaeufer_anteil_pct | |
| anteil_basis, anteil_pct | Bezugsgrösse und Anteil |
| silas_code, mint_code, bemerkung | |

### betrugsmuster.csv und kulanzfaelle.csv

| Spalte | Beschreibung |
|---|---|
| muster_code bzw. kulanz_code, bezeichnung, beschreibung | |
| produkte, leistungsarten | Betroffene Bereiche |
| anteil_basis, anteil_pct | Anteil an der Bezugsgrösse |
| signale | Feldnamen und Dokumentmerkmale |
| schwierigkeit | leicht bis sehr schwer |
| false_positive_zwilling | Legitimer Fall mit denselben Signalen (nur betrugsmuster) |
| aufdeckungsquote_pct, label_bias_hinweis | Sichtbare Labels sind unvollständig (nur betrugsmuster) |
| regelungslage_ch, regelungslage_de, typische_entscheidung, kulanzstufe, entscheid_grund_code, stolperstein_ref | nur kulanzfaelle |

### ueberschuss_parameter.csv

| Spalte | Beschreibung |
|---|---|
| generation_code, markt, jahr | 2016 bis 2025, nur Jahre nach Einführung der Generation |
| rechnungszins_pct | Garantierter Zins der Generation im Jahr |
| gesamtverzinsung_pct | Deklarierte Gesamtverzinsung (2025: DE 2.6, CH 2.0) |
| zinsueberschuss_pct | max(0, Gesamtverzinsung − Rechnungszins); null bei Hochzinsgenerationen |
| risikoueberschuss_pct | Prozent der Risikoprämie (Prämienrabatt Risikoleben) |
| schlussueberschuss_pct | Prozent des Deckungskapitals bei Ablauf |
| kommentar | |

### dokumenttypen.csv

| Spalte | Beschreibung |
|---|---|
| dokumenttyp_code, name, phase | D01 bis D42 |
| formate, umfang_seiten_min, umfang_seiten_max | |
| anzahl_pro_1000_vertraege, anzahl_pro_1000_leistungsfaelle | Mengengerüst |
| sprache_varianten, quellsystem | VERA, SILAS, DOKU, MINT |
| gesundheitsdaten | JA, wenn das Dokument Gesundheitsangaben enthält |
| layout_generationen | Unterschiedliche Layouts je Generation (Scans, Handschrift) |
| bemerkung | |

### lebenszyklus_raten.csv

| Spalte | Beschreibung |
|---|---|
| produkt_code, markt, kanal, herkunft | Kanal agentur, makler, direkt, bank; Herkunft alle (bis 2019), pfefferminz oder minzia (ab 2020, Minzia nur LV-RISK und LV-EU im Direktkanal) |
| jahr | 2016 bis 2025 |
| neugeschaeft_rate_pct | Neugeschäft in Prozent des Bestands; LV-VORS DE null |
| storno_rueckkauf_rate_pct | Kündigung und Rückkauf; 2023 Zinsanstieg, 2025 Fusionseffekt |
| beitragsfrei_rate_pct | Beitragsfreistellungen |
| dynamik_annahme_rate_pct | Anteil angenommener Dynamikerhöhungen, sinkend |
| leistungsfall_rate_pct | Leistungsfälle inkl. Erleben |
| bemerkung | |

## Konkretisierte Spannen

Wo Planung 02 Spannen nennt, wurden feste Werte gewählt und dokumentiert: Raucherfaktor 2.0 auf die Risikoprämie; Risikoüberschuss 30 Prozent DE und 25 Prozent CH; Gesamtverzinsung als Zeitreihe mit Tief 2022 und Anstieg ab 2024; Stornoabzug 5 Prozent (PK-2007) fallend auf 2 Prozent (PZ-2025); Abschlusskosten 40 Promille in Altgenerationen, 8 Promille bei Minzia. Die Rückkaufstabellen der Generationen PK-85 bis PK-2004 sind Setzungen, die die Zillmerung im ersten Jahr abbilden.
