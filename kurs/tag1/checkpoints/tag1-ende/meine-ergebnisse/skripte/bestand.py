"""Erzeugt die Daten fuer den Cockpit-Reiter «Bestand».

Liest die bereinigte Vertragstabelle zeilenweise (fuer Kacheln, Aufschluesselung
und Filter im Browser) und stellt einen Katalog aller Datentabellen des Projekts
zusammen (Name in Worten, Zeilen, Spalten, Zweck). Schreibt beides als
JavaScript-Konstante nach meine-ergebnisse/cockpit-daten/bestand.js, damit das
Cockpit ohne Server im Browser laeuft.
"""

import json
import pandas as pd
from pathlib import Path

PROJEKT_ROOT = Path(__file__).resolve().parents[2]
CURATED = PROJEKT_ROOT / "data" / "curated" / "S" / "csv"
MIGRATION = PROJEKT_ROOT / "data" / "migration" / "S" / "csv"
RAW_PVS = PROJEKT_ROOT / "data" / "raw" / "S" / "pvs"
RAW_MINT = PROJEKT_ROOT / "data" / "raw" / "S" / "mint"
REFERENCE = PROJEKT_ROOT / "data" / "reference"
AUSGABE = PROJEKT_ROOT / "meine-ergebnisse" / "cockpit-daten" / "bestand.js"

STICHTAG = "2025-12-31"
JAHRESANFANG = "2025-01-01"
JAHRESENDE = "2025-12-31"
KURS_EUR_CHF_2025 = 0.94
NICHT_CHURN_CODES = ["K07", "K13", "K15", "K16"]
QUOTEN_JAHRE = list(range(2019, 2026))
GELB_PUFFER_PP = 0.5


def vertragszeilen():
    v = pd.read_csv(CURATED / "vertrag.csv")
    spalten = [
        "vertrag_id",
        "sparte",
        "markt",
        "herkunft",
        "status",
        "versicherungsnehmer_id",
        "jahrespraemie_brutto",
        "waehrung",
        "quellsystem",
        "migriert_am",
        "beginn",
        "storno_datum",
        "storno_grund_code",
        "kanal",
        "tarifgeneration_id",
    ]
    zeilen = []
    for _, r in v[spalten].iterrows():
        zeilen.append({
            "id": r["vertrag_id"],
            "sparte": r["sparte"],
            "markt": r["markt"],
            "herkunft": r["herkunft"],
            "status": r["status"],
            "vn": r["versicherungsnehmer_id"],
            "praemie": None if pd.isna(r["jahrespraemie_brutto"]) else float(r["jahrespraemie_brutto"]),
            "waehrung": r["waehrung"],
            "migriertAufMint": (r["quellsystem"] == "MINT") or (not pd.isna(r["migriert_am"])),
            "beginn": None if pd.isna(r["beginn"]) else str(r["beginn"]),
            "stornoDatum": None if pd.isna(r["storno_datum"]) else str(r["storno_datum"]),
            "stornoGrund": None if pd.isna(r["storno_grund_code"]) else r["storno_grund_code"],
            "kanal": r["kanal"],
            "tarifgeneration": r["tarifgeneration_id"],
        })
    return zeilen


def tarifgenerationen_leben():
    tg = pd.read_csv(CURATED / "tarifgeneration.csv")
    lv_tg = tg[tg.sparte == "LV"][["tarifgeneration_id", "bezeichnung"]]
    up = pd.read_csv(REFERENCE / "lv" / "ueberschuss_parameter.csv")
    up25 = up[up.jahr == 2025]

    eintraege = []
    for _, row in lv_tg.iterrows():
        code = row["tarifgeneration_id"]
        zeilen_up = up25[up25.generation_code == code]
        for markt in ["DE", "CH"]:
            treffer = zeilen_up[zeilen_up.markt == markt]
            if treffer.empty:
                continue
            garantiezins = float(treffer["rechnungszins_pct"].iloc[0])
            gesamtverzinsung = float(treffer["gesamtverzinsung_pct"].iloc[0])
            abstand = gesamtverzinsung - garantiezins
            if abstand < 0:
                status = "rot"
            elif abstand <= GELB_PUFFER_PP:
                status = "gelb"
            else:
                status = "gruen"
            eintraege.append({
                "code": code,
                "bezeichnung": row["bezeichnung"],
                "markt": markt,
                "garantiezins": garantiezins,
                "gesamtverzinsung": gesamtverzinsung,
                "ampel": status,
            })
    return eintraege


def zeilen_spalten(pfad, **read_kwargs):
    df = pd.read_csv(pfad, **read_kwargs)
    return len(df), len(df.columns)


def katalog():
    eintraege = []

    curated_zwecke = {
        "partner.csv": ("Partner", "Alle natürlichen und juristischen Personen im Bestand: Kunden, Mitversicherte, Begünstigte, Firmen."),
        "partner_adresse.csv": ("Partneradressen", "Anschriften der Partner, auch frühere Adressen bei einem Umzug."),
        "partner_kontakt.csv": ("Partnerkontakte", "Telefonnummern und E-Mail-Adressen der Partner."),
        "partner_firma.csv": ("Partnerfirmen", "Zusatzangaben zu Firmenkunden: Rechtsform und Branche."),
        "partner_beziehung.csv": ("Partnerbeziehungen", "Verknüpfungen zwischen Partnern, etwa Haushalt oder Vertretung."),
        "vertrag.csv": ("Verträge", "Herzstück des Bestands: Sparte, Prämie, Status, Kanal, Herkunft und Quellsystem je Vertrag."),
        "vertrag_partner_rolle.csv": ("Vertragsrollen", "Welche Rolle ein Partner an einem Vertrag hat: Versicherungsnehmer, mitversichert, begünstigt."),
        "deckung.csv": ("Deckungen", "Vertragsbausteine und Deckungssummen je Vertrag."),
        "risiko_objekt.csv": ("Risikoobjekte", "Das versicherte Objekt oder Risiko je Vertrag."),
        "antrag.csv": ("Anträge", "Antragsdaten inklusive Risikoprüfungsentscheid: Annahme, Zuschlag oder Ablehnung."),
        "produkt.csv": ("Produkte", "Katalog der angebotenen Versicherungsprodukte."),
        "tarifgeneration.csv": ("Tarifgenerationen", "Tarifwerke, mit denen Produkte im Zeitverlauf kalkuliert wurden."),
        "schaden.csv": ("Schäden", "Schadenfälle im Bestand, nur die zehn Kunden-Personas."),
        "schaden_position.csv": ("Schadenpositionen", "Einzelne Reserve- und Zahlungsposten je Schaden."),
        "interaktion.csv": ("Interaktionen", "Kundenkontakte: Anrufe, Briefe, E-Mails."),
        "dokument.csv": ("Dokumente", "Verweise auf Schreiben, Policen und Gutachten als Dateien."),
        "vermittler.csv": ("Vermittler", "Einzelne Vermittlerinnen und Vermittler."),
        "agentur.csv": ("Agenturen", "Vermittlerorganisationen."),
        "mitarbeiter.csv": ("Mitarbeitende", "Personal der Pfefferminzia."),
        "org_einheit.csv": ("Organisationseinheiten", "Abteilungen und Teams."),
    }
    for datei, (name, zweck) in curated_zwecke.items():
        z, s = zeilen_spalten(CURATED / datei)
        eintraege.append({"kategorie": "Bereinigte Tabellen", "name": name, "zeilen": z, "spalten": s, "zweck": zweck})

    migration_zwecke = {
        "partner_xref.csv": ("Partner-Zuordnung", "Verknüpft Partnersätze aus HAPO und VERA mit dem MINT-Satz, inklusive Zuordnungsmethode und Score."),
        "vertrag_xref.csv": ("Vertrags-Zuordnung", "Verknüpft Vertragssätze aus HAPO und VERA mit dem MINT-Satz."),
        "feld_mapping.csv": ("Feld-Zuordnung", "Erklärt, wie Altsystem-Codes in die bereinigten Felder übersetzt wurden."),
        "migrationslog.csv": ("Migrationsprotokoll", "Ergebnis je migriertem Objekt: unauffällig, mit Warnung oder mit Fehler."),
    }
    for datei, (name, zweck) in migration_zwecke.items():
        z, s = zeilen_spalten(MIGRATION / datei)
        eintraege.append({"kategorie": "Migrationsbrücken", "name": name, "zeilen": z, "spalten": s, "zweck": zweck})

    raw_zwecke = [
        ("HAPO_PARTNER.csv", "HAPO Partner (Rohdaten)", "Rohe Kundendaten des alten Haftpflicht-Hostsystems Pfefferminz, im Original als Fixed-Width- und Semikolon-Datei."),
        ("HAPO_VERTRAG.csv", "HAPO Vertrag (Rohdaten)", "Rohe Vertragsdaten des alten Haftpflicht-Hostsystems Pfefferminz."),
        ("VERA_PARTNER.csv", "VERA Partner (Rohdaten)", "Rohe Kundendaten des alten Lebensversicherungs-Hostsystems."),
        ("VERA_VERTRAG.csv", "VERA Vertrag (Rohdaten)", "Rohe Vertragsdaten des alten Lebensversicherungs-Hostsystems."),
    ]
    for datei, name, zweck in raw_zwecke:
        z, s = zeilen_spalten(RAW_PVS / datei, encoding="iso-8859-1", sep=";")
        eintraege.append({"kategorie": "Rohdaten Altsysteme", "name": name, "zeilen": z, "spalten": s, "zweck": zweck})

    mint_zwecke = [
        ("customers.jsonl", "MINT Kunden (Rohdaten)", "Rohe Kundendaten der Minzia-Cloud-Plattform, heutiger Endzustand nach der Migration."),
        ("policies.jsonl", "MINT Policen (Rohdaten)", "Rohe Vertragsdaten der Minzia-Cloud-Plattform, heutiger Endzustand nach der Migration."),
    ]
    for datei, name, zweck in mint_zwecke:
        with open(RAW_MINT / datei, encoding="utf-8") as fh:
            zeilen_liste = [json.loads(z) for z in fh]
        z = len(zeilen_liste)
        s = len(zeilen_liste[0].keys()) if zeilen_liste else 0
        eintraege.append({"kategorie": "Rohdaten Altsysteme", "name": name, "zeilen": z, "spalten": s, "zweck": zweck})

    referenz_zwecke = {
        "hp/ablehnungsgruende.csv": ("Ablehnungsgründe Haftpflicht", "Codes und Texte für abgelehnte Anträge in der Haftpflicht."),
        "hp/bausteine.csv": ("Deckungsbausteine Haftpflicht", "Stammdaten der einzelnen Deckungsbausteine in der Haftpflicht."),
        "hp/berufsgruppen.csv": ("Berufsgruppen Haftpflicht", "Einstufung der Berufsgruppen für die Risikoeinschätzung."),
        "hp/betrugsmuster.csv": ("Betrugsmuster Haftpflicht", "Muster, die auf möglichen Versicherungsbetrug hindeuten."),
        "hp/branchenklassen.csv": ("Branchenklassen Haftpflicht", "Einstufung der Branchen für Betriebshaftpflicht-Tarife."),
        "hp/deckungssummen.csv": ("Deckungssummen Haftpflicht", "Mindest- und Höchstsummen je Deckungsbaustein."),
        "hp/dokumenttypen.csv": ("Dokumenttypen Haftpflicht", "Katalog der Dokumentarten in der Haftpflicht-Akte."),
        "hp/lebenszyklus_raten.csv": ("Lebenszyklusraten Haftpflicht", "Übergangswahrscheinlichkeiten für die Generierung von Vertragsverläufen."),
        "hp/plz_zonen.csv": ("PLZ-Zonen Haftpflicht", "Regionale Risikozonen nach Postleitzahl."),
        "hp/produkte.csv": ("Produktstammdaten Haftpflicht", "Grunddaten der Haftpflichtprodukte."),
        "hp/schadenarten.csv": ("Schadenarten Haftpflicht", "Katalog der möglichen Schadenarten."),
        "hp/schadenfrequenzen.csv": ("Schadenfrequenzen Haftpflicht", "Erwartete Schadenhäufigkeiten je Risikogruppe."),
        "hp/selbstbehalte.csv": ("Selbstbehalte Haftpflicht", "Mögliche Selbstbehaltsstufen je Produkt."),
        "hp/status_codes.csv": ("Statuscodes Haftpflicht", "Bedeutung der Vertragsstatus- und Stornogrundcodes."),
        "hp/tarifgenerationen.csv": ("Tarifgenerationen Haftpflicht (Details)", "Parameter der Tarifgenerationen in der Haftpflicht."),
        "hp/vollmachtsstufen.csv": ("Vollmachtsstufen Haftpflicht", "Kompetenzstufen für Entscheidungen im Vertrag."),
        "lv/betrugsmuster.csv": ("Betrugsmuster Leben", "Muster, die auf möglichen Versicherungsbetrug hindeuten."),
        "lv/diagnose_bibliothek.csv": ("Diagnosebibliothek Leben", "Medizinische Diagnosen für die Risikoprüfung."),
        "lv/dokumenttypen.csv": ("Dokumenttypen Leben", "Katalog der Dokumentarten in der Lebensversicherungs-Akte."),
        "lv/gesundheitsfragen.csv": ("Gesundheitsfragen Leben", "Fragen des Antragsformulars zur Gesundheit."),
        "lv/kulanzfaelle.csv": ("Kulanzfälle Leben", "Fälle, in denen aus Kulanz abweichend entschieden wurde."),
        "lv/laufzeiten.csv": ("Laufzeiten Leben", "Mögliche Vertragslaufzeiten je Produkt."),
        "lv/lebenszyklus_raten.csv": ("Lebenszyklusraten Leben", "Übergangswahrscheinlichkeiten für die Generierung von Vertragsverläufen."),
        "lv/leistungsarten.csv": ("Leistungsarten Leben", "Katalog der möglichen Leistungsfälle."),
        "lv/produkte.csv": ("Produktstammdaten Leben", "Grunddaten der Lebensversicherungsprodukte."),
        "lv/status_codes.csv": ("Statuscodes Leben", "Bedeutung der Vertragsstatus- und Stornogrundcodes, inklusive Stornoquoten-Zählregel."),
        "lv/sterbetafel.csv": ("Sterbetafel", "Sterbewahrscheinlichkeiten für die Tarifkalkulation."),
        "lv/tarifgenerationen.csv": ("Tarifgenerationen Leben (Details)", "Parameter der Tarifgenerationen in der Lebensversicherung, inklusive Garantiezins."),
        "lv/ueberschuss_parameter.csv": ("Überschussparameter Leben", "Parameter der Gesamtverzinsung je Tarifgeneration und Jahr."),
        "lv/underwriting_entscheidungen.csv": ("Underwriting-Entscheidungen Leben", "Bedeutung der Risikoprüfungscodes im Antrag."),
        "lv/versicherungssummen.csv": ("Versicherungssummen Leben", "Mindest- und Höchstsummen je Produkt."),
        "geo/orte_ch.csv": ("Orte Schweiz", "Ortsnamen und Postleitzahlen für die Datengenerierung."),
        "geo/orte_de.csv": ("Orte Deutschland", "Ortsnamen und Postleitzahlen für die Datengenerierung."),
        "geo/strassennamen.csv": ("Strassennamen", "Strassennamen für die Datengenerierung."),
        "namen/blocklist.csv": ("Namen-Sperrliste", "Namen, die der Generator nicht verwenden darf."),
        "namen/firmennamen_bausteine.csv": ("Firmennamen-Bausteine", "Bausteine für erfundene Firmennamen."),
        "namen/nachnamen.csv": ("Nachnamen", "Nachnamen für die Datengenerierung."),
        "namen/vornamen.csv": ("Vornamen", "Vornamen für die Datengenerierung."),
    }
    for pfad, (name, zweck) in referenz_zwecke.items():
        z, s = zeilen_spalten(REFERENCE / pfad)
        eintraege.append({"kategorie": "Referenz- und Stammdaten", "name": name, "zeilen": z, "spalten": s, "zweck": zweck})

    return eintraege


def main():
    daten = {
        "stichtag": STICHTAG,
        "jahresanfang": JAHRESANFANG,
        "jahresende": JAHRESENDE,
        "kursEurChf2025": KURS_EUR_CHF_2025,
        "nichtChurnCodes": NICHT_CHURN_CODES,
        "quotenJahre": QUOTEN_JAHRE,
        "gelbPufferPp": GELB_PUFFER_PP,
        "vertraege": vertragszeilen(),
        "katalog": katalog(),
        "tarifgenerationenLeben": tarifgenerationen_leben(),
    }
    js = "// Erzeugt von meine-ergebnisse/skripte/bestand.py -- nicht von Hand editieren.\n"
    js += "const BESTAND_DATEN = " + json.dumps(daten, ensure_ascii=False, indent=None) + ";\n"
    AUSGABE.write_text(js, encoding="utf-8")
    print(f"Geschrieben: {AUSGABE} ({len(daten['vertraege'])} Vertraege, {len(daten['katalog'])} Katalogeintraege)")


if __name__ == "__main__":
    main()
