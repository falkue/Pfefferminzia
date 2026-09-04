"""Kleine, im Code gefuehrte Referenzlisten (Berufe, Codes, Kanaele), die keine eigene CSV rechtfertigen.

Alles Fiktive und Fachliche mit Aussenwirkung liegt unter ``data/reference/``; hier stehen nur
Kodierungen und Ziehungsgewichte, die der Generator intern braucht.
"""

from __future__ import annotations

# (code, text_de, berufsgruppe_eu_bu 1-5, gewicht, selbstaendig_anteil)
BERUFE: list[tuple[str, str, int, float, float]] = [
    ("B01", "Kaufmännische Angestellte / Kaufmännischer Angestellter", 2, 12.0, 0.02),
    ("B02", "Informatikerin / Informatiker", 1, 6.0, 0.10),
    ("B03", "Lehrerin / Lehrer", 1, 5.0, 0.0),
    ("B04", "Pflegefachfrau / Pflegefachmann", 3, 5.0, 0.02),
    ("B05", "Verkäuferin / Verkäufer", 2, 6.0, 0.03),
    ("B06", "Elektroinstallateurin / Elektroinstallateur", 3, 3.0, 0.15),
    ("B07", "Sanitärinstallateurin / Sanitärinstallateur", 3, 2.5, 0.18),
    ("B08", "Schreinerin / Schreiner", 4, 2.5, 0.20),
    ("B09", "Maurerin / Maurer", 4, 2.0, 0.08),
    ("B10", "Ingenieurin / Ingenieur", 1, 4.0, 0.08),
    ("B11", "Ärztin / Arzt", 1, 1.5, 0.35),
    ("B12", "Juristin / Jurist", 1, 1.5, 0.25),
    ("B13", "Treuhänderin / Treuhänder", 1, 1.5, 0.30),
    ("B14", "Architektin / Architekt", 1, 1.2, 0.40),
    ("B15", "Köchin / Koch", 3, 2.5, 0.10),
    ("B16", "Chauffeuse / Chauffeur", 3, 2.5, 0.12),
    ("B17", "Coiffeuse / Coiffeur", 2, 1.5, 0.35),
    ("B18", "Physiotherapeutin / Physiotherapeut", 2, 1.5, 0.30),
    ("B19", "Landwirtin / Landwirt", 4, 1.5, 0.85),
    ("B20", "Polizistin / Polizist", 3, 1.0, 0.0),
    ("B21", "Beraterin / Berater", 1, 2.5, 0.35),
    ("B22", "Studentin / Student", 2, 3.0, 0.0),
    ("B23", "Rentnerin / Rentner", 2, 9.0, 0.0),
    ("B24", "Hausfrau / Hausmann", 2, 2.0, 0.0),
    ("B25", "Mechanikerin / Mechaniker", 3, 2.5, 0.10),
    ("B26", "Logistikerin / Logistiker", 3, 2.5, 0.05),
    ("B27", "Grafikerin / Grafiker", 1, 1.2, 0.40),
    ("B28", "Bankangestellte / Bankangestellter", 1, 2.0, 0.0),
    ("B29", "Gerüstbauerin / Gerüstbauer", 5, 0.6, 0.10),
    ("B30", "Forstwartin / Forstwart", 5, 0.5, 0.05),
    ("B31", "Dachdeckerin / Dachdecker", 4, 1.0, 0.20),
    ("B32", "Malerin / Maler", 3, 1.8, 0.20),
    ("B33", "Apothekerin / Apotheker", 2, 0.8, 0.30),
    ("B34", "Sozialarbeiterin / Sozialarbeiter", 2, 1.5, 0.02),
    ("B35", "Verwaltungsangestellte / Verwaltungsangestellter", 2, 4.0, 0.0),
    ("B36", "Gastwirtin / Gastwirt", 3, 1.0, 0.80),
    ("B37", "Kunstschaffende / Kunstschaffender", 3, 0.6, 0.70),
    ("B38", "Pilotin / Pilot", 2, 0.2, 0.0),
    ("B39", "Berufsmusikerin / Berufsmusiker", 5, 0.3, 0.60),
    ("B40", "Selbständige Unternehmerin / Selbständiger Unternehmer", 2, 2.0, 1.0),
]

# Freitextvarianten fuer MINT-Selbstregistrierung (DQ-21): code -> Varianten
BERUF_FREITEXT: dict[str, list[str]] = {
    "B01": ["Kaufmann", "kaufm. Angestellte", "Sachbearbeiterin", "Büro", "KV"],
    "B02": ["IT", "Informatik", "Software Engineer", "Dev", "Programmierer", "🧑‍💻"],
    "B03": ["Lehrer", "Lehrerin Primar", "Gymnasiallehrer", "Teacher"],
    "B04": ["Pflege", "Krankenschwester", "Pflegefachmann HF", "Nurse"],
    "B05": ["Verkauf", "Detailhandel", "Retail", "Verkäuferin"],
    "B10": ["Ingenieur", "Ing.", "Engineer", "Maschinenbauing."],
    "B21": ["Beratung", "Consultant", "Berater", "Unternehmensberatung"],
    "B22": ["Student", "Studi", "Studentin ETH", "studiere noch"],
    "B23": ["pensioniert", "Rentner", "Ruhestand", "AHV"],
    "B40": ["Selbständig", "selbstständig", "Selbstständige", "Eigenes Geschäft", "Unternehmer"],
}

STORNO_GRUENDE: list[tuple[str, str, str, float]] = [
    # code, bezeichnung, status, gewicht (Kuendigung durch VN)
    ("K01", "Wechsel zu anderem Versicherer (Preis)", "GEKUENDIGT_VN", 34.0),
    ("K02", "Kündigung nach Prämienerhöhung", "GEKUENDIGT_VN", 14.0),
    ("K03", "Kündigung im Schadenfall durch VN", "GEKUENDIGT_VN", 6.0),
    ("K04", "Kündigung nach Ablehnung eines Schadens", "GEKUENDIGT_VN", 5.0),
    ("K05", "Wegzug ins Ausland", "GEKUENDIGT_VN", 4.0),
    ("K06", "Doppelversicherung / Zusammenlegung Haushalt", "GEKUENDIGT_VN", 8.0),
    ("K07", "Tod des Versicherungsnehmers", "STORNIERT", 3.0),
    ("K08", "Betriebsaufgabe", "GEKUENDIGT_VN", 4.0),
    ("K09", "Unzufriedenheit mit Service / Beschwerde", "GEKUENDIGT_VN", 5.0),
    ("K10", "Kündigung durch Versicherer im Schadenfall", "GEKUENDIGT_VU", 2.0),
    ("K11", "Kündigung durch Versicherer wegen Anzeigepflichtverletzung", "GEKUENDIGT_VU", 1.0),
    ("K12", "Storno wegen Nichtzahlung", "STORNIERT", 8.0),
    ("K13", "Widerruf innerhalb der Frist", "STORNIERT", 2.0),
    ("K14", "Rückkauf (Leben)", "RUECKKAUF", 0.0),
    ("K15", "Ablauf / Erleben (Leben)", "ABGELAUFEN", 0.0),
    ("K16", "Leistungsfall Tod (Leben)", "LEISTUNG_ERBRACHT", 0.0),
    ("K17", "Kündigung ohne Angabe von Gründen", "GEKUENDIGT_VN", 4.0),
]

# Codes der Altsysteme (Datenarchitektur 2.1 / 2.3)
PVS_GESCHLECHT = {"M": "1", "W": "2", "D": "9", "UNBEKANNT": "0"}
PVS_ZIVILSTAND = {"LEDIG": "1", "VERHEIRATET": "2", "GESCHIEDEN": "3", "VERWITWET": "4", "PARTNERSCHAFT": "5",
                  "UNBEKANNT": "0"}
PVS_ZAHLWEISE = {"JAEHRLICH": "1", "HALBJAEHRLICH": "2", "VIERTELJAEHRLICH": "4", "MONATLICH": "12"}
PVS_STATUS = {"AKTIV": "A", "RUHEND": "A", "GEKUENDIGT_VN": "S", "GEKUENDIGT_VU": "S", "STORNIERT": "S",
              "ABGELAUFEN": "E", "LEISTUNG_ERBRACHT": "L", "RUECKKAUF": "R", "ANTRAG": "P"}
PVS_STORNOGRUND = {"GEKUENDIGT_VN": "01", "GEKUENDIGT_VU": "02", "STORNIERT": "05"}
PVS_LANDKZ = {"CH": "756", "DE": "276"}

MINT_STATUS_V1 = {"AKTIV": "active", "RUHEND": "suspended", "GEKUENDIGT_VN": "cancelled",
                  "GEKUENDIGT_VU": "cancelled_by_insurer", "STORNIERT": "lapsed", "ABGELAUFEN": "expired",
                  "LEISTUNG_ERBRACHT": "claimed", "RUECKKAUF": "surrendered", "ANTRAG": "quote"}
MINT_STATUS_V2 = {k: v.upper() for k, v in MINT_STATUS_V1.items()}
MINT_STATUS_V3 = {"AKTIV": "ACTIVE", "RUHEND": "SUSPENDED", "GEKUENDIGT_VN": "TERMINATED",
                  "GEKUENDIGT_VU": "TERMINATED", "STORNIERT": "LAPSED", "ABGELAUFEN": "EXPIRED",
                  "LEISTUNG_ERBRACHT": "SETTLED", "RUECKKAUF": "SURRENDERED", "ANTRAG": "QUOTED"}

KANAELE = ("agentur", "makler", "direkt", "bank")
ZAHLUNGSWEISEN = ("JAEHRLICH", "HALBJAEHRLICH", "VIERTELJAEHRLICH", "MONATLICH")
