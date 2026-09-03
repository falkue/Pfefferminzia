"""Manifest des erzeugten Datensatzes (Datenarchitektur 4.4, Konventionen §7).

Jede Ausgabedatei erhaelt einen SHA-256-Hash. Das Manifest wird von ``export`` befuellt und in der
Stufe ``validate`` geschrieben.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DISCLAIMER_KURZ = (
    "Fiktives Lehrbeispiel. Alle Daten synthetisch. "
    "Keine Verbindung zu realen Personen, Unternehmen oder Marken."
)


def sha256_datei(pfad: Path, blockgroesse: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with Path(pfad).open("rb") as fh:
        for block in iter(lambda: fh.read(blockgroesse), b""):
            h.update(block)
    return h.hexdigest()


def _erzeugt_am() -> str:
    """Zeitstempel UTC; ueber SOURCE_DATE_EPOCH fixierbar (Byte-Identitaet)."""
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    ts = datetime.fromtimestamp(int(epoch), tz=UTC) if epoch else datetime.now(tz=UTC)
    return ts.replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class TabellenEintrag:
    name: str
    layer: str
    rows: int
    columns: int
    files: dict[str, str] = field(default_factory=dict)
    sha256: dict[str, str] = field(default_factory=dict)
    schema: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "name": self.name,
            "layer": self.layer,
            "rows": self.rows,
            "columns": self.columns,
            "files": dict(sorted(self.files.items())),
            "sha256": dict(sorted(self.sha256.items())),
        }
        if self.schema:
            d["schema"] = self.schema
        return d


@dataclass
class Manifest:
    dataset: str = "pfefferminzia"
    version: str = "0.1.0"
    schema_version: str = "0.1.0"
    scale: str = "S"
    stichtag: str = "2025-12-31"
    master_seed: int = 20250101
    config_version: str = "0.1.0"
    license: str = "CC-BY-4.0"
    code_license: str = "MIT"
    generated_at: str = field(default_factory=_erzeugt_am)
    tables: dict[str, TabellenEintrag] = field(default_factory=dict)
    dateien: dict[str, str] = field(default_factory=dict)  # sonstige Dateien: relpfad -> sha256
    disclaimer: str = DISCLAIMER_KURZ

    def add_table(self, eintrag: TabellenEintrag) -> None:
        schluessel = f"{eintrag.layer}/{eintrag.name}"
        vorhanden = self.tables.get(schluessel)
        if vorhanden:
            vorhanden.files.update(eintrag.files)
            vorhanden.sha256.update(eintrag.sha256)
            vorhanden.rows, vorhanden.columns = eintrag.rows, eintrag.columns
        else:
            self.tables[schluessel] = eintrag

    def add_datei(self, relpfad: str, sha: str) -> None:
        self.dateien[relpfad] = sha

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset": self.dataset,
            "version": self.version,
            "schema_version": self.schema_version,
            "scale": self.scale,
            "stichtag": self.stichtag,
            "generated_at": self.generated_at,
            "generator": {
                "repo": "Pfefferminzia",
                "package": "pfefferminzia",
                "master_seed": self.master_seed,
                "config_version": self.config_version,
            },
            "license": self.license,
            "code_license": self.code_license,
            "tables": [self.tables[k].to_dict() for k in sorted(self.tables)],
            "files": dict(sorted(self.dateien.items())),
            "disclaimer": self.disclaimer,
        }

    def write(self, pfad: Path) -> Path:
        pfad = Path(pfad)
        pfad.parent.mkdir(parents=True, exist_ok=True)
        with pfad.open("w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, ensure_ascii=False, indent=2, sort_keys=False)
            fh.write("\n")
        return pfad

    @classmethod
    def load(cls, pfad: Path) -> Manifest:
        with Path(pfad).open("r", encoding="utf-8") as fh:
            d = json.load(fh)
        m = cls(
            dataset=d["dataset"],
            version=d["version"],
            schema_version=d.get("schema_version", "0.1.0"),
            scale=d["scale"],
            stichtag=d["stichtag"],
            master_seed=d["generator"]["master_seed"],
            config_version=d["generator"].get("config_version", "0.1.0"),
            license=d.get("license", "CC-BY-4.0"),
            code_license=d.get("code_license", "MIT"),
            generated_at=d["generated_at"],
            dateien=d.get("files", {}),
            disclaimer=d.get("disclaimer", DISCLAIMER_KURZ),
        )
        for t in d.get("tables", []):
            m.add_table(
                TabellenEintrag(
                    name=t["name"], layer=t["layer"], rows=t["rows"], columns=t["columns"],
                    files=t.get("files", {}), sha256=t.get("sha256", {}), schema=t.get("schema"),
                )
            )
        return m
