"""Erzeugt die Daten für den Cockpit-Reiter 'Bestand' aus den bereinigten Tabellen.

Liest die Vertragstabelle (Datensatz Stufe S) und den Konzernkurs, schreibt eine
JSON-Struktur nach meine-ergebnisse/cockpit-daten/bestand.js als globale
JavaScript-Konstante, damit das Cockpit ohne Server im Browser läuft.
Ausserdem: ein Tabellenkatalog (Zeilen, Spalten, Zweck) der bereinigten Tabellen,
Migrationsbrücken und Rohdaten der Alt- und Zielsysteme.
"""

import json
import math

import pandas as pd
import yaml

REPO_ROOT = __import__("pathlib").Path(__file__).resolve().parents[2]


def clean(value):
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if pd.isna(value):
        return None
    return value


def vertraege_laden():
    v = pd.read_csv(REPO_ROOT / "data/curated/S/csv/vertrag.csv")
    spalten = [
        "vertrag_id",
        "sparte",
        "markt",
        "herkunft",
        "kanal",
        "status",
        "waehrung",
        "jahrespraemie_netto",
        "beginn",
        "storno_datum",
        "storno_grund_code",
        "quellsystem",
        "migriert_am",
        "tarifgeneration_id",
        "versicherungsnehmer_id",
    ]
    v = v[spalten]
    zeilen = []
    for _, row in v.iterrows():
        zeilen.append({spalte: clean(row[spalte]) for spalte in spalten})
    return zeilen


def partner_typen_laden():
    p = pd.read_csv(REPO_ROOT / "data/curated/S/csv/partner.csv")
    return {row["partner_id"]: row["partner_typ"] for _, row in p[["partner_id", "partner_typ"]].iterrows()}


def lv_garantiezins_2025_laden():
    tg = pd.read_csv(REPO_ROOT / "data/reference/lv/tarifgenerationen.csv")
    ue = pd.read_csv(REPO_ROOT / "data/reference/lv/ueberschuss_parameter.csv")
    ue_2025 = ue[ue["jahr"] == 2025].set_index(["generation_code", "markt"])["gesamtverzinsung_pct"]

    zeilen = []
    for _, g in tg.iterrows():
        code = g["generation_code"]
        for markt in ["CH", "DE"]:
            if markt == "CH":
                garantiezins = g["technischer_zins_ch_pct"]
            else:
                kandidaten = [g["rechnungszins_de_pct"]]
                if pd.notna(g["rechnungszins_de_ab_2022_pct"]):
                    kandidaten.append(g["rechnungszins_de_ab_2022_pct"])
                garantiezins = max(kandidaten)
            gesamtverzinsung = ue_2025.get((code, markt))
            if gesamtverzinsung is None:
                continue
            zeilen.append({
                "generation_code": code,
                "bezeichnung": g["bezeichnung"],
                "markt": markt,
                "garantiezins": round(float(garantiezins), 2),
                "gesamtverzinsung_2025": round(float(gesamtverzinsung), 2),
            })
    return zeilen


def konzernkurs_laden():
    with open(REPO_ROOT / "data/reference/kennzahlen_master.yaml", encoding="utf-8") as f:
        ref = yaml.safe_load(f)
    return ref["meta"]["umrechnungskurs_eur_chf"][2025]


def spalten_zaehlen_csv(pfad, **kwargs):
    df = pd.read_csv(pfad, **kwargs)
    return len(df), len(df.columns)


def spalten_zaehlen_jsonl(pfad):
    with open(pfad, encoding="utf-8") as f:
        erste_zeile = json.loads(f.readline())
        anzahl = 1
        for _ in f:
            anzahl += 1
    return anzahl, len(erste_zeile.keys())


def tabellenkatalog_bauen():
    katalog = []

    bereinigt = [
        ("Partner", "partner.csv", "Alle Personen und Firmen im System – Kundinnen und Kunden, Mitversicherte, Begünstigte."),
        ("Partneradresse", "partner_adresse.csv", "Adresshistorie je Partner mit Gültigkeit von/bis."),
        ("Partnerkontakt", "partner_kontakt.csv", "Telefonnummern und E-Mail-Adressen je Partner."),
        ("Partnerfirma", "partner_firma.csv", "Firmenspezifische Angaben (Rechtsform, Handelsregister) zu Firmenpartnern."),
        ("Partnerbeziehung", "partner_beziehung.csv", "Beziehungen zwischen Partnern, etwa Familie oder Bevollmächtigte."),
        ("Vertrag", "vertrag.csv", "Zentrale Vertragstabelle: Sparte, Prämie, Status, Vertriebskanal, Herkunft."),
        ("Vertragspartnerrolle", "vertrag_partner_rolle.csv", "Weitere Rollen an einem Vertrag, etwa Mitversicherte oder Begünstigte."),
        ("Deckung", "deckung.csv", "Deckungsbausteine je Vertrag."),
        ("Risikoobjekt", "risiko_objekt.csv", "Das versicherte Risiko (Gebäude, Person, Betrieb) je Vertrag."),
        ("Antrag", "antrag.csv", "Anträge inklusive Risikoprüfungsentscheid."),
        ("Schaden", "schaden.csv", "Schadenfälle, nur für die zehn Kunden-Personas erfasst."),
        ("Schadenposition", "schaden_position.csv", "Einzelpositionen wie Reserve oder Zahlung je Schaden."),
        ("Interaktion", "interaktion.csv", "Kontakte mit Kundinnen und Kunden: Anrufe, Mails, Briefe."),
        ("Dokument", "dokument.csv", "Dokumente wie Briefe, Policen oder Gutachten mit Verweis auf die Datei."),
        ("Produkt", "produkt.csv", "Produktkatalog."),
        ("Tarifgeneration", "tarifgeneration.csv", "Tarifgenerationen je Produkt."),
        ("Vermittler", "vermittler.csv", "Vermittlerinnen und Vermittler."),
        ("Agentur", "agentur.csv", "Agenturen."),
        ("Mitarbeiter", "mitarbeiter.csv", "Mitarbeitende, nur ein Ausschnitt des Personals."),
        ("Organisationseinheit", "org_einheit.csv", "Organisationsstruktur."),
    ]
    for name, datei, zweck in bereinigt:
        zeilen, spalten = spalten_zaehlen_csv(REPO_ROOT / "data/curated/S/csv" / datei)
        katalog.append({
            "kategorie": "Bereinigte Tabelle",
            "name": name,
            "zeilen": zeilen,
            "spalten": spalten,
            "zweck": zweck,
        })

    bruecken = [
        ("Partnerbrücke", "partner_xref.csv", "Ordnet jeden Partner-Rohsatz aus HAPO, VERA oder MINT der bereinigten Partnernummer zu, mit Zuordnungsmethode und Übereinstimmungswert."),
        ("Vertragsbrücke", "vertrag_xref.csv", "Ordnet jeden Vertrags-Rohsatz aus HAPO, VERA oder MINT der bereinigten Vertragsnummer zu."),
        ("Migrationslog", "migrationslog.csv", "Protokoll je migriertem Objekt am jeweiligen Migrationstag: unauffällig, Warnung oder Fehler."),
        ("Feldmapping", "feld_mapping.csv", "Übersetzt die Codes der Altsysteme in ihre Bedeutung."),
    ]
    for name, datei, zweck in bruecken:
        zeilen, spalten = spalten_zaehlen_csv(REPO_ROOT / "data/migration/S/csv" / datei)
        katalog.append({
            "kategorie": "Migrationsbrücke",
            "name": name,
            "zeilen": zeilen,
            "spalten": spalten,
            "zweck": zweck,
        })

    altsysteme = [
        ("HAPO Partner", "HAPO_PARTNER.csv", "Rohsatz Partner aus dem Haftpflicht-Altsystem HAPO, Stand 31.12.2024."),
        ("HAPO Vertrag", "HAPO_VERTRAG.csv", "Rohsatz Vertrag aus dem Haftpflicht-Altsystem HAPO, Stand 31.12.2024."),
        ("VERA Partner", "VERA_PARTNER.csv", "Rohsatz Partner aus dem Lebensversicherungs-Altsystem VERA, Stand 31.12.2024."),
        ("VERA Vertrag", "VERA_VERTRAG.csv", "Rohsatz Vertrag aus dem Lebensversicherungs-Altsystem VERA, Stand 31.12.2024."),
    ]
    for name, datei, zweck in altsysteme:
        zeilen, spalten = spalten_zaehlen_csv(REPO_ROOT / "data/raw/S/pvs" / datei, sep=";", encoding="iso-8859-1")
        katalog.append({
            "kategorie": "Rohdaten Altsystem",
            "name": name,
            "zeilen": zeilen,
            "spalten": spalten,
            "zweck": zweck,
        })

    ziel = [
        ("MINT Kunden", "customers.jsonl", "Kundendatensätze auf der Zielplattform MINT – migrierte und seit der Fusion neu erfasste Kundinnen und Kunden."),
        ("MINT Policen", "policies.jsonl", "Vertragsdatensätze auf der Zielplattform MINT."),
    ]
    for name, datei, zweck in ziel:
        zeilen, spalten = spalten_zaehlen_jsonl(REPO_ROOT / "data/raw/S/mint" / datei)
        katalog.append({
            "kategorie": "Rohdaten Zielplattform MINT",
            "name": name,
            "zeilen": zeilen,
            "spalten": spalten,
            "zweck": zweck,
        })

    return katalog


def main():
    daten = {
        "stichtag": "31.12.2025",
        "datenbasis": "Datensatz Stufe S",
        "konzernkurs_eur_chf_2025": konzernkurs_laden(),
        "stornogruende_zaehlt_nicht": ["K07", "K13", "K15", "K16"],
        "partner_typ": partner_typen_laden(),
        "lv_garantiezins_2025": lv_garantiezins_2025_laden(),
        "vertraege": vertraege_laden(),
        "tabellenkatalog": tabellenkatalog_bauen(),
    }
    ziel_datei = REPO_ROOT / "meine-ergebnisse/cockpit-daten/bestand.js"
    with open(ziel_datei, "w", encoding="utf-8") as f:
        f.write("const BESTAND_DATEN = ")
        json.dump(daten, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print(f"Geschrieben: {ziel_datei} ({len(daten['vertraege'])} Verträge, {len(daten['tabellenkatalog'])} Tabellen)")


if __name__ == "__main__":
    main()
