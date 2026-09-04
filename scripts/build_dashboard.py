"""Erzeugt ein eigenstaendiges Inspektions-Dashboard ``docs/datensatz/dashboard-<Stufe>.html``.

Aufruf: ``uv run python scripts/build_dashboard.py [S]``

Das Dashboard bettet alle curated-, truth- und migration-Tabellen (als JSON), Ausschnitte der Rohdateien,
die Ergebnisse der Validierungssuite und Kennzahlen ein und laeuft ohne Server im Browser.
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MAX_ZEILEN = 5000  # je Tabelle eingebettet


def lade_tabellen(manifest: dict) -> dict[str, pd.DataFrame]:
    return {f"{t['layer']}/{t['name']}": pd.read_parquet(ROOT / t["files"]["parquet"]) for t in manifest["tables"]}


def spalten_profil(df: pd.DataFrame) -> list[dict]:
    out = []
    for c in df.columns:
        s = df[c]
        nn = s.dropna()
        eintrag = {"name": c, "typ": str(s.dtype), "null_pct": round(100 * s.isna().mean(), 1), "distinct": int(nn.nunique()),
                   "beispiel": "" if nn.empty else str(nn.iloc[0])[:60]}
        if pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s) and not nn.empty:
            eintrag.update({"min": float(nn.min()), "median": float(nn.median()), "max": float(nn.max())})
        elif nn.nunique() <= 12 and not nn.empty:
            vc = nn.astype(str).value_counts().head(12)
            eintrag["werte"] = {str(k): int(v) for k, v in vc.items()}
        out.append(eintrag)
    return out


def zeilen_json(df: pd.DataFrame) -> list[list]:
    d = df.head(MAX_ZEILEN).copy()
    for c in d.columns:
        if pd.api.types.is_datetime64_any_dtype(d[c]):
            d[c] = d[c].dt.strftime("%Y-%m-%d %H:%M")
        elif d[c].dtype == object or str(d[c].dtype).startswith("str"):
            d[c] = d[c].map(lambda v: v if v is None or isinstance(v, (str, int, float, bool)) else str(v))
    d = d.astype(object).where(pd.notna(d), None)
    return d.values.tolist()


def kennzahlen(t: dict[str, pd.DataFrame]) -> dict:
    p, v = t["curated/partner"], t["curated/vertrag"]
    kurs = 0.94
    praemie_chf = float((v.loc[v["status"] == "AKTIV", "jahrespraemie_brutto"] * v.loc[v["status"] == "AKTIV", "waehrung"].map({"CHF": 1.0, "EUR": kurs})).sum())
    beginn_jahr = pd.to_datetime(v["beginn"]).dt.year.value_counts().sort_index()
    return {
        "partner": len(p), "juristisch": int((p["partner_typ"] == "JURISTISCH").sum()), "anteil_ch": round(100 * (p["land_wohnsitz"] == "CH").mean(), 1),
        "vertraege": len(v), "aktiv": int((v["status"] == "AKTIV").sum()), "praemie_aktiv_chf": round(praemie_chf),
        "antraege": len(t["curated/antrag"]), "dq": len(t["truth/dq_injektionen"]) if "truth/dq_injektionen" in t else 0,
        "verteilungen": {
            "Verträge je Produkt": v["produkt_id"].value_counts().to_dict(),
            "Vertragsstatus": v["status"].value_counts().to_dict(),
            "Quellsystem der Verträge": v["quellsystem"].value_counts().to_dict(),
            "Vertriebskanal": v["kanal"].value_counts().to_dict(),
            "Tarifgeneration": v["tarifgeneration_id"].value_counts().to_dict(),
            "Vertragsbeginn je Jahr": {str(k): int(x) for k, x in beginn_jahr.items()},
            "Partner nach Herkunft": p["herkunft"].value_counts().to_dict(),
            "Partner nach Sprache": p["sprache"].value_counts().to_dict(),
            "Underwriting-Entscheid (Anträge)": t["curated/antrag"]["uw_entscheid_code"].value_counts().to_dict(),
            "DQ-Injektionen je Regel": t["truth/dq_injektionen"]["dq_regel"].value_counts().to_dict() if "truth/dq_injektionen" in t else {},
            "Migrationslog": t["migration/migrationslog"]["ergebnis"].value_counts().to_dict() if "migration/migrationslog" in t else {},
        },
    }


def checks(t: dict[str, pd.DataFrame], stufe: str) -> list[dict]:
    from pfefferminzia.context import RunContext
    from pfefferminzia.pipeline import run_pipeline
    from pfefferminzia.validate import run_checks

    ctx = RunContext.erstellen(stufe=stufe, root=ROOT)
    run_pipeline(ctx, nur=["config", "reference"])
    for key, df in t.items():
        layer, name = key.split("/", 1)
        ctx.tabellen.register(name, df, layer=layer, ersetzen=True)
    b = run_checks(ctx)
    return [{"name": e.name, "status": "übersprungen" if e.uebersprungen else ("ok" if e.ok else "FEHLER"),
             "befunde": [{"schwere": x.schwere, "meldung": x.meldung, "tabelle": x.tabelle or ""} for x in e.befunde]} for e in b.ergebnisse]


def rohdaten(manifest: dict, zeilen: int = 25) -> list[dict]:
    out = []
    for f in sorted(manifest["files"]):
        pfad = ROOT / f
        enc = "utf-8" if f.endswith(".jsonl") else "iso-8859-1"
        try:
            with pfad.open(encoding=enc, errors="replace") as fh:
                kopf = [next(fh).rstrip("\r\n") for _ in range(zeilen)]
        except StopIteration:
            kopf = pfad.read_text(encoding=enc, errors="replace").splitlines()[:zeilen]
        out.append({"datei": f, "encoding": enc, "groesse": pfad.stat().st_size, "zeilen": kopf})
    return out


def personas(t: dict[str, pd.DataFrame]) -> list[dict]:
    p = t["curated/partner"]
    v = t["curated/vertrag"]
    out = []
    for _, r in p[p["ist_persona"]].head(20).iterrows():
        vs = v[v["versicherungsnehmer_id"] == r["partner_id"]]
        out.append({"partner_id": r["partner_id"], "name": r["firmenname"] if r["partner_typ"] == "JURISTISCH" else f"{r['vorname']} {r['nachname']}",
                    "land": r["land_wohnsitz"], "vertraege": [f"{x['vertrag_id']} {x['produkt_id']} {x['status']}" for _, x in vs.iterrows()]})
    return out


STYLE = """<title>Pfefferminzia Datenschau {stufe}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {{ --bg:#f3f5f2; --fg:#1e2622; --muted:#63706a; --line:#d6ddd7; --card:#ffffff; --head:#e9efea; --accent:#1c6b4c; --accent-soft:#cfe6da;
        --warn:#a8281f; --ok:#1c6b4c; --code-bg:#1e2622; --code-fg:#e6ece7; --null:#a9b3ac; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#151a17; --fg:#e6ece7; --muted:#98a59d; --line:#2b342e; --card:#1c2320;
        --head:#232c27; --accent:#6fc79b; --accent-soft:#25473a; --warn:#f08a80; --ok:#6fc79b; --code-bg:#0f1311; --code-fg:#d8e0da; --null:#5d6862; }} }}
:root[data-theme="dark"] {{ --bg:#151a17; --fg:#e6ece7; --muted:#98a59d; --line:#2b342e; --card:#1c2320; --head:#232c27; --accent:#6fc79b;
        --accent-soft:#25473a; --warn:#f08a80; --ok:#6fc79b; --code-bg:#0f1311; --code-fg:#d8e0da; --null:#5d6862; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font:14px/1.45 "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; color:var(--fg); background:var(--bg); }}
.kopf {{ padding:18px 24px; background:var(--card); border-bottom:1px solid var(--line); display:flex; gap:24px; align-items:baseline; flex-wrap:wrap; }}
.kopf h1 {{ font-size:20px; margin:0; font-weight:600; letter-spacing:-0.01em; }}
.kopf .meta {{ color:var(--muted); font-size:13px; font-variant-numeric:tabular-nums; }}
nav {{ display:flex; gap:6px; padding:10px 24px; background:var(--card); border-bottom:1px solid var(--line); position:sticky; top:0; z-index:5; flex-wrap:wrap; }}
nav button, .toolbar button {{ border:1px solid var(--line); background:var(--card); color:var(--fg); padding:6px 12px; border-radius:6px; cursor:pointer; font:inherit; }}
nav button.active {{ background:var(--accent); color:var(--bg); border-color:var(--accent); }}
nav button:focus-visible, .list button:focus-visible, input:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
main {{ padding:20px 24px; }}
section {{ display:none; }} section.active {{ display:block; }}
.tiles {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(170px, 1fr)); gap:12px; margin-bottom:20px; }}
.tile {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:12px 14px; }}
.tile .v {{ font-size:24px; font-weight:600; font-variant-numeric:tabular-nums; }} .tile .l {{ color:var(--muted); font-size:12px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:14px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:12px 14px; }}
.card h3 {{ margin:0 0 8px; font-size:14px; font-weight:600; }}
.bar {{ display:grid; grid-template-columns:150px 1fr 60px; gap:8px; align-items:center; font-size:12px; margin:2px 0; }}
.bar .k {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.bar .b {{ height:14px; background:var(--accent-soft); border-radius:3px; }}
.bar .b span {{ display:block; height:100%; background:var(--accent); border-radius:3px; }}
.bar .n {{ text-align:right; color:var(--muted); font-variant-numeric:tabular-nums; }}
.layout {{ display:grid; grid-template-columns:260px 1fr; gap:16px; }}
@media (max-width: 800px) {{ .layout {{ grid-template-columns:1fr; }} }}
.list {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:6px; max-height:75vh; overflow:auto; }}
.list button {{ display:block; width:100%; text-align:left; border:0; background:none; color:var(--fg); padding:6px 8px; border-radius:5px; cursor:pointer; font:inherit; }}
.list button.active {{ background:var(--accent-soft); }}
.list .layer {{ color:var(--muted); font-size:11px; text-transform:uppercase; letter-spacing:0.06em; padding:8px 8px 2px; }}
.list small {{ color:var(--muted); float:right; font-variant-numeric:tabular-nums; }}
.tablewrap {{ overflow:auto; max-height:60vh; border:1px solid var(--line); border-radius:8px; background:var(--card); }}
table {{ border-collapse:collapse; font-size:12px; white-space:nowrap; font-family:"IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace; font-variant-numeric:tabular-nums; }}
th, td {{ padding:4px 8px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }}
th {{ position:sticky; top:0; background:var(--head); cursor:pointer; font-family:"IBM Plex Sans", system-ui, sans-serif; font-weight:600; }}
td.null {{ color:var(--null); font-style:italic; }}
.toolbar {{ display:flex; gap:10px; align-items:center; margin:8px 0; flex-wrap:wrap; }}
input[type=search] {{ padding:6px 10px; border:1px solid var(--line); border-radius:6px; font:inherit; min-width:260px; background:var(--card); color:var(--fg); }}
.prof td {{ white-space:normal; font-family:"IBM Plex Sans", system-ui, sans-serif; }}
.ok {{ color:var(--ok); font-weight:600; }} .fehler {{ color:var(--warn); font-weight:600; }}
pre {{ background:var(--code-bg); color:var(--code-fg); padding:12px; border-radius:8px; overflow:auto; font:12px/1.4 "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace; }}
details {{ margin-bottom:10px; }} summary {{ cursor:pointer; font-weight:600; }}
.muted {{ color:var(--muted); }}
.fuss {{ padding:16px 24px; color:var(--muted); font-size:12px; border-top:1px solid var(--line); }}
</style>
"""

BODY = """<div class="kopf"><h1>Pfefferminzia – Datenschau Stufe {stufe}</h1>
<div class="meta">Stichtag {stichtag} · Master-Seed {seed} · Version {version} · erzeugt {generated}</div></div>
<nav>
<button data-s="uebersicht" class="active">Übersicht</button>
<button data-s="tabellen">Tabellen</button>
<button data-s="qualitaet">Qualität</button>
<button data-s="rohdaten">Rohdaten</button>
<button data-s="personas">Personas</button>
</nav>
<main>
<section id="uebersicht" class="active">
  <div class="tiles" id="tiles"></div>
  <div class="grid" id="charts"></div>
</section>
<section id="tabellen">
  <div class="layout">
    <div class="list" id="tablist"></div>
    <div>
      <div class="toolbar">
        <strong id="tname"></strong><span class="muted" id="tinfo"></span>
        <input type="search" id="search" placeholder="Zeilen filtern (alle Spalten) …" aria-label="Zeilen filtern">
        <label><input type="checkbox" id="showprofile" checked> Spaltenprofil</label>
        <span class="muted" id="pageinfo"></span>
        <button id="prev" aria-label="vorherige Seite">‹</button><button id="next" aria-label="nächste Seite">›</button>
      </div>
      <div id="profile"></div>
      <div class="tablewrap"><table id="grid"></table></div>
    </div>
  </div>
</section>
<section id="qualitaet">
  <div class="grid" id="checks"></div>
  <h3>Datenqualitäts-Injektionen (truth/dq_injektionen)</h3>
  <p class="muted">Jede Zeile ist ein bewusst eingebauter Fehler in den Rohdaten mit Originalwert. Die Regeln DQ-01 bis DQ-28 sind in der Datenarchitektur-Planung beschrieben.</p>
  <div id="dqchart" class="card"></div>
</section>
<section id="rohdaten"><div id="raw"></div></section>
<section id="personas"><div id="pers" class="grid"></div></section>
</main>
<div class="fuss">Fiktives Lehrbeispiel. Alle Daten synthetisch. Keine Verbindung zu realen Personen, Unternehmen oder Marken.</div>
<script id="data" type="application/json">{daten}</script>
"""

SCRIPT = r"""<script>
const D = JSON.parse(document.getElementById('data').textContent);
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmt = n => typeof n === 'number' ? n.toLocaleString('de-CH') : n;
document.querySelectorAll('nav button').forEach(b => b.onclick = () => {
  document.querySelectorAll('nav button').forEach(x => x.classList.toggle('active', x === b));
  document.querySelectorAll('main section').forEach(s => s.classList.toggle('active', s.id === b.dataset.s));
});
// Übersicht
const K = D.kennzahlen;
$('#tiles').innerHTML = [
  ['Partner', K.partner], ['davon juristisch', K.juristisch], ['Anteil Schweiz', K.anteil_ch + ' %'], ['Verträge', K.vertraege],
  ['davon aktiv', K.aktiv], ['Jahresprämie aktiv (CHF)', fmt(K.praemie_aktiv_chf)], ['Anträge', K.antraege], ['DQ-Injektionen', K.dq],
  ['Tabellen', D.tables.length], ['Rohdateien', D.raw.length]
].map(([l, v]) => `<div class="tile"><div class="v">${fmt(v)}</div><div class="l">${l}</div></div>`).join('');
function bars(obj, sortByKey) {
  const entries = Object.entries(obj); if (sortByKey) entries.sort((a, b) => a[0].localeCompare(b[0])); else entries.sort((a, b) => b[1] - a[1]);
  const max = Math.max(...entries.map(e => e[1]), 1);
  return entries.map(([k, v]) => `<div class="bar"><div class="k" title="${esc(k)}">${esc(k)}</div><div class="b"><span style="width:${100 * v / max}%"></span></div><div class="n">${fmt(v)}</div></div>`).join('');
}
$('#charts').innerHTML = Object.entries(K.verteilungen).map(([t, o]) => `<div class="card"><h3>${esc(t)}</h3>${bars(o, t.includes('Jahr'))}</div>`).join('');
// Tabellen
let cur = null, page = 0, sortCol = null, sortDir = 1, filtered = [];
const PAGE = 50;
$('#tablist').innerHTML = ['curated', 'migration', 'truth'].map(layer => `<div class="layer">${layer}</div>` +
  D.tables.filter(t => t.layer === layer).map(t => `<button data-key="${t.layer}/${t.name}">${t.name}<small>${fmt(t.rows)}</small></button>`).join('')).join('');
document.querySelectorAll('#tablist button').forEach(b => b.onclick = () => openTable(b.dataset.key));
function openTable(key) {
  cur = D.tables.find(t => t.layer + '/' + t.name === key); page = 0; sortCol = null; $('#search').value = '';
  document.querySelectorAll('#tablist button').forEach(b => b.classList.toggle('active', b.dataset.key === key));
  $('#tname').textContent = key; $('#tinfo').textContent = ` ${fmt(cur.rows)} Zeilen, ${cur.columns.length} Spalten` + (cur.rows > cur.data.length ? ` (${cur.data.length} eingebettet)` : '') + ' – ' + (cur.beschreibung || '');
  renderProfile(); applyFilter();
}
function renderProfile() {
  if (!$('#showprofile').checked) { $('#profile').innerHTML = ''; return; }
  $('#profile').innerHTML = `<details open><summary>Spaltenprofil</summary><div class="tablewrap" style="max-height:32vh"><table class="prof"><tr><th>Spalte</th><th>Typ</th><th>Null %</th><th>Distinct</th><th>Min / Median / Max bzw. Werte</th><th>Beispiel</th></tr>` +
    cur.profil.map(c => `<tr><td>${esc(c.name)}</td><td>${esc(c.typ)}</td><td>${c.null_pct}</td><td>${fmt(c.distinct)}</td><td>${c.min !== undefined ? `${fmt(c.min)} / ${fmt(c.median)} / ${fmt(c.max)}` : (c.werte ? Object.entries(c.werte).map(([k, v]) => `${esc(k)} (${v})`).join(', ') : '')}</td><td>${esc(c.beispiel)}</td></tr>`).join('') + '</table></div></details>';
}
$('#showprofile').onchange = renderProfile;
function applyFilter() {
  const q = $('#search').value.toLowerCase();
  filtered = cur.data.filter(r => !q || r.some(v => v !== null && String(v).toLowerCase().includes(q)));
  if (sortCol !== null) filtered.sort((a, b) => { const x = a[sortCol], y = b[sortCol]; if (x === null) return 1; if (y === null) return -1; return (x > y ? 1 : x < y ? -1 : 0) * sortDir; });
  page = Math.min(page, Math.max(0, Math.ceil(filtered.length / PAGE) - 1)); renderGrid();
}
function renderGrid() {
  const rows = filtered.slice(page * PAGE, (page + 1) * PAGE);
  $('#grid').innerHTML = '<tr>' + cur.columns.map((c, i) => `<th data-i="${i}">${esc(c)}${sortCol === i ? (sortDir > 0 ? ' ▲' : ' ▼') : ''}</th>`).join('') + '</tr>' +
    rows.map(r => '<tr>' + r.map(v => v === null ? '<td class="null">null</td>' : `<td>${esc(v)}</td>`).join('') + '</tr>').join('');
  document.querySelectorAll('#grid th').forEach(th => th.onclick = () => { const i = +th.dataset.i; sortDir = sortCol === i ? -sortDir : 1; sortCol = i; applyFilter(); });
  $('#pageinfo').textContent = `${fmt(filtered.length)} Treffer · Seite ${page + 1} / ${Math.max(1, Math.ceil(filtered.length / PAGE))}`;
}
$('#search').oninput = () => { page = 0; applyFilter(); };
$('#prev').onclick = () => { if (page > 0) { page--; renderGrid(); } };
$('#next').onclick = () => { if ((page + 1) * PAGE < filtered.length) { page++; renderGrid(); } };
openTable('curated/vertrag');
// Qualität
$('#checks').innerHTML = D.checks.map(c => `<div class="card"><h3>${esc(c.name)} <span class="${c.status === 'ok' ? 'ok' : 'fehler'}">${c.status}</span></h3>` +
  (c.befunde.length ? '<ul>' + c.befunde.map(b => `<li><b>${b.schwere}</b>: ${esc(b.meldung)} <span class="muted">${esc(b.tabelle)}</span></li>`).join('') + '</ul>' : '<p class="muted">keine Befunde</p>') + '</div>').join('');
$('#dqchart').innerHTML = bars(K.verteilungen['DQ-Injektionen je Regel'] || {});
// Rohdaten
$('#raw').innerHTML = D.raw.map(r => `<details ${r.datei.includes('PARTNER.txt') || r.datei.includes('customers') ? 'open' : ''}><summary>${esc(r.datei)} <span class="muted">(${r.encoding}, ${fmt(r.groesse)} Bytes, erste ${r.zeilen.length} Zeilen)</span></summary><pre>${esc(r.zeilen.join('\\n'))}</pre></details>`).join('');
// Personas
$('#pers').innerHTML = D.personas.map(p => `<div class="card"><h3>${esc(p.partner_id)} – ${esc(p.name)} <span class="muted">${p.land}</span></h3>` +
  (p.vertraege.length ? '<ul>' + p.vertraege.map(v => `<li>${esc(v)}</li>`).join('') + '</ul>' : '<p class="muted">keine eigenen Verträge (Bezugsperson)</p>') + '</div>').join('');
</script>
"""


def main(stufe: str = "S") -> None:
    manifest = json.loads((ROOT / f"data/manifest_{stufe}.json").read_text(encoding="utf-8"))
    t = lade_tabellen(manifest)
    from build_data_dictionary import BESCHREIBUNG  # noqa: E402

    tables = []
    for key, df in t.items():
        layer, name = key.split("/", 1)
        tables.append({"layer": layer, "name": name, "rows": len(df), "columns": list(df.columns), "profil": spalten_profil(df),
                       "data": zeilen_json(df), "beschreibung": BESCHREIBUNG.get(key, "")})
    daten = {"tables": tables, "kennzahlen": kennzahlen(t), "checks": checks(t, stufe), "raw": rohdaten(manifest), "personas": personas(t)}
    js = json.dumps(daten, ensure_ascii=False, default=str).replace("</", "<\\/")
    felder = dict(stufe=stufe, stichtag=manifest["stichtag"], seed=manifest["generator"]["master_seed"], version=manifest["version"],
                  generated=html.escape(manifest["generated_at"]), daten=js)
    inhalt = STYLE.format(**felder) + BODY.format(**felder) + SCRIPT
    # Artifact-Variante: nur Seiteninhalt (der Host liefert den Dokumentrahmen)
    ziel_a = ROOT / "docs" / "datensatz" / f"dashboard-{stufe}.artifact.html"
    ziel_a.write_text(inhalt, encoding="utf-8")
    # Lokale Variante: vollstaendiges Dokument
    ziel = ROOT / "docs" / "datensatz" / f"dashboard-{stufe}.html"
    ziel.write_text('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                    + STYLE.format(**felder) + '</head>\n<body>\n' + BODY.format(**felder) + SCRIPT + '</body>\n</html>\n', encoding="utf-8")
    for z in (ziel, ziel_a):
        print(z.relative_to(ROOT), f"{z.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main(sys.argv[1] if len(sys.argv) > 1 else "S")
