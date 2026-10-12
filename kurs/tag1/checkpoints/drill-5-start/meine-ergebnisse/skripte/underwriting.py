"""Erzeugt die Daten fuer den Cockpit-Reiter «Underwriting».

Liest die Entscheidungsvorlagen unter meine-ergebnisse/ (Dr. Nazari, Katrin
Brandes, Bruno Pedrazzini, Lea Hartwig) und stellt daneben den Regelpfad zusammen, den die
Annahmerichtlinie Leben (RW-LV-ARL-2025) und die Kompetenzordnung (RW-GRUPPE-R08-2025)
fuer jeden Antrag vorschreiben: Pruefumfang, Gewicht, Nikotin, Beruf, Vorerkrankungen,
Freizeit, Kombination/Risikoklasse und Kompetenz. Schreibt eine JavaScript-Konstante
nach meine-ergebnisse/cockpit-daten/underwriting.js, damit das Cockpit ohne Server
im Browser laeuft.
"""

import json
from pathlib import Path

ERGEBNISSE = Path(__file__).resolve().parents[1]
AUSGABE = ERGEBNISSE / "cockpit-daten" / "underwriting.js"


def maskiere(text):
    return text.replace("<", "‹").replace(">", "›")


def lies_vorlage(dateiname):
    pfad = ERGEBNISSE / dateiname
    return maskiere(pfad.read_text(encoding="utf-8").strip())


# --- Regelpfad je Antrag: Schrittfolge vom Pruefumfang bis zur Kompetenz ---
# "mensch": True markiert den Schritt, an dem eine natuerliche Person entscheiden muss.

REGELPFAD_NAZARI = [
    {"schritt": "Prüfumfang", "paragraf": "§ 2 ARL-2025",
     "ergebnis": "Summe EUR 1'200'000.00, Alter 51 (unter 55) → Stufe bis EUR 1'500'000.00: Fragebogen, Hausarztzeugnis, Vertrauensarzt, Labor. Alle vier Unterlagen liegen vor."},
    {"schritt": "Gewicht", "paragraf": "§ 3 ARL-2025",
     "ergebnis": "BMI 26.9, Altersgruppe 40 bis 59, Spanne 18.5 bis 27.9 → Zuschlag 0.0 %."},
    {"schritt": "Nikotin", "paragraf": "§ 4 ARL-2025",
     "ergebnis": "Angabe Nein, Cotinin negativ → Nichtrauchertarif, 0.0 %."},
    {"schritt": "Beruf", "paragraf": "§ 5 ARL-2025",
     "ergebnis": "Keine Zusatzversicherung Erwerbs- oder Berufsunfähigkeit → nicht anwendbar."},
    {"schritt": "Vorerkrankungen", "paragraf": "§ 6 ARL-2025, Tabelle 6.1",
     "ergebnis": "Bluthochdruck seit 2021, RR unter 140/90, Behandlungsbeginn unter 5 Jahren, Summe über EUR 750'000.00 → ~~Zuschlag 25.0 % bis 50.0 % (Spanne, Vorschlag 37.5 %)~~ Zuschlag 50.0 % (entschieden durch mich, wegen LDL und Familienanamnese). Bandscheibenvorfall 2019 ohne Operation → 0.0 %."},
    {"schritt": "Freizeit", "paragraf": "§ 7 ARL-2025",
     "ergebnis": "Skitouren auf markierten Routen → 0.0 ‰."},
    {"schritt": "Kombination und Risikoklasse", "paragraf": "§ 8 ARL-2025",
     "ergebnis": "~~Gesamtzuschlag 25.0 % bis 50.0 % (Vorschlag 37.5 %)~~ Gesamtzuschlag 50.0 % (entschieden durch mich) → Risikoklasse 2, leicht erhöht."},
    {"schritt": "Kompetenz", "paragraf": "§ 9 Nr. 1 und Nr. 3 ARL-2025, § 4 Kompetenzordnung",
     "ergebnis": "Zuschlag wird nie automatisiert entschieden; Summe über EUR 750'000.00 → Gesellschaftsarzt entscheidet. Entscheid getroffen: 50.0 % Zuschlag (entschieden durch mich).",
     "mensch": True},
]

REGELPFAD_BRANDES = [
    {"schritt": "Prüfumfang", "paragraf": "§ 2 ARL-2025",
     "ergebnis": "Summe EUR 400'000.00, Alter 44 (unter 55) → Stufe bis EUR 750'000.00: Fragebogen und Hausarztzeugnis. Beide Unterlagen liegen vor, ein Cotinin-Test ist unterhalb EUR 750'000.00 nicht nötig."},
    {"schritt": "Gewicht", "paragraf": "§ 3 ARL-2025",
     "ergebnis": "BMI 31.2, Altersgruppe 40 bis 59, Spanne 30.0 bis 32.9 → Zuschlag 25.0 %."},
    {"schritt": "Nikotin", "paragraf": "§ 4 ARL-2025",
     "ergebnis": "Ca. 15 Zigaretten pro Tag → Rauchertarif, kein zusätzlicher Prozentzuschlag (nicht über 20 pro Tag)."},
    {"schritt": "Beruf", "paragraf": "§ 5 ARL-2025",
     "ergebnis": "Keine Zusatzversicherung Erwerbs- oder Berufsunfähigkeit → nicht anwendbar."},
    {"schritt": "Vorerkrankungen", "paragraf": "§ 6 ARL-2025",
     "ergebnis": "Asthma bronchiale leicht, gut kontrolliert → 0.0 %. Diabetes mellitus Typ 2, HbA1c 6.6 % (Laborbefund liegt vor) → Zuschlag 75.0 %."},
    {"schritt": "Freizeit", "paragraf": "§ 7 ARL-2025",
     "ergebnis": "Tauchen bis 30 m mit Tauchschein → 0.0 ‰."},
    {"schritt": "Kombination und Risikoklasse", "paragraf": "§ 8 ARL-2025",
     "ergebnis": "Gesamtzuschlag 25.0 % + 75.0 % = 100.0 % → Risikoklasse 3, erhöht."},
    {"schritt": "Kompetenz", "paragraf": "§ 9 Nr. 1 und Nr. 2 ARL-2025, § 4 Kompetenzordnung",
     "ergebnis": "Zuschlag wird nie automatisiert entschieden; Risikoklasse 3 und Summe bis EUR 750'000.00 → Sachbearbeitung entscheidet.",
     "mensch": True},
]

REGELPFAD_PEDRAZZINI = [
    {"schritt": "Prüfumfang", "paragraf": "§ 2 ARL-2025",
     "ergebnis": "Summe CHF 600'000.00 läge in der Stufe bis CHF 750'000.00; weil Herr Pedrazzini bei Antragseingang 58 Jahre (55 oder älter) ist, gilt die nächststrengere Stufe bis CHF 1'500'000.00: Fragebogen, Hausarztzeugnis, Vertrauensarzt, Labor. Vertrauensarzt und Labor der Gesellschaft fehlen noch – Prüfumfang unvollständig."},
    {"schritt": "Gewicht", "paragraf": "§ 3 ARL-2025",
     "ergebnis": "BMI 38.4, Altersgruppe 40 bis 59, Spanne 36.0 bis 39.9 → Zuschlag 150.0 %, ärztliches Zeugnis obligatorisch (liegt vor)."},
    {"schritt": "Nikotin", "paragraf": "§ 4 ARL-2025",
     "ergebnis": "Rauchstopp Mai 2022, mehr als 12 Monate zurück → Nichtrauchertarif, 0.0 %."},
    {"schritt": "Beruf", "paragraf": "§ 5 ARL-2025",
     "ergebnis": "Keine Zusatzversicherung Erwerbsunfähigkeit → nicht anwendbar."},
    {"schritt": "Vorerkrankungen", "paragraf": "§ 6 ARL-2025",
     "ergebnis": "Myokardinfarkt 04/2022, EF 55 %, älter als 2 Jahre → Zuschlag 150.0 % (Facharztnachweis liegt vor). Hypercholesterinämie unter Statin → 0.0 %."},
    {"schritt": "Freizeit", "paragraf": "§ 7 ARL-2025",
     "ergebnis": "Keine gefährliche Sportart (Wandern) → 0.0 ‰."},
    {"schritt": "Kombination und Risikoklasse", "paragraf": "§ 8 ARL-2025",
     "ergebnis": "Gesamtzuschlag 150.0 % + 150.0 % = 300.0 %, über 251 % → Risikoklasse 5, Ablehnung."},
    {"schritt": "Kompetenz", "paragraf": "§ 9 Nr. 1 und Nr. 3a ARL-2025, § 5 Nr. 2 Kompetenzordnung",
     "ergebnis": "Ablehnungen werden nie automatisiert entschieden; Gesellschaftsarzt entscheidet (Rückversicherung nicht nötig, Summe unter CHF 1'500'000.00). Entschieden durch mich: Vertrauensarzt und Labor werden zuerst angefordert, bevor über Annahme, Zuschlag oder Ablehnung entschieden wird.",
     "mensch": True},
]

REGELPFAD_HARTWIG = [
    {"schritt": "Prüfumfang", "paragraf": "§ 2 ARL-2025",
     "ergebnis": "Summe CHF 250'000.00, Alter 34 (unter 55) → Stufe bis CHF 300'000.00: nur Fragebogen. Die Gesundheitserklärung liegt unterschrieben vor, Prüfumfang vollständig erfüllt."},
    {"schritt": "Gewicht", "paragraf": "§ 3 ARL-2025",
     "ergebnis": "BMI 22.5, Altersgruppe 18 bis 39, Spanne 18.5 bis 27.9 → Zuschlag 0.0 %."},
    {"schritt": "Nikotin", "paragraf": "§ 4 ARL-2025",
     "ergebnis": "Angabe «nie geraucht» → Nichtrauchertarif, 0.0 %."},
    {"schritt": "Beruf", "paragraf": "§ 5 ARL-2025",
     "ergebnis": "Keine Zusatzversicherung Erwerbsunfähigkeit beantragt → nicht anwendbar."},
    {"schritt": "Vorerkrankungen", "paragraf": "§ 6 ARL-2025",
     "ergebnis": "Heuschnupfen im Frühling (J30, Allergische Rhinitis), Nasenspray bei Bedarf → NORMAL, 0.0 %. Alle übrigen Fragen mit Nein beantwortet."},
    {"schritt": "Freizeit", "paragraf": "§ 7 ARL-2025",
     "ergebnis": "Reiten in der Freizeit → 0.0 ‰, gilt als normal."},
    {"schritt": "Kombination und Risikoklasse", "paragraf": "§ 8 ARL-2025",
     "ergebnis": "Gesamtzuschlag 0.0 % → Risikoklasse 1, normal."},
    {"schritt": "Kompetenz", "paragraf": "§ 9 Nr. 1 ARL-2025, § 4 Kompetenzordnung",
     "ergebnis": "Risikoklasse 1, Summe bis CHF 400'000.00, keine EU/BU-Rente, ausschliesslich positiver Entscheid ohne Erschwerung → automatische Annahme durch die MINT Underwriting-Engine v2 (Modellinventar MI-03), mit 10 Prozent manueller Stichprobe."},
]

ANTRAEGE = [
    {
        "id": "nazari",
        "antragsteller": "Dr. Farid Nazari",
        "antragId": "ANT-00000602",
        "summeText": "EUR 1'200'000.00",
        "risikoklasse": 2,
        "risikoklasseText": "2 – leicht erhöht",
        "empfehlung": "Annahme mit Zuschlag 50.0 % (entschieden durch mich)",
        "regelpfad": REGELPFAD_NAZARI,
        "vorlage": lies_vorlage("entscheidungsvorlage-nazari.md"),
    },
    {
        "id": "brandes",
        "antragsteller": "Katrin Brandes",
        "antragId": "ANT-00009001",
        "summeText": "EUR 400'000.00",
        "risikoklasse": 3,
        "risikoklasseText": "3 – erhöht",
        "empfehlung": "Annahme mit Zuschlag 100.0 %",
        "regelpfad": REGELPFAD_BRANDES,
        "vorlage": lies_vorlage("entscheidungsvorlage-brandes.md"),
    },
    {
        "id": "pedrazzini",
        "antragsteller": "Bruno Pedrazzini",
        "antragId": "ANT-00009002",
        "summeText": "CHF 600'000.00",
        "risikoklasse": 5,
        "risikoklasseText": "5 (Berechnung, Entscheid ausstehend)",
        "empfehlung": "Vertrauensarzt und Labor zuerst angefordert (entschieden durch mich)",
        "regelpfad": REGELPFAD_PEDRAZZINI,
        "vorlage": lies_vorlage("entscheidungsvorlage-pedrazzini.md"),
    },
    {
        "id": "hartwig",
        "antragsteller": "Lea Hartwig",
        "antragId": "ANT-00009003",
        "summeText": "CHF 250'000.00",
        "risikoklasse": 1,
        "risikoklasseText": "1 – normal",
        "empfehlung": "Automatische Annahme ohne Zuschlag",
        "regelpfad": REGELPFAD_HARTWIG,
        "vorlage": lies_vorlage("entscheidungsvorlage-hartwig.md"),
    },
]

DATEN = {
    "stichtag": "Bewertungsstand je Antrag, siehe Entscheidungsvorlage",
    "regel": "Regelpfad nach der Annahmerichtlinie Leben (RW-LV-ARL-2025) und der Kompetenzordnung (RW-GRUPPE-R08-2025): Prüfumfang, Gewicht, Nikotin, Beruf, Vorerkrankungen, Freizeit, Kombination/Risikoklasse, Kompetenz. Der rot markierte Schritt zeigt, wo eine natürliche Person entscheidet, nie ein System.",
    "antraege": ANTRAEGE,
}

AUSGABE.parent.mkdir(parents=True, exist_ok=True)
AUSGABE.write_text("const UNDERWRITING_DATEN = " + json.dumps(DATEN, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
print(f"geschrieben: {AUSGABE} ({len(ANTRAEGE)} Anträge)")
