"""Seed-Konzept gemaess docs/konventionen.md §7.

* Master-Seed ``20250101`` (Closing-Datum), konfigurierbar in ``config/generator.yaml``.
* Abgeleiteter Seed: ``sha256(f"{master_seed}:{modul}:{entity_id}")``, erste 8 Bytes als Integer
  (Big-Endian, vorzeichenlos).
* Jeder Zufallszug laeuft ueber einen ``numpy.random.Generator`` (PCG64), der aus einem
  abgeleiteten Seed erzeugt wird. Es gibt keine globalen Zufallsquellen.
"""

from __future__ import annotations

import hashlib
from typing import Any

import numpy as np

MASTER_SEED = 20250101


def derive_seed(modul: str, entity_id: Any, master_seed: int = MASTER_SEED) -> int:
    """Leitet einen 64-Bit-Seed deterministisch aus Master-Seed, Modul und Entitaets-ID ab."""
    if not modul:
        raise ValueError("modul darf nicht leer sein")
    text = f"{int(master_seed)}:{modul}:{entity_id}"
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], byteorder="big", signed=False)


def rng_for(modul: str, entity_id: Any, master_seed: int = MASTER_SEED) -> np.random.Generator:
    """Liefert einen unabhaengigen PCG64-Generator fuer (modul, entity_id)."""
    return np.random.Generator(np.random.PCG64(derive_seed(modul, entity_id, master_seed)))


def faker_for(modul: str, entity_id: Any, locale: str = "de_CH", master_seed: int = MASTER_SEED):
    """Faker-Instanz mit entitaetsbezogenem Seed.

    Faker wird nur fuer Strukturen (Formate) genutzt; Namen und Orte kommen aus den
    kuratierten Referenzlisten unter ``data/reference/``.
    """
    from faker import Faker

    fake = Faker(locale)
    fake.seed_instance(derive_seed(modul, entity_id, master_seed) % (2**32))
    return fake
