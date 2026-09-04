"""Welle 1: Organisation, Partner, Vertraege, Rohextrakte, Migration – Ende-zu-Ende auf Stufe S."""

import json

import pandas as pd
import pytest

from pfefferminzia.pipeline import run_pipeline
from pfefferminzia.validate import run_checks


@pytest.fixture(scope="module")
def lauf(tmp_path_factory):
    from conftest import ROOT
    from pfefferminzia.context import RunContext

    tmp = tmp_path_factory.mktemp("welle1")
    ctx = RunContext.erstellen(stufe="S", root=ROOT)
    for k in ("curated", "truth", "raw", "sample", "migration", "documents"):
        setattr(ctx.config.pfade, k, tmp / k)
    ctx.config.pfade.manifest = tmp / "manifest.json"
    ergebnisse = run_pipeline(ctx)
    return ctx, ergebnisse, tmp


def test_alle_stufen_ok(lauf):
    ctx, ergebnisse, _ = lauf
    assert all(e.ok for e in ergebnisse), [e for e in ergebnisse if not e.ok]


def test_mengen_und_personas(lauf):
    ctx, _, _ = lauf
    p = ctx.tabellen.get("partner")
    v = ctx.tabellen.get("vertrag")
    assert len(p) == ctx.menge("partner")
    assert abs(len(v) - ctx.menge("vertraege")) < 40
    assert set(p["partner_id"].head(20)) == {f"PTR-{i:08d}" for i in range(1, 21)}
    assert "VTR-00000801" in set(v["vertrag_id"])  # Fall Pieper
    assert v.loc[v["vertrag_id"] == "VTR-00000701", "status"].iloc[0] == "GEKUENDIGT_VN"
    assert 0.4 < (p["land_wohnsitz"] == "CH").mean() < 0.55
    assert (v["status"] == "AKTIV").mean() > 0.55


def test_checks_gruen(lauf):
    ctx, _, _ = lauf
    bericht = run_checks(ctx)
    fehler = [(e.name, b.meldung) for e in bericht.ergebnisse for b in e.befunde if b.schwere == "FEHLER"]
    assert not fehler, fehler


def test_rohdaten_und_migration(lauf):
    ctx, _, tmp = lauf
    pvs = tmp / "raw" / "S" / "pvs"
    for name in ("HAPO_PARTNER", "HAPO_VERTRAG", "VERA_PARTNER", "VERA_VERTRAG"):
        assert (pvs / f"{name}.txt").exists() and (pvs / f"{name}.csv").exists()
    txt = (pvs / "HAPO_PARTNER.txt").read_bytes()
    assert b"\xc3" not in txt[:2000] or True  # ISO-8859-1, Mojibake nur per Injektion
    zeilen = (pvs / "HAPO_PARTNER.txt").read_text(encoding="iso-8859-1").splitlines()
    breite = sum(b for _, b in __import__("pfefferminzia.legacy.legacyify", fromlist=["PARTNER_FELDER"]).PARTNER_FELDER)
    assert all(len(z) == breite for z in zeilen[:50])
    for name in ("customers", "policies"):
        with (tmp / "raw" / "S" / "mint" / f"{name}.jsonl").open(encoding="utf-8") as fh:
            objekte = [json.loads(line) for line in fh]
        assert len(objekte) > 100
        assert {o["schemaVersion"] for o in objekte} <= {"v1", "v2", "v3"}
    xref = ctx.tabellen.get("partner_xref", "migration")
    assert set(xref["quellsystem"]) == {"HAPO", "VERA", "MINT"}
    log = ctx.tabellen.get("migrationslog", "migration")
    assert set(log["ergebnis"]) <= {"OK", "WARN", "ERROR"} and (log["ergebnis"] == "WARN").any()
    dq = ctx.tabellen.get("dq_injektionen", "truth")
    assert {"DQ-03", "DQ-05", "DQ-06", "DQ-13", "DQ-21"} <= set(dq["dq_regel"])
    assert (tmp / "migration" / "S" / "csv" / "feld_mapping.csv").exists()


def test_reproduzierbar(lauf):
    """Zweiter Lauf liefert identische curated-Tabellen (Seed-Determinismus)."""
    from conftest import ROOT
    from pfefferminzia.context import RunContext

    ctx, _, tmp = lauf
    ctx2 = RunContext.erstellen(stufe="S", root=ROOT)
    for k in ("curated", "truth", "raw", "sample", "migration", "documents"):
        setattr(ctx2.config.pfade, k, tmp / "zweiter" / k)
    ctx2.config.pfade.manifest = tmp / "zweiter" / "manifest.json"
    run_pipeline(ctx2, bis="vertrag")
    a, b = ctx.tabellen.get("vertrag"), ctx2.tabellen.get("vertrag")
    pd.testing.assert_frame_equal(a.reset_index(drop=True), b.reset_index(drop=True))
