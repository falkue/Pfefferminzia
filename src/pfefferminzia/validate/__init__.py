"""Validierungssuite: erweiterbare Checks-Registry (Datenarchitektur 5.8).

Checks werden mit ``@check`` registriert und von ``run_checks(ctx)`` ausgefuehrt. Grundgeruest:
Schema-Check (pandera), Referenzintegritaet, Fiktionalitaets-Blocklist.
"""

# Registrierung der Basis-Checks durch Import
from pfefferminzia.validate import fiction, integrity, schema, zeit  # noqa: E402, F401
from pfefferminzia.validate.registry import (
    Befund,
    Bericht,
    Check,
    CheckErgebnis,
    check,
    checks,
    run_checks,
)

__all__ = ["Befund", "Bericht", "Check", "CheckErgebnis", "check", "checks", "run_checks"]
