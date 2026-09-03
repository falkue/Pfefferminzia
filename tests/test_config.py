from datetime import date

import pytest
from pydantic import ValidationError

from pfefferminzia.config import GeneratorConfig, load_config


def test_config_laden(config):
    assert config.master_seed == 20250101
    assert config.zeit.stichtag == date(2025, 12, 31)
    assert config.zeit.closing == date(2025, 1, 1)
    assert abs(config.markt.anteil_ch - 0.47) < 1e-9
    assert set(config.stufen) == {"S", "M", "L"}


def test_stufen_mengen(config):
    s, m, ll = config.stufe("S"), config.stufe("M"), config.stufe("L")
    assert s.menge("partner") == 1000 and s.menge("vertraege") == 1500
    assert m.menge("partner") == 50000 and m.menge("vertraege") == 75000 and m.menge("schaeden") == 27000
    assert ll.faktor == 5.0 and ll.menge("vertraege") == 5 * m.menge("vertraege")
    assert s.dokumente_rendern == "alle" and ll.dokumente_rendern == "keine"
    with pytest.raises(KeyError):
        s.menge("gibt_es_nicht")
    assert s.menge("gibt_es_nicht", 7) == 7


def test_fallen(config):
    f = config.fallen
    assert f.aktiv("leakage") and f.staerke("underwriting_bias") == pytest.approx(0.6)
    f2 = f.model_copy(update={"saubere_variante": True})
    assert not f2.aktiv("leakage") and f2.staerke("underwriting_bias") == 0.0


def test_teilbaum_validierung():
    basis = {
        "stufen": {
            "S": {"faktor": 0.02, "mengen": {"partner": 1000}},
            "M": {"faktor": 1.0, "mengen": {"partner": 500}},
            "L": {"faktor": 5.0, "mengen": {"partner": 250000}},
        }
    }
    with pytest.raises(ValidationError):
        GeneratorConfig.model_validate(basis)
    basis["stufen"]["M"]["mengen"]["partner"] = 50000
    assert GeneratorConfig.model_validate(basis).stufe("M").menge("partner") == 50000


def test_unbekannte_felder_abgelehnt():
    with pytest.raises(ValidationError):
        GeneratorConfig.model_validate({"stufen": {"S": {"faktor": 1}, "M": {"faktor": 1}, "L": {"faktor": 1}},
                                        "unbekannt": 1})


def test_fehlende_datei(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nix.yaml")
