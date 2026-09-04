"""Tarifierung Haftpflicht und Leben nach ``data/reference/hp/tarifparameter.yaml`` und
``data/reference/lv/tarifparameter.yaml`` (Formeln in den jeweiligen ``tarifformel.md``).

Die Funktionen liefern die Jahresnettoprämie (vor Steuer) sowie die Bruttoprämie und sind so
gehalten, dass Seminarteilnehmer die Werte in Excel nachrechnen können.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import pandas as pd

from pfefferminzia.reference import ReferenceLoader


def _stufe(tabelle: dict, wert: float) -> float:
    """Waehlt aus einem Mapping ``{schwelle: faktor}`` den Faktor der groessten Schwelle <= wert."""
    schluessel = sorted(int(k) for k in tabelle)
    gewaehlt = schluessel[0]
    for s in schluessel:
        if wert >= s:
            gewaehlt = s
    return float(tabelle[gewaehlt] if gewaehlt in tabelle else tabelle[str(gewaehlt)])


def _runden(betrag: float, markt: str) -> float:
    return round(round(betrag / 0.05) * 0.05, 2) if markt == "CH" else round(betrag, 2)


@dataclass
class Praemie:
    netto: float
    steuer: float
    brutto: float
    faktoren: dict


class TarifHP:
    def __init__(self, ref: ReferenceLoader):
        self.p = ref.yaml("hp/tarifparameter.yaml")
        self.bausteine = ref.csv("hp/bausteine.csv")

    def praemie(self, produkt: str, markt: str, generation: str, *, deckungssumme: float, selbstbehalt: float,
                tarifzone: str, personenkreis: str = "einzel", alter_vn: int = 40, vorschaeden: int = 0,
                kanal: str = "agentur", mehrjahres: int = 1, bausteine: tuple[str, ...] = (), risikoklasse: int = 2,
                bemessung: float = 0.0, mitarbeitende: int = 1, berufsgruppe: str = "BG-ARCH", untergruppe: str = "architekt",
                taetigkeit: str | None = None, buendel: bool = False, papierlos: bool = False) -> Praemie:
        meta, gen_f = self.p["meta"], float(self.p["generationsfaktor"][generation])
        prod = self.p[produkt]
        f: dict[str, float] = {"generation": gen_f}
        if produkt == "HP-PRIV":
            basis = float(prod["grundpraemie"][markt][personenkreis])
            f["deckungssumme"] = _stufe(prod["deckungssumme"][markt], deckungssumme)
            f["selbstbehalt"] = _stufe(prod["selbstbehalt"][markt], selbstbehalt)
            f["tarifzone"] = float(prod["tarifzone"][markt][str(tarifzone)])
            f["alter"] = float(prod["alter_vn"]["bis_25"] if alter_vn <= 25 else prod["alter_vn"]["ab_61"] if alter_vn >= 61 else prod["alter_vn"]["26_bis_60"])
            f["vorschaeden"] = float(prod["vorschaeden_5_jahre"][min(vorschaeden, 3)])
            netto = basis * math.prod(f.values())
            zusatz = 0.0
            for b in bausteine:
                z = self.bausteine[self.bausteine["kuerzel"] == b]
                if len(z):
                    wert = z.iloc[0]["zusatzpraemie_ch" if markt == "CH" else "zusatzpraemie_de"]
                    zusatz += float(wert) if pd.notna(wert) and str(z.iloc[0]["zusatzpraemie_typ"]).startswith("fix") else 0.0
            netto += zusatz
            r = prod["rabatte"]
            rab = (float(r["buendel_mit_leben"]) if buendel else 1.0) * float(r["kanal"][kanal]) * (float(r["papierlos"]) if papierlos else 1.0)
            if markt == "CH":
                rab *= float(r["mehrjahresvertrag_ch"][max(k for k in (1, 3, 5) if k <= mehrjahres)])
            netto *= rab
            f["rabatte"] = rab
        elif produkt == "HP-BETR":
            satz = float(prod["praemiensatz_promille"]["CH_lohnsumme" if markt == "CH" else "DE_umsatz"][risikoklasse])
            basis = bemessung * satz / 1000
            if markt == "DE" and risikoklasse >= 3 and bemessung < 300000:
                basis = mitarbeitende * float(prod["pro_kopf_de_handwerk"][risikoklasse])
            f["deckungssumme"] = _stufe(prod["deckungssumme"][markt], deckungssumme)
            f["selbstbehalt"] = _stufe(prod["selbstbehalt"][markt], selbstbehalt)
            f["tarifzone"] = float(prod["tarifzone"][markt][str(tarifzone)])
            ms = prod["mitarbeiterstaffel"]
            f["mitarbeiter"] = float(ms["bis_5"] if mitarbeitende <= 5 else ms["6_bis_20"] if mitarbeitende <= 20 else ms["21_bis_50"])
            for b in bausteine:
                if b in prod["bausteine_pct"]:
                    f[f"baustein_{b}"] = 1 + float(prod["bausteine_pct"][b]) / 100
            f["vorschaeden"] = 1 + float(prod["zuschlaege_pct"]["schadenquote_3_jahre"]["40_bis_80" if vorschaeden == 1 else "ueber_80" if vorschaeden >= 2 else "unter_40"]) / 100
            netto = basis * math.prod(f.values())
        else:  # HP-BERUF
            satz = float(prod["praemiensatz_promille"][berufsgruppe][untergruppe])
            basis = bemessung * satz / 1000
            f["deckungssumme"] = _stufe(prod["deckungssumme"][markt], deckungssumme)
            f["selbstbehalt"] = float(prod["selbstbehalt"]["prozent_min"])
            f["taetigkeit"] = float(prod["taetigkeitsfaktor"].get(taetigkeit, 1.0)) if taetigkeit else 1.0
            f["vorschaeden"] = float(prod["vorschaeden_5_jahre"][min(vorschaeden, 3)])
            f["tarifzone"] = float(prod["tarifzone"][markt][str(tarifzone)])
            netto = basis * math.prod(f.values())
        netto = max(netto, float(meta["mindestpraemie"][produkt][markt]))
        netto = _runden(netto, markt)
        steuer = round(netto * float(meta["steuer"][markt]["satz"]), 2)
        return Praemie(netto, steuer, round(netto + steuer, 2), f)


class TarifLV:
    def __init__(self, ref: ReferenceLoader):
        self.p = ref.yaml("lv/tarifparameter.yaml")
        self.tafeln = ref.csv("lv/sterbetafel.csv")
        gen = ref.csv("lv/tarifgenerationen.csv")
        self.gen = gen.set_index("generation_code")
        self.ueb = ref.csv("lv/ueberschuss_parameter.csv")
        self._qx: dict[tuple[str, int, str], float] = {}

    def qx(self, tafel: str, alter: int, spalte: str) -> float:
        alter = int(min(max(alter, 18), 85))
        key = (tafel, alter, spalte)
        if key not in self._qx:
            t = self.tafeln[(self.tafeln["tafel"] == tafel) & (self.tafeln["alter"] == alter)]
            self._qx[key] = float(t.iloc[0][spalte])
        return self._qx[key]

    def rechnungszins(self, generation: str, markt: str, abschlussjahr: int) -> float:
        g = self.gen.loc[generation]
        if markt == "CH":
            return float(g["technischer_zins_ch_pct"]) / 100
        if abschlussjahr >= 2022 and pd.notna(g["rechnungszins_de_ab_2022_pct"]) and str(g["rechnungszins_de_ab_2022_pct"]) != "":
            return float(g["rechnungszins_de_ab_2022_pct"]) / 100
        return float(g["rechnungszins_de_pct"]) / 100

    def unisex(self, generation: str, markt: str, abschluss: pd.Timestamp | None) -> bool:
        if generation == "MZ-2020":
            return True
        if markt == "CH":
            return False
        return abschluss is None or abschluss >= pd.Timestamp("2012-12-21")

    def praemie(self, produkt: str, markt: str, generation: str, *, summe: float, alter: int, laufzeit: int, geschlecht: str,
                raucher: bool, abschluss: pd.Timestamp, zuschlag_pct: float = 0.0, summenverlauf: str = "KONSTANT",
                zahlweise: str = "JAEHRLICH", eu_rente_jahr: float = 0.0, berufsgruppe: int = 2) -> Praemie:
        p, kosten = self.p, self.p["kosten"][generation]
        g = self.gen.loc[generation]
        tafel = str(g["sterbetafel_vereinfacht"])
        spalte = "qx_unisex" if self.unisex(generation, markt, abschluss) else ("qx_w" if geschlecht == "W" else "qx_m")
        mittleres_alter = int(round(alter + laufzeit / 2))
        q = self.qx(tafel, mittleres_alter, spalte)
        raucher_f = float(p["risikofaktoren"]["raucher"]["raucher" if raucher else "nichtraucher"])
        i = self.rechnungszins(generation, markt, abschluss.year)
        f = {"qx": q, "raucher": raucher_f, "zuschlag": 1 + zuschlag_pct / 100, "rechnungszins": i}
        stueck = float(kosten["stueck"][markt])
        alpha = float(kosten["alpha_promille"]) * summe / 1000 / max(laufzeit, 1)
        beta = float(kosten["beta_pct"]) / 100
        if produkt == "LV-RISK":
            risikosumme = summe * float(p["LV-RISK"]["summenverlauf_faktor"][summenverlauf])
            risiko = risikosumme * q * raucher_f * (1 + zuschlag_pct / 100)
            rab = p["risikofaktoren"]["summenrabatt"]["LV-RISK"]
            srab = float(rab["ab_1000000"] if summe >= 1_000_000 else rab["ab_500000"] if summe >= 500_000 else rab["ab_250000"] if summe >= 250_000 else rab["bis_250000"])
            netto = risiko + alpha * srab + stueck
            spar = 0.0
        elif produkt in ("LV-VORS", "LV-RENTE"):
            n = max(laufzeit, 1)
            spar = summe * i / ((1 + i) ** n - 1) if i > 0 else summe / n
            dk_mitte = ((1 + i) ** (n / 2) - 1) / ((1 + i) ** n - 1) if i > 0 else 0.5
            risikosumme = summe * (1 - dk_mitte) if produkt == "LV-VORS" else 0.0
            risiko = risikosumme * q * raucher_f * (1 + zuschlag_pct / 100)
            netto = spar + risiko + alpha + stueck
        else:  # LV-EU Zusatz
            satz = float(p["LV-EU"]["praemie_pct_der_jahresrente"][markt]) / 100
            bg = float(p["risikofaktoren"]["berufsgruppe_eu_bu"][berufsgruppe])
            risiko = eu_rente_jahr * satz * bg * (1 + zuschlag_pct / 100)
            netto, spar = risiko, 0.0
        tarif = netto / (1 - beta)
        tarif = max(tarif, float(p["meta"]["mindestpraemie_jahr"][produkt][markt]))
        f.update({"sparpraemie": round(spar, 2), "risikopraemie": round(risiko, 2), "alpha": round(alpha, 2), "beta": beta, "stueck": stueck})
        zahl = tarif
        if produkt == "LV-RISK":
            jahr = min(max(abschluss.year, 2016), 2025)
            u = self.ueb[(self.ueb["generation_code"] == generation) & (self.ueb["markt"] == markt) & (self.ueb["jahr"] == jahr)]
            rueb = float(u.iloc[0]["risikoueberschuss_pct"]) / 100 if len(u) else 0.25
            zahl = tarif * (1 - rueb)
            f["risikoueberschuss"] = rueb
        zuschlag = float(p["meta"]["zahlweise_zuschlag"][zahlweise.lower()])
        zahl = _runden(zahl * (1 + zuschlag), markt)
        steuer = 0.0
        return Praemie(_runden(tarif, markt), steuer, zahl, f)
