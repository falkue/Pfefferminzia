"""Export einer Tabelle als Parquet (kanonisch) und CSV (UTF-8 mit BOM) plus Manifest-Eintrag.

CSV-Konventionen (Datenarchitektur 4.1): Komma, ``\\n``-Zeilenende, Nullwert = leeres Feld,
Datum ``YYYY-MM-DD``, Zeitstempel ``YYYY-MM-DDTHH:MM:SSZ``, Booleans ``true``/``false``,
Dezimalpunkt. Parquet ohne Zeitstempel-Metadaten fuer Byte-Identitaet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from pfefferminzia.manifest import Manifest, TabellenEintrag, sha256_datei

Format = Literal["parquet", "csv"]
Layer = Literal["curated", "raw", "truth", "reference", "sample", "migration"]


@dataclass
class ExportErgebnis:
    name: str
    layer: str
    rows: int
    columns: int
    pfade: dict[str, Path] = field(default_factory=dict)
    sha256: dict[str, str] = field(default_factory=dict)


def _csv_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Bereitet einen DataFrame fuer die CSV-Konventionen auf (Kopie)."""
    out = df.copy()
    for spalte in out.columns:
        s = out[spalte]
        dtype = s.dtype
        if pd.api.types.is_bool_dtype(dtype):
            out[spalte] = s.map({True: "true", False: "false"})
        elif isinstance(dtype, pd.BooleanDtype):
            out[spalte] = s.map({True: "true", False: "false"}).astype("string")
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            if getattr(dtype, "tz", None) is not None:
                out[spalte] = s.dt.tz_convert("UTC").dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                # naive Zeitstempel: reine Datumswerte als Datum, sonst als UTC-Zeitstempel
                nur_datum = bool(((s.dropna().dt.normalize() == s.dropna())).all())
                fmt = "%Y-%m-%d" if nur_datum else "%Y-%m-%dT%H:%M:%SZ"
                out[spalte] = s.dt.strftime(fmt)
        elif dtype == object:
            out[spalte] = s.map(
                lambda v: v.isoformat() if hasattr(v, "isoformat") and not isinstance(v, str) else v
            )
    return out


def schreibe_csv(df: pd.DataFrame, pfad: Path, bom: bool = True, zeilenende: str = "\n") -> Path:
    pfad = Path(pfad)
    pfad.parent.mkdir(parents=True, exist_ok=True)
    _csv_frame(df).to_csv(
        pfad,
        index=False,
        encoding="utf-8-sig" if bom else "utf-8",
        lineterminator=zeilenende,
        na_rep="",
        float_format="%.2f" if _nur_betraege(df) else None,
    )
    return pfad


def _nur_betraege(df: pd.DataFrame) -> bool:
    """Heuristik: Float-Spalten, die wie Betraege heissen, mit 2 Nachkommastellen schreiben."""
    floats = [c for c in df.columns if pd.api.types.is_float_dtype(df[c].dtype)]
    return bool(floats) and all(
        any(t in c for t in ("betrag", "praemie", "summe", "wert", "kapital", "reserve"))
        for c in floats
    )


def schreibe_parquet(df: pd.DataFrame, pfad: Path, kompression: str = "snappy") -> Path:
    pfad = Path(pfad)
    pfad.parent.mkdir(parents=True, exist_ok=True)
    tabelle = pa.Table.from_pandas(df, preserve_index=False)
    # pandas-Metadaten entfernen: sie enthalten Versionsstrings und stoeren die Byte-Identitaet
    tabelle = tabelle.replace_schema_metadata(None)
    pq.write_table(
        tabelle,
        pfad,
        compression=None if kompression == "none" else kompression,
        store_schema=True,
        write_statistics=True,
    )
    return pfad


def lese_parquet(pfad: Path) -> pd.DataFrame:
    return pq.read_table(pfad).to_pandas()


def lese_csv(pfad: Path, **kwargs) -> pd.DataFrame:
    return pd.read_csv(pfad, encoding="utf-8-sig", keep_default_na=True, **kwargs)


def exportiere_tabelle(
    df: pd.DataFrame,
    name: str,
    ausgabe_dir: Path,
    layer: str = "curated",
    formate: tuple[str, ...] = ("parquet", "csv"),
    manifest: Manifest | None = None,
    manifest_root: Path | None = None,
    bom: bool = True,
    zeilenende: str = "\n",
    kompression: str = "snappy",
) -> ExportErgebnis:
    """Schreibt ``df`` in ``ausgabe_dir/<format>/<name>.<ext>`` und traegt Hashes ins Manifest ein."""
    if not name or not name.replace("_", "").isalnum():
        raise ValueError(f"Ungueltiger Tabellenname: {name!r}")
    ausgabe_dir = Path(ausgabe_dir)
    erg = ExportErgebnis(name=name, layer=layer, rows=len(df), columns=len(df.columns))
    for fmt in formate:
        if fmt == "parquet":
            pfad = schreibe_parquet(df, ausgabe_dir / "parquet" / f"{name}.parquet", kompression)
        elif fmt == "csv":
            pfad = schreibe_csv(df, ausgabe_dir / "csv" / f"{name}.csv", bom, zeilenende)
        else:
            raise ValueError(f"Format {fmt!r} wird von exportiere_tabelle nicht unterstuetzt")
        erg.pfade[fmt] = pfad
        erg.sha256[fmt] = sha256_datei(pfad)
    if manifest is not None:
        root = manifest_root or ausgabe_dir
        manifest.add_table(
            TabellenEintrag(
                name=name,
                layer=layer,
                rows=erg.rows,
                columns=erg.columns,
                files={f: _relativ(p, root) for f, p in erg.pfade.items()},
                sha256=dict(erg.sha256),
            )
        )
    return erg


def _relativ(pfad: Path, root: Path) -> str:
    try:
        return pfad.resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return pfad.as_posix()
