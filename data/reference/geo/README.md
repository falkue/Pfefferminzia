# Referenzdaten Geografie

Erzeugt durch `scripts/build_reference_geo_namen.py` (deterministisch, ohne Zufall). Nicht von Hand editieren, sondern das Skript anpassen und neu ausführen.

Regel aus `docs/konventionen.md` §1: Postleitzahlen und Orte sind real, Strassennamen ausschliesslich generiert.

## orte_ch.csv

Reale Schweizer Orte mit Postleitzahl. Alle 26 Kantone sind vertreten, Schwerpunkt Deutschschweiz. Der Kanton Solothurn ist im Ziehungsgewicht um den Faktor 2.5 überrepräsentiert, weil der Hauptsitz in Olten liegt.

| Spalte | Typ | Beschreibung |
|---|---|---|
| plz | Text (4 Ziffern) | Postleitzahl |
| ort | Text | Ortsname in Landessprache, bei Mehrdeutigkeit mit Kantonskürzel (z. B. „Buchs SG") |
| kanton | Text (2 Buchstaben) | Kantonskürzel |
| sprachregion | de, fr, it | Sprache des Orts; steuert Sprache von Kundendokumenten und Strassennamen |
| einwohner | Ganzzahl | Ungefähre Einwohnerzahl (gerundet, Stand ca. 2020) |
| gewicht | Dezimal | Ziehungsgewicht für den Generator (Einwohner in Tausend, Solothurn ×2.5) |
| tarifzone | 1, 2, 3 | Haftpflicht-Regionalzone: 1 Grossstadt/teure Agglomeration, 2 Mittelland, 3 ländlich/alpin |
| urbanitaet | STADT, AGGLO, LAND | Grossstädte und Orte ab 100'000 Einwohnern STADT, ab 10'000 AGGLO, sonst LAND |

## orte_de.csv

Reale deutsche Orte mit Postleitzahl. Alle 16 Bundesländer sind vertreten. Grossstädte haben mehrere Postleitzahlen und erscheinen daher mehrfach mit gleichem Ortsnamen.

| Spalte | Typ | Beschreibung |
|---|---|---|
| plz | Text (5 Ziffern) | Postleitzahl, eindeutig |
| ort | Text | Ortsname |
| bundesland_kuerzel | Text (2 Buchstaben) | BW, BY, BE, BB, HB, HH, HE, MV, NI, NW, RP, SL, SN, ST, SH, TH |
| bundesland | Text | Ausgeschriebener Name |
| einwohner | Ganzzahl | Ungefähre Einwohnerzahl des Orts bzw. PLZ-Gebiets |
| gewicht | Dezimal | Ziehungsgewicht (Einwohner in Tausend) |
| tarifzone | 1, 2, 3 | 1 die sieben grössten Metropolen, 2 übrige Grossstädte, 3 alle anderen |
| urbanitaet | STADT, AGGLO, LAND | wie CH |

## strassennamen.csv

Generierte Strassennamen aus Stamm × Typ je Sprache. Keine Zuordnung zu realen Strassen beabsichtigt. Sehr verbreitete Namen (Hauptstrasse, Bahnhofstrasse) sind als generisch markiert; sie existieren in fast jedem Ort und sind daher unproblematisch.

| Spalte | Typ | Beschreibung |
|---|---|---|
| strasse | Text | Vollständiger Strassenname, eindeutig je Sprache |
| sprache | de-CH, de-DE, fr, it | de-CH mit „strasse", de-DE mit „straße" |
| typ | Text | Strassentyp (Strasse, Weg, Gasse, Platz, Rue, Chemin, Via …) |
| generisch | true/false | Gehört zu den überall vorkommenden Standardnamen |

Mindestens 400 Namen je Sprache.
