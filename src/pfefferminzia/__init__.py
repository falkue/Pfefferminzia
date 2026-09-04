"""Pfefferminzia – Generator fuer den synthetischen Lehr-Datensatz.

Fiktives Lehrbeispiel. Alle Daten synthetisch. Keine Verbindung zu realen Personen,
Unternehmen oder Marken.
"""

from pfefferminzia.seeds import MASTER_SEED, derive_seed, rng_for

__version__ = "0.1.0"
__all__ = ["MASTER_SEED", "__version__", "derive_seed", "rng_for"]
