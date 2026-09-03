import hashlib

import numpy as np

from pfefferminzia.seeds import MASTER_SEED, derive_seed, faker_for, rng_for


def test_master_seed_ist_closing_datum():
    assert MASTER_SEED == 20250101


def test_derive_seed_entspricht_konvention():
    erwartet = int.from_bytes(hashlib.sha256(b"20250101:partner:PTR-00000001").digest()[:8], "big")
    assert derive_seed("partner", "PTR-00000001") == erwartet
    assert 0 <= derive_seed("x", 1) < 2**64


def test_derive_seed_deterministisch_und_unterscheidbar():
    assert derive_seed("partner", 1) == derive_seed("partner", 1)
    assert derive_seed("partner", 1) != derive_seed("partner", 2)
    assert derive_seed("partner", 1) != derive_seed("vertrag", 1)
    assert derive_seed("partner", 1) != derive_seed("partner", 1, master_seed=1)


def test_rng_for_reproduzierbar():
    a = rng_for("schaden", "SCH-00000042").random(5)
    b = rng_for("schaden", "SCH-00000042").random(5)
    c = rng_for("schaden", "SCH-00000043").random(5)
    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)
    assert isinstance(rng_for("m", 1), np.random.Generator)


def test_faker_for_reproduzierbar():
    assert faker_for("t", 1, "de_CH").pystr() == faker_for("t", 1, "de_CH").pystr()
