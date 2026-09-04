"""Checks-Registry und Berichtsstruktur."""

from __future__ import annotations

import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from pfefferminzia.context import RunContext

Schwere = Literal["FEHLER", "WARNUNG", "INFO"]


@dataclass
class Befund:
    schwere: Schwere
    meldung: str
    tabelle: str | None = None
    spalte: str | None = None
    anzahl: int | None = None


@dataclass
class CheckErgebnis:
    name: str
    befunde: list[Befund] = field(default_factory=list)
    dauer_s: float = 0.0
    uebersprungen: bool = False
    grund: str = ""

    @property
    def ok(self) -> bool:
        return not any(b.schwere == "FEHLER" for b in self.befunde)

    def fehler(self, meldung: str, **kw) -> None:
        self.befunde.append(Befund("FEHLER", meldung, **kw))

    def warnung(self, meldung: str, **kw) -> None:
        self.befunde.append(Befund("WARNUNG", meldung, **kw))

    def info(self, meldung: str, **kw) -> None:
        self.befunde.append(Befund("INFO", meldung, **kw))


CheckFn = Callable[["RunContext", CheckErgebnis], None]


@dataclass(frozen=True)
class Check:
    name: str
    beschreibung: str
    fn: CheckFn
    klasse: str = "allgemein"  # schema | integritaet | fiktionalitaet | zeit | bilanz | verteilung ...
    reihenfolge: int = 100


_REGISTRY: dict[str, Check] = {}


def check(name: str, beschreibung: str = "", klasse: str = "allgemein", reihenfolge: int = 100):
    """Dekorator: registriert eine Funktion ``fn(ctx, ergebnis)`` als Check."""

    def deco(fn: CheckFn) -> CheckFn:
        if name in _REGISTRY:
            raise ValueError(f"Check {name} ist bereits registriert")
        _REGISTRY[name] = Check(name, beschreibung or (fn.__doc__ or "").strip(), fn, klasse, reihenfolge)
        return fn

    return deco


def checks() -> list[Check]:
    return sorted(_REGISTRY.values(), key=lambda c: (c.reihenfolge, c.name))


@dataclass
class Bericht:
    ergebnisse: list[CheckErgebnis] = field(default_factory=list)

    @property
    def fehler(self) -> int:
        return sum(1 for e in self.ergebnisse for b in e.befunde if b.schwere == "FEHLER")

    @property
    def warnungen(self) -> int:
        return sum(1 for e in self.ergebnisse for b in e.befunde if b.schwere == "WARNUNG")

    @property
    def ok(self) -> bool:
        return self.fehler == 0

    def zusammenfassung(self) -> str:
        n = len(self.ergebnisse)
        u = sum(1 for e in self.ergebnisse if e.uebersprungen)
        return f"{n} Checks ({u} uebersprungen), {self.fehler} Fehler, {self.warnungen} Warnungen"


def run_checks(ctx: RunContext, namen: Iterable[str] | None = None, klassen: Iterable[str] | None = None) -> Bericht:
    auswahl = checks()
    if namen:
        gewuenscht = set(namen)
        unbekannt = gewuenscht - {c.name for c in auswahl}
        if unbekannt:
            raise KeyError(f"Unbekannte Checks: {sorted(unbekannt)}")
        auswahl = [c for c in auswahl if c.name in gewuenscht]
    if klassen:
        auswahl = [c for c in auswahl if c.klasse in set(klassen)]
    bericht = Bericht()
    for c in auswahl:
        erg = CheckErgebnis(name=c.name)
        t0 = time.perf_counter()
        try:
            c.fn(ctx, erg)
        except Exception as exc:  # noqa: BLE001 – ein defekter Check darf die Suite nicht abbrechen
            erg.fehler(f"Check abgebrochen: {exc!r}")
        erg.dauer_s = time.perf_counter() - t0
        bericht.ergebnisse.append(erg)
    return bericht
