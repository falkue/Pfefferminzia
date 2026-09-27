const AKTE_DATEN = {
  "kopf": {
    "kunde": "Hans-Georg Pieper, geb. 02.09.1962, Dresden",
    "vertrag": "VTR-00000801 · Privathaftpflicht (HP-PRIV) · seit 01.01.2013",
    "versicherungsschein": "vormals 40.288.506-6 (HAPO)",
    "schaden": "SCH-00000810 · Anzeige S2025/001002 · Status: geschlossen"
  },
  "kacheln": [
    {
      "label": "Schadentag",
      "wert": "21.03.2025",
      "definition": "Datum des Ereignisses. Quelle: Schadentabelle, Schadendatum."
    },
    {
      "label": "Tage bis zur Zahlung",
      "wert": "27",
      "definition": "Kalendertage vom Schadentag bis zur Zahlung an den Geschädigten. Quelle: Schadentabelle, Schadendatum; Schadenposition, Zahlung."
    },
    {
      "label": "Bezahlter Betrag",
      "wert": "EUR 1'340.00",
      "definition": "Summe aller Zahlungspositionen (Regulierung an den Geschädigten und Kulanz an den Kunden). Quelle: Schadenposition, Art Zahlung."
    },
    {
      "label": "Zahl der Dokumente",
      "wert": "17",
      "definition": "Dokumente und Kontakte der Fallakte (Briefe, E-Mails, Telefonnotiz, interne Dokumente), vollständig gelesen. Quelle: Ordner der Fallakte PTR-00000008."
    },
    {
      "label": "Tage Ablehnung → Zahlung",
      "wert": "24",
      "definition": "Kalendertage von der automatischen Ablehnung bis zur Zahlung. Quelle: Brief INT-00000802 (Ablehnung); Schadenposition, Zahlung."
    }
  ],
  "gruppen": [
    {
      "id": "kunde",
      "name": "Kunde",
      "farbe": "var(--pfefferminz)"
    },
    {
      "id": "schaden",
      "name": "Schadenabteilung",
      "farbe": "var(--hp)"
    },
    {
      "id": "intern",
      "name": "intern und IT",
      "farbe": "var(--text-secondary)"
    },
    {
      "id": "ombudsmann",
      "name": "Ombudsmann",
      "farbe": "var(--minzia)"
    },
    {
      "id": "aufsicht",
      "name": "Aufsicht",
      "farbe": "var(--lv)"
    }
  ],
  "ereignisse": [
    {
      "id": "vertrag-beginn",
      "datum": "2013-01-01",
      "art": "Vertragstabelle",
      "titel": "Vertragsbeginn Privathaftpflicht (vormals Policennummer 40.288.506-6)",
      "von": "",
      "an": "Hans-Georg Pieper",
      "gruppen": [
        "kunde"
      ],
      "kennungText": "Vertragstabelle, Beginn",
      "volltext": ""
    },
    {
      "id": "DOK-00000802",
      "datum": "2019-02-12",
      "art": "Beratungsprotokoll",
      "titel": "Beratungsdokumentation Paragraph 61 VVG: Hundehalterhaftpflicht",
      "von": "Agentur Dresden",
      "an": "Hans-Georg Pieper",
      "gruppen": [
        "kunde"
      ],
      "kennungText": "Beratungsprotokoll DOK-00000802",
      "volltext": "Anlass: Kunde hat Hund aus dem Tierheim uebernommen (Schaeferhund-Mischling, ca. 3 Jahre).\nWunsch: Absicherung fuer Schaeden durch den Hund.\nEmpfehlung: Einschluss Tierhalterbaustein in bestehende Privathaftpflicht (guenstiger als Einzelpolice). Hinweis auf Listenhunde-Regelung: nicht betroffen.\nEntscheid: Einschluss ab 01.03.2019, Zuschlag EUR 56,50 jaehrlich inkl. VersSt.\nKunde wuenscht Post per Brief, keine E-Mail.\nUnterschrift Kunde / Vermittler 12.02.2019\n\n---"
    },
    {
      "id": "DOK-00000801",
      "datum": "2019-02-15",
      "art": "Nachtrag",
      "titel": "Nachtrag Nr. 2 zum Versicherungsschein 40.288.506-6, wirksam 01.03.2019",
      "von": "Pfefferminzia (Agentur Dresden)",
      "an": "Hans-Georg Pieper",
      "gruppen": [
        "kunde"
      ],
      "kennungText": "Nachtrag DOK-00000801",
      "volltext": "Aenderungsgrund: Einschluss Baustein Tierhalterhaftpflicht (Hund)\n\n                          bisher            neu\nBaustein Tierhalter       nicht versichert  eingeschlossen, 1 Hund (Schaeferhund-Mischling 'Rex', kein Listenhund)\nDeckungssumme Tierhalter  -                 innerhalb Deckungssumme EUR 5 Mio.\nJahresbeitrag brutto      EUR 74,90         EUR 131,40 (Zuschlag Hund EUR 56,50 inkl. Versicherungsteuer)\n\nHinweis: In Sachsen besteht keine allgemeine Hundehalterhaftpflicht-Pflicht (vereinfachte Darstellung). Die uebrigen Bestimmungen bleiben unveraendert. Bedingungsgeneration HP-MODERN.\n\nAgentur Dresden, 15.02.2019\n\n---"
    },
    {
      "id": "baustein-wirksam",
      "datum": "2019-03-01",
      "art": "Deckungstabelle",
      "titel": "Baustein Tierhalterhaftpflicht (BS-TIER-HUND) wirksam",
      "von": "",
      "an": "Hans-Georg Pieper",
      "gruppen": [
        "kunde"
      ],
      "kennungText": "Deckungstabelle, Baustein, gültig ab",
      "volltext": ""
    },
    {
      "id": "migration",
      "datum": "2025-03-03",
      "art": "Migrationslog",
      "titel": "Migration Pilotwelle Privathaftpflicht Deutschland: Bausteincode Tierhalter nicht ins Zielschema übernommen (Warnung)",
      "von": "",
      "an": "",
      "gruppen": [
        "intern"
      ],
      "kennungText": "Migrationslog, Vorgang HP-2025-PILOT",
      "volltext": ""
    },
    {
      "id": "INT-00000801",
      "datum": "2025-03-21T16:35",
      "art": "Telefonnotiz",
      "titel": "Telefonnotiz Schadenmeldung Hundebiss",
      "von": "Hans-Georg Pieper",
      "an": "Contact Center Leipzig",
      "gruppen": [
        "kunde",
        "schaden"
      ],
      "kennungText": "Telefonnotiz INT-00000801",
      "volltext": "Tel. VN Pieper, Contact Center Leipzig (Aushilfe), 7 Min. Stichworte: Hund, Biss, Radfahrer, Leine ja, Wade, Notaufnahme Uniklinik, Hose kaputt. Geschaedigter: Herr M., Dresden, Kontaktdaten aufgenommen. VN sagt 'Hund ist doch bei euch versichert, seit 2019'. Erfasst in MINT als Schaden SCH-00000810, Kategorie Tierhalter.\n\n---"
    },
    {
      "id": "SCH-00000810-01",
      "datum": "2025-03-21",
      "art": "Schadenposition",
      "titel": "Erstreserve automatisch gebildet, EUR 1'500.00",
      "von": "",
      "an": "",
      "gruppen": [
        "intern"
      ],
      "kennungText": "Schadenposition SCH-00000810-01",
      "volltext": ""
    },
    {
      "id": "INT-00000802",
      "datum": "2025-03-24T06:00",
      "art": "Brief",
      "titel": "Ablehnung Ihres Schadens SCH-00000810 (automatisch)",
      "von": "Pfefferminzia, Schaden Haftpflicht (maschinell erstellt, ohne Unterschrift)",
      "an": "Hans-Georg Pieper",
      "gruppen": [
        "kunde",
        "schaden"
      ],
      "kennungText": "Brief INT-00000802",
      "volltext": "Sehr geehrter Herr Pieper,\n\nSie haben uns einen Schaden vom 21.03.2025 gemeldet, den Ihr Hund verursacht hat. Nach Pruefung Ihres Vertrages VTR-00000801 muessen wir Ihnen mitteilen, dass Schaeden durch Tiere nur versichert sind, wenn der Baustein Tierhalterhaftpflicht eingeschlossen ist. Ihr Vertrag enthaelt diesen Baustein nicht. Wir koennen den Schaden daher nicht uebernehmen (AHB 2013 Ziffer 7.4 in Verbindung mit BBR 2015).\n\nSollten Sie mit dieser Entscheidung nicht einverstanden sein, koennen Sie sich an den Versicherungsombudsmann e. V. wenden.\n\nMit freundlichen Gruessen\nPfefferminzia Versicherung AG, Niederlassung Deutschland\nSchaden Haftpflicht\n\nDieses Schreiben wurde maschinell erstellt und ist ohne Unterschrift gueltig.\n\n---",
      "wendepunkt": "Automatische Ablehnung"
    },
    {
      "id": "DOK-00000803",
      "datum": "2025-03-25",
      "art": "Arztrechnung",
      "titel": "Rechnung Notfallbehandlung Hundebiss",
      "von": "Universitätsklinikum Dresden, Notaufnahme",
      "an": "Radfahrer (Geschädigter)",
      "gruppen": [],
      "kennungText": "Arztrechnung DOK-00000803",
      "volltext": "Patient: Herr M., Dresden. Behandlungsdatum 21.03.2025.\nDiagnose: Bissverletzung rechte Wade (S81.8), oberflaechlich, Wundreinigung, Tetanus-Auffrischung, Antibiotikaprophylaxe.\n\nNotfallpauschale                 EUR 210,00\nWundversorgung                    EUR 145,00\nImpfung und Medikamente           EUR 85,00\nGesamt                            EUR 440,00\n\nZahlbar durch den Patienten; Weiterberechnung an den Tierhalter vorbehalten.\n\n---"
    },
    {
      "id": "INT-00000803",
      "datum": "2025-03-28",
      "art": "Brief",
      "titel": "BESCHWERDE – SCHADEN NR. SCH-00000810 – ABLEHNUNG UNBERECHTIGT",
      "von": "Hans-Georg Pieper",
      "an": "Aylin Demirci, Teamleiterin Schaden Haftpflicht Deutschland",
      "gruppen": [
        "kunde",
        "schaden"
      ],
      "kennungText": "Beschwerdebrief INT-00000803",
      "volltext": "Dresden, den 28. Maerz 2025\n\nBESCHWERDE – SCHADEN NR. SCH-00000810 – ABLEHNUNG UNBERECHTIGT\n\nSehr geehrte Damen und Herren,\n\nIhr Schreiben vom 24.03.2025 habe ich erhalten. Sie behaupten, mein Vertrag enthalte keinen Tierhalterbaustein. DAS IST FALSCH. Ich habe den Baustein seit dem 1. Maerz 2019 in meinem Vertrag, damals bei Ihrer Agentur in Dresden abgeschlossen. Ich habe das Beratungsprotokoll und den Nachtrag Nr. 2 hier vor mir liegen, mit Unterschrift Ihres Vertreters. Seit 2019 bezahle ich dafuer jedes Jahr 56,50 Euro mehr.\n\nEs ist mein gutes Recht, dass Sie den Schaden meines Nachbarn bezahlen. Herr M. hat mir gesagt, er wartet noch bis Mitte April, dann geht er zum Anwalt.\n\nIch fordere Sie auf, den Schaden binnen 14 Tagen zu regulieren und mir schriftlich zu erklaeren, wer diesen Brief geschrieben hat. Ein Computer kann mir nicht meinen Vertrag absprechen. Sollten Sie nicht reagieren, wende ich mich an die Saechsische Zeitung und an den Ombudsmann.\n\nHochachtungsvoll\nH.-G. Pieper\n\nAnlagen: Kopie Nachtrag Nr. 2 vom 15.02.2019, Kopie Beratungsprotokoll\n\n---"
    },
    {
      "id": "INT-00000804",
      "datum": "2025-04-02T11:20",
      "art": "E-Mail",
      "titel": "Eingangsbestaetigung Ihrer Beschwerde",
      "von": "Pfefferminzia, Kundenservice Leipzig",
      "an": "Hans-Georg Pieper",
      "gruppen": [
        "kunde",
        "schaden"
      ],
      "kennungText": "E-Mail INT-00000804",
      "volltext": "Sehr geehrter Herr Pieper,\n\nvielen Dank fuer Ihr Schreiben vom 28.03.2025. Ihr Anliegen wird geprueft. Wir melden uns innerhalb von 15 Arbeitstagen bei Ihnen.\n\nMit freundlichen Gruessen\nKundenservice Leipzig"
    },
    {
      "id": "INT-00000805",
      "datum": "2025-04-15",
      "art": "Brief",
      "titel": "ZWEITE BESCHWERDE – OMBUDSMANN UND BAFIN",
      "von": "Hans-Georg Pieper",
      "an": "Miriam Steinbrecher, Compliance Officer Deutschland",
      "gruppen": [
        "kunde",
        "schaden"
      ],
      "kennungText": "Beschwerdebrief INT-00000805",
      "volltext": "Dresden, den 15. April 2025\n\nZWEITE BESCHWERDE – SCHADEN NR. SCH-00000810\n\nSehr geehrte Damen und Herren,\n\nauf meine Beschwerde vom 28.03. habe ich eine Standardmail bekommen, in der steht, mein Anliegen werde geprueft. Seither: NICHTS. Herr M. war gestern bei mir und hat mir die Anwaltskarte gezeigt.\n\nIch habe mich heute schriftlich an den Versicherungsombudsmann e. V. in Berlin gewandt (Kopie anbei). Ich werde mich ausserdem bei der Bundesanstalt fuer Finanzdienstleistungsaufsicht beschweren, weil Sie einen Vertrag, den ich seit sechs Jahren bezahle, per Computer fuer nicht existent erklaeren. Sie haben das schriftlich.\n\nHochachtungsvoll\nH.-G. Pieper\n\n---"
    },
    {
      "id": "INT-00000806",
      "datum": "2025-04-16T09:05",
      "art": "interne E-Mail",
      "titel": "Eskalation Fall Pieper: automatische Ablehnung trotz Baustein",
      "von": "Aylin Demirci, Teamleiterin Schaden Haftpflicht Deutschland",
      "an": "Jonas Pfister, MLOps, Miriam Steinbrecher, Compliance Officer Deutschland (Cc Martina Jost)",
      "gruppen": [
        "intern"
      ],
      "kennungText": "interne E-Mail INT-00000806",
      "volltext": "An: Jonas Pfister (MLOps), Miriam Steinbrecher (Compliance DE); Cc: Martina Jost\n\nHallo zusammen,\n\nwir haben ein Problem. Der Kunde Pieper (VTR-00000801) hat seit 2019 den Baustein Tierhalter, das sehe ich in HAPO (ZUSATZ1 = 'HUND', BST=01). In MINT ist das Feld coverages nach der Migration leer. Die Triage v3 hat den Schaden am 24.03. automatisch abgelehnt und das Ablehnungsschreiben ist rausgegangen, ohne dass jemand draufgeschaut hat. Der Kunde ist beim Ombudsmann und will zur BaFin.\n\nIch reguliere heute. Aber: Wie viele Vertraege sind noch betroffen? Und warum konnte eine Ablehnung automatisch raus? Die Kompetenzordnung sagt, Ablehnungen nie automatisch.\n\nAylin"
    },
    {
      "id": "INT-00000807",
      "datum": "2025-04-16T14:40",
      "art": "interne E-Mail",
      "titel": "Re: Eskalation Fall Pieper",
      "von": "Jonas Pfister, MLOps",
      "an": "Aylin Demirci, Teamleiterin Schaden Haftpflicht Deutschland",
      "gruppen": [
        "intern"
      ],
      "kennungText": "interne E-Mail INT-00000807",
      "volltext": "Hi Aylin,\n\nich habe es gefunden. Im Migrationsmapping der Pilotwelle HP-2025-PILOT (Privathaftpflicht DE, seit 03.03. in MINT) wurde der HAPO-Bausteincode BST=01 (Tierhalter) nicht auf coverages gemappt, weil in HAPO die Rasse im Freitext ZUSATZ1 steht und der Parser das Feld als Bemerkung behandelt hat. Betroffen: 214 Vertraege mit BST=01 in der Pilotwelle, davon 11 mit Schaden seit Maerz, alle 11 automatisch abgelehnt (Pieper eingeschlossen) (Regel 'Tierhalter ohne Baustein' = Ablehnung).\n\nZur zweiten Frage: Die Regel war als 'Deckungspruefung negativ' konfiguriert und hat den Vier-Augen-Schritt nicht ausgeloest, weil sie als Konfigurationsregel und nicht als Modellentscheidung galt. Das habe ich im Review uebersehen. Heute Nachmittag: Regel deaktiviert, die 11 Faelle an dein Team, Nachmigration der 214 Vertraege bis Freitag. Das Mapping fuer die Hauptwelle am 15.05. korrigiere ich gleich mit.\n\nJonas",
      "wendepunkt": "Ursache gefunden, Regel deaktiviert"
    },
    {
      "id": "R08-v2.1",
      "datum": "2025-04-16",
      "art": "Regelwerk",
      "titel": "Kompetenzordnung R08 tritt in Version 2.1 in Kraft: Ablehnungen technisch nur noch mit Freigabe durch eine Person",
      "von": "",
      "an": "",
      "gruppen": [
        "intern"
      ],
      "kennungText": "Kompetenzordnung RW-GRUPPE-R08-2025, gültig ab",
      "volltext": ""
    },
    {
      "id": "INT-00000808",
      "datum": "2025-04-17",
      "art": "Brief",
      "titel": "Ihr Schaden SCH-00000810: Regulierung und Entschuldigung",
      "von": "Aylin Demirci, Teamleiterin Schaden Haftpflicht Deutschland",
      "an": "Hans-Georg Pieper",
      "gruppen": [
        "kunde",
        "schaden"
      ],
      "kennungText": "Brief INT-00000808",
      "volltext": "Sehr geehrter Herr Pieper,\n\nSie haben recht, und wir haben einen Fehler gemacht. Ihr Vertrag enthaelt seit dem 01.03.2019 den Baustein Tierhalterhaftpflicht. Bei der Uebernahme Ihres Vertrages in unser neues System im Maerz 2025 ist dieser Baustein nicht uebertragen worden. Unser Schadensystem hat deshalb Ihre Meldung automatisch abgelehnt. Das haette nicht passieren duerfen: Eine Ablehnung muss bei uns immer von einem Menschen geprueft werden.\n\nWir haben den Schaden heute reguliert: EUR 1.240,00 wurden an Herrn M. ueberwiesen (Arztkosten, Schmerzensgeld und Hose). Ein Selbstbehalt faellt nicht an. Fuer Ihren Aufwand und die Verzoegerung ueberweisen wir Ihnen zusaetzlich EUR 100,00 auf das uns bekannte Konto.\n\nIhr Vertrag ist korrigiert; der Baustein ist wieder im System sichtbar. Ich bitte Sie um Entschuldigung. Fuer Rueckfragen erreichen Sie mich direkt unter der unten stehenden Nummer.\n\nMit freundlichen Gruessen\nAylin Demirci\nTeamleiterin Schaden Haftpflicht Deutschland\n\n---",
      "wendepunkt": "Regulierung und Entschuldigung"
    },
    {
      "id": "SCH-00000810-03",
      "datum": "2025-04-17",
      "art": "Schadenposition",
      "titel": "Reserve wiedereröffnet, EUR 1'500.00",
      "von": "",
      "an": "",
      "gruppen": [
        "intern"
      ],
      "kennungText": "Schadenposition SCH-00000810-03",
      "volltext": ""
    },
    {
      "id": "SCH-00000810-04",
      "datum": "2025-04-17",
      "art": "Schadenposition",
      "titel": "Zahlung an den Geschädigten (Arztkosten, Schmerzensgeld, Hose), EUR 1'240.00, ohne Selbstbehalt",
      "von": "",
      "an": "Radfahrer (Geschädigter)",
      "gruppen": [
        "intern"
      ],
      "kennungText": "Schadenposition SCH-00000810-04",
      "volltext": ""
    },
    {
      "id": "SCH-00000810-05",
      "datum": "2025-04-17",
      "art": "Schadenposition",
      "titel": "Kulanzzahlung für Aufwand und Verzögerung, EUR 100.00",
      "von": "",
      "an": "Hans-Georg Pieper",
      "gruppen": [
        "intern"
      ],
      "kennungText": "Schadenposition SCH-00000810-05",
      "volltext": ""
    },
    {
      "id": "nachmigration",
      "datum": "2025-04-18",
      "art": "Memo",
      "titel": "Nachmigration der 214 betroffenen Verträge abgeschlossen",
      "von": "",
      "an": "",
      "gruppen": [
        "intern"
      ],
      "kennungText": "Root-Cause-Memo DOK-00000804, Massnahmen",
      "volltext": ""
    },
    {
      "id": "INT-00000809",
      "datum": "2025-04-24",
      "art": "Brief",
      "titel": "Versicherungsombudsmann e. V.: Beschwerde Pieper ./. Pfefferminzia, Az. O-2025-04-1187",
      "von": "Versicherungsombudsmann e. V.",
      "an": "Pfefferminzia",
      "gruppen": [
        "ombudsmann"
      ],
      "kennungText": "Brief INT-00000809",
      "volltext": "Sehr geehrte Damen und Herren,\n\nHerr Hans-Georg Pieper, Dresden, hat sich mit Schreiben vom 15.04.2025 an den Versicherungsombudsmann gewandt. Gegenstand ist die Ablehnung eines Haftpflichtschadens vom 21.03.2025 (Ihr Zeichen SCH-00000810) mit der Begruendung, der Vertrag enthalte keine Tierhalterdeckung, obwohl der Beschwerdefuehrer einen Nachtrag vom 15.02.2019 vorlegt.\n\nWir bitten um Stellungnahme innerhalb von drei Wochen, insbesondere zu folgenden Punkten: (1) Vertragsstand zum Schadenzeitpunkt, (2) Zustandekommen der Ablehnung, (3) ob die Ablehnung automatisiert erfolgte und ob eine Ueberpruefung durch eine natuerliche Person stattgefunden hat, (4) zwischenzeitliche Regulierung.\n\nMit freundlichen Gruessen\nVersicherungsombudsmann e. V., Referat Haftpflicht\n\n---"
    },
    {
      "id": "SCH-00000810-06",
      "datum": "2025-04-24",
      "art": "Schadenposition",
      "titel": "Schaden geschlossen, Reserve auf null",
      "von": "",
      "an": "",
      "gruppen": [
        "intern"
      ],
      "kennungText": "Schadenposition SCH-00000810-06",
      "volltext": ""
    },
    {
      "id": "DOK-00000804",
      "datum": "2025-05-06",
      "art": "Memo",
      "titel": "Root-Cause-Analyse Vorfall VF-2025-03: automatisierte Fehlablehnungen nach Pilotmigration Haftpflicht",
      "von": "Compliance DE, Data & AI Office",
      "an": "Geschäftsleitung, Modellrisiko-Komitee",
      "gruppen": [
        "intern"
      ],
      "kennungText": "Memo DOK-00000804",
      "volltext": "1. Sachverhalt\nZwischen 24.03. und 15.04.2025 hat das Schadensystem MINT (Triage v3) elf Haftpflichtschaeden mit Tierbezug automatisch abgelehnt, weil der Tierhalterbaustein im migrierten Vertragsstand fehlte. Ausloeser der Aufdeckung: Beschwerde des Kunden Pieper (SCH-00000810) mit Eskalation an den Versicherungsombudsmann und Ankuendigung einer BaFin-Beschwerde.\n\n2. Ursachen\na) Migrationsmapping der Pilotwelle HP-2025-PILOT (Privathaftpflicht DE, migriert am 03.03.2025): Der HAPO-Bausteincode BST=01 wurde nicht auf das Zielfeld coverages abgebildet, weil das Quellfeld ZUSATZ1 (Freitext, enthaelt Hunderasse) als Bemerkung klassifiziert wurde. Betroffen: 214 Vertraege. Das Mapping wurde vor der Hauptwelle Haftpflicht (15.05.2025) korrigiert.\nb) Konfiguration Triage v3: Die Regel 'Tierhalterschaden ohne Baustein' war als Deckungsregel mit Ergebnis 'Ablehnung' konfiguriert und umging den Vier-Augen-Schritt, der fuer Modellentscheidungen gilt. Der Review hat die Regel als reine Konfiguration behandelt.\nc) Prozess: Das Ablehnungsschreiben wurde ohne Sichtkontrolle versandt; die Eingangsbestaetigung der Beschwerde erfolgte fristgerecht, die inhaltliche Bearbeitung erst nach der zweiten Beschwerde (Frist von 15 Arbeitstagen ueberschritten).\n\n3. Massnahmen\n- Regel deaktiviert (16.04.), Nachmigration der 214 Vertraege (18.04.), elf Faelle wiedereroeffnet und reguliert (bis 25.04.).\n- Kompetenzordnung R08 Version 2.1: Jede ablehnende Entscheidung, gleich ob Modell oder Regel, erfordert eine Freigabe durch eine natuerliche Person; technisch erzwungen (Freigabe-Workflow).\n- Modellinventar: Eintrag Triage v3 mit Vorfall VF-2025-03, Konfigurationsregeln werden wie Modellentscheidungen behandelt.\n- Beschwerdeprozess: Beschwerden ueber automatisierte Entscheidungen werden mit Prioritaet 1 an die Beschwerdestelle geroutet.\n\n4. Bewertung\nKein Vermoegensschaden fuer Kunden nach Regulierung; Reputationsrisiko durch Ombudsmann- und Aufsichtskontakt; meldepflichtiger Vorfall im Sinne der KI-Governance-Richtlinie (Kategorie B). Bericht an das Technology & AI Committee erfolgt in der Sitzung vom 09.2025.\n\n---"
    },
    {
      "id": "INT-00000811",
      "datum": "2025-05-08",
      "art": "Brief",
      "titel": "Stellungnahme zur Beschwerde Az. O-2025-04-1187",
      "von": "Miriam Steinbrecher, Compliance Officer Deutschland",
      "an": "Versicherungsombudsmann e. V.",
      "gruppen": [
        "ombudsmann"
      ],
      "kennungText": "Brief INT-00000811",
      "volltext": "Sehr geehrte Damen und Herren,\n\nzu Ihrer Anfrage vom 24.04.2025 nehmen wir wie folgt Stellung:\n\n1. Vertragsstand: Der Vertrag VTR-00000801 (vormals 40.288.506-6) enthielt zum Schadenzeitpunkt den Baustein Tierhalterhaftpflicht (Nachtrag Nr. 2 vom 15.02.2019, wirksam 01.03.2019). Die Deckung bestand.\n2. Zustandekommen der Ablehnung: Bei der vorgezogenen Migration der Privathaftpflichtvertraege in unser neues Bestandssystem (Pilotwelle am 03.03.2025) wurde der Bausteincode aus dem Altsystem nicht uebernommen. Das Schadensystem prueft Deckungen gegen das neue Bestandssystem und kam deshalb zu einem falschen Ergebnis. Es handelt sich um einen Datenfehler, nicht um eine Ermessensentscheidung.\n3. Automatisierung: Die Ablehnung erfolgte automatisiert durch eine Konfigurationsregel unseres Schadensystems, ohne Ueberpruefung durch eine natuerliche Person. Das widerspricht unserer internen Kompetenzordnung, nach der ablehnende Entscheidungen stets durch Mitarbeitende zu treffen sind. Ursache war eine Fehlkonfiguration der Regel, die den vorgesehenen Vier-Augen-Schritt nicht ausloeste. Wir haben die Regel am 16.04.2025 deaktiviert, die Kompetenzordnung in Version 2.1 technisch abgesichert (Ablehnungen nur noch mit Freigabe) und alle 214 von demselben Migrationsfehler betroffenen Vertraege korrigiert. Zehn weitere Faelle mit gleicher Fehlablehnung wurden von Amts wegen wiedereroeffnet und reguliert.\n4. Regulierung: Der Schaden wurde am 17.04.2025 vollstaendig reguliert (EUR 1.240,00 an den Geschaedigten fuer Arztkosten, Schmerzensgeld und Kleidung), dem Beschwerdefuehrer wurde eine Kulanzzahlung von EUR 100,00 geleistet und eine schriftliche Entschuldigung uebermittelt.\n\nWir bedauern den Vorfall und betrachten die Beschwerde als berechtigt.\n\nMit freundlichen Gruessen\nMiriam Steinbrecher, Compliance Officer und Leiterin Beschwerdestelle Deutschland\n\n---"
    },
    {
      "id": "DOK-00000805",
      "datum": "2025-06-10",
      "art": "Aufsichtskorrespondenz",
      "titel": "Beschwerde eines Versicherungsnehmers, Az. VA 25-K 1187, Bitte um Stellungnahme",
      "von": "Bundesanstalt für Finanzdienstleistungsaufsicht",
      "an": "Pfefferminzia, Hauptbevollmächtigte",
      "gruppen": [
        "aufsicht"
      ],
      "kennungText": "Aufsichtskorrespondenz DOK-00000805",
      "volltext": "Sehr geehrte Damen und Herren,\n\nHerr Hans-Georg Pieper, Dresden, hat sich mit Schreiben vom 20.05.2025 an uns gewandt und beanstandet, dass ein Haftpflichtschaden durch ein automatisiertes Verfahren abgelehnt worden sei, obwohl Versicherungsschutz bestand. Wir bitten um Stellungnahme innerhalb von vier Wochen, insbesondere zu den organisatorischen Vorkehrungen, die eine Ueberpruefung automatisierter Entscheidungen durch natuerliche Personen sicherstellen, sowie zu Anzahl und Behandlung gleichartiger Faelle.\n\nDieses Schreiben ist eine vereinfachte, fiktive Darstellung fuer Lehrzwecke.\n\nMit freundlichen Gruessen\nReferat Verbraucherschutz Versicherungen\n\n---"
    },
    {
      "id": "INT-00000823",
      "datum": "2025-07-07",
      "art": "Brief",
      "titel": "Schriftliche Zusicherung: keine Computerentscheidung mehr",
      "von": "Hans-Georg Pieper",
      "an": "Aylin Demirci, Teamleiterin Schaden Haftpflicht Deutschland",
      "gruppen": [
        "kunde",
        "schaden"
      ],
      "kennungText": "Brief INT-00000823",
      "volltext": "Sehr geehrte Frau Demirci,\n\nIhr Brief vom 17. April und das Geld sind angekommen, dafuer danke ich Ihnen. Ich bleibe bei Ihnen versichert. Aber ich moechte es schriftlich haben, dass kein Computer mehr ueber meine Schaeden entscheidet. Bitte bestaetigen Sie mir das.\n\nHochachtungsvoll\nH.-G. Pieper\n\n---"
    },
    {
      "id": "INT-00000824",
      "datum": "2025-07-14",
      "art": "Brief",
      "titel": "Re: Schriftliche Zusicherung",
      "von": "Aylin Demirci, Teamleiterin Schaden Haftpflicht Deutschland",
      "an": "Hans-Georg Pieper",
      "gruppen": [
        "kunde",
        "schaden"
      ],
      "kennungText": "Brief INT-00000824",
      "volltext": "Sehr geehrter Herr Pieper,\n\ngerne bestaetige ich Ihnen: Ablehnungen von Schaeden werden bei uns ausschliesslich von Mitarbeitenden entschieden und seit April zusaetzlich technisch durch eine zweite Freigabe abgesichert. Unser System darf Schaeden nur dann selbststaendig bearbeiten, wenn es sie bezahlt, und auch das nur bis EUR 5.000 bei eindeutiger Deckung. Jede Ablehnung, jede Kuerzung und jede Kulanzentscheidung trifft ein Mensch.\n\nIch freue mich, dass Sie bei uns bleiben.\n\nMit freundlichen Gruessen\nAylin Demirci\n\n---"
    }
  ],
  "faktencheckRegel": "Jede Aussage mit Datum, Betrag, Zahl oder einem erledigten Zustand wird gegen Tabellen und Originaldokumente der Akte geprüft (nicht gegen die eigene Chronologie): belegt (grün, mit Quelle nachvollziehbar), vermutet (gelb, plausibel aber nicht in Stufe S nachzählbar oder nicht im Wortlaut vorliegend), nicht belegt (rot, widerspricht der Akte oder ist durch nichts gedeckt).",
  "faktencheck": [
    {
      "schreiben": "Kunde",
      "aussage": "Vertrag enthält seit dem 01.03.2019 den Baustein Tierhalterhaftpflicht.",
      "status": "gruen",
      "quelle": "Deckungstabelle, Baustein BS-TIER-HUND, gültig ab; Nachtrag DOK-00000801"
    },
    {
      "schreiben": "Kunde",
      "aussage": "Bei der Übernahme des Vertrags in das neue System im März 2025 wurde der Baustein nicht übertragen.",
      "status": "gruen",
      "quelle": "Migrationslog, Vorgang HP-2025-PILOT; interne E-Mail INT-00000807"
    },
    {
      "schreiben": "Kunde",
      "aussage": "Das Schadensystem hat die Meldung deshalb automatisch abgelehnt.",
      "status": "gruen",
      "quelle": "Brief INT-00000802; interne E-Mail INT-00000807"
    },
    {
      "schreiben": "Kunde",
      "aussage": "Eine Ablehnung muss bei uns immer von einem Menschen geprüft werden.",
      "status": "gelb",
      "quelle": "Kompetenzordnung RW-GRUPPE-R08-2025 – Grundsatz belegt (§ 5 Version 2.1, interne E-Mail INT-00000806), am Schadentag (24.03.2025) galt aber Version 2.0, deren Wortlaut nicht in der Akte vorliegt"
    },
    {
      "schreiben": "Kunde",
      "aussage": "Schaden am 17.04.2025 reguliert: EUR 1'240.00 an den Geschädigten.",
      "status": "gruen",
      "quelle": "Schadenposition SCH-00000810-04"
    },
    {
      "schreiben": "Kunde",
      "aussage": "Ein Selbstbehalt fällt nicht an.",
      "status": "gruen",
      "quelle": "Schadenposition SCH-00000810-04, Vermerk «ohne Selbstbehalt»"
    },
    {
      "schreiben": "Kunde",
      "aussage": "Zusätzlich EUR 100.00 Kulanz für Aufwand und Verzögerung.",
      "status": "gruen",
      "quelle": "Schadenposition SCH-00000810-05"
    },
    {
      "schreiben": "Kunde",
      "aussage": "Vertrag ist korrigiert, der Baustein ist wieder im System sichtbar.",
      "status": "gruen",
      "quelle": "Root-Cause-Memo DOK-00000804, Massnahme «Nachmigration der 214 Verträge (18.04.)»"
    },
    {
      "schreiben": "Ombudsmann",
      "aussage": "Vertrag enthielt zum Schadenzeitpunkt den Baustein Tierhalterhaftpflicht (Nachtrag Nr. 2 vom 15.02.2019, wirksam 01.03.2019).",
      "status": "gruen",
      "quelle": "Nachtrag DOK-00000801; Deckungstabelle"
    },
    {
      "schreiben": "Ombudsmann",
      "aussage": "Bausteincode wurde bei der Pilotmigration am 03.03.2025 nicht übernommen; Datenfehler, keine Ermessensentscheidung.",
      "status": "gruen",
      "quelle": "Migrationslog, Vorgang HP-2025-PILOT; interne E-Mail INT-00000807"
    },
    {
      "schreiben": "Ombudsmann",
      "aussage": "Ablehnung erfolgte automatisiert ohne Prüfung durch eine natürliche Person; widerspricht der internen Kompetenzordnung.",
      "status": "gelb",
      "quelle": "interne E-Mail INT-00000806/807 belegen den Grundsatz; der am 24.03.2025 geltende Wortlaut der Kompetenzordnung (Version 2.0) liegt nicht in der Akte vor, nur Version 2.1 (ab 16.04.2025)"
    },
    {
      "schreiben": "Ombudsmann",
      "aussage": "Regel am 16.04.2025 deaktiviert, Kompetenzordnung in Version 2.1 technisch abgesichert.",
      "status": "gruen",
      "quelle": "interne E-Mail INT-00000807; Kompetenzordnung RW-GRUPPE-R08-2025, gültig ab 16.04.2025"
    },
    {
      "schreiben": "Ombudsmann",
      "aussage": "Alle 214 vom selben Migrationsfehler betroffenen Verträge korrigiert.",
      "status": "gruen",
      "quelle": "Root-Cause-Memo DOK-00000804, Ursache a) und Massnahmen"
    },
    {
      "schreiben": "Ombudsmann",
      "aussage": "Zehn weitere Fälle mit gleicher Fehlablehnung von Amts wegen wiedereröffnet und reguliert.",
      "status": "gelb",
      "quelle": "Root-Cause-Memo DOK-00000804 nennt elf automatisch abgelehnte Fälle insgesamt (Pieper eingeschlossen, also zehn weitere); Einzelfälle und deren Regulierung sind unternehmensweite Zahlen, im Datensatz Stufe S nicht nachzählbar"
    },
    {
      "schreiben": "Ombudsmann",
      "aussage": "Schaden am 17.04.2025 vollständig reguliert, EUR 1'240.00 an den Geschädigten, EUR 100.00 Kulanz, schriftliche Entschuldigung.",
      "status": "gruen",
      "quelle": "Schadenposition SCH-00000810-04/05; Brief INT-00000808"
    }
  ],
  "schreibenAntwortKunde": "Entwurf, Stand 17.04.2025, zur Unterschrift durch Aylin Demirci, Teamleiterin Schaden Haftpflicht Deutschland.\n\nPfefferminzia Versicherung AG\nNiederlassung Deutschland\nSchaden Haftpflicht\n\nHerrn\nHans-Georg Pieper\nErlensteig 27\n01309 Dresden\n\n17. April 2025\n\nIhr Schaden SCH-00000810: Regulierung, Korrektur und Entschuldigung\n\nSehr geehrter Herr Pieper,\n\nvielen Dank für Ihre Schreiben vom 28. März und vom 15. April 2025 – und: Sie haben recht, und wir haben einen Fehler gemacht.\n\nDen Grund haben wir inzwischen gefunden: Als wir Ihren Vertrag im März 2025 in unser neues Bestandssystem übernommen haben, ist der Baustein Tierhalterhaftpflicht, den Sie seit dem 1. März 2019 bei uns haben, dabei leider verloren gegangen. Weil unser System Ihren Vertrag deshalb ohne diesen Baustein sah, hat es Ihre Schadenmeldung am 24. März 2025 selbständig abgelehnt – kein Mitarbeiter hat sich das vorher angesehen. Genau das darf nicht passieren: Eine Ablehnung gehört in Menschenhand, nicht in die eines Programms.\n\nWir schulden Ihnen zudem eine zweite Entschuldigung: Nach Ihrer ersten Beschwerde haben Sie am 2. April 2025 nur eine Zwischennachricht bekommen; die darin zugesagte inhaltliche Antwort binnen 15 Arbeitstagen haben wir Ihnen nicht gegeben. Erst Ihr zweites Schreiben hat die Sache tatsächlich ins Rollen gebracht, und das ist nicht in Ordnung.\n\nWir haben den Fall heute, am 17. April 2025, abschließend bearbeitet: An Herrn M. gehen EUR 1.240,00 für die Arztkosten, das Schmerzensgeld und die beschädigte Hose, ohne dass wir dabei einen Selbstbehalt abziehen. Für die Umstände und die verlorene Zeit erhalten Sie zusätzlich eine Kulanzzahlung von EUR 100,00 auf Ihr uns bekanntes Konto.\n\nIhr Vertrag zeigt den Baustein jetzt wieder korrekt, und wir haben unsere Abläufe angepasst: Eine Ablehnung kann unser System ab sofort nicht mehr allein aussprechen, das trifft bei uns von nun an ausnahmslos ein Mensch.\n\nWenn Sie Fragen haben, erreichen Sie mich direkt unter [Telefon prüfen].\n\nMit freundlichen Grüßen\n\nAylin Demirci\nTeamleiterin Schaden Haftpflicht Deutschland\n",
  "schreibenStellungnahme": "Entwurf, Stand 08.05.2025, zur Freigabe durch die Compliance.\n\nPfefferminzia Versicherung AG\nNiederlassung Deutschland\nCompliance\n\nVersicherungsombudsmann e. V.\nPostfach 08 06 32\n10006 Berlin\n\n8. Mai 2025\n\nStellungnahme zur Beschwerde Pieper ./. Pfefferminzia, Az. O-2025-04-1187 (unser Zeichen SCH-00000810)\n\nSehr geehrte Damen und Herren,\n\nzu Ihrer Anfrage vom 24. April 2025 nehmen wir zu den vier Punkten wie folgt Stellung.\n\nZum Vertragsstand: Der Vertrag VTR-00000801 (vormals Policennummer 40.288.506-6) führte den Baustein Tierhalterhaftpflicht bereits seit dem 1. März 2019, ausgestellt mit Nachtrag Nr. 2 vom 15. Februar 2019. Zum Zeitpunkt des Schadens am 21. März 2025 bestand demnach Versicherungsschutz.\n\nZum Zustandekommen der Ablehnung: Ursache ist ein Datenfehler bei der Migration. Als wir die Privathaftpflichtverträge am 3. März 2025 in einer ersten Welle in unser neues Bestandssystem überführt haben, ist der Code für den Tierhalterbaustein aus dem Altsystem nicht mitgekommen. Weil unser Schadensystem die Deckung gegen den neuen, unvollständigen Vertragsstand geprüft hat, kam es zu einem falschen Ergebnis – kein bewusstes Ermessen, sondern ein technischer Fehler bei der Übernahme.\n\nZur Automatisierung: Eine hinterlegte Regel unseres Schadensystems hat die Ablehnung selbständig ausgesprochen, ohne dass zuvor ein Mensch daraufgeschaut hat. Das steht im Widerspruch zu unserer eigenen Kompetenzordnung, wonach ablehnende Entscheidungen ausschließlich von Mitarbeitenden getroffen werden dürfen; die Regel war fehlerhaft eingerichtet und hat die dafür vorgesehene Zweitprüfung nicht ausgelöst. Wir haben sie am 16. April 2025 abgeschaltet und die Kompetenzordnung mit Version 2.1 so verschärft, dass eine Ablehnung technisch erst nach Freigabe durch eine Person entsteht. Im gleichen Zug haben wir sämtliche 214 Verträge, die vom selben Migrationsfehler betroffen waren, bis zum 18. April 2025 korrigiert und die zehn weiteren automatisch abgelehnten Schadenfälle von uns aus wiedereröffnet und reguliert.\n\nZur ersten Beschwerde vom 28. März 2025 räumen wir zudem ein: Die Eingangsbestätigung ging fristgerecht am 2. April 2025 heraus, die darin zugesagte inhaltliche Antwort innerhalb von 15 Arbeitstagen haben wir jedoch nicht gegeben. Erst nach der zweiten Beschwerde vom 15. April 2025 wurde der Fall mit Priorität bearbeitet.\n\nZur Regulierung: Am 17. April 2025 war der Fall abgeschlossen. Der Geschädigte erhielt EUR 1.240,00 für Arztkosten, Schmerzensgeld und die beschädigte Hose, Herr Pieper zusätzlich EUR 100,00 Kulanz sowie ein schriftliches Entschuldigungsschreiben.\n\nAls weitere Massnahme haben wir den Vorfall in unserem Modell- und Regelinventar dokumentiert und unseren Beschwerdeprozess so angepasst, dass Beschwerden über automatisierte Entscheidungen künftig mit höchster Priorität bearbeitet werden.\n\nDer Vorfall tut uns leid, wir halten die Beschwerde für begründet.\n\nMit freundlichen Grüßen\n\nMiriam Steinbrecher\nCompliance Officer Deutschland\n"
};
