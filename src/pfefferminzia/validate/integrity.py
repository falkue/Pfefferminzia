"""Referenzintegritaet: jeder Fremdschluessel in curated loest auf (Datenarchitektur 5.8)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pandas as pd

from pfefferminzia.validate.registry import CheckErgebnis, check

if TYPE_CHECKING:
    from pfefferminzia.context import RunContext


@dataclass(frozen=True)
class FkBeziehung:
    kind_tabelle: str
    kind_spalte: str
    eltern_tabelle: str
    eltern_spalte: str
    optional: bool = True  # NULL erlaubt


# Beziehungen werden von den Fachstufen ergaenzt (``FK_BEZIEHUNGEN.append(...)``).
FK_BEZIEHUNGEN: list[FkBeziehung] = [
    FkBeziehung("curated/partner_adresse", "partner_id", "curated/partner", "partner_id", optional=False),
    FkBeziehung("curated/vertrag", "versicherungsnehmer_id", "curated/partner", "partner_id", optional=False),
    FkBeziehung("curated/vertrag", "vermittler_id", "curated/vermittler", "vermittler_id"),
    FkBeziehung("curated/vertrag", "antrag_id", "curated/antrag", "antrag_id"),
    FkBeziehung("curated/schaden", "vertrag_id", "curated/vertrag", "vertrag_id", optional=False),
    FkBeziehung("curated/schaden", "sachbearbeiter_id", "curated/mitarbeiter", "mitarbeiter_id"),
    FkBeziehung("curated/vermittler", "agentur_id", "curated/agentur", "agentur_id"),
    FkBeziehung("curated/mitarbeiter", "org_einheit_id", "curated/org_einheit", "org_einheit_id"),
    FkBeziehung("curated/interaktion", "partner_id", "curated/partner", "partner_id"),
    FkBeziehung("curated/dokument", "partner_id", "curated/partner", "partner_id"),
]


def pruefe_fk(kind: pd.DataFrame, kind_spalte: str, eltern: pd.DataFrame, eltern_spalte: str) -> pd.Series:
    """Liefert die Werte des Kind-FK, die nicht im Eltern-PK vorkommen (NULL ignoriert)."""
    werte = kind[kind_spalte].dropna()
    return werte[~werte.isin(set(eltern[eltern_spalte].dropna()))]


@check("referenzintegritaet", "Fremdschluessel in curated loesen auf", klasse="integritaet", reihenfolge=20)
def referenzintegritaet(ctx: RunContext, erg: CheckErgebnis) -> None:
    geprueft = 0
    for fk in FK_BEZIEHUNGEN:
        if not (ctx.tabellen.has(fk.kind_tabelle) and ctx.tabellen.has(fk.eltern_tabelle)):
            continue
        kind, eltern = ctx.tabellen.get(fk.kind_tabelle), ctx.tabellen.get(fk.eltern_tabelle)
        if fk.kind_spalte not in kind.columns or fk.eltern_spalte not in eltern.columns:
            erg.warnung(f"Spalte fehlt fuer FK {fk.kind_tabelle}.{fk.kind_spalte} -> "
                        f"{fk.eltern_tabelle}.{fk.eltern_spalte}", tabelle=fk.kind_tabelle)
            continue
        geprueft += 1
        if not fk.optional and kind[fk.kind_spalte].isna().any():
            erg.fehler("Pflicht-FK enthaelt NULL", tabelle=fk.kind_tabelle, spalte=fk.kind_spalte,
                       anzahl=int(kind[fk.kind_spalte].isna().sum()))
        fehlend = pruefe_fk(kind, fk.kind_spalte, eltern, fk.eltern_spalte)
        if len(fehlend):
            erg.fehler(f"{len(fehlend)} FK-Werte ohne Ziel in {fk.eltern_tabelle} "
                       f"(z. B. {fehlend.iloc[0]!r})", tabelle=fk.kind_tabelle, spalte=fk.kind_spalte,
                       anzahl=int(len(fehlend)))
    erg.info(f"{geprueft} FK-Beziehungen geprueft")


@check("primaerschluessel", "Primaerschluessel eindeutig und im curated-Format", klasse="integritaet",
       reihenfolge=21)
def primaerschluessel(ctx: RunContext, erg: CheckErgebnis) -> None:
    from pfefferminzia.ids import PRAEFIXE, is_curated_id

    for key, df in ctx.tabellen.alle("curated").items():
        name = key.split("/", 1)[1]
        pk = f"{name}_id"
        if pk not in df.columns:
            continue
        dubl = df[pk].duplicated().sum()
        if dubl:
            erg.fehler(f"{dubl} doppelte Primaerschluessel", tabelle=key, spalte=pk, anzahl=int(dubl))
        if name in PRAEFIXE:
            falsch = (~df[pk].astype(str).map(lambda v, n=name: is_curated_id(v, n))).sum()
            if falsch:
                erg.fehler(f"{falsch} IDs nicht im Format {PRAEFIXE[name][0]}-…", tabelle=key,
                           spalte=pk, anzahl=int(falsch))
