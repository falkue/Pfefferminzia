"""Stufen-Registry der Generator-Pipeline (Gesamtplan 4.8, Datenarchitektur 5.2).

Reihenfolge: config → reference → organisation → partner → vertrag → schaden → finanz → prozess →
text → render → legacyify → mintify → export → validate. Jede Stufe ist eine Klasse mit
``run(ctx)``. Neue Stufen werden mit ``@register`` angemeldet; die Nummer bestimmt die Ordnung.
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass

from pfefferminzia.context import RunContext

log = logging.getLogger("pfefferminzia.pipeline")


class Stage(ABC):
    name: str = ""
    nummer: int = 0
    beschreibung: str = ""
    welle: int = 0  # Umsetzungswelle laut Gesamtplan §8

    @abstractmethod
    def run(self, ctx: RunContext) -> None: ...

    def stub(self, ctx: RunContext) -> None:
        ctx.ereignis(self.name, f"Stub – noch nicht implementiert (Welle {self.welle})")


_REGISTRY: dict[str, type[Stage]] = {}


def register(cls: type[Stage]) -> type[Stage]:
    if not cls.name:
        raise ValueError("Stage braucht einen Namen")
    if cls.name in _REGISTRY:
        raise ValueError(f"Stage {cls.name} ist bereits registriert")
    _REGISTRY[cls.name] = cls
    return cls


def stages() -> list[type[Stage]]:
    return sorted(_REGISTRY.values(), key=lambda c: c.nummer)


def stage_names() -> list[str]:
    return [s.name for s in stages()]


# ---------------------------------------------------------------------------
# Stufen
# ---------------------------------------------------------------------------


@register
class ConfigStage(Stage):
    name, nummer, welle = "config", 0, 0
    beschreibung = "Konfiguration validieren, Manifest initialisieren"

    def run(self, ctx: RunContext) -> None:
        sc = ctx.stufe_config
        ctx.ereignis(self.name, f"Stufe {ctx.stufe} (Faktor {sc.faktor}), Master-Seed {ctx.master_seed}, "
                                f"Stichtag {ctx.config.zeit.stichtag.isoformat()}")
        if ctx.config.fallen.saubere_variante:
            ctx.ereignis(self.name, "Saubere Variante: alle Fallen deaktiviert")


@register
class ReferenceStage(Stage):
    name, nummer, welle = "reference", 10, 0
    beschreibung = "Referenzdaten laden und als reference/* registrieren"

    def run(self, ctx: RunContext) -> None:
        import pandas as pd

        for st in ctx.reference.status():
            if not st.vorhanden:
                ctx.ereignis(self.name, f"Referenz {st.schluessel} fehlt ({st.hinweis})", fehlt=True)
                continue
            daten = ctx.reference.load(st.schluessel)
            if isinstance(daten, pd.DataFrame):
                ctx.tabellen.register(st.schluessel.replace(".", "_"), daten, layer="reference",
                                      ersetzen=True)
            elif isinstance(daten, dict):
                for k, v in daten.items():
                    if isinstance(v, pd.DataFrame):
                        ctx.tabellen.register(f"{st.schluessel}_{k}".replace(".", "_"), v,
                                              layer="reference", ersetzen=True)
            ctx.ereignis(self.name, f"Referenz {st.schluessel} geladen ({st.zeilen} Eintraege)")


@register
class OrganisationStage(Stage):
    name, nummer, welle = "organisation", 20, 1
    beschreibung = "Org-Einheiten, Mitarbeiter, Agenturen, Vermittler, Produkte, Tarifgenerationen"

    def run(self, ctx: RunContext) -> None:
        self.stub(ctx)


from pfefferminzia.synth.partner import PartnerStage


@register
class VertragStage(Stage):
    name, nummer, welle = "vertrag", 40, 1
    beschreibung = "Antraege, Underwriting, Vertraege, Versionen, Deckungen, Risikoobjekte"

    def run(self, ctx: RunContext) -> None:
        self.stub(ctx)


@register
class SchadenStage(Stage):
    name, nummer, welle = "schaden", 50, 5
    beschreibung = "Schaeden/Leistungsfaelle, Positionen, Beteiligte, Statusverlauf, Betrugswahrheit"

    def run(self, ctx: RunContext) -> None:
        self.stub(ctx)


@register
class FinanzStage(Stage):
    name, nummer, welle = "finanz", 60, 2
    beschreibung = "Rechnungen, Buchungen, Mahnungen, vertrag_jahr, Wechselkurse"

    def run(self, ctx: RunContext) -> None:
        self.stub(ctx)


@register
class ProzessStage(Stage):
    name, nummer, welle = "prozess", 70, 2
    beschreibung = "Aufgaben, Interaktions-Skelette, Beschwerden, Dokument-Skelette"

    def run(self, ctx: RunContext) -> None:
        self.stub(ctx)


@register
class TextStage(Stage):
    name, nummer, welle = "text", 80, 6
    beschreibung = "Freitexte (LLM mit Cache, Template-Fallback)"

    def run(self, ctx: RunContext) -> None:
        self.stub(ctx)


@register
class RenderStage(Stage):
    name, nummer, welle = "render", 85, 6
    beschreibung = "PDF/DOCX/PNG/EML, Scan-Simulation"

    def run(self, ctx: RunContext) -> None:
        self.stub(ctx)


@register
class LegacyifyStage(Stage):
    name, nummer, welle = "legacyify", 90, 1
    beschreibung = "raw VERA/HAPO/SILAS/DOKU mit DQ-Injektion, Migrationslog, xref"

    def run(self, ctx: RunContext) -> None:
        self.stub(ctx)


@register
class MintifyStage(Stage):
    name, nummer, welle = "mintify", 91, 1
    beschreibung = "raw MINT (JSONL, Schema-Drift, Migrationsartefakte)"

    def run(self, ctx: RunContext) -> None:
        self.stub(ctx)


@register
class ExportStage(Stage):
    name, nummer, welle = "export", 95, 0
    beschreibung = "Registrierte Tabellen als Parquet + CSV schreiben, Manifest fuellen"

    def run(self, ctx: RunContext) -> None:
        from pfefferminzia.export import exportiere_tabelle

        formate = tuple(f for f in ctx.stufe_config.formate if f in ("parquet", "csv"))
        anzahl = 0
        for key, df in ctx.tabellen.alle().items():
            layer, name = key.split("/", 1)
            if layer == "reference":
                continue  # Referenzdaten werden nicht re-exportiert
            exportiere_tabelle(
                df, name, ctx.ausgabe_dir(layer), layer=layer, formate=formate,
                manifest=ctx.manifest, manifest_root=ctx.root,
                bom=ctx.config.export.csv_bom, zeilenende=ctx.config.export.csv_zeilenende,
                kompression=ctx.config.export.parquet_kompression,
            )
            anzahl += 1
        ctx.ereignis(self.name, f"{anzahl} Tabellen exportiert ({', '.join(formate) or 'keine Formate'})")


@register
class ValidateStage(Stage):
    name, nummer, welle = "validate", 99, 0
    beschreibung = "Checks ausfuehren, Manifest schreiben"

    def run(self, ctx: RunContext) -> None:
        from pfefferminzia.validate import run_checks

        bericht = run_checks(ctx)
        ctx.ereignis(self.name, bericht.zusammenfassung(), fehler=bericht.fehler)
        if ctx.manifest is not None:
            pfad = ctx.manifest.write(ctx.pfade.manifest.with_name(f"manifest_{ctx.stufe}.json"))
            ctx.ereignis(self.name, f"Manifest geschrieben: {pfad}")


# ---------------------------------------------------------------------------
# Ausfuehrung
# ---------------------------------------------------------------------------


@dataclass
class StufenErgebnis:
    name: str
    dauer_s: float
    ok: bool
    fehler: str | None = None


def auswahl(von: str | None = None, bis: str | None = None, nur: Iterable[str] | None = None) -> list[type[Stage]]:
    alle = stages()
    namen = [s.name for s in alle]
    if nur:
        unbekannt = [n for n in nur if n not in namen]
        if unbekannt:
            raise KeyError(f"Unbekannte Stufen: {unbekannt}; bekannt: {namen}")
        return [s for s in alle if s.name in set(nur)]
    start = namen.index(von) if von else 0
    ende = namen.index(bis) if bis else len(namen) - 1
    if start > ende:
        raise ValueError(f"von={von} liegt nach bis={bis}")
    return alle[start : ende + 1]


def run_pipeline(
    ctx: RunContext,
    von: str | None = None,
    bis: str | None = None,
    nur: Iterable[str] | None = None,
    abbruch_bei_fehler: bool = True,
) -> list[StufenErgebnis]:
    ergebnisse: list[StufenErgebnis] = []
    for cls in auswahl(von, bis, nur):
        stufe = cls()
        t0 = time.perf_counter()
        try:
            log.info("Stufe %s (%02d) startet: %s", stufe.name, stufe.nummer, stufe.beschreibung)
            stufe.run(ctx)
            ergebnisse.append(StufenErgebnis(stufe.name, time.perf_counter() - t0, True))
        except Exception as exc:
            ergebnisse.append(StufenErgebnis(stufe.name, time.perf_counter() - t0, False, repr(exc)))
            log.exception("Stufe %s fehlgeschlagen", stufe.name)
            if abbruch_bei_fehler:
                raise
    return ergebnisse
