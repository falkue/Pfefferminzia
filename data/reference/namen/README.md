# Referenzdaten Namen

Erzeugt durch `scripts/build_reference_geo_namen.py` (deterministisch). Nicht von Hand editieren, sondern das Skript anpassen und neu ausführen.

Regel aus `docs/konventionen.md` §1: Personennamen stammen aus kuratierten Listen, Kombinationen aus der Blocklist werden nie erzeugt.

## vornamen.csv

Vornamen mit Dekadengewichten, damit Name und Geburtsjahr zusammenpassen (eine Person mit Jahrgang 1945 heisst eher Ruth oder Werner, eine mit Jahrgang 2003 eher Mia oder Noah). Die Gewichte folgen einer Glockenkurve um die typische Peak-Dekade, Minimum 1.

| Spalte | Typ | Beschreibung |
|---|---|---|
| vorname | Text | |
| geschlecht | M, W, U | U = geschlechtsneutral (z. B. Dominique, Claude) |
| sprachraum | de-CH, de-DE, fr, it, international | international = Namen mit Migrationshintergrund, in beiden Ländern verwendet |
| g_1930 … g_2000 | Dezimal 1–100 | Ziehungsgewicht je Geburtsdekade |

## nachnamen.csv

| Spalte | Typ | Beschreibung |
|---|---|---|
| nachname | Text | |
| sprachraum | de-CH, de-DE, fr, it, international | |
| gewicht | Dezimal | Relative Häufigkeit innerhalb des Sprachraums |
| synthetisch | true/false | false = real vorkommender Familienname; true reserviert für künftig erfundene Namen |

Nachnamen kommen bewusst in beiden deutschen Sprachräumen vor (z. B. Müller, Meier), aber mit unterschiedlichen Gewichten.

## firmennamen_bausteine.csv

Bausteine für fiktive KMU-Namen nach dem Muster „Stamm Branche Rechtsform" (z. B. „Aare Schreinerei AG", „Neckar Elektro GmbH").

| Spalte | Typ | Beschreibung |
|---|---|---|
| art | stamm, branche, rechtsform | |
| wert | Text | Der Baustein |
| land | CH, DE oder leer | Leer = in beiden Ländern verwendbar |
| branche | Text | Nur bei art = branche: fachliche Branche für die Zuordnung zu Branchenklassen |

Stämme sind Flüsse, Berge und Regionen, die keinem realen Unternehmen der Versicherungsbranche entsprechen.

## blocklist.csv

Kombinationen, die der Generator nie erzeugen darf. Die Prüfung erfolgt in `pfefferminzia.validate.fiction`.

| Spalte | Typ | Beschreibung |
|---|---|---|
| typ | person, firma | |
| vorname, nachname | Text | Nur bei person; die Kombination ist gesperrt, nicht die einzelnen Namen |
| name | Text | Nur bei firma; Teilstring-Prüfung gegen Firmennamen |
| kategorie | prominenz, versicherung, medium, versicherer | Grund der Sperrung |

Kategorie „medium" bezeichnet das real existierende Fachmedium gleichen Namens und dessen KI-Autorenfigur (siehe Entscheidung E01).
