"""Schema-Checks mit pandera. Schemas werden je Tabelle in ``SCHEMAS`` registriert."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pfefferminzia.validate.registry import CheckErgebnis, check

if TYPE_CHECKING:
    from pfefferminzia.context import RunContext

try:
    import pandera.pandas as pa

    PANDERA = True
except ImportError:  # pragma: no cover – pandera ist Dev-Abhaengigkeit
    try:
        import pandera as pa  # type: ignore[no-redef]

        PANDERA = True
    except ImportError:
        pa = None  # type: ignore[assignment]
        PANDERA = False


def _schemas() -> dict[str, object]:
    if not PANDERA:
        return {}
    str_ = pa.Column(str)
    return {
        "reference/geo_orte_ch": pa.DataFrameSchema(
            {
                "plz": pa.Column(str, pa.Check.str_matches(r"^\d{4}$")),
                "ort": str_,
                "kanton": pa.Column(str, pa.Check.str_matches(r"^[A-Z]{2}$")),
                "sprachregion": pa.Column(str, pa.Check.isin(["de", "fr", "it"])),
                "einwohner": pa.Column(int, pa.Check.gt(0), coerce=True),
                "gewicht": pa.Column(float, pa.Check.gt(0), coerce=True),
                "tarifzone": str_,
                "urbanitaet": pa.Column(str, pa.Check.isin(["STADT", "AGGLO", "LAND"])),
            },
            unique=["plz", "ort"],
            strict=False,
        ),
        "reference/geo_orte_de": pa.DataFrameSchema(
            {
                "plz": pa.Column(str, pa.Check.str_matches(r"^\d{5}$")),
                "ort": str_,
                "bundesland": str_,
                "bundesland_kuerzel": pa.Column(str, pa.Check.str_matches(r"^[A-Z]{2}$")),
                "einwohner": pa.Column(int, pa.Check.gt(0), coerce=True),
                "gewicht": pa.Column(float, pa.Check.gt(0), coerce=True),
                "tarifzone": str_,
                "urbanitaet": pa.Column(str, pa.Check.isin(["STADT", "AGGLO", "LAND"])),
            },
            unique=["plz", "ort"],
            strict=False,
        ),
        "reference/geo_strassennamen": pa.DataFrameSchema(
            {
                "strasse": str_,
                "sprache": pa.Column(str, pa.Check.isin(["de-CH", "de-DE", "fr", "it"])),
                "typ": str_,
                "generisch": pa.Column(bool, coerce=True),
            },
            unique=["strasse", "sprache"],
            strict=False,
        ),
        "reference/namen_vornamen": pa.DataFrameSchema(
            {
                "vorname": str_,
                "geschlecht": pa.Column(str, pa.Check.isin(["M", "W", "U"])),
                "sprachraum": pa.Column(str, pa.Check.isin(["de-CH", "de-DE", "fr", "it", "international"])),
                **{f"g_{d}": pa.Column(float, pa.Check.ge(0), coerce=True)
                   for d in range(1930, 2010, 10)},
            },
            unique=["vorname", "geschlecht", "sprachraum"],
            strict=False,
        ),
        "reference/namen_nachnamen": pa.DataFrameSchema(
            {
                "nachname": str_,
                "sprachraum": pa.Column(str, pa.Check.isin(["de-CH", "de-DE", "fr", "it", "international"])),
                "gewicht": pa.Column(float, pa.Check.gt(0), coerce=True),
                "synthetisch": pa.Column(bool, coerce=True),
            },
            unique=["nachname", "sprachraum"],
            strict=False,
        ),
        "reference/namen_blocklist": pa.DataFrameSchema(
            {
                "typ": pa.Column(str, pa.Check.isin(["person", "firma"])),
                "kategorie": str_,
            },
            strict=False,
        ),
    }


SCHEMAS: dict[str, object] = _schemas()


@check("schema", "Schema-Check registrierter Tabellen (pandera)", klasse="schema", reihenfolge=10)
def schema_check(ctx: RunContext, erg: CheckErgebnis) -> None:
    if not PANDERA:
        erg.uebersprungen, erg.grund = True, "pandera nicht installiert"
        erg.warnung("pandera nicht installiert – Schema-Check uebersprungen")
        return
    geprueft = 0
    for key, df in ctx.tabellen.alle().items():
        schema = SCHEMAS.get(key)
        if schema is None:
            continue
        geprueft += 1
        try:
            schema.validate(df, lazy=True)
        except pa.errors.SchemaErrors as exc:
            for _, zeile in exc.failure_cases.iterrows():
                erg.fehler(
                    f"{zeile.get('check')}: {zeile.get('failure_case')!r}",
                    tabelle=key, spalte=str(zeile.get("column")),
                )
    erg.info(f"{geprueft} Tabellen mit Schema geprueft, {len(ctx.tabellen)} registriert")
