"""Kommandozeile: ``pfefferminzia generate|validate|reference``."""

from __future__ import annotations

import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from pfefferminzia import __version__

app = typer.Typer(help="Pfefferminzia – Generator fuer den synthetischen Lehr-Datensatz.",
                  no_args_is_help=True)
reference_app = typer.Typer(help="Referenzdaten unter data/reference/ pruefen und anzeigen.",
                            no_args_is_help=True)
app.add_typer(reference_app, name="reference")
console = Console()


def _logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(console=console, show_path=False, rich_tracebacks=True)],
        force=True,
    )


def _ctx(stufe: str, config: Path | None, root: Path | None):
    from pfefferminzia.context import RunContext

    return RunContext.erstellen(stufe=stufe, config_pfad=config, root=root)


@app.callback()
def _haupt(version: bool = typer.Option(False, "--version", help="Version anzeigen und beenden")):
    if version:
        console.print(f"pfefferminzia {__version__}")
        raise typer.Exit()


@app.command()
def generate(
    stufe: str = typer.Option("S", "--stufe", "-s", help="Groessenstufe S, M oder L"),
    config: Path | None = typer.Option(None, "--config", "-c", help="Pfad zu generator.yaml"),
    root: Path | None = typer.Option(None, "--root", help="Projektwurzel (Default: automatisch)"),
    von: str | None = typer.Option(None, "--von", help="Erste Stufe (Name)"),
    bis: str | None = typer.Option(None, "--bis", help="Letzte Stufe (Name)"),
    nur: list[str] | None = typer.Option(None, "--nur", help="Nur diese Stufen (mehrfach)"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Pipeline ausfuehren (alle oder ausgewaehlte Stufen)."""
    from pfefferminzia.pipeline import run_pipeline

    _logging(verbose)
    if stufe not in ("S", "M", "L"):
        raise typer.BadParameter("Stufe muss S, M oder L sein")
    ctx = _ctx(stufe, config, root)
    ergebnisse = run_pipeline(ctx, von=von, bis=bis, nur=nur or None)
    t = Table(title=f"Pipeline Stufe {stufe}")
    t.add_column("Stufe")
    t.add_column("Dauer [s]", justify="right")
    t.add_column("Status")
    for e in ergebnisse:
        t.add_row(e.name, f"{e.dauer_s:.2f}", "[green]ok[/]" if e.ok else f"[red]{e.fehler}[/]")
    console.print(t)


@app.command()
def validate(
    stufe: str = typer.Option("S", "--stufe", "-s"),
    config: Path | None = typer.Option(None, "--config", "-c"),
    root: Path | None = typer.Option(None, "--root"),
    check: list[str] | None = typer.Option(None, "--check", help="Nur diese Checks (mehrfach)"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Validierungssuite auf den Referenzdaten (und ggf. geladenen Tabellen) ausfuehren."""
    from pfefferminzia.pipeline import run_pipeline
    from pfefferminzia.validate import run_checks

    _logging(verbose)
    ctx = _ctx(stufe, config, root)
    run_pipeline(ctx, nur=["config", "reference"])
    bericht = run_checks(ctx, namen=check or None)
    t = Table(title="Validierung")
    t.add_column("Check")
    t.add_column("Status")
    t.add_column("Befunde")
    for e in bericht.ergebnisse:
        status = "[yellow]uebersprungen[/]" if e.uebersprungen else ("[green]ok[/]" if e.ok else "[red]FEHLER[/]")
        text = "\n".join(f"{b.schwere}: {b.meldung}" + (f" [{b.tabelle}]" if b.tabelle else "")
                         for b in e.befunde) or "-"
        t.add_row(e.name, status, text)
    console.print(t)
    console.print(bericht.zusammenfassung())
    raise typer.Exit(code=0 if bericht.ok else 1)


@reference_app.command("check")
def reference_check(
    config: Path | None = typer.Option(None, "--config", "-c"),
    root: Path | None = typer.Option(None, "--root"),
    streng: bool = typer.Option(False, "--streng", help="Exit-Code 1, wenn Dateien fehlen"),
):
    """Zeigt, welche Referenzdateien vorhanden sind und wie viele Eintraege sie haben."""
    ctx = _ctx("S", config, root)
    t = Table(title=f"Referenzdaten unter {ctx.pfade.reference}")
    t.add_column("Schluessel")
    t.add_column("Datei")
    t.add_column("Team")
    t.add_column("ab Stufe")
    t.add_column("Status")
    t.add_column("Eintraege", justify="right")
    fehlend = 0
    for s in ctx.reference.status():
        if s.vorhanden and not s.hinweis:
            status = "[green]ok[/]"
        elif s.vorhanden:
            status = f"[red]{s.hinweis}[/]"
        else:
            status, fehlend = "[yellow]fehlt[/]", fehlend + 1
        t.add_row(s.schluessel, str(s.pfad.relative_to(ctx.root)), s.team, s.pflicht_ab_stufe, status,
                  "" if s.zeilen is None else str(s.zeilen))
    console.print(t)
    if streng and fehlend:
        raise typer.Exit(code=1)


@reference_app.command("show")
def reference_show(
    schluessel: str = typer.Argument(..., help="z. B. geo.orte_ch"),
    zeilen: int = typer.Option(10, "--zeilen", "-n"),
    root: Path | None = typer.Option(None, "--root"),
):
    """Zeigt die ersten Zeilen einer Referenzdatei."""
    ctx = _ctx("S", None, root)
    daten = ctx.reference.load(schluessel)
    console.print(daten.head(zeilen).to_string() if hasattr(daten, "head") else daten)


if __name__ == "__main__":  # pragma: no cover
    app()
