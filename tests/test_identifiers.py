import re

import pytest

from pfefferminzia.seeds import rng_for
from pfefferminzia.synth import identifiers as idf


@pytest.fixture()
def rng():
    return rng_for("test.identifiers", 1)


def test_iban_ch(rng):
    for _ in range(50):
        iban = idf.iban_ch(rng)
        assert re.fullmatch(r"CH\d{19}", iban)
        assert iban[4:9] == "99999"
        assert idf.iban_gueltig(iban)
    assert idf.iban_gueltig("CH9300762011623852957")  # bekanntes Beispiel
    assert not idf.iban_gueltig("CH9300762011623852958")


def test_iban_de(rng):
    for _ in range(50):
        iban = idf.iban_de(rng)
        assert re.fullmatch(r"DE\d{20}", iban)
        assert iban[4:12] == "99999999"
        assert idf.iban_gueltig(iban)
    assert idf.iban_gueltig("DE89370400440532013000")
    assert idf.iban_formatiert("DE89370400440532013000") == "DE89 3704 0044 0532 0130 00"


def test_ahv_nummer(rng):
    for _ in range(100):
        n = idf.ahv_nummer(rng)
        assert re.fullmatch(r"756\.\d{4}\.\d{4}\.\d{2}", n)
        assert idf.ahv_gueltig(n)
    assert idf.ahv_gueltig("756.9217.0769.85")  # Beispielnummer der ZAS
    assert not idf.ahv_gueltig("756.9217.0769.86")


def test_steuer_id(rng):
    for _ in range(200):
        s = idf.steuer_id(rng)
        assert re.fullmatch(r"[1-9]\d{10}", s)
        assert idf.steuer_id_gueltig(s)
        zaehl = {d: s[:10].count(d) for d in set(s[:10])}
        assert sorted(zaehl.values())[-1] in (2, 3)
        assert sum(1 for v in zaehl.values() if v > 1) == 1
    assert idf.steuer_id_pruefziffer("8657125149") == 5  # Beispiel aus der Literatur (86571251495)
    assert not idf.steuer_id_gueltig("86571251496")


def test_che_uid(rng):
    for _ in range(100):
        u = idf.che_uid(rng)
        assert re.fullmatch(r"CHE-499\.\d{3}\.\d{3}", u)
        assert idf.uid_gueltig(u)
    assert idf.uid_gueltig("CHE-109.322.551")  # oeffentlich bekanntes Format-Beispiel (BFS)
    assert not idf.uid_gueltig("CHE-109.322.552")


def test_telefon_und_email(rng):
    assert re.fullmatch(r"\+41 44 000 \d{2} \d{2}", idf.telefon_ch(rng))
    assert re.fullmatch(r"\+49 30 23125 \d{3}", idf.telefon_de(rng))
    assert re.fullmatch(r"\+49 152 28817 \d{3}", idf.mobil_de(rng))
    assert idf.telefon(rng, "DE", mobil=True).startswith("+49 152")
    for _ in range(20):
        assert idf.email_privat(rng, "Léa", "Müller", 1994).endswith(".example")
    assert idf.email_firma("Brunnmatt Sanitär GmbH") == "info@brunnmatt-sanitaer.example"
    assert idf.email_mitarbeiter("Hans-Peter", "Müller") == "hans-peter.mueller@pfefferminzia.example"
    assert idf.ascii_handle("Zoë Straßer") == "zoe-strasser"
    assert idf.kennzeichen(rng, "CH").split()[1] == "000"
