"""Erzeugt die Daten fuer den Cockpit-Reiter «Akte» (Fall Pieper, PTR-00000008).

Liest Partner-, Vertrags-, Deckungs-, Schaden-, Schadenposition- und Mitarbeitertabelle,
die Kompetenzordnung R08, alle 17 Dateien der Fallakte unter
data/documents/S/personas/PTR-00000008/ (Markdown mit Frontmatter und .eml) sowie die
Entwuerfe der beiden Schreiben und den Faktencheck, und schreibt eine JavaScript-Konstante
nach meine-ergebnisse/cockpit-daten/akte.js, damit das Cockpit ohne Server im Browser laeuft.
"""

import csv
import email
import json
import re
from pathlib import Path

PROJEKT_ROOT = Path(__file__).resolve().parents[2]
CURATED = PROJEKT_ROOT / "data" / "curated" / "S" / "csv"
DOKUMENTE = PROJEKT_ROOT / "data" / "documents" / "S" / "personas" / "PTR-00000008"
ERGEBNISSE = PROJEKT_ROOT / "meine-ergebnisse"
AUSGABE = ERGEBNISSE / "cockpit-daten" / "akte.js"


def lies_csv(pfad):
    with open(pfad, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def zeile(zeilen, feld, wert):
    for z in zeilen:
        if z.get(feld) == wert:
            return z
    return {}


def lies_markdown_dokument(pfad):
    text = pfad.read_text(encoding="utf-8")
    teile = text.split("---\n")
    # teile[0] == "", teile[1] == Frontmatter, Rest = Koerper (kann weitere --- enthalten)
    frontmatter_text = teile[1]
    koerper = "---\n".join(teile[2:])
    frontmatter = {}
    for zeile_fm in frontmatter_text.strip("\n").split("\n"):
        if ":" in zeile_fm:
            k, _, v = zeile_fm.partition(":")
            frontmatter[k.strip()] = v.strip().strip('"')
    # Fusszeile "Fiktives Lehrbeispiel ..." entfernen
    koerper = koerper.split("Fiktives Lehrbeispiel.")[0].strip()
    # Erste Ueberschrift entfernen, sie steht schon im Kopf
    koerper = re.sub(r"^#\s+.*\n+", "", koerper, count=1)
    return frontmatter, koerper.strip()


def lies_eml(pfad):
    msg = email.message_from_bytes(pfad.read_bytes())
    body = msg.get_payload()
    body = body.split("-- \nFiktives Lehrbeispiel")[0].strip()
    return {
        "von": msg.get("From", ""),
        "an": msg.get("To", ""),
        "datum": msg.get("Date", ""),
        "betreff": msg.get("Subject", ""),
    }, body.strip()


partner = zeile(lies_csv(CURATED / "partner.csv"), "partner_id", "PTR-00000008")
vertrag = zeile(lies_csv(CURATED / "vertrag.csv"), "vertrag_id", "VTR-00000801")
deckungen = [d for d in lies_csv(CURATED / "deckung.csv") if d.get("vertrag_id") == "VTR-00000801"]
schaden = zeile(lies_csv(CURATED / "schaden.csv"), "schaden_id", "SCH-00000810")
positionen = [p for p in lies_csv(CURATED / "schaden_position.csv") if p.get("schaden_id") == "SCH-00000810"]
mitarbeitende = {m["mitarbeiter_id"]: m for m in lies_csv(CURATED / "mitarbeiter.csv")}

kunde_name = f"{partner['vorname']} {partner['nachname']}"
baustein = next(d for d in deckungen if d["deckungsart"] == "BAUSTEIN")

# --- Dokumente und Kontakte der Fallakte lesen (alle 17) ---
dateien = sorted(DOKUMENTE.iterdir())
gelesen = {}
for pfad in dateien:
    kennung = pfad.name.split("_")[0].split(".")[0]
    if pfad.suffix == ".eml":
        kopf, text = lies_eml(pfad)
        gelesen[kennung] = {"kopf": kopf, "text": text, "typ": "eml"}
    else:
        kopf, text = lies_markdown_dokument(pfad)
        gelesen[kennung] = {"kopf": kopf, "text": text, "typ": "md"}

assert len(gelesen) == 17, f"erwartet 17 Dateien der Fallakte, gelesen: {len(gelesen)}"

AYLIN = "Aylin Demirci, Teamleiterin Schaden Haftpflicht Deutschland"
MIRIAM = "Miriam Steinbrecher, Compliance Officer Deutschland"
JONAS = "Jonas Pfister, MLOps"
PIEPER = "Hans-Georg Pieper"

# Gruppenregel: Kunde+Schadenabteilung bei Korrespondenz mit dem Kunden ueber den Fall,
# Ombudsmann bzw. Aufsicht bei Korrespondenz mit diesen Stellen, sonst intern und IT.
EREIGNISSE = [
    {"id": "vertrag-beginn", "datum": "2013-01-01", "art": "Vertragstabelle", "titel": "Vertragsbeginn Privathaftpflicht (vormals Policennummer 40.288.506-6)",
     "von": "", "an": PIEPER, "gruppen": ["kunde"], "kennungText": "Vertragstabelle, Beginn", "volltext": ""},
    {"id": "DOK-00000802", "datum": "2019-02-12", "art": "Beratungsprotokoll", "titel": gelesen["DOK-00000802"]["kopf"]["titel"],
     "von": "Agentur Dresden", "an": PIEPER, "gruppen": ["kunde"], "kennungText": "Beratungsprotokoll DOK-00000802", "volltext": gelesen["DOK-00000802"]["text"]},
    {"id": "DOK-00000801", "datum": "2019-02-15", "art": "Nachtrag", "titel": gelesen["DOK-00000801"]["kopf"]["titel"],
     "von": "Pfefferminzia (Agentur Dresden)", "an": PIEPER, "gruppen": ["kunde"], "kennungText": "Nachtrag DOK-00000801", "volltext": gelesen["DOK-00000801"]["text"]},
    {"id": "baustein-wirksam", "datum": "2019-03-01", "art": "Deckungstabelle", "titel": "Baustein Tierhalterhaftpflicht (BS-TIER-HUND) wirksam",
     "von": "", "an": PIEPER, "gruppen": ["kunde"], "kennungText": "Deckungstabelle, Baustein, gültig ab", "volltext": ""},
    {"id": "migration", "datum": "2025-03-03", "art": "Migrationslog", "titel": "Migration Pilotwelle Privathaftpflicht Deutschland: Bausteincode Tierhalter nicht ins Zielschema übernommen (Warnung)",
     "von": "", "an": "", "gruppen": ["intern"], "kennungText": "Migrationslog, Vorgang HP-2025-PILOT", "volltext": ""},
    {"id": "INT-00000801", "datum": "2025-03-21T16:35", "art": "Telefonnotiz", "titel": gelesen["INT-00000801"]["kopf"]["betreff"],
     "von": PIEPER, "an": "Contact Center Leipzig", "gruppen": ["kunde", "schaden"], "kennungText": "Telefonnotiz INT-00000801", "volltext": gelesen["INT-00000801"]["text"]},
    {"id": "SCH-00000810-01", "datum": "2025-03-21", "art": "Schadenposition", "titel": "Erstreserve automatisch gebildet, EUR 1'500.00",
     "von": "", "an": "", "gruppen": ["intern"], "kennungText": "Schadenposition SCH-00000810-01", "volltext": ""},
    {"id": "INT-00000802", "datum": "2025-03-24T06:00", "art": "Brief", "titel": gelesen["INT-00000802"]["kopf"]["betreff"],
     "von": "Pfefferminzia, Schaden Haftpflicht (maschinell erstellt, ohne Unterschrift)", "an": PIEPER, "gruppen": ["kunde", "schaden"], "kennungText": "Brief INT-00000802", "volltext": gelesen["INT-00000802"]["text"]},
    {"id": "DOK-00000803", "datum": "2025-03-25", "art": "Arztrechnung", "titel": gelesen["DOK-00000803"]["kopf"]["titel"],
     "von": "Universitätsklinikum Dresden, Notaufnahme", "an": "Radfahrer (Geschädigter)", "gruppen": [], "kennungText": "Arztrechnung DOK-00000803", "volltext": gelesen["DOK-00000803"]["text"]},
    {"id": "INT-00000803", "datum": "2025-03-28", "art": "Brief", "titel": gelesen["INT-00000803"]["kopf"]["betreff"],
     "von": PIEPER, "an": AYLIN, "gruppen": ["kunde", "schaden"], "kennungText": "Beschwerdebrief INT-00000803", "volltext": gelesen["INT-00000803"]["text"]},
    {"id": "INT-00000804", "datum": "2025-04-02T11:20", "art": "E-Mail", "titel": gelesen["INT-00000804"]["kopf"]["betreff"],
     "von": "Pfefferminzia, Kundenservice Leipzig", "an": PIEPER, "gruppen": ["kunde", "schaden"], "kennungText": "E-Mail INT-00000804", "volltext": gelesen["INT-00000804"]["text"]},
    {"id": "INT-00000805", "datum": "2025-04-15", "art": "Brief", "titel": gelesen["INT-00000805"]["kopf"]["betreff"],
     "von": PIEPER, "an": MIRIAM, "gruppen": ["kunde", "schaden"], "kennungText": "Beschwerdebrief INT-00000805", "volltext": gelesen["INT-00000805"]["text"]},
    {"id": "INT-00000806", "datum": "2025-04-16T09:05", "art": "interne E-Mail", "titel": gelesen["INT-00000806"]["kopf"]["betreff"],
     "von": AYLIN, "an": f"{JONAS}, {MIRIAM} (Cc Martina Jost)", "gruppen": ["intern"], "kennungText": "interne E-Mail INT-00000806", "volltext": gelesen["INT-00000806"]["text"]},
    {"id": "INT-00000807", "datum": "2025-04-16T14:40", "art": "interne E-Mail", "titel": gelesen["INT-00000807"]["kopf"]["betreff"],
     "von": JONAS, "an": AYLIN, "gruppen": ["intern"], "kennungText": "interne E-Mail INT-00000807", "volltext": gelesen["INT-00000807"]["text"], "wendepunkt": "Ursache gefunden, Regel deaktiviert"},
    {"id": "R08-v2.1", "datum": "2025-04-16", "art": "Regelwerk", "titel": "Kompetenzordnung R08 tritt in Version 2.1 in Kraft: Ablehnungen technisch nur noch mit Freigabe durch eine Person",
     "von": "", "an": "", "gruppen": ["intern"], "kennungText": "Kompetenzordnung RW-GRUPPE-R08-2025, gültig ab", "volltext": ""},
    {"id": "INT-00000808", "datum": "2025-04-17", "art": "Brief", "titel": gelesen["INT-00000808"]["kopf"]["betreff"],
     "von": AYLIN, "an": PIEPER, "gruppen": ["kunde", "schaden"], "kennungText": "Brief INT-00000808", "volltext": gelesen["INT-00000808"]["text"], "wendepunkt": "Regulierung und Entschuldigung"},
    {"id": "SCH-00000810-03", "datum": "2025-04-17", "art": "Schadenposition", "titel": "Reserve wiedereröffnet, EUR 1'500.00",
     "von": "", "an": "", "gruppen": ["intern"], "kennungText": "Schadenposition SCH-00000810-03", "volltext": ""},
    {"id": "SCH-00000810-04", "datum": "2025-04-17", "art": "Schadenposition", "titel": "Zahlung an den Geschädigten (Arztkosten, Schmerzensgeld, Hose), EUR 1'240.00, ohne Selbstbehalt",
     "von": "", "an": "Radfahrer (Geschädigter)", "gruppen": ["intern"], "kennungText": "Schadenposition SCH-00000810-04", "volltext": ""},
    {"id": "SCH-00000810-05", "datum": "2025-04-17", "art": "Schadenposition", "titel": "Kulanzzahlung für Aufwand und Verzögerung, EUR 100.00",
     "von": "", "an": PIEPER, "gruppen": ["intern"], "kennungText": "Schadenposition SCH-00000810-05", "volltext": ""},
    {"id": "nachmigration", "datum": "2025-04-18", "art": "Memo", "titel": "Nachmigration der 214 betroffenen Verträge abgeschlossen",
     "von": "", "an": "", "gruppen": ["intern"], "kennungText": "Root-Cause-Memo DOK-00000804, Massnahmen", "volltext": ""},
    {"id": "INT-00000809", "datum": "2025-04-24", "art": "Brief", "titel": gelesen["INT-00000809"]["kopf"]["betreff"],
     "von": "Versicherungsombudsmann e. V.", "an": "Pfefferminzia", "gruppen": ["ombudsmann"], "kennungText": "Brief INT-00000809", "volltext": gelesen["INT-00000809"]["text"]},
    {"id": "SCH-00000810-06", "datum": "2025-04-24", "art": "Schadenposition", "titel": "Schaden geschlossen, Reserve auf null",
     "von": "", "an": "", "gruppen": ["intern"], "kennungText": "Schadenposition SCH-00000810-06", "volltext": ""},
    {"id": "DOK-00000804", "datum": "2025-05-06", "art": "Memo", "titel": gelesen["DOK-00000804"]["kopf"]["titel"],
     "von": "Compliance DE, Data & AI Office", "an": "Geschäftsleitung, Modellrisiko-Komitee", "gruppen": ["intern"], "kennungText": "Memo DOK-00000804", "volltext": gelesen["DOK-00000804"]["text"]},
    {"id": "INT-00000811", "datum": "2025-05-08", "art": "Brief", "titel": gelesen["INT-00000811"]["kopf"]["betreff"],
     "von": MIRIAM, "an": "Versicherungsombudsmann e. V.", "gruppen": ["ombudsmann"], "kennungText": "Brief INT-00000811", "volltext": gelesen["INT-00000811"]["text"]},
    {"id": "DOK-00000805", "datum": "2025-06-10", "art": "Aufsichtskorrespondenz", "titel": gelesen["DOK-00000805"]["kopf"]["titel"],
     "von": "Bundesanstalt für Finanzdienstleistungsaufsicht", "an": "Pfefferminzia, Hauptbevollmächtigte", "gruppen": ["aufsicht"], "kennungText": "Aufsichtskorrespondenz DOK-00000805", "volltext": gelesen["DOK-00000805"]["text"]},
    {"id": "INT-00000823", "datum": "2025-07-07", "art": "Brief", "titel": gelesen["INT-00000823"]["kopf"]["betreff"],
     "von": PIEPER, "an": AYLIN, "gruppen": ["kunde", "schaden"], "kennungText": "Brief INT-00000823", "volltext": gelesen["INT-00000823"]["text"]},
    {"id": "INT-00000824", "datum": "2025-07-14", "art": "Brief", "titel": gelesen["INT-00000824"]["kopf"]["betreff"],
     "von": AYLIN, "an": PIEPER, "gruppen": ["kunde", "schaden"], "kennungText": "Brief INT-00000824", "volltext": gelesen["INT-00000824"]["text"]},
]

# Wendepunkt 1: die automatische Ablehnung selbst
for e in EREIGNISSE:
    if e["id"] == "INT-00000802":
        e["wendepunkt"] = "Automatische Ablehnung"

# --- Kacheln ---
bezahlt_total = sum(float(p["betrag"]) for p in positionen if p["art"] == "ZAHLUNG")
zahlungsdatum = max(p["datum"] for p in positionen if p["art"] == "ZAHLUNG")
from datetime import date
schadentag = date.fromisoformat(schaden["schadendatum"])
tag_zahlung = date.fromisoformat(zahlungsdatum)
tag_ablehnung = date.fromisoformat("2025-03-24")
tage_bis_zahlung = (tag_zahlung - schadentag).days
tage_ablehnung_zahlung = (tag_zahlung - tag_ablehnung).days


def fmt_eur(n):
    ganze, rappen = f"{n:.2f}".split(".")
    ganze_gruppiert = f"{int(ganze):,}".replace(",", "'")
    return f"EUR {ganze_gruppiert}.{rappen}"


KACHELN = [
    {"label": "Schadentag", "wert": "21.03.2025", "definition": "Datum des Ereignisses. Quelle: Schadentabelle, Schadendatum."},
    {"label": "Tage bis zur Zahlung", "wert": f"{tage_bis_zahlung}", "definition": "Kalendertage vom Schadentag bis zur Zahlung an den Geschädigten. Quelle: Schadentabelle, Schadendatum; Schadenposition, Zahlung."},
    {"label": "Bezahlter Betrag", "wert": fmt_eur(bezahlt_total), "definition": "Summe aller Zahlungspositionen (Regulierung an den Geschädigten und Kulanz an den Kunden). Quelle: Schadenposition, Art Zahlung."},
    {"label": "Zahl der Dokumente", "wert": "17", "definition": "Dokumente und Kontakte der Fallakte (Briefe, E-Mails, Telefonnotiz, interne Dokumente), vollständig gelesen. Quelle: Ordner der Fallakte PTR-00000008."},
    {"label": "Tage Ablehnung → Zahlung", "wert": f"{tage_ablehnung_zahlung}", "definition": "Kalendertage von der automatischen Ablehnung bis zur Zahlung. Quelle: Brief INT-00000802 (Ablehnung); Schadenposition, Zahlung."},
]

GRUPPEN = [
    {"id": "kunde", "name": "Kunde", "farbe": "var(--pfefferminz)"},
    {"id": "schaden", "name": "Schadenabteilung", "farbe": "var(--hp)"},
    {"id": "intern", "name": "intern und IT", "farbe": "var(--text-secondary)"},
    {"id": "ombudsmann", "name": "Ombudsmann", "farbe": "var(--minzia)"},
    {"id": "aufsicht", "name": "Aufsicht", "farbe": "var(--lv)"},
]

geburtsdatum_tt = ".".join(reversed(partner["geburtsdatum"].split("-")))

KOPF = {
    "kunde": f"{kunde_name}, geb. {geburtsdatum_tt}, Dresden",
    "vertrag": f"{vertrag['vertrag_id']} · Privathaftpflicht (HP-PRIV) · seit 01.01.2013",
    "versicherungsschein": "vormals 40.288.506-6 (HAPO)",
    "schaden": f"{schaden['schaden_id']} · Anzeige {schaden['schadennummer_anzeige']} · Status: geschlossen",
}

# --- Faktencheck (Etappe 4) ---
FAKTENCHECK_REGEL = "Jede Aussage mit Datum, Betrag, Zahl oder einem erledigten Zustand wird gegen Tabellen und Originaldokumente der Akte geprüft (nicht gegen die eigene Chronologie): belegt (grün, mit Quelle nachvollziehbar), vermutet (gelb, plausibel aber nicht in Stufe S nachzählbar oder nicht im Wortlaut vorliegend), nicht belegt (rot, widerspricht der Akte oder ist durch nichts gedeckt)."

FAKTENCHECK = [
    {"schreiben": "Kunde", "aussage": "Vertrag enthält seit dem 01.03.2019 den Baustein Tierhalterhaftpflicht.", "status": "gruen", "quelle": "Deckungstabelle, Baustein BS-TIER-HUND, gültig ab; Nachtrag DOK-00000801"},
    {"schreiben": "Kunde", "aussage": "Bei der Übernahme des Vertrags in das neue System im März 2025 wurde der Baustein nicht übertragen.", "status": "gruen", "quelle": "Migrationslog, Vorgang HP-2025-PILOT; interne E-Mail INT-00000807"},
    {"schreiben": "Kunde", "aussage": "Das Schadensystem hat die Meldung deshalb automatisch abgelehnt.", "status": "gruen", "quelle": "Brief INT-00000802; interne E-Mail INT-00000807"},
    {"schreiben": "Kunde", "aussage": "Eine Ablehnung muss bei uns immer von einem Menschen geprüft werden.", "status": "gelb", "quelle": "Kompetenzordnung RW-GRUPPE-R08-2025 – Grundsatz belegt (§ 5 Version 2.1, interne E-Mail INT-00000806), am Schadentag (24.03.2025) galt aber Version 2.0, deren Wortlaut nicht in der Akte vorliegt"},
    {"schreiben": "Kunde", "aussage": "Schaden am 17.04.2025 reguliert: EUR 1'240.00 an den Geschädigten.", "status": "gruen", "quelle": "Schadenposition SCH-00000810-04"},
    {"schreiben": "Kunde", "aussage": "Ein Selbstbehalt fällt nicht an.", "status": "gruen", "quelle": "Schadenposition SCH-00000810-04, Vermerk «ohne Selbstbehalt»"},
    {"schreiben": "Kunde", "aussage": "Zusätzlich EUR 100.00 Kulanz für Aufwand und Verzögerung.", "status": "gruen", "quelle": "Schadenposition SCH-00000810-05"},
    {"schreiben": "Kunde", "aussage": "Vertrag ist korrigiert, der Baustein ist wieder im System sichtbar.", "status": "gruen", "quelle": "Root-Cause-Memo DOK-00000804, Massnahme «Nachmigration der 214 Verträge (18.04.)»"},
    {"schreiben": "Ombudsmann", "aussage": "Vertrag enthielt zum Schadenzeitpunkt den Baustein Tierhalterhaftpflicht (Nachtrag Nr. 2 vom 15.02.2019, wirksam 01.03.2019).", "status": "gruen", "quelle": "Nachtrag DOK-00000801; Deckungstabelle"},
    {"schreiben": "Ombudsmann", "aussage": "Bausteincode wurde bei der Pilotmigration am 03.03.2025 nicht übernommen; Datenfehler, keine Ermessensentscheidung.", "status": "gruen", "quelle": "Migrationslog, Vorgang HP-2025-PILOT; interne E-Mail INT-00000807"},
    {"schreiben": "Ombudsmann", "aussage": "Ablehnung erfolgte automatisiert ohne Prüfung durch eine natürliche Person; widerspricht der internen Kompetenzordnung.", "status": "gelb", "quelle": "interne E-Mail INT-00000806/807 belegen den Grundsatz; der am 24.03.2025 geltende Wortlaut der Kompetenzordnung (Version 2.0) liegt nicht in der Akte vor, nur Version 2.1 (ab 16.04.2025)"},
    {"schreiben": "Ombudsmann", "aussage": "Regel am 16.04.2025 deaktiviert, Kompetenzordnung in Version 2.1 technisch abgesichert.", "status": "gruen", "quelle": "interne E-Mail INT-00000807; Kompetenzordnung RW-GRUPPE-R08-2025, gültig ab 16.04.2025"},
    {"schreiben": "Ombudsmann", "aussage": "Alle 214 vom selben Migrationsfehler betroffenen Verträge korrigiert.", "status": "gruen", "quelle": "Root-Cause-Memo DOK-00000804, Ursache a) und Massnahmen"},
    {"schreiben": "Ombudsmann", "aussage": "Zehn weitere Fälle mit gleicher Fehlablehnung von Amts wegen wiedereröffnet und reguliert.", "status": "gelb", "quelle": "Root-Cause-Memo DOK-00000804 nennt elf automatisch abgelehnte Fälle insgesamt (Pieper eingeschlossen, also zehn weitere); Einzelfälle und deren Regulierung sind unternehmensweite Zahlen, im Datensatz Stufe S nicht nachzählbar"},
    {"schreiben": "Ombudsmann", "aussage": "Schaden am 17.04.2025 vollständig reguliert, EUR 1'240.00 an den Geschädigten, EUR 100.00 Kulanz, schriftliche Entschuldigung.", "status": "gruen", "quelle": "Schadenposition SCH-00000810-04/05; Brief INT-00000808"},
]


def maskiere(text):
    text = text.replace("<", "‹").replace(">", "›")
    return text


ANTWORT_KUNDE = maskiere((ERGEBNISSE / "pieper-antwort-kunde.md").read_text(encoding="utf-8")) if (ERGEBNISSE / "pieper-antwort-kunde.md").exists() else ""
STELLUNGNAHME = maskiere((ERGEBNISSE / "pieper-stellungnahme-ombudsmann.md").read_text(encoding="utf-8")) if (ERGEBNISSE / "pieper-stellungnahme-ombudsmann.md").exists() else ""

for e in EREIGNISSE:
    e["volltext"] = maskiere(e["volltext"])
    e["titel"] = maskiere(e["titel"])

DATEN = {
    "kopf": KOPF,
    "kacheln": KACHELN,
    "gruppen": GRUPPEN,
    "ereignisse": EREIGNISSE,
    "faktencheckRegel": FAKTENCHECK_REGEL,
    "faktencheck": FAKTENCHECK,
    "schreibenAntwortKunde": ANTWORT_KUNDE,
    "schreibenStellungnahme": STELLUNGNAHME,
}

AUSGABE.parent.mkdir(parents=True, exist_ok=True)
AUSGABE.write_text("const AKTE_DATEN = " + json.dumps(DATEN, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
print(f"geschrieben: {AUSGABE} ({len(EREIGNISSE)} Ereignisse, {len(FAKTENCHECK)} Faktencheck-Zeilen)")
