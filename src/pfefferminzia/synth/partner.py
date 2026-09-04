"""Stufe ``partner``: Partner (natuerliche und juristische Personen), Haushalte, Adressen, Kontakte.

Grundsatz (Datenarchitektur 5.1): zuerst die wahre Welt (Identitaet, Haushalt, latente Neigungen),
daraus die beobachtbaren Stammdaten. Die Kunden-Personas belegen die IDs PTR-00000001 bis
PTR-00000020; alle weiteren Partner werden synthetisch erzeugt.

Tabellen (curated): partner, partner_adresse, partner_kontakt, partner_beziehung.
Tabellen (truth): partner_latent.
"""

from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd

from pfefferminzia.context import RunContext
from pfefferminzia.ids import partner_id
from pfefferminzia.pipeline import Stage, register
from pfefferminzia.synth.addresses import AddressSynth, Adresse
from pfefferminzia.synth.identifiers import che_uid, email_privat, telefon
from pfefferminzia.synth.names import NameSynth, firmenname
from pfefferminzia.synth.referenz_intern import BERUFE
from pfefferminzia.validate.fiction import lade_blocklist

PERSONA_RESERVIERT = 20

# Bezugspersonen der Kunden-Personas (docs/personas/kunden): id, vorname, nachname, geschlecht, geburtsdatum,
# haushalt der Persona, rolle, land, plz, ort, strasse, hausnummer, sprache, verstorben_am
BEZUGSPERSONEN = [
    (11, "Reto", "Niederberger", "M", "1982-07-21", 1, "EHEPARTNER", "CH", "6004", "Luzern", "Rebhaldenweg", "7", "de", None),
    (12, "Bruno", "Kaufmann", "M", "1968-10-05", 3, "INHABER", "CH", "5600", "Lenzburg", "Sägereiweg", "4", "de", None),
    (13, "Marc", "Kaufmann", "M", "1994-03-18", 3, "KONTAKT", "CH", "5600", "Lenzburg", "Sägereiweg", "4", "de", None),
    (14, "Kerstin", "Bergmann", "W", "1977-02-03", 4, "GESCHAEFTSFUEHRUNG", "DE", "01796", "Pirna", "Kupferring", "18", "de", None),
    (15, "Walter", "Vogt", "M", "1951-08-30", 5, "EHEPARTNER", "CH", "4500", "Solothurn", "Lindenrain", "3", "de", "2019-02-14"),
    (16, "Sabine", "Nazari", "W", "1976-05-12", 6, "EHEPARTNER", "DE", "81925", "München", "Sternenallee", "41", "de", None),
    (17, "Marcel", "Grimm", "M", "1986-07-11", 9, "INHABER", "DE", "15711", "Königs Wusterhausen", "Sandacker", "5", "de", None),
    (18, "Rui", "Ferreira", "M", "1977-09-02", 10, "EHEPARTNER", "CH", "4051", "Basel", "Silberhalde", "14", "de", None),
    (19, "Lina", "Niederberger", "W", "2014-04-09", 1, "KIND", "CH", "6004", "Luzern", "Rebhaldenweg", "7", "de", None),
    (20, "Noah", "Niederberger", "M", "2017-11-23", 1, "KIND", "CH", "6004", "Luzern", "Rebhaldenweg", "7", "de", None),
]

ZIVILSTAND_P = {"LEDIG": 0.34, "VERHEIRATET": 0.44, "GESCHIEDEN": 0.10, "VERWITWET": 0.06, "PARTNERSCHAFT": 0.05,
                "UNBEKANNT": 0.01}
NATIONALITAET = {"CH": (["CH", "DE", "IT", "PT", "FR", "TR", "RS", "ES", "AT", "XK"], [0.72, 0.06, 0.06, 0.04, 0.03, 0.02, 0.02, 0.02, 0.02, 0.01]),
                 "DE": (["DE", "TR", "PL", "IT", "RO", "SY", "CH", "AT", "RS", "GR"], [0.83, 0.04, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01])}


def _quellsystem(rng: np.random.Generator, land: str, herkunft: str, sparten: str) -> str:
    if herkunft == "minzia":
        return "MINT"
    return "VERA" if sparten == "LV" else "HAPO"


class PartnerWelt:
    """Erzeugt Haushalte und Partner bis zur Zielmenge."""

    def __init__(self, ctx: RunContext):
        self.ctx = ctx
        ref = ctx.reference
        self.ns = NameSynth(ref.csv("namen.vornamen"), ref.csv("namen.nachnamen"), lade_blocklist(ctx))
        self.ad = AddressSynth(ref.csv("geo.orte_ch"), ref.csv("geo.orte_de"), ref.csv("geo.strassennamen"))
        self.bausteine = ref.csv("namen.firmennamen_bausteine")
        self.branchen = ref.verzeichnis("hp")["branchenklassen"].copy()
        for c in ("noga_code", "wz_code"):
            self.branchen[c] = self.branchen[c].map(lambda v: f"{float(v):.2f}")
        self.stichtag = ctx.config.zeit.stichtag
        self.partner: list[dict] = []
        self.adressen: list[dict] = []
        self.kontakte: list[dict] = []
        self.beziehungen: list[dict] = []
        self.latent: list[dict] = []
        self.berufe_gew = np.array([b[3] for b in BERUFE])

    # -- Bausteine ---------------------------------------------------------------
    def _person(self, n: int, rng, land: str, geschlecht: str | None = None, geburtsjahr: int | None = None,
                nachname: str | None = None, adresse: Adresse | None = None, herkunft: str = "pfefferminz",
                haushalt_id: str | None = None, sprache: str | None = None) -> dict:
        if geschlecht is None:
            geschlecht = str(rng.choice(["M", "W", "D"], p=[0.49, 0.50, 0.01]))
        if geburtsjahr is None:
            geburtsjahr = int(np.clip(rng.normal(self.stichtag.year - 44, 14), 1930, 2007))
        if adresse is None:
            adresse = self.ad.adresse(rng, land)
        sprache = sprache or adresse.sprache
        p = self.ns.person(rng, "M" if geschlecht == "D" else geschlecht, land, geburtsjahr, sprache)
        if nachname is not None and rng.random() < 0.7:
            p.nachname = nachname
        gebdatum = date(geburtsjahr, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
        alter = self.stichtag.year - geburtsjahr
        nat_liste, nat_p = NATIONALITAET[land]
        beruf_idx = int(rng.choice(len(BERUFE), p=self.berufe_gew / self.berufe_gew.sum()))
        if alter >= 65:
            beruf_idx = 22
        elif alter < 25 and rng.random() < 0.5:
            beruf_idx = 21
        beruf = BERUFE[beruf_idx]
        zivil = self._zivilstand(rng, alter)
        verstorben = rng.random() < (0.002 + 0.0006 * max(alter - 60, 0))
        todesdatum = None
        if verstorben:
            todesdatum = self.stichtag - timedelta(days=int(rng.integers(1, 365 * 6)))
        pid = partner_id(n)
        eintrag = {
            "partner_id": pid, "partner_typ": "NATUERLICH", "anrede": {"M": "Herr", "W": "Frau", "D": ""}[geschlecht],
            "titel": "Dr." if (beruf[0] in ("B11", "B12", "B14") and rng.random() < 0.4) else None,
            "vorname": p.vorname, "nachname": p.nachname, "firmenname": None, "rechtsform": None, "uid_hrb_nummer": None,
            "geburtsdatum": gebdatum, "geschlecht": geschlecht, "nationalitaet": str(rng.choice(nat_liste, p=nat_p)),
            "zivilstand": zivil, "beruf_code": beruf[0], "beruf_text": beruf[1], "beruf_selbstaendig": bool(rng.random() < beruf[4]),
            "sprache": sprache, "land_wohnsitz": land, "kundensegment": "PRIVAT", "kunde_seit": None,
            "status": "VERSTORBEN" if verstorben else "AKTIV", "todesdatum": todesdatum,
            "datenschutz_werbung_ok": bool(rng.random() < 0.55), "datenschutz_ki_ok": bool(rng.random() < (0.7 if herkunft == "minzia" else 0.35)),
            "herkunft": herkunft, "quellsystem_primaer": None, "haushalt_id": haushalt_id, "ist_persona": False,
            "erstellt_am": None, "geaendert_am": None,
        }
        self._adresse(pid, adresse, rng, umzug=rng.random() < 0.28 and not verstorben)
        self._kontakte(pid, rng, p.vorname, p.nachname, geburtsjahr, land, herkunft)
        self.latent.append({
            "partner_id": pid, "kuendigungsneigung": float(np.clip(rng.beta(2, 6) * (1.4 if alter < 30 else 1.0), 0, 1)),
            "betrugsneigung": float(np.clip(rng.beta(1.2, 20), 0, 1)),
            "preissensitivitaet": float(rng.beta(3, 3)), "digitalaffinitaet": float(np.clip(rng.beta(4, 3) - 0.008 * max(alter - 40, 0), 0, 1)),
            "bmi": float(np.clip(rng.normal(25.5, 4.2), 16, 48)), "raucher": bool(rng.random() < (0.22 if alter < 60 else 0.12)),
            "gesundheit_score": float(np.clip(rng.beta(5, 2) - 0.004 * max(alter - 50, 0), 0, 1)),
            "todesdatum": todesdatum, "hund": bool(rng.random() < 0.12),
        })
        return eintrag

    def _zivilstand(self, rng, alter: int) -> str:
        if alter < 25:
            return "LEDIG"
        keys, p = zip(*ZIVILSTAND_P.items(), strict=True)
        return str(rng.choice(keys, p=np.array(p) / sum(p)))

    def _adresse(self, pid: str, adresse: Adresse, rng, umzug: bool) -> None:
        heute = self.stichtag
        if umzug:
            alt = self.ad.adresse(rng, adresse.land, adresse.sprache)
            seit_alt = heute - timedelta(days=int(rng.integers(365 * 4, 365 * 25)))
            wechsel = heute - timedelta(days=int(rng.integers(30, 365 * 4)))
            self.adressen.append(self._adr_zeile(pid, alt, seit_alt, wechsel - timedelta(days=1), "WOHNSITZ", False))
            self.adressen.append(self._adr_zeile(pid, adresse, wechsel, None, "WOHNSITZ", True))
        else:
            seit = heute - timedelta(days=int(rng.integers(180, 365 * 30)))
            self.adressen.append(self._adr_zeile(pid, adresse, seit, None, "WOHNSITZ", True))

    @staticmethod
    def _adr_zeile(pid, a: Adresse, von, bis, typ, aktuell) -> dict:
        return {"partner_id": pid, "adresse_typ": typ, "strasse": a.strasse, "hausnummer": a.hausnummer, "plz": a.plz,
                "ort": a.ort, "region": a.region, "land": a.land, "tarifzone": a.tarifzone, "gueltig_von": von,
                "gueltig_bis": bis, "ist_aktuell": aktuell}

    def _kontakte(self, pid, rng, vorname, nachname, geburtsjahr, land, herkunft) -> None:
        p_email = 0.98 if herkunft == "minzia" else (0.6 if geburtsjahr < 1955 else 0.85)
        if rng.random() < p_email:
            self.kontakte.append({"partner_id": pid, "kontakt_typ": "EMAIL", "wert": email_privat(rng, vorname, nachname, geburtsjahr),
                                  "ist_primaer": True})
        mobil = rng.random() < (0.95 if geburtsjahr > 1960 else 0.6)
        self.kontakte.append({"partner_id": pid, "kontakt_typ": "MOBIL" if mobil else "TELEFON",
                              "wert": telefon(rng, land, mobil=mobil and land == "DE"), "ist_primaer": True})

    def _firma(self, n: int, rng, land: str, herkunft: str, inhaber_id: str | None) -> dict:
        adresse = self.ad.adresse(rng, land)
        gew = self.branchen["anteil_bestand_pct"].to_numpy(dtype=float)
        br = self.branchen.iloc[int(rng.choice(len(self.branchen), p=gew / gew.sum()))]
        name = firmenname(rng, self.bausteine, land, lade_blocklist(self.ctx))
        rechtsform = name.split(" ")[-1] if name.split(" ")[-1] in ("AG", "GmbH", "Sàrl", "SA", "Sagl", "KG", "e.K.") else "Einzelfirma"
        pid = partner_id(n)
        gruendung = date(int(rng.integers(1975, 2023)), int(rng.integers(1, 13)), 1)
        eintrag = {
            "partner_id": pid, "partner_typ": "JURISTISCH", "anrede": "Firma", "titel": None, "vorname": None, "nachname": None,
            "firmenname": name, "rechtsform": rechtsform,
            "uid_hrb_nummer": che_uid(rng) if land == "CH" else f"HRB {int(rng.integers(1000, 99999))}",
            "geburtsdatum": gruendung, "geschlecht": "UNBEKANNT", "nationalitaet": land, "zivilstand": "UNBEKANNT",
            "beruf_code": None, "beruf_text": None, "beruf_selbstaendig": None, "sprache": adresse.sprache, "land_wohnsitz": land,
            "kundensegment": "KMU", "kunde_seit": None, "status": "AKTIV", "todesdatum": None,
            "datenschutz_werbung_ok": bool(rng.random() < 0.6), "datenschutz_ki_ok": bool(rng.random() < 0.45),
            "herkunft": herkunft, "quellsystem_primaer": None, "haushalt_id": None, "ist_persona": False,
            "erstellt_am": None, "geaendert_am": None,
            "branche_id": br["branche_id"], "nace_code": br["noga_code"], "risikoklasse": int(br["risikoklasse"]),
            "mitarbeitende": int(np.clip(rng.lognormal(1.6, 0.9), 1, 50)),
        }
        eintrag["umsatz"] = float(round(eintrag["mitarbeitende"] * float(rng.lognormal(11.6, 0.35)), -3))
        self.adressen.append(self._adr_zeile(pid, adresse, gruendung, None, "GESCHAEFTSSITZ", True))
        self.kontakte.append({"partner_id": pid, "kontakt_typ": "EMAIL", "wert": f"info@{name.split(' ')[0].lower()}-{name.split(' ')[1].lower()}.example",
                              "ist_primaer": True})
        self.kontakte.append({"partner_id": pid, "kontakt_typ": "TELEFON", "wert": telefon(rng, land), "ist_primaer": True})
        if inhaber_id:
            self.beziehungen.append({"partner_id_von": inhaber_id, "partner_id_zu": pid, "beziehung": "INHABER", "seit": gruendung})
        self.latent.append({"partner_id": pid, "kuendigungsneigung": float(rng.beta(2, 5)), "betrugsneigung": float(np.clip(rng.beta(1.2, 25), 0, 1)),
                            "preissensitivitaet": float(rng.beta(4, 3)), "digitalaffinitaet": float(rng.beta(3, 3)), "bmi": None,
                            "raucher": None, "gesundheit_score": None, "todesdatum": None, "hund": False})
        return eintrag

    # -- Personas ----------------------------------------------------------------
    def personas(self) -> None:
        k = self.ctx.reference.csv("personas_kunden.csv")
        rng = self.ctx.rng("partner", "personas")
        for _, r in k.iterrows():
            pid = r["partner_id"]
            n = int(pid.split("-")[1])
            land = r["land"]
            gew = self.branchen["anteil_bestand_pct"].to_numpy(dtype=float)
            juristisch = r["kundentyp"] == "gewerbe"
            adr = Adresse(r["strasse"], str(r["hausnummer"]), str(r["plz"]), r["ort"], land, r["kanton_bundesland"], "de",
                          self._zone(str(r["plz"]), land))
            herkunft = "minzia" if r["quellsystem"] == "MINT" else "pfefferminz"
            if juristisch:
                br = self.branchen.iloc[int(rng.choice(len(self.branchen), p=gew / gew.sum()))]
                nace = {"PTR-00000003": "43.32", "PTR-00000004": "43.22", "PTR-00000009": "49.41"}.get(pid, br["noga_code"])
                brz = self.branchen[self.branchen["noga_code"] == nace].iloc[0]
                self.partner.append({
                    "partner_id": pid, "partner_typ": "JURISTISCH", "anrede": "Firma", "titel": None, "vorname": None, "nachname": None,
                    "firmenname": r["nachname"], "rechtsform": r["nachname"].split(" ")[-1], "uid_hrb_nummer": che_uid(rng) if land == "CH" else f"HRB {int(rng.integers(1000, 99999))}",
                    "geburtsdatum": pd.to_datetime(r["geburtsdatum"]).date(), "geschlecht": "UNBEKANNT", "nationalitaet": land, "zivilstand": "UNBEKANNT",
                    "beruf_code": None, "beruf_text": None, "beruf_selbstaendig": None, "sprache": "de", "land_wohnsitz": land,
                    "kundensegment": "KMU", "kunde_seit": None, "status": "AKTIV", "todesdatum": None,
                    "datenschutz_werbung_ok": True, "datenschutz_ki_ok": pid != "PTR-00000009", "herkunft": herkunft,
                    "quellsystem_primaer": None, "haushalt_id": f"HH-{n:06d}", "ist_persona": True, "erstellt_am": None, "geaendert_am": None,
                    "branche_id": brz["branche_id"], "nace_code": nace, "risikoklasse": int(brz["risikoklasse"]),
                    "mitarbeitende": {"PTR-00000003": 14, "PTR-00000004": 42, "PTR-00000009": 3}[pid],
                    "umsatz": {"PTR-00000003": 2600000.0, "PTR-00000004": 6800000.0, "PTR-00000009": 310000.0}[pid],
                })
                self.adressen.append(self._adr_zeile(pid, adr, pd.to_datetime(r["geburtsdatum"]).date(), None, "GESCHAEFTSSITZ", True))
                self.kontakte.append({"partner_id": pid, "kontakt_typ": "TELEFON", "wert": telefon(rng, land), "ist_primaer": True})
                self.latent.append({"partner_id": pid, "kuendigungsneigung": 0.2, "betrugsneigung": 0.95 if pid == "PTR-00000009" else 0.02,
                                    "preissensitivitaet": 0.5, "digitalaffinitaet": 0.6, "bmi": None, "raucher": None,
                                    "gesundheit_score": None, "todesdatum": None, "hund": False})
            else:
                gebdatum = pd.to_datetime(r["geburtsdatum"]).date()
                alter = self.stichtag.year - gebdatum.year
                beruf = {"PTR-00000001": BERUFE[17], "PTR-00000002": BERUFE[26], "PTR-00000005": BERUFE[22], "PTR-00000006": BERUFE[10],
                         "PTR-00000007": BERUFE[21], "PTR-00000008": BERUFE[22], "PTR-00000010": BERUFE[20]}[pid]
                self.partner.append({
                    "partner_id": pid, "partner_typ": "NATUERLICH", "anrede": "Herr" if r["geschlecht"] == "M" else "Frau",
                    "titel": "Dr. med." if pid == "PTR-00000006" else None, "vorname": r["vorname"], "nachname": r["nachname"],
                    "firmenname": None, "rechtsform": None, "uid_hrb_nummer": None, "geburtsdatum": gebdatum, "geschlecht": r["geschlecht"],
                    "nationalitaet": "PT" if pid == "PTR-00000010" else land, "zivilstand": {"PTR-00000001": "VERHEIRATET", "PTR-00000005": "VERWITWET",
                                                                                              "PTR-00000006": "VERHEIRATET", "PTR-00000008": "GESCHIEDEN",
                                                                                              "PTR-00000010": "VERHEIRATET"}.get(pid, "LEDIG"),
                    "beruf_code": beruf[0], "beruf_text": r["beruf_branche"], "beruf_selbstaendig": pid in ("PTR-00000006", "PTR-00000010"),
                    "sprache": "de", "land_wohnsitz": land, "kundensegment": "PREMIUM" if pid in ("PTR-00000006", "PTR-00000010") else "PRIVAT",
                    "kunde_seit": None, "status": "AKTIV", "todesdatum": None, "datenschutz_werbung_ok": pid not in ("PTR-00000005", "PTR-00000008"),
                    "datenschutz_ki_ok": pid in ("PTR-00000002", "PTR-00000007", "PTR-00000001"), "herkunft": herkunft, "quellsystem_primaer": None,
                    "haushalt_id": f"HH-{n:06d}", "ist_persona": True, "erstellt_am": None, "geaendert_am": None,
                })
                self.adressen.append(self._adr_zeile(pid, adr, date(2021, 1, 1) if alter < 30 else date(2010, 1, 1), None, "WOHNSITZ", True))
                if pid == "PTR-00000001":  # alte Adresse (HAPO), siehe Persona
                    self.adressen[-1]["gueltig_von"] = date(2023, 6, 1)
                    self.adressen.append(self._adr_zeile(pid, Adresse("Kreuzmattweg", "22", "6003", "Luzern", "CH", "LU", "de", "2"),
                                                         date(2009, 4, 1), date(2023, 5, 31), "WOHNSITZ", False))
                if pid == "PTR-00000002":
                    self.adressen[-1]["gueltig_von"] = date(2021, 9, 1)
                    self.adressen.append(self._adr_zeile(pid, Adresse("Amselgasse", "8", "04600", "Altenburg", "DE", "TH", "de", "3"),
                                                         date(1996, 8, 22), date(2021, 8, 31), "WOHNSITZ", False))
                if pid != "PTR-00000005":
                    self.kontakte.append({"partner_id": pid, "kontakt_typ": "EMAIL", "wert": email_privat(rng, r["vorname"], r["nachname"], gebdatum.year), "ist_primaer": True})
                self.kontakte.append({"partner_id": pid, "kontakt_typ": "MOBIL" if pid in ("PTR-00000002", "PTR-00000007") else "TELEFON",
                                      "wert": telefon(rng, land, mobil=(land == "DE" and pid == "PTR-00000002")), "ist_primaer": True})
                self.latent.append({"partner_id": pid, "kuendigungsneigung": {"PTR-00000007": 0.85, "PTR-00000008": 0.4}.get(pid, 0.15),
                                    "betrugsneigung": 0.01, "preissensitivitaet": 0.8 if pid == "PTR-00000007" else 0.4,
                                    "digitalaffinitaet": 0.95 if herkunft == "minzia" else 0.3, "bmi": 27.0 if pid == "PTR-00000006" else 23.0,
                                    "raucher": False, "gesundheit_score": 0.6 if pid == "PTR-00000006" else 0.85, "todesdatum": None,
                                    "hund": pid in ("PTR-00000005", "PTR-00000008")})
        for n, vn, nn, g, geb, hh, rolle, land, plz, ort, strasse, hnr, spr, tod in BEZUGSPERSONEN:
            pid = partner_id(n)
            gebd = date.fromisoformat(geb)
            todd = date.fromisoformat(tod) if tod else None
            self.partner.append({
                "partner_id": pid, "partner_typ": "NATUERLICH", "anrede": "Herr" if g == "M" else "Frau", "titel": None, "vorname": vn, "nachname": nn,
                "firmenname": None, "rechtsform": None, "uid_hrb_nummer": None, "geburtsdatum": gebd, "geschlecht": g, "nationalitaet": "PT" if n == 18 else land,
                "zivilstand": "VERHEIRATET" if rolle == "EHEPARTNER" else "LEDIG", "beruf_code": "B23" if n == 15 else ("B22" if rolle == "KIND" else "B01"),
                "beruf_text": BERUFE[22][1] if n == 15 else (BERUFE[21][1] if rolle == "KIND" else BERUFE[0][1]), "beruf_selbstaendig": rolle == "INHABER",
                "sprache": spr, "land_wohnsitz": land, "kundensegment": "PRIVAT", "kunde_seit": None, "status": "VERSTORBEN" if todd else "AKTIV",
                "todesdatum": todd, "datenschutz_werbung_ok": False, "datenschutz_ki_ok": False, "herkunft": "pfefferminz", "quellsystem_primaer": None,
                "haushalt_id": f"HH-{hh:06d}", "ist_persona": True, "erstellt_am": None, "geaendert_am": None,
            })
            self.adressen.append(self._adr_zeile(pid, Adresse(strasse, hnr, plz, ort, land, "", spr, self._zone(plz, land)), date(2010, 1, 1), None, "WOHNSITZ", True))
            self.beziehungen.append({"partner_id_von": pid, "partner_id_zu": partner_id(hh), "beziehung": rolle, "seit": date(2010, 1, 1)})
            self.latent.append({"partner_id": pid, "kuendigungsneigung": 0.2, "betrugsneigung": 0.9 if n == 17 else 0.01, "preissensitivitaet": 0.5,
                                "digitalaffinitaet": 0.5, "bmi": 24.0, "raucher": False, "gesundheit_score": 0.8, "todesdatum": todd, "hund": False})
        # Adress-Region fuer Bezugspersonen nachtragen
        for a in self.adressen:
            if not a["region"]:
                tab = self.ad.orte[a["land"]]
                treffer = tab[tab["plz"] == a["plz"]]
                if len(treffer):
                    a["region"] = str(treffer.iloc[0]["kanton" if a["land"] == "CH" else "bundesland_kuerzel"])

    def _zone(self, plz: str, land: str) -> str:
        tab = self.ad.orte[land]
        t = tab[tab["plz"] == plz]
        return str(t.iloc[0]["tarifzone"]) if len(t) else ("2" if land == "CH" else "3")

    # -- Synthese ------------------------------------------------------------------
    def erzeugen(self) -> None:
        self.personas()
        ziel = self.ctx.menge("partner")
        anteil_ch = self.ctx.config.markt.anteil_ch
        n = PERSONA_RESERVIERT + 1
        hh = PERSONA_RESERVIERT + 1
        while len(self.partner) < ziel:
            rng = self.ctx.rng("haushalt", hh)
            herkunft = "minzia" if rng.random() < 0.32 else "pfefferminz"
            # Pfefferminz CH-lastig (60/40), Minzia DE-lastig (20/80); Gesamt ~47 % CH
            p_ch = 0.62 if herkunft == "pfefferminz" else 0.18
            land = "CH" if rng.random() < p_ch else "DE"
            _ = anteil_ch
            haushalt_id = f"HH-{hh:06d}"
            if rng.random() < 0.11:  # juristische Person, evtl. mit Inhaber
                inhaber = None
                if rng.random() < 0.6 and len(self.partner) + 1 < ziel:
                    inhaber_e = self._person(n, rng, land, geburtsjahr=int(np.clip(rng.normal(1972, 10), 1945, 1995)),
                                             herkunft=herkunft, haushalt_id=haushalt_id)
                    inhaber_e["beruf_code"], inhaber_e["beruf_text"], inhaber_e["beruf_selbstaendig"] = "B40", BERUFE[39][1], True
                    self.partner.append(inhaber_e)
                    inhaber = inhaber_e["partner_id"]
                    n += 1
                self.partner.append(self._firma(n, rng, land, herkunft, inhaber))
                n += 1
            else:
                groesse = int(rng.choice([1, 2, 3, 4, 5], p=[0.38, 0.32, 0.14, 0.11, 0.05]))
                if herkunft == "minzia":
                    groesse = int(rng.choice([1, 2, 3], p=[0.62, 0.3, 0.08]))
                kopf = self._person(n, rng, land, herkunft=herkunft, haushalt_id=haushalt_id)
                kopf_alter = self.stichtag.year - kopf["geburtsdatum"].year
                self.partner.append(kopf)
                n += 1
                adresse = self._aktuelle_adresse(kopf["partner_id"])
                if groesse >= 2 and len(self.partner) < ziel and kopf_alter >= 22:
                    g2 = "W" if kopf["geschlecht"] == "M" else "M"
                    if rng.random() < 0.06:
                        g2 = kopf["geschlecht"]
                    p2 = self._person(n, rng, land, geschlecht=g2, geburtsjahr=int(np.clip(kopf["geburtsdatum"].year + rng.integers(-6, 7), 1930, 2005)),
                                      nachname=kopf["nachname"], adresse=adresse, herkunft=herkunft, haushalt_id=haushalt_id, sprache=kopf["sprache"])
                    p2["zivilstand"] = kopf["zivilstand"] = "VERHEIRATET" if rng.random() < 0.75 else "PARTNERSCHAFT"
                    self.partner.append(p2)
                    self.beziehungen.append({"partner_id_von": p2["partner_id"], "partner_id_zu": kopf["partner_id"], "beziehung": "EHEPARTNER", "seit": None})
                    n += 1
                    for _k in range(groesse - 2):
                        if len(self.partner) >= ziel:
                            break
                        kj = int(np.clip(kopf["geburtsdatum"].year + rng.integers(24, 40), 1950, self.stichtag.year - 1))
                        if kj > 2007:
                            kj = 2007
                        kind = self._person(n, rng, land, geburtsjahr=kj, nachname=kopf["nachname"], adresse=adresse, herkunft=herkunft,
                                            haushalt_id=haushalt_id, sprache=kopf["sprache"])
                        kind["zivilstand"] = "LEDIG"
                        self.partner.append(kind)
                        self.beziehungen.append({"partner_id_von": kind["partner_id"], "partner_id_zu": kopf["partner_id"], "beziehung": "KIND", "seit": kind["geburtsdatum"]})
                        n += 1
            hh += 1

    def _aktuelle_adresse(self, pid: str) -> Adresse:
        for a in reversed(self.adressen):
            if a["partner_id"] == pid and a["ist_aktuell"]:
                return Adresse(a["strasse"], a["hausnummer"], a["plz"], a["ort"], a["land"], a["region"], "de" if a["land"] == "DE" else "de", a["tarifzone"])
        raise KeyError(pid)

    def tabellen(self) -> dict[str, pd.DataFrame]:
        partner = pd.DataFrame(self.partner)
        firmen_spalten = ["branche_id", "nace_code", "risikoklasse", "mitarbeitende", "umsatz"]
        for c in firmen_spalten:
            if c not in partner.columns:
                partner[c] = None
        firma = partner.loc[partner["partner_typ"] == "JURISTISCH", ["partner_id", *firmen_spalten]].reset_index(drop=True)
        partner = partner.drop(columns=firmen_spalten)
        adressen = pd.DataFrame(self.adressen)
        adressen.insert(0, "adresse_id", [f"ADR-{i + 1:08d}" for i in range(len(adressen))])
        kontakte = pd.DataFrame(self.kontakte)
        kontakte.insert(0, "kontakt_id", [f"KON-{i + 1:08d}" for i in range(len(kontakte))])
        beziehungen = pd.DataFrame(self.beziehungen)
        return {"partner": partner, "partner_firma": firma, "partner_adresse": adressen, "partner_kontakt": kontakte,
                "partner_beziehung": beziehungen, "partner_latent": pd.DataFrame(self.latent)}


@register
class PartnerStage(Stage):
    name, nummer, welle = "partner", 30, 1
    beschreibung = "Partner, Adressen, Kontakte, Beziehungen, latente Kundenmerkmale"

    def run(self, ctx: RunContext) -> None:
        welt = PartnerWelt(ctx)
        welt.erzeugen()
        t = welt.tabellen()
        for name, df in t.items():
            ctx.tabellen.register(name, df, layer="truth" if name.endswith("_latent") else "curated", ersetzen=True)
        ctx.ereignis(self.name, f"{len(t['partner'])} Partner ({int((t['partner']['partner_typ'] == 'JURISTISCH').sum())} juristisch), "
                                f"{len(t['partner_adresse'])} Adressen, {len(t['partner_beziehung'])} Beziehungen")
