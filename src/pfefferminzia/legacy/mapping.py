"""Stufe-Hilfsdaten: statische Feldmapping-Tabelle Quellsystem -> curated (Datenarchitektur 2.3a)."""

from __future__ import annotations

import pandas as pd

SPALTEN = ["ziel_tabelle", "ziel_feld", "quellsystem", "quell_tabelle", "quell_feld", "transformation", "wertemapping", "dq_regel", "bemerkung"]

FELD_MAPPING = [
    ("partner", "partner_id", "HAPO", "PARTNER", "PARTNR", "xref (Dedup ueber Name+Geburtsdatum+PLZ, Score >= 0.85)", "", "DQ-01;DQ-02", "Dubletten behalten match_score in partner_xref"),
    ("partner", "partner_id", "VERA", "PARTNER", "PARTNR", "xref (Dedup ueber Name+Geburtsdatum+PLZ, Score >= 0.85)", "", "DQ-01;DQ-02", "eigener Nummernkreis, Kollision mit HAPO moeglich"),
    ("partner", "partner_id", "MINT", "customers", "customerId / id", "xref 1:1, ausser DQ-18", "", "DQ-18", "Feldname je Schema-Version"),
    ("partner", "nachname", "HAPO;VERA", "PARTNER", "NAME1", "split_name(NAME1) 'NACHNAME VORNAME'; Ruecktransliteration mit Woerterbuch", "MUELLER->Mueller/Mueller? (nicht eindeutig)", "DQ-03;DQ-04", "name_konfidenz in xref"),
    ("partner", "vorname", "HAPO;VERA", "PARTNER", "NAME1", "split_name(NAME1), zweiter Teil", "", "DQ-04", "Doppelnamen teils in NAME2"),
    ("partner", "firmenname", "HAPO;VERA", "PARTNER", "NAME1", "unveraendert bei GESCHL=0 und GEBDAT=00000000", "", "", "Rechtsform in NAME2"),
    ("partner", "geburtsdatum", "HAPO;VERA", "PARTNER", "GEBDAT", "int_yyyymmdd_to_date, Platzhalter -> null", "00000000->null;19000101->null", "DQ-05", ""),
    ("partner", "geburtsdatum", "MINT", "customers", "birthDate / dateOfBirth / person.birthDate", "ISO-Datum; 1900-01-01 -> null", "1900-01-01->null", "DQ-24", "migrierte Saetze"),
    ("partner", "geschlecht", "HAPO;VERA", "PARTNER", "GESCHL", "Codeliste", "1->M;2->W;9->D;0->UNBEKANNT", "DQ-26", ""),
    ("partner", "geschlecht", "MINT", "customers", "gender", "Enum-Normalisierung", "male/MALE->M;female/FEMALE->W;diverse/DIVERSE->D;null->UNBEKANNT", "DQ-16", ""),
    ("partner", "zivilstand", "HAPO;VERA", "PARTNER", "ZIVST", "Codeliste", "1->LEDIG;2->VERHEIRATET;3->GESCHIEDEN;4->VERWITWET;5->PARTNERSCHAFT;0->UNBEKANNT", "", ""),
    ("partner", "sprache", "HAPO;VERA", "PARTNER", "SPRACHE", "Codeliste", "D->de;F->fr;I->it;E->en", "", ""),
    ("partner", "land_wohnsitz", "HAPO;VERA", "PARTNER", "LANDKZ", "ISO-3166 numerisch -> alpha-2", "756->CH;276->DE", "", ""),
    ("partner", "beruf_text", "MINT", "customers", "occupation / occupationText", "Normalisierung Freitext -> ref Beruf", "", "DQ-21", "Embedding/Regeln"),
    ("partner_adresse", "strasse;hausnummer;plz;ort", "HAPO;VERA", "PARTNER", "ADR1;ADR2;ADR3", "parse_adresse_ch_de() regelbasiert + PLZ-Referenz", "", "DQ-13;DQ-27", "Hausnummer teils in ADR2"),
    ("partner_adresse", "strasse;hausnummer;plz;ort", "MINT", "customers", "address / addresses[]", "strukturiert; Ortsname normalisieren", "", "DQ-13", "Tippfehler im Ortsnamen"),
    ("partner_kontakt", "wert (EMAIL)", "HAPO;VERA", "PARTNER", "EMAIL", "unveraendert; leer -> kein Kontakt", "", "DQ-06", ""),
    ("partner_kontakt", "wert (EMAIL)", "MINT", "customers", "email / contact.email / contacts[type=EMAIL]", "Missing-Varianten -> null", "''->null;n/a->null;null->null", "DQ-17", ""),
    ("vertrag", "vertrag_id", "HAPO", "VERTRAG", "VERTRNR", "xref; Pruefziffer Modulo-10-rekursiv", "", "", "40.xxx.xxx-P"),
    ("vertrag", "vertrag_id", "VERA", "VERTRAG", "VERTRNR", "xref", "", "", "L-nnnnnnn"),
    ("vertrag", "vertrag_id", "MINT", "policies", "policyId", "xref 1:1", "", "", "policyNumber kundenseitig"),
    ("vertrag", "produkt_id", "HAPO", "VERTRAG", "SPARTE", "Codeliste", "10->HP-PRIV;20->HP-BETR;30->HP-BERUF", "", ""),
    ("vertrag", "produkt_id", "VERA", "VERTRAG", "SPARTE", "Codeliste", "R1->LV-RISK;K1->LV-VORS;N1->LV-RENTE;E1->LV-EU", "", ""),
    ("vertrag", "produkt_id", "MINT", "policies", "product", "Enum", "private_liability->HP-PRIV;business_liability->HP-BETR;professional_liability->HP-BERUF;term_life->LV-RISK;endowment_life->LV-VORS;annuity->LV-RENTE", "", ""),
    ("vertrag", "tarifgeneration_id", "HAPO", "VERTRAG", "TARIF", "Codeliste", "PFM-K->HP-KLASSIK;PFM-M->HP-MODERN;MZD->MZ-DIRECT;PM25->PM-2025", "", ""),
    ("vertrag", "tarifgeneration_id", "VERA", "VERTRAG", "TARIF", "Codeliste", "K85->PK-85;K95->PK-95;K00->PK-2000;K04->PK-2004;K07->PK-2007;L12->PL-2012;L15->PL-2015;L17->PL-2017;M20->MZ-2020;Z25->PZ-2025", "", ""),
    ("vertrag", "beginn", "HAPO;VERA", "VERTRAG", "BEGDAT", "int_yyyymmdd_to_date (TXT) bzw. DD.MM.YY (CSV, Jahrhundert ableiten)", "", "DQ-05;DQ-14", "CSV zweistelliges Jahr"),
    ("vertrag", "ablauf", "HAPO;VERA", "VERTRAG", "ENDDAT", "99991231 -> null", "", "DQ-05", ""),
    ("vertrag", "jahrespraemie_brutto", "HAPO;VERA", "VERTRAG", "PRAEM", "/100; Waehrung aus LANDKZ", "756->CHF;276->EUR", "DQ-12", "Integer in Rappen/Cent"),
    ("vertrag", "jahrespraemie_brutto", "MINT", "policies", "premium.amount", "Decimal-String bzw. Float (v1) -> decimal(12,2)", "", "DQ-23", "Rundungsartefakte v1"),
    ("vertrag", "versicherungssumme", "HAPO;VERA", "VERTRAG", "SUMME", "/100", "", "DQ-12", ""),
    ("vertrag", "zahlungsweise", "HAPO;VERA", "VERTRAG", "ZAHLWS", "Codeliste", "1->JAEHRLICH;2->HALBJAEHRLICH;4->VIERTELJAEHRLICH;12->MONATLICH", "", ""),
    ("vertrag", "status", "HAPO;VERA", "VERTRAG", "STATUS+STORNOGRD", "Regelwerk", "A->AKTIV;S+01->GEKUENDIGT_VN;S+02->GEKUENDIGT_VU;S+05->STORNIERT;S+ZZ->(ignorieren, migriert);E->ABGELAUFEN;L->LEISTUNG_ERBRACHT;R->RUECKKAUF", "DQ-08;DQ-25", "Migrationsstorno zaehlt nicht als Churn"),
    ("vertrag", "status", "MINT", "policies", "status / lifecycle.state", "versionsabhaengig", "active/ACTIVE->AKTIV;cancelled/CANCELLED/TERMINATED->GEKUENDIGT_VN;lapsed/LAPSED->STORNIERT;expired/EXPIRED->ABGELAUFEN;surrendered->RUECKKAUF;claimed/SETTLED->LEISTUNG_ERBRACHT", "DQ-16", ""),
    ("vertrag", "storno_datum", "HAPO;VERA", "VERTRAG", "STORNODAT", "int -> date; bei STORNOGRD=ZZ ignorieren", "", "DQ-25", ""),
    ("vertrag", "vermittler_id", "HAPO;VERA", "VERTRAG", "VERMNR / VERMNR_ALT", "Lookup mit Fallback auf Alt-Nummer", "", "DQ-11", ""),
    ("vertrag", "vermittler_id", "MINT", "policies", "agentId", "xref; channel=web ohne Agent", "", "", ""),
    ("risiko_objekt", "hund", "HAPO", "VERTRAG", "ZUSATZ1", "nur wenn SPARTE=10; Freitext -> bool + Rasse", "HUND*->true", "DQ-07", "ueberladenes Feld"),
    ("risiko_objekt", "raucher_angabe", "VERA", "VERTRAG", "ZUSATZ1", "nur wenn SPARTE=R1/K1", "J->true;N->false;' '->null", "DQ-07", "ueberladenes Feld"),
    ("risiko_objekt", "bmi_angabe", "VERA", "VERTRAG", "ZUSATZ2", "BMInn -> int", "", "DQ-07", ""),
    ("deckung", "baustein", "HAPO", "VERTRAG", "ZUSATZ2", "Kuerzelliste -> Bausteincodes", "TIE->BS-TIER-*;GEB->BS-GEBAEUDE;...", "DQ-07", "im Fall Pieper nicht migriert"),
    ("deckung", "baustein", "MINT", "policies", "coverages[type=ADDON].code", "1:1", "", "DQ-24", "fehlend bei Migrationsartefakt"),
]


def feld_mapping() -> pd.DataFrame:
    return pd.DataFrame(FELD_MAPPING, columns=SPALTEN)
