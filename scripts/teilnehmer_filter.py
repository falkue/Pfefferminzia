#!/usr/bin/env python3
"""Entfernt Loesungs- und Dozenteninhalte aus einem Arbeitsbaum fuer den Zweig ``teilnehmer``.

Wird von ``scripts/build_teilnehmer_branch.sh`` im temporaeren Arbeitsbaum aufgerufen, nachdem dort der
verwaiste Zweig ``teilnehmer`` angelegt wurde. Aendert nur Dateien in diesem Arbeitsbaum, nie ``main``.

Was entfernt wird:
1. Ganze Pfade: ``data/truth``, Akten-Quelltexte, ``docs/stammdaten`` (Dozentenerlaeuterungen), ``docs/planung``
   (Fallenkatalog, Loesungsheft, Stolpersteine mit Aufloesung), die Datenschau ``docs/datensatz/dashboard-S*.html``
   (bettet die latente Wahrheit ein).
2. Markdown-Abschnitte ab einer passenden Ueberschrift bis zur naechsten gleich- oder hoeherrangigen Ueberschrift:
   in Persona-Steckbriefen «Rolle im Datensatz», ueberall Ueberschriften mit «Ground Truth», «Wahrheit», «Loesung»,
   «Dozent», «Trainer», «Fallenkatalog», «Stolperstein» sowie die ``truth/``-Tabellen im Data Dictionary.
3. Einzelne Zeilen und Randvermerke: Tabellenzeilen ``| truth/…`` im Data Dictionary, Verweise auf entfernte
   Ordner im README, Vermerke «Ground Truth: …», «(Stolperstein …)», «Muster F…» in den Persona-Geschichten,
   ``didaktik_falle``/``didaktik_hinweis`` in den Annahmerichtlinien-Tabellen, der Bias-Vermerk in
   ``underwriting_entscheidungen.csv``.

Aufruf (nur im Arbeitsbaum des Zweigs teilnehmer): ``python3 scripts/teilnehmer_filter.py``
Das Skript bricht ab, wenn der ausgecheckte Zweig nicht ``teilnehmer`` heisst.
"""

from __future__ import annotations

import csv
import io
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()

PFADE_ENTFERNEN = [
    "data/truth",
    "src/pfefferminzia/synth/akten_inhalte.py",
    "src/pfefferminzia/synth/akten_inhalte_2.py",
    "docs/stammdaten",
    "docs/planung",
    "docs/datensatz/dashboard-S.html",
    "docs/datensatz/dashboard-S.artifact.html",
]

# Ueberschriften, deren Abschnitt ueberall (docs/, data/documents/, kurs/, Wurzel) entfernt wird
UEBERSCHRIFT_UEBERALL = re.compile(
    r"ground[\s-]?truth|wahrheit|l(ö|oe)sung(en|sheft|sskizze)?\b|musterl(ö|oe)sung|dozent|trainer|fallenkatalog|stolperstein",
    re.IGNORECASE,
)
# Zusaetzlich in Persona-Steckbriefen
UEBERSCHRIFT_PERSONAS = re.compile(r"^rolle im datensatz$", re.IGNORECASE)
# Zusaetzlich im Data Dictionary: Beschreibung der truth-Tabellen
UEBERSCHRIFT_DATA_DICTIONARY = re.compile(r"^truth/", re.IGNORECASE)

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")

protokoll: list[str] = []


def pruefe_zweig() -> None:
    zweig = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    if zweig != "teilnehmer":
        sys.exit(f"Abbruch: ausgecheckt ist «{zweig or 'kein Zweig'}», erwartet «teilnehmer». main wird nie gefiltert.")


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def streiche_abschnitte(text: str, passt) -> tuple[str, list[str]]:
    """Entfernt Abschnitte ab passender Ueberschrift bis zur naechsten Ueberschrift gleicher oder hoeherer Ebene."""
    zeilen = text.split("\n")
    aus, gestrichen = [], []
    im_code = False
    skip_ebene: int | None = None
    for z in zeilen:
        if FENCE.match(z):
            im_code = not im_code
        m = None if im_code else HEADING.match(z)
        if skip_ebene is not None:
            if m and len(m.group(1)) <= skip_ebene:
                skip_ebene = None
            else:
                continue
        if m and passt(m.group(2)):
            skip_ebene = len(m.group(1))
            gestrichen.append(m.group(2))
            # Leerzeilen vor dem gestrichenen Abschnitt nicht verdoppeln
            while aus and aus[-1].strip() == "":
                aus.pop()
            aus.append("")
            continue
        aus.append(z)
    return "\n".join(aus), gestrichen


def ersetze(text: str, muster: str, ersatz: str, flags: int = 0) -> tuple[str, int]:
    return re.subn(muster, ersatz, text, flags=flags)


def markdown_dateien() -> list[Path]:
    dateien = []
    for basis in ("docs", "data/documents", "kurs"):
        dateien += sorted((ROOT / basis).rglob("*.md"))
    dateien += sorted(ROOT.glob("*.md"))
    return dateien


def filtere_markdown() -> None:
    for p in markdown_dateien():
        r = rel(p)
        text = p.read_text(encoding="utf-8")
        neu = text

        def passt(titel: str, r=r) -> bool:
            if UEBERSCHRIFT_UEBERALL.search(titel):
                return True
            if r.startswith("docs/personas/") and UEBERSCHRIFT_PERSONAS.search(titel.strip()):
                return True
            if r == "docs/datensatz/data-dictionary-S.md" and UEBERSCHRIFT_DATA_DICTIONARY.search(titel.strip()):
                return True
            return False

        neu, gestrichen = streiche_abschnitte(neu, passt)
        for g in gestrichen:
            protokoll.append(f"{r}: Abschnitt «{g}» entfernt")

        if r.startswith("docs/personas/"):
            neu, n1 = ersetze(neu, r"Ground Truth:[^|\n]*", "– ")
            neu, n2 = ersetze(neu, r"\s*\((?:Stolperstein|[\w-]*Falle)\b[^()\n]*\)", "")
            neu, n3 = ersetze(neu, r",\s*Muster F\d+[^|\n]*?(?=\s*\|)", "")
            if n1 + n2 + n3:
                protokoll.append(f"{r}: {n1 + n2 + n3} Randvermerke (Ground Truth, Stolperstein, Betrugsmuster) entfernt")

        if r == "docs/datensatz/data-dictionary-S.md":
            zeilen = neu.split("\n")
            behalten = [z for z in zeilen if not z.startswith("| truth/")]
            if len(behalten) != len(zeilen):
                protokoll.append(f"{r}: {len(zeilen) - len(behalten)} Tabellenzeilen truth/… entfernt")
            neu = "\n".join(behalten)

        if r == "README.md":
            zeilen = neu.split("\n")
            behalten = [z for z in zeilen if not re.match(r"^- `docs/(planung|stammdaten)/`", z)]
            if len(behalten) != len(zeilen):
                protokoll.append(f"{r}: {len(zeilen) - len(behalten)} Verweise auf entfernte Ordner gestrichen")
            neu = "\n".join(behalten)

        if neu != text:
            p.write_text(re.sub(r"\n{3,}", "\n\n", neu), encoding="utf-8")


def filtere_referenzdaten() -> None:
    # Annahmerichtlinien-Tabellen: Didaktik-Markierungen der Bias-Fallen
    p = ROOT / "data/reference/lv/annahmerichtlinie_tabellen.yaml"
    if p.exists():
        text = p.read_text(encoding="utf-8")
        neu = text.replace(
            " Sie enthalten den historischen Bias bewusst und markieren ihn mit\n# didaktik_falle: true.", "\n#"
        )
        neu = re.sub(r"^#.*Bias-Fallen.*\n", "", neu, flags=re.MULTILINE)
        neu = re.sub(r",\s*didaktik_falle:\s*(true|false)", "", neu)
        neu = re.sub(r",?\s*didaktik_hinweis:\s*\"[^\"]*\"(?=\s*\})", "", neu)
        neu = re.sub(r"^\s*didaktik_(falle|hinweis):.*\n", "", neu, flags=re.MULTILINE)
        if "didaktik_" in neu:
            sys.exit(f"Abbruch: {rel(p)} enthaelt nach dem Filtern noch didaktik_-Eintraege.")
        try:
            import yaml  # type: ignore

            yaml.safe_load(neu)
        except ImportError:
            pass
        except Exception as e:  # noqa: BLE001
            sys.exit(f"Abbruch: {rel(p)} ist nach dem Filtern kein gueltiges YAML ({e}).")
        if neu != text:
            p.write_text(neu, encoding="utf-8")
            protokoll.append(f"{rel(p)}: Markierungen didaktik_falle/didaktik_hinweis und Bias-Kommentar entfernt")

    # Underwriting-Entscheide: Vermerk zur Bias-Falle in der Spalte bemerkung
    p = ROOT / "data/reference/lv/underwriting_entscheidungen.csv"
    if p.exists():
        roh = p.read_bytes()
        bom = roh.startswith(b"\xef\xbb\xbf")
        text = roh.decode("utf-8-sig")
        zeilen = list(csv.reader(io.StringIO(text)))
        kopf = zeilen[0]
        i = kopf.index("bemerkung")
        n = 0
        for z in zeilen[1:]:
            if len(z) > i and re.search(r"Bias-Falle", z[i]):
                z[i] = ""
                n += 1
        if n:
            puffer = io.StringIO()
            csv.writer(puffer, lineterminator="\n" if "\r\n" not in text else "\r\n").writerows(zeilen)
            p.write_bytes((b"\xef\xbb\xbf" if bom else b"") + puffer.getvalue().encode("utf-8"))
            protokoll.append(f"{rel(p)}: Bias-Vermerk in {n} Zeilen der Spalte bemerkung geleert")


def entferne_pfade() -> None:
    for pfad in PFADE_ENTFERNEN:
        p = ROOT / pfad
        if p.is_dir():
            shutil.rmtree(p)
            protokoll.append(f"{pfad}/: Ordner entfernt")
        elif p.exists():
            p.unlink()
            protokoll.append(f"{pfad}: Datei entfernt")


def schlusspruefung() -> bool:
    reste = []
    for p in markdown_dateien():
        for nr, z in enumerate(p.read_text(encoding="utf-8").split("\n"), start=1):
            if re.search(r"ground[\s-]?truth", z, re.IGNORECASE) and not z.lstrip().startswith("|"):
                reste.append(f"{rel(p)}:{nr}: {z.strip()[:100]}")
            elif re.match(r"^#{1,6}\s+.*(Ground Truth|Rolle im Datensatz)", z):
                reste.append(f"{rel(p)}:{nr}: {z.strip()[:100]}")
    if (ROOT / "data/truth").exists():
        reste.append("data/truth existiert noch")
    for r in reste:
        protokoll.append(f"PRUEFEN: {r}")
    return bool(reste)


def main() -> None:
    pruefe_zweig()
    entferne_pfade()
    filtere_markdown()
    filtere_referenzdaten()
    offen = schlusspruefung()
    for z in protokoll:
        print(z)
    if offen:
        sys.exit("Abbruch: Loesungsinhalte nach dem Filtern gefunden (Zeilen PRUEFEN).")


if __name__ == "__main__":
    main()
