"""Tarifgenerationen als lesbare Markdown- und PDF-Tarifblaetter rendern."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

from pfefferminzia.context import RunContext
from pfefferminzia.export import _relativ
from pfefferminzia.manifest import sha256_datei

DISCLAIMER_KURZ = "Fiktives Lehrbeispiel. Alle Daten synthetisch. Keine Verbindung zu realen Personen, Unternehmen oder Marken."
DISCLAIMER_LANG = (
    "Pfefferminzia ist ein frei erfundenes Unternehmen für Lehrzwecke. Alle Personen, Firmen, Adressen, "
    "Verträge, Schäden, Kennzahlen und Ereignisse sind synthetisch erzeugt. Ähnlichkeiten mit real "
    "existierenden Personen, Unternehmen oder Marken, insbesondere mit gleichnamigen Medien oder "
    "Dienstleistern, sind unbeabsichtigt und nicht intendiert. Rechtliche und regulatorische Aussagen "
    "sind vereinfacht, Stand 2026, und ersetzen keine Rechtsberatung. Teile dieses Materials wurden mit "
    "Unterstützung von KI erzeugt."
)

GRUEN = HexColor("#164F3B")
MINT = HexColor("#C7E8D5")
TEXT = HexColor("#1B2A23")
GRAU = HexColor("#65766D")
HELLGRAU = HexColor("#92A099")
LINIE = HexColor("#D4DFD8")
FLAECHE = HexColor("#F1F7F3")
GELB = HexColor("#F5C451")
GELB_HELL = HexColor("#FFF8E5")
VIOLETT = HexColor("#5A407A")
VIOLETT_HELL = HexColor("#F2EAF8")


@dataclass(frozen=True)
class Tarifblatt:
    dokument_id: str
    sparte: str
    markt: str
    generation: str
    bezeichnung: str
    gueltig_ab: str
    gueltig_bis: str | None
    produkte: tuple[str, ...]
    merkmale: str
    daten: tuple[tuple[str, str], ...]
    details: tuple[str, ...]
    besonderer_hinweis: str


def _wert(zeile: pd.Series, spalte: str) -> str:
    wert = zeile.get(spalte)
    return "" if pd.isna(wert) else str(wert)


def _markttext(text: str, markt: str) -> str:
    return text.replace("ß", "ss") if markt == "CH" else text


def _modelle(ctx: RunContext) -> list[Tarifblatt]:
    result: list[Tarifblatt] = []
    for _, zeile in ctx.reference.csv("hp/tarifgenerationen.csv").iterrows():
        for markt in ("CH", "DE"):
            produkte = tuple(_wert(zeile, "produkte").split(";"))
            result.append(Tarifblatt(
                dokument_id=_wert(zeile, "bedingungswerk_ch" if markt == "CH" else "bedingungswerk_de"),
                sparte="HP", markt=markt, generation=_wert(zeile, "kuerzel"), bezeichnung=_wert(zeile, "bezeichnung"),
                gueltig_ab=_wert(zeile, "gueltig_ab"), gueltig_bis=_wert(zeile, "gueltig_bis") or None,
                produkte=produkte, merkmale=_markttext(_wert(zeile, "kernunterschiede"), markt),
                daten=(
                    ("Produkte", ", ".join(produkte)),
                    ("Neugeschäft", f"{_wert(zeile, 'gueltig_ab')} bis {_wert(zeile, 'gueltig_bis') or 'offen'}"),
                    ("Herkunft", _wert(zeile, "herkunft")),
                    ("Primäres System", _wert(zeile, "quellsystem_primaer")),
                    ("Tarifhandbuch", _wert(zeile, "tarifhandbuch_version")),
                    ("Bestandsanteil", f"{_wert(zeile, 'anteil_bestand_pct')} %"),
                ),
                details=(
                    f"Bedingungswerk: {_wert(zeile, 'bedingungswerk_ch' if markt == 'CH' else 'bedingungswerk_de')}",
                    f"Revisionen: {_wert(zeile, 'revisionen') or 'keine separate Angabe'}",
                    f"Neugeschäftsausnahme bis: {_wert(zeile, 'neugeschaeft_ausnahme_bis') or 'keine'}",
                    f"Altes Planungskürzel: {_wert(zeile, 'alt_kuerzel_planung') or 'keines'}",
                ),
                besonderer_hinweis=_markttext(_wert(zeile, "revisionen") or "Keine separate Revision ausgewiesen.", markt),
            ))
    for _, zeile in ctx.reference.csv("lv/tarifgenerationen.csv").iterrows():
        for markt in ("CH", "DE"):
            produkte = tuple(_wert(zeile, "produkte").split(";"))
            zins = _wert(zeile, "technischer_zins_ch_pct" if markt == "CH" else "rechnungszins_de_pct")
            tafel = _wert(zeile, "sterbetafel_ch" if markt == "CH" else "sterbetafel_de")
            suizidfrist = _wert(zeile, "suizidfrist_jahre_ch" if markt == "CH" else "suizidfrist_jahre_de")
            dokument_id = _wert(zeile, "bedingungswerk_id_ch" if markt == "CH" else "bedingungswerk_id_de")
            result.append(Tarifblatt(
                dokument_id=dokument_id, sparte="LV", markt=markt, generation=_wert(zeile, "generation_code"),
                bezeichnung=_wert(zeile, "bezeichnung"), gueltig_ab=_wert(zeile, "gueltig_ab"),
                gueltig_bis=_wert(zeile, "gueltig_bis") or None, produkte=produkte,
                merkmale=_markttext(_wert(zeile, "kernunterschiede_bemerkung"), markt),
                daten=(
                    ("Produkte", ", ".join(produkte)),
                    ("Neugeschäft", f"{_wert(zeile, 'gueltig_ab')} bis {_wert(zeile, 'gueltig_bis') or 'offen'}"),
                    ("Rechnungszins", f"{zins} %"),
                    ("Sterbetafel", tafel),
                    ("Annahmerichtlinie", _wert(zeile, "annahmerichtlinie_version")),
                    ("Gesundheitsfragen", _wert(zeile, "gesundheitsfragebogen_version")),
                ),
                details=(
                    f"Bedingungswerk: {dokument_id}",
                    f"Suizidfrist: {suizidfrist} Jahr(e)",
                    f"Unisex: {_wert(zeile, 'unisex_ch' if markt == 'CH' else 'unisex_de')}",
                    f"Rückkaufsmethode: {_wert(zeile, 'rueckkauf_methode')}",
                    f"Zillmerung: {_wert(zeile, 'zillmerung')}",
                ),
                besonderer_hinweis=_markttext(
                    f"Flugrisiko-Ausschluss: {_wert(zeile, 'flugrisiko_ausschluss')}. "
                    f"Nachversicherungsgarantie: {_wert(zeile, 'nachversicherungsgarantie')}. "
                    f"Verweisung EU/BU: {_wert(zeile, 'verweisung_bu')}.", markt,
                ),
            ))
    return result


def _pdf_text(text: str) -> str:
    return text.replace("–", "-").replace("—", "-").replace("’", "'").replace("→", "->").replace("\u00a0", " ")


def _zeilen(text: str, schrift: str, groesse: float, breite: float) -> list[str]:
    result: list[str] = []
    for absatz in _pdf_text(text).splitlines() or [""]:
        zeile = ""
        for wort in absatz.split():
            kandidat = f"{zeile} {wort}".strip()
            if zeile and stringWidth(kandidat, schrift, groesse) > breite:
                result.append(zeile)
                zeile = wort
            else:
                zeile = kandidat
        result.append(zeile)
    return result


def _absatz(pdf: Canvas, text: str, x: float, y: float, breite: float, *, schrift: str = "Helvetica",
            groesse: float = 9, farbe=GRAU, zeilenhoehe: float = 13) -> float:
    pdf.setFont(schrift, groesse)
    pdf.setFillColor(farbe)
    for zeile in _zeilen(text, schrift, groesse, breite):
        pdf.drawString(x, y, zeile or " ")
        y -= zeilenhoehe
    return y


def _kopf(pdf: Canvas, modell: Tarifblatt, seite: int) -> None:
    breite, hoehe = A4
    pdf.setFillColor(GRUEN)
    pdf.rect(0, hoehe - 76, breite, 76, fill=1, stroke=0)
    pdf.setFillColor(MINT)
    pdf.circle(49, hoehe - 38, 18, fill=1, stroke=0)
    pdf.setFillColor(GRUEN)
    pdf.circle(55, hoehe - 33, 10, fill=1, stroke=0)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(82, hoehe - 35, "PFEFFERMINZIA")
    pdf.setFillColor(MINT)
    pdf.setFont("Helvetica", 6.7)
    pdf.drawString(82, hoehe - 50, "VERSICHERUNGEN  /  TARIFINFORMATION")
    pdf.setStrokeColor(MINT)
    pdf.rect(breite - 174, hoehe - 49, 136, 22, fill=0, stroke=1)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 6.6)
    pdf.drawCentredString(breite - 106, hoehe - 41.5, "SYNTHETISCHES TARIFBLATT")
    pdf.setStrokeColor(LINIE)
    pdf.line(38, 44, breite - 38, 44)
    pdf.setFillColor(HELLGRAU)
    pdf.setFont("Helvetica-Bold", 6.4)
    pdf.drawString(38, 27, f"FIKTIVES LEHRBEISPIEL  ·  {modell.dokument_id}")
    pdf.drawRightString(breite - 38, 27, f"SEITE {seite} / 2")


def _abschnitt(pdf: Canvas, nummer: int, titel: str, y: float) -> float:
    pdf.setFillColor(GRUEN)
    pdf.circle(51, y + 2, 11, fill=1, stroke=0)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 7)
    pdf.drawCentredString(51, y - 1.5, str(nummer))
    pdf.setFillColor(GRUEN)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(72, y, titel.upper())
    pdf.setStrokeColor(LINIE)
    pdf.line(72, y - 7, 557, y - 7)
    return y - 27


def _karte(pdf: Canvas, x: float, y: float, breite: float, titel: str, wert: str) -> None:
    pdf.setFillColor(FLAECHE)
    pdf.setStrokeColor(LINIE)
    pdf.rect(x, y - 50, breite, 50, fill=1, stroke=1)
    pdf.setFillColor(HELLGRAU)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.drawString(x + 11, y - 15, titel.upper())
    _absatz(pdf, wert, x + 11, y - 31, breite - 22, schrift="Helvetica-Bold", groesse=8.2, farbe=TEXT, zeilenhoehe=10)


def _markdown(modell: Tarifblatt) -> str:
    gueltig_bis = modell.gueltig_bis or "null"
    sprache = "de-CH" if modell.markt == "CH" else "de-DE"
    geltung = f"Die Tarifgeneration {modell.generation} gilt für {', '.join(modell.produkte)} im Markt "
    geltung += f"{'Schweiz' if modell.markt == 'CH' else 'Deutschland'} ab {modell.gueltig_ab}"
    geltung += f" bis {modell.gueltig_bis}." if modell.gueltig_bis else "."
    daten = "\n".join(f"- **{titel}:** {wert}" for titel, wert in modell.daten)
    details = "\n".join(f"- {detail}" for detail in modell.details)
    return f"""---
dokument_id: {modell.dokument_id}
titel: Tarifblatt {modell.bezeichnung}
typ: regelwerk
sparte: {modell.sparte}
markt: {modell.markt}
sprache: {sprache}
version: "1.0"
gueltig_ab: {modell.gueltig_ab}
gueltig_bis: {gueltig_bis}
tarifgeneration: {modell.generation}
quelle_system: null
absender: Pfefferminzia Versicherungen AG
vertraulichkeit: oeffentlich
erzeugt_am: 2026-09-04
---

# Tarifblatt {modell.sparte} – {modell.bezeichnung}

## Geltungsbereich

{_markttext(geltung, modell.markt)}

## Tarifmerkmale

{modell.merkmale}

## Tarifdaten

{daten}

## Version und Grundlagen

{details}

## Besondere Hinweise

{modell.besonderer_hinweis}

---

{DISCLAIMER_LANG}
"""


def _pdf(modell: Tarifblatt, ziel: Path) -> None:
    pdf = Canvas(str(ziel), pagesize=A4, pageCompression=1, invariant=1)
    pdf.setTitle(f"Tarifblatt {modell.sparte} – {modell.bezeichnung}")
    pdf.setAuthor("Pfefferminzia Versicherungen AG (fiktiv)")
    pdf.setSubject("Synthetisches Tarifblatt für Lehrzwecke")
    pdf.setCreator("Pfefferminzia Dokumentgenerator")
    _kopf(pdf, modell, 1)
    pdf.setFillColor(GRUEN)
    pdf.setFont("Helvetica-Bold", 7.2)
    pdf.drawString(38, 716, f"{'HAFTPFLICHT' if modell.sparte == 'HP' else 'LEBENSVERSICHERUNG'} · TARIFGENERATION")
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica-Bold", 27)
    pdf.drawString(38, 679, f"Tarifblatt {'Haftpflicht' if modell.sparte == 'HP' else 'Leben'}")
    pdf.setFillColor(GRAU)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(38, 636, f"{modell.bezeichnung} · {'Schweiz' if modell.markt == 'CH' else 'Deutschland'}")
    karten = (("Dokument-ID", modell.dokument_id), ("Tarifgeneration", modell.generation),
              ("Markt", "Schweiz" if modell.markt == "CH" else "Deutschland"), ("Gültig ab", modell.gueltig_ab))
    for index, (titel, wert) in enumerate(karten):
        _karte(pdf, 38 + index * 130, 588, 122, titel, wert)
    pdf.setFillColor(GELB_HELL)
    pdf.setStrokeColor(GELB)
    pdf.rect(38, 466, 519, 72, fill=1, stroke=1)
    pdf.setFillColor(GELB)
    pdf.rect(38, 466, 5, 72, fill=1, stroke=0)
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica-Bold", 7.5)
    pdf.drawString(56, 517, "WICHTIGER NUTZUNGSHINWEIS")
    _absatz(pdf, "Dieses Tarifblatt fasst die Merkmale der genannten Tarifgeneration zusammen. Verbindlich sind der "
             "individuelle Vertrag, die Police, Nachträge und die vollständigen Bedingungen.", 56, 499, 478, groesse=8.3, zeilenhoehe=11.5)
    y = _abschnitt(pdf, 1, "Geltungsbereich", 427)
    geltung = f"Die Tarifgeneration {modell.generation} gilt für {', '.join(modell.produkte)} im Markt "
    geltung += f"{'Schweiz' if modell.markt == 'CH' else 'Deutschland'}. Der Neugeschäftszeitraum beginnt am {modell.gueltig_ab}"
    geltung += f" und endet am {modell.gueltig_bis}." if modell.gueltig_bis else " und hat kein hinterlegtes Enddatum."
    y = _absatz(pdf, _markttext(geltung, modell.markt), 38, y, 519, groesse=9.2, zeilenhoehe=14) - 17
    y = _abschnitt(pdf, 2, "Tarifmerkmale", y)
    _absatz(pdf, modell.merkmale, 38, y, 519, groesse=9.2, zeilenhoehe=14)
    pdf.showPage()

    _kopf(pdf, modell, 2)
    pdf.setFillColor(GRUEN)
    pdf.setFont("Helvetica-Bold", 7.2)
    pdf.drawString(38, 735, f"Tarifblatt {modell.sparte}  /  {modell.bezeichnung}")
    y = _abschnitt(pdf, 3, "Tarifdaten", 697)
    for index, (titel, wert) in enumerate(modell.daten[:6]):
        x = 38 + (index % 2) * 269
        fy = y - (index // 2) * 42
        pdf.setFillColor(HELLGRAU)
        pdf.setFont("Helvetica-Bold", 5.8)
        pdf.drawString(x, fy, titel.upper())
        _absatz(pdf, _markttext(wert, modell.markt), x, fy - 14, 250, groesse=8.2, farbe=TEXT, zeilenhoehe=10.5)
    y -= 145
    y = _abschnitt(pdf, 4, "Version und Grundlagen", y)
    for detail in modell.details:
        pdf.setFillColor(GRUEN)
        pdf.circle(41, y + 2, 2.3, fill=1, stroke=0)
        y = _absatz(pdf, _markttext(detail, modell.markt), 52, y + 6, 505, groesse=8.4, zeilenhoehe=12) - 6
    y = _abschnitt(pdf, 5, "Besondere Hinweise", y - 9)
    pdf.setFillColor(VIOLETT_HELL)
    pdf.setStrokeColor(HexColor("#C5B0D6"))
    pdf.rect(38, y - 76, 519, 76, fill=1, stroke=1)
    pdf.setFillColor(VIOLETT)
    pdf.setFont("Helvetica-Bold", 6.5)
    pdf.drawString(53, y - 20, "TARIFGENERATION")
    _absatz(pdf, modell.besonderer_hinweis, 53, y - 39, 488, groesse=8.4, farbe=VIOLETT, zeilenhoehe=11.5)
    y = _abschnitt(pdf, 6, "Dokumenthinweis", y - 104)
    _absatz(pdf, _markttext(DISCLAIMER_LANG, modell.markt), 38, y, 519, groesse=7.3, zeilenhoehe=10.2)
    pdf.save()


def render_tarifblaetter(ctx: RunContext) -> list[Path]:
    """Erzeugt fuer jede Tarifgeneration und jeden Markt ein Markdown- und PDF-Tarifblatt."""
    ziel = ctx.pfade.documents / ctx.stufe / "tarife"
    ziel.mkdir(parents=True, exist_ok=True)
    pfade: list[Path] = []
    for modell in _modelle(ctx):
        markdown = ziel / f"{modell.dokument_id}.md"
        pdf = ziel / f"{modell.dokument_id}.pdf"
        markdown.write_text(_markdown(modell), encoding="utf-8")
        _pdf(modell, pdf)
        pfade.extend((markdown, pdf))
        if ctx.manifest is not None:
            ctx.manifest.add_datei(_relativ(markdown, ctx.root), sha256_datei(markdown))
            ctx.manifest.add_datei(_relativ(pdf, ctx.root), sha256_datei(pdf))
    return pfade
