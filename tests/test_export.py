from datetime import date

import numpy as np
import pandas as pd

from pfefferminzia.export import exportiere_tabelle, lese_csv, lese_parquet
from pfefferminzia.manifest import Manifest, sha256_datei


def _beispiel() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "partner_id": ["PTR-00000001", "PTR-00000002", "PTR-00000003"],
            "nachname": ["Müller", "Brunner", None],
            "geburtsdatum": [date(1958, 3, 12), date(1994, 6, 2), None],
            "praemie_betrag": [180.0, 95.5, np.nan],
            "ist_aktiv": [True, False, True],
            "anzahl": [1, 2, 3],
        }
    )


def test_roundtrip_parquet_csv_und_manifest(tmp_path):
    df = _beispiel()
    m = Manifest(scale="S")
    erg = exportiere_tabelle(df, "partner", tmp_path, layer="curated", manifest=m, manifest_root=tmp_path)
    assert erg.rows == 3 and erg.columns == 6
    assert set(erg.pfade) == {"parquet", "csv"}

    # CSV: BOM, Konventionen
    roh = erg.pfade["csv"].read_bytes()
    assert roh.startswith(b"\xef\xbb\xbf")
    text = roh.decode("utf-8-sig")
    zeilen = text.split("\n")
    assert zeilen[0] == "partner_id,nachname,geburtsdatum,praemie_betrag,ist_aktiv,anzahl"
    assert zeilen[1] == "PTR-00000001,Müller,1958-03-12,180.00,true,1"
    assert zeilen[3] == "PTR-00000003,,,,true,3"
    assert "\r\n" not in text

    csv_df = lese_csv(erg.pfade["csv"])
    assert list(csv_df["partner_id"]) == list(df["partner_id"])
    assert csv_df["praemie_betrag"].iloc[1] == 95.5

    # Parquet: identischer Inhalt, keine pandas-Metadaten
    pq_df = lese_parquet(erg.pfade["parquet"])
    pd.testing.assert_frame_equal(pq_df[["partner_id", "nachname", "ist_aktiv", "anzahl"]],
                                  df[["partner_id", "nachname", "ist_aktiv", "anzahl"]])
    import pyarrow.parquet as pq

    assert pq.read_schema(erg.pfade["parquet"]).metadata in (None, {})

    # Manifest
    eintrag = m.tables["curated/partner"]
    assert eintrag.rows == 3
    assert eintrag.sha256["csv"] == sha256_datei(erg.pfade["csv"]) == erg.sha256["csv"]
    assert eintrag.files["csv"] == "csv/partner.csv"
    pfad = m.write(tmp_path / "manifest.json")
    geladen = Manifest.load(pfad)
    assert geladen.tables["curated/partner"].sha256 == eintrag.sha256
    assert geladen.master_seed == 20250101 and "synthetisch" in geladen.disclaimer


def test_export_byte_identisch(tmp_path):
    df = _beispiel()
    a = exportiere_tabelle(df, "t", tmp_path / "a")
    b = exportiere_tabelle(df.copy(), "t", tmp_path / "b")
    assert a.sha256 == b.sha256
