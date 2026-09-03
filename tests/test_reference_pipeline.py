import pytest

from pfefferminzia.pipeline import auswahl, run_pipeline, stage_names
from pfefferminzia.reference import ReferenceLoader, ReferenzFehltError


def test_stufenreihenfolge():
    assert stage_names() == [
        "config", "reference", "organisation", "partner", "vertrag", "schaden", "finanz", "prozess",
        "text", "render", "legacyify", "mintify", "export", "validate",
    ]
    assert [s.name for s in auswahl("partner", "schaden")] == ["partner", "vertrag", "schaden"]
    assert [s.name for s in auswahl(nur=["export"])] == ["export"]
    with pytest.raises(KeyError):
        auswahl(nur=["gibt_es_nicht"])


def test_reference_loader_fehlermeldung(tmp_path):
    ldr = ReferenceLoader(tmp_path)
    with pytest.raises(ReferenzFehltError) as exc:
        ldr.csv("kennzahlen_master")
    assert "Team Unternehmen" in str(exc.value) and "organisation" in str(exc.value)
    with pytest.raises(ReferenzFehltError):
        ldr.csv("irgendwas/unbekannt.csv")
    status = {s.schluessel: s for s in ldr.status()}
    assert not status["geo.orte_ch"].vorhanden


def test_reference_loader_geo_und_namen(root):
    ldr = ReferenceLoader(root / "data" / "reference")
    ch = ldr.csv("geo.orte_ch")
    assert 150 <= len(ch) <= 250
    assert str(ch["plz"].dtype) == "string" and ch["plz"].str.len().eq(4).all()
    assert (ch["ort"] == "Olten").any()
    assert set(ch["kanton"]) == {
        "AG", "AI", "AR", "BE", "BL", "BS", "FR", "GE", "GL", "GR", "JU", "LU", "NE", "NW", "OW",
        "SG", "SH", "SO", "SZ", "TG", "TI", "UR", "VD", "VS", "ZG", "ZH",
    }
    de = ldr.csv("geo.orte_de")
    assert 300 <= len(de) <= 400 and de["plz"].str.len().eq(5).all()
    assert de["bundesland_kuerzel"].nunique() == 16
    st = ldr.csv("geo.strassennamen")
    assert (st.groupby("sprache").size() >= 400).all()
    assert not st.duplicated(["strasse", "sprache"]).any()
    vn = ldr.csv("namen.vornamen")
    assert len(vn) >= 400 and {"g_1930", "g_2000"} <= set(vn.columns)
    nn = ldr.csv("namen.nachnamen")
    assert len(nn) >= 500
    bl = ldr.csv("namen.blocklist")
    assert {"person", "firma"} <= set(bl["typ"])
    assert ldr.csv("geo.orte_ch") is ch  # Cache
    assert ldr.csv("namen.firmennamen_bausteine")["art"].isin(["stamm", "branche", "rechtsform"]).all()


def test_pipeline_stubs_und_export(ctx):
    import pandas as pd

    ergebnisse = run_pipeline(ctx, bis="reference")
    assert all(e.ok for e in ergebnisse)
    assert ctx.tabellen.has("geo_orte_ch", "reference")
    ctx.tabellen.register("partner", pd.DataFrame({"partner_id": ["PTR-00000001"], "vorname": ["Lea"],
                                                   "nachname": ["Brunner"], "email": ["lea@web.example"]}))
    ergebnisse = run_pipeline(ctx, von="organisation")
    assert all(e.ok for e in ergebnisse)
    assert (ctx.pfade.curated / "S" / "parquet" / "partner.parquet").exists()
    assert (ctx.pfade.curated / "S" / "csv" / "partner.csv").exists()
    assert (ctx.pfade.manifest.parent / "manifest_S.json").exists()


def test_validate_checks_auf_referenzen(ctx):
    import pandas as pd

    from pfefferminzia.validate import run_checks

    run_pipeline(ctx, bis="reference")
    bericht = run_checks(ctx)
    assert bericht.ok, [b for e in bericht.ergebnisse for b in e.befunde if b.schwere == "FEHLER"]
    # Blocklist und Domain-Check schlagen bei Verstoessen an
    ctx.tabellen.register("partner", pd.DataFrame({
        "partner_id": ["PTR-00000001", "PTR-00000001"],
        "vorname": ["Roger", "Lea"], "nachname": ["Federer", "Brunner"],
        "email": ["a@b.example", "x@example.com"], "telefon": ["+41 44 000 12 34", "+41 44 123 45 67"],
    }))
    bericht = run_checks(ctx)
    namen = {e.name: e for e in bericht.ergebnisse}
    assert not namen["blocklist_personen"].ok
    assert not namen["domains_telefon"].ok
    assert not namen["primaerschluessel"].ok
