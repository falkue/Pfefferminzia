"""
Erzeugt cockpit-daten/akte.js für den Cockpit-Reiter «Akte»: Fallakte
Hans-Georg Pieper (PTR-00000008), Vertrag VTR-00000801, Schaden SCH-00000810.

Liest ausschliesslich aus den bereinigten Tabellen und den Fallakte-Dateien
unter data/documents/S/personas/PTR-00000008/. Verändert keine Quelldaten.
"""
import json
from pathlib import Path
from datetime import date

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "curated" / "S" / "csv"
MIG = ROOT / "data" / "migration" / "S" / "csv"
OUT = ROOT / "meine-ergebnisse" / "cockpit-daten" / "akte.js"

partner = pd.read_csv(CSV / "partner.csv")
vertrag = pd.read_csv(CSV / "vertrag.csv")
antrag = pd.read_csv(CSV / "antrag.csv")
deckung = pd.read_csv(CSV / "deckung.csv")
schaden = pd.read_csv(CSV / "schaden.csv")
position = pd.read_csv(CSV / "schaden_position.csv")
interaktion = pd.read_csv(CSV / "interaktion.csv")
dokument = pd.read_csv(CSV / "dokument.csv")
mitarbeiter = pd.read_csv(CSV / "mitarbeiter.csv")
vertrag_xref = pd.read_csv(MIG / "vertrag_xref.csv")
migrationslog = pd.read_csv(MIG / "migrationslog.csv")

P_ID, V_ID, S_ID = "PTR-00000008", "VTR-00000801", "SCH-00000810"

p = partner[partner["partner_id"] == P_ID].iloc[0]
v = vertrag[vertrag["vertrag_id"] == V_ID].iloc[0]
s = schaden[schaden["schaden_id"] == S_ID].iloc[0]
pos = position[position["schaden_id"] == S_ID].set_index("position_id")


def mit_name(mit_id):
    row = mitarbeiter[mitarbeiter["mitarbeiter_id"] == mit_id]
    if row.empty:
        return mit_id
    r = row.iloc[0]
    return f"{r['vorname']} {r['nachname']}, {r['rolle']}"


def txt(df, id_col, id_val):
    row = df[df[id_col] == id_val]
    if row.empty:
        return ""
    v = row.iloc[0]["text_body"]
    return "" if pd.isna(v) else str(v)


def absaetze(rohtext):
    """Text in Absätze zerlegen; eine mit Leerzeichen ausgerichtete
    Vergleichstabelle (Spalten 'bisher'/'neu') in klare Zeilen mit
    Doppelpunkt umbauen, da der Browser mehrfache Leerzeichen zusammenfasst."""
    result = []
    for absatz in rohtext.split("\n\n"):
        zeilen = absatz.split("\n")
        if len(zeilen) >= 2 and "bisher" in zeilen[0] and "neu" in zeilen[0]:
            for zeile in zeilen[1:]:
                teile = [t for t in __import__("re").split(r"\s{2,}", zeile.strip()) if t]
                if len(teile) == 3:
                    label, bisher, neu = teile
                    result.append(f"{label} — bisher: {bisher}; neu: {neu}")
                else:
                    result.append(zeile.strip())
        else:
            result.append(absatz)
    return result


def abs_emp_dokument(dok_id):
    row = dokument[dokument["dokument_id"] == dok_id].iloc[0]
    return row["absender"], row["empfaenger"]


AYLIN = mit_name("MIT-00009")
MIRIAM = mit_name("MIT-00012")
JONAS = mit_name("MIT-00010")

# --- Kacheln ---
schadentag = s["schadendatum"]
zahlungsdatum = pos.loc["SCH-00000810-04", "datum"]
tage_bis_zahlung = (date.fromisoformat(zahlungsdatum) - date.fromisoformat(schadentag)).days
bezahlt_total = float(s["bezahlt_total"])

anzahl_dokumente_tabelle = len(dokument[dokument["partner_id"] == P_ID])
anzahl_interaktionen = len(interaktion[interaktion["partner_id"] == P_ID])
anzahl_dateien = anzahl_dokumente_tabelle + anzahl_interaktionen

kacheln = [
    {
        "titel": "Schadentag",
        "wert": schadentag,
        "definition": "Tag des Schadenereignisses laut Schadentabelle.",
    },
    {
        "titel": "Tage bis zur Zahlung",
        "wert": str(tage_bis_zahlung),
        "definition": f"Kalendertage vom Schadentag ({schadentag}) bis zur Regulierungszahlung an den Geschädigten ({zahlungsdatum}).",
    },
    {
        "titel": "Bezahlter Betrag",
        "wert": f"EUR {bezahlt_total:,.2f}".replace(",", "'"),
        "definition": "Summe aller Zahlungen aus der Schadentabelle: Regulierung an den Geschädigten und Kulanz an den Versicherungsnehmer.",
    },
    {
        "titel": "Zahl der Dokumente",
        "wert": str(anzahl_dateien),
        "definition": f"Dokumente ({anzahl_dokumente_tabelle}) und Kontakte einschliesslich E-Mails ({anzahl_interaktionen}) der Fallakte zusammen.",
    },
]

# --- Kopfzeile ---
xref_hapo = vertrag_xref[(vertrag_xref["curated_id"] == V_ID) & (vertrag_xref["quellsystem"] == "HAPO")].iloc[0]
kopfzeile = {
    "kunde": f"{p['vorname']} {p['nachname']}",
    "vertrag": f"{V_ID} · Privathaftpflicht Deutschland, seit {v['beginn']}",
    "versicherungsschein": f"vormals {xref_hapo['quell_id']} (HAPO), migriert nach MINT am {xref_hapo['gueltig_bis']}",
    "schaden": f"{S_ID} (Anzeige {s['schadennummer_anzeige']}) · Hundebiss vom {s['schadendatum']}, Status {s['status'].lower()}",
}

GRUPPEN_NAMEN = {
    "kunde": "Kunde",
    "schaden": "Schadenabteilung",
    "intern": "intern und IT",
    "ombudsmann": "Ombudsmann",
    "aufsicht": "Aufsicht",
}

# --- Ereignisse ---
# art: "Brief" | "E-Mail" | "Telefonnotiz" | "Dokument" | "Tabellenereignis"
ereignisse = []

# Die drei Wendepunkte der Fallgeschichte: Fehler wird wirksam, Fehler wird
# korrigiert, Fall wird abgeschlossen. Zuordnung über die Kennung des Ereignisses.
WENDEPUNKTE = {
    "INT-00000802": {"nr": 1, "bezeichnung": "Wendepunkt 1: Fehler wird wirksam"},
    "INT-00000808": {"nr": 2, "bezeichnung": "Wendepunkt 2: Fehler korrigiert"},
    "INT-00000824": {"nr": 3, "bezeichnung": "Wendepunkt 3: Fall abgeschlossen"},
}


def add(datum, art, titel, gruppen, sender_gruppe, absender=None, empfaenger=None,
        kennung=None, quelle=None, text=None):
    ereignisse.append({
        "id": f"EV-{len(ereignisse) + 1:02d}",
        "datum": datum,
        "art": art,
        "titel": titel,
        "gruppen": gruppen,
        "senderGruppe": sender_gruppe,
        "absender": absender,
        "empfaenger": empfaenger,
        "kennung": kennung,
        "quelle": quelle,
        "text": text,
        "wendepunkt": WENDEPUNKTE.get(kennung),
    })


ant = antrag[antrag["antrag_id"] == v["antrag_id"]].iloc[0]

add(ant["eingang"], "Tabellenereignis", "Antrag Privathaftpflicht eingereicht",
    ["kunde"], "kunde", quelle="Antragstabelle",
    text=["Antrag auf eine Privathaftpflichtversicherung eingereicht, Vertriebsweg Agentur (Generalagentur Elbland Petrov, Dresden)."])

add(ant["entscheid_am"], "Tabellenereignis", "Antrag angenommen",
    ["kunde"], "kunde", quelle="Antragstabelle",
    text=["Antrag angenommen: normale Annahme ohne Zuschlag, nicht automatisiert entschieden."])

add(v["beginn"], "Tabellenereignis", "Vertragsbeginn Privathaftpflicht",
    ["kunde"], "kunde", quelle="Vertragstabelle",
    text=[f"Vertrag {V_ID} beginnt (damalige Policennummer {xref_hapo['quell_id']} im Altsystem HAPO). Versicherungssumme EUR {v['versicherungssumme']:,.0f}, Jahresprämie brutto EUR {v['jahrespraemie_brutto']:.2f}.".replace(",", "'")])

dbp_abs, dbp_emp = abs_emp_dokument("DOK-00000802")
add("2019-02-12", "Dokument", "Beratung zum Einschluss Tierhalterbaustein",
    ["kunde"], "kunde", absender=dbp_abs, empfaenger=dbp_emp, kennung="DOK-00000802",
    text=absaetze(txt(dokument, "dokument_id", "DOK-00000802")))

dnt_abs, dnt_emp = abs_emp_dokument("DOK-00000801")
add("2019-02-15", "Dokument", "Nachtrag Nr. 2: Einschluss Tierhalterhaftpflicht, wirksam 01.03.2019",
    ["kunde"], "kunde", absender=dnt_abs, empfaenger=dnt_emp, kennung="DOK-00000801",
    text=absaetze(txt(dokument, "dokument_id", "DOK-00000801")))

mig = migrationslog[(migrationslog["quell_id"] == xref_hapo["quell_id"]) & (migrationslog["ziel_id"] == V_ID)].iloc[0]
add("2025-03-03", "Tabellenereignis", "Migration nach MINT (Pilotwelle Privathaftpflicht Deutschland)",
    ["intern"], "intern", quelle="Migrationslog",
    text=["Bausteincode Tierhalter (BST=01) wird beim Mapping nicht ins Zielschema übernommen, Feld bleibt leer. Warnung im Migrationslog: „" + mig["meldung"] + "“"])

add("2025-03-21T16:35", "Telefonnotiz", "Schadenmeldung Hundebiss",
    ["kunde", "schaden"], "kunde",
    absender=f"{p['vorname']} {p['nachname']}", empfaenger="Contact Center Leipzig",
    kennung="INT-00000801", text=absaetze(txt(interaktion, "interaktion_id", "INT-00000801")))

add(pos.loc["SCH-00000810-01", "datum"], "Tabellenereignis", "Erstreserve gebildet",
    ["schaden"], "schaden", quelle="Schadenposition 01",
    text=[f"Reserve EUR {pos.loc['SCH-00000810-01','betrag']:.2f}: {pos.loc['SCH-00000810-01','beschreibung']}"])

dar_abs, dar_emp = abs_emp_dokument("DOK-00000803")
add("2025-03-21", "Dokument", "Notfallbehandlung des Geschädigten, Arztrechnung",
    ["kunde"], "kunde", absender=dar_abs, empfaenger=dar_emp, kennung="DOK-00000803",
    text=absaetze(txt(dokument, "dokument_id", "DOK-00000803")))

add(pos.loc["SCH-00000810-02", "datum"], "Tabellenereignis", "Reserve aufgelöst, automatische Ablehnung",
    ["schaden"], "schaden", quelle="Schadenposition 02",
    text=[f"Reserve auf EUR {pos.loc['SCH-00000810-02','betrag']:.2f}: {pos.loc['SCH-00000810-02','beschreibung']}"])

add("2025-03-24", "Brief", "Ablehnung des Schadens (automatisch)",
    ["schaden", "kunde"], "schaden",
    absender="Pfefferminzia Versicherung AG, Niederlassung Deutschland, Schaden Haftpflicht (maschinell erstellt, ohne Unterschrift)",
    empfaenger=f"{p['vorname']} {p['nachname']}",
    kennung="INT-00000802", text=absaetze(txt(interaktion, "interaktion_id", "INT-00000802")))

add("2025-03-28", "Brief", "Erste Beschwerde: Ablehnung unberechtigt",
    ["kunde", "schaden"], "kunde",
    absender=f"{p['vorname']} {p['nachname']}", empfaenger=AYLIN,
    kennung="INT-00000803", text=absaetze(txt(interaktion, "interaktion_id", "INT-00000803")))

add("2025-04-02T11:20", "E-Mail", "Eingangsbestätigung der Beschwerde",
    ["schaden", "kunde"], "schaden",
    absender="Pfefferminzia, Kundenservice Leipzig", empfaenger=f"{p['vorname']} {p['nachname']}",
    kennung="INT-00000804", text=absaetze(txt(interaktion, "interaktion_id", "INT-00000804")))

add("2025-04-15", "Brief", "Zweite Beschwerde: Ombudsmann und BaFin angekündigt",
    ["kunde", "intern"], "kunde",
    absender=f"{p['vorname']} {p['nachname']}", empfaenger=MIRIAM,
    kennung="INT-00000805", text=absaetze(txt(interaktion, "interaktion_id", "INT-00000805")))

add("2025-04-16T09:05", "E-Mail", "Interne Eskalation: automatische Ablehnung trotz Baustein",
    ["schaden", "intern"], "schaden",
    absender=AYLIN, empfaenger=f"{JONAS}, {MIRIAM} (Cc Martina Jost)",
    kennung="INT-00000806", text=absaetze(txt(interaktion, "interaktion_id", "INT-00000806")))

add("2025-04-16T14:40", "E-Mail", "Ursache gefunden: Migrationsmapping und Vier-Augen-Lücke",
    ["intern", "schaden"], "intern",
    absender=JONAS, empfaenger=AYLIN,
    kennung="INT-00000807", text=absaetze(txt(interaktion, "interaktion_id", "INT-00000807")))

add("2025-04-17", "Tabellenereignis", "Baustein Tierhalter manuell nachgetragen",
    ["intern"], "intern", quelle="Migrationslog",
    text=["Baustein am 17.04.2025 manuell im Vertrag nachgetragen, nachmigriert am 18.04.2025."])

add(pos.loc["SCH-00000810-03", "datum"], "Tabellenereignis", "Reserve wiedereröffnet",
    ["schaden"], "schaden", quelle="Schadenposition 03",
    text=[f"Reserve EUR {pos.loc['SCH-00000810-03','betrag']:.2f}: {pos.loc['SCH-00000810-03','beschreibung']}"])

add(pos.loc["SCH-00000810-04", "datum"], "Tabellenereignis", "Regulierungszahlung an den Geschädigten",
    ["schaden"], "schaden", quelle="Schadenposition 04",
    text=[f"Zahlung EUR {pos.loc['SCH-00000810-04','betrag']:.2f} an {pos.loc['SCH-00000810-04','empfaenger']}: {pos.loc['SCH-00000810-04','beschreibung']}"])

add(pos.loc["SCH-00000810-05", "datum"], "Tabellenereignis", "Kulanzzahlung an den Versicherungsnehmer",
    ["schaden", "kunde"], "schaden", quelle="Schadenposition 05",
    text=[f"Zahlung EUR {pos.loc['SCH-00000810-05','betrag']:.2f} an {pos.loc['SCH-00000810-05','empfaenger']}: {pos.loc['SCH-00000810-05','beschreibung']}"])

add("2025-04-17", "Brief", "Regulierung und Entschuldigung",
    ["schaden", "kunde"], "schaden",
    absender=AYLIN, empfaenger=f"{p['vorname']} {p['nachname']}",
    kennung="INT-00000808", text=absaetze(txt(interaktion, "interaktion_id", "INT-00000808")))

add("2025-04-18", "Tabellenereignis", "Nachmigration der betroffenen Verträge",
    ["intern"], "intern", quelle="Migrationslog",
    text=["Nachmigration der 214 von demselben Migrationsfehler betroffenen Verträge der Pilotwelle (unternehmensweit)."])

add(pos.loc["SCH-00000810-06", "datum"], "Tabellenereignis", "Schaden geschlossen",
    ["schaden"], "schaden", quelle="Schadenposition 06",
    text=["Reserve auf EUR 0.00, Schaden geschlossen."])

add("2025-04-24", "Brief", "Anfrage des Versicherungsombudsmanns",
    ["ombudsmann", "intern"], "ombudsmann",
    absender="Versicherungsombudsmann e. V., Referat Haftpflicht", empfaenger=f"{MIRIAM}, Beschwerdestelle Deutschland",
    kennung="INT-00000809", text=absaetze(txt(interaktion, "interaktion_id", "INT-00000809")))

dmemo_abs, dmemo_emp = abs_emp_dokument("DOK-00000804")
add("2025-05-06", "Dokument", "Root-Cause-Analyse Vorfall VF-2025-03",
    ["intern"], "intern", absender=dmemo_abs, empfaenger=dmemo_emp, kennung="DOK-00000804",
    text=absaetze(txt(dokument, "dokument_id", "DOK-00000804")))

add("2025-05-08", "Brief", "Stellungnahme an den Ombudsmann",
    ["intern", "ombudsmann"], "intern",
    absender=MIRIAM, empfaenger="Versicherungsombudsmann e. V., Referat Haftpflicht",
    kennung="INT-00000811", text=absaetze(txt(interaktion, "interaktion_id", "INT-00000811")))

add("2025-05-20", "Tabellenereignis", "Beschwerde bei der BaFin (nur erwähnt)",
    ["kunde", "aufsicht"], "kunde", quelle="erwähnt in Dokument DOK-00000805",
    text=["Herr Pieper wendet sich schriftlich an die Bundesanstalt für Finanzdienstleistungsaufsicht. Das Schreiben selbst liegt der Fallakte nicht vor, nur die Erwähnung im Antwortschreiben der Aufsicht."])

daufs_abs, daufs_emp = abs_emp_dokument("DOK-00000805")
add("2025-06-10", "Dokument", "Anfrage der BaFin, Bitte um Stellungnahme",
    ["aufsicht", "intern"], "aufsicht", absender=daufs_abs, empfaenger=daufs_emp, kennung="DOK-00000805",
    text=absaetze(txt(dokument, "dokument_id", "DOK-00000805")))

add("2025-07-07", "Brief", "Bitte um schriftliche Zusicherung",
    ["kunde", "schaden"], "kunde",
    absender=f"{p['vorname']} {p['nachname']}", empfaenger=AYLIN,
    kennung="INT-00000823", text=absaetze(txt(interaktion, "interaktion_id", "INT-00000823")))

add("2025-07-14", "Brief", "Schriftliche Zusicherung: keine automatisierte Ablehnung mehr ohne Prüfung",
    ["schaden", "kunde"], "schaden",
    absender=AYLIN, empfaenger=f"{p['vorname']} {p['nachname']}",
    kennung="INT-00000824", text=absaetze(txt(interaktion, "interaktion_id", "INT-00000824")))

ereignisse.sort(key=lambda e: e["datum"])

ablehnung_datum = interaktion[interaktion["interaktion_id"] == "INT-00000802"].iloc[0]["zeitpunkt"][:10]
zahlung_datum = pos.loc["SCH-00000810-04", "datum"]
tage_ablehnung_zahlung = (date.fromisoformat(zahlung_datum) - date.fromisoformat(ablehnung_datum)).days

kennzahlAblehnungZahlung = {
    "tage": tage_ablehnung_zahlung,
    "ablehnungDatum": ablehnung_datum,
    "zahlungDatum": zahlung_datum,
    "definition": "Kalendertage von der automatisierten Ablehnung (Interaktion INT-00000802) bis zur Regulierungszahlung an den Geschädigten (Schadenposition 04).",
}

# --- Faktencheck der beiden Entwürfe in meine-ergebnisse/ ---
# Geprüft werden die eigenen Entwürfe, wie sie dort liegen, nie die Schreiben,
# die damals tatsächlich rausgingen. Jedes Zitat muss wortgleich im Entwurf
# vorkommen, sonst bricht das Skript ab.
ERGEBNISSE = ROOT / "meine-ergebnisse"


def lade_brief(dateiname):
    rohtext = (ERGEBNISSE / dateiname).read_text(encoding="utf-8").strip()
    zeilen = rohtext.split("\n")
    meta = zeilen[0]
    rest = "\n".join(zeilen[1:]).strip()
    absaetze_liste = [a for a in rest.split("\n\n") if a.strip()]
    return {
        "volltext": rest,
        "meta": meta,
        "betreff": absaetze_liste[0],
        "anrede": absaetze_liste[1],
        "absaetze": absaetze_liste[2:-2],
        "gruss": absaetze_liste[-2],
        "unterschrift": absaetze_liste[-1].split("\n"),
    }


def zeile(aussage, status, ampel, quelle, bemerkung=""):
    assert status in ("belegt", "vermutet", "nicht belegt")
    assert ampel in ("gruen", "gelb", "rot")
    return {"aussage": aussage, "status": status, "ampel": ampel, "quelle": quelle, "bemerkung": bemerkung}


def pruefe_zitate(brief, zeilen_liste):
    for z in zeilen_liste:
        if z["aussage"] not in brief["volltext"]:
            raise SystemExit(
                f"Zitat nicht wortgleich im Entwurf gefunden, Abbruch: {z['aussage']!r}"
            )


brief_kunde = lade_brief("pieper-antwort-kunde.md")
brief_ombudsmann = lade_brief("pieper-stellungnahme-ombudsmann.md")

FAKTENCHECK_REGEL = (
    "Grün: Aussage ist in einer Tabelle, einem Dokument oder einer eindeutigen Nachrechnung belegt, "
    "und die dafür nötige Quelle liegt nicht nach dem Datum des Schreibens. "
    "Gelb: Aussage ist nur vermutet — etwa eine Zahl fürs ganze Unternehmen, die sich in unseren eigenen "
    "Tabellen (Datensatz Stufe S) nicht nachzählen lässt, oder eine Regel, die nur in einer späteren "
    "Fassung eines Regelwerks belegt ist. Rot: Aussage ist nicht belegt, oder die einzige verfügbare "
    "Quelle liegt nach dem Datum des Schreibens — auch wenn die Sache später zutraf."
)

zeilen_kunde = [
    zeile("Sie haben recht, und wir haben einen Fehler gemacht.", "belegt", "gruen",
          "Beschwerderichtlinie R05, Anhang A, Textbaustein «Anerkennung»",
          "Zulässiger Textbaustein, identisch mit dem historischen Schreiben INT-00000808 vom 17.04.2025 — Übernahme von Textbausteinen ist ausdrücklich erlaubt."),
    zeile("Ihre Schreiben vom 28. März 2025 und vom 15. April 2025 zu Ihrem Schaden SCH-00000810", "belegt", "gruen",
          "Interaktion INT-00000803 (Brief vom 28.03.2025), Interaktion INT-00000805 (Brief vom 15.04.2025), Schadentabelle SCH-00000810",
          "Beide Quellen liegen vor dem Datum dieses Schreibens (17.04.2025)."),
    zeile("den Hundebiss vom 21. März 2025", "belegt", "gruen", "Schadentabelle, Schaden SCH-00000810, Schadentag"),
    zeile("unsere Ablehnung vom 24. März 2025", "belegt", "gruen", "Interaktion INT-00000802 (Brief vom 24.03.2025)"),
    zeile("die Standardmail vom 2. April 2025", "belegt", "gruen", "Interaktion INT-00000804 (E-Mail vom 02.04.2025)"),
    zeile("danach lange nichts mehr von uns gehört", "belegt", "gruen",
          "Kontakttabelle: kein weiterer ausgehender Kontakt an Hans-Georg Pieper zwischen Interaktion INT-00000804 und diesem Schreiben",
          "Geprüft durch Fehlen eines Gegenbelegs in der Kontakttabelle, nicht durch eine positive Erwähnung."),
    zeile("Es war kein Mensch, sondern ein Computerprogramm in unserem Schadensystem", "belegt", "gruen",
          "Interaktion INT-00000806 und INT-00000807 (interne E-Mails vom 16.04.2025)"),
    zeile("Ihr Vertrag ist Anfang März 2025 in unser neues System übernommen worden", "belegt", "gruen",
          "Vertragstabelle VTR-00000801, Feld migriert am (03.03.2025); Migrationslog"),
    zeile("der Baustein Tierhalterhaftpflicht, den Sie seit dem 1. März 2019 eingeschlossen haben", "belegt", "gruen",
          "Dokument DOK-00000801 (Nachtrag Nr. 2, wirksam 01.03.2019)"),
    zeile("versehentlich vergessen", "belegt", "gruen",
          "Migrationslog, Vertrag VTR-00000801 (Bausteincode Tierhalter nicht ins Zielschema übernommen)"),
    zeile("ohne dass zuvor eine Mitarbeiterin oder ein Mitarbeiter dies gesehen hat", "belegt", "gruen",
          "Interaktion INT-00000806 vom 16.04.2025; Interaktion INT-00000802 selbst (maschinell erstellt, ohne Unterschrift)"),
    zeile("die Frist von 14 Tagen, die Sie uns in Ihrem Schreiben vom 28. März 2025 gesetzt hatten", "belegt", "gruen",
          "Interaktion INT-00000803 (\"binnen 14 Tagen\")"),
    zeile("Diese Frist lief am 11. April 2025 ab", "belegt", "gruen",
          "Nachgerechnet: Interaktion INT-00000803 (28.03.2025) plus 14 Kalendertage",
          "Zählweise Kalendertage."),
    zeile("reguliert haben wir den Schaden erst heute, sechs Tage später", "belegt", "gruen",
          "Schadenposition SCH-00000810-04 (Zahlung 17.04.2025); nachgerechnet 17.04. minus 11.04. = 6 Tage"),
    zeile("Wir haben den Baustein Tierhalterhaftpflicht heute wieder in Ihrem Vertrag eingetragen", "belegt", "gruen",
          "Migrationslog, Vertrag VTR-00000801 (Baustein am 17.04.2025 manuell nachgetragen)",
          "Nach der Korrektur (voriger Entwurf: „ist ab sofort wieder ... hinterlegt“, Ampel rot, weil die im Migrationslog vermerkte Nachmigration erst auf den 18.04.2025 datierte). Die jetzige Formulierung behauptet nur den manuellen Eintrag vom 17.04.2025 selbst, der belegt und taggleich ist; die spätere technische Nachmigration (18.04.2025) wird nicht mehr behauptet."),
    zeile("An Herrn M. sind EUR 1.240,00 für Arztkosten, Schmerzensgeld und die beschädigte Hose überwiesen worden", "belegt", "gruen",
          "Schadenposition SCH-00000810-04 (17.04.2025)"),
    zeile("auf den vertraglichen Selbstbehalt von EUR 150,00 verzichten wir bei dieser Zahlung", "belegt", "gruen",
          "Schadenposition SCH-00000810-04; Deckungstabelle DEK-00000801-01 (Selbstbehalt EUR 150 fix)",
          "Ursprünglich nahezu wortgleich mit dem historischen Schreiben INT-00000808 (\"Den Selbstbehalt von EUR 150,00 aus Ihrem Vertrag ziehen wir nicht ab.\"); im Zuge dieser Prüfung umformuliert."),
    zeile("erhalten Sie von uns zusätzlich EUR 100,00", "belegt", "gruen",
          "Schadenposition SCH-00000810-05 (17.04.2025)",
          "Ursprünglich wortgleich mit dem historischen Schreiben INT-00000808 (\"Fuer Ihren Aufwand und die Verzoegerung ueberweisen wir Ihnen zusaetzlich EUR 100,00 auf das uns bekannte Konto.\"); im Zuge dieser Prüfung umformuliert."),
    zeile("Ab sofort sieht bei jeder Ablehnung zuerst ein Mensch Ihren Fall an, bevor ein Brief an Sie geht.", "belegt", "gruen",
          "Regelwerk RW-GRUPPE-R08-2025, Version 2.1, gültig ab 16.04.2025",
          "Satz von der Teamleiterin wörtlich vorgegeben; inhaltlich geprüft und bestätigt."),
    zeile("Bei Fragen können Sie mich jederzeit unter der unten angegebenen Telefonnummer erreichen.", "belegt", "gruen",
          "kein Tatsachengehalt, Höflichkeitsfloskel",
          "Ursprünglich wortgleich mit dem historischen Schreiben INT-00000808 (\"Fuer Rueckfragen erreichen Sie mich direkt unter der unten stehenden Nummer.\"); im Zuge dieser Prüfung umformuliert."),
]
pruefe_zitate(brief_kunde, zeilen_kunde)

zeilen_ombudsmann = [
    zeile("Ihre Anfrage vom 24. April 2025 (Az. O-2025-04-1187)", "belegt", "gruen",
          "Interaktion INT-00000809 (Brief vom 24.04.2025, Az. O-2025-04-1187)"),
    zeile("die von Ihnen gesetzte Frist von drei Wochen läuft am 15. Mai 2025 ab", "belegt", "gruen",
          "Nachgerechnet: Interaktion INT-00000809 (\"innerhalb von drei Wochen\") ab 24.04.2025 plus 21 Kalendertage"),
    zeile("wir antworten Ihnen damit sieben Tage vor Fristablauf", "belegt", "gruen",
          "Nachgerechnet: 15.05.2025 minus 08.05.2025 (Datum dieses Schreibens)"),
    zeile("Er wurde am 12. Februar 2019 beraten", "belegt", "gruen", "Dokument DOK-00000802 (Beratungsprotokoll, 12.02.2019)"),
    zeile("mit Nachtrag Nr. 2 vom 15. Februar 2019 zum 1. März 2019 in den Vertrag aufgenommen", "belegt", "gruen",
          "Dokument DOK-00000801 (Nachtrag Nr. 2, erstellt 15.02.2019, wirksam 01.03.2019)",
          "Kernangaben (Vertrag, Baustein, Daten) sind zwangsläufig ähnlich wie im historischen Schreiben INT-00000811 formuliert, da es sich um dieselben Fakten handelt; Satzbau bewusst abweichend gehalten."),
    zeile("Die Deckung ist zu keinem späteren Zeitpunkt entfallen oder gekündigt worden", "belegt", "gruen",
          "Deckungstabelle, Baustein BS-TIER-HUND zu Vertrag VTR-00000801 (kein Enddatum eingetragen)"),
    zeile("Am 3. März 2025 wurde der Vertrag im Rahmen einer vorgezogenen Migrationswelle für Privathaftpflichtverträge in Deutschland in unser neues Bestandssystem überführt", "belegt", "gruen",
          "Vertragstabelle VTR-00000801 (migriert am 03.03.2025); Migrationslog, Welle HP-2025-PILOT"),
    zeile("Der Code für den Baustein Tierhalterhaftpflicht ging bei dieser Überführung verloren und wurde im neuen System nicht angelegt", "belegt", "gruen",
          "Migrationslog, Vertrag VTR-00000801 (Bausteincode Tierhalter nicht ins Zielschema übernommen)"),
    zeile("Als die Schadenmeldung vom 21. März 2025 einging", "belegt", "gruen", "Schadentabelle, Schaden SCH-00000810, Schadentag"),
    zeile("Ja, die Ablehnung kam ohne jede menschliche Beteiligung zustande", "belegt", "gruen",
          "Interaktion INT-00000806 und INT-00000807 (16.04.2025); Interaktion INT-00000802 (\"maschinell erstellt, ohne Unterschrift\")"),
    zeile("Bereits zum Zeitpunkt der Ablehnung galt bei uns intern der Grundsatz, dass über eine Ablehnung immer ein Mensch entscheidet", "belegt", "gruen",
          "Regelwerk RW-GRUPPE-R08-2025, Präambel (Grundsatz § 5 Nr. 2 galt schon in Version 2.0)",
          "Beleg ist die rückblickende Aussage der Präambel von Version 2.1; der Wortlaut von Version 2.0 selbst liegt nicht vor."),
    zeile("dieser Grundsatz wurde in diesem Fall nicht beachtet, weil die zuständige Regel technisch nicht als prüfpflichtige Entscheidung eingestuft war", "belegt", "gruen",
          "Interaktion INT-00000807 vom 16.04.2025"),
    zeile("Die Zahlung an den Geschädigten in Höhe von EUR 1.240,00 für Arztkosten, Schmerzensgeld und die beschädigte Kleidung ist am 17. April 2025 erfolgt", "belegt", "gruen",
          "Schadenposition SCH-00000810-04"),
    zeile("den vertraglich vorgesehenen Selbstbehalt von EUR 150,00 haben wir dabei nicht in Abzug gebracht", "belegt", "gruen",
          "Schadenposition SCH-00000810-04; Deckungstabelle DEK-00000801-01"),
    zeile("Am selben Tag haben wir Herrn Pieper EUR 100,00 als Kulanz für seinen Aufwand und die Wartezeit ausgezahlt", "belegt", "gruen",
          "Schadenposition SCH-00000810-05 (17.04.2025)"),
    zeile("und uns schriftlich bei ihm entschuldigt", "belegt", "gruen", "Interaktion INT-00000808 (Brief vom 17.04.2025)"),
    zeile("Wir haben den Eingang fristgerecht am 2. April 2025 bestätigt", "vermutet", "gelb",
          "Interaktion INT-00000804 (E-Mail vom 02.04.2025); Beschwerderichtlinie R05 § 4 Nr. 1 (Eingangsbestätigung innert fünf Arbeitstagen)",
          "Die Fünf-Arbeitstage-Regel ist nur in der ab 01.05.2025 gültigen Fassung 2025.2 dokumentiert; ob sie am 28.03./02.04.2025 in dieser Form bereits galt, ist nicht belegt."),
    zeile("eine inhaltliche Prüfung und Korrektur erfolgten jedoch nicht innerhalb der von Herrn Pieper gesetzten Frist von 14 Tagen, die am 11. April 2025 ablief", "belegt", "gruen",
          "Interaktion INT-00000803; nachgerechnet 28.03.2025 plus 14 Kalendertage"),
    zeile("Reguliert haben wir erst am 17. April 2025, sechs Tage nach Ablauf dieser Frist", "belegt", "gruen",
          "Schadenposition SCH-00000810-04; nachgerechnet"),
    zeile("erst nach einer zweiten, deutlich schärferen Beschwerde vom 15. April 2025", "belegt", "gruen", "Interaktion INT-00000805"),
    zeile("Innerhalb unserer eigenen internen Bearbeitungsfrist von 15 Arbeitstagen lag die Regulierung noch, am 14. Arbeitstag nach der ersten Beschwerde", "vermutet", "gelb",
          "Nachgerechnet: Arbeitstage 29.03.–17.04.2025, keine Feiertage in diesem Fenster (Karfreitag 18.04., Ostermontag 21.04. liegen danach); Beschwerderichtlinie R05 § 4 Nr. 2 (Antwort innert 15 Arbeitstagen)",
          "Die Tageszählung selbst ist nachgerechnet und belegt; ob die 15-Arbeitstage-Regel am 28.03.2025 in dieser Form bereits galt, ist nicht belegt, nur vermutet."),
    zeile("Die betroffene Regel unseres Schadensystems wurde am 16. April 2025 deaktiviert", "belegt", "gruen", "Interaktion INT-00000807 (16.04.2025)"),
    zeile("Der Baustein wurde im Vertrag von Herrn Pieper am 17. April 2025 manuell nachgetragen", "belegt", "gruen", "Migrationslog, Vertrag VTR-00000801"),
    zeile("Nach unserer internen Auswertung vom 6. Mai 2025 waren insgesamt elf Schadenfälle von dieser automatisierten Fehlablehnung betroffen", "vermutet", "gelb",
          "Dokument DOK-00000804 (Root-Cause-Analyse, 06.05.2025)",
          "Zahl fürs ganze Unternehmen; im Datensatz Stufe S liegt nur der Schadenfall SCH-00000810 vor, die Zahl elf lässt sich in unseren eigenen Tabellen nicht nachzählen. Die jetzige Formulierung nennt die Quelle (interne Auswertung vom 6. Mai 2025) immerhin transparent im Schreiben selbst; das ändert an der fehlenden eigenen Nachzählbarkeit nichts, bleibt deshalb gelb."),
    zeile("die übrigen zehn hat unser Haus aus eigener Initiative aufgegriffen und bis zum 25. April 2025 abschließend bearbeitet", "vermutet", "gelb",
          "Dokument DOK-00000804 (06.05.2025)",
          "Unternehmensweite Zahl, nicht nachzählbar. Ursprünglich nahe an der Formulierung des historischen Schreibens INT-00000811 (\"wiedereröffnet und reguliert\"); umformuliert."),
    zeile("Nach derselben internen Auswertung vom 6. Mai 2025 waren zudem 214 Verträge dieser Migrationswelle von demselben Migrationsfehler betroffen", "vermutet", "gelb",
          "Dokument DOK-00000804 (06.05.2025: 214 Verträge)",
          "Zahl fürs ganze Unternehmen, in Stufe S nicht nachzählbar; Quelle jetzt transparent im Schreiben genannt, bleibt aber gelb."),
    zeile("sie wurden am 18. April 2025 nachträglich korrekt übertragen", "belegt", "gruen",
          "Migrationslog, Vertrag VTR-00000801 (nachmigriert 18.04.2025); Dokument DOK-00000804 (Nachmigration 18.04.) für die Gesamtzahl",
          "Für Piepers eigenen Vertrag ist das Datum unmittelbar belegt; die Übertragung auf alle 214 Verträge stützt sich auf dieselbe unternehmensweite Auswertung wie oben."),
    zeile("das fehlerhafte Zuordnungsschema wurde noch vor der bevorstehenden Hauptwelle der Migration Haftpflicht am 15. Mai 2025 korrigiert", "belegt", "gruen",
          "Dokument DOK-00000804 (06.05.2025: Mapping vor der Hauptwelle korrigiert)"),
    zeile("Seit dem 16. April 2025 gilt in unserer Kompetenzordnung (R08, Fassung 2.1) zusätzlich eine technische Absicherung", "belegt", "gruen",
          "Regelwerk RW-GRUPPE-R08-2025, Version 2.1, gültig ab 16.04.2025"),
    zeile("ein Anteil der automatisierten Entscheidungen wird zusätzlich stichprobenweise nachgeprüft", "belegt", "gruen",
          "Regelwerk RW-GRUPPE-R08-2025 § 5 Nr. 4 (zehn Prozent werden manuell nachgeprüft)"),
    zeile("Seit dem 1. Mai 2025 gilt zudem eine überarbeitete Beschwerderichtlinie (R05, Fassung 2025.2)", "belegt", "gruen",
          "Regelwerk RW-GRUPPE-R05-2025, Version 2025.2, gültig ab 01.05.2025"),
    zeile("Beschwerden über automatisierte Entscheidungen erhalten Priorität 1 und werden innerhalb von zwei Arbeitstagen darauf geprüft, ob bereits eine Überprüfung durch eine natürliche Person stattgefunden hat", "belegt", "gruen",
          "Regelwerk RW-GRUPPE-R05-2025 § 5 Nr. 3"),
    zeile("Die Meldung dieses Vorfalls an das unternehmensinterne Gremium für Modellrisiken ist veranlasst; die Befassung ist für eine Sitzung im September 2025 vorgesehen und hat zum jetzigen Zeitpunkt noch nicht stattgefunden", "belegt", "gruen",
          "Dokument DOK-00000804 (06.05.2025: Bericht an das Technology & AI Committee in der Sitzung 09/2025)",
          "Korrekt als veranlasst/nicht erledigt gekennzeichnet, konsistent mit der Quelle."),
    zeile("Wir sind zu dem Ergebnis gekommen, dass die Beschwerde von Herrn Pieper zu Recht erhoben wurde", "belegt", "gruen",
          "Schadenfall insgesamt (Regulierung, interne E-Mails, Root-Cause-Analyse)",
          "Ursprünglich nahe an der Formulierung des historischen Schreibens INT-00000811 (\"Wir bedauern den Vorfall und betrachten die Beschwerde als berechtigt.\"); umformuliert."),
]
pruefe_zitate(brief_ombudsmann, zeilen_ombudsmann)

VOLLSTAENDIGKEIT_KUNDE = [
    "Keine wesentliche inhaltliche Lücke gefunden.",
    "Einzige Auffälligkeit: Die Aussage «ist ab sofort wieder in Ihrem Vertrag hinterlegt» stützt sich auf den manuellen Eintrag vom 17.04.2025; die vollständige technische Nachmigration ist im Migrationslog erst für den 18.04.2025 vermerkt, einen Tag nach diesem Schreiben (siehe Zeile, Ampel rot).",
]
VOLLSTAENDIGKEIT_OMBUDSMANN = [
    "Der Root-Cause-Analyse vom 06.05.2025 zufolge wurde der Vorfall zusätzlich im Modellinventar erfasst (Eintrag zu Vorfall VF-2025-03) und als meldepflichtiger Vorfall der KI-Governance-Richtlinie eingestuft; beides war am Datum dieser Stellungnahme bekannt, im Entwurf aber nicht erwähnt.",
]

faktencheck = {
    "regel": FAKTENCHECK_REGEL,
    "briefe": [
        {
            "id": "kunde", "titel": "Antwort an Herrn Pieper", "dateiname": "pieper-antwort-kunde.md",
            "datum": "2025-04-17", "meta": brief_kunde["meta"],
            "betreff": brief_kunde["betreff"], "anrede": brief_kunde["anrede"],
            "absaetze": brief_kunde["absaetze"], "gruss": brief_kunde["gruss"],
            "unterschrift": brief_kunde["unterschrift"],
            "zeilen": zeilen_kunde, "vollstaendigkeit": VOLLSTAENDIGKEIT_KUNDE,
        },
        {
            "id": "ombudsmann", "titel": "Stellungnahme an den Versicherungsombudsmann", "dateiname": "pieper-stellungnahme-ombudsmann.md",
            "datum": "2025-05-08", "meta": brief_ombudsmann["meta"],
            "betreff": brief_ombudsmann["betreff"], "anrede": brief_ombudsmann["anrede"],
            "absaetze": brief_ombudsmann["absaetze"], "gruss": brief_ombudsmann["gruss"],
            "unterschrift": brief_ombudsmann["unterschrift"],
            "zeilen": zeilen_ombudsmann, "vollstaendigkeit": VOLLSTAENDIGKEIT_OMBUDSMANN,
        },
    ],
}

daten = {
    "kopfzeile": kopfzeile,
    "kacheln": kacheln,
    "gruppenNamen": GRUPPEN_NAMEN,
    "gruppenReihenfolge": ["kunde", "schaden", "intern", "ombudsmann", "aufsicht"],
    "kennzahlAblehnungZahlung": kennzahlAblehnungZahlung,
    "ereignisse": ereignisse,
    "faktencheck": faktencheck,
}

OUT.write_text("const AKTE_DATEN = " + json.dumps(daten, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
print(f"Geschrieben: {OUT} ({len(ereignisse)} Ereignisse)")
