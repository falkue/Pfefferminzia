import re
import uuid

import pytest

from pfefferminzia import ids


def test_curated_formate():
    assert ids.partner_id(12345) == "PTR-00012345"
    assert ids.vertrag_id(12345) == "VTR-00012345"
    assert ids.antrag_id(1) == "ANT-00000001"
    assert ids.schaden_id(4512) == "SCH-00004512"
    assert ids.dokument_id(9) == "DOK-00000009"
    assert ids.interaktion_id(9) == "INT-00000009"
    assert ids.mitarbeiter_id(123) == "MIT-00123"
    assert ids.vermittler_id(123) == "VRM-00123"
    assert ids.agentur_id(12) == "AGT-0012"
    assert ids.regelwerk_id("HP", "avb", "CH", 2025) == "RW-HP-AVB-CH-2025"


def test_curated_bereich_und_parse():
    with pytest.raises(ValueError):
        ids.partner_id(10**8)
    with pytest.raises(KeyError):
        ids.curated_id("unbekannt", 1)
    assert ids.parse_curated_id("PTR-00012345") == ("PTR", 12345)
    assert ids.is_curated_id("PTR-00012345", "partner")
    assert not ids.is_curated_id("PTR-0012345")
    assert not ids.is_curated_id("VTR-00012345", "partner")


def test_produkt_und_tarifkuerzel():
    assert "HP-PRIV" in ids.PRODUKTE and "LV-EU" in ids.PRODUKTE
    assert ids.TARIFGENERATIONEN_HP == ("HP-KLASSIK", "HP-MODERN", "MZ-DIRECT", "PM-2025")
    assert ids.TARIFGENERATIONEN_LV[0] == "PK-85" and ids.TARIFGENERATIONEN_LV[-1] == "PZ-2025"


def test_legacy_formate():
    assert ids.vera_vertragsnummer(98765) == "L-0098765"
    hapo = ids.hapo_vertragsnummer(40987112)
    assert re.fullmatch(r"\d{2}\.\d{3}\.\d{3}-\d", hapo)
    assert hapo.startswith("40.987.112-")
    assert ids.hapo_vertragsnummer_gueltig(hapo)
    assert not ids.hapo_vertragsnummer_gueltig("40.987.112-" + str((int(hapo[-1]) + 1) % 10))
    assert ids.silas_schadennummer(2019, 4512) == "S2019/004512"
    assert ids.doku_archivnummer(123456) == "DOKU-0000123456"
    assert ids.personalnummer(123) == "00123"
    assert ids.agenturnummer(12) == "0012"


def test_legacy_partnernummern_eigene_kreise():
    v, h = ids.legacy_partnernummer("VERA", 234567), ids.legacy_partnernummer("HAPO", 234567)
    assert re.fullmatch(r"\d{8}", v) and re.fullmatch(r"\d{8}", h)
    assert v != h


def test_modulo10_rekursiv_bekannter_wert():
    # ESR-Referenz 96111690000000660000000928 hat Pruefziffer 4 (Standardbeispiel)
    assert ids.modulo10_rekursiv("96111690000000660000000928") == 4


def test_mint_uuid_deterministisch_v4():
    a = ids.mint_uuid("customer", "PTR-00000001")
    b = ids.mint_uuid("customer", "PTR-00000001")
    c = ids.mint_uuid("customer", "PTR-00000002")
    assert a == b != c
    u = uuid.UUID(a)
    assert u.version == 4 and u.variant == uuid.RFC_4122
    assert ids.mint_policennummer(2021, 123) == "MZ-2021-000123-P"
    assert ids.mint_schadennummer(2022, 4512) == "CLM-2022-0004512"
    assert ids.mint_email_handle("Lea", "Müller") == "lea.mueller"
