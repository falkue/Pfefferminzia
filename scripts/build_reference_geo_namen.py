"""Erzeugt die geografischen und namensbezogenen Referenzdaten unter ``data/reference/``.

Aufruf: ``uv run python scripts/build_reference_geo_namen.py``

Regeln (docs/konventionen.md §1):
- Orte und Postleitzahlen sind real; Strassennamen sind ausschliesslich generiert (Stamm x Typ).
- Vornamen tragen Dekadengewichte (g_1930 … g_2000), damit Name und Alter zusammenpassen.
- Die Blocklist enthaelt reale Personen und Firmen der Versicherungsbranche sowie Prominente.

Die Ausgabe ist deterministisch (kein Zufall), damit Laeufe byte-identisch sind.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEO = ROOT / "data" / "reference" / "geo"
NAMEN = ROOT / "data" / "reference" / "namen"

# ---------------------------------------------------------------------------------------------
# Orte Schweiz: (plz, ort, kanton, sprachregion, einwohner_tsd)
# ---------------------------------------------------------------------------------------------
ORTE_CH: list[tuple[str, str, str, str, float]] = [
    # Zuerich
    ("8001", "Zürich", "ZH", "de", 420), ("8400", "Winterthur", "ZH", "de", 115),
    ("8600", "Dübendorf", "ZH", "de", 30), ("8610", "Uster", "ZH", "de", 35),
    ("8620", "Wetzikon", "ZH", "de", 25), ("8700", "Küsnacht", "ZH", "de", 14),
    ("8800", "Thalwil", "ZH", "de", 18), ("8820", "Wädenswil", "ZH", "de", 24),
    ("8952", "Schlieren", "ZH", "de", 20), ("8953", "Dietikon", "ZH", "de", 28),
    ("8302", "Kloten", "ZH", "de", 21), ("8304", "Wallisellen", "ZH", "de", 16),
    ("8330", "Pfäffikon ZH", "ZH", "de", 12), ("8340", "Hinwil", "ZH", "de", 11),
    ("8630", "Rüti ZH", "ZH", "de", 12), ("8180", "Bülach", "ZH", "de", 22),
    ("8134", "Adliswil", "ZH", "de", 19), ("8810", "Horgen", "ZH", "de", 23),
    ("8910", "Affoltern am Albis", "ZH", "de", 12), ("8105", "Regensdorf", "ZH", "de", 18),
    ("8153", "Rümlang", "ZH", "de", 8), ("8604", "Volketswil", "ZH", "de", 19),
    ("8353", "Elgg", "ZH", "de", 5), ("8712", "Stäfa", "ZH", "de", 15),
    ("8708", "Männedorf", "ZH", "de", 11), ("8600", "Dübendorf Gfenn", "ZH", "de", 2),
    ("8500", "Frauenfeld", "TG", "de", 26),
    # Bern
    ("3000", "Bern", "BE", "de", 135), ("3600", "Thun", "BE", "de", 45),
    ("2500", "Biel/Bienne", "BE", "de", 55), ("3400", "Burgdorf", "BE", "de", 17),
    ("3800", "Interlaken", "BE", "de", 6), ("3072", "Ostermundigen", "BE", "de", 18),
    ("3098", "Köniz", "BE", "de", 42), ("3053", "Münchenbuchsee", "BE", "de", 10),
    ("3250", "Lyss", "BE", "de", 15), ("3550", "Langnau im Emmental", "BE", "de", 10),
    ("4900", "Langenthal", "BE", "de", 16), ("3700", "Spiez", "BE", "de", 13),
    ("3860", "Meiringen", "BE", "de", 5), ("3780", "Gstaad", "BE", "de", 3),
    ("3123", "Belp", "BE", "de", 12), ("3110", "Münsingen", "BE", "de", 13),
    ("3270", "Aarberg", "BE", "de", 5), ("3612", "Steffisburg", "BE", "de", 16),
    ("3627", "Heimberg", "BE", "de", 7), ("4950", "Huttwil", "BE", "de", 5),
    ("3714", "Frutigen", "BE", "de", 7), ("3818", "Grindelwald", "BE", "de", 4),
    ("2740", "Moutier", "BE", "fr", 7), ("2610", "Saint-Imier", "BE", "fr", 5),
    # Luzern
    ("6003", "Luzern", "LU", "de", 82), ("6010", "Kriens", "LU", "de", 28),
    ("6020", "Emmenbrücke", "LU", "de", 32), ("6210", "Sursee", "LU", "de", 10),
    ("6130", "Willisau", "LU", "de", 8), ("6280", "Hochdorf", "LU", "de", 10),
    ("6048", "Horw", "LU", "de", 14), ("6030", "Ebikon", "LU", "de", 14),
    ("6110", "Wolhusen", "LU", "de", 4), ("6260", "Reiden", "LU", "de", 7),
    # Uri, Schwyz, Obwalden, Nidwalden, Glarus, Zug
    ("6460", "Altdorf UR", "UR", "de", 10), ("6472", "Erstfeld", "UR", "de", 4),
    ("6490", "Andermatt", "UR", "de", 1.5), ("6454", "Flüelen", "UR", "de", 2),
    ("6430", "Schwyz", "SZ", "de", 15), ("8808", "Pfäffikon SZ", "SZ", "de", 8),
    ("6410", "Goldau", "SZ", "de", 8), ("8840", "Einsiedeln", "SZ", "de", 16),
    ("8853", "Lachen SZ", "SZ", "de", 9), ("6440", "Brunnen", "SZ", "de", 8),
    ("8832", "Wollerau", "SZ", "de", 7),
    ("6060", "Sarnen", "OW", "de", 10), ("6390", "Engelberg", "OW", "de", 4),
    ("6072", "Sachseln", "OW", "de", 5),
    ("6370", "Stans", "NW", "de", 8), ("6362", "Stansstad", "NW", "de", 5),
    ("6374", "Buochs", "NW", "de", 6), ("6052", "Hergiswil NW", "NW", "de", 6),
    ("8750", "Glarus", "GL", "de", 12), ("8752", "Näfels", "GL", "de", 4),
    ("8762", "Schwanden GL", "GL", "de", 2),
    ("6300", "Zug", "ZG", "de", 30), ("6330", "Cham", "ZG", "de", 17),
    ("6340", "Baar", "ZG", "de", 25), ("6312", "Steinhausen", "ZG", "de", 10),
    ("6343", "Rotkreuz", "ZG", "de", 12), ("6314", "Unterägeri", "ZG", "de", 9),
    # Freiburg
    ("1700", "Fribourg", "FR", "fr", 40), ("1630", "Bulle", "FR", "fr", 24),
    ("3280", "Murten", "FR", "de", 8), ("1680", "Romont FR", "FR", "fr", 5),
    ("3186", "Düdingen", "FR", "de", 8), ("1712", "Tafers", "FR", "de", 3),
    ("1618", "Châtel-St-Denis", "FR", "fr", 7), ("1470", "Estavayer-le-Lac", "FR", "fr", 6),
    ("3175", "Flamatt", "FR", "de", 3), ("1762", "Givisiez", "FR", "fr", 3),
    # Solothurn (Hauptsitz Olten: Region ueberrepraesentiert)
    ("4600", "Olten", "SO", "de", 19), ("4500", "Solothurn", "SO", "de", 17),
    ("2540", "Grenchen", "SO", "de", 17), ("4632", "Trimbach", "SO", "de", 7),
    ("4653", "Obergösgen", "SO", "de", 2), ("4656", "Starrkirch-Wil", "SO", "de", 1.5),
    ("4657", "Dulliken", "SO", "de", 5), ("4658", "Däniken SO", "SO", "de", 3),
    ("4702", "Oensingen", "SO", "de", 6), ("4710", "Balsthal", "SO", "de", 6),
    ("4528", "Zuchwil", "SO", "de", 9), ("4553", "Subingen", "SO", "de", 3),
    ("4562", "Biberist", "SO", "de", 8), ("4563", "Gerlafingen", "SO", "de", 5),
    ("2544", "Bettlach", "SO", "de", 5), ("4614", "Hägendorf", "SO", "de", 5),
    ("4612", "Wangen bei Olten", "SO", "de", 5), ("4616", "Kappel SO", "SO", "de", 3),
    ("4617", "Gunzgen", "SO", "de", 2), ("4622", "Egerkingen", "SO", "de", 3),
    ("4623", "Neuendorf", "SO", "de", 2), ("4625", "Oberbuchsiten", "SO", "de", 2),
    ("4629", "Fulenbach", "SO", "de", 1.5), ("4654", "Lostorf", "SO", "de", 4),
    ("4655", "Stüsslingen", "SO", "de", 1), ("4513", "Langendorf", "SO", "de", 4),
    ("4542", "Luterbach", "SO", "de", 4), ("4143", "Dornach", "SO", "de", 7),
    ("4226", "Breitenbach", "SO", "de", 4), ("5012", "Schönenwerd", "SO", "de", 4),
    ("5013", "Niedergösgen", "SO", "de", 4), ("5015", "Erlinsbach SO", "SO", "de", 3),
    # Basel-Stadt, Basel-Landschaft
    ("4051", "Basel", "BS", "de", 175), ("4125", "Riehen", "BS", "de", 21),
    ("4126", "Bettingen", "BS", "de", 1),
    ("4410", "Liestal", "BL", "de", 15), ("4132", "Muttenz", "BL", "de", 18),
    ("4127", "Birsfelden", "BL", "de", 10), ("4153", "Reinach BL", "BL", "de", 19),
    ("4102", "Binningen", "BL", "de", 16), ("4123", "Allschwil", "BL", "de", 21),
    ("4104", "Oberwil BL", "BL", "de", 11), ("4133", "Pratteln", "BL", "de", 17),
    ("4142", "Münchenstein", "BL", "de", 12), ("4450", "Sissach", "BL", "de", 7),
    ("4460", "Gelterkinden", "BL", "de", 6), ("4242", "Laufen", "BL", "de", 6),
    ("4402", "Frenkendorf", "BL", "de", 6), ("4415", "Lausen", "BL", "de", 5),
    # Schaffhausen, Appenzell, St. Gallen
    ("8200", "Schaffhausen", "SH", "de", 37), ("8212", "Neuhausen am Rheinfall", "SH", "de", 11),
    ("8240", "Thayngen", "SH", "de", 5), ("8260", "Stein am Rhein", "SH", "de", 3),
    ("9100", "Herisau", "AR", "de", 16), ("9053", "Teufen AR", "AR", "de", 6),
    ("9410", "Heiden", "AR", "de", 4), ("9043", "Trogen", "AR", "de", 2),
    ("9050", "Appenzell", "AI", "de", 6), ("9108", "Gonten", "AI", "de", 1.5),
    ("9000", "St. Gallen", "SG", "de", 76), ("9500", "Wil SG", "SG", "de", 24),
    ("8640", "Rapperswil-Jona", "SG", "de", 27), ("9400", "Rorschach", "SG", "de", 9),
    ("9470", "Buchs SG", "SG", "de", 13), ("8730", "Uznach", "SG", "de", 6),
    ("9200", "Gossau SG", "SG", "de", 18), ("9450", "Altstätten SG", "SG", "de", 12),
    ("7320", "Sargans", "SG", "de", 6), ("9630", "Wattwil", "SG", "de", 9),
    ("8880", "Walenstadt", "SG", "de", 6), ("9430", "St. Margrethen", "SG", "de", 6),
    ("9240", "Uzwil", "SG", "de", 13), ("9230", "Flawil", "SG", "de", 10),
    ("7310", "Bad Ragaz", "SG", "de", 6),
    # Graubuenden
    ("7000", "Chur", "GR", "de", 37), ("7500", "St. Moritz", "GR", "de", 5),
    ("7270", "Davos Platz", "GR", "de", 11), ("7050", "Arosa", "GR", "de", 3),
    ("7130", "Ilanz", "GR", "de", 5), ("7430", "Thusis", "GR", "de", 3),
    ("7302", "Landquart", "GR", "de", 9), ("7013", "Domat/Ems", "GR", "de", 8),
    ("7550", "Scuol", "GR", "de", 5), ("7742", "Poschiavo", "GR", "it", 3),
    ("7402", "Bonaduz", "GR", "de", 3), ("7220", "Schiers", "GR", "de", 3),
    # Aargau
    ("5000", "Aarau", "AG", "de", 21), ("5400", "Baden", "AG", "de", 20),
    ("5600", "Lenzburg", "AG", "de", 11), ("4800", "Zofingen", "AG", "de", 12),
    ("5200", "Brugg AG", "AG", "de", 12), ("5430", "Wettingen", "AG", "de", 21),
    ("5610", "Wohlen AG", "AG", "de", 17), ("5630", "Muri AG", "AG", "de", 8),
    ("4310", "Rheinfelden", "AG", "de", 13), ("5620", "Bremgarten AG", "AG", "de", 8),
    ("4663", "Aarburg", "AG", "de", 8), ("4665", "Oftringen", "AG", "de", 14),
    ("5722", "Gränichen", "AG", "de", 8), ("5734", "Reinach AG", "AG", "de", 9),
    ("5330", "Bad Zurzach", "AG", "de", 4), ("5070", "Frick", "AG", "de", 6),
    ("5080", "Laufenburg", "AG", "de", 4), ("5033", "Buchs AG", "AG", "de", 8),
    ("5036", "Oberentfelden", "AG", "de", 8), ("5643", "Sins", "AG", "de", 4),
    ("8965", "Berikon", "AG", "de", 5), ("5507", "Mellingen", "AG", "de", 6),
    ("4852", "Rothrist", "AG", "de", 9), ("4802", "Strengelbach", "AG", "de", 5),
    # Thurgau
    ("8280", "Kreuzlingen", "TG", "de", 22), ("9320", "Arbon", "TG", "de", 15),
    ("8590", "Romanshorn", "TG", "de", 11), ("8570", "Weinfelden", "TG", "de", 11),
    ("8580", "Amriswil", "TG", "de", 14), ("8360", "Eschlikon", "TG", "de", 4),
    ("9542", "Münchwilen TG", "TG", "de", 5), ("8266", "Steckborn", "TG", "de", 4),
    ("8355", "Aadorf", "TG", "de", 9),
    # Tessin
    ("6900", "Lugano", "TI", "it", 63), ("6500", "Bellinzona", "TI", "it", 44),
    ("6600", "Locarno", "TI", "it", 16), ("6850", "Mendrisio", "TI", "it", 15),
    ("6830", "Chiasso", "TI", "it", 8), ("6612", "Ascona", "TI", "it", 5),
    ("6982", "Agno", "TI", "it", 4), ("6710", "Biasca", "TI", "it", 6),
    ("6592", "Sant'Antonino", "TI", "it", 2.5), ("6828", "Balerna", "TI", "it", 3.5),
    ("6942", "Savosa", "TI", "it", 2), ("6614", "Brissago", "TI", "it", 2),
    ("6928", "Manno", "TI", "it", 1.3),
    # Waadt
    ("1003", "Lausanne", "VD", "fr", 140), ("1400", "Yverdon-les-Bains", "VD", "fr", 30),
    ("1800", "Vevey", "VD", "fr", 20), ("1820", "Montreux", "VD", "fr", 26),
    ("1110", "Morges", "VD", "fr", 16), ("1260", "Nyon", "VD", "fr", 21),
    ("1020", "Renens VD", "VD", "fr", 21), ("1030", "Bussigny", "VD", "fr", 9),
    ("1040", "Echallens", "VD", "fr", 6), ("1350", "Orbe", "VD", "fr", 7),
    ("1450", "Sainte-Croix", "VD", "fr", 4.5), ("1860", "Aigle", "VD", "fr", 10),
    ("1009", "Pully", "VD", "fr", 18), ("1180", "Rolle", "VD", "fr", 6),
    ("1196", "Gland", "VD", "fr", 13), ("1530", "Payerne", "VD", "fr", 10),
    ("1510", "Moudon", "VD", "fr", 6), ("1315", "La Sarraz", "VD", "fr", 2.5),
    ("1025", "St-Sulpice VD", "VD", "fr", 4), ("1066", "Epalinges", "VD", "fr", 10),
    ("1023", "Crissier", "VD", "fr", 8), ("1052", "Le Mont-sur-Lausanne", "VD", "fr", 9),
    ("1854", "Leysin", "VD", "fr", 4), ("1337", "Vallorbe", "VD", "fr", 3.5),
    # Wallis
    ("1950", "Sion", "VS", "fr", 35), ("1920", "Martigny", "VS", "fr", 18),
    ("3900", "Brig", "VS", "de", 13), ("3930", "Visp", "VS", "de", 8),
    ("1870", "Monthey", "VS", "fr", 18), ("3920", "Zermatt", "VS", "de", 6),
    ("1936", "Verbier", "VS", "fr", 3), ("3954", "Leukerbad", "VS", "de", 1.5),
    ("1963", "Vétroz", "VS", "fr", 6), ("3960", "Sierre", "VS", "fr", 17),
    ("1890", "St-Maurice", "VS", "fr", 4.5), ("3904", "Naters", "VS", "de", 10),
    ("1997", "Haute-Nendaz", "VS", "fr", 3), ("3906", "Saas-Fee", "VS", "de", 1.5),
    ("1907", "Saxon", "VS", "fr", 6), ("1868", "Collombey", "VS", "fr", 9),
    # Neuenburg, Genf, Jura
    ("2000", "Neuchâtel", "NE", "fr", 45), ("2300", "La Chaux-de-Fonds", "NE", "fr", 37),
    ("2400", "Le Locle", "NE", "fr", 10), ("2074", "Marin-Epagnier", "NE", "fr", 6),
    ("2034", "Peseux", "NE", "fr", 6), ("2013", "Colombier NE", "NE", "fr", 5.5),
    ("2114", "Fleurier", "NE", "fr", 4), ("2525", "Le Landeron", "NE", "fr", 4.5),
    ("1201", "Genève", "GE", "fr", 200), ("1227", "Carouge GE", "GE", "fr", 22),
    ("1214", "Vernier", "GE", "fr", 35), ("1217", "Meyrin", "GE", "fr", 25),
    ("1224", "Chêne-Bougeries", "GE", "fr", 12), ("1212", "Grand-Lancy", "GE", "fr", 33),
    ("1218", "Le Grand-Saconnex", "GE", "fr", 12), ("1290", "Versoix", "GE", "fr", 13),
    ("1226", "Thônex", "GE", "fr", 15), ("1213", "Onex", "GE", "fr", 19),
    ("1228", "Plan-les-Ouates", "GE", "fr", 11), ("1245", "Collonge-Bellerive", "GE", "fr", 8),
    ("2800", "Delémont", "JU", "fr", 12), ("2900", "Porrentruy", "JU", "fr", 7),
    ("2350", "Saignelégier", "JU", "fr", 2.5), ("2822", "Courroux", "JU", "fr", 3),
    ("2830", "Courrendlin", "JU", "fr", 3), ("2854", "Bassecourt", "JU", "fr", 3.5),
    ("2926", "Boncourt", "JU", "fr", 1.2),
]

# Tarifzonen CH (Haftpflicht-Regionalfaktor): 1 = Grossstadt/teure Agglomeration, 2 = Mittelland/
# Agglomeration, 3 = laendlich/alpin. Zuordnung ueber Kanton, Grossstaedte ueberschreiben.
TARIFZONE_CH_KANTON = {
    "ZH": "2", "GE": "1", "BS": "1", "VD": "2", "BE": "2", "AG": "2", "SO": "2", "LU": "2",
    "SG": "2", "TG": "2", "ZG": "1", "BL": "2", "TI": "2", "FR": "2", "NE": "2", "SH": "2",
    "SZ": "2", "GR": "3", "VS": "3", "JU": "3", "UR": "3", "OW": "3", "NW": "3", "GL": "3",
    "AR": "3", "AI": "3",
}
GROSSSTAEDTE_CH = {"Zürich", "Genève", "Basel", "Lausanne", "Bern", "Winterthur", "Luzern", "St. Gallen",
                   "Lugano", "Biel/Bienne"}

# ---------------------------------------------------------------------------------------------
# Orte Deutschland: (plz, ort, bundesland_kuerzel, einwohner_tsd)
# ---------------------------------------------------------------------------------------------
BUNDESLAENDER = {
    "BW": "Baden-Württemberg", "BY": "Bayern", "BE": "Berlin", "BB": "Brandenburg", "HB": "Bremen",
    "HH": "Hamburg", "HE": "Hessen", "MV": "Mecklenburg-Vorpommern", "NI": "Niedersachsen",
    "NW": "Nordrhein-Westfalen", "RP": "Rheinland-Pfalz", "SL": "Saarland", "SN": "Sachsen",
    "ST": "Sachsen-Anhalt", "SH": "Schleswig-Holstein", "TH": "Thüringen",
}

ORTE_DE: list[tuple[str, str, str, float]] = [
    # Berlin (mehrere PLZ, Ortsteil im Ortsnamen)
    ("10115", "Berlin", "BE", 90), ("10178", "Berlin", "BE", 80), ("10245", "Berlin", "BE", 120),
    ("10405", "Berlin", "BE", 110), ("10585", "Berlin", "BE", 100), ("10707", "Berlin", "BE", 90),
    ("10823", "Berlin", "BE", 100), ("10961", "Berlin", "BE", 110), ("10999", "Berlin", "BE", 90),
    ("12043", "Berlin", "BE", 130), ("12157", "Berlin", "BE", 90), ("12435", "Berlin", "BE", 80),
    ("12489", "Berlin", "BE", 60), ("12555", "Berlin", "BE", 70), ("13086", "Berlin", "BE", 70),
    ("13347", "Berlin", "BE", 100), ("13405", "Berlin", "BE", 80), ("13593", "Berlin", "BE", 90),
    ("14109", "Berlin", "BE", 40), ("14195", "Berlin", "BE", 50),
    # Hamburg
    ("20095", "Hamburg", "HH", 90), ("20144", "Hamburg", "HH", 80), ("20249", "Hamburg", "HH", 70),
    ("20357", "Hamburg", "HH", 80), ("20457", "Hamburg", "HH", 50), ("20537", "Hamburg", "HH", 60),
    ("21029", "Hamburg", "HH", 60), ("21073", "Hamburg", "HH", 70), ("22041", "Hamburg", "HH", 70),
    ("22083", "Hamburg", "HH", 60), ("22111", "Hamburg", "HH", 70), ("22297", "Hamburg", "HH", 50),
    ("22359", "Hamburg", "HH", 40), ("22525", "Hamburg", "HH", 50), ("22587", "Hamburg", "HH", 30),
    ("22765", "Hamburg", "HH", 70),
    # Bremen
    ("28195", "Bremen", "HB", 90), ("28213", "Bremen", "HB", 60), ("28359", "Bremen", "HB", 60),
    ("28717", "Bremen", "HB", 50), ("28779", "Bremen", "HB", 40), ("27568", "Bremerhaven", "HB", 60),
    ("27574", "Bremerhaven", "HB", 50),
    # Baden-Wuerttemberg
    ("70173", "Stuttgart", "BW", 150), ("70199", "Stuttgart", "BW", 100), ("70435", "Stuttgart", "BW", 90),
    ("70565", "Stuttgart", "BW", 90), ("70619", "Stuttgart", "BW", 70), ("70806", "Kornwestheim", "BW", 34),
    ("71032", "Böblingen", "BW", 50), ("71063", "Sindelfingen", "BW", 65), ("71083", "Herrenberg", "BW", 32),
    ("71229", "Leonberg", "BW", 49), ("71332", "Waiblingen", "BW", 56), ("71364", "Winnenden", "BW", 29),
    ("71634", "Ludwigsburg", "BW", 93), ("71665", "Vaihingen an der Enz", "BW", 30),
    ("72070", "Tübingen", "BW", 92), ("72250", "Freudenstadt", "BW", 24), ("72336", "Balingen", "BW", 35),
    ("72379", "Hechingen", "BW", 20), ("72458", "Albstadt", "BW", 45), ("72488", "Sigmaringen", "BW", 17),
    ("72555", "Metzingen", "BW", 23), ("72622", "Nürtingen", "BW", 42), ("72764", "Reutlingen", "BW", 117),
    ("73033", "Göppingen", "BW", 58), ("73230", "Kirchheim unter Teck", "BW", 41),
    ("73312", "Geislingen an der Steige", "BW", 28), ("73430", "Aalen", "BW", 68),
    ("73525", "Schwäbisch Gmünd", "BW", 61), ("73728", "Esslingen am Neckar", "BW", 93),
    ("74072", "Heilbronn", "BW", 127), ("74172", "Neckarsulm", "BW", 27),
    ("74321", "Bietigheim-Bissingen", "BW", 43), ("74523", "Schwäbisch Hall", "BW", 42),
    ("74564", "Crailsheim", "BW", 35), ("74653", "Künzelsau", "BW", 15), ("74821", "Mosbach", "BW", 23),
    ("74889", "Sinsheim", "BW", 36), ("75015", "Bretten", "BW", 30), ("75172", "Pforzheim", "BW", 126),
    ("75365", "Calw", "BW", 24), ("76133", "Karlsruhe", "BW", 310), ("76275", "Ettlingen", "BW", 39),
    ("76437", "Rastatt", "BW", 50), ("76530", "Baden-Baden", "BW", 56), ("76646", "Bruchsal", "BW", 46),
    ("77652", "Offenburg", "BW", 61), ("77694", "Kehl", "BW", 37), ("77855", "Achern", "BW", 26),
    ("77933", "Lahr", "BW", 48), ("78050", "Villingen-Schwenningen", "BW", 86), ("78224", "Singen", "BW", 48),
    ("78462", "Konstanz", "BW", 86), ("78532", "Tuttlingen", "BW", 37), ("78628", "Rottweil", "BW", 26),
    ("79098", "Freiburg im Breisgau", "BW", 232), ("79539", "Lörrach", "BW", 50),
    ("79618", "Rheinfelden (Baden)", "BW", 33), ("79713", "Bad Säckingen", "BW", 18),
    ("79761", "Waldshut-Tiengen", "BW", 25), ("88045", "Friedrichshafen", "BW", 62),
    ("88212", "Ravensburg", "BW", 51), ("88400", "Biberach an der Riss", "BW", 34),
    ("88662", "Überlingen", "BW", 23), ("89073", "Ulm", "BW", 128), ("89518", "Heidenheim", "BW", 50),
    ("68159", "Mannheim", "BW", 315), ("69115", "Heidelberg", "BW", 160), ("69469", "Weinheim", "BW", 45),
    # Bayern
    ("80331", "München", "BY", 150), ("80636", "München", "BY", 120), ("80797", "München", "BY", 120),
    ("81241", "München", "BY", 100), ("81371", "München", "BY", 110), ("81541", "München", "BY", 100),
    ("81673", "München", "BY", 90), ("81925", "München", "BY", 80), ("82031", "Grünwald", "BY", 11),
    ("82152", "Planegg", "BY", 11), ("82256", "Fürstenfeldbruck", "BY", 38), ("82319", "Starnberg", "BY", 23),
    ("82362", "Weilheim in Oberbayern", "BY", 23), ("82467", "Garmisch-Partenkirchen", "BY", 27),
    ("83022", "Rosenheim", "BY", 64), ("83278", "Traunstein", "BY", 21), ("83395", "Freilassing", "BY", 17),
    ("83646", "Bad Tölz", "BY", 19), ("84028", "Landshut", "BY", 74), ("84503", "Altötting", "BY", 13),
    ("85049", "Ingolstadt", "BY", 139), ("85221", "Dachau", "BY", 48), ("85356", "Freising", "BY", 49),
    ("85435", "Erding", "BY", 37), ("85521", "Ottobrunn", "BY", 22), ("85737", "Ismaning", "BY", 18),
    ("86150", "Augsburg", "BY", 300), ("86720", "Nördlingen", "BY", 21), ("86899", "Landsberg am Lech", "BY", 29),
    ("87435", "Kempten (Allgäu)", "BY", 70), ("87600", "Kaufbeuren", "BY", 45), ("87700", "Memmingen", "BY", 44),
    ("88131", "Lindau (Bodensee)", "BY", 26), ("89231", "Neu-Ulm", "BY", 60), ("90402", "Nürnberg", "BY", 520),
    ("90762", "Fürth", "BY", 130), ("91052", "Erlangen", "BY", 115), ("91126", "Schwabach", "BY", 41),
    ("91522", "Ansbach", "BY", 42), ("92224", "Amberg", "BY", 42), ("92637", "Weiden in der Oberpfalz", "BY", 43),
    ("93047", "Regensburg", "BY", 155), ("94032", "Passau", "BY", 53), ("94315", "Straubing", "BY", 48),
    ("94469", "Deggendorf", "BY", 34), ("95028", "Hof", "BY", 46), ("95444", "Bayreuth", "BY", 75),
    ("96047", "Bamberg", "BY", 78), ("96450", "Coburg", "BY", 41), ("97070", "Würzburg", "BY", 128),
    ("97421", "Schweinfurt", "BY", 54), ("63739", "Aschaffenburg", "BY", 72), ("84453", "Mühldorf am Inn", "BY", 21),
    ("85276", "Pfaffenhofen an der Ilm", "BY", 26), ("86551", "Aichach", "BY", 21),
    # Hessen
    ("60311", "Frankfurt am Main", "HE", 150), ("60486", "Frankfurt am Main", "HE", 110),
    ("60598", "Frankfurt am Main", "HE", 100), ("60320", "Frankfurt am Main", "HE", 90),
    ("65929", "Frankfurt am Main", "HE", 80), ("61118", "Bad Vilbel", "HE", 35),
    ("61169", "Friedberg (Hessen)", "HE", 30), ("61348", "Bad Homburg vor der Höhe", "HE", 54),
    ("61440", "Oberursel (Taunus)", "HE", 47), ("63065", "Offenbach am Main", "HE", 132),
    ("63225", "Langen (Hessen)", "HE", 39), ("63450", "Hanau", "HE", 100), ("63571", "Gelnhausen", "HE", 23),
    ("64283", "Darmstadt", "HE", 162), ("64521", "Groß-Gerau", "HE", 26), ("64646", "Heppenheim", "HE", 26),
    ("64720", "Michelstadt", "HE", 16), ("65183", "Wiesbaden", "HE", 280), ("65343", "Eltville am Rhein", "HE", 17),
    ("65428", "Rüsselsheim am Main", "HE", 66), ("65510", "Idstein", "HE", 25), ("65549", "Limburg an der Lahn", "HE", 36),
    ("65760", "Eschborn", "HE", 22), ("65812", "Bad Soden am Taunus", "HE", 23), ("34117", "Kassel", "HE", 200),
    ("34212", "Melsungen", "HE", 14), ("35037", "Marburg", "HE", 78), ("35390", "Gießen", "HE", 92),
    ("35576", "Wetzlar", "HE", 54), ("35683", "Dillenburg", "HE", 23), ("36037", "Fulda", "HE", 69),
    ("36251", "Bad Hersfeld", "HE", 30), ("65719", "Hofheim am Taunus", "HE", 40), ("61231", "Bad Nauheim", "HE", 33),
    ("68519", "Viernheim", "HE", 34), ("64625", "Bensheim", "HE", 41), ("36304", "Alsfeld", "HE", 16),
    # Niedersachsen
    ("30159", "Hannover", "NI", 150), ("30419", "Hannover", "NI", 110), ("30625", "Hannover", "NI", 100),
    ("30880", "Laatzen", "NI", 43), ("30823", "Garbsen", "NI", 61), ("31134", "Hildesheim", "NI", 101),
    ("31224", "Peine", "NI", 50), ("31303", "Burgdorf", "NI", 31), ("31515", "Wunstorf", "NI", 42),
    ("31582", "Nienburg (Weser)", "NI", 32), ("31655", "Stadthagen", "NI", 22), ("31785", "Hameln", "NI", 57),
    ("37073", "Göttingen", "NI", 119), ("37154", "Northeim", "NI", 29), ("37574", "Einbeck", "NI", 31),
    ("38100", "Braunschweig", "NI", 250), ("38226", "Salzgitter", "NI", 104), ("38300", "Wolfenbüttel", "NI", 52),
    ("38440", "Wolfsburg", "NI", 124), ("38518", "Gifhorn", "NI", 42), ("38640", "Goslar", "NI", 50),
    ("26121", "Oldenburg", "NI", 170), ("26382", "Wilhelmshaven", "NI", 76), ("26506", "Norden", "NI", 25),
    ("26603", "Aurich", "NI", 42), ("26721", "Emden", "NI", 50), ("26789", "Leer (Ostfriesland)", "NI", 35),
    ("27283", "Verden (Aller)", "NI", 28), ("27356", "Rotenburg (Wümme)", "NI", 22), ("27472", "Cuxhaven", "NI", 48),
    ("27749", "Delmenhorst", "NI", 77), ("28816", "Stuhr", "NI", 34), ("29221", "Celle", "NI", 69),
    ("29525", "Uelzen", "NI", 33), ("29614", "Soltau", "NI", 22), ("21335", "Lüneburg", "NI", 77),
    ("21614", "Buxtehude", "NI", 41), ("21680", "Stade", "NI", 48), ("21423", "Winsen (Luhe)", "NI", 36),
    ("49074", "Osnabrück", "NI", 165), ("49377", "Vechta", "NI", 33), ("49661", "Cloppenburg", "NI", 36),
    ("49808", "Lingen (Ems)", "NI", 58), ("48527", "Nordhorn", "NI", 54), ("49716", "Meppen", "NI", 36),
    ("37603", "Holzminden", "NI", 20), ("30926", "Seelze", "NI", 34), ("21244", "Buchholz in der Nordheide", "NI", 41),
    # Nordrhein-Westfalen
    ("40213", "Düsseldorf", "NW", 150), ("40476", "Düsseldorf", "NW", 120), ("40699", "Erkrath", "NW", 44),
    ("40721", "Hilden", "NW", 56), ("40764", "Langenfeld (Rheinland)", "NW", 59), ("40822", "Mettmann", "NW", 39),
    ("40878", "Ratingen", "NW", 88), ("41061", "Mönchengladbach", "NW", 260), ("41460", "Neuss", "NW", 153),
    ("41515", "Grevenbroich", "NW", 63), ("41747", "Viersen", "NW", 77), ("42103", "Wuppertal", "NW", 355),
    ("42551", "Velbert", "NW", 82), ("42651", "Solingen", "NW", 160), ("42853", "Remscheid", "NW", 111),
    ("44135", "Dortmund", "NW", 590), ("44532", "Lünen", "NW", 86), ("44575", "Castrop-Rauxel", "NW", 73),
    ("44623", "Herne", "NW", 156), ("44787", "Bochum", "NW", 365), ("45127", "Essen", "NW", 580),
    ("45468", "Mülheim an der Ruhr", "NW", 170), ("45657", "Recklinghausen", "NW", 112),
    ("45879", "Gelsenkirchen", "NW", 260), ("46045", "Oberhausen", "NW", 210), ("46236", "Bottrop", "NW", 117),
    ("46395", "Bocholt", "NW", 71), ("46483", "Wesel", "NW", 60), ("47051", "Duisburg", "NW", 500),
    ("47441", "Moers", "NW", 104), ("47798", "Krefeld", "NW", 227), ("48143", "Münster", "NW", 316),
    ("48431", "Rheine", "NW", 76), ("48565", "Steinfurt", "NW", 34), ("48653", "Coesfeld", "NW", 36),
    ("49477", "Ibbenbüren", "NW", 52), ("50667", "Köln", "NW", 200), ("50823", "Köln", "NW", 150),
    ("51063", "Köln", "NW", 140), ("50858", "Köln", "NW", 100), ("50226", "Frechen", "NW", 52),
    ("50354", "Hürth", "NW", 61), ("50374", "Erftstadt", "NW", 50), ("50389", "Wesseling", "NW", 37),
    ("51371", "Leverkusen", "NW", 164), ("51427", "Bergisch Gladbach", "NW", 112), ("51643", "Gummersbach", "NW", 51),
    ("52062", "Aachen", "NW", 250), ("52349", "Düren", "NW", 92), ("52511", "Geilenkirchen", "NW", 28),
    ("53111", "Bonn", "NW", 330), ("53721", "Siegburg", "NW", 42), ("53757", "Sankt Augustin", "NW", 56),
    ("53840", "Troisdorf", "NW", 76), ("53879", "Euskirchen", "NW", 59), ("57072", "Siegen", "NW", 102),
    ("57462", "Olpe", "NW", 25), ("58095", "Hagen", "NW", 190), ("58239", "Schwerte", "NW", 47),
    ("58452", "Witten", "NW", 97), ("58507", "Lüdenscheid", "NW", 73), ("58636", "Iserlohn", "NW", 93),
    ("59065", "Hamm", "NW", 180), ("59174", "Kamen", "NW", 44), ("59423", "Unna", "NW", 59),
    ("59494", "Soest", "NW", 48), ("59555", "Lippstadt", "NW", 68), ("59821", "Arnsberg", "NW", 74),
    ("33098", "Paderborn", "NW", 152), ("33330", "Gütersloh", "NW", 101), ("33602", "Bielefeld", "NW", 335),
    ("32052", "Herford", "NW", 67), ("32423", "Minden", "NW", 84), ("32756", "Detmold", "NW", 75),
    ("45964", "Gladbeck", "NW", 76), ("47533", "Kleve", "NW", 52), ("47623", "Kevelaer", "NW", 28),
    ("41812", "Erkelenz", "NW", 44), ("52146", "Würselen", "NW", 39), ("59872", "Meschede", "NW", 30),
    ("48231", "Warendorf", "NW", 37), ("59269", "Beckum", "NW", 37), ("53604", "Bad Honnef", "NW", 26),
    # Rheinland-Pfalz
    ("55116", "Mainz", "RP", 220), ("55411", "Bingen am Rhein", "RP", 25), ("55543", "Bad Kreuznach", "RP", 51),
    ("55743", "Idar-Oberstein", "RP", 29), ("56068", "Koblenz", "RP", 114), ("56410", "Montabaur", "RP", 14),
    ("56564", "Neuwied", "RP", 65), ("56727", "Mayen", "RP", 19), ("56812", "Cochem", "RP", 5),
    ("54290", "Trier", "RP", 111), ("54516", "Wittlich", "RP", 19), ("54634", "Bitburg", "RP", 15),
    ("55232", "Alzey", "RP", 19), ("67059", "Ludwigshafen am Rhein", "RP", 172), ("67227", "Frankenthal (Pfalz)", "RP", 49),
    ("67346", "Speyer", "RP", 51), ("67433", "Neustadt an der Weinstraße", "RP", 53), ("67547", "Worms", "RP", 84),
    ("67655", "Kaiserslautern", "RP", 100), ("66482", "Zweibrücken", "RP", 34), ("66953", "Pirmasens", "RP", 40),
    ("76829", "Landau in der Pfalz", "RP", 47), ("53474", "Bad Neuenahr-Ahrweiler", "RP", 28),
    ("57610", "Altenkirchen (Westerwald)", "RP", 6), ("67098", "Bad Dürkheim", "RP", 19),
    ("55218", "Ingelheim am Rhein", "RP", 36), ("65582", "Diez", "RP", 11), ("56130", "Bad Ems", "RP", 10),
    # Saarland
    ("66111", "Saarbrücken", "SL", 180), ("66424", "Homburg", "SL", 42), ("66538", "Neunkirchen", "SL", 46),
    ("66740", "Saarlouis", "SL", 35), ("66822", "Lebach", "SL", 19), ("66663", "Merzig", "SL", 30),
    ("66386", "St. Ingbert", "SL", 36), ("66606", "St. Wendel", "SL", 26), ("66333", "Völklingen", "SL", 39),
    ("66280", "Sulzbach/Saar", "SL", 16),
    # Sachsen
    ("01067", "Dresden", "SN", 150), ("01097", "Dresden", "SN", 120), ("01159", "Dresden", "SN", 100),
    ("01219", "Dresden", "SN", 100), ("01309", "Dresden", "SN", 90), ("01445", "Radebeul", "SN", 34),
    ("01587", "Riesa", "SN", 30), ("01662", "Meißen", "SN", 28), ("01796", "Pirna", "SN", 38),
    ("01855", "Sebnitz", "SN", 9), ("01877", "Bischofswerda", "SN", 11), ("01917", "Kamenz", "SN", 15),
    ("02625", "Bautzen", "SN", 38), ("02763", "Zittau", "SN", 25), ("02826", "Görlitz", "SN", 56),
    ("02977", "Hoyerswerda", "SN", 32), ("04103", "Leipzig", "SN", 150), ("04155", "Leipzig", "SN", 120),
    ("04229", "Leipzig", "SN", 110), ("04275", "Leipzig", "SN", 100), ("04315", "Leipzig", "SN", 90),
    ("04357", "Leipzig", "SN", 80), ("04416", "Markkleeberg", "SN", 25), ("04509", "Delitzsch", "SN", 25),
    ("04720", "Döbeln", "SN", 24), ("04808", "Wurzen", "SN", 16), ("04838", "Eilenburg", "SN", 16),
    ("08056", "Zwickau", "SN", 88), ("08209", "Auerbach/Vogtland", "SN", 18), ("08280", "Aue-Bad Schlema", "SN", 20),
    ("08371", "Glauchau", "SN", 22), ("08523", "Plauen", "SN", 64), ("09111", "Chemnitz", "SN", 150),
    ("09112", "Chemnitz", "SN", 90), ("09217", "Burgstädt", "SN", 11), ("09306", "Rochlitz", "SN", 6),
    ("09405", "Zschopau", "SN", 9), ("09456", "Annaberg-Buchholz", "SN", 20), ("09496", "Marienberg", "SN", 17),
    ("09599", "Freiberg", "SN", 40), ("09648", "Mittweida", "SN", 14), ("04552", "Borna", "SN", 19),
    # Sachsen-Anhalt
    ("39104", "Magdeburg", "ST", 150), ("39112", "Magdeburg", "ST", 90), ("39218", "Schönebeck (Elbe)", "ST", 30),
    ("39288", "Burg", "ST", 22), ("39340", "Haldensleben", "ST", 19), ("39576", "Stendal", "ST", 39),
    ("39638", "Gardelegen", "ST", 22), ("06108", "Halle (Saale)", "ST", 130), ("06120", "Halle (Saale)", "ST", 100),
    ("06217", "Merseburg", "ST", 33), ("06366", "Köthen (Anhalt)", "ST", 25), ("06406", "Bernburg (Saale)", "ST", 32),
    ("06484", "Quedlinburg", "ST", 24), ("06526", "Sangerhausen", "ST", 26), ("06618", "Naumburg (Saale)", "ST", 32),
    ("06712", "Zeitz", "ST", 27), ("06766", "Bitterfeld-Wolfen", "ST", 38), ("06844", "Dessau-Roßlau", "ST", 79),
    ("06886", "Lutherstadt Wittenberg", "ST", 45), ("38855", "Wernigerode", "ST", 32), ("38820", "Halberstadt", "ST", 40),
    ("29410", "Salzwedel", "ST", 23), ("06295", "Lutherstadt Eisleben", "ST", 22), ("06449", "Aschersleben", "ST", 26),
    # Schleswig-Holstein
    ("24103", "Kiel", "SH", 150), ("24143", "Kiel", "SH", 90), ("24534", "Neumünster", "SH", 80),
    ("24837", "Schleswig", "SH", 25), ("24937", "Flensburg", "SH", 92), ("25336", "Elmshorn", "SH", 51),
    ("25421", "Pinneberg", "SH", 44), ("25746", "Heide", "SH", 22), ("25813", "Husum", "SH", 23),
    ("25980", "Sylt", "SH", 14), ("22850", "Norderstedt", "SH", 80), ("22926", "Ahrensburg", "SH", 34),
    ("23552", "Lübeck", "SH", 220), ("23701", "Eutin", "SH", 17), ("23730", "Neustadt in Holstein", "SH", 16),
    ("23795", "Bad Segeberg", "SH", 18), ("23843", "Bad Oldesloe", "SH", 25), ("23909", "Ratzeburg", "SH", 15),
    ("24768", "Rendsburg", "SH", 29), ("24211", "Preetz", "SH", 16), ("21465", "Reinbek", "SH", 28),
    ("21502", "Geesthacht", "SH", 31), ("25541", "Brunsbüttel", "SH", 13), ("25348", "Glückstadt", "SH", 11),
    # Mecklenburg-Vorpommern
    ("19053", "Schwerin", "MV", 97), ("19370", "Parchim", "MV", 18), ("18055", "Rostock", "MV", 150),
    ("18119", "Rostock", "MV", 60), ("18273", "Güstrow", "MV", 29), ("18437", "Stralsund", "MV", 60),
    ("18528", "Bergen auf Rügen", "MV", 13), ("17033", "Neubrandenburg", "MV", 64), ("17109", "Demmin", "MV", 11),
    ("17235", "Neustrelitz", "MV", 20), ("17389", "Anklam", "MV", 12), ("17489", "Greifswald", "MV", 59),
    ("23936", "Grevesmühlen", "MV", 10), ("23966", "Wismar", "MV", 43), ("18209", "Bad Doberan", "MV", 13),
    ("17192", "Waren (Müritz)", "MV", 21), ("19288", "Ludwigslust", "MV", 12), ("17358", "Torgelow", "MV", 9),
    # Brandenburg
    ("14467", "Potsdam", "BB", 100), ("14469", "Potsdam", "BB", 80), ("14513", "Teltow", "BB", 28),
    ("14532", "Kleinmachnow", "BB", 20), ("14612", "Falkensee", "BB", 45), ("14641", "Nauen", "BB", 18),
    ("14770", "Brandenburg an der Havel", "BB", 72), ("14806", "Bad Belzig", "BB", 11), ("14943", "Luckenwalde", "BB", 21),
    ("15230", "Frankfurt (Oder)", "BB", 57), ("15344", "Strausberg", "BB", 27), ("15517", "Fürstenwalde/Spree", "BB", 32),
    ("15711", "Königs Wusterhausen", "BB", 38), ("15745", "Wildau", "BB", 11), ("15806", "Zossen", "BB", 20),
    ("15831", "Blankenfelde-Mahlow", "BB", 29), ("15848", "Beeskow", "BB", 8), ("15890", "Eisenhüttenstadt", "BB", 24),
    ("16225", "Eberswalde", "BB", 40), ("16303", "Schwedt/Oder", "BB", 30), ("16321", "Bernau bei Berlin", "BB", 41),
    ("16515", "Oranienburg", "BB", 47), ("16761", "Hennigsdorf", "BB", 27), ("16816", "Neuruppin", "BB", 31),
    ("16909", "Wittstock/Dosse", "BB", 14), ("17291", "Prenzlau", "BB", 19), ("03046", "Cottbus", "BB", 100),
    ("03172", "Guben", "BB", 17), ("03222", "Lübbenau/Spreewald", "BB", 16), ("03238", "Finsterwalde", "BB", 16),
    ("04910", "Elsterwerda", "BB", 8), ("01968", "Senftenberg", "BB", 24), ("19348", "Perleberg", "BB", 12),
    # Thueringen
    ("99084", "Erfurt", "TH", 130), ("99089", "Erfurt", "TH", 80), ("99423", "Weimar", "TH", 65),
    ("99510", "Apolda", "TH", 22), ("99610", "Sömmerda", "TH", 19), ("99706", "Sondershausen", "TH", 21),
    ("99734", "Nordhausen", "TH", 41), ("99817", "Eisenach", "TH", 42), ("99867", "Gotha", "TH", 45),
    ("99947", "Bad Langensalza", "TH", 17), ("07545", "Gera", "TH", 93), ("07607", "Eisenberg", "TH", 11),
    ("07743", "Jena", "TH", 110), ("07907", "Schleiz", "TH", 8), ("07973", "Greiz", "TH", 20),
    ("98527", "Suhl", "TH", 36), ("98617", "Meiningen", "TH", 25), ("98693", "Ilmenau", "TH", 38),
    ("98544", "Zella-Mehlis", "TH", 12), ("96515", "Sonneberg", "TH", 23), ("98574", "Schmalkalden", "TH", 20),
    ("37308", "Heilbad Heiligenstadt", "TH", 17), ("37339", "Leinefelde-Worbis", "TH", 19), ("07318", "Saalfeld/Saale", "TH", 29),
    ("07407", "Rudolstadt", "TH", 24), ("36433", "Bad Salzungen", "TH", 15), ("99310", "Arnstadt", "TH", 27),
    ("04600", "Altenburg", "TH", 31), ("07356", "Bad Lobenstein", "TH", 6),
]

# Tarifzonen DE: aus PLZ-Leitregion (erste Ziffer) und Grossstadt-Status; 1 = teuer, 3 = guenstig.
GROSSSTAEDTE_DE = {"Berlin", "Hamburg", "München", "Köln", "Frankfurt am Main", "Stuttgart", "Düsseldorf",
                   "Leipzig", "Dortmund", "Essen", "Bremen", "Dresden", "Hannover", "Nürnberg", "Duisburg",
                   "Bochum", "Wuppertal", "Bielefeld", "Bonn", "Münster", "Karlsruhe", "Mannheim",
                   "Augsburg", "Wiesbaden", "Mönchengladbach", "Gelsenkirchen", "Braunschweig", "Aachen",
                   "Kiel", "Chemnitz", "Halle (Saale)", "Magdeburg", "Freiburg im Breisgau", "Krefeld",
                   "Mainz", "Lübeck", "Erfurt", "Oberhausen", "Rostock", "Kassel", "Hagen", "Saarbrücken",
                   "Potsdam", "Ludwigshafen am Rhein", "Oldenburg", "Osnabrück", "Leverkusen", "Heidelberg",
                   "Darmstadt", "Solingen", "Regensburg", "Herne", "Paderborn", "Neuss", "Ingolstadt",
                   "Offenbach am Main", "Fürth", "Würzburg", "Ulm", "Heilbronn", "Pforzheim", "Wolfsburg",
                   "Göttingen", "Bottrop", "Reutlingen", "Koblenz", "Bremerhaven", "Recklinghausen",
                   "Erlangen", "Bergisch Gladbach", "Trier", "Jena", "Remscheid", "Salzgitter", "Moers",
                   "Siegen", "Hildesheim", "Gütersloh", "Kaiserslautern", "Cottbus", "Schwerin"}


def urbanitaet(einwohner_tsd: float, ort: str, grossstaedte: set[str]) -> str:
    if ort in grossstaedte or einwohner_tsd >= 100:
        return "STADT"
    if einwohner_tsd >= 10:
        return "AGGLO"
    return "LAND"


def tarifzone_de(plz: str, ort: str, einwohner_tsd: float) -> str:
    if ort in {"Berlin", "Hamburg", "München", "Köln", "Frankfurt am Main", "Stuttgart", "Düsseldorf"}:
        return "1"
    if ort in GROSSSTAEDTE_DE or einwohner_tsd >= 100:
        return "2"
    return "3"


# ---------------------------------------------------------------------------------------------
# Strassennamen (generiert: Stamm x Typ)
# ---------------------------------------------------------------------------------------------
STAEMME_DE = [
    "Ahorn", "Birken", "Linden", "Rosen", "Tannen", "Buchen", "Eichen", "Erlen", "Eschen", "Fichten",
    "Föhren", "Kastanien", "Pappel", "Ulmen", "Weiden", "Kirsch", "Apfel", "Nuss", "Holunder", "Flieder",
    "Tulpen", "Nelken", "Veilchen", "Enzian", "Edelweiss", "Alpenrosen", "Farn", "Moos", "Heide", "Wiesen",
    "Feld", "Acker", "Garten", "Mühle", "Mühlen", "Brunnen", "Quell", "Bach", "Fluss", "Teich", "Weiher",
    "See", "Ufer", "Insel", "Brücken", "Steg", "Berg", "Hügel", "Tal", "Höhen", "Hang", "Halden", "Fels",
    "Stein", "Kies", "Sand", "Lehm", "Ton", "Sonnen", "Mond", "Sternen", "Morgen", "Abend", "Winter",
    "Sommer", "Frühlings", "Herbst", "Nord", "Süd", "Ost", "West", "Kirch", "Kapellen", "Kloster", "Schul",
    "Bahn", "Post", "Markt", "Rathaus", "Zunft", "Schmiede", "Weber", "Müller", "Gerber", "Färber", "Bäcker",
    "Metzger", "Sattler", "Wagner", "Ziegel", "Kalk", "Salz", "Eisen", "Kupfer", "Silber", "Gold", "Bären",
    "Hirsch", "Reh", "Fuchs", "Hasen", "Adler", "Falken", "Lerchen", "Amsel", "Drossel", "Finken", "Meisen",
    "Schwalben", "Storchen", "Reiher", "Schwanen", "Enten", "Forellen", "Hecht", "Bienen", "Schmetterlings",
    "Amsel", "Rebstock", "Reben", "Trauben", "Hopfen", "Korn", "Roggen", "Hafer", "Gersten", "Flachs",
]
TYPEN_DE_CH = ["strasse", "weg", "gasse", "platz", "rain", "halde", "matte", "acker", "hof", "ring", "steig"]
TYPEN_DE_DE = ["straße", "weg", "gasse", "platz", "allee", "ring", "damm", "steig", "pfad", "hof", "kamp"]

STAEMME_FR = [
    "Tilleuls", "Bouleaux", "Chênes", "Érables", "Sapins", "Mélèzes", "Peupliers", "Saules", "Noyers",
    "Cerisiers", "Pommiers", "Vignes", "Roses", "Lilas", "Tulipes", "Œillets", "Violettes", "Gentianes",
    "Prés", "Champs", "Jardins", "Moulins", "Fontaines", "Sources", "Ruisseaux", "Rives", "Étangs", "Lacs",
    "Îles", "Ponts", "Collines", "Vallons", "Coteaux", "Rochers", "Pierres", "Sables", "Soleils", "Étoiles",
    "Aurores", "Crépuscules", "Hivers", "Printemps", "Automnes", "Chapelles", "Clochers", "Écoles", "Gares",
    "Marchés", "Forgerons", "Tisserands", "Meuniers", "Tanneurs", "Boulangers", "Bouchers", "Vignerons",
    "Bergers", "Cerfs", "Chevreuils", "Renards", "Lièvres", "Aigles", "Faucons", "Alouettes", "Merles",
    "Grives", "Pinsons", "Mésanges", "Hirondelles", "Cigognes", "Hérons", "Cygnes", "Truites", "Abeilles",
    "Papillons", "Ormes", "Frênes", "Aulnes", "Hêtres", "Châtaigniers", "Oliviers", "Lauriers", "Bruyères",
    "Fougères", "Mousses", "Genêts", "Cyclamens", "Narcisses", "Primevères", "Marronniers", "Platanes",
]
TYPEN_FR = ["Rue des", "Chemin des", "Avenue des", "Route des", "Impasse des", "Sentier des",
            "Allée des", "Place des", "Promenade des"]

STAEMME_IT = [
    "Tigli", "Betulle", "Querce", "Aceri", "Abeti", "Larici", "Pioppi", "Salici", "Noci", "Ciliegi", "Meli",
    "Vigne", "Rose", "Lillà", "Tulipani", "Garofani", "Viole", "Genziane", "Prati", "Campi", "Giardini",
    "Mulini", "Fontane", "Sorgenti", "Ruscelli", "Rive", "Stagni", "Laghi", "Ponti", "Colline", "Valli",
    "Rocce", "Sassi", "Sabbie", "Soli", "Stelle", "Aurore", "Tramonti", "Inverni", "Primavere", "Autunni",
    "Cappelle", "Campanili", "Scuole", "Stazioni", "Mercati", "Fabbri", "Tessitori", "Mugnai", "Conciatori",
    "Fornai", "Macellai", "Vignaioli", "Pastori", "Cervi", "Caprioli", "Volpi", "Lepri", "Aquile", "Falchi",
    "Allodole", "Merli", "Tordi", "Fringuelli", "Cince", "Rondini", "Cicogne", "Aironi", "Cigni", "Trote",
    "Api", "Farfalle", "Olmi", "Frassini", "Ontani", "Faggi", "Castagni", "Ulivi", "Allori", "Eriche",
    "Felci", "Muschi", "Ginestre", "Ciclamini", "Narcisi", "Primule", "Ippocastani", "Platani", "Glicini",
]
TYPEN_IT = ["Via dei", "Via delle", "Vicolo dei", "Viale dei", "Sentiero dei", "Piazza dei", "Strada dei",
            "Passaggio dei"]

GENERISCH = {"Hauptstrasse", "Bahnhofstrasse", "Dorfstrasse", "Kirchgasse", "Schulstrasse", "Hauptstraße",
             "Bahnhofstraße", "Dorfstraße", "Kirchstraße", "Schulstraße", "Rue de la Gare", "Grand-Rue",
             "Via Cantonale", "Via Stazione"}

# ---------------------------------------------------------------------------------------------
# Vornamen: (name, geschlecht, sprachraum, peak_dekade)
# ---------------------------------------------------------------------------------------------
VORNAMEN: list[tuple[str, str, str, int]] = [
    # de-CH weiblich
    ("Vreni", "W", "de-CH", 1930), ("Trudi", "W", "de-CH", 1930), ("Heidi", "W", "de-CH", 1940),
    ("Ruth", "W", "de-CH", 1940), ("Margrit", "W", "de-CH", 1940), ("Rosmarie", "W", "de-CH", 1940),
    ("Elisabeth", "W", "de-CH", 1940), ("Verena", "W", "de-CH", 1950), ("Ursula", "W", "de-CH", 1950),
    ("Silvia", "W", "de-CH", 1950), ("Beatrice", "W", "de-CH", 1950), ("Christine", "W", "de-CH", 1960),
    ("Barbara", "W", "de-CH", 1960), ("Monika", "W", "de-CH", 1960), ("Brigitte", "W", "de-CH", 1960),
    ("Daniela", "W", "de-CH", 1970), ("Sandra", "W", "de-CH", 1970), ("Andrea", "W", "de-CH", 1970),
    ("Claudia", "W", "de-CH", 1970), ("Nicole", "W", "de-CH", 1970), ("Manuela", "W", "de-CH", 1970),
    ("Nadine", "W", "de-CH", 1980), ("Stefanie", "W", "de-CH", 1980), ("Corinne", "W", "de-CH", 1980),
    ("Fabienne", "W", "de-CH", 1980), ("Melanie", "W", "de-CH", 1980), ("Jasmin", "W", "de-CH", 1990),
    ("Larissa", "W", "de-CH", 1990), ("Michelle", "W", "de-CH", 1990), ("Selina", "W", "de-CH", 1990),
    ("Tamara", "W", "de-CH", 1990), ("Lea", "W", "de-CH", 2000), ("Lara", "W", "de-CH", 2000),
    ("Mia", "W", "de-CH", 2000), ("Elena", "W", "de-CH", 2000), ("Nina", "W", "de-CH", 2000),
    ("Alina", "W", "de-CH", 2000), ("Livia", "W", "de-CH", 2000), ("Noemi", "W", "de-CH", 2000),
    ("Ladina", "W", "de-CH", 1990), ("Seraina", "W", "de-CH", 1990), ("Flurina", "W", "de-CH", 2000),
    ("Anja", "W", "de-CH", 1980), ("Karin", "W", "de-CH", 1960), ("Esther", "W", "de-CH", 1950),
    ("Regula", "W", "de-CH", 1960), ("Käthi", "W", "de-CH", 1940), ("Annemarie", "W", "de-CH", 1940),
    ("Bettina", "W", "de-CH", 1970), ("Franziska", "W", "de-CH", 1980), ("Simone", "W", "de-CH", 1970),
    ("Yvonne", "W", "de-CH", 1970), ("Carmen", "W", "de-CH", 1960), ("Priska", "W", "de-CH", 1970),
    ("Marlies", "W", "de-CH", 1950), ("Doris", "W", "de-CH", 1950), ("Irene", "W", "de-CH", 1950),
    ("Sara", "W", "de-CH", 1990), ("Laura", "W", "de-CH", 1990), ("Anna", "W", "de-CH", 2000),
    ("Sophie", "W", "de-CH", 2000), ("Emma", "W", "de-CH", 2000), ("Lena", "W", "de-CH", 2000),
    # de-CH maennlich
    ("Ernst", "M", "de-CH", 1930), ("Hans", "M", "de-CH", 1930), ("Fritz", "M", "de-CH", 1930),
    ("Walter", "M", "de-CH", 1930), ("Werner", "M", "de-CH", 1940), ("Kurt", "M", "de-CH", 1940),
    ("Ruedi", "M", "de-CH", 1940), ("Heinz", "M", "de-CH", 1940), ("Peter", "M", "de-CH", 1950),
    ("Urs", "M", "de-CH", 1950), ("Beat", "M", "de-CH", 1950), ("René", "M", "de-CH", 1950),
    ("Bruno", "M", "de-CH", 1950), ("Markus", "M", "de-CH", 1960), ("Thomas", "M", "de-CH", 1960),
    ("Daniel", "M", "de-CH", 1960), ("Christoph", "M", "de-CH", 1960), ("Andreas", "M", "de-CH", 1960),
    ("Stefan", "M", "de-CH", 1970), ("Michael", "M", "de-CH", 1970), ("Patrick", "M", "de-CH", 1970),
    ("Reto", "M", "de-CH", 1970), ("Adrian", "M", "de-CH", 1970), ("Marcel", "M", "de-CH", 1970),
    ("Roger", "M", "de-CH", 1970), ("Pascal", "M", "de-CH", 1980), ("Fabian", "M", "de-CH", 1980),
    ("Sandro", "M", "de-CH", 1980), ("Simon", "M", "de-CH", 1980), ("Lukas", "M", "de-CH", 1990),
    ("Jonas", "M", "de-CH", 1990), ("Luca", "M", "de-CH", 1990), ("Nico", "M", "de-CH", 1990),
    ("Joel", "M", "de-CH", 1990), ("Noah", "M", "de-CH", 2000), ("Leon", "M", "de-CH", 2000),
    ("Elias", "M", "de-CH", 2000), ("Levin", "M", "de-CH", 2000), ("Nils", "M", "de-CH", 2000),
    ("Gian", "M", "de-CH", 1990), ("Flurin", "M", "de-CH", 2000), ("Silvan", "M", "de-CH", 1990),
    ("Roman", "M", "de-CH", 1980), ("Martin", "M", "de-CH", 1960), ("Ueli", "M", "de-CH", 1950),
    ("Köbi", "M", "de-CH", 1940), ("Sepp", "M", "de-CH", 1940), ("Hansruedi", "M", "de-CH", 1940),
    ("Christian", "M", "de-CH", 1970), ("Matthias", "M", "de-CH", 1970), ("Tobias", "M", "de-CH", 1980),
    ("Philipp", "M", "de-CH", 1980), ("Dominik", "M", "de-CH", 1980), ("Raphael", "M", "de-CH", 1980),
    ("Manuel", "M", "de-CH", 1980), ("Samuel", "M", "de-CH", 1990), ("David", "M", "de-CH", 1990),
    ("Jan", "M", "de-CH", 1990), ("Tim", "M", "de-CH", 2000), ("Ben", "M", "de-CH", 2000),
    ("Rolf", "M", "de-CH", 1950), ("Jürg", "M", "de-CH", 1950), ("Hanspeter", "M", "de-CH", 1950),
    ("Felix", "M", "de-CH", 1990), ("Cyrill", "M", "de-CH", 1990), ("Yannick", "M", "de-CH", 1990),
    # de-DE weiblich
    ("Erna", "W", "de-DE", 1930), ("Hildegard", "W", "de-DE", 1930), ("Irmgard", "W", "de-DE", 1930),
    ("Gerda", "W", "de-DE", 1930), ("Ingrid", "W", "de-DE", 1940), ("Helga", "W", "de-DE", 1940),
    ("Gisela", "W", "de-DE", 1940), ("Renate", "W", "de-DE", 1940), ("Ursula", "W", "de-DE", 1940),
    ("Christa", "W", "de-DE", 1940), ("Karin", "W", "de-DE", 1950), ("Monika", "W", "de-DE", 1950),
    ("Brigitte", "W", "de-DE", 1950), ("Gabriele", "W", "de-DE", 1950), ("Angelika", "W", "de-DE", 1950),
    ("Sabine", "W", "de-DE", 1960), ("Petra", "W", "de-DE", 1960), ("Susanne", "W", "de-DE", 1960),
    ("Birgit", "W", "de-DE", 1960), ("Martina", "W", "de-DE", 1960), ("Andrea", "W", "de-DE", 1960),
    ("Stefanie", "W", "de-DE", 1970), ("Nicole", "W", "de-DE", 1970), ("Tanja", "W", "de-DE", 1970),
    ("Katrin", "W", "de-DE", 1970), ("Anke", "W", "de-DE", 1970), ("Silke", "W", "de-DE", 1970),
    ("Julia", "W", "de-DE", 1980), ("Katharina", "W", "de-DE", 1980), ("Christina", "W", "de-DE", 1980),
    ("Jennifer", "W", "de-DE", 1980), ("Sarah", "W", "de-DE", 1980), ("Nadine", "W", "de-DE", 1980),
    ("Lisa", "W", "de-DE", 1990), ("Laura", "W", "de-DE", 1990), ("Vanessa", "W", "de-DE", 1990),
    ("Jessica", "W", "de-DE", 1990), ("Franziska", "W", "de-DE", 1990), ("Hanna", "W", "de-DE", 2000),
    ("Leonie", "W", "de-DE", 2000), ("Marie", "W", "de-DE", 2000), ("Sophia", "W", "de-DE", 2000),
    ("Emilia", "W", "de-DE", 2000), ("Lina", "W", "de-DE", 2000), ("Mia", "W", "de-DE", 2000),
    ("Johanna", "W", "de-DE", 2000), ("Charlotte", "W", "de-DE", 2000), ("Greta", "W", "de-DE", 2000),
    ("Heike", "W", "de-DE", 1960), ("Kerstin", "W", "de-DE", 1970), ("Manuela", "W", "de-DE", 1970),
    ("Anja", "W", "de-DE", 1970), ("Melanie", "W", "de-DE", 1980), ("Jana", "W", "de-DE", 1980),
    ("Annika", "W", "de-DE", 1990), ("Maren", "W", "de-DE", 1980), ("Svenja", "W", "de-DE", 1990),
    ("Elke", "W", "de-DE", 1950), ("Hannelore", "W", "de-DE", 1940), ("Waltraud", "W", "de-DE", 1930),
    ("Cornelia", "W", "de-DE", 1960), ("Ute", "W", "de-DE", 1950), ("Dagmar", "W", "de-DE", 1950),
    # de-DE maennlich
    ("Wilhelm", "M", "de-DE", 1930), ("Heinrich", "M", "de-DE", 1930), ("Karl", "M", "de-DE", 1930),
    ("Günter", "M", "de-DE", 1930), ("Horst", "M", "de-DE", 1940), ("Klaus", "M", "de-DE", 1940),
    ("Dieter", "M", "de-DE", 1940), ("Manfred", "M", "de-DE", 1940), ("Wolfgang", "M", "de-DE", 1940),
    ("Jürgen", "M", "de-DE", 1950), ("Uwe", "M", "de-DE", 1950), ("Bernd", "M", "de-DE", 1950),
    ("Rainer", "M", "de-DE", 1950), ("Norbert", "M", "de-DE", 1950), ("Frank", "M", "de-DE", 1960),
    ("Michael", "M", "de-DE", 1960), ("Thomas", "M", "de-DE", 1960), ("Andreas", "M", "de-DE", 1960),
    ("Stefan", "M", "de-DE", 1960), ("Jörg", "M", "de-DE", 1960), ("Torsten", "M", "de-DE", 1960),
    ("Christian", "M", "de-DE", 1970), ("Markus", "M", "de-DE", 1970), ("Sven", "M", "de-DE", 1970),
    ("Dirk", "M", "de-DE", 1970), ("Oliver", "M", "de-DE", 1970), ("Marco", "M", "de-DE", 1970),
    ("Sebastian", "M", "de-DE", 1980), ("Daniel", "M", "de-DE", 1980), ("Jan", "M", "de-DE", 1980),
    ("Florian", "M", "de-DE", 1980), ("Tobias", "M", "de-DE", 1980), ("Dennis", "M", "de-DE", 1980),
    ("Kevin", "M", "de-DE", 1990), ("Tim", "M", "de-DE", 1990), ("Jonas", "M", "de-DE", 1990),
    ("Maximilian", "M", "de-DE", 1990), ("Niklas", "M", "de-DE", 1990), ("Lukas", "M", "de-DE", 1990),
    ("Finn", "M", "de-DE", 2000), ("Leon", "M", "de-DE", 2000), ("Paul", "M", "de-DE", 2000),
    ("Elias", "M", "de-DE", 2000), ("Noah", "M", "de-DE", 2000), ("Ben", "M", "de-DE", 2000),
    ("Luis", "M", "de-DE", 2000), ("Henry", "M", "de-DE", 2000), ("Emil", "M", "de-DE", 2000),
    ("Matthias", "M", "de-DE", 1970), ("Holger", "M", "de-DE", 1960), ("Ralf", "M", "de-DE", 1960),
    ("Carsten", "M", "de-DE", 1960), ("Björn", "M", "de-DE", 1970), ("Lars", "M", "de-DE", 1970),
    ("Philipp", "M", "de-DE", 1980), ("Moritz", "M", "de-DE", 1990), ("Felix", "M", "de-DE", 1990),
    ("Hans-Jürgen", "M", "de-DE", 1940), ("Karl-Heinz", "M", "de-DE", 1940), ("Gerhard", "M", "de-DE", 1940),
    ("Helmut", "M", "de-DE", 1930), ("Reinhard", "M", "de-DE", 1950), ("Volker", "M", "de-DE", 1950),
    # fr
    ("Marie", "W", "fr", 1940), ("Jeanne", "W", "fr", 1930), ("Madeleine", "W", "fr", 1930),
    ("Monique", "W", "fr", 1940), ("Françoise", "W", "fr", 1940), ("Nicole", "W", "fr", 1950),
    ("Christiane", "W", "fr", 1950), ("Josiane", "W", "fr", 1950), ("Chantal", "W", "fr", 1950),
    ("Sylvie", "W", "fr", 1960), ("Catherine", "W", "fr", 1960), ("Isabelle", "W", "fr", 1960),
    ("Valérie", "W", "fr", 1960), ("Nathalie", "W", "fr", 1970), ("Sandrine", "W", "fr", 1970),
    ("Céline", "W", "fr", 1970), ("Stéphanie", "W", "fr", 1970), ("Aurélie", "W", "fr", 1980),
    ("Émilie", "W", "fr", 1980), ("Élodie", "W", "fr", 1980), ("Julie", "W", "fr", 1980),
    ("Camille", "W", "fr", 1990), ("Manon", "W", "fr", 1990), ("Léa", "W", "fr", 1990),
    ("Chloé", "W", "fr", 1990), ("Océane", "W", "fr", 1990), ("Emma", "W", "fr", 2000),
    ("Louise", "W", "fr", 2000), ("Zoé", "W", "fr", 2000), ("Jade", "W", "fr", 2000),
    ("Inès", "W", "fr", 2000), ("Alice", "W", "fr", 2000), ("Lucie", "W", "fr", 1990),
    ("Anne", "W", "fr", 1950), ("Martine", "W", "fr", 1950), ("Dominique", "U", "fr", 1950),
    ("Claude", "U", "fr", 1940), ("Jean", "M", "fr", 1930), ("Pierre", "M", "fr", 1940),
    ("André", "M", "fr", 1930), ("Michel", "M", "fr", 1940), ("Bernard", "M", "fr", 1940),
    ("Jacques", "M", "fr", 1940), ("Alain", "M", "fr", 1950), ("Philippe", "M", "fr", 1950),
    ("Gérard", "M", "fr", 1940), ("Daniel", "M", "fr", 1950), ("Patrick", "M", "fr", 1960),
    ("Christophe", "M", "fr", 1960), ("Laurent", "M", "fr", 1960), ("Olivier", "M", "fr", 1960),
    ("Pascal", "M", "fr", 1960), ("Frédéric", "M", "fr", 1970), ("Sébastien", "M", "fr", 1970),
    ("Nicolas", "M", "fr", 1970), ("Julien", "M", "fr", 1980), ("Cédric", "M", "fr", 1970),
    ("Guillaume", "M", "fr", 1980), ("Jérôme", "M", "fr", 1970), ("Mathieu", "M", "fr", 1980),
    ("Antoine", "M", "fr", 1990), ("Maxime", "M", "fr", 1990), ("Thomas", "M", "fr", 1990),
    ("Alexandre", "M", "fr", 1990), ("Hugo", "M", "fr", 2000), ("Louis", "M", "fr", 2000),
    ("Gabriel", "M", "fr", 2000), ("Nathan", "M", "fr", 2000), ("Arthur", "M", "fr", 2000),
    ("Théo", "M", "fr", 2000), ("Loïc", "M", "fr", 1980), ("Yann", "M", "fr", 1980),
    # it
    ("Maria", "W", "it", 1930), ("Rosa", "W", "it", 1930), ("Anna", "W", "it", 1940),
    ("Giuseppina", "W", "it", 1930), ("Carla", "W", "it", 1940), ("Franca", "W", "it", 1940),
    ("Luisa", "W", "it", 1950), ("Gabriella", "W", "it", 1950), ("Patrizia", "W", "it", 1960),
    ("Daniela", "W", "it", 1960), ("Paola", "W", "it", 1960), ("Laura", "W", "it", 1960),
    ("Cristina", "W", "it", 1970), ("Monica", "W", "it", 1970), ("Simona", "W", "it", 1970),
    ("Elisa", "W", "it", 1980), ("Chiara", "W", "it", 1980), ("Valentina", "W", "it", 1980),
    ("Silvia", "W", "it", 1980), ("Giulia", "W", "it", 1990), ("Martina", "W", "it", 1990),
    ("Alessia", "W", "it", 1990), ("Sara", "W", "it", 1990), ("Sofia", "W", "it", 2000),
    ("Aurora", "W", "it", 2000), ("Giorgia", "W", "it", 2000), ("Alice", "W", "it", 2000),
    ("Emma", "W", "it", 2000), ("Greta", "W", "it", 2000), ("Beatrice", "W", "it", 2000),
    ("Giovanni", "M", "it", 1930), ("Giuseppe", "M", "it", 1930), ("Mario", "M", "it", 1940),
    ("Luigi", "M", "it", 1940), ("Franco", "M", "it", 1940), ("Pietro", "M", "it", 1940),
    ("Roberto", "M", "it", 1950), ("Paolo", "M", "it", 1950), ("Claudio", "M", "it", 1950),
    ("Marco", "M", "it", 1960), ("Stefano", "M", "it", 1960), ("Massimo", "M", "it", 1960),
    ("Fabio", "M", "it", 1970), ("Andrea", "M", "it", 1970), ("Luca", "M", "it", 1970),
    ("Alessandro", "M", "it", 1980), ("Matteo", "M", "it", 1980), ("Davide", "M", "it", 1980),
    ("Simone", "M", "it", 1980), ("Francesco", "M", "it", 1990), ("Lorenzo", "M", "it", 1990),
    ("Riccardo", "M", "it", 1990), ("Gabriele", "M", "it", 1990), ("Leonardo", "M", "it", 2000),
    ("Tommaso", "M", "it", 2000), ("Mattia", "M", "it", 2000), ("Edoardo", "M", "it", 2000),
    ("Dario", "M", "it", 1970), ("Nicola", "M", "it", 1980), ("Michele", "M", "it", 1970),
    # international (Migrationshintergrund, beide Laender)
    ("Fatma", "W", "international", 1960), ("Ayşe", "W", "international", 1970), ("Elif", "W", "international", 1990),
    ("Zeynep", "W", "international", 2000), ("Aylin", "W", "international", 1990), ("Meryem", "W", "international", 1980),
    ("Ana", "W", "international", 1970), ("Maria José", "W", "international", 1960), ("Carla", "W", "international", 1980),
    ("Ivana", "W", "international", 1970), ("Dragana", "W", "international", 1970), ("Jelena", "W", "international", 1980),
    ("Milica", "W", "international", 1990), ("Vesna", "W", "international", 1960), ("Amira", "W", "international", 1990),
    ("Leila", "W", "international", 1990), ("Priya", "W", "international", 1990), ("Olga", "W", "international", 1970),
    ("Svetlana", "W", "international", 1970), ("Katarzyna", "W", "international", 1980), ("Agnieszka", "W", "international", 1980),
    ("Eleni", "W", "international", 1970), ("Sofia", "W", "international", 2000), ("Aisha", "W", "international", 2000),
    ("Mehmet", "M", "international", 1960), ("Mustafa", "M", "international", 1970), ("Emre", "M", "international", 1990),
    ("Can", "M", "international", 2000), ("Murat", "M", "international", 1970), ("Ali", "M", "international", 1980),
    ("José", "M", "international", 1960), ("Carlos", "M", "international", 1970), ("Miguel", "M", "international", 1980),
    ("Dragan", "M", "international", 1960), ("Goran", "M", "international", 1970), ("Milan", "M", "international", 1980),
    ("Nikola", "M", "international", 1990), ("Luka", "M", "international", 2000), ("Amir", "M", "international", 1990),
    ("Omar", "M", "international", 1990), ("Rajesh", "M", "international", 1980), ("Igor", "M", "international", 1970),
    ("Piotr", "M", "international", 1980), ("Tomasz", "M", "international", 1980), ("Dimitrios", "M", "international", 1960),
    ("Yannis", "M", "international", 1980), ("Samuel", "M", "international", 2000), ("Adam", "M", "international", 2000),
]

# ---------------------------------------------------------------------------------------------
# Nachnamen: (name, sprachraum, gewicht)
# ---------------------------------------------------------------------------------------------
NACHNAMEN_DE_CH = [
    ("Müller", 100), ("Meier", 80), ("Schmid", 75), ("Keller", 70), ("Weber", 65), ("Huber", 60),
    ("Schneider", 55), ("Meyer", 55), ("Steiner", 50), ("Fischer", 50), ("Gerber", 45), ("Brunner", 45),
    ("Baumann", 40), ("Frei", 40), ("Zimmermann", 40), ("Moser", 38), ("Widmer", 38), ("Wyss", 36),
    ("Graf", 35), ("Roth", 35), ("Suter", 34), ("Bühler", 32), ("Berger", 32), ("Kaufmann", 30),
    ("Hofer", 30), ("Lüthi", 28), ("Koch", 28), ("Bachmann", 27), ("Zürcher", 26), ("Gasser", 26),
    ("Egli", 25), ("Kunz", 25), ("Hess", 24), ("Bieri", 24), ("Christen", 23), ("Marti", 23),
    ("Wenger", 22), ("Studer", 22), ("Stalder", 22), ("Ammann", 21), ("Lehmann", 21), ("Aebi", 20),
    ("Bader", 20), ("Bürgi", 20), ("Flückiger", 20), ("Frey", 20), ("Furrer", 19), ("Gloor", 19),
    ("Haas", 19), ("Hauser", 19), ("Hunziker", 18), ("Imhof", 18), ("Jenni", 18), ("Kälin", 18),
    ("Kohler", 18), ("Kuhn", 17), ("Leuenberger", 17), ("Locher", 17), ("Maurer", 17), ("Nussbaumer", 16),
    ("Odermatt", 16), ("Peter", 16), ("Pfister", 16), ("Rüegg", 16), ("Rohrer", 15), ("Sägesser", 15),
    ("Schärer", 15), ("Schwab", 15), ("Senn", 15), ("Sigrist", 15), ("Spörri", 14), ("Stadler", 14),
    ("Stoll", 14), ("Tanner", 14), ("Thommen", 14), ("Tschudi", 14), ("Vogel", 14), ("Vogt", 14),
    ("Von Arx", 13), ("Wagner", 13), ("Walder", 13), ("Wüthrich", 13), ("Zaugg", 13), ("Zbinden", 13),
    ("Zehnder", 12), ("Ziegler", 12), ("Zumstein", 12), ("Amstutz", 12), ("Arnold", 12), ("Bättig", 12),
    ("Bolliger", 12), ("Bossard", 12), ("Bucher", 12), ("Burkhalter", 11), ("Dietiker", 11), ("Eggenberger", 11),
    ("Eichenberger", 11), ("Emmenegger", 11), ("Fankhauser", 11), ("Fuchs", 11), ("Gehrig", 11), ("Gfeller", 11),
    ("Gisler", 11), ("Grob", 10), ("Gubler", 10), ("Hänni", 10), ("Härdi", 10), ("Hauenstein", 10),
    ("Heiniger", 10), ("Hirt", 10), ("Hürlimann", 10), ("Iten", 10), ("Jäggi", 10), ("Jost", 10),
    ("Kessler", 10), ("Kissling", 10), ("Krebs", 10), ("Kühni", 9), ("Lang", 9), ("Läubli", 9),
    ("Liechti", 9), ("Lienhard", 9), ("Marbach", 9), ("Mathys", 9), ("Merz", 9), ("Mettler", 9),
    ("Michel", 9), ("Niederberger", 9), ("Oberholzer", 9), ("Portmann", 9), ("Probst", 9), ("Reber", 9),
    ("Rickli", 9), ("Rudolf", 8), ("Rüfenacht", 8), ("Ryser", 8), ("Schaffner", 8), ("Scherrer", 8),
    ("Schläfli", 8), ("Schüpbach", 8), ("Sommer", 8), ("Spahr", 8), ("Stäheli", 8), ("Staub", 8),
    ("Stucki", 8), ("Sutter", 8), ("Trachsel", 8), ("Ulrich", 8), ("Vetterli", 8), ("Waser", 8),
    ("Wehrli", 8), ("Wild", 8), ("Winkler", 8), ("Wirz", 8), ("Wittwer", 8), ("Wolf", 8),
    ("Zingg", 7), ("Zollinger", 7), ("Zwahlen", 7), ("Amrein", 7), ("Bächtold", 7), ("Balmer", 7),
    ("Bättig", 7), ("Bertschi", 7), ("Blaser", 7), ("Bösch", 7), ("Brägger", 7), ("Bruderer", 7),
]
NACHNAMEN_DE_DE = [
    ("Müller", 100), ("Schmidt", 95), ("Schneider", 80), ("Fischer", 75), ("Weber", 70), ("Meyer", 68),
    ("Wagner", 65), ("Becker", 62), ("Schulz", 60), ("Hoffmann", 58), ("Schäfer", 55), ("Koch", 54),
    ("Bauer", 52), ("Richter", 50), ("Klein", 50), ("Wolf", 48), ("Schröder", 47), ("Neumann", 46),
    ("Schwarz", 45), ("Zimmermann", 44), ("Braun", 43), ("Krüger", 42), ("Hofmann", 41), ("Hartmann", 40),
    ("Lange", 40), ("Schmitt", 39), ("Werner", 38), ("Schmitz", 37), ("Krause", 36), ("Meier", 36),
    ("Lehmann", 35), ("Schmid", 34), ("Schulze", 34), ("Maier", 33), ("Köhler", 33), ("Herrmann", 32),
    ("König", 32), ("Walter", 31), ("Mayer", 31), ("Huber", 30), ("Kaiser", 30), ("Fuchs", 29),
    ("Peters", 29), ("Lang", 28), ("Scholz", 28), ("Möller", 27), ("Weiß", 27), ("Jung", 26),
    ("Hahn", 26), ("Schubert", 25), ("Vogel", 25), ("Friedrich", 25), ("Keller", 24), ("Günther", 24),
    ("Frank", 24), ("Berger", 23), ("Winkler", 23), ("Roth", 23), ("Beck", 22), ("Lorenz", 22),
    ("Baumann", 22), ("Franke", 21), ("Albrecht", 21), ("Schuster", 21), ("Simon", 20), ("Ludwig", 20),
    ("Böhm", 20), ("Winter", 20), ("Kraus", 19), ("Martin", 19), ("Schumacher", 19), ("Krämer", 19),
    ("Vogt", 18), ("Stein", 18), ("Jäger", 18), ("Otto", 18), ("Sommer", 18), ("Groß", 17),
    ("Seidel", 17), ("Heinrich", 17), ("Brandt", 17), ("Haas", 17), ("Schreiber", 16), ("Graf", 16),
    ("Schulte", 16), ("Dietrich", 16), ("Ziegler", 16), ("Kuhn", 16), ("Kühn", 15), ("Pohl", 15),
    ("Engel", 15), ("Horn", 15), ("Busch", 15), ("Bergmann", 15), ("Thomas", 14), ("Voigt", 14),
    ("Sauer", 14), ("Arnold", 14), ("Wolff", 14), ("Pfeiffer", 14), ("Ortlepp", 5), ("Steinbrecher", 6),
    ("Vollmer", 8), ("Lindqvist", 2), ("Brandt", 10), ("Kolbe", 8), ("Nowak", 12), ("Kowalski", 10),
    ("Wieczorek", 6), ("Janssen", 10), ("Hansen", 12), ("Petersen", 12), ("Jensen", 8), ("Carstensen", 5),
    ("Lüders", 6), ("Behrens", 8), ("Reimers", 6), ("Wessel", 6), ("Bosch", 7), ("Ebner", 7),
    ("Gruber", 8), ("Hofer", 6), ("Kern", 8), ("Kurz", 7), ("Löffler", 6), ("Merkel", 4),
    ("Neubauer", 8), ("Oswald", 6), ("Pichler", 5), ("Reinhardt", 7), ("Sattler", 6), ("Strobel", 6),
    ("Thiel", 8), ("Ullrich", 7), ("Vetter", 6), ("Wendt", 7), ("Wilhelm", 7), ("Zander", 6),
    ("Adler", 6), ("Bachmann", 6), ("Brinkmann", 7), ("Dörr", 5), ("Eckert", 7), ("Fiedler", 7),
    ("Geiger", 7), ("Haase", 7), ("Hübner", 7), ("Jahn", 6), ("Kastner", 5), ("Lindner", 8),
    ("Marx", 6), ("Nagel", 7), ("Ostermann", 4), ("Pape", 5), ("Rauch", 6), ("Sperling", 4),
    ("Tröger", 3), ("Unger", 6), ("Voss", 7), ("Wegner", 7), ("Zeller", 5), ("Ahrens", 6),
    ("Bock", 6), ("Cordes", 4), ("Dittrich", 5), ("Ernst", 7), ("Feldmann", 5), ("Gerlach", 6),
    ("Heller", 6), ("Ilgner", 2), ("Jacobs", 6), ("Kessler", 6), ("Lutz", 7), ("Menzel", 6),
    ("Naumann", 6), ("Opitz", 5), ("Preuß", 5), ("Rudolph", 6), ("Stark", 6), ("Timm", 5),
]
NACHNAMEN_FR = [
    ("Favre", 40), ("Rochat", 35), ("Bovet", 30), ("Chappuis", 28), ("Cornu", 26), ("Dubois", 26),
    ("Gilliéron", 22), ("Martin", 30), ("Mermoud", 20), ("Monnier", 22), ("Pittet", 22), ("Rey", 20),
    ("Rossier", 20), ("Bugnon", 18), ("Cuendet", 16), ("Dupraz", 16), ("Gaillard", 18), ("Golay", 16),
    ("Jaquet", 16), ("Mottier", 14), ("Nicolet", 14), ("Perrin", 16), ("Reymond", 16), ("Vuilleumier", 14),
    ("Bourquin", 14), ("Droz", 14), ("Ducommun", 12), ("Huguenin", 12), ("Jeanneret", 12), ("Matthey", 12),
    ("Perret", 12), ("Robert", 14), ("Sandoz", 12), ("Vuille", 10), ("Berthoud", 10), ("Blanc", 14),
    ("Bonvin", 12), ("Bruchez", 10), ("Crettaz", 10), ("Fournier", 12), ("Gay", 10), ("Moret", 10),
    ("Roduit", 8), ("Zufferey", 10), ("Aubert", 10), ("Barbey", 8), ("Bertholet", 8), ("Chevalley", 8),
    ("Décosterd", 6), ("Delacrétaz", 6), ("Desponds", 6), ("Fontannaz", 6), ("Gonin", 6), ("Grandjean", 8),
    ("Henchoz", 6), ("Jordan", 8), ("Lambert", 8), ("Maillard", 8), ("Meylan", 8), ("Michaud", 8),
    ("Morel", 8), ("Paccaud", 6), ("Pasche", 6), ("Piguet", 8), ("Rouiller", 6), ("Savary", 6),
    ("Tissot", 8), ("Vallotton", 6), ("Vonlanthen", 6), ("Wicht", 6), ("Bays", 5), ("Chardonnens", 5),
    ("Dénervaud", 4), ("Ecoffey", 4), ("Gremaud", 6), ("Jungo", 5), ("Kolly", 5), ("Pasquier", 6),
    ("Repond", 5), ("Sudan", 5), ("Terrapon", 4), ("Vial", 5), ("Willemin", 4), ("Fleury", 5),
    ("Chételat", 4), ("Comte", 5), ("Frésard", 4), ("Membrez", 4), ("Prêtre", 4), ("Voisard", 4),
]
NACHNAMEN_IT = [
    ("Bernasconi", 30), ("Rossi", 28), ("Bianchi", 26), ("Ferrari", 22), ("Galli", 20), ("Colombo", 18),
    ("Fontana", 18), ("Rezzonico", 14), ("Pedrazzini", 14), ("Ghiringhelli", 12), ("Pellegrini", 14),
    ("Lombardi", 14), ("Rusca", 10), ("Soldati", 10), ("Genazzi", 8), ("Casanova", 10), ("Cattaneo", 12),
    ("Beretta", 10), ("Bottani", 8), ("Cereghetti", 8), ("Croci", 8), ("Delcò", 6), ("Gianella", 8),
    ("Giudici", 8), ("Guidotti", 6), ("Lurati", 6), ("Maggi", 8), ("Mombelli", 6), ("Morisoli", 6),
    ("Pini", 8), ("Quadri", 6), ("Riva", 8), ("Rossetti", 6), ("Sassi", 6), ("Solari", 6),
    ("Tettamanti", 6), ("Togni", 6), ("Vanini", 6), ("Zanetti", 8), ("Zappa", 6), ("Bassi", 6),
    ("Bruni", 6), ("Cavalli", 6), ("De Marchi", 6), ("Esposito", 8), ("Greco", 8), ("Marino", 8),
    ("Moretti", 8), ("Ricci", 8), ("Romano", 8), ("Russo", 8), ("Santoro", 6), ("Vitale", 6),
    ("Conti", 8), ("Costa", 8), ("Ferrara", 6), ("Gallo", 8), ("Leone", 6), ("Mancini", 6),
    ("Marchetti", 6), ("Martini", 6), ("Parisi", 5), ("Rinaldi", 6), ("Serra", 5), ("Villa", 6),
]
NACHNAMEN_INT = [
    ("Yilmaz", 20), ("Kaya", 14), ("Demir", 14), ("Şahin", 12), ("Çelik", 12), ("Öztürk", 12),
    ("Demirci", 8), ("Aydın", 10), ("Arslan", 10), ("Doğan", 8), ("Da Silva", 12), ("Dos Santos", 10),
    ("Pereira", 8), ("Oliveira", 8), ("Fernandes", 8), ("García", 10), ("Rodríguez", 8), ("López", 8),
    ("Martínez", 8), ("Petrović", 10), ("Jovanović", 10), ("Nikolić", 8), ("Marković", 8), ("Đorđević", 6),
    ("Kovačević", 8), ("Horvat", 8), ("Novak", 8), ("Krasniqi", 8), ("Gashi", 6), ("Berisha", 6),
    ("Shala", 5), ("Hoxha", 5), ("Nowak", 8), ("Kowalczyk", 6), ("Wiśniewski", 6), ("Zieliński", 5),
    ("Papadopoulos", 6), ("Georgiou", 4), ("Ivanov", 6), ("Petrov", 5), ("Smirnova", 4), ("Kuznetsov", 4),
    ("Haddad", 6), ("Khalil", 5), ("Mansour", 5), ("Hassan", 6), ("Ahmed", 6), ("Hussain", 5),
    ("Patel", 8), ("Sharma", 6), ("Singh", 6), ("Nguyen", 8), ("Tran", 5), ("Chen", 6), ("Wang", 6),
    ("Kim", 5), ("Mbatha", 3), ("Okafor", 3), ("Mensah", 3), ("Diallo", 3), ("Silva", 6),
]

# ---------------------------------------------------------------------------------------------
# Firmennamen-Bausteine
# ---------------------------------------------------------------------------------------------
FIRMEN_STAEMME_CH = ["Aare", "Jura", "Alpina", "Mittelland", "Säntis", "Rigi", "Pilatus", "Napf", "Emme",
                     "Limmat", "Reuss", "Thur", "Töss", "Sihl", "Gotthard", "Bernina", "Léman", "Ticino",
                     "Helvetia-Nord", "Weissenstein", "Born", "Engelberg", "Hasli", "Simme", "Rhone", "Glatt",
                     "Furka", "Albula", "Uetli", "Bantiger", "Belchen", "Passwang", "Wasserfallen", "Grenchenberg",
                     "Olten-Süd", "Solothurn-West", "Dünnern", "Wigger", "Suhre", "Bünz"]
FIRMEN_STAEMME_DE = ["Rhein", "Main", "Neckar", "Isar", "Elbe", "Spree", "Havel", "Weser", "Ems", "Ruhr",
                     "Lippe", "Donau", "Inn", "Lech", "Mosel", "Saar", "Nahe", "Lahn", "Fulda", "Werra",
                     "Leine", "Aller", "Oder", "Neisse", "Saale", "Mulde", "Taunus", "Odenwald", "Spessart",
                     "Harz", "Eifel", "Hunsrück", "Allgäu", "Schwarzwald", "Bergstrasse", "Havelland", "Uckermark",
                     "Vogtland", "Erzgebirge", "Nordlicht", "Hanse", "Alster", "Nordsee", "Ostsee"]
FIRMEN_BRANCHEN = [
    ("Schreinerei", "Handwerk Holz"), ("Zimmerei", "Handwerk Holz"), ("Sanitär", "Handwerk Gebäudetechnik"),
    ("Heizungsbau", "Handwerk Gebäudetechnik"), ("Elektro", "Handwerk Elektro"), ("Malerei", "Handwerk Bau"),
    ("Gipserei", "Handwerk Bau"), ("Dachdeckerei", "Handwerk Bau"), ("Bauunternehmung", "Bau"),
    ("Gartenbau", "Gartenbau"), ("Metallbau", "Metallbau"), ("Mechanik", "Maschinenbau"),
    ("Präzisionstechnik", "Maschinenbau"), ("Transporte", "Transport"), ("Logistik", "Transport"),
    ("Treuhand", "Treuhand"), ("Revisions", "Treuhand"), ("Consulting", "Beratung"), ("Beratung", "Beratung"),
    ("Informatik", "IT"), ("Software", "IT"), ("Digital", "IT"), ("Systems", "IT"), ("Architekten", "Architektur"),
    ("Ingenieure", "Ingenieurwesen"), ("Planung", "Ingenieurwesen"), ("Immobilien", "Immobilien"),
    ("Verwaltungs", "Immobilien"), ("Gastro", "Gastronomie"), ("Bäckerei", "Lebensmittel"), ("Metzgerei", "Lebensmittel"),
    ("Handel", "Handel"), ("Textil", "Handel"), ("Optik", "Handel"), ("Apotheke", "Gesundheit"),
    ("Physiotherapie", "Gesundheit"), ("Pflege", "Gesundheit"), ("Reinigung", "Dienstleistung"),
    ("Sicherheits", "Dienstleistung"), ("Event", "Dienstleistung"), ("Medien", "Medien"), ("Druck", "Medien"),
    ("Fahrschule", "Bildung"), ("Kinderkrippe", "Bildung"), ("Reisen", "Tourismus"), ("Hotel", "Tourismus"),
    ("Carrosserie", "Auto"), ("Garage", "Auto"), ("Autohaus", "Auto"), ("Velo", "Handel"),
]
RECHTSFORMEN = [("AG", "CH"), ("GmbH", "CH"), ("Sàrl", "CH"), ("SA", "CH"), ("Sagl", "CH"), ("KlG", "CH"),
                ("GmbH", "DE"), ("AG", "DE"), ("GmbH & Co. KG", "DE"), ("KG", "DE"), ("e.K.", "DE"), ("UG (haftungsbeschränkt)", "DE")]

# ---------------------------------------------------------------------------------------------
# Blocklist (reale Personen und Firmen, die nie als Kombination erzeugt werden duerfen)
# ---------------------------------------------------------------------------------------------
BLOCK_PERSONEN = [
    # Prominente CH/DE (Auswahl)
    ("Roger", "Federer"), ("Stan", "Wawrinka"), ("Martina", "Hingis"), ("Belinda", "Bencic"), ("Lara", "Gut"),
    ("Beat", "Feuz"), ("Marco", "Odermatt"), ("Simon", "Ammann"), ("Fabian", "Cancellara"), ("Nino", "Schurter"),
    ("Ursula", "Andress"), ("Bruno", "Ganz"), ("Emil", "Steinberger"), ("Beat", "Schlatter"), ("Roger", "Köppel"),
    ("Alain", "Berset"), ("Karin", "Keller-Sutter"), ("Viola", "Amherd"), ("Guy", "Parmelin"), ("Ignazio", "Cassis"),
    ("Elisabeth", "Baume-Schneider"), ("Albert", "Rösti"), ("Beat", "Jans"), ("Simonetta", "Sommaruga"),
    ("Ueli", "Maurer"), ("Doris", "Leuthard"), ("Christoph", "Blocher"), ("Magdalena", "Martullo-Blocher"),
    ("Angela", "Merkel"), ("Olaf", "Scholz"), ("Friedrich", "Merz"), ("Robert", "Habeck"), ("Annalena", "Baerbock"),
    ("Christian", "Lindner"), ("Markus", "Söder"), ("Frank-Walter", "Steinmeier"), ("Gerhard", "Schröder"),
    ("Helmut", "Kohl"), ("Helmut", "Schmidt"), ("Boris", "Becker"), ("Steffi", "Graf"), ("Michael", "Schumacher"),
    ("Sebastian", "Vettel"), ("Manuel", "Neuer"), ("Thomas", "Müller"), ("Toni", "Kroos"), ("Philipp", "Lahm"),
    ("Bastian", "Schweinsteiger"), ("Lukas", "Podolski"), ("Jürgen", "Klopp"), ("Franz", "Beckenbauer"),
    ("Dirk", "Nowitzki"), ("Til", "Schweiger"), ("Heidi", "Klum"), ("Helene", "Fischer"), ("Herbert", "Grönemeyer"),
    ("Udo", "Lindenberg"), ("Nina", "Hagen"), ("Günther", "Jauch"), ("Thomas", "Gottschalk"), ("Stefan", "Raab"),
    ("Anke", "Engelke"), ("Hape", "Kerkeling"), ("Dieter", "Bohlen"), ("Carolin", "Kebekus"), ("Jan", "Böhmermann"),
    # Versicherungsbranche CH/DE (Fuehrungspersonen, Auswahl, Stand des Wissens)
    ("Oliver", "Bäte"), ("Christian", "Mumenthaler"), ("Andreas", "Berger"), ("Mario", "Greco"), ("Patrick", "Frost"),
    ("Philomena", "Colatrella"), ("Michael", "Müller"), ("Thomas", "Buberl"), ("Joachim", "Wenning"),
    ("Markus", "Rieß"), ("Torsten", "Leue"), ("Thomas", "Brahm"), ("Ulrich", "Leitermann"), ("Norbert", "Rollinger"),
    ("Fabian", "Rupprecht"), ("Juan", "Beer"), ("Peter", "Zutter"), ("Michael", "Hengartner"),
    # Reales Medium und dessen KI-Figur (Konventionen §1, Entscheidung E01)
    ("Minzia", "Kolberg"),
]
BLOCK_FIRMEN = [
    "Pfefferminzia Medien", "Pfefferminzia Beteiligungs", "Allianz", "AXA", "Zurich Insurance", "Zürich Versicherung",
    "Swiss Re", "Munich Re", "Münchener Rück", "Helvetia", "Mobiliar", "Baloise", "Bâloise", "Generali", "ERGO",
    "HDI", "Talanx", "Debeka", "Signal Iduna", "R+V", "Swiss Life", "Vaudoise", "Sympany", "Groupe Mutuel",
    "CSS Versicherung", "Visana", "Concordia", "Sanitas", "Helsana", "Assura", "Smile Direct", "Simpego",
    "Emmental Versicherung", "GVB", "Basler Versicherung", "National Versicherung", "Winterthur Versicherung",
    "Huk-Coburg", "Württembergische", "Wüstenrot", "Gothaer", "Nürnberger Versicherung", "Alte Leipziger",
    "Hannover Rück", "Provinzial", "LVM", "VHV", "Barmenia", "Continentale", "Hallesche", "Bayerische Versicherungskammer",
    "Versicherungskammer Bayern", "DEVK", "ADAC Versicherung", "Cosmos Direkt", "Europa Versicherung", "Ottonova",
    "Getsafe", "Wefox", "Clark", "Lemonade", "Ping An", "Prudential", "MetLife", "Aviva", "Chubb", "AIG",
]


# ---------------------------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------------------------
def schreibe(pfad: Path, spalten: list[str], zeilen: list[list]) -> None:
    pfad.parent.mkdir(parents=True, exist_ok=True)
    with pfad.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(spalten)
        w.writerows(zeilen)
    print(f"{pfad.relative_to(ROOT)}: {len(zeilen)} Zeilen")


def dekadengewichte(peak: int) -> list[float]:
    """Glockenkurve um die Peak-Dekade (Sigma 1.5 Dekaden), Werte 0–100, Minimum 1."""
    out = []
    for d in range(1930, 2010, 10):
        x = (d - peak) / 10
        out.append(max(1.0, round(100 * math.exp(-(x * x) / (2 * 1.5**2)), 1)))
    return out


def strassen(staemme: list[str], typen: list[str], sprache: str, verbinder: str = "") -> list[list]:
    zeilen = []
    gesehen: set[str] = set()
    for s in staemme:
        for t in typen:
            if verbinder:
                name = f"{t} {s}"
                typ = t.split()[0]
            else:
                name = f"{s}{t}"
                typ = t.capitalize()
            if name in gesehen:
                continue
            gesehen.add(name)
            zeilen.append([name, sprache, typ, str(name in GENERISCH).lower()])
    return zeilen


VERSICHERUNG_PERSONEN = {("Minzia", "Kolberg")}


def kategorie_person(v: str, n: str) -> str:
    if (v, n) in VERSICHERUNG_PERSONEN:
        return "medium"
    idx = BLOCK_PERSONEN.index((v, n))
    return "versicherung" if idx >= BLOCK_PERSONEN.index(("Oliver", "Bäte")) else "prominenz"


def main() -> None:
    # --- Orte CH ---
    zeilen = []
    for plz, ort, kanton, sprach, ew in ORTE_CH:
        zone = "1" if ort in GROSSSTAEDTE_CH else TARIFZONE_CH_KANTON[kanton]
        gewicht = round(ew * (2.5 if kanton == "SO" else 1.0), 2)  # Region Olten ueberrepraesentiert
        zeilen.append([plz, ort, kanton, sprach, int(ew * 1000), gewicht, zone,
                       urbanitaet(ew, ort, GROSSSTAEDTE_CH)])
    assert 150 <= len(zeilen) <= 320, len(zeilen)
    assert {z[2] for z in zeilen} == set(TARIFZONE_CH_KANTON), "nicht alle Kantone abgedeckt"
    schreibe(GEO / "orte_ch.csv",
             ["plz", "ort", "kanton", "sprachregion", "einwohner", "gewicht", "tarifzone", "urbanitaet"],
             sorted(zeilen, key=lambda z: (z[0], z[1])))

    # --- Orte DE ---
    zeilen = []
    for plz, ort, bl, ew in ORTE_DE:
        zeilen.append([plz, ort, bl, BUNDESLAENDER[bl], int(ew * 1000), round(ew, 2),
                       tarifzone_de(plz, ort, ew), urbanitaet(ew, ort, GROSSSTAEDTE_DE)])
    assert 300 <= len(zeilen) <= 600, len(zeilen)
    assert {z[2] for z in zeilen} == set(BUNDESLAENDER), "nicht alle Bundeslaender abgedeckt"
    assert len({z[0] for z in zeilen}) == len(zeilen), "PLZ doppelt"
    schreibe(GEO / "orte_de.csv",
             ["plz", "ort", "bundesland_kuerzel", "bundesland", "einwohner", "gewicht", "tarifzone",
              "urbanitaet"],
             sorted(zeilen, key=lambda z: z[0]))

    # --- Strassennamen ---
    zeilen = (strassen(STAEMME_DE, TYPEN_DE_CH, "de-CH") + strassen(STAEMME_DE, TYPEN_DE_DE, "de-DE")
              + strassen(STAEMME_FR, TYPEN_FR, "fr", verbinder=" ") + strassen(STAEMME_IT, TYPEN_IT, "it", verbinder=" "))
    for sp in ("de-CH", "de-DE", "fr", "it"):
        n = sum(1 for z in zeilen if z[1] == sp)
        assert n >= 400, (sp, n)
    schreibe(GEO / "strassennamen.csv", ["strasse", "sprache", "typ", "generisch"], zeilen)

    # --- Vornamen ---
    zeilen = []
    gesehen = set()
    for name, g, sr, peak in VORNAMEN:
        if (name, sr) in gesehen:
            continue
        gesehen.add((name, sr))
        zeilen.append([name, g, sr, *dekadengewichte(peak)])
    assert len(zeilen) >= 400, len(zeilen)
    schreibe(NAMEN / "vornamen.csv", ["vorname", "geschlecht", "sprachraum", *[f"g_{d}" for d in range(1930, 2010, 10)]],
             zeilen)

    # --- Nachnamen ---
    zeilen = []
    gesehen = set()
    for liste, sr in ((NACHNAMEN_DE_CH, "de-CH"), (NACHNAMEN_DE_DE, "de-DE"), (NACHNAMEN_FR, "fr"),
                      (NACHNAMEN_IT, "it"), (NACHNAMEN_INT, "international")):
        for name, gew in liste:
            if (name, sr) in gesehen:
                continue
            gesehen.add((name, sr))
            zeilen.append([name, sr, gew, "false"])
    assert len(zeilen) >= 500, len(zeilen)
    schreibe(NAMEN / "nachnamen.csv", ["nachname", "sprachraum", "gewicht", "synthetisch"], zeilen)

    # --- Firmennamen-Bausteine ---
    zeilen = [["stamm", s, "CH", ""] for s in FIRMEN_STAEMME_CH] + [["stamm", s, "DE", ""] for s in FIRMEN_STAEMME_DE]
    zeilen += [["branche", b, "", br] for b, br in FIRMEN_BRANCHEN]
    zeilen += [["rechtsform", rf, land, ""] for rf, land in RECHTSFORMEN]
    schreibe(NAMEN / "firmennamen_bausteine.csv", ["art", "wert", "land", "branche"], zeilen)

    # --- Blocklist ---
    zeilen = [["person", v, n, "", kategorie_person(v, n)] for v, n in BLOCK_PERSONEN]
    zeilen += [["firma", "", "", f, "medium" if "Pfefferminzia" in f else "versicherer"] for f in BLOCK_FIRMEN]
    schreibe(NAMEN / "blocklist.csv", ["typ", "vorname", "nachname", "name", "kategorie"], zeilen)


if __name__ == "__main__":
    main()
