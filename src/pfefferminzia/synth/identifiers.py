"""Fiktive, aber pruefziffernvalide Identifikatoren (Konventionen §1, Entscheidung E10).

* IBAN CH: Clearing 99999 (fiktive "Oltener Kantonalbank"); IBAN DE: BLZ 99999999 ("Spree Volksbank").
* AHV-Nummer: ``756.xxxx.xxxx.xx`` mit EAN-13-Pruefziffer.
* Deutsche Steuer-ID: 11 Stellen, ISO 7064 MOD 11,10, Mehrfachziffer-Regel.
* CH-UID: ``CHE-4xx.xxx.xxx`` mit Modulo-11-Pruefziffer, Bereich CHE-499 als fiktiv dokumentiert.
* Telefon: ausschliesslich Fiktionsbereiche ``+41 44 000 xx xx``, ``+49 30 23125 xxx``, ``+49 152 28817 xxx``.
* E-Mail: nur ``.example``-Domains.
"""

from __future__ import annotations

import re
import unicodedata

import numpy as np

CLEARING_OLTENER_KB = "99999"
BLZ_SPREE_VOLKSBANK = "99999999"
BIC_PFEFFERMINZIA = "PFMZCHZZXXX"
KUNDEN_DOMAINS = ("mail.example", "web.example", "bluemail.example", "post.example")
FIRMEN_DOMAIN_TLD = "example"
UID_FIKTIV_PRAEFIX = "499"

_TRANSLIT = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "æ": "ae", "ø": "oe", "œ": "oe"}


def ascii_handle(text: str) -> str:
    """ASCII-Handle fuer E-Mails/Logins: Umlaute transliteriert, Rest ohne Diakritika, klein."""
    t = text.lower()
    for k, v in _TRANSLIT.items():
        t = t.replace(k, v)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "x"


def _ziffern(rng: np.random.Generator, n: int) -> str:
    return "".join(str(d) for d in rng.integers(0, 10, size=n))


# ---------------------------------------------------------------------------
# IBAN
# ---------------------------------------------------------------------------


def _iban_pruefziffer(land: str, bban: str) -> str:
    umgestellt = bban + land + "00"
    zahl = "".join(str(int(c, 36)) for c in umgestellt)
    return f"{98 - int(zahl) % 97:02d}"


def iban_gueltig(iban: str) -> bool:
    iban = iban.replace(" ", "").upper()
    if not re.match(r"^[A-Z]{2}\d{2}[A-Z0-9]{11,30}$", iban):
        return False
    umgestellt = iban[4:] + iban[:4]
    return int("".join(str(int(c, 36)) for c in umgestellt)) % 97 == 1


def iban_ch(rng: np.random.Generator) -> str:
    """CH-IBAN (21 Stellen) bei der fiktiven Oltener Kantonalbank, Clearing 99999."""
    bban = CLEARING_OLTENER_KB + _ziffern(rng, 12)
    return "CH" + _iban_pruefziffer("CH", bban) + bban


def iban_de(rng: np.random.Generator) -> str:
    """DE-IBAN (22 Stellen) bei der fiktiven Spree Volksbank, BLZ 99999999."""
    bban = BLZ_SPREE_VOLKSBANK + _ziffern(rng, 10)
    return "DE" + _iban_pruefziffer("DE", bban) + bban


def iban_formatiert(iban: str) -> str:
    iban = iban.replace(" ", "")
    return " ".join(iban[i : i + 4] for i in range(0, len(iban), 4))


# ---------------------------------------------------------------------------
# AHV-Nummer (CH)
# ---------------------------------------------------------------------------


def ean13_pruefziffer(zwoelf: str) -> int:
    if len(zwoelf) != 12 or not zwoelf.isdigit():
        raise ValueError("EAN-13 braucht 12 Ziffern")
    summe = sum(int(z) * (1 if i % 2 == 0 else 3) for i, z in enumerate(zwoelf))
    return (10 - summe % 10) % 10


def ahv_nummer(rng: np.random.Generator) -> str:
    """AHV-Nummer ``756.xxxx.xxxx.xx`` mit EAN-13-Pruefziffer; Stammnummer zufaellig (fiktiv)."""
    stamm = "756" + _ziffern(rng, 9)
    voll = stamm + str(ean13_pruefziffer(stamm))
    return f"{voll[:3]}.{voll[3:7]}.{voll[7:11]}.{voll[11:]}"


def ahv_gueltig(nummer: str) -> bool:
    z = nummer.replace(".", "")
    return len(z) == 13 and z.isdigit() and z.startswith("756") and ean13_pruefziffer(z[:12]) == int(z[12])


# ---------------------------------------------------------------------------
# Steuer-ID (DE)
# ---------------------------------------------------------------------------


def steuer_id_pruefziffer(zehn: str) -> int:
    """ISO 7064 MOD 11,10 wie beim BZSt."""
    if len(zehn) != 10 or not zehn.isdigit():
        raise ValueError("Steuer-ID braucht 10 Ziffern vor der Pruefziffer")
    produkt = 10
    for z in zehn:
        summe = (int(z) + produkt) % 10
        if summe == 0:
            summe = 10
        produkt = (summe * 2) % 11
    pz = 11 - produkt
    return 0 if pz == 10 else pz


def _steuer_id_struktur_ok(zehn: str) -> bool:
    """Erste Ziffer != 0; genau eine Ziffer kommt zwei- oder dreimal vor, keine oefter."""
    if zehn[0] == "0":
        return False
    zaehl = {d: zehn.count(d) for d in set(zehn)}
    mehrfach = [d for d, n in zaehl.items() if n > 1]
    return len(mehrfach) == 1 and zaehl[mehrfach[0]] in (2, 3)


def steuer_id(rng: np.random.Generator) -> str:
    """Deutsche Steuer-ID (11 Stellen) mit gueltiger Pruefziffer und Mehrfachziffer-Regel."""
    while True:
        ziffern = list(rng.permutation(10))
        anzahl_doppel = 2 if rng.random() < 0.85 else 3
        basis = ziffern[: 11 - anzahl_doppel]  # 9 bzw. 8 verschiedene Ziffern
        doppel = basis[int(rng.integers(0, len(basis)))]
        werte = basis + [doppel] * (anzahl_doppel - 1)
        werte = [int(v) for v in rng.permutation(werte)]
        zehn = "".join(str(v) for v in werte)
        if _steuer_id_struktur_ok(zehn):
            return zehn + str(steuer_id_pruefziffer(zehn))


def steuer_id_gueltig(nummer: str) -> bool:
    n = nummer.replace(" ", "")
    return (len(n) == 11 and n.isdigit() and _steuer_id_struktur_ok(n[:10])
            and steuer_id_pruefziffer(n[:10]) == int(n[10]))


# ---------------------------------------------------------------------------
# CH-UID
# ---------------------------------------------------------------------------

_UID_GEWICHTE = (5, 4, 3, 2, 7, 6, 5, 4)


def uid_pruefziffer(acht: str) -> int | None:
    """Modulo-11-Pruefziffer der UID; None, wenn keine gueltige Pruefziffer existiert (Rest 1)."""
    if len(acht) != 8 or not acht.isdigit():
        raise ValueError("UID braucht 8 Ziffern vor der Pruefziffer")
    rest = sum(int(z) * g for z, g in zip(acht, _UID_GEWICHTE, strict=True)) % 11
    pz = 11 - rest
    if pz == 11:
        return 0
    if pz == 10:
        return None
    return pz


def che_uid(rng: np.random.Generator) -> str:
    """UID ``CHE-499.xxx.xxx`` (fiktiver Bereich) mit gueltiger Pruefziffer."""
    while True:
        acht = UID_FIKTIV_PRAEFIX + _ziffern(rng, 5)
        pz = uid_pruefziffer(acht)
        if pz is not None:
            neun = acht + str(pz)
            return f"CHE-{neun[:3]}.{neun[3:6]}.{neun[6:]}"


def uid_gueltig(uid: str) -> bool:
    m = re.match(r"^CHE-(\d{3})\.(\d{3})\.(\d{3})$", uid.strip())
    if not m:
        return False
    neun = "".join(m.groups())
    return uid_pruefziffer(neun[:8]) == int(neun[8])


# ---------------------------------------------------------------------------
# Telefon und E-Mail
# ---------------------------------------------------------------------------


def telefon_ch(rng: np.random.Generator) -> str:
    """``+41 44 000 xx xx`` – Bereich 000 ist nicht vergeben."""
    return f"+41 44 000 {_ziffern(rng, 2)} {_ziffern(rng, 2)}"


def telefon_de(rng: np.random.Generator) -> str:
    """``+49 30 23125 xxx`` – offizieller Fiktionsbereich Berlin."""
    return f"+49 30 23125 {_ziffern(rng, 3)}"


def mobil_de(rng: np.random.Generator) -> str:
    """``+49 152 28817 xxx`` – Fiktionsbereich Mobil."""
    return f"+49 152 28817 {_ziffern(rng, 3)}"


def telefon(rng: np.random.Generator, land: str, mobil: bool = False) -> str:
    if land == "CH":
        return telefon_ch(rng)
    if land == "DE":
        return mobil_de(rng) if mobil else telefon_de(rng)
    raise ValueError("land muss CH oder DE sein")


def email_privat(rng: np.random.Generator, vorname: str, nachname: str, geburtsjahr: int | None = None) -> str:
    """Kunden-E-Mail auf einer ``.example``-Domain, Muster variieren wie im echten Leben."""
    v, n = ascii_handle(vorname), ascii_handle(nachname)
    muster = int(rng.integers(0, 5))
    if muster == 0:
        lokal = f"{v}.{n}"
    elif muster == 1:
        lokal = f"{v[0]}{n}" if v else n
    elif muster == 2:
        lokal = f"{n}.{v}"
    elif muster == 3 and geburtsjahr:
        lokal = f"{v}.{n}{str(geburtsjahr)[-2:]}"
    else:
        lokal = f"{v}{int(rng.integers(1, 99))}"
    domain = KUNDEN_DOMAINS[int(rng.integers(0, len(KUNDEN_DOMAINS)))]
    return f"{lokal}@{domain}"


def email_firma(firmenname: str, praefix: str = "info") -> str:
    """Firmen-E-Mail ``info@<firma>.example`` (Rechtsform wird entfernt)."""
    kern = re.sub(r"\b(AG|GmbH|Sàrl|SA|SARL|KG|OHG|e\.K\.|Einzelfirma|UG)\b", "", firmenname, flags=re.I)
    return f"{praefix}@{ascii_handle(kern)}.{FIRMEN_DOMAIN_TLD}"


def email_mitarbeiter(vorname: str, nachname: str, gesellschaft: str = "pfefferminzia") -> str:
    if gesellschaft not in ("pfefferminzia", "pfefferminz", "minzia"):
        raise ValueError("gesellschaft muss pfefferminzia, pfefferminz oder minzia sein")
    return f"{ascii_handle(vorname)}.{ascii_handle(nachname)}@{gesellschaft}.example"


def kennzeichen(rng: np.random.Generator, land: str) -> str:
    """Fiktive Kennzeichen ``ZH 000 000`` bzw. ``B-PM 0000`` (Datenarchitektur 6.1)."""
    if land == "CH":
        return f"{['ZH', 'BE', 'SO', 'AG', 'BL', 'LU'][int(rng.integers(0, 6))]} 000 {_ziffern(rng, 3)}"
    return f"{['B', 'HH', 'M', 'K', 'F', 'S'][int(rng.integers(0, 6))]}-PM {_ziffern(rng, 4)}"
