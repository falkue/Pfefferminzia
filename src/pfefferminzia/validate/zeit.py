"""Zeitkonsistenz-Checks (Datenarchitektur 5.5) fuer Partner, Antrag und Vertrag."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from pfefferminzia.validate.registry import CheckErgebnis, check

if TYPE_CHECKING:
    from pfefferminzia.context import RunContext


def _d(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce")


@check("zeit_vertrag", "Vertrag: Beginn >= 18. Geburtstag des VN, Antrag vor Beginn, Ende nach Beginn, Stichtag", klasse="zeit",
       reihenfolge=40)
def zeit_vertrag(ctx: RunContext, erg: CheckErgebnis) -> None:
    if not (ctx.tabellen.has("vertrag") and ctx.tabellen.has("partner")):
        erg.uebersprungen, erg.grund = True, "vertrag/partner fehlen"
        return
    v = ctx.tabellen.get("vertrag")
    p = ctx.tabellen.get("partner").set_index("partner_id")
    stichtag = pd.Timestamp(ctx.config.zeit.stichtag)
    beginn, ablauf, storno = _d(v["beginn"]), _d(v["ablauf"]), _d(v["storno_datum"])
    geburt = _d(v["versicherungsnehmer_id"].map(p["geburtsdatum"]))
    typ = v["versicherungsnehmer_id"].map(p["partner_typ"])
    zu_jung = (typ == "NATUERLICH") & ((beginn - geburt).dt.days < 18 * 365.25)
    if zu_jung.any():
        erg.fehler(f"{int(zu_jung.sum())} Vertraege mit VN unter 18 bei Beginn", tabelle="curated/vertrag", anzahl=int(zu_jung.sum()))
    nach_stichtag = beginn > stichtag
    if nach_stichtag.any():
        erg.fehler(f"{int(nach_stichtag.sum())} Vertraege beginnen nach dem Stichtag", tabelle="curated/vertrag", anzahl=int(nach_stichtag.sum()))
    ende_vor_beginn = storno.notna() & (storno < beginn)
    if ende_vor_beginn.any():
        erg.fehler(f"{int(ende_vor_beginn.sum())} Vertraege enden vor Beginn", tabelle="curated/vertrag", anzahl=int(ende_vor_beginn.sum()))
    aktiv_mit_storno = (v["status"] == "AKTIV") & storno.notna()
    if aktiv_mit_storno.any():
        erg.fehler(f"{int(aktiv_mit_storno.sum())} aktive Vertraege mit Stornodatum", tabelle="curated/vertrag")
    beendet_ohne = (~v["status"].isin(["AKTIV", "RUHEND", "ANTRAG"])) & storno.isna()
    if beendet_ohne.any():
        erg.fehler(f"{int(beendet_ohne.sum())} beendete Vertraege ohne Enddatum", tabelle="curated/vertrag")
    ablauf_vor_beginn = ablauf.notna() & (ablauf <= beginn)
    if ablauf_vor_beginn.any():
        erg.fehler(f"{int(ablauf_vor_beginn.sum())} Vertraege mit Ablauf vor Beginn", tabelle="curated/vertrag")
    if ctx.tabellen.has("antrag"):
        a = ctx.tabellen.get("antrag").set_index("antrag_id")
        ein = _d(v["antrag_id"].map(a["eingang"]))
        ent = _d(v["antrag_id"].map(a["entscheid_am"]))
        falsch = (ein > ent) | (ent > beginn + pd.Timedelta(days=30))
        if falsch.any():
            erg.fehler(f"{int(falsch.sum())} Vertraege mit Antrag/Entscheid nach Beginn", tabelle="curated/antrag", anzahl=int(falsch.sum()))
    # Verstorbene: keine aktiven Vertraege nach Todesdatum
    tod = _d(v["versicherungsnehmer_id"].map(p["todesdatum"]))
    aktiv_tot = (v["status"] == "AKTIV") & tod.notna() & (tod <= stichtag)
    if aktiv_tot.any():
        erg.warnung(f"{int(aktiv_tot.sum())} aktive Vertraege verstorbener VN (DQ-26 nur in raw erlaubt)", tabelle="curated/vertrag")
    erg.info(f"{len(v)} Vertraege geprueft")


@check("zeit_partner", "Partner: Geburtsdatum plausibel, Todesdatum nach Geburt, Adresshistorie ohne Ueberlappung", klasse="zeit",
       reihenfolge=41)
def zeit_partner(ctx: RunContext, erg: CheckErgebnis) -> None:
    if not ctx.tabellen.has("partner"):
        erg.uebersprungen, erg.grund = True, "partner fehlt"
        return
    p = ctx.tabellen.get("partner")
    stichtag = pd.Timestamp(ctx.config.zeit.stichtag)
    geb = _d(p["geburtsdatum"])
    nat = p["partner_typ"] == "NATUERLICH"
    alt = nat & ((stichtag - geb).dt.days > 105 * 365.25)
    if alt.any():
        erg.fehler(f"{int(alt.sum())} Partner aelter als 105 Jahre", tabelle="curated/partner")
    tod = _d(p["todesdatum"])
    tod_falsch = tod.notna() & ((tod < geb) | (tod > stichtag))
    if tod_falsch.any():
        erg.fehler(f"{int(tod_falsch.sum())} Todesdaten ausserhalb Geburt..Stichtag", tabelle="curated/partner")
    status_falsch = (p["status"] == "VERSTORBEN") != tod.notna()
    if status_falsch.any():
        erg.fehler(f"{int(status_falsch.sum())} Partner mit Status/Todesdatum-Widerspruch", tabelle="curated/partner")
    if ctx.tabellen.has("partner_adresse"):
        a = ctx.tabellen.get("partner_adresse")
        von, bis = _d(a["gueltig_von"]), _d(a["gueltig_bis"])
        falsch = bis.notna() & (bis < von)
        if falsch.any():
            erg.fehler(f"{int(falsch.sum())} Adressen mit gueltig_bis vor gueltig_von", tabelle="curated/partner_adresse")
        mehrfach_aktuell = a[a["ist_aktuell"]].groupby("partner_id").size()
        if (mehrfach_aktuell > 1).any():
            erg.fehler(f"{int((mehrfach_aktuell > 1).sum())} Partner mit mehreren aktuellen Adressen", tabelle="curated/partner_adresse")
    erg.info(f"{len(p)} Partner geprueft")
