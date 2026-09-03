"""Implementierung der PartnerStage zur Erzeugung von Kundendaten."""

import numpy as np
import pandas as pd

from pfefferminzia.context import RunContext
from pfefferminzia.pipeline import Stage, register
from pfefferminzia.synth.names import NameSynth


@register
class PartnerStage(Stage):
    name, nummer, welle = "partner", 30, 1
    beschreibung = "Partner, Adressen, Kontakte, Beziehungen, latente Kundenmerkmale"

    def run(self, ctx: RunContext) -> None:
        """Erzeugt Kundendaten (Personen/Firmen)."""
        rng = np.random.default_rng(ctx.master_seed)

        # Lade Referenzdaten für Namen und Adressen
        vornamen = ctx.reference.load("namen.vornamen")
        nachnamen = ctx.reference.load("namen.nachnamen")
        from pfefferminzia.validate.fiction import lade_blocklist
        name_synth = NameSynth(vornamen, nachnamen, blocklist=lade_blocklist(ctx))

        # Adressen (vereinfacht für den Stub/Initialisierung)
        # In einer echten Implementierung würde AddressSynth genutzt werden

        anzahl = 500
        daten = []

        for i in range(anzahl):
            # 50:50 Geschlechterverteilung (M/W)
            geschlecht = "M" if rng.random() < 0.5 else "W"

            # Verteilung CH vs DE (Annahme: 50:50 für den Testfall)
            land = "CH" if rng.random() < 0.5 else "DE"
            sprache = "de" # Vereinfacht

            # Geburtsjahr zwischen 1940 und 2005
            geburtsjahr = rng.integers(1940, 2006)

            # Name generieren
            p = name_synth.person(rng, geschlecht, land, geburtsjahr, sprache=sprache)

            # ID generieren (einfach für den Stub)
            partner_id = f"PART-{i:05d}"

            daten.append({
                "partner_id": partner_id,
                "vorname": p.vorname,
                "nachname": p.nachname,
                "geschlecht": p.geschlecht,
                "land": land,
                "sprache": sprache,
                "geburtsjahr": geburtsjahr,
                "typ": "Person" # Im nächsten Schritt Erweiterung auf Firma
            })

        df = pd.DataFrame(daten)
        ctx.tabellen.register("partner_personen", df, layer="partner")

        ctx.ereignis(self.name, f"{anzahl} Partner (Personen) erzeugt.")
