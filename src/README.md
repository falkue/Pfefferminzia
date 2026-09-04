# Pfefferminzia – Generator (Entwicklerdokumentation)

Python-Paket `pfefferminzia` unter `src/pfefferminzia/`. Es erzeugt den synthetischen Lehr-Datensatz des
fiktiven Versicherers Pfefferminzia gemäss `docs/planung/00-gesamtplan.md` und
`docs/planung/03-datenarchitektur.md`. Verbindliche Regeln: `docs/konventionen.md`, `docs/entscheidungen.md`.

Lizenz des Codes: MIT. Daten und Texte: CC BY 4.0.

## Setup

Voraussetzungen: `uv` (≥ 0.5) und Python 3.12 (`.python-version`).

```bash
uv sync                      # legt .venv an, installiert Paket und Dev-Abhaengigkeiten
uv run pfefferminzia --help  # CLI
uv run pytest                # Tests
uv run ruff check            # Lint
```

`uv.lock` wird versioniert (Reproduzierbarkeit). `.venv/` ist ignoriert.

## Befehle

| Befehl | Zweck |
|---|---|
| `uv run pfefferminzia generate --stufe S` | Pipeline für Stufe S (M, L) ausführen |
| `uv run pfefferminzia generate --stufe S --von partner --bis schaden` | Teilbereich der Pipeline |
| `uv run pfefferminzia generate --nur config --nur reference` | Nur ausgewählte Stufen |
| `uv run pfefferminzia validate --stufe S` | Checks-Registry auf Referenzdaten (und geladenen Tabellen) ausführen |
| `uv run pfefferminzia reference check` | Zeigt, welche Referenzdateien vorhanden sind (Team, Stufe, Zeilenzahl) |
| `uv run pfefferminzia reference show geo.orte_ch -n 5` | Kopf einer Referenzdatei |

Alle Pfade sind relativ zur Projektwurzel (Ordner mit `pyproject.toml`, überschreibbar mit
`PFEFFERMINZIA_ROOT`). Konfiguration: `config/generator.yaml` (`--config` für Alternativen).

## Modulschnitt

| Modul | Inhalt |
|---|---|
| `paths.py` | Projektwurzel, Standardpfade |
| `config.py` | Pydantic-Modelle für `config/generator.yaml`: Seed, Zeitachse, Markt, Stufen S/M/L mit Mengengerüst, Pfade, Fallen, DQ-Raten, LLM, Export. `load_config()` validiert u. a. `S ⊂ M ⊂ L`. |
| `seeds.py` | `MASTER_SEED = 20250101`, `derive_seed(modul, entity_id)` = erste 8 Bytes von `sha256("{master}:{modul}:{entity_id}")`, `rng_for(...)` liefert `numpy.random.Generator(PCG64)`, `faker_for(...)` nur für Formate. |
| `ids.py` | curated-IDs (`PTR-00012345`, `VTR-`, `ANT-`, `SCH-`, `DOK-`, `INT-`, `MIT-00123`, `VRM-00123`, `AGT-0012`, `RW-HP-AVB-CH-2025`), Produkt- und Tarifgenerationskürzel, Legacy-Formate VERA `L-0098765`, HAPO `40.987.112-3` (Modulo-10-rekursiv-Prüfziffer), SILAS `S2019/004512`, DOKU `DOKU-0000123456`, Legacy-Partnernummern je Nummernkreis, MINT-UUID v4 deterministisch aus Seed. |
| `reference.py` | `ReferenceLoader` für CSV/YAML/Glob/Ordner unter `data/reference/` mit Cache; Katalog `REFERENZEN` (Schlüssel, Pfad, Team, benötigt ab Stufe); `ReferenzFehltError` mit klarer Meldung. |
| `context.py` | `RunContext` (Konfiguration, Stufe, Pfade, `TabellenRegistry` im Speicher als `<layer>/<name>`, Manifest, Ereignisprotokoll, `ctx.rng(modul, id)`). |
| `pipeline.py` | `Stage`-Basisklasse, `@register`, Stufen `config → reference → organisation → partner → vertrag → schaden → finanz → prozess → text → render → legacyify → mintify → export → validate`, `run_pipeline(ctx, von, bis, nur)`. Fachstufen sind Stubs mit Logging. |
| `export.py` | `exportiere_tabelle()` schreibt Parquet (Snappy, ohne pandas-Metadaten) und CSV (UTF-8 mit BOM, Komma, `\n`, ISO-Datum, `true`/`false`, Null = leer) und trägt SHA-256 ins Manifest ein. |
| `manifest.py` | `Manifest`/`TabellenEintrag`, `sha256_datei()`, Kurz-Disclaimer; `SOURCE_DATE_EPOCH` fixiert den Zeitstempel. |
| `validate/` | Checks-Registry (`@check`), `run_checks(ctx)`, Basis-Checks: `schema` (pandera-Schemas je Tabelle in `SCHEMAS`), `referenzintegritaet`/`primaerschluessel` (`FK_BEZIEHUNGEN`), `blocklist_personen`, `domains_telefon`. |
| `synth/identifiers.py` | Prüfziffernvalide, fiktive IBAN CH (Clearing 99999) / DE (BLZ 99999999), AHV-Nummer (EAN-13), Steuer-ID (ISO 7064 MOD 11,10 inkl. Mehrfachziffer-Regel), CH-UID (`CHE-499.xxx.xxx`, Modulo 11), Telefonnummern der Fiktionsbereiche, `.example`-E-Mails, fiktive Kennzeichen. |
| `synth/names.py` | `NameSynth` (Vorname nach Geschlecht/Sprachraum/Dekade, Nachname nach Sprachraum, Blocklist-Neuziehung), `firmenname()` aus Bausteinen. |
| `synth/addresses.py` | `AddressSynth` (Ort nach Gewicht/Sprachregion/Region, generierte Strasse, Hausnummer 1–180), `geo_versatz()`. |
| `tarifblaetter.py` | Rendert die Tarifgenerationen aus den HP-/LV-Referenztabellen als reproduzierbare Markdown- und PDF-Tarifblätter. |
| `cli.py` | typer-App. |

## Eine Stufe implementieren

1. Klasse in `pipeline.py` (oder in einem eigenen Modul, das `pipeline` importiert) mit `@register`:

   ```python
   @register
   class PartnerStage(Stage):
       name, nummer, welle = "partner", 30, 1
       beschreibung = "Partner, Adressen, Kontakte"

       def run(self, ctx: RunContext) -> None:
           orte = ctx.reference.csv("geo.orte_ch")
           n = ctx.menge("partner")
           zeilen = []
           for i in range(1, n + 1):
               pid = ids.partner_id(i)
               rng = ctx.rng("partner", pid)      # ein Generator je Entität
               ...
           ctx.tabellen.register("partner", pd.DataFrame(zeilen))          # layer curated
           ctx.tabellen.register("kunde_latent", latent, layer="truth")
           ctx.ereignis(self.name, f"{n} Partner erzeugt")
   ```

2. Regeln: kein globaler Zufall (`ctx.rng(modul, entity_id)` je Entität), IDs nur aus `ids.py` und aus
   laufenden Nummern (stabil über Stufen S/M/L: Stufe S sind die ersten `menge()` Nummern der Welt M),
   Mengen aus `ctx.menge(...)`, Referenzen über `ctx.reference`, Fallen über `ctx.config.fallen.aktiv(...)`
   und `.staerke(...)`, DQ-Raten über `ctx.config.dq.raten`.
3. Tabellen in `ctx.tabellen` registrieren; die Stufe `export` schreibt alle Nicht-Referenz-Tabellen in
   `data/<layer>/<stufe>/{parquet,csv}/`, `validate` schreibt `data/manifest_<stufe>.json`.
4. Schema in `validate/schema.py` (`SCHEMAS["curated/partner"] = pa.DataFrameSchema(...)`) und
   FK-Beziehungen in `validate/integrity.py` ergänzen; zusätzliche Checks mit `@check(...)`.
5. Tests unter `tests/` (Determinismus: zwei Läufe mit gleichem Seed → identische Hashes).

## Referenzdaten anderer Teams

`reference check` zeigt, welche Dateien noch fehlen (`kennzahlen_master.yaml`, `organisationseinheiten.csv`,
`standorte.csv`, `systeme.csv`, `personas_*.csv`, `hp/`, `lv/`). Der Loader setzt sie nicht voraus; Stufen,
die sie brauchen, sollen `ctx.reference.vorhanden(...)` prüfen und mit `ReferenzFehltError` abbrechen.

---

Fiktives Lehrbeispiel. Alle Daten synthetisch. Keine Verbindung zu realen Personen, Unternehmen oder Marken.
