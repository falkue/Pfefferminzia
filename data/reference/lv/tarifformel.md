# Tarifformel Leben

Die Parameter stehen in `tarifparameter.yaml`, Rechnungszins und Tafelzuordnung je Generation in `tarifgenerationen.csv`, die Sterbewahrscheinlichkeiten in `sterbetafel.csv`. Die Kalkulation ist bewusst vereinfacht, damit Seminarteilnehmer sie in Excel nachvollziehen können. Sie ersetzt keine aktuarielle Tarifierung.

## Grundstruktur

```
Risikoprämie   = Risikosumme × qx(Tafel, mittleres Alter) × Raucherfaktor × weitere Risikofaktoren
Sparprämie     = Erlebensfallsumme × i / ((1 + i)^n − 1)          nur Vorsorge und Rente, i = Rechnungszins
Kostenanteil   = alpha‰ × Summe / 1000 / Laufzeit × Summenrabatt + Stückkosten
Nettoprämie    = Risikoprämie + Sparprämie + Kostenanteil
Tarifprämie    = Nettoprämie / (1 − beta)                          beta = Verwaltungskosten in Prozent
Zahlprämie     = Tarifprämie × (1 − Risikoüberschuss)              nur Risikoleben (Beitragsverrechnung)
Zahlweise      = Zahlprämie × (1 + Zuschlag) / Anzahl Raten
```

**Mittleres Alter** = Eintrittsalter + Laufzeit / 2, gerundet. Die Sterbewahrscheinlichkeit wird aus `sterbetafel.csv` gelesen: Spalte `qx_m` oder `qx_w` bei geschlechtsabhängiger Kalkulation, `qx_unisex` bei Unisex (DE ab 21. Dezember 2012, Minzia immer). Bei fallender Summe wird die Risikosumme mit dem Faktor aus `summenverlauf_faktor` multipliziert.

**Risikosumme** bei Vorsorge = Todesfallsumme minus Deckungskapital zur Laufzeitmitte, vereinfacht: Todesfallsumme × (1 − ((1 + i)^(n/2) − 1) / ((1 + i)^n − 1)).

## Beispiel 1: RisikoLeben Schweiz, Generation PZ-2025

Mann, 35 Jahre, Nichtraucher, Berufsgruppe 1, Summe CHF 500'000 konstant, Laufzeit 20 Jahre, jährliche Zahlung.

| Schritt | Rechnung | Wert |
|---|---|---|
| Mittleres Alter | 35 + 20 / 2 | 45 |
| qx Tafel T2020, Mann, Alter 45 | aus sterbetafel.csv | 0.001546 |
| Risikoprämie | 500'000 × 0.001546 × 1.00 | 773.00 |
| Abschlusskosten alpha PZ-2025 | 20 ‰ × 500'000 / 1000 / 20 | 500.00 |
| Summenrabatt ab 500'000 | × 0.94 | 470.00 |
| Stückkosten CH | | 36.00 |
| Nettoprämie | 773.00 + 470.00 + 36.00 | 1'279.00 |
| Tarifprämie | 1'279.00 / (1 − 0.035) | 1'325.39 → 1'325.40 |
| Risikoüberschuss CH 2025 (ueberschuss_parameter.csv) | 25 % Prämienrabatt | |
| **Zahlprämie jährlich** | 1'325.40 × 0.75 | **994.05 CHF** |
| Zahlprämie monatlich (Zuschlag 5 %) | 994.05 × 1.05 / 12 | 86.98 CHF |

Raucher: Risikoprämie × 2.00 = 1'546.00, Tarifprämie 2'126.42, Zahlprämie 1'594.80 CHF, das entspricht dem in Planung 02 genannten Faktor von rund 1.6 auf die Gesamtprämie.

## Beispiel 2: Kapitalleben Deutschland, Altbestand PK-2000

Frau, 30 Jahre bei Abschluss 2001, Nichtraucherin, Versicherungssumme DM 50'000, umgerechnet EUR 25'564.59, Laufzeit 30 Jahre, Rechnungszins 3.25 %, geschlechtsabhängige Tafel T1985 (vor Unisex).

| Schritt | Rechnung | Wert |
|---|---|---|
| Sparprämie | 25'564.59 × 0.0325 / (1.0325^30 − 1) = 25'564.59 × 0.020186 | 516.05 |
| Deckungskapital zur Laufzeitmitte (Anteil) | (1.0325^15 − 1) / (1.0325^30 − 1) | 0.3823 |
| Risikosumme | 25'564.59 × (1 − 0.3823) | 15'791.25 |
| qx Tafel T1985, Frau, Alter 45 | aus sterbetafel.csv | 0.001580 |
| Risikoprämie | 15'791.25 × 0.001580 | 24.95 |
| Abschlusskosten alpha PK-2000 | 40 ‰ × 25'564.59 / 1000 / 30 | 34.09 |
| Stückkosten DE | | 36.00 |
| Nettoprämie | 516.05 + 24.95 + 34.09 + 36.00 | 611.09 |
| **Tarifprämie jährlich** | 611.09 / (1 − 0.055) | **646.66 EUR** |
| Monatlich (Zuschlag 5 %) | 646.66 × 1.05 / 12 | 56.58 EUR |

Die Überschussbeteiligung wird bei Kapitalleben nicht mit der Prämie verrechnet, sondern jährlich dem Vertrag gutgeschrieben (ueberschuss_parameter.csv, Spalten zinsueberschuss_pct und schlussueberschuss_pct).

## Beispiel 3: Zusatzbaustein Erwerbsunfähigkeit Schweiz

EU-Rente CHF 2'000 monatlich (Jahresrente 24'000), Wartefrist 24 Monate, Endalter 65, Berufsgruppe 3.

| Schritt | Rechnung | Wert |
|---|---|---|
| Grundsatz CH | 3.2 % der Jahresrente | 768.00 |
| Berufsgruppe 3 | × 1.30 | 998.40 |
| Wartefrist 24 Monate | × 0.85 | 848.64 |
| Endalter 65 | × 1.00 | 848.64 |
| **Nettoprämie jährlich** | | **848.65 CHF** |

Kostenzuschläge und Zahlweise wie beim Hauptvertrag.

## Bewusste Vereinfachungen und Abweichungen

- Die Risikoprämie mit dem mittleren Alter ist eine Näherung an die aktuarielle Nivellierung; sie überschätzt junge Eintrittsalter leicht. Die Zahlprämien liegen dennoch innerhalb der Richtwerte aus Planung 02 §1.2.
- Rechnungszins DE der Generation PL-2017 sinkt ab 2022 auf 0.25 % (Spalte rechnungszins_de_ab_2022_pct); für Verträge derselben Generation gelten deshalb je nach Abschlussjahr unterschiedliche Sparprämien. Das ist gewollt.
- Altverträge PK-85 und PK-95 sind teilweise mit Tarifhandbüchern kalkuliert, die im Datensatz nicht vorliegen. Für sie gilt: Prämie = beobachteter Wert aus VERA.
- 2 bis 4 Prozent der Verträge tragen Prämien, die um mehr als 3 Prozent von der Formel abweichen (manuelle Zuschläge, Erfassungsfehler, DM-Rundung). Sie sind in der Ground Truth markiert.
