# Tarifformel Haftpflicht

Die Parameter stehen in `tarifparameter.yaml`, die Bausteinprämien in `bausteine.csv`, die Branchensätze in `branchenklassen.csv` und die Berufsgruppensätze in `berufsgruppen.csv`. Die Formel ist bewusst einfach gehalten, damit Seminarteilnehmer Prämien in Excel nachrechnen können.

## Allgemeine Struktur

```
Nettoprämie  = max( Mindestprämie,
                    Grundprämie × Generationsfaktor × Π Faktoren
                    + Σ Bausteinprämien (fix)
                  ) × Π Rabatte
Steuer       = Nettoprämie × Steuersatz        (CH Stempelabgabe 5 %, DE Versicherungsteuer 19 %)
Bruttoprämie = Nettoprämie + Steuer
Ratenzuschlag auf Bruttoprämie bei unterjähriger Zahlung.
Rundung: CH auf 5 Rappen, DE auf 1 Cent.
```

Prozentuale Bausteine (Betriebshaftpflicht) und Zuschläge werden als Faktor `1 + Prozent/100` in das Produkt der Faktoren aufgenommen.

## Privathaftpflicht (HP-PRIV)

```
Grundprämie(Personenkreis)
× Generationsfaktor
× Deckungssummenfaktor × Selbstbehaltfaktor × Tarifzonenfaktor × Altersfaktor × Vorschadenfaktor
+ Bausteine (fix)
× Bündelrabatt × Mehrjahresrabatt (CH) × Berufsgruppenrabatt (DE) × Kanalrabatt × Papierlos-Rabatt
```

### Beispiel 1: Familie in Olten, Schweiz, Generation PM-2025

| Schritt | Wert |
|---|---|
| Grundprämie Familie CH | 165.00 |
| Generationsfaktor PM-2025 | × 1.00 |
| Deckungssumme 5 Mio. | × 1.00 |
| Selbstbehalt 200 | × 1.00 |
| Tarifzone Olten = 2 | × 1.00 |
| Alter VN 42 | × 1.00 |
| Vorschäden 0 | × 0.95 |
| Zwischensumme | 156.75 |
| Baustein Hund (CH im Grundtarif) | + 0.00 |
| Mehrjahresvertrag 3 Jahre | × 0.95 |
| Papierlos | × 0.98 |
| **Nettoprämie** | **145.93** → gerundet 145.95 |
| Stempelabgabe 5 % | + 7.30 |
| **Bruttoprämie jährlich** | **153.25 CHF** |

### Beispiel 2: Einzelperson in Berlin, Generation MZ-DIRECT, Direktkanal, monatliche Zahlung

| Schritt | Wert |
|---|---|
| Grundprämie Einzel DE | 52.00 |
| Generationsfaktor MZ-DIRECT | × 0.92 |
| Deckungssumme 10 Mio. | × 1.05 |
| Selbstbehalt 150 | × 0.85 |
| Tarifzone Berlin = 1 | × 1.10 |
| Alter VN 24 | × 1.10 |
| Vorschäden 1 | × 1.00 |
| Zwischensumme | 51.65 |
| Kanal direkt | × 0.95 |
| Papierlos | × 0.98 |
| **Nettoprämie** | **48.09** |
| Versicherungsteuer 19 % | + 9.14 |
| Bruttoprämie jährlich | 57.23 |
| Ratenzuschlag monatlich 5 % | × 1.05 |
| **Bruttoprämie jährlich bei Monatszahlung** | **60.09 EUR** (12 × 5.01) |

## Betriebshaftpflicht (HP-BETR)

```
Bemessungsgrundlage × Prämiensatz(Risikoklasse) / 1000
× Generationsfaktor
× Deckungssummenfaktor × Selbstbehaltfaktor × Tarifzonenfaktor × Mitarbeiterstaffel
× Π (1 + Baustein-%) × Π (1 + Zuschlag-%)
× Zertifizierungsrabatt × Schadenfreiheitsrabatt
mindestens Mindestprämie
```

CH bemisst auf der Lohnsumme, DE auf dem Umsatz. Für DE-Handwerksbetriebe der Risikoklassen 3 bis 5 kann alternativ pro Kopf tarifiert werden; der Generator wählt pro Kopf, wenn der Umsatz fehlt oder unter EUR 300'000 liegt.

### Beispiel 3: Sanitärbetrieb in Hannover, 12 Beschäftigte, Umsatz EUR 1'400'000, Generation HP-MODERN

| Schritt | Wert |
|---|---|
| Branche 43.22 Sanitär, Risikoklasse 4, Satz DE 3.0 ‰ | 1'400'000 × 3.0 / 1000 = 4'200.00 |
| Generationsfaktor HP-MODERN | × 0.95 |
| Deckungssumme 5 Mio. | × 1.00 |
| Selbstbehalt 500 | × 1.00 |
| Tarifzone Hannover = 2 | × 1.02 |
| Mitarbeiterstaffel 6 bis 20 | × 1.00 |
| Baustein Umwelt 10 % | × 1.10 |
| Zuschlag Heissarbeiten 8 % | × 1.08 |
| Zuschlag Schadenquote 3 Jahre 40 bis 80 % | × 1.10 |
| Rabatt schadenfrei 3 Jahre | entfällt |
| **Nettoprämie** | **5'320.52** |
| Versicherungsteuer 19 % | + 1'010.90 |
| **Bruttoprämie jährlich** | **6'331.42 EUR** |

### Beispiel 4: Coiffeursalon in Thun, Lohnsumme CHF 180'000, 3 Beschäftigte, Generation PM-2025

| Schritt | Wert |
|---|---|
| Branche 96.02, Risikoklasse 1, Satz CH 1.5 ‰ auf Lohnsumme | 180'000 × 1.5 / 1000 = 270.00 |
| Generationsfaktor PM-2025 | × 1.00 |
| Deckungssumme 5 Mio., SB 500, Zone 2 | × 1.00 |
| Mitarbeiterstaffel bis 5 | × 0.95 |
| Zwischensumme | 256.50 |
| Mindestprämie CH HP-BETR 350.00 | greift: 350.00 |
| **Nettoprämie** | **350.00** |
| Stempelabgabe 5 % | + 17.50 |
| **Bruttoprämie jährlich** | **367.50 CHF** |

## Berufshaftpflicht (HP-BERUF)

```
Honorar- oder Umsatzsumme × Prämiensatz(Berufsgruppe, Untergruppe) / 1000
× Generationsfaktor
× Deckungssummenfaktor × Selbstbehaltfaktor × Tätigkeitsfaktor × Vorschadenfaktor × Tarifzonenfaktor
× Verbandsrabatt
mindestens Mindestprämie
```

### Beispiel 5: Architekturbüro in Zürich, Honorarsumme CHF 900'000, mit Bauleitung, Generation HP-MODERN

| Schritt | Wert |
|---|---|
| BG-ARCH Architekt 8.0 ‰ | 900'000 × 8.0 / 1000 = 7'200.00 |
| Generationsfaktor HP-MODERN | × 0.95 |
| Deckungssumme 2 Mio. | × 1.18 |
| Selbstbehalt 10 % min. 5'000 | × 0.93 |
| Tätigkeit Bauleitung | × 1.30 |
| Vorschäden 1 | × 1.00 |
| Tarifzone Zürich = 1 | × 1.04 |
| Verbandsmitglied | × 0.95 |
| **Nettoprämie** | **9'640.04** → 9'640.05 |
| Stempelabgabe 5 % | + 482.00 |
| **Bruttoprämie jährlich** | **10'122.05 CHF** |

## Bewusste Abweichungen im Datensatz

- 3 bis 5 % der Verträge weichen um mehr als 2 % vom Tarif ab (manuelle Rabatte, Altbestand mit eingefrorener Prämie, Erfassungsfehler). Diese Verträge sind in `truth/` markiert und dienen Anomalie-Übungen.
- Altverträge der Generation HP-KLASSIK tragen teilweise noch Prämien aus Tarifhandbüchern vor 2013, die im Datensatz nicht enthalten sind. Für sie gilt: Prämie = beobachteter Wert, keine Nachrechenbarkeit. Das ist realistisch und im Data Dictionary vermerkt.
- Die Prämienharmonisierung 2025 hebt alle Generationen schrittweise auf Faktor 1.00; im Stichtagsbestand ist sie erst für Neugeschäft und Nachträge 2025 wirksam.
