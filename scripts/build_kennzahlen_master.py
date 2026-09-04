"""Erzeugt die Kennzahlen-Masterdatei ``data/reference/kennzahlen_master.yaml``.

Aufruf: ``uv run python scripts/build_kennzahlen_master.py``

Die Masterdatei ist die einzige Quelle aller Unternehmenszahlen (Konventionen §2). Sie wird per Skript
erzeugt, damit Summen, Quoten und Absolutwerte rechnerisch zusammenpassen. Grundannahmen stammen aus
Planung 05 §1.3 und den Lebenszyklusraten der Sparten; abgeleitete Werte werden hier berechnet.
Alle Betraege in Millionen der jeweiligen Waehrung, sofern nicht anders angegeben.
"""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ZIEL = ROOT / "data" / "reference" / "kennzahlen_master.yaml"

KURS_EUR_CHF = {2021: 1.08, 2022: 1.00, 2023: 0.97, 2024: 0.95, 2025: 0.94}
JAHRE = [2021, 2022, 2023, 2024, 2025]

# Segmentbasis GJ 2025 (Planung 05 §1.3, Verträge in Tausend, Prämien in Mio. Landeswährung)
SEGMENTE_2025 = {
    # segment: (gesellschaft, sparte, produkt, markt, waehrung, praemie, vertraege_tsd, cr_oder_marge, kanalmix)
    "HP-PRIV-CH": ("PVAG", "HP", "HP-PRIV", "CH", "CHF", 210.0, 520, {"combined_ratio_pct": 91.0},
                   {"agentur": 45, "makler": 10, "direkt": 35, "bank": 10}),
    "HP-BETR-CH": ("PVAG", "HP", "HP-BETR", "CH", "CHF", 190.0, 68, {"combined_ratio_pct": 96.0},
                   {"agentur": 40, "makler": 55, "direkt": 5, "bank": 0}),
    "HP-PRIV-DE": ("PVAG-NL-DE", "HP", "HP-PRIV", "DE", "EUR", 165.0, 410, {"combined_ratio_pct": 94.0},
                   {"agentur": 0, "makler": 30, "direkt": 55, "bank": 15}),
    "HP-BETR-DE": ("PVAG-NL-DE", "HP", "HP-BETR", "DE", "EUR", 120.0, 39, {"combined_ratio_pct": 99.0},
                   {"agentur": 0, "makler": 75, "direkt": 25, "bank": 0}),
    "LV-RISK-CH": ("PLAG", "LV", "LV-RISK", "CH", "CHF", 240.0, 145, {"neugeschaeftsmarge_pct": 3.1},
                   {"agentur": 50, "makler": 25, "direkt": 5, "bank": 20}),
    "LV-VORS-RENTE-CH": ("PLAG", "LV", "LV-VORS;LV-RENTE", "CH", "CHF", 690.0, 118, {"neugeschaeftsmarge_pct": 1.8},
                         {"agentur": 55, "makler": 15, "direkt": 0, "bank": 30}),
    "LV-RISK-DE": ("PLDAG", "LV", "LV-RISK", "DE", "EUR", 95.0, 72, {"neugeschaeftsmarge_pct": 2.4},
                   {"agentur": 0, "makler": 50, "direkt": 35, "bank": 15}),
    "LV-VORS-RENTE-DE": ("PLDAG", "LV", "LV-VORS;LV-RENTE", "DE", "EUR", 310.0, 63, {"neugeschaeftsmarge_pct": 1.1},
                         {"agentur": 0, "makler": 60, "direkt": 5, "bank": 35}),
}
# Berufshaftpflicht ist in HP-BETR enthalten (Planung 05 fuehrt sie nicht separat); Anteil ca. 12 % der BETR-Praemie.

# Wachstumspfad 2021-2025 je Segment (Faktor auf den 2025-Wert), Pfefferminz-Historie
WACHSTUM = {2021: 0.90, 2022: 0.93, 2023: 0.95, 2024: 0.97, 2025: 1.00}
# Minzia: vermittelte Praemien (EUR Mio.) und aktive Policen (Tsd.), Privathaftpflicht DE Direkt; ab 2025 in HP-PRIV-DE enthalten
MINZIA = {2021: (6.0, 9), 2022: (14.0, 21), 2023: (24.0, 33), 2024: (38.0, 41)}

# Schaden-Kennzahlen HP 2025: Frequenz (Schaeden je Vertrag) und Durchschnittsschaden (Landeswaehrung)
SCHADEN = {"HP-PRIV-CH": (0.065, 3600), "HP-BETR-CH": (0.12, 13500), "HP-PRIV-DE": (0.07, 3500), "HP-BETR-DE": (0.13, 15000)}
KOSTENQUOTE_HP = {"HP-PRIV-CH": 33.0, "HP-BETR-CH": 38.0, "HP-PRIV-DE": 32.5, "HP-BETR-DE": 35.0}
STORNO = {"HP-PRIV-CH": 6.0, "HP-BETR-CH": 10.0, "HP-PRIV-DE": 11.0, "HP-BETR-DE": 10.0,
          "LV-RISK-CH": 4.3, "LV-VORS-RENTE-CH": 3.0, "LV-RISK-DE": 5.8, "LV-VORS-RENTE-DE": 3.5}
NEUGESCHAEFT = {"HP-PRIV-CH": 10.0, "HP-BETR-CH": 12.5, "HP-PRIV-DE": 13.0, "HP-BETR-DE": 12.5,
                "LV-RISK-CH": 9.0, "LV-VORS-RENTE-CH": 4.5, "LV-RISK-DE": 11.0, "LV-VORS-RENTE-DE": 5.0}
LEISTUNGSQUOTE_LV = {"LV-RISK-CH": 48.0, "LV-VORS-RENTE-CH": 71.0, "LV-RISK-DE": 52.0, "LV-VORS-RENTE-DE": 74.0}
KOSTENQUOTE_LV = {"LV-RISK-CH": 18.0, "LV-VORS-RENTE-CH": 9.5, "LV-RISK-DE": 21.0, "LV-VORS-RENTE-DE": 11.0}

GESELLSCHAFTEN = {
    "PHAG": {"name": "Pfefferminzia Holding AG", "sitz": "Olten", "land": "CH", "aufsicht": "FINMA (Gruppenaufsicht)",
             "funktion": "Konzernholding"},
    "PVAG": {"name": "Pfefferminzia Versicherung AG", "sitz": "Olten", "land": "CH", "aufsicht": "FINMA (SST)",
             "funktion": "Schadenversicherer Haftpflicht CH, fuehrt die Niederlassung Deutschland"},
    "PVAG-NL-DE": {"name": "Pfefferminzia Versicherung AG, Niederlassung Deutschland", "sitz": "Leipzig", "land": "DE",
                   "aufsicht": "BaFin (Niederlassungsaufsicht)", "funktion": "Haftpflicht DE"},
    "PLAG": {"name": "Pfefferminzia Leben AG", "sitz": "Olten", "land": "CH", "aufsicht": "FINMA (SST)",
             "funktion": "Lebensversicherer CH"},
    "PLDAG": {"name": "Pfefferminzia Lebensversicherung Deutschland AG", "sitz": "Leipzig", "land": "DE",
              "aufsicht": "BaFin (Solvency II)", "funktion": "Lebensversicherer DE"},
    "MTG": {"name": "Minzia Technologies GmbH", "sitz": "Berlin", "land": "DE",
            "aufsicht": "keine Versicherungsaufsicht; gruppeninternes Outsourcing",
            "funktion": "IT- und KI-Dienstleisterin, Betreiberin MINT und Herbarium"},
    "PSAG": {"name": "Pfefferminzia Service AG", "sitz": "Olten", "land": "CH", "aufsicht": "keine",
             "funktion": "Shared Services HR, Finanzen, Einkauf"},
}

# FTE je Standort und Herkunft, Stichtag 2025-12-31
FTE_2025 = {
    "Olten": {"pfefferminz": 985, "minzia": 12, "neu": 53},
    "Leipzig": {"pfefferminz": 590, "minzia": 8, "neu": 22},
    "Berlin": {"pfefferminz": 15, "minzia": 228, "neu": 17},
    "Zuerich": {"pfefferminz": 150, "minzia": 28, "neu": 12},
    "Bern": {"pfefferminz": 78, "minzia": 0, "neu": 2},
    "St. Gallen": {"pfefferminz": 76, "minzia": 0, "neu": 4},
    "Lausanne": {"pfefferminz": 58, "minzia": 0, "neu": 2},
    "Remote": {"pfefferminz": 20, "minzia": 45, "neu": 5},
}
FTE_HISTORIE = {  # Pfefferminz und Minzia getrennt bis 2024
    2021: {"pfefferminz": 2085, "minzia": 95}, 2022: {"pfefferminz": 2110, "minzia": 130},
    2023: {"pfefferminz": 2130, "minzia": 160}, 2024: {"pfefferminz": 2150, "minzia": 185},
}


def r(x: float, n: int = 1) -> float:
    return round(float(x), n)


def segment_jahr(key: str, jahr: int) -> dict:
    ges, sparte, produkt, markt, waehrung, praemie25, vertr25, kennzahl, kanal = SEGMENTE_2025[key]
    w = WACHSTUM[jahr]
    praemie = praemie25 * w
    vertraege = vertr25 * w
    if key == "HP-PRIV-DE" and jahr < 2025:
        # Minzia-Policen (Assekuradeur) sind bis 2024 nicht bei Pfefferminz; 2025 migriert
        praemie -= MINZIA[jahr][0] * 0.0  # bereits im Wachstumspfad beruecksichtigt
    out = {
        "gesellschaft": ges, "sparte": sparte, "produkte": produkt, "markt": markt, "waehrung": waehrung,
        "bruttopraemien_mio": r(praemie), "vertragsbestand_tsd": r(vertraege),
        "neugeschaeft_stueck_tsd": r(vertraege * NEUGESCHAEFT[key] / 100 * (0.9 if jahr == 2021 else 1.0)),
        "storno_quote_pct": r(STORNO[key] * (1.3 if (jahr == 2025 and markt == "CH") else 1.0)
                              * (1.15 if (jahr == 2025 and markt == "DE") else 1.0)),
        "vertriebskanal_anteile_pct": kanal,
    }
    if sparte == "HP":
        freq, avg = SCHADEN[key]
        n = vertraege * 1000 * freq * (1.05 if jahr == 2020 else 1.0)
        schadenaufwand = n * avg * (1 + 0.02 * (2025 - jahr)) / 1e6
        sq = schadenaufwand / praemie * 100
        kq = KOSTENQUOTE_HP[key] + (1.5 if jahr == 2025 else 0.0)  # Integrationskosten 2025
        out.update({
            "schadenanzahl_tsd": r(n / 1000), "durchschnittsschaden": r(avg * (1 + 0.02 * (2025 - jahr)), 0),
            "schadenaufwand_mio": r(schadenaufwand), "schadenquote_pct": r(sq), "kostenquote_pct": r(kq),
            "combined_ratio_pct": r(sq + kq),
        })
    else:
        out.update({
            "leistungsquote_pct": r(LEISTUNGSQUOTE_LV[key] + (2.0 if jahr in (2020, 2021) else 0.0)),
            "kostenquote_pct": r(KOSTENQUOTE_LV[key]),
            "neugeschaeftsmarge_pct": r(kennzahl["neugeschaeftsmarge_pct"] - (0.4 if jahr < 2024 else 0.0)),
        })
    return out


def main() -> None:
    daten: dict = {
        "meta": {
            "stichtag": "2025-12-31",
            "waehrung_gruppe": "CHF",
            "umrechnungskurs_eur_chf": KURS_EUR_CHF,
            "stichprobenfaktor_stufe_m": 0.05,
            "stichprobe_hinweis": "Stufe M des Datensatzes entspricht rund 5 Prozent des Realbestands (75'000 von rund 1.44 Mio. Vertraegen)",
            "erzeugt_durch": "scripts/build_kennzahlen_master.py",
            "hinweis": "Einzige Quelle aller Unternehmenszahlen. Kein Dokument erfindet eigene Zahlen (Konventionen §2).",
        },
        "gesellschaften": GESELLSCHAFTEN,
        "jahre": {},
    }
    for jahr in JAHRE:
        kurs = KURS_EUR_CHF[jahr]
        segmente = {k: segment_jahr(k, jahr) for k in SEGMENTE_2025}
        praemie_chf = sum(s["bruttopraemien_mio"] * (kurs if s["waehrung"] == "EUR" else 1) for s in segmente.values())
        vertraege = sum(s["vertragsbestand_tsd"] for s in segmente.values())
        schaeden = sum(s.get("schadenanzahl_tsd", 0) for s in segmente.values())
        if jahr < 2025:
            fte = FTE_HISTORIE[jahr]
            fte_gesamt = fte["pfefferminz"] + fte["minzia"]
            fte_standorte = None
            minzia = {"vermittelte_praemien_eur_mio": MINZIA[jahr][0], "aktive_policen_tsd": MINZIA[jahr][1],
                      "nutzerkonten_tsd": r(MINZIA[jahr][1] * 1.5, 0), "mitarbeiter_fte": fte["minzia"],
                      "hinweis": "Assekuradeur ohne eigenes Risiko; Zahlen nicht in den Segmenten enthalten"}
        else:
            fte_standorte = FTE_2025
            fte = {h: sum(s[h] for s in FTE_2025.values()) for h in ("pfefferminz", "minzia", "neu")}
            fte_gesamt = sum(fte.values())
            minzia = {"hinweis": "Ab 2025 konsolidiert; Minzia-Policen in HP-PRIV-DE enthalten"}
        kunden_tsd = r(vertraege * 0.73, 0)
        beschwerden = int(kunden_tsd * 1000 * (0.0023 if jahr == 2025 else 0.0018))
        jahr_daten = {
            "konsolidiert": jahr == 2025,
            "hinweis": "2021 bis 2024 Pfefferminz-Gruppe, Minzia separat unter 'minzia'" if jahr < 2025 else "Erstes konsolidiertes Jahr nach Closing 2025-01-01",
            "gruppe": {
                "bruttopraemien_chf_mio": r(praemie_chf), "vertragsbestand_tsd": r(vertraege),
                "kundenbeziehungen_tsd": kunden_tsd, "schadenanzahl_hp_tsd": r(schaeden),
                "mitarbeiter_fte": fte_gesamt, "mitarbeiter_fte_nach_herkunft": fte,
                "beschwerden_anzahl": beschwerden,
                "beschwerden_je_10000_kunden": r(beschwerden / kunden_tsd * 10, 1),
                "rating": {"agentur": "Nordstern Rating (fiktiv)", "note": "A-", "ausblick": "stabil"},
                "it_kosten_chf_mio": r(praemie_chf * (0.052 if jahr == 2025 else 0.041)),
                "ki_projekte_anzahl": {2021: 2, 2022: 3, 2023: 5, 2024: 8, 2025: 14}[jahr],
                "ki_modelle_produktiv": {2021: 1, 2022: 2, 2023: 3, 2024: 5, 2025: 9}[jahr],
            },
            "solvenz": {
                "PVAG_sst_quotient_pct": {2021: 212, 2022: 205, 2023: 198, 2024: 191, 2025: 186}[jahr],
                "PLAG_sst_quotient_pct": {2021: 178, 2022: 171, 2023: 169, 2024: 174, 2025: 181}[jahr],
                "PLDAG_solvency2_quote_pct": {2021: 264, 2022: 241, 2023: 233, 2024: 246, 2025: 258}[jahr],
                "hinweis": "SST fuer CH-Gesellschaften, Solvency II fuer die DE-Lebenstochter; vereinfacht, zu verifizieren",
            },
            "segmente": segmente,
            "minzia": minzia,
        }
        if fte_standorte:
            jahr_daten["gruppe"]["mitarbeiter_fte_nach_standort"] = fte_standorte
        if jahr == 2025:
            jahr_daten["kulturumfrage_2025"] = {
                "teilnehmer": 1830, "ruecklauf_pct": 76.0,
                "zustimmung_ki_hilft_meiner_arbeit_pct": {"pfefferminz": 41, "minzia": 88, "neu": 67, "gesamt": 49},
                "vertrauen_in_ki_entscheidungen_pct": {"pfefferminz": 28, "minzia": 71, "neu": 52, "gesamt": 35},
                "zugehoerigkeit_neue_firma_pct": {"pfefferminz": 54, "minzia": 63, "neu": 79, "agenturen_extern": 38},
                "freitextkommentare": 200,
            }
            jahr_daten["vertrieb"] = {
                "agenturen_ch": 96, "agenturen_de": 38, "aktive_makler_ch": 400, "aktive_makler_de": 1200,
                "app_nutzerkonten_tsd": 118, "bancassurance_partner": ["Aare-Bank AG (fiktiv)", "Saechsische Genossenschaftskasse eG (fiktiv)"],
            }
            jahr_daten["migration"] = {
                "hp_de_neugeschaeft_auf_mint_pct": 100, "hp_ch_neugeschaeft_auf_mint_pct": 60,
                "hp_bestand_migriert_pct": 100, "lv_bestand_migriert_pct": 100,
                "migrationswellen": {"HP": "2025-Q2", "LV": "2025-Q4"},
                "vertraege_mit_migrationsartefakten": 214,
                "hinweis": "Zahl 214 bezieht sich auf den Fall Pieper (Bausteincode nicht uebernommen)",
            }
        daten["jahre"][jahr] = jahr_daten
    ZIEL.write_text("# Kennzahlen-Masterdatei Pfefferminzia. Erzeugt durch scripts/build_kennzahlen_master.py, nicht von Hand editieren.\n"
                    + yaml.safe_dump(daten, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    g = daten["jahre"][2025]["gruppe"]
    print(f"2025: Praemien CHF {g['bruttopraemien_chf_mio']} Mio., Vertraege {g['vertragsbestand_tsd']} Tsd., "
          f"Kunden {g['kundenbeziehungen_tsd']} Tsd., FTE {g['mitarbeiter_fte']}")
    for k, s in daten["jahre"][2025]["segmente"].items():
        if s["sparte"] == "HP":
            print(f"  {k}: CR {s['combined_ratio_pct']} (SQ {s['schadenquote_pct']} + KQ {s['kostenquote_pct']})")


if __name__ == "__main__":
    main()
