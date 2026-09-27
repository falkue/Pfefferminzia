const UNDERWRITING_DATEN = {
  "stichtag": "Bewertungsstand je Antrag, siehe Entscheidungsvorlage",
  "regel": "Regelpfad nach der Annahmerichtlinie Leben (RW-LV-ARL-2025) und der Kompetenzordnung (RW-GRUPPE-R08-2025): Prüfumfang, Gewicht, Nikotin, Beruf, Vorerkrankungen, Freizeit, Kombination/Risikoklasse, Kompetenz. Der rot markierte Schritt zeigt, wo eine natürliche Person entscheidet, nie ein System.",
  "antraege": [
    {
      "id": "nazari",
      "antragsteller": "Dr. Farid Nazari",
      "antragId": "ANT-00000602",
      "summeText": "EUR 1'200'000.00",
      "risikoklasse": 2,
      "risikoklasseText": "2 – leicht erhöht",
      "empfehlung": "Annahme mit Zuschlag 50.0 % (entschieden durch mich)",
      "regelpfad": [
        {
          "schritt": "Prüfumfang",
          "paragraf": "§ 2 ARL-2025",
          "ergebnis": "Summe EUR 1'200'000.00, Alter 51 (unter 55) → Stufe bis EUR 1'500'000.00: Fragebogen, Hausarztzeugnis, Vertrauensarzt, Labor. Alle vier Unterlagen liegen vor."
        },
        {
          "schritt": "Gewicht",
          "paragraf": "§ 3 ARL-2025",
          "ergebnis": "BMI 26.9, Altersgruppe 40 bis 59, Spanne 18.5 bis 27.9 → Zuschlag 0.0 %."
        },
        {
          "schritt": "Nikotin",
          "paragraf": "§ 4 ARL-2025",
          "ergebnis": "Angabe Nein, Cotinin negativ → Nichtrauchertarif, 0.0 %."
        },
        {
          "schritt": "Beruf",
          "paragraf": "§ 5 ARL-2025",
          "ergebnis": "Keine Zusatzversicherung Erwerbs- oder Berufsunfähigkeit → nicht anwendbar."
        },
        {
          "schritt": "Vorerkrankungen",
          "paragraf": "§ 6 ARL-2025, Tabelle 6.1",
          "ergebnis": "Bluthochdruck seit 2021, RR unter 140/90, Behandlungsbeginn unter 5 Jahren, Summe über EUR 750'000.00 → ~~Zuschlag 25.0 % bis 50.0 % (Spanne, Vorschlag 37.5 %)~~ Zuschlag 50.0 % (entschieden durch mich, wegen LDL und Familienanamnese). Bandscheibenvorfall 2019 ohne Operation → 0.0 %."
        },
        {
          "schritt": "Freizeit",
          "paragraf": "§ 7 ARL-2025",
          "ergebnis": "Skitouren auf markierten Routen → 0.0 ‰."
        },
        {
          "schritt": "Kombination und Risikoklasse",
          "paragraf": "§ 8 ARL-2025",
          "ergebnis": "~~Gesamtzuschlag 25.0 % bis 50.0 % (Vorschlag 37.5 %)~~ Gesamtzuschlag 50.0 % (entschieden durch mich) → Risikoklasse 2, leicht erhöht."
        },
        {
          "schritt": "Kompetenz",
          "paragraf": "§ 9 Nr. 1 und Nr. 3 ARL-2025, § 4 Kompetenzordnung",
          "ergebnis": "Zuschlag wird nie automatisiert entschieden; Summe über EUR 750'000.00 → Gesellschaftsarzt entscheidet. Entscheid getroffen: 50.0 % Zuschlag (entschieden durch mich).",
          "mensch": true
        }
      ],
      "vorlage": "# Entscheidungsvorlage Risikoprüfung Leben – Dr. Farid Nazari\n\nAntrag ANT-00000602 · Partner PTR-00000006 · Bewertungsstand 28.05.2025 (Stand der damaligen Entscheidung) · Datenbasis: Kundenakte Dr. Nazari, Datensatz Stufe S\n\n## Antrag in Kürze\n\nDr. med. Farid Nazari, geb. 30.11.1973, 51 Jahre bei Antragseingang. Facharzt für Orthopädie, selbständig in einer Gemeinschaftspraxis, Jahreseinkommen ca. EUR 240'000.00. Produkt RisikoLeben, Todesfallsumme EUR 1'200'000.00 konstant, Laufzeit 18 Jahre. Zweck: Absicherung Praxisdarlehen EUR 900'000.00 und Familie. Bezugsberechtigt: Ehefrau Dr. Sabine Nazari. Antrag unterschrieben 10.03.2025, eingereicht über die Isarwerk Finanzberatung GmbH.\n\n## Prüfumfang und vorliegende Unterlagen\n\nBei einer Todesfallsumme über EUR 750'000.00 und einem Alter unter 55 Jahren verlangt § 2 der Annahmerichtlinie die Stufe bis EUR 1'500'000.00: Fragebogen, ärztliches Zeugnis des Hausarztes, Untersuchung beim Vertrauensarzt und Labor. Vorliegend zum Bewertungsstand: Gesundheitserklärung im Antrag vom 10.03.2025, Hausarztzeugnis Dr. Steiner vom 24.04.2025 und Untersuchungsbericht des Vertrauensarztes Dr. Hofmann mit Laborwerten vom 05.05.2025. Der Prüfumfang ist damit vollständig erfüllt.\n\n## Bewertung Schritt für Schritt\n\n- Gewicht (§ 3): 181 cm / 88 kg, BMI 26.9 (Vertrauensarzt am 05.05.2025: 87.5 kg, BMI 26.7). Beide Werte liegen in der Spanne 18.5 bis 27.9, Altersgruppe 40 bis 59. Zuschlag: 0.0 %.\n- Nikotin (§ 4): Angabe Nein, Cotinin im Labor negativ. Nichtrauchertarif. Zuschlag: 0.0 %.\n- Beruf (§ 5): Keine Zusatzversicherung Erwerbs- oder Berufsunfähigkeit beantragt; § 5 bewertet nur diese Deckung. Nicht anwendbar.\n- Vorerkrankung – Bluthochdruck (§ 6, Tabelle 6.1): seit 2021 mit Ramipril eingestellt, RR 134/84 bis 135/85 (unter 140/90), Behandlungsbeginn vor weniger als 5 Jahren, Summe über EUR 750'000.00. ~~Zuschlag: 25.0 % bis 50.0 % (Spanne, siehe unten).~~ Zuschlag: 50.0 % (entschieden durch mich, wegen LDL und Familienanamnese; siehe unten).\n- Vorerkrankung – Bandscheibenvorfall L5/S1 2019 (§ 6): konservativ behandelt, seit 2020 beschwerdefrei; entspricht am ehesten Rückenschmerzen unspezifisch, keiner Operation. Zuschlag: 0.0 %.\n- Freizeit (§ 7): Skitouren auf markierten Routen. Zuschlag: 0.0 ‰.\n\n### Spanne beim Bluthochdruck (§ 6, Tabelle 6.1)\n\nDie Richtlinie lässt für diesen Befund eine Spanne von 25.0 % bis 50.0 % und verlangt, dass die Risikoprüfung innerhalb der Spanne nach Blutdruckwerten, Blutfetten und Familienanamnese entscheidet.\n\n- Für den unteren Rand (25.0 %) spricht: Blutdruck durchgehend unter 140/90, laut Vertrauensarzt keine Endorganschäden.\n- Für den oberen Rand (50.0 %) spricht: leicht erhöhtes LDL (138 mg/dl) und Familienanamnese (Vater Myokardinfarkt mit 68 Jahren), beide vom Vertrauensarzt genannt.\n- ~~Vorschlag: 37.5 % (Mitte der Spanne). Begründung: Der Vertrauensarzt beschreibt die Situation selbst als versicherbar mit einem mässigen Zuschlag; die belastenden Befunde (LDL, Familienanamnese) wiegen nach dieser Einschätzung nicht so schwer wie ein durchgehend erhöhter Blutdruck, die günstige Einstellung rechtfertigt aber auch keinen Wert am unteren Rand.~~\n- ~~Wahl offen, bis Sie entscheiden.~~\n- **Entschieden: 50.0 % (oberer Rand der Spanne), wegen LDL und Familienanamnese (entschieden durch mich).**\n\n## Gesamtzuschlag und Risikoklasse\n\n~~Gesamtzuschlag nach § 8 (additiv): 0.0 % (Gewicht) plus 0.0 % (Bandscheibenvorfall) plus 25.0 % bis 50.0 % (Bluthochdruck, Vorschlag 37.5 %) ergibt 25.0 % bis 50.0 %, vorgeschlagen 37.5 %.~~ Gesamtzuschlag nach § 8 (additiv): 0.0 % (Gewicht) plus 0.0 % (Bandscheibenvorfall) plus 50.0 % (Bluthochdruck, entschieden durch mich) ergibt 50.0 %. Der Nichtrauchertarif gilt unabhängig davon. Freizeitzuschlag: 0.0 ‰.\n\n~~Risikoklasse (§ 8): In der gesamten Spanne von 25.0 % bis 50.0 % bleibt der Antrag in Risikoklasse 2, leicht erhöht (1 % bis 50 %); die Wahl innerhalb der Spanne ändert die Risikoklasse nicht.~~ Risikoklasse (§ 8): Bei einem Zuschlag von 50.0 % liegt der Antrag in Risikoklasse 2, leicht erhöht (1 % bis 50 %).\n\n## Wer entscheidet, System oder Mensch, und auf welcher Stufe\n\nEin Zuschlag wird nach § 9 Nr. 1 der Annahmerichtlinie nie automatisiert entschieden, unabhängig von der Risikoklasse. Zusätzlich liegt die Summe von EUR 1'200'000.00 über der Automatikgrenze von EUR 400'000.00. Zuständig ist ein Mensch auf der Stufe Gesellschaftsarzt (§ 9 Nr. 3 Annahmerichtlinie, § 4 Kompetenzordnung: Gesellschaftsarzt bis Risikoklasse 4 und Summe bis EUR 1'500'000.00).\n\n## Empfehlung\n\nAnnahme mit Zuschlag auf die Risikoprämie im Nichtrauchertarif, Risikoklasse 2. ~~Vorgeschlagener Zuschlag: 37.5 % innerhalb der Spanne 25.0 % bis 50.0 % – Wahl offen, bis Sie entscheiden.~~ Entschieden: Zuschlag 50.0 %, wegen LDL und Familienanamnese (entschieden durch mich). Nachprüfung gemäss § 9 Nr. 5 nach Ablauf von zwei Jahren möglich, wenn die Blutdruckwerte stabil bleiben.\n\n## Offene Rückfragen\n\nKeine: Der Prüfumfang nach § 2 ist mit Fragebogen, Hausarztzeugnis, Vertrauensarztbericht und Labor vollständig erfüllt. ~~Optional liesse sich vor der endgültigen Wahl innerhalb der Spanne eine aktuelle Lipidkontrolle anfragen, da das LDL laut Vertrauensarzt leicht erhöht war.~~ Der Zuschlag ist entschieden (siehe Empfehlung).\n\n## Was nicht in die Entscheidung einfliessen darf\n\nNationalität und Herkunft sowie der Wohnort als Proxy für Herkunft (§ 1 Nr. 2). Ergebnisse genetischer Untersuchungen dürfen nicht verlangt und nicht verwendet werden (§ 1 Nr. 3); zum Bewertungsstand 28.05.2025 lag ohnehin kein Gentest vor, das Thema kam laut Kundenakte erst im September 2025 auf und bleibt für diese Entscheidung unbeachtlich. Das Geschlecht darf bei Neugeschäft in Deutschland nicht als Merkmal verwendet werden (§ 1 Nr. 2).\n\n## Vergleich mit dem damaligen Entscheid\n\nAm 28.05.2025 haben Frau S. Lehmann (Senior-Risikoprüfung) und Dr. med. K. Weber (Gesellschaftsarzt) den Antrag mit einem Zuschlag von 50.0 % auf die Risikoprämie angenommen (Gegenofferte vom 28.05.2025, Erläuterungsschreiben vom 16.06.2025). Das entspricht dem oberen Rand der hier ermittelten Spanne und ebenfalls Risikoklasse 2. ~~Die Entscheidungsstufe (Gesellschaftsarzt) stimmt mit dieser Vorlage überein; der damals gewählte Prozentsatz (50.0 %) liegt höher als der hier vorgeschlagene Mittelwert (37.5 %), aber innerhalb der von der Richtlinie erlaubten Spanne.~~ Die Entscheidungsstufe (Gesellschaftsarzt) und der Prozentsatz (50.0 %) stimmen mit dem hier getroffenen Entscheid überein."
    },
    {
      "id": "brandes",
      "antragsteller": "Katrin Brandes",
      "antragId": "ANT-00009001",
      "summeText": "EUR 400'000.00",
      "risikoklasse": 3,
      "risikoklasseText": "3 – erhöht",
      "empfehlung": "Annahme mit Zuschlag 100.0 %",
      "regelpfad": [
        {
          "schritt": "Prüfumfang",
          "paragraf": "§ 2 ARL-2025",
          "ergebnis": "Summe EUR 400'000.00, Alter 44 (unter 55) → Stufe bis EUR 750'000.00: Fragebogen und Hausarztzeugnis. Beide Unterlagen liegen vor, ein Cotinin-Test ist unterhalb EUR 750'000.00 nicht nötig."
        },
        {
          "schritt": "Gewicht",
          "paragraf": "§ 3 ARL-2025",
          "ergebnis": "BMI 31.2, Altersgruppe 40 bis 59, Spanne 30.0 bis 32.9 → Zuschlag 25.0 %."
        },
        {
          "schritt": "Nikotin",
          "paragraf": "§ 4 ARL-2025",
          "ergebnis": "Ca. 15 Zigaretten pro Tag → Rauchertarif, kein zusätzlicher Prozentzuschlag (nicht über 20 pro Tag)."
        },
        {
          "schritt": "Beruf",
          "paragraf": "§ 5 ARL-2025",
          "ergebnis": "Keine Zusatzversicherung Erwerbs- oder Berufsunfähigkeit → nicht anwendbar."
        },
        {
          "schritt": "Vorerkrankungen",
          "paragraf": "§ 6 ARL-2025",
          "ergebnis": "Asthma bronchiale leicht, gut kontrolliert → 0.0 %. Diabetes mellitus Typ 2, HbA1c 6.6 % (Laborbefund liegt vor) → Zuschlag 75.0 %."
        },
        {
          "schritt": "Freizeit",
          "paragraf": "§ 7 ARL-2025",
          "ergebnis": "Tauchen bis 30 m mit Tauchschein → 0.0 ‰."
        },
        {
          "schritt": "Kombination und Risikoklasse",
          "paragraf": "§ 8 ARL-2025",
          "ergebnis": "Gesamtzuschlag 25.0 % + 75.0 % = 100.0 % → Risikoklasse 3, erhöht."
        },
        {
          "schritt": "Kompetenz",
          "paragraf": "§ 9 Nr. 1 und Nr. 2 ARL-2025, § 4 Kompetenzordnung",
          "ergebnis": "Zuschlag wird nie automatisiert entschieden; Risikoklasse 3 und Summe bis EUR 750'000.00 → Sachbearbeitung entscheidet.",
          "mensch": true
        }
      ],
      "vorlage": "# Entscheidungsvorlage Risikoprüfung Leben – Katrin Brandes\n\nAntrag ANT-00009001 · Bewertungsstand 15.12.2025 (jüngste vorliegende Unterlage) · Datenbasis: Antragseingang Risikoprüfung Leben Dezember 2025, Neukundin ohne Partnernummer\n\n## Antrag in Kürze\n\nKatrin Brandes, geb. 12.06.1981, 44 Jahre bei Antragseingang. Pflegefachfrau im Schichtdienst, angestellt am Klinikum, Jahreseinkommen ca. EUR 52'000.00. Produkt RisikoLeben, Todesfallsumme EUR 400'000.00 konstant, Laufzeit 20 Jahre, gewünschter Beginn 01.01.2026. Zweck: Absicherung Baufinanzierung (Darlehen EUR 360'000.00) und Familie. Bezugsberechtigt: Ehemann Jens Brandes. Keine Zusatzversicherung Erwerbs- oder Berufsunfähigkeit. Antrag unterschrieben 28.11.2025, eingegangen 01.12.2025 über die Agentur Hannover-List.\n\n## Prüfumfang und vorliegende Unterlagen\n\nBei einer Todesfallsumme von EUR 400'000.00 und einem Alter unter 55 Jahren verlangt § 2 der Annahmerichtlinie die Stufe bis EUR 750'000.00: Fragebogen und ärztliches Zeugnis des Hausarztes. Vorliegend: Gesundheitserklärung im Antrag (unterschrieben 28.11.2025) und ärztliches Zeugnis von Dr. Neumann, eingegangen 15.12.2025, mit Laborbefund vom 18.11.2025 zum HbA1c-Wert. Der Prüfumfang ist damit vollständig erfüllt. Ein Cotinin-Test wäre erst ab einer Summe von EUR 750'000.00 nötig (§ 4) und ist hier nicht erforderlich.\n\n## Bewertung Schritt für Schritt\n\n- Gewicht (§ 3): 168 cm / 88 kg, BMI 31.2, Altersgruppe 40 bis 59. Das liegt in der Spanne 30.0 bis 32.9. Zuschlag: 25.0 %.\n- Nikotin (§ 4): Zigaretten, ca. 15 pro Tag seit dem 20. Lebensjahr, das entspricht Raucherin 11 bis 20 pro Tag. Rauchertarif (Faktor 2.0 auf die Risikoprämie), kein zusätzlicher Prozentzuschlag, da nicht über 20 Zigaretten pro Tag.\n- Beruf (§ 5): Keine Zusatzversicherung Erwerbs- oder Berufsunfähigkeit beantragt; § 5 bewertet nur diese Deckung. Nicht anwendbar. Zur Information: Pflegefachfrau im Schichtdienst entspräche Berufsgruppe 3, falls später eine solche Deckung beantragt wird.\n- Vorerkrankung – Asthma bronchiale (§ 6): leicht, gut kontrolliert, keine Exazerbation seit 2019. Zuschlag: 0.0 %.\n- Vorerkrankung – Diabetes mellitus Typ 2 (§ 6): seit 2022, ohne Komplikationen, HbA1c 6.6 % (unter 7 %, Laborbefund vom 18.11.2025 liegt vor). Zuschlag: 75.0 %.\n- Freizeit (§ 7): Tauchen im Urlaub, bis 30 m, mit Tauchschein. Zuschlag: 0.0 ‰.\n\nKeine der anwendbaren Zeilen lässt eine Spanne offen; alle Werte sind fest vorgegeben.\n\n## Gesamtzuschlag und Risikoklasse\n\nGesamtzuschlag nach § 8 (additiv): 25.0 % (Gewicht) plus 75.0 % (Diabetes) ergibt 100.0 %. Der Rauchertarif gilt zusätzlich und unabhängig als eigener Tarif. Freizeitzuschlag: 0.0 ‰.\n\nRisikoklasse (§ 8): 100.0 % liegt in der Spanne 51 % bis 100 % und damit in Risikoklasse 3, erhöht.\n\n## Wer entscheidet, System oder Mensch, und auf welcher Stufe\n\nEin Zuschlag wird nach § 9 Nr. 1 der Annahmerichtlinie nie automatisiert entschieden. Zuständig ist ein Mensch auf der Stufe Sachbearbeitung (§ 9 Nr. 2 Annahmerichtlinie, § 4 Kompetenzordnung: Sachbearbeitung bis Risikoklasse 3 und Summe bis EUR 750'000.00).\n\n## Empfehlung\n\nAnnahme mit Zuschlag von 100.0 % auf die Risikoprämie im Rauchertarif, Risikoklasse 3.\n\n## Offene Rückfragen\n\nKeine zwingenden: Der Prüfumfang nach § 2 ist vollständig erfüllt, der Diabetes-Nachweis liegt per Labor vor, das Asthma ist laut Hausärztin ohne Exazerbation seit 2019. Freiwillig nachverfolgen liesse sich die vom Hausarzt empfohlene Rauchentwöhnung; sie hat keinen Einfluss auf diesen Entscheid.\n\n## Was nicht in die Entscheidung einfliessen darf\n\nNationalität und Herkunft sowie der Wohnort als Proxy für Herkunft (§ 1 Nr. 2). Ergebnisse genetischer Untersuchungen dürfen nicht verlangt und nicht verwendet werden (§ 1 Nr. 3), auch wenn keine solchen Angaben vorliegen. Das Geschlecht darf bei Neugeschäft in Deutschland nicht als Merkmal verwendet werden (§ 1 Nr. 2)."
    },
    {
      "id": "pedrazzini",
      "antragsteller": "Bruno Pedrazzini",
      "antragId": "ANT-00009002",
      "summeText": "CHF 600'000.00",
      "risikoklasse": 5,
      "risikoklasseText": "5 (Berechnung, Entscheid ausstehend)",
      "empfehlung": "Vertrauensarzt und Labor zuerst angefordert (entschieden durch mich)",
      "regelpfad": [
        {
          "schritt": "Prüfumfang",
          "paragraf": "§ 2 ARL-2025",
          "ergebnis": "Summe CHF 600'000.00 läge in der Stufe bis CHF 750'000.00; weil Herr Pedrazzini bei Antragseingang 58 Jahre (55 oder älter) ist, gilt die nächststrengere Stufe bis CHF 1'500'000.00: Fragebogen, Hausarztzeugnis, Vertrauensarzt, Labor. Vertrauensarzt und Labor der Gesellschaft fehlen noch – Prüfumfang unvollständig."
        },
        {
          "schritt": "Gewicht",
          "paragraf": "§ 3 ARL-2025",
          "ergebnis": "BMI 38.4, Altersgruppe 40 bis 59, Spanne 36.0 bis 39.9 → Zuschlag 150.0 %, ärztliches Zeugnis obligatorisch (liegt vor)."
        },
        {
          "schritt": "Nikotin",
          "paragraf": "§ 4 ARL-2025",
          "ergebnis": "Rauchstopp Mai 2022, mehr als 12 Monate zurück → Nichtrauchertarif, 0.0 %."
        },
        {
          "schritt": "Beruf",
          "paragraf": "§ 5 ARL-2025",
          "ergebnis": "Keine Zusatzversicherung Erwerbsunfähigkeit → nicht anwendbar."
        },
        {
          "schritt": "Vorerkrankungen",
          "paragraf": "§ 6 ARL-2025",
          "ergebnis": "Myokardinfarkt 04/2022, EF 55 %, älter als 2 Jahre → Zuschlag 150.0 % (Facharztnachweis liegt vor). Hypercholesterinämie unter Statin → 0.0 %."
        },
        {
          "schritt": "Freizeit",
          "paragraf": "§ 7 ARL-2025",
          "ergebnis": "Keine gefährliche Sportart (Wandern) → 0.0 ‰."
        },
        {
          "schritt": "Kombination und Risikoklasse",
          "paragraf": "§ 8 ARL-2025",
          "ergebnis": "Gesamtzuschlag 150.0 % + 150.0 % = 300.0 %, über 251 % → Risikoklasse 5, Ablehnung."
        },
        {
          "schritt": "Kompetenz",
          "paragraf": "§ 9 Nr. 1 und Nr. 3a ARL-2025, § 5 Nr. 2 Kompetenzordnung",
          "ergebnis": "Ablehnungen werden nie automatisiert entschieden; Gesellschaftsarzt entscheidet (Rückversicherung nicht nötig, Summe unter CHF 1'500'000.00). Entschieden durch mich: Vertrauensarzt und Labor werden zuerst angefordert, bevor über Annahme, Zuschlag oder Ablehnung entschieden wird.",
          "mensch": true
        }
      ],
      "vorlage": "# Entscheidungsvorlage Risikoprüfung Leben – Bruno Pedrazzini\n\nAntrag ANT-00009002 · Bewertungsstand 19.12.2025 (jüngste vorliegende Unterlage; Prüfumfang nicht vollständig) · Datenbasis: Antragseingang Risikoprüfung Leben Dezember 2025, Neukunde ohne Partnernummer\n\n## Antrag in Kürze\n\nBruno Pedrazzini, geb. 03.02.1967, 58 Jahre bei Antragseingang. Betriebsleiter in einer Druckerei, angestellt, Jahreseinkommen ca. CHF 118'000.00, italienische Staatsangehörigkeit mit Niederlassungsbewilligung C. Produkt RisikoLeben, Todesfallsumme CHF 600'000.00 konstant, Laufzeit 7 Jahre (bis Alter 65), gewünschter Beginn 01.02.2026. Zweck: Absicherung Hypothek Eigenheim (CHF 540'000.00). Bezugsberechtigt: Ehefrau Carla Pedrazzini. Keine Zusatzversicherung Erwerbsunfähigkeit. Antrag unterschrieben 01.12.2025, eingegangen 03.12.2025 über die Partnerbank, Filiale Lugano.\n\n## Prüfumfang und vorliegende Unterlagen\n\nBei einer Summe von CHF 600'000.00 würde § 2 die Stufe bis CHF 750'000.00 vorsehen (Fragebogen und Hausarztzeugnis). Weil Herr Pedrazzini bei Antragseingang 58 Jahre und damit 55 oder älter ist, gilt nach § 2 ausdrücklich die nächststrengere Stufe bis CHF 1'500'000.00: Fragebogen, ärztliches Zeugnis Hausarzt, Untersuchung Vertrauensarzt und Labor.\n\nVorliegend: Gesundheitserklärung im Antrag (unterschrieben 01.12.2025), ärztliches Zeugnis von Dr. Bernasconi, eingegangen 19.12.2025, mit kardiologischem Kontrollbericht vom 16.09.2025. Nicht vorliegend: Untersuchung beim Vertrauensarzt und Laborbefund der Gesellschaft – das Hausarztzeugnis vermerkt dies ausdrücklich als noch ausstehend. Der Prüfumfang nach § 2 ist damit wegen des Alters noch nicht vollständig erfüllt; die folgende Bewertung stützt sich nur auf die vorliegenden Unterlagen und ist vorläufig.\n\n## Bewertung Schritt für Schritt\n\n- Gewicht (§ 3): 176 cm / 119 kg, BMI 38.4, Altersgruppe 40 bis 59. Das liegt in der Spanne 36.0 bis 39.9. Zuschlag: 150.0 %. Massnahme laut Tabelle: ärztliches Zeugnis obligatorisch – liegt mit dem Hausarztzeugnis vor.\n- Nikotin (§ 4): Kein Konsum in den letzten 12 Monaten, Rauchstopp im Mai 2022, damit mehr als 12 Monate zurück. Nichtrauchertarif. Zuschlag: 0.0 %.\n- Beruf (§ 5): Keine Zusatzversicherung Erwerbsunfähigkeit beantragt; § 5 bewertet nur diese Deckung. Nicht anwendbar.\n- Vorerkrankung – Myokardinfarkt (§ 6): 14.04.2022 mit Stent, seither beschwerdefrei, Auswurffraktion 55 % (über 50 %), damit älter als 2 Jahre und mit erhaltener Funktion. Zuschlag: 150.0 %. Nachweis Facharzt liegt mit dem Kardiologiebericht vom 16.09.2025 vor.\n- Vorerkrankung – Hypercholesterinämie (§ 6): unter Statin, LDL 92 mg/dl. Zuschlag: 0.0 %.\n- Freizeit (§ 7): Keine gefährliche Sportart angegeben, Wandern. Nicht aufgeführte Aktivitäten ohne besondere Gefahr gelten als normal. Zuschlag: 0.0 ‰.\n\nKeine der anwendbaren Zeilen lässt eine Spanne offen; sowohl Gewicht als auch Herzinfarkt sind mit festen Werten hinterlegt.\n\n## Gesamtzuschlag und Risikoklasse\n\nGesamtzuschlag nach § 8 (additiv): 150.0 % (Gewicht) plus 150.0 % (Herzinfarkt) ergibt 300.0 %. Der Nichtrauchertarif gilt zusätzlich. Freizeitzuschlag: 0.0 ‰.\n\nRisikoklasse (§ 8): 300.0 % liegt über 251 % und damit in Risikoklasse 5, Ablehnung.\n\n## Wer entscheidet, System oder Mensch, und auf welcher Stufe\n\nAblehnungen werden nie automatisiert entschieden (§ 9 Nr. 1 und Nr. 3a Annahmerichtlinie; § 5 Nr. 2 Kompetenzordnung: jede Ablehnung trifft eine natürliche Person). Zuständig ist der Gesellschaftsarzt (§ 9 Nr. 3a Annahmerichtlinie, § 4 Kompetenzordnung). Die Rückversicherung ist nicht zusätzlich zu beteiligen, da die Summe von CHF 600'000.00 unter der Grenze von CHF 1'500'000.00 liegt.\n\n## Empfehlung\n\n~~Auf Basis der vorliegenden Unterlagen weist der Antrag einen Gesamtzuschlag von 300.0 % aus und liegt damit in Risikoklasse 5. Die Annahmerichtlinie sieht dafür grundsätzlich Ablehnung vor (§ 8, § 10 Code AB-MED, medizinisches Gesamtrisiko über der Annahmegrenze). Diese Empfehlung ist vorläufig: Der Prüfumfang nach § 2 ist wegen des Alters noch nicht erfüllt, solange Untersuchung beim Vertrauensarzt und Laborbefund der Gesellschaft fehlen. Der Gesellschaftsarzt sollte den Entscheid erst nach Eingang dieser Unterlagen endgültig treffen.~~\n\nEntschieden durch mich: Bevor über den Antrag entschieden wird, fordern wir die Untersuchung beim Vertrauensarzt und den Laborbefund der Gesellschaft an, wie es § 2 wegen des Alters vorschreibt. Der Gesellschaftsarzt trifft den Entscheid zu Annahme, Zuschlag oder Ablehnung erst nach deren Eingang; die auf den bisherigen Unterlagen beruhende Berechnung eines Gesamtzuschlags von 300.0 % (Risikoklasse 5) dient bis dahin nur der Einordnung, nicht der Entscheidung.\n\n## Offene Rückfragen\n\nKeine mehr offen, sondern entschieden durch mich (siehe Empfehlung): Untersuchung beim Vertrauensarzt und Laborbefund der Gesellschaft werden nach § 2 wegen des Alters angefordert, bevor ein Entscheid ergeht. Die Partnerbank beziehungsweise Herr Pedrazzini werden über den Termin informiert.\n\n## Was nicht in die Entscheidung einfliessen darf\n\nNationalität und Aufenthaltsstatus dürfen nach § 1 Nr. 2 nicht verwendet werden, ebenso nicht der Wohnort als Proxy für Herkunft. Ergebnisse genetischer Untersuchungen dürfen nicht verlangt und nicht verwendet werden (§ 1 Nr. 3), auch wenn keine solchen Angaben vorliegen."
    },
    {
      "id": "hartwig",
      "antragsteller": "Lea Hartwig",
      "antragId": "ANT-00009003",
      "summeText": "CHF 250'000.00",
      "risikoklasse": 1,
      "risikoklasseText": "1 – normal",
      "empfehlung": "Automatische Annahme ohne Zuschlag",
      "regelpfad": [
        {
          "schritt": "Prüfumfang",
          "paragraf": "§ 2 ARL-2025",
          "ergebnis": "Summe CHF 250'000.00, Alter 34 (unter 55) → Stufe bis CHF 300'000.00: nur Fragebogen. Die Gesundheitserklärung liegt unterschrieben vor, Prüfumfang vollständig erfüllt."
        },
        {
          "schritt": "Gewicht",
          "paragraf": "§ 3 ARL-2025",
          "ergebnis": "BMI 22.5, Altersgruppe 18 bis 39, Spanne 18.5 bis 27.9 → Zuschlag 0.0 %."
        },
        {
          "schritt": "Nikotin",
          "paragraf": "§ 4 ARL-2025",
          "ergebnis": "Angabe «nie geraucht» → Nichtrauchertarif, 0.0 %."
        },
        {
          "schritt": "Beruf",
          "paragraf": "§ 5 ARL-2025",
          "ergebnis": "Keine Zusatzversicherung Erwerbsunfähigkeit beantragt → nicht anwendbar."
        },
        {
          "schritt": "Vorerkrankungen",
          "paragraf": "§ 6 ARL-2025",
          "ergebnis": "Heuschnupfen im Frühling (J30, Allergische Rhinitis), Nasenspray bei Bedarf → NORMAL, 0.0 %. Alle übrigen Fragen mit Nein beantwortet."
        },
        {
          "schritt": "Freizeit",
          "paragraf": "§ 7 ARL-2025",
          "ergebnis": "Reiten in der Freizeit → 0.0 ‰, gilt als normal."
        },
        {
          "schritt": "Kombination und Risikoklasse",
          "paragraf": "§ 8 ARL-2025",
          "ergebnis": "Gesamtzuschlag 0.0 % → Risikoklasse 1, normal."
        },
        {
          "schritt": "Kompetenz",
          "paragraf": "§ 9 Nr. 1 ARL-2025, § 4 Kompetenzordnung",
          "ergebnis": "Risikoklasse 1, Summe bis CHF 400'000.00, keine EU/BU-Rente, ausschliesslich positiver Entscheid ohne Erschwerung → automatische Annahme durch die MINT Underwriting-Engine v2 (Modellinventar MI-03), mit 10 Prozent manueller Stichprobe."
        }
      ],
      "vorlage": "# Entscheidungsvorlage Risikoprüfung Leben – Lea Hartwig\n\nAntrag ANT-00009003 · Bewertungsstand 08.12.2025 (einzige vorliegende Unterlage, Prüfumfang vollständig) · Datenbasis: Antragseingang Risikoprüfung Leben Dezember 2025, Neukundin ohne Partnernummer\n\n## Antrag in Kürze\n\nLea Hartwig, geb. 22.05.1991, 34 Jahre bei Antragseingang. Primarlehrerin, angestellt, Jahreseinkommen ca. CHF 96'000.00, schweizerische Staatsangehörigkeit, wohnhaft in Basel. Produkt RisikoLeben, Todesfallsumme CHF 250'000.00 konstant, Laufzeit 25 Jahre, gewünschter Beginn 01.01.2026. Zweck: Absicherung der Familie (zwei Kinder). Bezugsberechtigt: Lebenspartner Marc Frei. Keine Zusatzversicherung Erwerbsunfähigkeit. Antrag eingegangen 08.12.2025 online (Direktabschluss), Gesundheitserklärung gleichentags unterschrieben.\n\n## Prüfumfang und vorliegende Unterlagen\n\nBei einer Summe von CHF 250'000.00 sieht § 2 die Stufe bis CHF 300'000.00 vor: es genügt der Fragebogen. Frau Hartwig ist bei Antragseingang 34 Jahre und damit deutlich unter 55, die Alters-Verschärfung nach § 2 greift nicht. Vorliegend: Gesundheitserklärung (Fragebogen GF-2025), unterschrieben 08.12.2025, mit Einwilligung zur Entbindung von der Schweigepflicht. Damit ist der Prüfumfang nach § 2 vollständig erfüllt; es sind keine weiteren Unterlagen anzufordern.\n\n## Bewertung Schritt für Schritt\n\n- Gewicht (§ 3): 170 cm / 65 kg, BMI 22.5, Altersgruppe 18 bis 39. Das liegt in der Spanne 18.5 bis 27.9. Zuschlag: 0.0 %.\n- Nikotin (§ 4): Angabe «nie geraucht» → Nichtrauchertarif. Zuschlag: 0.0 %.\n- Beruf (§ 5): Keine Zusatzversicherung Erwerbsunfähigkeit beantragt; § 5 bewertet nur diese Deckung. Nicht anwendbar.\n- Vorerkrankungen (§ 6): Heuschnupfen im Frühling mit Nasenspray bei Bedarf entspricht der Diagnosegruppe J30 (Allergische Rhinitis) → NORMAL, Zuschlag 0.0 %, Nachweis Fragebogen liegt vor. Herz-Kreislauf, Bewegungsapparat, Stoffwechsel, psychische Erkrankungen und Dauermedikation wurden je mit Nein beantwortet.\n- Freizeit (§ 7): Reiten in der Freizeit → Zuschlag 0 ‰, gilt nach der Tabelle ausdrücklich als normal.\n\nKeine der anwendbaren Zeilen lässt eine Spanne offen; alle Werte sind fest.\n\n## Gesamtzuschlag und Risikoklasse\n\nGesamtzuschlag nach § 8 (additiv): 0.0 % (Gewicht) + 0.0 % (Nikotin, nicht zutreffend über § 4 hinaus) + 0.0 % (Vorerkrankung) = 0.0 %. Freizeitzuschlag: 0.0 ‰.\n\nRisikoklasse (§ 8): 0.0 % entspricht Risikoklasse 1, normal.\n\n## Wer entscheidet, System oder Mensch, und auf welcher Stufe\n\nRisikoklasse 1 (bis 2), Todesfallsumme CHF 250'000.00 (bis 400'000.00), keine EU/BU-Rente beantragt, ausschliesslich ein positiver Entscheid ohne jede Erschwerung (kein Zuschlag, kein Ausschluss, keine Zurückstellung). Damit erfüllt der Antrag die Voraussetzungen für die automatische Annahme nach § 9 Nr. 1 ARL-2025 und § 4 Kompetenzordnung: Die MINT Underwriting-Engine v2 (Modellinventar MI-03) kann den Antrag ohne Sachbearbeitung annehmen. Vollständige Protokollierung und eine manuelle Stichprobe von 10 Prozent sind vorgeschrieben.\n\n## Empfehlung\n\nAutomatische Annahme zu Normalbedingungen (Risikoklasse 1, kein Zuschlag), Beginn wie beantragt am 01.01.2026. Kein Zuschlag, kein Ausschluss, keine Zurückstellung; keine Beteiligung von Sachbearbeitung, Gesellschaftsarzt oder Rückversicherung erforderlich.\n\n## Offene Rückfragen\n\nKeine. Der Prüfumfang nach § 2 ist mit dem Fragebogen vollständig erfüllt, und keine der Angaben erfordert einen zusätzlichen Nachweis.\n\n## Was nicht in die Entscheidung einfliessen darf\n\nNationalität und Wohnort dürfen nach § 1 Nr. 2 nicht verwendet werden, auch wenn Frau Hartwig schweizerische Staatsangehörige mit Wohnsitz in Basel ist. Ergebnisse genetischer Untersuchungen dürfen nicht verlangt und nicht verwendet werden (§ 1 Nr. 3), auch wenn keine solchen Angaben vorliegen.\n\nEntscheid durch: offen"
    }
  ]
};
