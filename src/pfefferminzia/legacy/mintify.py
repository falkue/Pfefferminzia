"""Stufe ``mintify``: Rohextrakt der Minzia-Plattform MINT als JSON Lines (Datenarchitektur 2.1, 2.2).

``raw/<stufe>/mint/customers.jsonl`` und ``policies.jsonl``: ein Objekt je Zeile, Schema-Drift v1/v2/v3
nach Erstellungsdatum (DQ-16), Missing-Value-Varianten (DQ-17), Registrierungsdubletten (DQ-18),
Testdaten (DQ-19), Zeitzonenmix (DQ-20), Freitextberufe (DQ-21), Boolean-Varianten (DQ-22),
Float-Rundung in v1 (DQ-23), Migrationsartefakte ``legacyAttributes`` (DQ-24).
"""

from __future__ import annotations

import json
from datetime import date, datetime, timedelta

import pandas as pd

from pfefferminzia.context import RunContext
from pfefferminzia.export import _relativ
from pfefferminzia.ids import mint_policennummer, mint_uuid
from pfefferminzia.legacy.dq import DqProtokoll
from pfefferminzia.manifest import sha256_datei
from pfefferminzia.pipeline import Stage, register
from pfefferminzia.synth.referenz_intern import BERUF_FREITEXT, MINT_STATUS_V1, MINT_STATUS_V2, MINT_STATUS_V3

PRODUKT_MINT = {"HP-PRIV": "private_liability", "HP-BETR": "business_liability", "HP-BERUF": "professional_liability",
                "LV-RISK": "term_life", "LV-VORS": "endowment_life", "LV-RENTE": "annuity", "LV-EU": "disability_rider"}
GENDER = {"v1": {"M": "male", "W": "female", "D": "diverse", "UNBEKANNT": None}, "v2": {"M": "MALE", "W": "FEMALE", "D": "DIVERSE", "UNBEKANNT": "UNKNOWN"},
          "v3": {"M": "MALE", "W": "FEMALE", "D": "DIVERSE", "UNBEKANNT": "UNKNOWN"}}
FREQ = {"JAEHRLICH": "yearly", "HALBJAEHRLICH": "half_yearly", "VIERTELJAEHRLICH": "quarterly", "MONATLICH": "monthly"}


def _sauber(o):
    """Ersetzt NaN/NaT/pandas-Nullwerte rekursiv durch None (JSON-konform)."""
    if isinstance(o, dict):
        return {k: _sauber(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_sauber(v) for v in o]
    if isinstance(o, float) and o != o:
        return None
    try:
        if o is not None and not isinstance(o, (str, int, float, bool, list, dict)) and pd.isna(o):
            return None
    except (TypeError, ValueError):
        pass
    return o


def schema_version(d: date) -> str:
    if d < date(2020, 7, 1):
        return "v1"
    if d < date(2023, 1, 1):
        return "v2"
    return "v3"


def ts(d: date | datetime, rng, naiv_rate: float, dq: DqProtokoll | None = None, oid: str = "", feld: str = "") -> str:
    """ISO-Zeitstempel; mit Rate ``naiv_rate`` ohne Zeitzone (Europe/Berlin-Lokalzeit, DQ-20)."""
    if isinstance(d, date) and not isinstance(d, datetime):
        d = datetime(d.year, d.month, d.day, int(rng.integers(7, 20)), int(rng.integers(0, 60)), int(rng.integers(0, 60)))
    if rng.random() < naiv_rate:
        if dq is not None:
            dq.notiere("MINT", "customers", oid, feld, "DQ-20", d.isoformat() + "Z", d.isoformat())
        return d.isoformat()
    return d.isoformat() + "Z"


def missing(rng, wert, rate: float):
    """DQ-17: null, fehlendes Feld (Marker), leerer String oder 'n/a'."""
    if wert is None or rng.random() >= rate:
        return wert, False
    return str(rng.choice(["", "n/a", "__MISSING__", "null"])), True


def boolean(rng, wert: bool, rate: float):
    if rng.random() < rate:
        return str(rng.choice(["yes", "Y", "1", "true"])) if wert else str(rng.choice(["no", "N", "0", "false"]))
    return bool(wert)


class Mint:
    def __init__(self, ctx: RunContext):
        self.ctx = ctx
        self.r = ctx.config.dq.raten
        self.aktiv = ctx.config.dq.aktiv
        self.dq = DqProtokoll()
        t = ctx.tabellen
        self.partner = t.get("partner")
        self.adr = t.get("partner_adresse")
        self.kontakt = t.get("partner_kontakt")
        self.vertrag = t.get("vertrag")
        self.deckung = t.get("deckung")
        self.vermittler = t.get("vermittler").set_index("vermittler_id")
        self.xref_p = t.get("partner_xref", "migration") if t.has("partner_xref", "migration") else pd.DataFrame(columns=["curated_id", "quellsystem", "quell_id"])
        self.xref_v = t.get("vertrag_xref", "migration") if t.has("vertrag_xref", "migration") else pd.DataFrame(columns=["curated_id", "quellsystem", "quell_id"])
        self.xref_neu: list[dict] = []
        self.stichtag = ctx.config.zeit.stichtag

    def rate(self, regel: str, default: float) -> float:
        return float(self.r.get(regel, default)) if self.aktiv else 0.0

    def kunden(self) -> tuple[list[dict], dict[str, str]]:
        v = self.vertrag
        mint_native = set(v[(v["quellsystem"] == "MINT")]["versicherungsnehmer_id"])
        migriert = set(v[v["migriert_am"].notna()]["versicherungsnehmer_id"])
        ids = sorted(mint_native | migriert)
        akt = self.adr[self.adr["ist_aktuell"]].drop_duplicates("partner_id").set_index("partner_id")
        email = self.kontakt[self.kontakt["kontakt_typ"] == "EMAIL"].drop_duplicates("partner_id").set_index("partner_id")["wert"]
        tel = self.kontakt[self.kontakt["kontakt_typ"].isin(["TELEFON", "MOBIL"])].drop_duplicates("partner_id").set_index("partner_id")["wert"]
        legacy = {(r["curated_id"], r["quellsystem"]): r["quell_id"] for _, r in self.xref_p.iterrows()}
        p = self.partner.set_index("partner_id")
        objekte, cid_von = [], {}
        for pid in ids:
            z = p.loc[pid]
            rng = self.ctx.rng("mint.customer", pid)
            cid = mint_uuid("customer", pid, self.ctx.master_seed)
            cid_von[pid] = cid
            ist_migriert = pid in migriert and pid not in mint_native
            erstellt = self.stichtag if ist_migriert else (z["kunde_seit"] if pd.notna(z["kunde_seit"]) else date(2021, 6, 1))
            if ist_migriert:
                erstellt = min(d for d in (date(2025, 5, 15), date(2025, 11, 15)))
            version = "v3" if ist_migriert else schema_version(erstellt)
            a = akt.loc[pid] if pid in akt.index else None
            mail, _ = missing(rng, str(email.get(pid, "")) or None, self.rate("DQ-17", 0.10))
            telefon, _ = missing(rng, str(tel.get(pid, "")) or None, self.rate("DQ-17", 0.10))
            beruf = str(z["beruf_text"] or "")
            if z["beruf_code"] in BERUF_FREITEXT and rng.random() < self.rate("DQ-21", 0.60) and not ist_migriert:
                alt = beruf
                beruf = str(rng.choice(BERUF_FREITEXT[z["beruf_code"]]))
                self.dq.notiere("MINT", "customers", cid, "occupation", "DQ-21", alt, beruf)
            geb = z["geburtsdatum"].isoformat() if pd.notna(z["geburtsdatum"]) else None
            adresse = None if a is None else {"street": a["strasse"], "houseNumber": str(a["hausnummer"]), "postalCode": str(a["plz"]), "city": a["ort"],
                                              "countryCode": a["land"]}
            if adresse and rng.random() < 0.03 and not ist_migriert:
                alt = adresse["city"]
                adresse["city"] = alt.replace("ü", "u").replace("ch", "h") if any(c in alt for c in "üch") else alt.lower()
                self.dq.notiere("MINT", "customers", cid, "address.city", "DQ-13", alt, adresse["city"])
            if version == "v1":
                obj = {"schemaVersion": "v1", "customerId": cid, "firstName": z["vorname"] if z["partner_typ"] == "NATUERLICH" else z["firmenname"],
                       "lastName": z["nachname"] if z["partner_typ"] == "NATUERLICH" else "", "gender": GENDER["v1"].get(str(z["geschlecht"])),
                       "birthDate": geb, "email": mail, "phone": telefon, "address": adresse, "occupation": beruf,
                       "createdAt": ts(erstellt, rng, self.rate("DQ-20", 0.15), self.dq, cid, "createdAt"), "status": "active" if z["status"] == "AKTIV" else "inactive"}
            elif version == "v2":
                obj = {"schemaVersion": "v2", "customerId": cid, "name": {"first": z["vorname"], "last": z["nachname"]} if z["partner_typ"] == "NATUERLICH" else {"company": z["firmenname"], "legalForm": z["rechtsform"]},
                       "gender": GENDER["v2"].get(str(z["geschlecht"])), "dateOfBirth": geb, "contact": {"email": mail, "mobile": telefon},
                       "address": adresse, "occupationText": beruf, "consents": {"marketing": boolean(rng, bool(z["datenschutz_werbung_ok"]), self.rate("DQ-22", 0.05)),
                                                                                  "aiProcessing": boolean(rng, bool(z["datenschutz_ki_ok"]), self.rate("DQ-22", 0.05))},
                       "createdAt": ts(erstellt, rng, self.rate("DQ-20", 0.15), self.dq, cid, "createdAt"), "status": "ACTIVE" if z["status"] == "AKTIV" else "INACTIVE"}
            else:
                geb3 = geb
                legacy_attr = None
                if ist_migriert:
                    legacy_attr = {"PARTNR_HAPO": legacy.get((pid, "HAPO")), "PARTNR_VERA": legacy.get((pid, "VERA")),
                                   "GESCHL": {"M": "1", "W": "2"}.get(str(z["geschlecht"]), "0"), "SPRACHE": str(z["sprache"])[:1].upper(),
                                   "BEMERK": "MIGR " + ("HP-2025-Q2" if legacy.get((pid, "HAPO")) else "LV-2025-Q4")}
                    if geb3 is None or rng.random() < 0.03:
                        geb3 = "1900-01-01"  # DQ-24 Dummy
                        self.dq.notiere("MINT", "customers", cid, "person.birthDate", "DQ-24", geb, geb3)
                obj = {"schemaVersion": "v3", "id": cid,
                       "person": ({"givenName": z["vorname"], "familyName": z["nachname"], "gender": GENDER["v3"].get(str(z["geschlecht"])), "birthDate": geb3,
                                   "title": z["titel"]} if z["partner_typ"] == "NATUERLICH" else None),
                       "organization": ({"name": z["firmenname"], "legalForm": z["rechtsform"], "registrationId": z["uid_hrb_nummer"]} if z["partner_typ"] == "JURISTISCH" else None),
                       "contacts": [c for c in ({"type": "EMAIL", "value": mail} if mail else None, {"type": "PHONE", "value": telefon} if telefon else None) if c],
                       "addresses": [dict(adresse, type="HOME", validFrom=str(a["gueltig_von"]))] if adresse else [],
                       "language": str(z["sprache"]).upper(), "segment": str(z["kundensegment"]),
                       "lifecycle": {"state": {"AKTIV": "ACTIVE", "INAKTIV": "INACTIVE", "VERSTORBEN": "DECEASED"}.get(str(z["status"]), "ACTIVE")},
                       "consents": {"marketing": boolean(rng, bool(z["datenschutz_werbung_ok"]), self.rate("DQ-22", 0.05)),
                                    "aiProcessing": boolean(rng, bool(z["datenschutz_ki_ok"]), self.rate("DQ-22", 0.05))},
                       "source": "MIGRATION" if ist_migriert else str(rng.choice(["WEB", "APP", "BROKER_API"], p=[0.5, 0.4, 0.1])),
                       "createdAt": ts(erstellt, rng, self.rate("DQ-20", 0.15), self.dq, cid, "createdAt"),
                       "legacyAttributes": legacy_attr}
            objekte.append({k: v for k, v in obj.items() if v != "__MISSING__"})
            self.xref_neu.append({"curated_id": pid, "quellsystem": "MINT", "quell_id": cid, "match_methode": "MIGRATIONSLOG" if ist_migriert else "DIREKT",
                                  "match_score": 1.0, "gueltig_von": erstellt, "gueltig_bis": None, "bemerkung": "migriert" if ist_migriert else ""})
            # DQ-18: Registrierungsdublette (zweites Konto mit anderer E-Mail)
            if not ist_migriert and z["partner_typ"] == "NATUERLICH" and rng.random() < self.rate("DQ-18", 0.04):
                cid2 = mint_uuid("customer.dup", pid, self.ctx.master_seed)
                dup = dict(obj)
                dup[("customerId" if version != "v3" else "id")] = cid2
                mail2 = (mail or "kunde").split("@")[0] + f".{int(rng.integers(1, 99))}@{str(rng.choice(['web', 'mail', 'post']))}.example"
                if version == "v1":
                    dup["email"] = mail2
                    dup["firstName"] = str(dup["firstName"]).lower()
                elif version == "v2":
                    dup["contact"] = {"email": mail2, "mobile": telefon}
                else:
                    dup["contacts"] = [{"type": "EMAIL", "value": mail2}]
                    dup["person"] = dict(dup["person"], givenName=str(dup["person"]["givenName"]).strip().lower()) if dup.get("person") else None
                objekte.append(dup)
                self.dq.notiere("MINT", "customers", cid2, "email", "DQ-18", mail, mail2)
                self.xref_neu.append({"curated_id": pid, "quellsystem": "MINT", "quell_id": cid2, "match_methode": "PROBABILISTISCH", "match_score": 0.88,
                                      "gueltig_von": erstellt, "gueltig_bis": None, "bemerkung": "Registrierungsdublette"})
            # DQ-19: Testdaten in Produktion
            if not ist_migriert and rng.random() < self.rate("DQ-19", 0.003):
                cidt = mint_uuid("customer.test", pid, self.ctx.master_seed)
                objekte.append({"schemaVersion": version, ("customerId" if version != "v3" else "id"): cidt, "firstName": "Test", "lastName": "Tester",
                                "email": "test@qa.example", "birthDate": "2000-01-01", "createdAt": ts(erstellt, rng, 0.0), "status": "active"})
                self.dq.notiere("MINT", "customers", cidt, "*", "DQ-19", "", "Test Tester")
        return objekte, cid_von

    def policen(self, cid_von: dict[str, str]) -> list[dict]:
        v = self.vertrag[(self.vertrag["quellsystem"] == "MINT") | self.vertrag["migriert_am"].notna()].sort_values("vertrag_id")
        legacy_v = {(r["curated_id"], r["quellsystem"]): r["quell_id"] for _, r in self.xref_v.iterrows()}
        objekte = []
        for k, (_, r) in enumerate(v.iterrows(), start=1):
            rng = self.ctx.rng("mint.policy", r["vertrag_id"])
            pid = mint_uuid("policy", r["vertrag_id"], self.ctx.master_seed)
            migriert = pd.notna(r["migriert_am"])
            erstellt = r["migriert_am"] if migriert else r["erstellt_am"]
            version = "v3" if migriert else schema_version(erstellt)
            status_map = {"v1": MINT_STATUS_V1, "v2": MINT_STATUS_V2, "v3": MINT_STATUS_V3}[version]
            deck = self.deckung[self.deckung["vertrag_id"] == r["vertrag_id"]]
            coverages = [{"type": "MAIN" if d["deckungsart"] == "HAUPTDECKUNG" else ("RIDER" if d["deckungsart"] == "ZUSATZ" else "ADDON"),
                          "code": d["baustein"], "sumInsured": float(d["summe"]) if pd.notna(d["summe"]) else None,
                          "deductible": float(d["selbstbehalt"]) if pd.notna(d["selbstbehalt"]) else None} for _, d in deck.iterrows()]
            betrag = float(r["jahrespraemie_brutto"])
            if version == "v1":
                praemie = {"amount": betrag + (float(rng.uniform(-0.0000009, 0.0000009)) if rng.random() < 0.7 else 0.0), "currency": r["waehrung"]}
                if praemie["amount"] != betrag:
                    self.dq.notiere("MINT", "policies", pid, "premium.amount", "DQ-23", betrag, praemie["amount"])
            else:
                praemie = {"amount": f"{betrag:.2f}", "currency": r["waehrung"]}
            agent = None if pd.isna(r["vermittler_id"]) or r["kanal"] == "direkt" else mint_uuid("agent", r["vermittler_id"], self.ctx.master_seed)
            basis = {"schemaVersion": version, "policyId": pid, "policyNumber": mint_policennummer(erstellt.year, k),
                     "customerId": cid_von.get(r["versicherungsnehmer_id"]), "product": PRODUKT_MINT.get(str(r["produkt_id"])),
                     "tariffGeneration": r["tarifgeneration_id"], "market": r["markt"], "effectiveDate": r["beginn"].isoformat(),
                     "expiryDate": r["ablauf"].isoformat() if pd.notna(r["ablauf"]) else None, "premium": praemie,
                     "paymentFrequency": FREQ.get(str(r["zahlungsweise"]), "yearly"), "channel": "web" if r["kanal"] == "direkt" else str(r["kanal"]).upper(),
                     "agentId": agent, "coverages": coverages, "createdAt": ts(erstellt, rng, self.rate("DQ-20", 0.15))}
            if version == "v3":
                basis["lifecycle"] = {"state": status_map.get(str(r["status"]), "ACTIVE"), "since": r["status_seit"].isoformat(),
                                      "terminationReason": r["storno_grund_code"] if pd.notna(r["storno_grund_code"]) else None}
                if migriert:
                    basis["migration"] = {"source": r["quellsystem"], "migratedAt": r["migriert_am"].isoformat(), "wave": "HP-2025-Q2" if r["quellsystem"] == "HAPO" else "LV-2025-Q4"}
                    basis["legacyAttributes"] = {"VERTRNR": legacy_v.get((r["vertrag_id"], r["quellsystem"])), "SPARTE": {"HP-PRIV": "10", "HP-BETR": "20", "HP-BERUF": "30"}.get(str(r["produkt_id"]), "K1"),
                                                 "STATUS": "S", "STORNOGRD": "ZZ", "ZAHLWS": {"JAEHRLICH": "1", "HALBJAEHRLICH": "2", "VIERTELJAEHRLICH": "4", "MONATLICH": "12"}.get(str(r["zahlungsweise"]), "1")}
                    # Migrationsartefakt: Bausteincode verloren (Fall Pieper), gemaess Migrationslog
                    if rng.random() < 0.03 and any(c["type"] == "ADDON" for c in coverages):
                        basis["coverages"] = [c for c in coverages if c["type"] != "ADDON"]
                        self.dq.notiere("MINT", "policies", pid, "coverages", "DQ-24", str(len(coverages)), str(len(basis["coverages"])))
            else:
                basis["status"] = status_map.get(str(r["status"]), "active")
                if pd.notna(r["storno_datum"]):
                    basis["cancelledAt" if version == "v1" else "terminatedAt"] = r["storno_datum"].isoformat()
            objekte.append(basis)
            self.xref_neu.append({"curated_id": r["vertrag_id"], "quellsystem": "MINT", "quell_id": pid, "match_methode": "MIGRATIONSLOG" if migriert else "DIREKT",
                                  "match_score": 1.0, "gueltig_von": erstellt, "gueltig_bis": None, "bemerkung": "migriert" if migriert else ""})
        return objekte

    def schreibe(self, name: str, objekte: list[dict]) -> None:
        ordner = self.ctx.ausgabe_dir("raw") / "mint"
        ordner.mkdir(parents=True, exist_ok=True)
        pfad = ordner / f"{name}.jsonl"
        with pfad.open("w", encoding="utf-8") as fh:
            for o in objekte:
                fh.write(json.dumps(_sauber(o), ensure_ascii=False, default=str) + "\n")
        if self.ctx.manifest is not None:
            self.ctx.manifest.add_datei(_relativ(pfad, self.ctx.root), sha256_datei(pfad))


@register
class MintifyStage(Stage):
    name, nummer, welle = "mintify", 91, 1
    beschreibung = "raw MINT (JSONL, Schema-Drift, Migrationsartefakte)"

    def run(self, ctx: RunContext) -> None:
        if not ctx.tabellen.has("vertrag"):
            self.stub(ctx)
            return
        m = Mint(ctx)
        kunden, cid_von = m.kunden()
        policen = m.policen(cid_von)
        m.schreibe("customers", kunden)
        m.schreibe("policies", policen)
        xp = [x for x in m.xref_neu if x["curated_id"].startswith("PTR")]
        xv = [x for x in m.xref_neu if x["curated_id"].startswith("VTR")]
        for name, neu in (("partner_xref", xp), ("vertrag_xref", xv)):
            alt = ctx.tabellen.get(name, "migration") if ctx.tabellen.has(name, "migration") else pd.DataFrame()
            ctx.tabellen.register(name, pd.concat([alt, pd.DataFrame(neu)], ignore_index=True), layer="migration", ersetzen=True)
        vorhanden = ctx.tabellen.get("dq_injektionen", "truth") if ctx.tabellen.has("dq_injektionen", "truth") else pd.DataFrame()
        ctx.tabellen.register("dq_injektionen", pd.concat([vorhanden, pd.DataFrame(m.dq.eintraege)], ignore_index=True), layer="truth", ersetzen=True)
        ctx.ereignis(self.name, f"MINT: {len(kunden)} customers, {len(policen)} policies, {len(m.dq.eintraege)} DQ-Injektionen")


__all__ = ["MintifyStage", "timedelta"]
