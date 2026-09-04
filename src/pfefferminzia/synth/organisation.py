"""Stufe ``organisation``: Org-Einheiten, Mitarbeiter, Agenturen, Vermittler, Produkte, Tarifgenerationen.

Personas aus ``data/reference/personas_mitarbeiter.csv`` belegen die ersten Mitarbeiter-IDs; alle
weiteren Mitarbeitenden werden synthetisch erzeugt. Agenturen und Vermittler folgen dem Mengengeruest
der Konfiguration (Datenarchitektur 3.2).
"""

from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

from pfefferminzia.context import RunContext
from pfefferminzia.ids import agentur_id, mitarbeiter_id, vermittler_id
from pfefferminzia.pipeline import Stage, register
from pfefferminzia.synth.addresses import AddressSynth
from pfefferminzia.synth.identifiers import email_mitarbeiter, telefon
from pfefferminzia.synth.names import NameSynth, firmenname
from pfefferminzia.validate.fiction import lade_blocklist

AGENTUR_TYPEN = [  # typ, markt, anzahl-gewicht, kanal
    ("EXKLUSIVAGENTUR", "CH", 30, "agentur"), ("EXKLUSIVAGENTUR", "DE", 12, "agentur"),
    ("MAKLER", "CH", 14, "makler"), ("MAKLER", "DE", 22, "makler"),
    ("BANK", "CH", 1, "bank"), ("BANK", "DE", 1, "bank"),
    ("PORTAL", "DE", 2, "direkt"), ("DIREKT", "CH", 1, "direkt"), ("DIREKT", "DE", 1, "direkt"),
]
AGENTUR_ZUSATZ = {"EXKLUSIVAGENTUR": "Generalagentur", "MAKLER": "Versicherungsmakler", "BANK": "Bank",
                  "PORTAL": "Vergleichsportal", "DIREKT": "Direktvertrieb"}


def _synths(ctx: RunContext) -> tuple[NameSynth, AddressSynth, pd.DataFrame]:
    ref = ctx.reference
    ns = NameSynth(ref.csv("namen.vornamen"), ref.csv("namen.nachnamen"), lade_blocklist(ctx))
    ad = AddressSynth(ref.csv("geo.orte_ch"), ref.csv("geo.orte_de"), ref.csv("geo.strassennamen"))
    return ns, ad, ref.csv("namen.firmennamen_bausteine")


def org_einheiten(ctx: RunContext) -> pd.DataFrame:
    o = ctx.reference.csv("organisationseinheiten").copy()
    o = o.rename(columns={"org_id": "org_einheit_id", "uebergeordnet_org_id": "uebergeordnet_id"})
    o["fte"] = o["fte"].astype(int)
    o["ebene"] = o["ebene"].astype(int)
    return o[["org_einheit_id", "kuerzel", "name", "uebergeordnet_id", "ebene", "standort", "land", "fte",
              "herkunft", "leitung_rolle"]]


def mitarbeiter(ctx: RunContext, orgs: pd.DataFrame) -> pd.DataFrame:
    ns, _, _ = _synths(ctx)
    personas = ctx.reference.csv("personas_mitarbeiter.csv")
    kuerzel_zu_id = dict(zip(orgs["kuerzel"], orgs["org_einheit_id"], strict=True))
    ziel = ctx.menge("mitarbeiter", 60)
    zeilen: list[dict] = []
    for _, p in personas.iterrows():
        n = int(p["mitarbeiter_id"].split("-")[1])
        zeilen.append({
            "mitarbeiter_id": p["mitarbeiter_id"], "personalnummer": None, "vorname": p["vorname"],
            "nachname": p["nachname"], "geschlecht": p["geschlecht"], "geburtsjahr": int(p["geburtsjahr"]),
            "rolle": p["rolle"], "org_einheit_id": kuerzel_zu_id.get(p["org_kuerzel"]), "org_kuerzel": p["org_kuerzel"],
            "standort": p["standort"], "land": p["land"], "herkunft": p["herkunft"], "eintritt": date(int(p["eintrittsjahr"]), 1, 1),
            "austritt": None, "sprache": p["sprache"], "ki_haltung": p["ki_haltung"], "email": p["email"],
            "kompetenzstufe": 4 if p["org_kuerzel"] in ("GL", "DAO", "IT", "RM", "LEGAL", "HR") else 2,
            "ist_persona": True, "_n": n,
        })
    # Synthetische Mitarbeitende: Verteilung ueber operative Einheiten der Ebene 3 nach FTE
    op = orgs[(orgs["ebene"] == 3) & (orgs["fte"] > 0)].copy()
    gew = op["fte"].to_numpy(dtype=float)
    rollen = {"SL": ("Sachbearbeiter/in Schaden", "Teamleiter/in Schaden"), "UW": ("Underwriter/in", "Senior Underwriter/in"),
              "KS": ("Kundenberater/in", "Teamleiter/in Service"), "VT": ("Vertriebsbetreuer/in", "Regionalleiter/in"),
              "DAO": ("Data Scientist", "ML Engineer"), "IT": ("Systemspezialist/in", "Applikationsverantwortliche/r"),
              "FIN": ("Controller/in", "Buchhalter/in"), "RM": ("Risk Manager/in", "Modellvalidator/in"),
              "AKT": ("Aktuar/in", "Aktuarielle/r Analyst/in"), "HR": ("HR-Berater/in", "HR-Assistent/in"),
              "COMP": ("Compliance-Spezialist/in", "Beschwerdemanager/in"), "LEG": ("Jurist/in", "Paralegal"),
              "BV": ("Sachbearbeiter/in Bestand", "Teamleiter/in Bestand"), "SIU": ("Betrugsermittler/in", "Analyst/in SIU"),
              "REG": ("Regress-Spezialist/in", "Sachbearbeiter/in Regress"), "PM": ("Produktmanager/in", "Produktanalyst/in"),
              "PROZ": ("Prozessmanager/in", "Business Analyst/in")}
    n = len(personas) + 1
    while len(zeilen) < ziel:
        rng = ctx.rng("mitarbeiter", n)
        einheit = op.iloc[int(rng.choice(len(op), p=gew / gew.sum()))]
        herk = str(einheit["herkunft"])
        if herk == "gemischt":
            herk = str(rng.choice(["pfefferminz", "minzia", "neu"], p=[0.6, 0.25, 0.15]))
        land = str(einheit["land"])
        sprache = "de-CH" if land == "CH" else "de-DE"
        geschlecht = "W" if rng.random() < 0.52 else "M"
        geburtsjahr = int(np.clip(rng.normal(1982, 11), 1960, 2002))
        if herk == "minzia":
            eintritt_jahr = int(rng.integers(2019, 2025))
        elif herk == "neu":
            eintritt_jahr = 2025
        else:
            eintritt_jahr = int(np.clip(rng.integers(max(geburtsjahr + 20, 1990), 2025), 1990, 2024))
        person = ns.person(rng, geschlecht, land, geburtsjahr, "de")
        praefix = next((k for k in rollen if str(einheit["kuerzel"]).startswith(k)), None)
        rolle = rollen.get(praefix, ("Sachbearbeiter/in", "Fachspezialist/in"))[0 if rng.random() < 0.8 else 1]
        austritt = None
        if rng.random() < 0.06:  # Abgaenge nach dem Merger
            austritt = date(2025, int(rng.integers(2, 13)), 1)
        zeilen.append({
            "mitarbeiter_id": mitarbeiter_id(n), "personalnummer": None, "vorname": person.vorname,
            "nachname": person.nachname, "geschlecht": geschlecht, "geburtsjahr": geburtsjahr, "rolle": rolle,
            "org_einheit_id": einheit["org_einheit_id"], "org_kuerzel": einheit["kuerzel"], "standort": einheit["standort"],
            "land": land, "herkunft": herk, "eintritt": date(eintritt_jahr, int(rng.integers(1, 13)), 1), "austritt": austritt,
            "sprache": sprache, "ki_haltung": str(rng.choice(["skeptisch", "neutral", "befuerwortend", "treibend"],
                                                             p=[0.3, 0.35, 0.28, 0.07] if herk == "pfefferminz" else [0.05, 0.25, 0.5, 0.2])),
            "email": email_mitarbeiter(person.vorname, person.nachname), "kompetenzstufe": 2 if "Senior" in rolle or "Teamleiter" in rolle else 1,
            "ist_persona": False, "_n": n,
        })
        n += 1
    df = pd.DataFrame(zeilen)
    # Personalnummern nur fuer Ex-Pfefferminz (5-stellig, raw), MINT-Handle fuer alle
    df["personalnummer"] = [f"{10000 + i * 7 % 89999:05d}" if h == "pfefferminz" else None
                            for i, h in zip(df["_n"], df["herkunft"], strict=True)]
    df["mint_handle"] = [f"{v.lower()}.{nn.lower()}".replace(" ", "-") for v, nn in zip(df["vorname"], df["nachname"], strict=True)]
    return df.drop(columns=["_n"])


def agenturen_und_vermittler(ctx: RunContext) -> tuple[pd.DataFrame, pd.DataFrame]:
    ns, ad, bausteine = _synths(ctx)
    ziel_ag, ziel_vm = ctx.menge("agenturen", 12), ctx.menge("vermittler", 40)
    gew = np.array([t[2] for t in AGENTUR_TYPEN], dtype=float)
    ag_zeilen: list[dict] = []
    # Direkt und Bank je Markt sind Pflicht (Kanaele muessen existieren)
    pflicht = [t for t in AGENTUR_TYPEN if t[0] in ("DIREKT", "BANK")]
    n = 1
    for typ, markt, _, kanal in pflicht:
        ag_zeilen.append(_agentur(ctx, n, typ, markt, kanal, ns, ad, bausteine))
        n += 1
    while len(ag_zeilen) < ziel_ag:
        rng = ctx.rng("agentur", n)
        typ, markt, _, kanal = AGENTUR_TYPEN[int(rng.choice(len(AGENTUR_TYPEN), p=gew / gew.sum()))]
        if typ in ("DIREKT", "BANK"):
            continue
        ag_zeilen.append(_agentur(ctx, n, typ, markt, kanal, ns, ad, bausteine))
        n += 1
    ag = pd.DataFrame(ag_zeilen)
    vm_zeilen: list[dict] = []
    m = 1
    # Long-Tail: grosse Agenturen erhalten mehr Vermittler
    ag_gew = ag["groesse_gewicht"].to_numpy(dtype=float)
    while len(vm_zeilen) < ziel_vm:
        rng = ctx.rng("vermittler", m)
        a = ag.iloc[int(rng.choice(len(ag), p=ag_gew / ag_gew.sum()))]
        geschlecht = "W" if rng.random() < 0.42 else "M"
        geburtsjahr = int(np.clip(rng.normal(1975, 11), 1950, 1998))
        p = ns.person(rng, geschlecht, str(a["land"]), geburtsjahr, "de")
        vm_zeilen.append({
            "vermittler_id": vermittler_id(m), "agentur_id": a["agentur_id"], "vorname": p.vorname, "nachname": p.nachname,
            "geschlecht": geschlecht, "geburtsjahr": geburtsjahr, "markt": a["land"], "kanal": a["kanal"],
            "vermittlernummer_alt": f"{int(rng.integers(10000, 99999)):05d}", "vermittlernummer": f"{int(rng.integers(10000, 99999)):05d}",
            "aktiv_seit": date(int(np.clip(rng.integers(max(geburtsjahr + 22, 1995), 2025), 1995, 2025)), 1, 1),
            "aktiv_bis": None if rng.random() > 0.08 else date(int(rng.integers(2019, 2025)), 12, 31),
            "quellsystem": "MINT" if a["kanal"] == "direkt" else "PVS",
            "leistungsgewicht": float(rng.pareto(1.5) + 0.3),
        })
        m += 1
    return ag.drop(columns=["groesse_gewicht"]), pd.DataFrame(vm_zeilen)


def _agentur(ctx, n, typ, markt, kanal, ns, ad, bausteine) -> dict:
    rng = ctx.rng("agentur", n)
    adr = ad.adresse(rng, markt)
    if typ == "DIREKT":
        name = "Pfefferminzia Direkt" if markt == "CH" else "Pfefferminzia App (ehemals minzia.direct)"
    elif typ == "BANK":
        name = "Aare-Bank AG" if markt == "CH" else "Sächsische Genossenschaftskasse eG"
    elif typ == "PORTAL":
        name = str(rng.choice(["VergleichsWerk", "TarifKompass", "PolicenPilot"])) + " (Portal)"
    else:
        stamm = firmenname(rng, bausteine, markt, lade_blocklist(ctx)).split(" ")[0]
        p = ns.person(rng, "M" if rng.random() < 0.6 else "W", markt, 1970, "de")
        name = (f"Generalagentur {stamm} {p.nachname}" if typ == "EXKLUSIVAGENTUR"
                else f"{p.nachname} & Partner Versicherungsmakler {'AG' if markt == 'CH' else 'GmbH'}")
    return {
        "agentur_id": agentur_id(n), "name": name, "typ": typ, "kanal": kanal, "land": markt,
        "plz": adr.plz, "ort": adr.ort, "region": adr.region, "agenturnummer": f"{n:04d}",
        "seit": date(int(rng.integers(1990, 2022)) if typ != "DIREKT" else 2021, 1, 1),
        "herkunft": "minzia" if (typ in ("DIREKT", "PORTAL") and markt == "DE") else "pfefferminz",
        "groesse_gewicht": float(rng.pareto(1.2) + 0.5) * (3.0 if typ in ("DIREKT", "MAKLER") else 1.0),
    }


def produkte_und_generationen(ctx: RunContext) -> tuple[pd.DataFrame, pd.DataFrame]:
    hp, lv = ctx.reference.verzeichnis("hp"), ctx.reference.verzeichnis("lv")
    p_hp = hp["produkte"].rename(columns={"kuerzel": "produkt_id"})
    p_hp = p_hp.assign(sparte="HP", maerkte=p_hp["maerkte"])[["produkt_id", "marktname", "sparte", "maerkte", "status"]]
    p_lv = lv["produkte"].rename(columns={"produkt_code": "produkt_id"})
    p_lv = (p_lv.groupby("produkt_id", as_index=False).agg(marktname=("marktname", "first"), status=("status", "first"),
                                                            maerkte=("markt", lambda s: ";".join(sorted(set(s)))))
            .assign(sparte="LV"))[["produkt_id", "marktname", "sparte", "maerkte", "status"]]
    produkte = pd.concat([p_hp, p_lv], ignore_index=True)
    g_hp = hp["tarifgenerationen"].rename(columns={"kuerzel": "tarifgeneration_id"})
    g_hp = g_hp.assign(sparte="HP")[["tarifgeneration_id", "sparte", "bezeichnung", "herkunft", "gueltig_ab", "gueltig_bis",
                                     "produkte", "maerkte", "anteil_bestand_pct"]]
    g_lv = lv["tarifgenerationen"].rename(columns={"generation_code": "tarifgeneration_id"})
    g_lv = g_lv.assign(sparte="LV", maerkte="CH;DE")[["tarifgeneration_id", "sparte", "bezeichnung", "herkunft", "gueltig_ab",
                                                    "gueltig_bis", "produkte", "maerkte", "bestandsanteil_pct"]]
    g_lv = g_lv.rename(columns={"bestandsanteil_pct": "anteil_bestand_pct"})
    gen = pd.concat([g_hp, g_lv], ignore_index=True)
    gen["herkunft"] = gen["herkunft"].str.lower()
    gen["gueltig_ab"] = pd.to_datetime(gen["gueltig_ab"]).dt.date
    gen["gueltig_bis"] = pd.to_datetime(gen["gueltig_bis"]).dt.date
    return produkte, gen


@register
class OrganisationStage(Stage):
    name, nummer, welle = "organisation", 20, 1
    beschreibung = "Org-Einheiten, Mitarbeiter, Agenturen, Vermittler, Produkte, Tarifgenerationen"

    def run(self, ctx: RunContext) -> None:
        orgs = org_einheiten(ctx)
        ctx.tabellen.register("org_einheit", orgs, ersetzen=True)
        ma = mitarbeiter(ctx, orgs)
        ctx.tabellen.register("mitarbeiter", ma, ersetzen=True)
        ag, vm = agenturen_und_vermittler(ctx)
        ctx.tabellen.register("agentur", ag, ersetzen=True)
        ctx.tabellen.register("vermittler", vm, ersetzen=True)
        prod, gen = produkte_und_generationen(ctx)
        ctx.tabellen.register("produkt", prod, ersetzen=True)
        ctx.tabellen.register("tarifgeneration", gen, ersetzen=True)
        ctx.ereignis(self.name, f"{len(orgs)} Org-Einheiten, {len(ma)} Mitarbeitende, {len(ag)} Agenturen, "
                                f"{len(vm)} Vermittler, {len(prod)} Produkte, {len(gen)} Tarifgenerationen")


__all__ = ["OrganisationStage", "telefon"]
