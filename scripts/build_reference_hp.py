"""Erzeugt die tabellarischen Haftpflicht-Stammdaten, die sich aus Planung 01 ableiten lassen.

Aufruf: ``uv run python scripts/build_reference_hp.py``

Erzeugt unter ``data/reference/hp/``: branchenklassen.csv, plz_zonen.csv, schadenarten.csv,
dokumenttypen.csv, lebenszyklus_raten.csv. Die uebrigen Dateien des Ordners sind handgepflegt.
Deterministisch, ohne Zufall.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HP = ROOT / "data" / "reference" / "hp"

# ---------------------------------------------------------------------------------------------
# Branchenklassen Betriebshaftpflicht. NOGA 2008 (CH) und WZ 2008 (DE) beruhen beide auf NACE Rev. 2,
# die 4-stelligen Codes sind deshalb identisch. (nace, bezeichnung, risikoklasse, anteil_bestand_pct)
# Risikoklasse 1 = geringes Risiko … 5 = hohes Risiko / Referat; Status abgelehnt fuer Sonderrisiken.
# ---------------------------------------------------------------------------------------------
BRANCHEN: list[tuple[str, str, int, float, str]] = [
    # Bau und Ausbau
    ("41.20", "Bau von Gebäuden (Hochbau)", 4, 2.5, ""),
    ("42.11", "Strassenbau", 4, 0.6, ""),
    ("43.12", "Erdbewegungsarbeiten, Aushub", 4, 0.8, ""),
    ("43.21", "Elektroinstallation", 3, 5.5, "Solar-/PV-Montage auf Dächern: Zuschlag wie Dachdecker"),
    ("43.22", "Sanitär-, Heizungs- und Klimainstallation", 4, 6.0, "Hauptschadentreiber Wasserschäden"),
    ("43.29", "Sonstige Bauinstallation (Lift, Isolation)", 3, 0.7, ""),
    ("43.31", "Gipserei, Stuckateur", 3, 1.6, ""),
    ("43.32", "Bautischlerei, Fenster- und Türenmontage", 3, 2.0, ""),
    ("43.33", "Bodenleger, Plattenleger", 3, 1.8, ""),
    ("43.34", "Malerei und Glaserei", 3, 4.5, "Farbflecken auf Kundenmobiliar = Bearbeitungsschaden"),
    ("43.39", "Sonstiger Ausbau, Innenausbau", 3, 1.2, ""),
    ("43.91", "Dachdeckerei, Spenglerei", 5, 1.8, "Absturz- und Brandrisiko (Heissarbeiten)"),
    ("43.99", "Gerüstbau, Kranarbeiten, Abbruch", 5, 0.7, "Referat: Abbruch nur mit Nachweis"),
    ("16.23", "Zimmerei, Holzbau", 4, 2.2, ""),
    ("31.09", "Schreinerei, Möbelherstellung", 3, 3.0, ""),
    ("25.11", "Metallbau, Schlosserei", 3, 1.8, "Schweissarbeiten beim Kunden: Heissarbeiten-Klausel"),
    ("25.62", "Mechanische Bearbeitung, Dreherei", 2, 0.9, ""),
    ("28.29", "Maschinenbau (Sondermaschinen)", 3, 0.6, "Produkthaftpflicht-Baustein empfohlen"),
    ("33.12", "Reparatur und Wartung von Maschinen", 3, 0.8, ""),
    ("32.50", "Medizintechnik, Dentallabor", 3, 0.5, "Produkthaftpflicht zwingend"),
    ("22.29", "Kunststoffverarbeitung", 3, 0.5, ""),
    ("20.16", "Herstellung von Kunststoffen in Primärform", 4, 0.1, "Umweltbaustein zwingend"),
    ("20.42", "Herstellung von Kosmetika", 3, 0.2, "Produkthaftpflicht zwingend"),
    ("18.12", "Druckerei", 2, 0.6, ""),
    # Fahrzeuge, Transport
    ("45.11", "Handel mit Automobilen", 2, 0.9, "Kfz-Haftpflicht separat (nicht Gegenstand)"),
    ("45.20", "Reparatur von Kraftfahrzeugen, Garage, Carrosserie", 3, 2.8, "Obhutsschäden an Kundenfahrzeugen"),
    ("49.32", "Taxi, Personenbeförderung", 3, 0.5, "Nur Betriebs-HP, Fahrzeuge separat"),
    ("49.41", "Güterbeförderung im Strassenverkehr", 4, 1.4, "Be-/Entladeschäden"),
    ("52.29", "Spedition, Logistikdienstleistung", 2, 0.7, ""),
    ("53.20", "Kurier- und Expressdienste", 2, 0.6, ""),
    ("77.11", "Vermietung von Kraftwagen", 3, 0.2, ""),
    # Handel
    ("46.73", "Grosshandel mit Holz, Baustoffen", 2, 0.7, ""),
    ("46.75", "Grosshandel mit chemischen Erzeugnissen", 4, 0.2, "Umweltbaustein zwingend"),
    ("46.90", "Grosshandel ohne Schwerpunkt", 2, 0.8, ""),
    ("47.11", "Einzelhandel mit Lebensmitteln (Supermarkt, Dorfladen)", 2, 2.5, ""),
    ("47.19", "Sonstiger Einzelhandel (Warenhaus, Kiosk)", 1, 1.5, ""),
    ("47.52", "Einzelhandel mit Eisenwaren, Baumarkt", 2, 0.8, ""),
    ("47.71", "Einzelhandel mit Bekleidung", 1, 1.6, ""),
    ("47.73", "Apotheken", 2, 0.9, "Produkt-/Beratungsrisiko"),
    ("47.78", "Einzelhandel Optik, Foto, Geschenke", 1, 1.0, ""),
    ("47.91", "Versand- und Internet-Einzelhandel", 1, 1.2, ""),
    # Gastgewerbe, Lebensmittel
    ("55.10", "Hotels, Gasthöfe, Pensionen", 3, 1.8, "Gästeeffekten-Baustein"),
    ("55.20", "Ferienunterkünfte, Bed and Breakfast", 2, 0.6, ""),
    ("56.10", "Restaurants, Cafés, Imbiss", 3, 5.0, "Lebensmittelvergiftung als Kumulrisiko"),
    ("56.21", "Event-Caterer, Partyservice", 3, 0.8, ""),
    ("56.30", "Bars, Clubs", 3, 0.7, "Sicherheitsdienst-Abgrenzung"),
    ("10.13", "Metzgerei, Fleischverarbeitung", 3, 0.9, "Produkthaftpflicht inkludiert"),
    ("10.51", "Käserei, Milchverarbeitung", 3, 0.5, "Produkthaftpflicht inkludiert"),
    ("10.71", "Bäckerei, Konditorei", 2, 1.6, ""),
    ("11.02", "Weinbau, Weinkellerei", 2, 0.6, ""),
    ("01.13", "Gemüse- und Obstbau", 2, 0.5, ""),
    ("01.50", "Gemischte Landwirtschaft", 3, 1.0, "Tierhalter- und Gewässerrisiko (Gülle)"),
    # Dienstleistungen am Objekt und an Personen
    ("81.10", "Hauswartung, Facility Management", 2, 1.4, ""),
    ("81.21", "Gebäudereinigung", 2, 2.4, "Obhutsschäden (Böden, Fenster)"),
    ("81.30", "Garten- und Landschaftsbau", 3, 2.6, "Baumfällarbeiten: Zuschlag"),
    ("80.10", "Sicherheitsdienste, Bewachung", 3, 0.5, ""),
    ("96.02", "Coiffeur, Kosmetik", 1, 2.8, "Personenschäden (Verätzung, Allergie) mit kleinem Aufwand"),
    ("96.04", "Wellness, Massage, Solarium", 2, 0.6, ""),
    ("93.13", "Fitnesscenter", 2, 0.7, ""),
    ("93.29", "Freizeitanlagen (Kletterhalle, Trampolinpark)", 4, 0.3, "Personenschadenrisiko hoch"),
    ("88.91", "Kindertagesstätte, Kinderkrippe", 2, 1.1, "Aufsichtspflicht"),
    ("85.53", "Fahrschule", 3, 0.4, ""),
    ("86.21", "Arztpraxis (Allgemeinmedizin)", 2, 0.9, "Berufshaftpflicht Medizin nicht Gegenstand, nur Betriebsrisiko"),
    ("86.23", "Zahnarztpraxis", 2, 0.7, "wie 86.21"),
    ("86.90", "Physiotherapie, Gesundheitswesen a. n. g.", 2, 1.2, ""),
    ("87.30", "Alters- und Pflegeheim", 3, 0.6, ""),
    ("75.00", "Tierarztpraxis", 2, 0.4, ""),
    ("96.09", "Hundesalon, Tierpension, sonstige Dienstleistungen", 1, 0.5, ""),
    # Kreativ, Medien, Büro
    ("73.11", "Werbeagentur", 1, 1.0, "Reine Vermögensschäden: Berufshaftpflicht"),
    ("74.10", "Design, Grafik, Innenarchitektur", 1, 0.9, ""),
    ("74.20", "Fotografie", 1, 0.6, ""),
    ("58.11", "Verlag", 1, 0.3, ""),
    ("90.01", "Darstellende Kunst, Eventtechnik", 3, 0.5, "Traversen, Bühnenbau: Zuschlag"),
    ("95.11", "Reparatur von Computern", 1, 0.5, ""),
    ("62.01", "Softwareentwicklung (Betriebsrisiko)", 1, 1.4, "Vermögensschäden über Berufshaftpflicht BG-IT"),
    ("68.20", "Vermietung eigener Immobilien", 2, 1.5, "Gebäudehaftpflicht-Baustein"),
    ("68.32", "Immobilienverwaltung, Hauswartung", 1, 0.8, ""),
    ("79.11", "Reisebüro", 1, 0.4, ""),
    # Entsorgung, Umwelt, Sonderrisiken
    ("37.00", "Abwasserentsorgung, Kanalreinigung", 4, 0.2, "Umweltbaustein zwingend"),
    ("38.11", "Abfallsammlung", 4, 0.3, "Umweltbaustein zwingend"),
    ("38.21", "Abfallbehandlung, Deponie", 5, 0.1, "Referat: nur mit Umweltgutachten"),
    ("05.10", "Kohlenbergbau", 5, 0.0, "abgelehnt"),
    ("19.20", "Mineralölverarbeitung", 5, 0.0, "abgelehnt"),
    ("20.51", "Herstellung von Sprengstoffen, Pyrotechnik", 5, 0.0, "abgelehnt"),
    ("30.30", "Luft- und Raumfahrzeugbau", 5, 0.0, "abgelehnt"),
    ("51.10", "Personenbeförderung in der Luftfahrt", 5, 0.0, "abgelehnt"),
    ("92.00", "Spiel-, Wett- und Lotteriewesen", 5, 0.1, "Referat: Geldwäscherei-Abklärung"),
]
PRAEMIENSATZ_PROMILLE = {1: 0.6, 2: 1.0, 3: 1.8, 4: 3.0, 5: 4.5}


def zeichnungsstatus(klasse: int, bemerkung: str) -> str:
    if bemerkung == "abgelehnt":
        return "abgelehnt"
    if klasse == 5:
        return "referat"
    if klasse == 4:
        return "zuschlag"
    return "annehmbar"


# ---------------------------------------------------------------------------------------------
# Tarifzonen (die Zuordnung Ort -> Zone steht in geo/orte_*.csv, Spalte tarifzone)
# ---------------------------------------------------------------------------------------------
PLZ_ZONEN = [
    ("CH", "1", "Grossstadt und teure Agglomeration (Zürich, Genf, Basel, Lausanne, Bern, Zug …)", 1.05, 1.06, 1.04,
     "Höhere Sachwerte, dichtere Bebauung, mehr Mietsach- und Wasserschäden"),
    ("CH", "2", "Mittelland und Agglomerationen", 1.00, 1.00, 1.00, "Referenzzone"),
    ("CH", "3", "Ländlich und alpin (GR, VS, JU, Innerschweiz, AR/AI, GL)", 0.98, 0.96, 0.98,
     "Weniger Schäden je Vertrag, aber Wintersport-Kollisionen in Tourismusorten"),
    ("DE", "1", "Metropolen (Berlin, Hamburg, München, Köln, Frankfurt, Stuttgart, Düsseldorf)", 1.10, 1.08, 1.05,
     "Hohe Mietsachwerte, Schlüsselverlust-Häufung, höhere Anwaltsquote"),
    ("DE", "2", "Übrige Grossstädte ab ca. 100'000 Einwohner", 1.03, 1.02, 1.02, ""),
    ("DE", "3", "Klein- und Mittelstädte, ländlicher Raum", 0.97, 0.96, 0.98, "Referenzzone für Landkreise"),
]

# ---------------------------------------------------------------------------------------------
# Schadenarten: (id, bezeichnung, produkte, anteil je Produkt/Markt, mu, sigma, nullschaden, abwehr,
#                dauer_median, dauer_p90, saison_profil)
# Anteile aus Planung 01 §4.4.1, Lognormal-Parameter aus §4.4.3 (CHF und EUR nominal gleich behandelt).
# ---------------------------------------------------------------------------------------------
SAISON = {
    "flach": [1.0] * 12,
    "winter": [1.35, 1.30, 1.15, 0.85, 0.80, 0.85, 0.90, 0.90, 0.90, 0.95, 1.00, 1.05],
    "sommer": [0.85, 0.85, 0.95, 1.05, 1.10, 1.15, 1.20, 1.20, 1.05, 0.95, 0.85, 0.80],
    "bau": [0.70, 0.75, 0.95, 1.10, 1.20, 1.20, 1.15, 1.15, 1.15, 1.05, 0.85, 0.75],
    "dezember": [0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 1.00, 1.05, 1.40],
    "jahresende": [0.85, 0.85, 0.90, 0.95, 0.95, 1.00, 0.95, 0.90, 1.05, 1.15, 1.30, 1.45],
    "heizung": [1.20, 1.10, 0.95, 0.85, 0.80, 0.80, 0.80, 0.85, 1.05, 1.25, 1.25, 1.10],
}

SCHADENARTEN = [
    # id, bezeichnung, {produkt: {CH: anteil, DE: anteil}}, mu, sigma, null, abwehr, med, p90, saison
    ("SA-SACH-BEW", "Sachschaden Dritter an beweglichen Sachen",
     {"HP-PRIV": (55, 52), "HP-BETR": (30, 30), "HP-BERUF": (2, 2)}, 6.1, 0.9, 20, 15, 35, 120, "sommer"),
    ("SA-SACH-IMMO", "Sachschaden an Immobilie / Mietsache (Wasser, Brand, Parkett)",
     {"HP-PRIV": (18, 20), "HP-BETR": (15, 15), "HP-BERUF": (1, 1)}, 7.5, 1.0, 15, 15, 60, 240, "heizung"),
    ("SA-BEARB", "Bearbeitungs- / Obhutsschaden (Tätigkeitsschaden)",
     {"HP-BETR": (25, 25)}, 7.7, 1.0, 15, 20, 90, 300, "bau"),
    ("SA-PERS-LEICHT", "Personenschaden leicht (ambulant, unter 30 Tage Arbeitsunfähigkeit)",
     {"HP-PRIV": (12, 12), "HP-BETR": (12, 12)}, 7.1, 1.0, 25, 15, 120, 400, "winter"),
    ("SA-PERS-SCHWER", "Personenschaden schwer (stationär, Dauerschaden)",
     {"HP-PRIV": (2, 2), "HP-BETR": (3, 3)}, 10.7, 1.3, 10, 15, 1500, 2900, "winter"),
    ("SA-VERM", "Reiner Vermögensschaden",
     {"HP-PRIV": (3, 4), "HP-BETR": (8, 8)}, 6.8, 1.2, 40, 20, 90, 365, "flach"),
    ("SA-VERM-ARCH", "Vermögensschaden Planungsfehler (Architekten / Ingenieure)",
     {"HP-BERUF": (37, 36)}, 9.8, 1.2, 45, 45, 420, 1400, "jahresende"),
    ("SA-VERM-TREU", "Vermögensschaden Treuhand / Steuerberatung",
     {"HP-BERUF": (27, 30)}, 9.1, 1.2, 40, 45, 400, 1200, "jahresende"),
    ("SA-VERM-IT", "Vermögensschaden IT-Dienstleistung / Software",
     {"HP-BERUF": (21, 21)}, 9.6, 1.3, 50, 45, 380, 1100, "jahresende"),
    ("SA-VERM-BER", "Vermögensschaden Unternehmensberatung",
     {"HP-BERUF": (12, 10)}, 9.4, 1.2, 55, 45, 400, 1300, "jahresende"),
    ("SA-PRODUKT", "Produkthaftpflichtschaden",
     {"HP-BETR": (5, 5)}, 8.3, 1.4, 30, 20, 180, 700, "flach"),
    ("SA-UMWELT", "Umwelt- / Gewässerschaden",
     {"HP-PRIV": (1, 1), "HP-BETR": (2, 2)}, 9.4, 1.1, 25, 20, 240, 900, "heizung"),
    ("SA-TIER", "Tierhalterschaden (Hund, Pferd)",
     {"HP-PRIV": (9, 9)}, 6.4, 1.2, 20, 15, 45, 200, "sommer"),
    ("SA-SCHLUESSEL", "Schlüsselverlust (Sublimit)",
     {"HP-PRIV": (0, 0), "HP-BETR": (0, 0)}, 6.9, 0.7, 10, 10, 30, 90, "flach"),
]
# Schluesselverlust ist in SA-SACH-IMMO enthalten (Planung 01 §4.4.1); die Zeile mit Anteil 0 dient
# nur als Referenz fuer das Sublimit und den eigenen Ursachencode.

# ---------------------------------------------------------------------------------------------
# Dokumenttypen (Planung 01 §5.2, §5.3, Mengen §5.4)
# code, name, bereich, phase, format, laenge, anzahl_pro_1000, sprache, quellsystem, ground_truth
# ---------------------------------------------------------------------------------------------
DOKUMENTTYPEN = [
    ("V01", "Offerte / Angebot", "vertrag", "angebot", "pdf", "2-4", 1300, "de-CH;de-DE;fr;it", "HAPO;MINT", True),
    ("V02", "Antrag / Antragsformular", "vertrag", "antrag", "pdf;scan;json", "2-10", 1000, "de-CH;de-DE;fr;it", "DOKU;MINT", True),
    ("V03", "Betriebsbeschreibung / Risikofragebogen", "vertrag", "antrag", "pdf;docx;eml", "3-8", 250, "de-CH;de-DE", "DOKU;MINT", True),
    ("V04", "Beratungsprotokoll (nur DE)", "vertrag", "antrag", "pdf;scan", "1-3", 480, "de-DE", "DOKU;MINT", False),
    ("V05", "Produktinformationsblatt / IPID / Kundeninformation", "vertrag", "antrag", "pdf", "2-5", 1000, "de-CH;de-DE;fr", "DOKU;MINT", False),
    ("V06", "Police / Versicherungsschein", "vertrag", "policierung", "pdf;scan", "2-8", 1000, "de-CH;de-DE;fr;it", "HAPO;MINT", True),
    ("V07", "Allgemeine Versicherungsbedingungen (AVB CH / AHB DE)", "vertrag", "policierung", "pdf", "12-30", 1000, "de-CH;de-DE;fr", "DOKU;MINT", False),
    ("V08", "Besondere Bedingungen / Klauseln", "vertrag", "policierung", "pdf", "1-6", 600, "de-CH;de-DE", "DOKU;MINT", False),
    ("V09", "Nachtrag / Nachtragspolice", "vertrag", "bestand", "pdf", "1-3", 450, "de-CH;de-DE;fr", "HAPO;MINT", True),
    ("V10", "Deckungsbestätigung / Versicherungsnachweis", "vertrag", "bestand", "pdf", "1", 150, "de-CH;de-DE", "HAPO;MINT", False),
    ("V11", "Prämienrechnung / Beitragsrechnung", "vertrag", "inkasso", "pdf", "1-2", 2500, "de-CH;de-DE;fr;it", "HAPO;MINT", True),
    ("V12", "Zahlungserinnerung / Mahnung (Stufe 1-3)", "vertrag", "inkasso", "pdf", "1", 100, "de-CH;de-DE;fr", "HAPO;MINT", True),
    ("V13", "Mitteilung Deckungsunterbruch / Leistungsfreiheit", "vertrag", "inkasso", "pdf", "1", 15, "de-CH;de-DE", "HAPO", False),
    ("V14", "Kündigungsschreiben Versicherungsnehmer", "vertrag", "beendigung", "scan;eml;json", "0.5-1", 95, "de-CH;de-DE;fr;it", "DOKU;MINT", True),
    ("V15", "Kündigungsbestätigung / Kündigungsablehnung", "vertrag", "beendigung", "pdf", "1", 95, "de-CH;de-DE;fr", "HAPO;MINT", False),
    ("V16", "Kündigung durch Versicherer", "vertrag", "beendigung", "pdf", "1-2", 8, "de-CH;de-DE", "HAPO;MINT", True),
    ("V17", "Aufhebungsvereinbarung / Storno-Mitteilung", "vertrag", "beendigung", "pdf", "1", 20, "de-CH;de-DE", "HAPO;MINT", False),
    ("V18", "Vollmacht / Maklermandat", "vertrag", "antrag", "pdf;scan", "1-2", 220, "de-CH;de-DE", "DOKU;MINT", False),
    ("V19", "Umsatz- / Lohnsummenmeldung", "vertrag", "bestand", "pdf;eml;xlsx", "1-2", 900, "de-CH;de-DE", "DOKU;MINT", True),
    ("V20", "Korrespondenz allgemein (Vertrag)", "vertrag", "bestand", "eml;scan", "0.5-2", 400, "de-CH;de-DE;fr;it;en", "DOKU;MINT", False),
    ("V21", "Vorversicherer-Auskunft / Schadenfreiheitsbescheinigung", "vertrag", "antrag", "pdf", "1", 180, "de-CH;de-DE", "DOKU", True),
    ("V22", "Bonitäts- / Sanktionsprüfung (intern)", "vertrag", "antrag", "pdf", "1-3", 120, "de-CH;de-DE", "MINT", False),
    ("S01", "Schadenmeldung Versicherungsnehmer (Formular / Portal / App)", "schaden", "meldung", "pdf;scan;json", "2-3", 750, "de-CH;de-DE;fr;it", "SILAS;DOKU;MINT", True),
    ("S02", "Schadenmeldung per E-Mail / Telefonnotiz", "schaden", "meldung", "eml;txt", "0.3-1", 250, "de-CH;de-DE;fr;it", "SILAS;MINT", True),
    ("S03", "Anspruchsschreiben Geschädigter", "schaden", "meldung", "scan;eml", "1-2", 700, "de-CH;de-DE;fr;it", "DOKU;MINT", True),
    ("S04", "Anwaltsschreiben Geschädigtenvertreter", "schaden", "haftungspruefung", "pdf", "2-6", 250, "de-CH;de-DE;fr", "DOKU;MINT", True),
    ("S05", "Stellungnahme Versicherungsnehmer", "schaden", "erfassung", "eml;scan", "0.5-2", 500, "de-CH;de-DE;fr;it", "DOKU;MINT", True),
    ("S06", "Fotos (Platzhalter mit EXIF)", "schaden", "erfassung", "jpg", "1-10", 2500, "", "DOKU;MINT", True),
    ("S07", "Kostenvoranschlag / Reparaturofferte", "schaden", "regulierung", "pdf;scan;jpg", "1-2", 700, "de-CH;de-DE;fr;it", "DOKU;MINT", True),
    ("S08", "Rechnung / Quittung / Kaufbeleg", "schaden", "regulierung", "pdf;scan;jpg", "1", 700, "de-CH;de-DE;fr;it", "DOKU;MINT", True),
    ("S09", "Gutachten Sachverständiger (Sach)", "schaden", "regulierung", "pdf", "5-20", 60, "de-CH;de-DE", "DOKU;MINT", True),
    ("S10", "Arztbericht / Arztzeugnis / medizinisches Gutachten", "schaden", "regulierung", "pdf;scan", "1-40", 140, "de-CH;de-DE;fr", "DOKU;MINT", True),
    ("S11", "Polizeirapport / Unfallprotokoll", "schaden", "haftungspruefung", "pdf;scan", "2-6", 50, "de-CH;de-DE;fr;it", "DOKU", True),
    ("S12", "Zeugenaussage / Bestätigung Dritter", "schaden", "haftungspruefung", "eml;scan", "0.5-1", 120, "de-CH;de-DE;fr;it", "DOKU;MINT", False),
    ("S13", "Deckungszusage / Deckungsvorbehalt / Deckungsablehnung", "schaden", "deckungspruefung", "pdf", "1-2", 1000, "de-CH;de-DE;fr;it", "SILAS;MINT", True),
    ("S14", "Schreiben an Geschädigten (Haftung)", "schaden", "haftungspruefung", "pdf", "1-2", 900, "de-CH;de-DE;fr;it", "SILAS;MINT", True),
    ("S15", "Vergleichsvereinbarung / Abfindungserklärung", "schaden", "regulierung", "pdf;scan", "1-3", 80, "de-CH;de-DE;fr", "DOKU;MINT", True),
    ("S16", "Zahlungsavis / Zahlungsmitteilung", "schaden", "regulierung", "pdf", "1", 800, "de-CH;de-DE;fr;it", "SILAS;MINT", True),
    ("S17", "Regressforderung eingehend (Sozialversicherer)", "schaden", "regress", "pdf", "2-5", 60, "de-CH;de-DE;fr", "DOKU;MINT", True),
    ("S18", "Regressschreiben ausgehend", "schaden", "regress", "pdf", "1-2", 30, "de-CH;de-DE", "SILAS;MINT", False),
    ("S19", "Interne Schadennotiz / Bearbeitungsjournal", "schaden", "erfassung", "txt", "0.2-3", 1000, "de-CH;de-DE", "SILAS;MINT", True),
    ("S20", "Interne Haftungs- / Deckungsbeurteilung (Memo)", "schaden", "haftungspruefung", "docx;pdf", "1-4", 40, "de-CH;de-DE", "DOKU;MINT", True),
    ("S21", "Reserveprotokoll / Grossschadenmeldung", "schaden", "regulierung", "pdf", "1-3", 12, "de-CH;de-DE", "SILAS;MINT", False),
    ("S22", "Klageschrift / Klageantwort / Urteil", "schaden", "abwehr", "pdf", "10-40", 5, "de-CH;de-DE", "DOKU", False),
    ("S23", "Anwaltsrechnung / Gutachterrechnung", "schaden", "regulierung", "pdf", "1-2", 180, "de-CH;de-DE;fr", "DOKU;MINT", True),
    ("S24", "Betrugsprüfungsbericht (intern)", "schaden", "betrugspruefung", "pdf;docx", "2-6", 15, "de-CH;de-DE", "DOKU;MINT", True),
    ("S25", "Beschwerde / Anfrage Ombudsstelle", "schaden", "beschwerde", "scan;eml", "1-3", 25, "de-CH;de-DE;fr;it", "DOKU;MINT", True),
    ("S26", "Abschlussschreiben", "schaden", "abschluss", "pdf", "1", 850, "de-CH;de-DE;fr;it", "SILAS;MINT", False),
    ("S27", "Schadenmeldung an Rückversicherer", "schaden", "regulierung", "pdf", "1-2", 3, "de-CH;de-DE", "SILAS", False),
]

# ---------------------------------------------------------------------------------------------
# Lebenszyklusraten (Planung 01 §3.4), je Produkt x Markt x Kanal x Herkunft x Jahr
# ---------------------------------------------------------------------------------------------
BASIS = {  # produkt: (neugeschaeft, storno CH, storno DE, nachtrag, mahn, kuendigung_vu)
    "HP-PRIV": (10.0, 6.0, 11.0, 0.15, 7.5, 0.2),
    "HP-BETR": (12.5, 10.0, 10.0, 0.60, 10.0, 0.5),
    "HP-BERUF": (12.5, 10.0, 10.0, 0.40, 5.0, 0.3),
}
KANAL_FAKTOR = {  # kanal: (neugeschaeft, storno, mahn)
    "agentur": (1.00, 0.85, 0.90),
    "makler": (1.10, 1.05, 0.80),
    "direkt": (1.30, 1.35, 1.25),
    "bank": (0.70, 0.90, 0.95),
}
JAHR_TREND = {2016: 1.00, 2017: 1.00, 2018: 1.02, 2019: 1.03, 2020: 0.92, 2021: 1.05, 2022: 1.05,
              2023: 1.04, 2024: 1.06, 2025: 1.10}


def lebenszyklus() -> list[list]:
    zeilen = []
    for produkt, (ng, st_ch, st_de, nt, mahn, kvu) in BASIS.items():
        for markt in ("CH", "DE"):
            storno_basis = st_ch if markt == "CH" else st_de
            for kanal, (f_ng, f_st, f_mahn) in KANAL_FAKTOR.items():
                for jahr in range(2016, 2026):
                    herkuenfte = ["alle"] if jahr < 2021 else ["pfefferminz", "minzia"]
                    for herkunft in herkuenfte:
                        if herkunft == "minzia" and not (produkt == "HP-PRIV" and kanal == "direkt"):
                            continue  # Minzia hat bis 2024 nur Privathaftpflicht im Direktkanal
                        if herkunft == "minzia" and jahr < 2021:
                            continue
                        trend = JAHR_TREND[jahr]
                        neug = ng * f_ng * (1.6 if herkunft == "minzia" else 1.0) * (0.9 if jahr == 2020 else 1.0)
                        storno = storno_basis * f_st * trend
                        if herkunft == "minzia":
                            storno *= 1.25  # junge, wechselfreudige Kundschaft
                        if jahr == 2025 and herkunft == "pfefferminz":
                            storno *= 1.30  # Fusionseffekt: Ex-Pfefferminz-Kunden kuendigen haeufiger
                        if jahr == 2025 and herkunft == "minzia":
                            storno *= 1.10
                        mahnr = mahn * f_mahn * (1.15 if jahr in (2020, 2023) else 1.0)
                        bem = ""
                        if jahr == 2025 and herkunft == "pfefferminz":
                            bem = "Fusionseffekt: Praemienharmonisierung und Systemmigration"
                        elif jahr == 2020:
                            bem = "Pandemiejahr: weniger Neugeschaeft, mehr Mahnungen"
                        zeilen.append([produkt, markt, kanal, herkunft, jahr, round(neug, 2), round(storno, 2),
                                       round(nt, 2), round(mahnr, 2), round(kvu, 2), bem])
    return zeilen


def schreibe(pfad: Path, spalten: list[str], zeilen: list[list]) -> None:
    with pfad.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(spalten)
        w.writerows(zeilen)
    print(f"{pfad.relative_to(ROOT)}: {len(zeilen)} Zeilen")


def main() -> None:
    HP.mkdir(parents=True, exist_ok=True)

    zeilen = []
    for i, (nace, bez, klasse, anteil, bem) in enumerate(BRANCHEN, start=1):
        status = zeichnungsstatus(klasse, bem)
        zeilen.append([f"BK-{i:03d}", bez, nace, nace, klasse, PRAEMIENSATZ_PROMILLE[klasse], status, anteil,
                       "" if bem == "abgelehnt" else bem])
    assert len(zeilen) >= 60
    schreibe(HP / "branchenklassen.csv",
             ["branche_id", "bezeichnung_de", "noga_code", "wz_code", "risikoklasse", "grundpraemiensatz_promille",
              "zeichnungsstatus", "anteil_bestand_pct", "bemerkung"], zeilen)

    schreibe(HP / "plz_zonen.csv",
             ["markt", "tarifzone", "bezeichnung", "faktor_hp_priv", "faktor_hp_betr", "faktor_hp_beruf", "begruendung"],
             [list(z) for z in PLZ_ZONEN])

    zeilen = []
    monate = ["jan", "feb", "mar", "apr", "mai", "jun", "jul", "aug", "sep", "okt", "nov", "dez"]
    for sid, bez, anteile, mu, sigma, null, abwehr, med, p90, saison in SCHADENARTEN:
        for produkt, (a_ch, a_de) in anteile.items():
            for markt, anteil in (("CH", a_ch), ("DE", a_de)):
                zeilen.append([sid, bez, produkt, markt, anteil, "CHF" if markt == "CH" else "EUR", mu, sigma, null,
                               abwehr, med, p90, *SAISON[saison]])
    schreibe(HP / "schadenarten.csv",
             ["schadenart_id", "bezeichnung", "produkt", "markt", "anteil_pct", "waehrung", "lognormal_mu",
              "lognormal_sigma", "nullschaden_anteil_pct", "abwehrquote_pct", "abwicklungsdauer_median_tage",
              "abwicklungsdauer_p90_tage", *[f"saison_{m}" for m in monate]], zeilen)

    zeilen = [[c, n, b, ph, f, ln, anz, sp, qs, str(gt).lower()] for c, n, b, ph, f, ln, anz, sp, qs, gt in DOKUMENTTYPEN]
    assert len(zeilen) == 49
    schreibe(HP / "dokumenttypen.csv",
             ["code", "name", "bereich", "phase", "format", "laenge_seiten_typisch", "anzahl_pro_1000", "sprache",
              "quellsystem", "ground_truth_json"], zeilen)

    schreibe(HP / "lebenszyklus_raten.csv",
             ["produkt", "markt", "kanal", "herkunft", "jahr", "neugeschaeft_rate_pct", "storno_rate_pct",
              "nachtrag_rate", "mahn_rate_pct", "kuendigung_vu_rate_pct", "bemerkung"], lebenszyklus())


if __name__ == "__main__":
    main()
