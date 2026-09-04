"""Stufe ``legacyify``: Rohextrakte der Pfefferminz-Altsysteme VERA (Leben) und HAPO (Haftpflicht).

Erzeugt unter ``raw/<stufe>/pvs/`` je System eine PARTNER- und eine VERTRAG-Datei als Fixed-width-Text
(Satzarten, ISO-8859-1) und als Semikolon-CSV (Reporting-Extrakt), injiziert die Datenqualitaets-
probleme DQ-01 bis DQ-15 (Datenarchitektur 2.2) und protokolliert sie in ``truth/dq_injektionen``.
Zusaetzlich entstehen ``migration/partner_xref``, ``migration/vertrag_xref`` und ``migration/migrationslog``.

Extraktstand: 2025-12-31 (letzter Abzug vor Abschaltung). Migrierte Vertraege tragen STATUS S mit dem
undokumentierten Stornogrund ZZ und dem Migrationsdatum als AENDDAT (DQ-08, DQ-25).
"""

from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

from pfefferminzia.context import RunContext
from pfefferminzia.export import _relativ
from pfefferminzia.ids import hapo_vertragsnummer, legacy_partnernummer, vera_vertragsnummer
from pfefferminzia.legacy.dq import (
    DqProtokoll,
    adresse_freitext,
    bemerk,
    datum_int,
    datum_kurz,
    fixed,
    kuerze_name,
    mojibake,
    rappen,
    translit_upper,
)
from pfefferminzia.manifest import sha256_datei
from pfefferminzia.pipeline import Stage, register
from pfefferminzia.synth.referenz_intern import (
    PVS_GESCHLECHT,
    PVS_LANDKZ,
    PVS_STATUS,
    PVS_STORNOGRUND,
    PVS_ZAHLWEISE,
    PVS_ZIVILSTAND,
)

PARTNER_FELDER = [("PARTNR", 8), ("NAME1", 30), ("NAME2", 30), ("GEBDAT", 8), ("GESCHL", 1), ("ZIVST", 1), ("ADR1", 30), ("ADR2", 30),
                  ("ADR3", 30), ("LANDKZ", 3), ("SPRACHE", 1), ("TEL", 16), ("EMAIL", 40), ("BERUF", 20), ("KDSEIT", 8), ("AENDDAT", 8),
                  ("BEMERK", 60)]
VERTRAG_FELDER = [("VERTRNR", 12), ("PARTNR", 8), ("SPARTE", 2), ("TARIF", 10), ("BEGDAT", 8), ("ENDDAT", 8), ("PRAEM", 10), ("ZAHLWS", 2),
                  ("STATUS", 1), ("STORNOGRD", 2), ("STORNODAT", 8), ("LANDKZ", 3), ("VERMNR", 5), ("VERMNR_ALT", 5), ("SUMME", 12),
                  ("ZUSATZ1", 10), ("ZUSATZ2", 10), ("AENDDAT", 8), ("BEMERK", 60)]
SPRACHE_CODE = {"de": "D", "fr": "F", "it": "I", "en": "E"}
HAPO_SPARTE = {"HP-PRIV": "10", "HP-BETR": "20", "HP-BERUF": "30"}
VERA_TARIFCODE = {"PK-85": "K85", "PK-95": "K95", "PK-2000": "K00", "PK-2004": "K04", "PK-2007": "K07", "PL-2012": "L12", "PL-2015": "L15",
                  "PL-2017": "L17", "MZ-2020": "M20", "PZ-2025": "Z25"}
VERA_PRODUKT = {"LV-RISK": "R", "LV-VORS": "K", "LV-RENTE": "N", "LV-EU": "E"}
HAPO_GEN = {"HP-KLASSIK": "PFM-K", "HP-MODERN": "PFM-M", "MZ-DIRECT": "MZD", "PM-2025": "PM25"}
MIGRATION_DATUM = {"HAPO": date(2025, 5, 15), "VERA": date(2025, 11, 15)}


class Legacy:
    def __init__(self, ctx: RunContext):
        self.ctx = ctx
        self.raten = ctx.config.dq.raten
        self.aktiv = ctx.config.dq.aktiv
        self.dq = DqProtokoll()
        t = ctx.tabellen
        self.partner = t.get("partner").set_index("partner_id")
        self.adr = t.get("partner_adresse")
        self.kontakt = t.get("partner_kontakt")
        self.vertrag = t.get("vertrag")
        self.rollen = t.get("vertrag_partner_rolle")
        self.deckung = t.get("deckung")
        self.risiko = t.get("risiko_objekt").set_index("vertrag_id")
        self.vermittler = t.get("vermittler").set_index("vermittler_id")
        self.xref_partner: list[dict] = []
        self.xref_vertrag: list[dict] = []
        self.log: list[dict] = []
        self.stichtag = ctx.config.zeit.stichtag

    def rate(self, regel: str, default: float) -> float:
        return float(self.raten.get(regel, default)) if self.aktiv else 0.0

    # -- Partnerauswahl je System ----------------------------------------------------
    def partner_je_system(self, system: str) -> list[str]:
        v = self.vertrag[self.vertrag["quellsystem"] == system]
        ids = set(v["versicherungsnehmer_id"])
        rollen = self.rollen[self.rollen["vertrag_id"].isin(v["vertrag_id"]) & self.rollen["partner_id"].notna()]
        ids |= set(rollen["partner_id"])
        return sorted(ids)

    # -- Partnerdatei ----------------------------------------------------------------------
    def partner_zeilen(self, system: str, ids: list[str]) -> list[dict]:
        zeilen = []
        alt_adr = self.adr[~self.adr["ist_aktuell"]].drop_duplicates("partner_id", keep="last").set_index("partner_id")
        akt_adr = self.adr[self.adr["ist_aktuell"]].drop_duplicates("partner_id").set_index("partner_id")
        email = self.kontakt[self.kontakt["kontakt_typ"] == "EMAIL"].drop_duplicates("partner_id").set_index("partner_id")["wert"]
        tel = self.kontakt[self.kontakt["kontakt_typ"].isin(["TELEFON", "MOBIL"])].drop_duplicates("partner_id").set_index("partner_id")["wert"]
        for k, pid in enumerate(ids, start=1):
            p = self.partner.loc[pid]
            rng = self.ctx.rng(f"legacy.{system}.partner", pid)
            nr = legacy_partnernummer(system, k)
            ist_dublette_system = pid in self._andere_system_ids and system == "VERA"
            # DQ-01: Dublette zwischen HAPO und VERA mit abweichender Schreibweise / alter Adresse
            variante = ist_dublette_system and rng.random() < self.rate("DQ-01", 0.35)
            if p["partner_typ"] == "JURISTISCH":
                name1 = translit_upper(str(p["firmenname"]))[:30]
                name2 = translit_upper(str(p["rechtsform"] or ""))[:30]
                geb = "00000000"
                geschl, zivst = "0", "0"
            else:
                vorname, nachname = str(p["vorname"]), str(p["nachname"])
                if variante and "-" in nachname:
                    nachname = nachname.split("-")[0]
                elif variante and rng.random() < 0.5:
                    vorname = vorname[:1] + "."
                name1, name2, _ = kuerze_name(vorname, nachname, rng, self.dq, system, nr, self.rate("DQ-04", 0.06))
                if rng.random() < self.rate("DQ-03_mojibake", 0.04):
                    alt = name1
                    name1 = mojibake(name1, rng)
                    if name1 != alt:
                        self.dq.notiere(system, "PARTNER", nr, "NAME1", "DQ-03", alt, name1)
                geb = datum_int(p["geburtsdatum"])
                if rng.random() < self.rate("DQ-05_geburtsdatum", 0.05):
                    alt = geb
                    geb = str(rng.choice(["00000000", "19000101"]))
                    self.dq.notiere(system, "PARTNER", nr, "GEBDAT", "DQ-05", alt, geb)
                geschl = PVS_GESCHLECHT.get(str(p["geschlecht"]), "0")
                zivst = PVS_ZIVILSTAND.get(str(p["zivilstand"]), "0")
                if rng.random() < self.rate("DQ-26_anrede", 0.01):
                    alt = geschl
                    geschl = "2" if geschl == "1" else "1"
                    self.dq.notiere(system, "PARTNER", nr, "GESCHL", "DQ-26", alt, geschl)
            a = akt_adr.loc[pid] if pid in akt_adr.index else None
            if variante and pid in alt_adr.index:
                a = alt_adr.loc[pid]
                self.dq.notiere(system, "PARTNER", nr, "ADR1", "DQ-01", "aktuelle Adresse", "alte Adresse (Dublette)")
            verrutscht = rng.random() < self.rate("DQ-13_verrutscht", 0.10)
            if a is not None:
                adr1, adr2, adr3 = adresse_freitext(a["strasse"], a["hausnummer"], a["plz"], a["ort"], rng, verrutscht)
                if verrutscht:
                    self.dq.notiere(system, "PARTNER", nr, "ADR2", "DQ-13", "", adr2)
                if rng.random() < self.rate("DQ-27", 0.02):
                    alt = adr3
                    adr3 = translit_upper(f"{a['plz']} {a['ort'][:-1] if len(a['ort']) > 4 else a['ort']}X")
                    self.dq.notiere(system, "PARTNER", nr, "ADR3", "DQ-27", alt, adr3)
                landkz = PVS_LANDKZ.get(str(a["land"]), "756")
            else:
                adr1 = adr2 = adr3 = ""
                landkz = PVS_LANDKZ.get(str(p["land_wohnsitz"]), "756")
            mail = str(email.get(pid, ""))
            if mail and rng.random() < self.rate("DQ-06_email", 0.55):
                self.dq.notiere(system, "PARTNER", nr, "EMAIL", "DQ-06", mail, "")
                mail = ""
            telefon = str(tel.get(pid, ""))
            if telefon and rng.random() < self.rate("DQ-06_telefon", 0.20):
                self.dq.notiere(system, "PARTNER", nr, "TEL", "DQ-06", telefon, "")
                telefon = ""
            bem = ""
            if p["status"] == "VERSTORBEN":
                bem = f"VERST. {datum_kurz(p['todesdatum'])}"
                if rng.random() < self.rate("DQ-26_verstorben", 0.005):
                    self.dq.notiere(system, "PARTNER", nr, "BEMERK", "DQ-26", bem, "")
                    bem = ""
            elif rng.random() < 0.08:
                bem = bemerk(str(rng.choice(["VN tel. angefr., RR bis 15.3.", "Adr. lt. Post geaendert", "Kunde wuenscht keine Werbung",
                                             "Rueckruf erbeten", "Mahnung 1 versandt", "Dublette? s. PVS-L"])))
            zeilen.append({"PARTNR": nr, "NAME1": name1, "NAME2": name2, "GEBDAT": geb, "GESCHL": geschl, "ZIVST": zivst, "ADR1": adr1, "ADR2": adr2,
                           "ADR3": adr3, "LANDKZ": landkz, "SPRACHE": SPRACHE_CODE.get(str(p["sprache"]), "D"), "TEL": telefon[:16], "EMAIL": mail[:40],
                           "BERUF": translit_upper(str(p["beruf_text"]).split(" / ")[0])[:20] if pd.notna(p["beruf_text"]) else "",
                           "KDSEIT": datum_int(p["kunde_seit"]) if pd.notna(p["kunde_seit"]) else "00000000",
                           "AENDDAT": datum_int(self.stichtag if rng.random() < 0.3 else date(int(rng.integers(2015, 2025)), int(rng.integers(1, 13)), 1)),
                           "BEMERK": bem, "_pid": pid})
            self.xref_partner.append({"curated_id": pid, "quellsystem": system, "quell_id": nr, "match_methode": "MIGRATIONSLOG" if not variante else "PROBABILISTISCH",
                                      "match_score": 1.0 if not variante else round(float(rng.uniform(0.82, 0.95)), 2),
                                      "gueltig_von": p["kunde_seit"], "gueltig_bis": MIGRATION_DATUM[system],
                                      "bemerkung": "Dublette zu anderem Altsystem, Schreibweise/Adresse abweichend" if variante else ("in beiden Altsystemen" if ist_dublette_system else "")})
        # DQ-02: Dubletten innerhalb des Systems (Umzug -> Neuanlage)
        extra = []
        for z in zeilen:
            rng = self.ctx.rng(f"legacy.{system}.dq02", z["_pid"])
            if rng.random() < self.rate("DQ-02", 0.03) and z["GEBDAT"] != "00000000":
                k = len(zeilen) + len(extra) + 1
                nr = legacy_partnernummer(system, k)
                alt_datum = date(int(rng.integers(2005, 2019)), int(rng.integers(1, 13)), 1)
                d = dict(z, PARTNR=nr, ADR1=translit_upper(f"{str(rng.choice(['Alte', 'Obere', 'Untere']))}{z['ADR1'].split(' ')[0].title()} {int(rng.integers(1, 99))}"),
                         AENDDAT=datum_int(alt_datum), BEMERK="")
                extra.append(d)
                self.dq.notiere(system, "PARTNER", nr, "PARTNR", "DQ-02", z["PARTNR"], nr)
                self.xref_partner.append({"curated_id": z["_pid"], "quellsystem": system, "quell_id": nr, "match_methode": "PROBABILISTISCH",
                                          "match_score": round(float(rng.uniform(0.7, 0.9)), 2), "gueltig_von": None, "gueltig_bis": alt_datum,
                                          "bemerkung": "Dublette innerhalb des Systems nach Umzug"})
        return zeilen + extra

    # -- Vertragsdatei ------------------------------------------------------------------------
    def vertrag_zeilen(self, system: str, partnr: dict[str, str]) -> list[dict]:
        v = self.vertrag[self.vertrag["quellsystem"] == system].sort_values("vertrag_id")
        zeilen = []
        for k, (_, r) in enumerate(v.iterrows(), start=1):
            rng = self.ctx.rng(f"legacy.{system}.vertrag", r["vertrag_id"])
            nr = hapo_vertragsnummer(40_000_000 + k) if system == "HAPO" else vera_vertragsnummer(k)
            migriert = pd.notna(r["migriert_am"])
            status = PVS_STATUS.get(str(r["status"]), "A")
            stornogrd = PVS_STORNOGRUND.get(str(r["status"]), "  ") if status == "S" else "  "
            stornodat = datum_int(r["storno_datum"]) if pd.notna(r["storno_datum"]) else "00000000"
            aenddat = datum_int(r["storno_datum"]) if pd.notna(r["storno_datum"]) else datum_int(r["beginn"])
            if migriert and (status == "A" or (pd.notna(r["storno_datum"]) and r["storno_datum"] >= date(2025, 1, 1))):
                # DQ-25 / DQ-08: Migrationsstorno ZZ; Ereignisse nach dem Snapshot fehlen im Extrakt
                status, stornogrd = "S", "ZZ"
                stornodat = datum_int(MIGRATION_DATUM[system])
                aenddat = stornodat
            enddat = datum_int(r["ablauf"]) if pd.notna(r["ablauf"]) else "99991231"
            vermnr = self.vermittler.loc[r["vermittler_id"]]["vermittlernummer"] if pd.notna(r["vermittler_id"]) and r["vermittler_id"] in self.vermittler.index else "00000"
            vermnr_alt = self.vermittler.loc[r["vermittler_id"]]["vermittlernummer_alt"] if vermnr != "00000" else ""
            if rng.random() < self.rate("DQ-11", 0.07) and vermnr_alt:
                self.dq.notiere(system, "VERTRAG", nr, "VERMNR", "DQ-11", vermnr, vermnr_alt)
                vermnr, vermnr_alt = vermnr_alt, ""
            ris = self.risiko.loc[r["vertrag_id"]] if r["vertrag_id"] in self.risiko.index else None
            if system == "HAPO":
                sparte = HAPO_SPARTE.get(str(r["produkt_id"]), "10")
                tarif = HAPO_GEN.get(str(r["tarifgeneration_id"]), "PFM-M")
                bausteine = self.deckung[(self.deckung["vertrag_id"] == r["vertrag_id"]) & (self.deckung["deckungsart"] == "BAUSTEIN")]["baustein"].tolist()
                zusatz1 = "HUND" if "BS-TIER-HUND" in bausteine else ""
                if zusatz1 and rng.random() < 0.6:
                    zusatz1 = str(rng.choice(["HUND", "HUND LABRAD", "HUND MISCHL", "HUND 2X", "hund"]))
                zusatz2 = "/".join(b.replace("BS-", "")[:3] for b in bausteine if b != "BS-TIER-HUND")[:10]
            else:
                sparte = VERA_PRODUKT.get(str(r["produkt_id"]), "K") + "1"
                tarif = VERA_TARIFCODE.get(str(r["tarifgeneration_id"]), "L17")
                raucher = ris["raucher_angabe"] if ris is not None and pd.notna(ris.get("raucher_angabe")) else None
                zusatz1 = "J" if raucher else ("N" if raucher is False else " ")
                zusatz2 = f"BMI{int(ris['bmi_angabe'])}" if ris is not None and pd.notna(ris.get("bmi_angabe")) else ""
            bem = ""
            if rng.random() < 0.12:
                bem = bemerk(str(rng.choice(["Praemie lt. Nachtrag 01", "VN tel. angefr., RR bis 15.3.", "Mahnung 2 versandt", "Kuendigung erhalten, Frist prüfen",
                                             "Adressaenderung 01/23", "Baustein Hund nachgemeldet", "Deckung ruht", "Sanierung UW"])))
            if rng.random() < self.rate("DQ-15", 0.005):
                bem = bem + "\nRUECKRUF ERBETEN"
                self.dq.notiere(system, "VERTRAG", nr, "BEMERK", "DQ-15", bem.replace("\n", " "), "Zeilenumbruch")
            zeilen.append({"VERTRNR": nr, "PARTNR": partnr.get(r["versicherungsnehmer_id"], "00000000"), "SPARTE": sparte, "TARIF": tarif,
                           "BEGDAT": datum_int(r["beginn"]), "ENDDAT": enddat, "PRAEM": rappen(r["jahrespraemie_brutto"]),
                           "ZAHLWS": PVS_ZAHLWEISE.get(str(r["zahlungsweise"]), "1"), "STATUS": status, "STORNOGRD": stornogrd, "STORNODAT": stornodat,
                           "LANDKZ": PVS_LANDKZ.get(str(r["markt"]), "756"), "VERMNR": vermnr, "VERMNR_ALT": vermnr_alt or "",
                           "SUMME": rappen(r["versicherungssumme"]), "ZUSATZ1": zusatz1, "ZUSATZ2": zusatz2, "AENDDAT": aenddat, "BEMERK": bem,
                           "_vid": r["vertrag_id"], "_migriert": migriert, "_bausteine": len(bausteine) if system == "HAPO" else 0})
            self.xref_vertrag.append({"curated_id": r["vertrag_id"], "quellsystem": system, "quell_id": nr, "match_methode": "MIGRATIONSLOG" if migriert else "DIREKT",
                                      "match_score": 1.0, "gueltig_von": r["beginn"], "gueltig_bis": MIGRATION_DATUM[system] if migriert else r["storno_datum"],
                                      "bemerkung": "Migrationsstorno ZZ im Altsystem" if stornogrd == "ZZ" else ""})
        return zeilen

    # -- Migrationslog ---------------------------------------------------------------------
    def migrationslog(self, system: str, pz: list[dict], vz: list[dict]) -> None:
        welle = "HP-2025-Q2" if system == "HAPO" else "LV-2025-Q4"
        for z in pz:
            rng = self.ctx.rng(f"migration.{system}.partner", z["PARTNR"])
            erg, text = "OK", "Partner uebernommen"
            if z["GEBDAT"] in ("00000000", "19000101"):
                erg, text = "WARN", "Geburtsdatum Platzhalter, Dummy 1900-01-01 gesetzt"
            elif "Ã" in z["NAME1"]:
                erg, text = "WARN", "Zeichensatzfehler im Namen, manuelle Korrektur erforderlich"
            elif rng.random() < 0.01:
                erg, text = "ERROR", "Adresse nicht parsebar, Partner ohne Adresse angelegt"
            self.log.append({"welle": welle, "objekttyp": "PARTNER", "quellsystem": system, "quell_id": z["PARTNR"], "ziel_id": z["_pid"],
                             "zeitpunkt": MIGRATION_DATUM[system], "ergebnis": erg, "meldung": text})
        for z in vz:
            if not z["_migriert"]:
                continue
            rng = self.ctx.rng(f"migration.{system}.vertrag", z["VERTRNR"])
            erg, text = "OK", "Vertrag uebernommen"
            if system == "HAPO" and z["_bausteine"] > 0 and rng.random() < 0.03:
                erg, text = "WARN", "Bausteincode BST nicht im Zielschema, Feld leer uebernommen"
            elif z["STORNOGRD"] == "ZZ" and rng.random() < 0.005:
                erg, text = "ERROR", "Migrationsstorno ohne Zielvertrag (manuelle Nacharbeit)"
            elif rng.random() < 0.02:
                erg, text = "WARN", "Praemie mit Rundungsdifferenz (Rappen/Cent) uebernommen"
            self.log.append({"welle": welle, "objekttyp": "VERTRAG", "quellsystem": system, "quell_id": z["VERTRNR"], "ziel_id": z["_vid"],
                             "zeitpunkt": MIGRATION_DATUM[system], "ergebnis": erg, "meldung": text})

    # -- Dateien -------------------------------------------------------------------------------
    def schreibe(self, system: str, art: str, felder: list[tuple[str, int]], zeilen: list[dict]) -> list:
        ordner = self.ctx.ausgabe_dir("raw") / "pvs"
        ordner.mkdir(parents=True, exist_ok=True)
        pfade = []
        # Fixed-width (DQ-14: Trailing Spaces)
        txt = ordner / f"{system}_{art}.txt"
        with txt.open("w", encoding="iso-8859-1", errors="replace", newline="\r\n") as fh:
            for z in zeilen:
                fh.write("".join(fixed(z.get(name, ""), breite) for name, breite in felder) + "\n")
        pfade.append(txt)
        # Semikolon-CSV Reporting-Extrakt: Datum DD.MM.YY, fuehrende Nullen verloren (DQ-14), ohne Quoting (DQ-15)
        csv = ordner / f"{system}_{art}.csv"
        rng = self.ctx.rng(f"legacy.{system}.csv", art)
        nullen = rng.random() < self.rate("DQ-14_nullen", 0.30) or True
        with csv.open("w", encoding="iso-8859-1", errors="replace", newline="") as fh:
            fh.write(";".join(name for name, _ in felder) + "\r\n")
            for z in zeilen:
                werte = []
                for name, _ in felder:
                    w = str(z.get(name, "") or "")
                    if name.endswith("DAT") or name == "KDSEIT":
                        w = "" if w in ("00000000", "99991231") else f"{w[6:8]}.{w[4:6]}.{w[2:4]}" if len(w) == 8 else w
                    if name in ("PARTNR", "VERMNR") and nullen:
                        w = w.lstrip("0") or "0"
                    werte.append(w)
                fh.write(";".join(werte) + "\r\n")
        pfade.append(csv)
        satzbeschreibung = ordner / f"{system}_{art}_SATZART.txt"
        with satzbeschreibung.open("w", encoding="iso-8859-1") as fh:
            fh.write(f"SATZART {system} {art}  STAND {datum_int(self.stichtag)}  ZEICHENSATZ ISO-8859-1\n")
            pos = 1
            for name, breite in felder:
                fh.write(f"{name:<12}POS {pos:>4} LEN {breite:>3}\n")
                pos += breite
        pfade.append(satzbeschreibung)
        return pfade

    def run(self) -> dict:
        hapo_ids = set(self.partner_je_system("HAPO"))
        vera_ids = set(self.partner_je_system("VERA"))
        self._andere_system_ids = hapo_ids & vera_ids
        dateien = []
        anz = {}
        for system, ids in (("HAPO", sorted(hapo_ids)), ("VERA", sorted(vera_ids))):
            pz = self.partner_zeilen(system, ids)
            partnr = {z["_pid"]: z["PARTNR"] for z in pz}
            vz = self.vertrag_zeilen(system, partnr)
            self.migrationslog(system, pz, vz)
            dateien += self.schreibe(system, "PARTNER", PARTNER_FELDER, pz)
            dateien += self.schreibe(system, "VERTRAG", VERTRAG_FELDER, vz)
            anz[system] = (len(pz), len(vz))
        for pfad in dateien:
            if self.ctx.manifest is not None:
                self.ctx.manifest.add_datei(_relativ(pfad, self.ctx.root), sha256_datei(pfad))
        return anz


@register
class LegacyifyStage(Stage):
    name, nummer, welle = "legacyify", 90, 1
    beschreibung = "raw VERA/HAPO mit DQ-Injektion, Migrationslog, xref"

    def run(self, ctx: RunContext) -> None:
        if not ctx.tabellen.has("vertrag"):
            self.stub(ctx)
            return
        lg = Legacy(ctx)
        anz = lg.run()
        ctx.tabellen.register("partner_xref", pd.DataFrame(lg.xref_partner), layer="migration", ersetzen=True)
        ctx.tabellen.register("vertrag_xref", pd.DataFrame(lg.xref_vertrag), layer="migration", ersetzen=True)
        ctx.tabellen.register("migrationslog", pd.DataFrame(lg.log), layer="migration", ersetzen=True)
        vorhanden = ctx.tabellen.get("dq_injektionen", "truth") if ctx.tabellen.has("dq_injektionen", "truth") else pd.DataFrame()
        ctx.tabellen.register("dq_injektionen", pd.concat([vorhanden, pd.DataFrame(lg.dq.eintraege)], ignore_index=True), layer="truth", ersetzen=True)
        ctx.ereignis(self.name, "; ".join(f"{s}: {p} Partner, {v} Vertraege" for s, (p, v) in anz.items()) + f"; {len(lg.dq.eintraege)} DQ-Injektionen")


__all__ = ["LegacyifyStage", "Legacy", "np"]
