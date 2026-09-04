"""Erzeugt ``docs/datensatz/data-dictionary.md`` aus dem Manifest und den Parquet-Dateien einer Stufe.

Aufruf: ``uv run python scripts/build_data_dictionary.py [S]``
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

BESCHREIBUNG = {
    "curated/partner": "Partner: natuerliche und juristische Personen (Kunden, Mitversicherte, Beguenstigte, Inhaber)",
    "curated/partner_adresse": "Adressen mit Historie (Umzuege); genau eine aktuelle Adresse je Partner",
    "curated/partner_kontakt": "Kontaktkanaele (E-Mail, Telefon, Mobil), nur Fiktionsbereiche",
    "curated/partner_beziehung": "Beziehungen: Ehepartner, Kinder, Inhaber, Kontaktpersonen (von -> zu)",
    "curated/partner_firma": "Firmenmerkmale juristischer Personen: Branche (NACE), Risikoklasse, Umsatz, Mitarbeitende",
    "curated/org_einheit": "Organisationseinheiten der Gruppe (drei Ebenen)",
    "curated/mitarbeiter": "Mitarbeitende inkl. der 14 Personas; Herkunft Pfefferminz/Minzia/neu/extern",
    "curated/agentur": "Vertriebsorganisationen: Exklusivagenturen, Makler, Banken, Portale, Direkt",
    "curated/vermittler": "Vermittlerpersonen mit Agenturzuordnung, Alt- und Neunummer",
    "curated/produkt": "Produktkatalog beider Sparten",
    "curated/tarifgeneration": "Bedingungs- und Tarifgenerationen mit Gueltigkeit",
    "curated/antrag": "Antraege inkl. abgelehnter und zurueckgezogener; Underwriting-Entscheid, Angaben zu BMI und Rauchen",
    "curated/vertrag": "Vertraege beider Sparten mit Status, Praemie, Kanal, Quellsystem, Migrationsdatum",
    "curated/deckung": "Deckungen je Vertrag: Hauptdeckung, Bausteine, Zusatzversicherungen",
    "curated/risiko_objekt": "Risikoobjekt je Vertrag: Haushalt, Betrieb, Beruf oder versicherte Person",
    "curated/vertrag_partner_rolle": "Rollen der Partner am Vertrag: VN, mitversichert, versicherte Person, beguenstigt",
    "truth/partner_latent": "Latente Wahrheit je Partner: Kuendigungsneigung, Betrugsneigung, BMI, Raucher, Todesdatum (nur Dozenten)",
    "truth/vertrag_latent": "Latente Wahrheit je Vertrag: Tarifpraemie, Abweichung, Kuendigung in 12 Monaten, Bias-Anwendung (nur Dozenten)",
    "truth/dq_injektionen": "Protokoll aller injizierten Datenqualitaetsprobleme mit Originalwert (nur Dozenten)",
    "migration/partner_xref": "Kreuzreferenz Partner: curated-ID zu Quell-IDs in HAPO, VERA, MINT mit Match-Methode und Score",
    "migration/vertrag_xref": "Kreuzreferenz Vertraege: curated-ID zu Quell-IDs",
    "migration/migrationslog": "Simuliertes Log der Migrationswellen 2025 (OK/WARN/ERROR)",
    "migration/feld_mapping": "Feldweise Abbildung Quellsystem -> curated mit Transformationsregeln und DQ-Bezug",
}


def main(stufe: str = "S") -> None:
    manifest = json.loads((ROOT / f"data/manifest_{stufe}.json").read_text(encoding="utf-8"))
    out = [f"# Data Dictionary Stufe {stufe}", "",
           f"Erzeugt aus `data/manifest_{stufe}.json` durch `scripts/build_data_dictionary.py`. Stichtag {manifest['stichtag']}, "
           f"Master-Seed {manifest['generator']['master_seed']}, Version {manifest['version']}.", "",
           "Schichten: `curated` (harmonisiert, fuer Teilnehmer), `truth` (latente Wahrheit und Labels, nur Dozenten), "
           "`migration` (Kreuzreferenzen, Feldmapping, Migrationslog), `raw` (Rohextrakte der Quellsysteme, siehe unten).", ""]
    out += ["## Tabellen", "", "| Tabelle | Zeilen | Spalten | Beschreibung |", "|---|---|---|---|"]
    for t in manifest["tables"]:
        key = f"{t['layer']}/{t['name']}"
        out.append(f"| {key} | {t['rows']} | {t['columns']} | {BESCHREIBUNG.get(key, '')} |")
    out.append("")
    for t in manifest["tables"]:
        key = f"{t['layer']}/{t['name']}"
        pfad = ROOT / t["files"]["parquet"]
        df = pd.read_parquet(pfad)
        out += [f"### {key}", "", BESCHREIBUNG.get(key, ""), "", "| Spalte | Typ | Beispiel | Nullwerte |", "|---|---|---|---|"]
        for c in df.columns:
            s = df[c]
            bsp = s.dropna().iloc[0] if s.notna().any() else ""
            bsp = str(bsp)[:40].replace("|", "/")
            out.append(f"| {c} | {s.dtype} | {bsp} | {int(s.isna().sum())} |")
        out.append("")
    out += ["## Rohdaten (raw)", "", "| Datei | Beschreibung |", "|---|---|"]
    raw_besch = {"HAPO_PARTNER": "Partnerstamm Haftpflicht-Altsystem HAPO", "HAPO_VERTRAG": "Vertraege HAPO",
                 "VERA_PARTNER": "Partnerstamm Leben-Altsystem VERA", "VERA_VERTRAG": "Vertraege VERA",
                 "customers": "MINT-Kunden als JSON Lines (Schema v1 bis v3)", "policies": "MINT-Policen als JSON Lines"}
    for f in sorted(manifest["files"]):
        name = Path(f).stem.replace("_SATZART", "")
        art = "Satzartbeschreibung (Feldpositionen)" if "SATZART" in f else ("Fixed-width, ISO-8859-1" if f.endswith(".txt") else ("Semikolon-CSV, ISO-8859-1, Datum DD.MM.YY" if f.endswith(".csv") else "JSON Lines, UTF-8"))
        out.append(f"| {f} | {raw_besch.get(name, '')}; {art} |")
    out.append("")
    ziel = ROOT / "docs" / "datensatz" / f"data-dictionary-{stufe}.md"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text("\n".join(out), encoding="utf-8")
    print(ziel.relative_to(ROOT), len(manifest["tables"]), "Tabellen", len(manifest["files"]), "Rohdateien")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "S")
