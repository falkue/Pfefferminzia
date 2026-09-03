import pytest

from pfefferminzia.reference import ReferenceLoader
from pfefferminzia.seeds import rng_for
from pfefferminzia.synth.addresses import AddressSynth, geo_versatz
from pfefferminzia.synth.names import NameSynth, dekade, firmenname
from pfefferminzia.validate.fiction import Blocklist


@pytest.fixture(scope="module")
def ldr(root):
    return ReferenceLoader(root / "data" / "reference")


def test_namen_deterministisch_und_blocklist(ldr):
    bl = Blocklist(ldr.csv("namen.blocklist"))
    ns = NameSynth(ldr.csv("namen.vornamen"), ldr.csv("namen.nachnamen"), bl)
    p1 = ns.person(rng_for("t", 1), "W", "CH", 1965, "de")
    p2 = ns.person(rng_for("t", 1), "W", "CH", 1965, "de")
    assert p1 == p2 and p1.vorname and p1.nachname
    assert dekade(1929) == 1930 and dekade(2007) == 2000 and dekade(1965) == 1960
    for i in range(200):
        p = ns.person(rng_for("t", i), "M" if i % 2 else "W", "DE" if i % 3 else "CH", 1940 + i % 60)
        assert not bl.person_gesperrt(p.vorname, p.nachname)
    assert bl.person_gesperrt("Roger", "Federer")


def test_firmenname(ldr):
    bl = Blocklist(ldr.csv("namen.blocklist"))
    b = ldr.csv("namen.firmennamen_bausteine")
    n1 = firmenname(rng_for("f", 1), b, "CH", bl)
    assert n1 == firmenname(rng_for("f", 1), b, "CH", bl)
    assert any(n1.endswith(rf) for rf in ("AG", "GmbH", "Sàrl", "SA", "Sagl")) or len(n1.split()) >= 2


def test_adressen(ldr):
    a = AddressSynth(ldr.csv("geo.orte_ch"), ldr.csv("geo.orte_de"), ldr.csv("geo.strassennamen"))
    adr = a.adresse(rng_for("a", 1), "CH", sprachregion="fr")
    assert adr.sprache == "fr" and len(adr.plz) == 4
    adr_de = a.adresse(rng_for("a", 2), "DE")
    assert len(adr_de.plz) == 5 and adr_de.zeile().endswith(adr_de.ort)
    assert a.adresse(rng_for("a", 3), "CH") == a.adresse(rng_for("a", 3), "CH")
    ort = a.ort(rng_for("a", 4), "CH", region="SO")
    assert ort.region == "SO"
    lat, lon = geo_versatz(rng_for("g", 1), 47.35, 7.9)
    assert abs(lat - 47.35) < 0.02 and abs(lon - 7.9) < 0.03
