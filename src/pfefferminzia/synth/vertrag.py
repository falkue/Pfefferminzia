"""Stufe ``vertrag``: Antraege, Underwriting, Vertraege, Deckungen, Risikoobjekte, Partnerrollen.

Vorgehen je Vertrag (Datenarchitektur 5.1, 5.4, 5.5): Versicherungsnehmer waehlen, Generation und
Beginn ziehen, Tarif rechnen, Lebenszyklus bis zum Stichtag simulieren (Storno, Ablauf, Tod), dann
die beobachtbaren Tabellen ableiten. Die latente Wahrheit (Kuendigungsgrund, Bias-Anwendung,
Tarifabweichung) landet in ``truth/vertrag_latent``.

Vertrags-IDs unter 2000 sind fuer die Kunden-Personas reserviert.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np
import pandas as pd

from pfefferminzia.context import RunContext
from pfefferminzia.ids import antrag_id, vertrag_id
from pfefferminzia.pipeline import Stage, register
from pfefferminzia.synth.referenz_intern import BERUFE, STORNO_GRUENDE, ZAHLUNGSWEISEN
from pfefferminzia.synth.tarif import TarifHP, TarifLV

PERSONA_VERTRAEGE_RESERVIERT = 2000
MIGRATION = {"HP": date(2025, 5, 15), "LV": date(2025, 11, 15)}
SPARTE = {"HP-PRIV": "HP", "HP-BETR": "HP", "HP-BERUF": "HP", "LV-RISK": "LV", "LV-VORS": "LV", "LV-RENTE": "LV", "LV-EU": "LV"}
KANALMIX = {  # (produkt, markt): agentur, makler, direkt, bank  (Kennzahlen-Masterdatei 2025)
    ("HP-PRIV", "CH"): (45, 10, 35, 10), ("HP-BETR", "CH"): (40, 55, 5, 0), ("HP-BERUF", "CH"): (25, 70, 5, 0),
    ("HP-PRIV", "DE"): (0, 30, 55, 15), ("HP-BETR", "DE"): (0, 75, 25, 0), ("HP-BERUF", "DE"): (0, 85, 15, 0),
    ("LV-RISK", "CH"): (50, 25, 5, 20), ("LV-VORS", "CH"): (55, 15, 0, 30), ("LV-RENTE", "CH"): (55, 15, 0, 30),
    ("LV-RISK", "DE"): (0, 50, 35, 15), ("LV-VORS", "DE"): (0, 60, 5, 35), ("LV-RENTE", "DE"): (0, 60, 5, 35),
}

# Persona-Vertraege (docs/personas/kunden): id, produkt, generation, vn, versicherte_person, markt, beginn, ablauf,
# praemie_brutto_jahr, summe, status, storno_datum, storno_grund, kanal, bemerkung
PERSONA_VERTRAEGE = [
    (101, "HP-PRIV", "HP-MODERN", 1, 1, "CH", "2016-03-01", None, 168.00, 5_000_000, "AKTIV", None, None, "agentur", "Familie, Hund"),
    (102, "LV-RISK", "PL-2017", 1, 1, "CH", "2019-05-01", "2044-05-01", 486.00, 300_000, "AKTIV", None, None, "agentur", ""),
    (103, "LV-RISK", "PL-2017", 11, 11, "CH", "2019-05-01", "2044-05-01", 612.00, 300_000, "AKTIV", None, None, "agentur", ""),
    (104, "LV-VORS", "PL-2017", 1, 1, "CH", "2020-01-01", "2049-03-14", 3_600.00, 120_000, "AKTIV", None, None, "agentur", "Saeule 3a"),
    (201, "HP-PRIV", "MZ-DIRECT", 2, 2, "DE", "2021-09-01", None, 63.60, 10_000_000, "AKTIV", None, None, "direkt", "Neuabschluss nach Widerruf"),
    (202, "LV-RISK", "PZ-2025", 2, 2, "DE", "2025-10-01", "2055-10-01", 175.20, 200_000, "AKTIV", None, None, "direkt", ""),
    (203, "HP-PRIV", "MZ-DIRECT", 2, 2, "DE", "2021-03-15", None, 58.80, 10_000_000, "STORNIERT", "2021-03-24", "K13", "direkt", "Widerruf innerhalb 14 Tagen"),
    (301, "HP-BETR", "HP-MODERN", 3, 3, "CH", "2016-01-01", None, 4_851.00, 5_000_000, "AKTIV", None, None, "makler", "Sanierung 2025"),
    (302, "LV-RISK", "PL-2017", 3, 12, "CH", "2019-07-01", "2033-07-01", 2_268.00, 900_000, "AKTIV", None, None, "makler", "Kollektiv Kader"),
    (401, "HP-BETR", "HP-MODERN", 4, 4, "DE", "2014-01-01", None, 6_331.42, 5_000_000, "AKTIV", None, None, "makler", "Nachtrag Photovoltaik 2025"),
    (402, "LV-RENTE", "PL-2017", 14, 14, "DE", "2018-03-01", "2042-03-01", 4_800.00, 120_000, "AKTIV", None, None, "makler", ""),
    (501, "LV-VORS", "PK-95", 5, 5, "CH", "1995-07-01", "2019-06-09", 4_236.00, 120_000, "ABGELAUFEN", "2019-06-09", "K15", "agentur", "Ablauf, Auszahlung 168420"),
    (502, "LV-RENTE", "PL-2017", 5, 5, "CH", "2019-09-01", None, 0.00, 150_000, "AKTIV", None, None, "agentur", "Einmalpraemie, Rentenbezug"),
    (503, "HP-PRIV", "HP-KLASSIK", 5, 5, "CH", "2001-01-01", None, 124.60, 5_000_000, "AKTIV", None, None, "agentur", "Altpraemie eingefroren; lautet auf beide Ehegatten"),
    (601, "LV-RENTE", "PL-2015", 6, 6, "DE", "2016-04-01", "2038-11-30", 12_000.00, 250_000, "AKTIV", None, None, "makler", ""),
    (602, "LV-RISK", "PZ-2025", 6, 6, "DE", "2025-07-01", "2043-07-01", 2_889.18, 1_200_000, "AKTIV", None, None, "makler", "Zuschlag 50 Prozent"),
    (701, "HP-PRIV", "HP-MODERN", 7, 7, "CH", "2024-09-01", None, 129.20, 5_000_000, "GEKUENDIGT_VN", "2025-12-31", "K01", "direkt", "Wechsel Anbieter"),
    (702, "LV-VORS", "PZ-2025", 7, 7, "CH", "2025-02-01", "2066-04-17", 1_800.00, 60_000, "AKTIV", None, None, "direkt", "Saeule 3a, Beitragspause 2025"),
    (801, "HP-PRIV", "HP-MODERN", 8, 8, "DE", "2013-01-01", None, 131.40, 5_000_000, "AKTIV", None, None, "agentur", "Hundebaustein seit 2019, Fall Pieper"),
    (901, "HP-BETR", "HP-MODERN", 9, 9, "DE", "2022-02-01", None, 2_140.00, 3_000_000, "GEKUENDIGT_VU", "2025-01-15", "K10", "direkt", "Betrugsfall"),
    (902, "HP-PRIV", "MZ-DIRECT", 17, 17, "DE", "2023-05-15", None, 63.60, 10_000_000, "GEKUENDIGT_VU", "2025-01-15", "K10", "direkt", "Betrugsfall, Dublette"),
    (1001, "LV-VORS", "PZ-2025", 10, 10, "CH", "2025-07-01", "2039-07-01", 0.00, 480_000, "AKTIV", None, None, "makler", "Einmalpraemie 450000, AML-Pruefung"),
]


@dataclass
class Kontext:
    ctx: RunContext
    partner: pd.DataFrame
    latent: pd.DataFrame
    adressen: pd.DataFrame
    firma: pd.DataFrame
    beziehungen: pd.DataFrame
    vermittler: pd.DataFrame
    mitarbeiter: pd.DataFrame
    generationen: pd.DataFrame
    hp: dict[str, pd.DataFrame]
    lv: dict[str, pd.DataFrame]
    tarif_hp: TarifHP
    tarif_lv: TarifLV


class VertragWelt:
    def __init__(self, ctx: RunContext):
        self.ctx = ctx
        t = ctx.tabellen
        self.k = Kontext(
            ctx, t.get("partner"), t.get("partner_latent", "truth").set_index("partner_id"), t.get("partner_adresse"),
            t.get("partner_firma").set_index("partner_id") if len(t.get("partner_firma")) else pd.DataFrame(), t.get("partner_beziehung"),
            t.get("vermittler"), t.get("mitarbeiter"), t.get("tarifgeneration"), ctx.reference.verzeichnis("hp"),
            ctx.reference.verzeichnis("lv"), TarifHP(ctx.reference), TarifLV(ctx.reference),
        )
        self.stichtag = ctx.config.zeit.stichtag
        self.p = self.k.partner.set_index("partner_id")
        akt = self.k.adressen[self.k.adressen["ist_aktuell"]].drop_duplicates("partner_id").set_index("partner_id")
        self.adr = akt
        self.raten = self._raten()
        self.uw = self.k.lv["underwriting_entscheidungen"]
        self.vertraege: list[dict] = []
        self.antraege: list[dict] = []
        self.deckungen: list[dict] = []
        self.risiko: list[dict] = []
        self.rollen: list[dict] = []
        self.latent: list[dict] = []
        self.vertrag_pro_partner: dict[str, int] = {}
        self.hh_mit_phv: set[str] = set()
        self.storno_gew = np.array([g[3] for g in STORNO_GRUENDE])
        self.vm_index = self._vermittler_index()
        self.sb_index = self._sachbearbeiter_index()
        self.zaehler_antrag = PERSONA_VERTRAEGE_RESERVIERT + 1

    # -- Hilfsindizes ------------------------------------------------------------
    def _raten(self) -> dict:
        out = {}
        for _, r in self.k.hp["lebenszyklus_raten"].iterrows():
            out[(r["produkt"], r["markt"], r["kanal"], r["herkunft"], int(r["jahr"]))] = (float(r["neugeschaeft_rate_pct"]), float(r["storno_rate_pct"]))
        for _, r in self.k.lv["lebenszyklus_raten"].iterrows():
            out[(r["produkt_code"], r["markt"], r["kanal"], r["herkunft"], int(r["jahr"]))] = (float(r["neugeschaeft_rate_pct"]), float(r["storno_rueckkauf_rate_pct"]))
        return out

    def storno_rate(self, produkt: str, markt: str, kanal: str, herkunft: str, jahr: int) -> float:
        jahr = min(max(jahr, 2016), 2025)
        h = "alle" if jahr < (2021 if produkt.startswith("HP") else 2020) else herkunft
        r = self.raten.get((produkt, markt, kanal, h, jahr)) or self.raten.get((produkt, markt, kanal, "pfefferminz", jahr)) \
            or self.raten.get((produkt, markt, "agentur", "alle", 2018)) or (10.0, 6.0)
        return r[1] / 100

    def _vermittler_index(self) -> dict[tuple[str, str], pd.DataFrame]:
        vm = self.k.vermittler
        return {(m, k): vm[(vm["markt"] == m) & (vm["kanal"] == k)] for m in ("CH", "DE") for k in ("agentur", "makler", "direkt", "bank")}

    def _sachbearbeiter_index(self) -> dict[tuple[str, str], pd.DataFrame]:
        ma = self.k.mitarbeiter
        out = {}
        for sparte in ("HP", "LV"):
            for markt in ("CH", "DE"):
                sel = ma[ma["org_kuerzel"].str.startswith("UW-" + ("HP" if sparte == "HP" else "LV")) & (ma["land"] == markt)]
                if sel.empty:
                    sel = ma[ma["org_kuerzel"].str.startswith("BV") | ma["org_kuerzel"].str.startswith("UW")]
                out[(sparte, markt)] = sel
        return out

    def vermittler(self, rng, markt: str, kanal: str) -> str | None:
        vm = self.vm_index.get((markt, kanal))
        if vm is None or vm.empty:
            vm = self.k.vermittler[self.k.vermittler["markt"] == markt]
        if vm.empty:
            return None
        g = vm["leistungsgewicht"].to_numpy(dtype=float)
        return str(vm.iloc[int(rng.choice(len(vm), p=g / g.sum()))]["vermittler_id"])

    def sachbearbeiter(self, rng, sparte: str, markt: str) -> str | None:
        sb = self.sb_index.get((sparte, markt))
        return None if sb is None or sb.empty else str(sb.iloc[int(rng.integers(0, len(sb)))]["mitarbeiter_id"])

    def kanal(self, rng, produkt: str, markt: str, herkunft: str) -> str:
        if herkunft == "minzia":
            return "direkt"
        w = np.array(KANALMIX[(produkt, markt)], dtype=float)
        if w.sum() == 0:
            return "makler"
        return str(rng.choice(["agentur", "makler", "direkt", "bank"], p=w / w.sum()))

    # -- Generation und Beginn ------------------------------------------------------
    def generation_und_beginn(self, rng, produkt: str, markt: str, herkunft: str, geburt: date | None,
                              tod: date | None = None) -> tuple[str, date]:
        g = self.k.generationen
        sparte = SPARTE[produkt]
        basis = g[(g["sparte"] == sparte) & g["produkte"].str.contains(produkt, regex=False) & g["maerkte"].str.contains(markt)]
        volljaehrig_ab = date(geburt.year + 18, geburt.month, min(geburt.day, 28)) if geburt is not None else None
        if volljaehrig_ab is not None:
            ende = basis["gueltig_bis"].map(lambda d: d if pd.notna(d) else self.stichtag)
            passend = basis[ende >= volljaehrig_ab]
            basis = passend if not passend.empty else basis
        if tod is not None:
            ende = basis["gueltig_ab"]
            passend = basis[ende <= tod - timedelta(days=400)]
            basis = passend if not passend.empty else basis
        if produkt == "HP-PRIV" and markt == "CH":
            basis = basis[basis["tarifgeneration_id"] != "MZ-DIRECT"]
        if herkunft == "minzia":
            kand = basis[basis["herkunft"] == "minzia"]
            if kand.empty:
                kand = basis[basis["herkunft"] == "pfefferminzia"]
        else:
            kand = basis[basis["herkunft"] != "minzia"]
        if kand.empty:
            kand = basis if not basis.empty else g[g["sparte"] == sparte]
        gew = kand["anteil_bestand_pct"].fillna(0).to_numpy(dtype=float) + 0.5
        gen = kand.iloc[int(rng.choice(len(kand), p=gew / gew.sum()))]
        von = gen["gueltig_ab"]
        bis = gen["gueltig_bis"] if pd.notna(gen["gueltig_bis"]) else self.stichtag
        bis = min(bis, self.stichtag)
        if tod is not None:
            bis = min(bis, tod - timedelta(days=365))
        if volljaehrig_ab is not None:
            von = max(von, volljaehrig_ab)
        if von > bis:
            bis = von + timedelta(days=1)
        tage = max((bis - von).days, 1)
        beginn = von + timedelta(days=int(rng.integers(0, tage)))
        beginn = beginn.replace(day=1)
        if volljaehrig_ab is not None and (beginn - geburt).days < 18 * 365.25 + 1:
            naechster = (beginn.replace(day=28) + timedelta(days=4)).replace(day=1)
            beginn = naechster if naechster <= self.stichtag else volljaehrig_ab + timedelta(days=1)
        return str(gen["tarifgeneration_id"]), beginn

    # -- Deckungssumme / Selbstbehalt -------------------------------------------------
    def _ziehe(self, rng, df: pd.DataFrame, gewicht: str = "anteil_bestand_pct"):
        g = df[gewicht].to_numpy(dtype=float)
        if len(df) == 0 or g.sum() <= 0:
            return None
        return df.iloc[int(rng.choice(len(df), p=g / g.sum()))]

    def deckungssumme(self, rng, produkt: str, markt: str, generation: str) -> float:
        d = self.k.hp["deckungssummen"]
        sel = d[(d["produkt"] == produkt) & (d["markt"] == markt) & (d["deckungsart"] == ("vermoegen" if produkt == "HP-BERUF" else "personen_sach"))
                & d["generationen"].str.contains(generation, regex=False)]
        z = self._ziehe(rng, sel)
        return float(z["betrag"]) if z is not None else (5_000_000.0 if produkt != "HP-BERUF" else 1_000_000.0)

    def selbstbehalt(self, rng, produkt: str, markt: str, generation: str) -> tuple[str, float]:
        d = self.k.hp["selbstbehalte"]
        sel = d[(d["produkt"] == produkt) & (d["markt"] == markt) & d["generationen"].str.contains(generation, regex=False)]
        z = self._ziehe(rng, sel)
        if z is None:
            return "fix", 0.0
        return str(z["selbstbehalt_typ"]), float(z["betrag"]) if pd.notna(z["betrag"]) else 0.0

    # -- Lebenszyklus -----------------------------------------------------------------
    def lebenszyklus(self, rng, produkt: str, markt: str, kanal: str, herkunft: str, beginn: date, ablauf: date | None,
                     vn: pd.Series, lat: pd.Series) -> tuple[str, date | None, str | None, bool]:
        """Liefert (status, ende, storno_grund, kuendigt_in_12m)."""
        tod = lat["todesdatum"] if pd.notna(lat["todesdatum"]) else None
        neigung = float(lat["kuendigungsneigung"])
        faktor = 0.5 + 1.6 * neigung
        jahr = beginn.year
        while True:
            ende_jahr = date(jahr, 12, 31)
            if tod is not None and tod <= ende_jahr and tod >= beginn:
                if produkt in ("LV-RISK", "LV-VORS"):
                    return "LEISTUNG_ERBRACHT", tod, "K16", False
                return "STORNIERT", tod + timedelta(days=int(rng.integers(10, 90))), "K07", False
            if ablauf is not None and ablauf <= self.stichtag and ablauf.year == jahr:
                return "ABGELAUFEN", ablauf, "K15", False
            if jahr >= self.stichtag.year:
                break
            if jahr > beginn.year:
                h = self.storno_rate(produkt, markt, kanal, herkunft, jahr) * faktor
                if produkt == "HP-PRIV" and (self.stichtag.year - vn["geburtsdatum"].year) < 30:
                    h *= 1.4
                if rng.random() < h:
                    ende = date(jahr, int(rng.integers(1, 13)), 1) if produkt.startswith("HP") else date(jahr, int(rng.integers(1, 13)), int(rng.integers(1, 28)))
                    ende = max(ende, beginn + timedelta(days=30))
                    if produkt.startswith("LV"):
                        grund = "K14" if rng.random() < 0.85 else "K12"
                        return ("RUECKKAUF" if grund == "K14" else "STORNIERT"), ende, grund, False
                    kand = [g for g in STORNO_GRUENDE if g[3] > 0]
                    gw = np.array([g[3] for g in kand])
                    g = kand[int(rng.choice(len(kand), p=gw / gw.sum()))]
                    return g[2], ende, g[0], False
            jahr += 1
        # aktiv am Stichtag: latente Kuendigung in den naechsten 12 Monaten
        h = self.storno_rate(produkt, markt, kanal, herkunft, 2025) * faktor
        return "AKTIV", None, None, bool(rng.random() < h)

    # -- Underwriting Leben -----------------------------------------------------------
    def underwriting_lv(self, rng, generation: str, markt: str, beginn: date, vn: pd.Series, lat: pd.Series, zone: str) -> dict:
        u = self.uw[(self.uw["generation_code"] == generation) & (self.uw["markt"] == markt)]
        codes = list(u["entscheid_code"]) or ["N", "Z", "A", "R", "X"]
        p = u["zielanteil_pct"].to_numpy(dtype=float) if len(u) else np.array([86, 8, 2, 2, 2], dtype=float)
        p = p / p.sum()
        bias = self.ctx.config.fallen.staerke("underwriting_bias")
        bias_angewendet = False
        # Historischer Bias (Annahmerichtlinien §6): Tarifzone 3, DE-Grossstadtzone 1 mit auslaendischer Nationalitaet, bis 2019
        if bias > 0 and beginn.year <= 2019 and generation not in ("MZ-2020", "PZ-2025"):
            if zone == "3" or (markt == "DE" and zone == "1" and vn["nationalitaet"] != "DE"):
                zi = codes.index("Z") if "Z" in codes else 1
                p = p.copy()
                p[zi] *= 1 + 1.5 * bias
                p = p / p.sum()
                bias_angewendet = True
        # Gesundheit: BMI und Raucher erhoehen Zuschlagswahrscheinlichkeit sachlich
        bmi = float(lat["bmi"]) if pd.notna(lat["bmi"]) else 24.0
        if bmi >= 30 or bool(lat["raucher"]):
            zi = codes.index("Z") if "Z" in codes else 1
            p = p.copy()
            p[zi] *= 1.8
            p = p / p.sum()
        code = str(rng.choice(codes, p=p))
        zuschlag = 0.0
        if code == "Z":
            zuschlag = float(rng.choice([25, 50, 75, 100], p=[0.45, 0.3, 0.15, 0.1]))
        auto_q = float(u[u["entscheid_code"] == code]["automatisierungsquote_pct"].iloc[0]) / 100 if len(u[u["entscheid_code"] == code]) else 0.0
        automatisiert = code == "N" and rng.random() < auto_q
        return {"entscheid_code": code, "zuschlag_pct": zuschlag, "automatisiert": automatisiert, "bias_angewendet": bias_angewendet,
                "bmi_angabe": round(bmi + float(rng.normal(0, 0.8)), 1), "raucher_angabe": bool(lat["raucher"]) if rng.random() > 0.06 else False}

    # -- Vertrag bauen ------------------------------------------------------------------
    def vertrag(self, n: int, produkt: str, vn_id: str, *, persona: dict | None = None) -> None:
        rng = self.ctx.rng("vertrag", n)
        vn = self.p.loc[vn_id]
        lat = self.k.latent.loc[vn_id]
        markt = str(vn["land_wohnsitz"])
        herkunft = str(vn["herkunft"])
        adr = self.adr.loc[vn_id] if vn_id in self.adr.index else None
        zone = str(adr["tarifzone"]) if adr is not None else ("2" if markt == "CH" else "3")
        sparte = SPARTE[produkt]
        geburt = vn["geburtsdatum"] if vn["partner_typ"] == "NATUERLICH" else None
        alter_beginn = None
        if persona:
            generation, beginn = persona["generation"], date.fromisoformat(persona["beginn"])
            kanal = persona["kanal"]
        else:
            kanal = self.kanal(rng, produkt, markt, herkunft)
            tod = lat["todesdatum"] if pd.notna(lat["todesdatum"]) else None
            generation, beginn = self.generation_und_beginn(rng, produkt, markt, herkunft, geburt, tod)
        if geburt is not None:
            alter_beginn = beginn.year - geburt.year - (1 if (beginn.month, beginn.day) < (geburt.month, geburt.day) else 0)
        waehrung = "CHF" if markt == "CH" else "EUR"
        zahlungsweise = str(rng.choice(ZAHLUNGSWEISEN, p=[0.65, 0.15, 0.15, 0.05] if herkunft == "minzia" or beginn.year >= 2020 else [0.72, 0.16, 0.12, 0.0]))
        zahlungsart = str(rng.choice(["RECHNUNG", "LASTSCHRIFT", "EBILL", "KREDITKARTE"],
                                     p=[0.55, 0.3, 0.13, 0.02] if herkunft != "minzia" else [0.1, 0.55, 0.15, 0.2]))
        # -- Sparte Haftpflicht
        deckungen: list[dict] = []
        risiko: dict = {}
        laufzeit, ablauf, summe = None, None, 0.0
        uw: dict = {"entscheid_code": "N", "zuschlag_pct": 0.0, "automatisiert": False, "bias_angewendet": False}
        if sparte == "HP":
            summe = self.deckungssumme(rng, produkt, markt, generation)
            sb_typ, sb = self.selbstbehalt(rng, produkt, markt, generation)
            bausteine = self._bausteine(rng, produkt, markt, generation, lat)
            if produkt == "HP-PRIV":
                hh = self.k.beziehungen[self.k.beziehungen["partner_id_zu"] == vn_id]
                personenkreis = "einzel" if len(hh) == 0 else ("paar" if (len(hh) == 1 and markt == "DE") else "familie")
                praemie = self.k.tarif_hp.praemie(produkt, markt, generation, deckungssumme=summe, selbstbehalt=sb, tarifzone=zone,
                                                  personenkreis=personenkreis, alter_vn=alter_beginn or 40, vorschaeden=int(rng.random() < 0.15),
                                                  kanal=kanal, mehrjahres=int(rng.choice([1, 3, 5], p=[0.5, 0.3, 0.2])) if markt == "CH" else 1,
                                                  bausteine=tuple(bausteine), buendel=bool(rng.random() < 0.2), papierlos=herkunft == "minzia")
                risiko = {"risiko_typ": "HAUSHALT", "personen": 1 + len(hh), "hund": "BS-TIER-HUND" in bausteine, "personenkreis": personenkreis}
            elif produkt == "HP-BETR":
                f = self.k.firma.loc[vn_id] if vn_id in self.k.firma.index else None
                rk = int(f["risikoklasse"]) if f is not None else 2
                umsatz = float(f["umsatz"]) if f is not None else 800000.0
                ma = int(f["mitarbeitende"]) if f is not None else 5
                bemessung = umsatz * (0.42 if markt == "CH" else 1.0)  # CH: Lohnsumme ~ 42 % des Umsatzes
                praemie = self.k.tarif_hp.praemie(produkt, markt, generation, deckungssumme=summe, selbstbehalt=sb, tarifzone=zone,
                                                  risikoklasse=rk, bemessung=bemessung, mitarbeitende=ma, bausteine=tuple(bausteine),
                                                  vorschaeden=int(rng.choice([0, 1, 2], p=[0.7, 0.22, 0.08])))
                if rk >= 4:
                    uw = {**uw, "entscheid_code": "Z" if rng.random() < 0.5 else "N", "zuschlag_pct": 10.0}
                risiko = {"risiko_typ": "BETRIEB", "branche_id": f["branche_id"] if f is not None else None, "nace_code": f["nace_code"] if f is not None else None,
                          "risikoklasse": rk, "umsatz": umsatz, "mitarbeitende": ma, "bemessungsgrundlage": bemessung}
            else:  # HP-BERUF
                bg = str(rng.choice(["BG-ARCH", "BG-TREU", "BG-IT", "BG-BER"], p=[0.36, 0.28, 0.22, 0.14]))
                ug = {"BG-ARCH": "architekt", "BG-TREU": "treuhaender", "BG-IT": "it_dienstleister", "BG-BER": "unternehmensberater"}[bg]
                if bg == "BG-TREU" and markt == "DE":
                    ug = "steuerberater_de"
                honorar = float(round(rng.lognormal(12.8, 0.6), -3))
                praemie = self.k.tarif_hp.praemie(produkt, markt, generation, deckungssumme=summe, selbstbehalt=sb, tarifzone=zone,
                                                  berufsgruppe=bg, untergruppe=ug, bemessung=honorar,
                                                  taetigkeit="bauleitung" if (bg == "BG-ARCH" and rng.random() < 0.4) else None,
                                                  vorschaeden=int(rng.choice([0, 1, 2], p=[0.75, 0.2, 0.05])))
                risiko = {"risiko_typ": "BERUF", "berufsgruppe": bg, "untergruppe": ug, "bemessungsgrundlage": honorar}
            netto, brutto = praemie.netto, praemie.brutto
            deckungen.append({"deckungsart": "HAUPTDECKUNG", "baustein": None, "summe": summe, "selbstbehalt": sb, "selbstbehalt_typ": sb_typ})
            deckungen += [{"deckungsart": "BAUSTEIN", "baustein": b, "summe": None, "selbstbehalt": None, "selbstbehalt_typ": None} for b in bausteine]
            hauptfaelligkeit = beginn
        # -- Sparte Leben
        else:
            vsummen = self.k.lv["versicherungssummen"]
            lz = self.k.lv["laufzeiten"]
            sel_s = vsummen[(vsummen["produkt_code"] == produkt) & (vsummen["markt"] == markt)]
            zs = self._ziehe(rng, sel_s, "bestandsanteil_pct")
            summe = float(round(rng.uniform(float(zs["klasse_von"]), float(zs["klasse_bis"])), -3)) if zs is not None else 100000.0
            sel_l = lz[(lz["produkt_code"] == produkt) & (lz["markt"] == markt)]
            zl = self._ziehe(rng, sel_l, "bestandsanteil_pct")
            laufzeit = int(rng.integers(int(zl["klasse_von_jahre"]), int(zl["klasse_bis_jahre"]) + 1)) if zl is not None else 20
            if alter_beginn is not None:
                endalter = int(zl["endalter_max"]) if zl is not None else 70
                laufzeit = max(5, min(laufzeit, endalter - alter_beginn))
            ablauf = date(beginn.year + laufzeit, beginn.month, beginn.day)
            uw = self.underwriting_lv(rng, generation, markt, beginn, vn, lat, zone)
            eu = produkt in ("LV-RISK", "LV-VORS") and rng.random() < 0.25
            eu_rente = float(rng.choice([1000, 1500, 2000, 2500, 3000])) * 12 if eu else 0.0
            beruf = next((b for b in BERUFE if b[0] == vn["beruf_code"]), BERUFE[0])
            praemie = self.k.tarif_lv.praemie(produkt, markt, generation, summe=summe, alter=alter_beginn or 35, laufzeit=laufzeit,
                                              geschlecht=str(vn["geschlecht"]), raucher=bool(uw.get("raucher_angabe", False)),
                                              abschluss=pd.Timestamp(beginn), zuschlag_pct=uw["zuschlag_pct"], zahlweise=zahlungsweise,
                                              summenverlauf=str(rng.choice(["KONSTANT", "LINEAR_FALLEND", "ANNUITAET"], p=[0.6, 0.15, 0.25])) if produkt == "LV-RISK" else "KONSTANT")
            netto, brutto = praemie.netto, praemie.brutto
            if eu:
                pe = self.k.tarif_lv.praemie("LV-EU", markt, generation, summe=0, alter=alter_beginn or 35, laufzeit=laufzeit, geschlecht=str(vn["geschlecht"]),
                                             raucher=False, abschluss=pd.Timestamp(beginn), eu_rente_jahr=eu_rente, berufsgruppe=beruf[2])
                netto, brutto = round(netto + pe.netto, 2), round(brutto + pe.brutto, 2)
                deckungen.append({"deckungsart": "ZUSATZ", "baustein": "LV-EU", "summe": eu_rente / 12, "selbstbehalt": None, "selbstbehalt_typ": None})
            deckungen.insert(0, {"deckungsart": "HAUPTDECKUNG", "baustein": None, "summe": summe, "selbstbehalt": None, "selbstbehalt_typ": None})
            risiko = {"risiko_typ": "VERSICHERTE_PERSON", "versicherte_person_id": vn_id, "eintrittsalter": alter_beginn,
                      "raucher_angabe": uw.get("raucher_angabe"), "bmi_angabe": uw.get("bmi_angabe"), "summenverlauf": praemie.faktoren.get("summenverlauf")}
            hauptfaelligkeit = beginn
            if uw["entscheid_code"] in ("X", "A") and not persona:
                # Ablehnung / Ausschluss: kein Vertrag, nur Antrag
                self._antrag(rng, n, produkt, vn_id, markt, generation, beginn, uw, kanal, sparte, vertrag=None)
                return
        einmalpraemie = None
        if produkt == "LV-RENTE" and markt == "CH":
            einmalpraemie = float(round(summe, -3))
            netto, brutto = 0.0, 0.0
            zahlungsweise = "EINMALIG"
        if persona and persona["praemie"] == 0.0 and produkt in ("LV-RENTE", "LV-VORS"):
            einmalpraemie = 150_000.0 if persona["vp"] == "PTR-00000005" else 450_000.0
            zahlungsweise = "EINMALIG"
        # -- Tarifabweichung (Falle)
        abweichung = 0.0
        if self.ctx.config.fallen.aktiv("tarifabweichung") and rng.random() < self.ctx.config.fallen.staerke("tarifabweichung"):
            abweichung = float(rng.choice([-0.12, -0.08, -0.05, 0.05, 0.09]))
        if generation in ("HP-KLASSIK", "PK-85", "PK-95") and rng.random() < 0.4:
            abweichung = float(rng.uniform(-0.2, -0.05))  # eingefrorene Altpraemien
        if persona:
            brutto_beob = float(persona["praemie"])
            netto_beob = round(brutto_beob / (1 + (0.05 if markt == "CH" else 0.19)), 2) if sparte == "HP" else brutto_beob
            abweichung = round(brutto_beob / brutto - 1, 4) if brutto else 0.0
            if einmalpraemie is not None:
                brutto_beob = netto_beob = 0.0
                abweichung = 0.0
        else:
            brutto_beob = round(brutto * (1 + abweichung), 2)
            netto_beob = round(netto * (1 + abweichung), 2)
        # -- Lebenszyklus
        if persona:
            status, ende, grund, k12 = persona["status"], (date.fromisoformat(persona["storno"]) if persona["storno"] else None), persona["grund"], False
        else:
            status, ende, grund, k12 = self.lebenszyklus(rng, produkt, markt, kanal, herkunft, beginn, ablauf, vn, lat)
        # -- Quellsystem
        if herkunft == "minzia":
            quelle, migriert = "MINT", None
        elif beginn >= date(2025, 1, 1):
            quelle, migriert = "MINT", None
        else:
            quelle = "HAPO" if sparte == "HP" else "VERA"
            migriert = MIGRATION[sparte] if (ende is None or ende >= date(2025, 1, 1)) else None
            if ende is not None and ende < date(2025, 1, 1):
                migriert = MIGRATION[sparte]  # Altbestand wurde vollstaendig migriert, auch beendete Vertraege
        vid = vertrag_id(n)
        vermittler = self.vermittler(rng, markt, kanal)
        sachbearbeiter = self.sachbearbeiter(rng, sparte, markt)
        antrag = self._antrag(rng, n, produkt, vn_id, markt, generation, beginn, uw, kanal, sparte, vertrag=vid)
        naechste_kuendigung = None
        if status == "AKTIV" and sparte == "HP":
            hf = date(2026, beginn.month, 1)
            naechste_kuendigung = hf if markt == "DE" else date(2026 + (0 if beginn.year % 3 else 0), beginn.month, 1)
        self.vertraege.append({
            "vertrag_id": vid, "policennummer_anzeige": None, "produkt_id": produkt, "sparte": sparte, "tarifgeneration_id": generation,
            "markt": markt, "waehrung": waehrung, "versicherungsnehmer_id": vn_id, "vermittler_id": vermittler, "kanal": kanal,
            "sachbearbeiter_id": sachbearbeiter, "antrag_id": antrag, "beginn": beginn, "ablauf": ablauf, "laufzeit_jahre": laufzeit,
            "hauptfaelligkeit": hauptfaelligkeit, "zahlungsweise": zahlungsweise, "zahlungsart": zahlungsart,
            "jahrespraemie_netto": netto_beob, "jahrespraemie_brutto": brutto_beob, "einmalpraemie": einmalpraemie, "versicherungssumme": summe,
            "status": status, "status_seit": ende or beginn, "storno_datum": ende if status not in ("AKTIV",) else None,
            "storno_grund_code": grund, "kuendigungsfrist_monate": 3 if sparte == "HP" else None, "naechste_kuendigungsmoeglichkeit": naechste_kuendigung,
            "risikoklasse_uw": {"N": "NORMAL", "Z": "ZUSCHLAG_1" if uw["zuschlag_pct"] <= 50 else "ZUSCHLAG_2", "A": "AUSSCHLUSS"}.get(uw["entscheid_code"], "NORMAL"),
            "mahnstufe_aktuell": 0, "herkunft": herkunft, "quellsystem": quelle, "migriert_am": migriert,
            "erstellt_am": beginn - timedelta(days=int(rng.integers(1, 40))), "bemerkung": persona["bemerkung"] if persona else None,
        })
        for i, d in enumerate(deckungen):
            self.deckungen.append({"deckung_id": f"DEK-{n:08d}-{i + 1:02d}", "vertrag_id": vid, **d, "gueltig_von": beginn, "gueltig_bis": ende})
        self.risiko.append({"risiko_objekt_id": f"RIS-{n:08d}", "vertrag_id": vid, **{k: risiko.get(k) for k in
                            ("risiko_typ", "personen", "hund", "personenkreis", "branche_id", "nace_code", "risikoklasse", "umsatz", "mitarbeitende",
                             "bemessungsgrundlage", "berufsgruppe", "untergruppe", "versicherte_person_id", "eintrittsalter", "raucher_angabe", "bmi_angabe",
                             "summenverlauf")}})
        self._rollen(rng, vid, vn_id, produkt, persona)
        self.latent.append({
            "vertrag_id": vid, "praemie_tarif_brutto": brutto, "tarifabweichung_pct": round(abweichung * 100, 2),
            "kuendigt_in_12m": k12, "kuendigungsgrund_latent": grund or (self._latenter_grund(rng) if k12 else None),
            "uw_entscheid": uw["entscheid_code"], "uw_zuschlag_pct": uw["zuschlag_pct"], "uw_bias_angewendet": uw["bias_angewendet"],
            "uw_automatisiert": uw["automatisiert"], "bmi_wahr": float(lat["bmi"]) if pd.notna(lat["bmi"]) else None,
            "raucher_wahr": bool(lat["raucher"]) if pd.notna(lat["raucher"]) else None,
        })
        self.vertrag_pro_partner[vn_id] = self.vertrag_pro_partner.get(vn_id, 0) + 1

    def _latenter_grund(self, rng) -> str:
        kand = [g for g in STORNO_GRUENDE if g[3] > 0]
        gw = np.array([g[3] for g in kand])
        return kand[int(rng.choice(len(kand), p=gw / gw.sum()))][0]

    def _bausteine(self, rng, produkt: str, markt: str, generation: str, lat: pd.Series) -> list[str]:
        b = self.k.hp["bausteine"]
        sel = b[b["produkte"].str.contains(produkt, regex=False) & b["maerkte"].str.contains(markt)]
        out = []
        for _, z in sel.iterrows():
            ab = z["ab_generation_ch" if markt == "CH" else "ab_generation_de"]
            if pd.isna(ab) or ab == "":
                continue
            gens = ["HP-KLASSIK", "HP-MODERN", "MZ-DIRECT", "PM-2025"]
            if gens.index(generation) < gens.index(ab) if ab in gens else False:
                continue
            anteil = float(z["anteil_vertraege_ch_pct" if markt == "CH" else "anteil_vertraege_de_pct"] or 0) / 100
            if z["kuerzel"] == "BS-TIER-HUND":
                if bool(lat.get("hund", False)) and produkt == "HP-PRIV":
                    out.append(z["kuerzel"])
                continue
            if rng.random() < anteil:
                out.append(str(z["kuerzel"]))
        return out

    def _antrag(self, rng, n: int, produkt: str, vn_id: str, markt: str, generation: str, beginn: date, uw: dict, kanal: str, sparte: str,
                vertrag: str | None) -> str:
        aid = antrag_id(n)
        eingang = beginn - timedelta(days=int(rng.integers(3, 75)))
        entscheid = eingang + timedelta(days=int(rng.integers(0, max((beginn - eingang).days, 1))))
        status = {"N": "ANGENOMMEN", "Z": "ANGENOMMEN_ZUSCHLAG", "A": "ANGENOMMEN_ZUSCHLAG", "R": "RUECKFRAGE", "X": "ABGELEHNT"}.get(uw["entscheid_code"], "ANGENOMMEN")
        if vertrag is None and status not in ("ABGELEHNT",):
            status = "ABGELEHNT" if uw["entscheid_code"] in ("X",) else "ZURUECKGEZOGEN"
        self.antraege.append({
            "antrag_id": aid, "vertrag_id": vertrag, "produkt_id": produkt, "antragsteller_id": vn_id, "markt": markt, "tarifgeneration_id": generation,
            "kanal": kanal, "eingang": eingang, "entscheid_am": entscheid, "gewuenschter_beginn": beginn, "status": status,
            "uw_entscheid_code": uw["entscheid_code"], "uw_zuschlag_pct": uw["zuschlag_pct"], "uw_automatisiert": uw["automatisiert"],
            "bmi_angabe": uw.get("bmi_angabe"), "raucher_angabe": uw.get("raucher_angabe"), "sparte": sparte,
        })
        return aid

    def _rollen(self, rng, vid: str, vn_id: str, produkt: str, persona: dict | None) -> None:
        self.rollen.append({"vertrag_id": vid, "partner_id": vn_id, "rolle": "VERSICHERUNGSNEHMER", "anteil_pct": None})
        bez = self.k.beziehungen[self.k.beziehungen["partner_id_zu"] == vn_id]
        if produkt == "HP-PRIV":
            for _, b in bez.iterrows():
                if b["beziehung"] in ("EHEPARTNER", "KIND"):
                    self.rollen.append({"vertrag_id": vid, "partner_id": b["partner_id_von"], "rolle": "MITVERSICHERT", "anteil_pct": None})
        elif produkt.startswith("LV"):
            vp = persona["vp"] if persona else vn_id
            self.rollen.append({"vertrag_id": vid, "partner_id": vp, "rolle": "VERSICHERTE_PERSON", "anteil_pct": None})
            eh = bez[bez["beziehung"] == "EHEPARTNER"]
            kinder = bez[bez["beziehung"] == "KIND"]
            if len(eh):
                self.rollen.append({"vertrag_id": vid, "partner_id": eh.iloc[0]["partner_id_von"], "rolle": "BEGUENSTIGT", "anteil_pct": 100.0 if not len(kinder) else 50.0})
                for _, kk in kinder.iterrows():
                    self.rollen.append({"vertrag_id": vid, "partner_id": kk["partner_id_von"], "rolle": "BEGUENSTIGT", "anteil_pct": round(50.0 / len(kinder), 2)})
            elif len(kinder):
                for _, kk in kinder.iterrows():
                    self.rollen.append({"vertrag_id": vid, "partner_id": kk["partner_id_von"], "rolle": "BEGUENSTIGT", "anteil_pct": round(100.0 / len(kinder), 2)})
            else:
                self.rollen.append({"vertrag_id": vid, "partner_id": None, "rolle": "BEGUENSTIGT_GESETZLICHE_ERBEN", "anteil_pct": 100.0})

    # -- Steuerung ------------------------------------------------------------------------
    def erzeugen(self) -> None:
        for (vid, produkt, gen, vn, vp, _markt, beginn, ablauf, praemie, summe, status, storno, grund, kanal, bem) in PERSONA_VERTRAEGE:
            vn_id = f"PTR-{vn:08d}"
            if vn_id not in self.p.index:
                continue
            self.vertrag(vid, produkt, vn_id, persona={"generation": gen, "beginn": beginn, "kanal": kanal, "praemie": praemie, "status": status,
                                                       "storno": storno, "grund": grund, "bemerkung": bem, "vp": f"PTR-{vp:08d}", "summe": summe, "ablauf": ablauf})
        p = self.p
        nat = p[(p["partner_typ"] == "NATUERLICH") & (~p["ist_persona"])]
        volljaehrig = nat[nat["geburtsdatum"].map(lambda d: (self.stichtag - d).days >= 18 * 365.25 + 32)]
        haushaltskopf = volljaehrig[~volljaehrig.index.isin(self.k.beziehungen["partner_id_von"])]
        jur = p[(p["partner_typ"] == "JURISTISCH") & (~p["ist_persona"])]
        mengen = {"HP-PRIV": self.ctx.menge("vertraege_hp_privat"), "HP-BETR": int(self.ctx.menge("vertraege_hp_betrieb") * 0.88),
                  "HP-BERUF": self.ctx.menge("vertraege_hp_betrieb") - int(self.ctx.menge("vertraege_hp_betrieb") * 0.88),
                  "LV-RISK": self.ctx.menge("vertraege_lv_risiko"), "LV-VORS": self.ctx.menge("vertraege_lv_kapital"), "LV-RENTE": self.ctx.menge("vertraege_lv_rente")}
        n = PERSONA_VERTRAEGE_RESERVIERT + 1
        for produkt, anzahl in mengen.items():
            pool = jur if produkt in ("HP-BETR", "HP-BERUF") else (haushaltskopf if produkt == "HP-PRIV" else volljaehrig)
            if produkt == "HP-BERUF":
                # Freiberufler: juristische Personen mit Beratungs-/Planungsbranchen oder selbstaendige natuerliche Personen
                pool = pd.concat([jur, volljaehrig[volljaehrig["beruf_code"].isin(["B10", "B12", "B13", "B14", "B21", "B02"])]])
            if produkt in ("LV-VORS", "LV-RENTE"):
                pool = volljaehrig[volljaehrig["herkunft"] == "pfefferminz"]
            if produkt == "LV-RENTE":
                pool = pool[pool["geburtsdatum"].map(lambda d: d.year) <= self.stichtag.year - 30]
            ids = list(pool.index)
            if not ids:
                continue
            rng = self.ctx.rng("vertrag.zuweisung", produkt)
            gewichte = np.ones(len(ids))
            if produkt == "HP-PRIV":
                gewichte = np.array([0.15 if h in self.hh_mit_phv else 1.0 for h in pool["haushalt_id"]])
            for _ in range(anzahl):
                idx = int(rng.choice(len(ids), p=gewichte / gewichte.sum()))
                vn_id = ids[idx]
                if produkt == "HP-PRIV":
                    gewichte[idx] *= 0.05  # ein Haushalt hat selten zwei Privathaftpflichten
                elif produkt.startswith("HP"):
                    gewichte[idx] *= 0.3
                else:
                    gewichte[idx] *= 0.5
                self.vertrag(n, produkt, vn_id)
                n += 1
        # Zusaetzliche Antraege ohne Vertrag (zurueckgezogen), ca. 6 % der Vertraege
        extra = int(len(self.vertraege) * 0.06)
        rng = self.ctx.rng("antrag.extra", 0)
        kand = list(volljaehrig.index)
        for _ in range(extra):
            vn_id = kand[int(rng.integers(0, len(kand)))]
            produkt = str(rng.choice(["HP-PRIV", "LV-RISK", "LV-VORS"], p=[0.5, 0.35, 0.15]))
            vn = self.p.loc[vn_id]
            gen, beginn = self.generation_und_beginn(rng, produkt, str(vn["land_wohnsitz"]), str(vn["herkunft"]), vn["geburtsdatum"])
            if beginn > self.stichtag:
                continue
            uw = {"entscheid_code": "N", "zuschlag_pct": 0.0, "automatisiert": False, "bias_angewendet": False}
            self._antrag(rng, n, produkt, vn_id, str(vn["land_wohnsitz"]), gen, beginn, uw, self.kanal(rng, produkt, str(vn["land_wohnsitz"]), str(vn["herkunft"])), SPARTE[produkt], vertrag=None)
            n += 1

    def tabellen(self) -> dict[str, pd.DataFrame]:
        v = pd.DataFrame(self.vertraege)
        return {"vertrag": v, "antrag": pd.DataFrame(self.antraege), "deckung": pd.DataFrame(self.deckungen),
                "risiko_objekt": pd.DataFrame(self.risiko), "vertrag_partner_rolle": pd.DataFrame(self.rollen),
                "vertrag_latent": pd.DataFrame(self.latent)}

    def partner_nachfuehren(self, vertrag: pd.DataFrame) -> pd.DataFrame:
        p = self.k.partner.copy()
        erst = vertrag.groupby("versicherungsnehmer_id")["beginn"].min()
        aktiv = vertrag[vertrag["status"] == "AKTIV"].groupby("versicherungsnehmer_id").size()
        kurs = 0.94
        vol = vertrag[vertrag["status"] == "AKTIV"].assign(chf=lambda d: d["jahrespraemie_brutto"] * np.where(d["waehrung"] == "EUR", kurs, 1.0)).groupby("versicherungsnehmer_id")["chf"].sum()
        quelle = vertrag.sort_values("beginn").groupby("versicherungsnehmer_id")["quellsystem"].first()
        p["kunde_seit"] = p["partner_id"].map(erst)
        p["quellsystem_primaer"] = p["partner_id"].map(quelle)
        p["quellsystem_primaer"] = p["quellsystem_primaer"].fillna(p["herkunft"].map({"minzia": "MINT", "pfefferminz": "HAPO"}))
        hat_aktiv = p["partner_id"].isin(aktiv.index)
        p.loc[(~hat_aktiv) & (p["status"] == "AKTIV") & p["partner_id"].isin(erst.index), "status"] = "INAKTIV"
        prem = p["partner_id"].map(vol).fillna(0) >= 5000
        p.loc[prem & (p["partner_typ"] == "NATUERLICH"), "kundensegment"] = "PREMIUM"
        p.loc[p["partner_id"].map(vol).fillna(0).ge(20000) & (p["partner_typ"] == "JURISTISCH"), "kundensegment"] = "GEWERBE"
        p["erstellt_am"] = pd.to_datetime(p["kunde_seit"].fillna(self.stichtag)).map(lambda d: d.to_pydatetime().replace(hour=9))
        p["geaendert_am"] = p["erstellt_am"]
        return p


@register
class VertragStage(Stage):
    name, nummer, welle = "vertrag", 40, 1
    beschreibung = "Antraege, Underwriting, Vertraege, Deckungen, Risikoobjekte, Partnerrollen"

    def run(self, ctx: RunContext) -> None:
        welt = VertragWelt(ctx)
        welt.erzeugen()
        t = welt.tabellen()
        for name, df in t.items():
            ctx.tabellen.register(name, df, layer="truth" if name.endswith("_latent") else "curated", ersetzen=True)
        ctx.tabellen.register("partner", welt.partner_nachfuehren(t["vertrag"]), ersetzen=True)
        v = t["vertrag"]
        ctx.ereignis(self.name, f"{len(v)} Vertraege ({int((v['status'] == 'AKTIV').sum())} aktiv), {len(t['antrag'])} Antraege, "
                                f"{len(t['deckung'])} Deckungen, {len(t['vertrag_partner_rolle'])} Rollen")
