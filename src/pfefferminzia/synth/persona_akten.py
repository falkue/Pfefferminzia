"""Stufen ``schaden`` (Persona-Schaeden), ``prozess`` (Persona-Korrespondenz und Dokumente) und ``render``
(Dateien der Persona-Akten).

In Welle 1 fuellen diese Stufen ausschliesslich die Akten der zehn Kunden-Personas aus
``akten_inhalte.py`` und ``akten_inhalte_2.py``. Die flaechige Erzeugung fuer alle Vertraege folgt in
den Wellen 2 und 5. Tabellen: schaden, schaden_position, interaktion, dokument (curated),
schaden_latent (truth). Dateien: ``data/documents/<Stufe>/personas/<PTR>/…`` als Markdown mit
Frontmatter (Briefe, Notizen, Berichte) und als EML (E-Mails).
"""

from __future__ import annotations

from datetime import date, datetime

import pandas as pd

from pfefferminzia.context import RunContext
from pfefferminzia.export import _relativ
from pfefferminzia.ids import mint_schadennummer, silas_schadennummer
from pfefferminzia.manifest import sha256_datei
from pfefferminzia.pipeline import Stage, register
from pfefferminzia.synth.akten_inhalte import AKTEN
from pfefferminzia.synth.akten_inhalte_2 import AKTEN_2
from pfefferminzia.tarifblaetter import render_tarifblaetter

ALLE_AKTEN = {**AKTEN, **AKTEN_2}
DISCLAIMER = "Fiktives Lehrbeispiel. Alle Daten synthetisch. Keine Verbindung zu realen Personen, Unternehmen oder Marken."
ORG_JE_SB = {"MIT-00007": "ORG-033", "MIT-00008": "ORG-042", "MIT-00009": "ORG-032", "MIT-00012": "ORG-084", "MIT-00013": "ORG-037",
             "MIT-00005": "ORG-080", "MIT-00006": "ORG-085", "MIT-00010": "ORG-063"}


def _d(s: str | None) -> date | None:
    return date.fromisoformat(s) if s else None


def _dt(s: str) -> datetime:
    return datetime.fromisoformat(s)


def schaden_tabellen(ctx: RunContext) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    vertrag = ctx.tabellen.get("vertrag").set_index("vertrag_id")
    zeilen, positionen, latent = [], [], []
    silas_n = {}
    for pid, akte in ALLE_AKTEN.items():
        for s in akte["schaeden"]:
            v = vertrag.loc[s["vertrag"]] if s["vertrag"] in vertrag.index else None
            quelle = "MINT" if (v is not None and (v["quellsystem"] == "MINT" or _d(s["meldung"]) >= date(2025, 7, 1))) else "SILAS"
            jahr = _d(s["meldung"]).year
            silas_n[jahr] = silas_n.get(jahr, 1000) + 1
            nummer = silas_schadennummer(jahr, silas_n[jahr]) if quelle == "SILAS" else mint_schadennummer(jahr, silas_n[jahr])
            zeilen.append({
                "schaden_id": s["id"], "schadennummer_anzeige": nummer, "vertrag_id": s["vertrag"], "partner_id": pid,
                "sparte": "LV" if s["art"].startswith("LV") else "HP", "art": s["art"], "ursache_code": s["ursache"],
                "schadendatum": _d(s["datum"]), "meldedatum": _d(s["meldung"]), "erfassungsdatum": _d(s["meldung"]),
                "meldekanal": s["kanal"], "schadenort_plz": s["plz"], "schadenort_land": s["land"], "beschreibung_kurz": s["kurz"],
                "status": s["status"], "status_seit": _d(s["seit"]), "reserve_aktuell": s["reserve"], "bezahlt_total": s["bezahlt"],
                "regress_total": s["regress"], "waehrung": s["waehrung"], "deckung_geprueft": True, "deckung_ergebnis": s["deckung"],
                "ablehnungsgrund_code": s["ablehnung"], "sachbearbeiter_id": s["sb"], "org_einheit_id": ORG_JE_SB.get(s["sb"]) if s["sb"] else None,
                "geschaedigter_text": s["geschaedigter"], "betrugsverdacht_sichtbar": s["betrug_sichtbar"], "quellsystem": quelle,
                "ist_persona_fall": True,
            })
            for i, (art, betrag, datum, empf, text) in enumerate(s["positionen"], start=1):
                positionen.append({"position_id": f"{s['id']}-{i:02d}", "schaden_id": s["id"], "art": art, "betrag": betrag, "waehrung": s["waehrung"],
                                   "datum": _d(datum), "empfaenger": empf, "beschreibung": text})
            latent.append({"schaden_id": s["id"], "betrug_wahr": s["betrug_wahr"], "betrugsmuster": ("F7/F1/F2" if s["betrug_wahr"] else None),
                           "bemerkung": "Persona-Fall, siehe docs/personas/kunden"})
    return pd.DataFrame(zeilen), pd.DataFrame(positionen), pd.DataFrame(latent)


def interaktion_tabelle(ctx: RunContext) -> pd.DataFrame:
    """Vermittler-IDs der Akten werden auf den Vermittler des zugehoerigen Vertrags abgebildet (Stufe-unabhaengig)."""
    vertrag = ctx.tabellen.get("vertrag").set_index("vertrag_id")
    schaden_vertrag = {}
    for akte in ALLE_AKTEN.values():
        for sch in akte["schaeden"]:
            schaden_vertrag[sch["id"]] = sch["vertrag"]
    antrag_vertrag = {r["antrag_id"]: v for v, r in vertrag.iterrows()} if "antrag_id" in vertrag.columns else {}
    bekannt = set(ctx.tabellen.get("vermittler")["vermittler_id"])

    def vermittler_fuer(i: dict) -> str | None:
        if i["vermittler"] in bekannt:
            return i["vermittler"]
        vid = {"VERTRAG": i["bezug_id"], "SCHADEN": schaden_vertrag.get(i["bezug_id"]), "ANTRAG": antrag_vertrag.get(i["bezug_id"])}.get(i["bezug_typ"])
        if vid in vertrag.index and pd.notna(vertrag.loc[vid, "vermittler_id"]):
            return str(vertrag.loc[vid, "vermittler_id"])
        return None

    zeilen = []
    for pid, akte in ALLE_AKTEN.items():
        for i in akte["interaktionen"]:
            zeilen.append({
                "interaktion_id": i["id"], "kanal": i["kanal"], "richtung": i["richtung"], "zeitpunkt": _dt(i["zeit"]),
                "dauer_sekunden": None, "partner_id": pid, "mitarbeiter_id": i["mitarbeiter"], "vermittler_id": vermittler_fuer(i) if i["vermittler"] else None,
                "bezug_typ": i["bezug_typ"], "bezug_id": i["bezug_id"], "thread_id": i["thread"], "betreff": i["betreff"],
                "zusammenfassung": None, "sprache": i["sprache"], "sentiment_agent": i["sentiment"],
                "datei_pfad": None, "text_body": i["text"], "ist_persona_fall": True,
            })
    return pd.DataFrame(zeilen)


def dokument_tabelle(ctx: RunContext) -> pd.DataFrame:
    zeilen = []
    for pid, akte in ALLE_AKTEN.items():
        for d in akte["dokumente"]:
            art, bezug_id = d["bezug"]
            zeilen.append({
                "dokument_id": d["id"], "dokument_typ": d["typ"], "richtung": d["richtung"], "format": d["format"], "ist_gerendert": False,
                "ocr_qualitaet": d["ocr"], "seiten": d["seiten"], "titel": d["titel"], "absender": d["absender"], "empfaenger": d["empfaenger"],
                "partner_id": pid, "vertrag_id": bezug_id if art == "vertrag" else None, "schaden_id": bezug_id if art == "schaden" else None,
                "antrag_id": bezug_id if art == "antrag" else None, "interaktion_id": None, "erstellt_am": _d(d["datum"]),
                "quellsystem": "DOKU" if _d(d["datum"]) < date(2025, 5, 15) else "MINT", "datei_pfad": None, "text_body": d["text"],
                "ist_persona_fall": True,
            })
    return pd.DataFrame(zeilen)


def _frontmatter(**k) -> str:
    zeilen = ["---"]
    for key, val in k.items():
        zeilen.append(f"{key}: {val if val is not None else 'null'}")
    zeilen.append("---")
    return "\n".join(zeilen) + "\n\n"


def render(ctx: RunContext, dok: pd.DataFrame, inter: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    basis = ctx.pfade.documents / ctx.stufe / "personas"
    partner = ctx.tabellen.get("partner").set_index("partner_id")
    pfade_dok, pfade_int = {}, {}
    for _, d in dok.iterrows():
        ordner = basis / d["partner_id"]
        ordner.mkdir(parents=True, exist_ok=True)
        pfad = ordner / f"{d['dokument_id']}_{d['dokument_typ'].lower()}.md"
        p = partner.loc[d["partner_id"]]
        markt = str(p["land_wohnsitz"])
        inhalt = _frontmatter(dokument_id=d["dokument_id"], titel=f'"{d["titel"]}"', typ="kunde" if d["richtung"] != "INTERN" else "intern",
                              dokument_typ=d["dokument_typ"], sparte="GRUPPE", markt=markt, sprache="de-CH" if markt == "CH" else "de-DE",
                              version='"1.0"', erstellt_am=d["erstellt_am"].isoformat(), absender=f'"{d["absender"]}"', empfaenger=f'"{d["empfaenger"]}"',
                              partner_id=d["partner_id"], vertrag_id=d["vertrag_id"], schaden_id=d["schaden_id"], antrag_id=d["antrag_id"],
                              ocr_qualitaet=d["ocr_qualitaet"], quelle_system=d["quellsystem"], vertraulichkeit="vertraulich")
        inhalt += f"# {d['titel']}\n\n{d['text_body']}\n\n---\n\n{DISCLAIMER}\n"
        pfad.write_text(inhalt, encoding="utf-8")
        pfade_dok[d["dokument_id"]] = _relativ(pfad, ctx.root)
        if ctx.manifest is not None:
            ctx.manifest.add_datei(pfade_dok[d["dokument_id"]], sha256_datei(pfad))
    for _, i in inter.iterrows():
        ordner = basis / i["partner_id"]
        ordner.mkdir(parents=True, exist_ok=True)
        p = partner.loc[i["partner_id"]]
        if i["kanal"] == "EMAIL":
            pfad = ordner / f"{i['interaktion_id']}.eml"
            kunde = f"{p['vorname']} {p['nachname']}" if pd.notna(p["vorname"]) else str(p["firmenname"])
            kunde_mail = f"{str(p['vorname'] or 'info').lower()}.{str(p['nachname'] or 'firma').lower()}@mail.example".replace(" ", "")
            firma = "schaden-de@pfefferminzia.example" if i["richtung"] == "AUSGEHEND" and p["land_wohnsitz"] == "DE" else "service@pfefferminzia.example"
            von, an = (kunde_mail, firma) if i["richtung"] == "EINGEHEND" else ((firma, kunde_mail) if i["richtung"] == "AUSGEHEND" else ("intern@pfefferminzia.example", "intern@pfefferminzia.example"))
            inhalt = (f"From: {kunde if i['richtung'] == 'EINGEHEND' else 'Pfefferminzia'} <{von}>\nTo: <{an}>\n"
                      f"Date: {i['zeitpunkt'].strftime('%a, %d %b %Y %H:%M:%S +0100')}\nSubject: {i['betreff']}\nMessage-ID: <{i['interaktion_id']}@pfefferminzia.example>\n"
                      f"X-Thread-ID: {i['thread_id']}\nX-Bezug: {i['bezug_typ']} {i['bezug_id'] or ''}\nContent-Type: text/plain; charset=utf-8\n\n{i['text_body']}\n\n-- \n{DISCLAIMER}\n")
        else:
            pfad = ordner / f"{i['interaktion_id']}_{i['kanal'].lower()}.md"
            inhalt = _frontmatter(interaktion_id=i["interaktion_id"], kanal=i["kanal"], richtung=i["richtung"], zeitpunkt=i["zeitpunkt"].isoformat(),
                                  partner_id=i["partner_id"], mitarbeiter_id=i["mitarbeiter_id"], bezug_typ=i["bezug_typ"], bezug_id=i["bezug_id"],
                                  thread_id=i["thread_id"], betreff=f'"{i["betreff"]}"', sprache=i["sprache"])
            inhalt += f"# {i['betreff']}\n\n{i['text_body']}\n\n---\n\n{DISCLAIMER}\n"
        pfad.write_text(inhalt, encoding="utf-8")
        pfade_int[i["interaktion_id"]] = _relativ(pfad, ctx.root)
        if ctx.manifest is not None:
            ctx.manifest.add_datei(pfade_int[i["interaktion_id"]], sha256_datei(pfad))
    dok = dok.copy()
    dok["datei_pfad"] = dok["dokument_id"].map(pfade_dok)
    dok["ist_gerendert"] = dok["datei_pfad"].notna()
    inter = inter.copy()
    inter["datei_pfad"] = inter["interaktion_id"].map(pfade_int)
    return dok, inter


@register
class SchadenStage(Stage):
    name, nummer, welle = "schaden", 50, 1
    beschreibung = "Schaeden/Leistungsfaelle: Persona-Akten (Welle 1), flaechig ab Welle 5"

    def run(self, ctx: RunContext) -> None:
        if not ctx.tabellen.has("vertrag"):
            self.stub(ctx)
            return
        s, pos, lat = schaden_tabellen(ctx)
        ctx.tabellen.register("schaden", s, ersetzen=True)
        ctx.tabellen.register("schaden_position", pos, ersetzen=True)
        ctx.tabellen.register("schaden_latent", lat, layer="truth", ersetzen=True)
        ctx.ereignis(self.name, f"{len(s)} Persona-Schaeden mit {len(pos)} Positionen")


@register
class ProzessStage(Stage):
    name, nummer, welle = "prozess", 70, 1
    beschreibung = "Interaktionen und Dokumente: Persona-Akten (Welle 1), flaechig ab Welle 2"

    def run(self, ctx: RunContext) -> None:
        if not ctx.tabellen.has("partner"):
            self.stub(ctx)
            return
        ctx.tabellen.register("interaktion", interaktion_tabelle(ctx), ersetzen=True)
        ctx.tabellen.register("dokument", dokument_tabelle(ctx), ersetzen=True)
        ctx.ereignis(self.name, f"{len(ctx.tabellen.get('interaktion'))} Interaktionen, {len(ctx.tabellen.get('dokument'))} Dokumente (Personas)")


@register
class RenderStage(Stage):
    name, nummer, welle = "render", 85, 1
    beschreibung = "Persona-Akten und Tarifblaetter unter data/documents"

    def run(self, ctx: RunContext) -> None:
        if ctx.stufe_config.dokumente_rendern == "keine":
            ctx.ereignis(self.name, "Rendering fuer diese Stufe deaktiviert")
            return
        tarifpfade = render_tarifblaetter(ctx)
        if not (ctx.tabellen.has("dokument") and ctx.tabellen.has("interaktion")):
            ctx.ereignis(self.name, f"{len(tarifpfade) // 2} Tarifblaetter als Markdown und PDF gerendert")
            return
        dok, inter = render(ctx, ctx.tabellen.get("dokument"), ctx.tabellen.get("interaktion"))
        ctx.tabellen.register("dokument", dok, ersetzen=True)
        ctx.tabellen.register("interaktion", inter, ersetzen=True)
        ctx.ereignis(
            self.name,
            f"{int(dok['ist_gerendert'].sum())} Dokumente, {inter['datei_pfad'].notna().sum()} Interaktionen "
            f"und {len(tarifpfade) // 2} Tarifblaetter gerendert",
        )
