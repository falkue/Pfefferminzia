const AKTE_DATEN = {
  "kopfzeile": {
    "kunde": "Hans-Georg Pieper",
    "vertrag": "VTR-00000801 · Privathaftpflicht Deutschland, seit 2013-01-01",
    "versicherungsschein": "vormals 40.288.506-6 (HAPO), migriert nach MINT am 2025-03-03",
    "schaden": "SCH-00000810 (Anzeige S2025/001002) · Hundebiss vom 2025-03-21, Status geschlossen"
  },
  "kacheln": [
    {
      "titel": "Schadentag",
      "wert": "2025-03-21",
      "definition": "Tag des Schadenereignisses laut Schadentabelle."
    },
    {
      "titel": "Tage bis zur Zahlung",
      "wert": "27",
      "definition": "Kalendertage vom Schadentag (2025-03-21) bis zur Regulierungszahlung an den Geschädigten (2025-04-17)."
    },
    {
      "titel": "Bezahlter Betrag",
      "wert": "EUR 1'340.00",
      "definition": "Summe aller Zahlungen aus der Schadentabelle: Regulierung an den Geschädigten und Kulanz an den Versicherungsnehmer."
    },
    {
      "titel": "Zahl der Dokumente",
      "wert": "17",
      "definition": "Dokumente (5) und Kontakte einschliesslich E-Mails (12) der Fallakte zusammen."
    }
  ],
  "gruppenNamen": {
    "kunde": "Kunde",
    "schaden": "Schadenabteilung",
    "intern": "intern und IT",
    "ombudsmann": "Ombudsmann",
    "aufsicht": "Aufsicht"
  },
  "gruppenReihenfolge": [
    "kunde",
    "schaden",
    "intern",
    "ombudsmann",
    "aufsicht"
  ],
  "kennzahlAblehnungZahlung": {
    "tage": 24,
    "ablehnungDatum": "2025-03-24",
    "zahlungDatum": "2025-04-17",
    "definition": "Kalendertage von der automatisierten Ablehnung (Interaktion INT-00000802) bis zur Regulierungszahlung an den Geschädigten (Schadenposition 04)."
  },
  "ereignisse": [
    {
      "id": "EV-01",
      "datum": "2012-11-13",
      "art": "Tabellenereignis",
      "titel": "Antrag Privathaftpflicht eingereicht",
      "gruppen": [
        "kunde"
      ],
      "senderGruppe": "kunde",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "Antragstabelle",
      "text": [
        "Antrag auf eine Privathaftpflichtversicherung eingereicht, Vertriebsweg Agentur (Generalagentur Elbland Petrov, Dresden)."
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-02",
      "datum": "2012-11-28",
      "art": "Tabellenereignis",
      "titel": "Antrag angenommen",
      "gruppen": [
        "kunde"
      ],
      "senderGruppe": "kunde",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "Antragstabelle",
      "text": [
        "Antrag angenommen: normale Annahme ohne Zuschlag, nicht automatisiert entschieden."
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-03",
      "datum": "2013-01-01",
      "art": "Tabellenereignis",
      "titel": "Vertragsbeginn Privathaftpflicht",
      "gruppen": [
        "kunde"
      ],
      "senderGruppe": "kunde",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "Vertragstabelle",
      "text": [
        "Vertrag VTR-00000801 beginnt (damalige Policennummer 40.288.506-6 im Altsystem HAPO). Versicherungssumme EUR 5'000'000' Jahresprämie brutto EUR 131.40."
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-04",
      "datum": "2019-02-12",
      "art": "Dokument",
      "titel": "Beratung zum Einschluss Tierhalterbaustein",
      "gruppen": [
        "kunde"
      ],
      "senderGruppe": "kunde",
      "absender": "Agentur Dresden",
      "empfaenger": "Hans-Georg Pieper",
      "kennung": "DOK-00000802",
      "quelle": null,
      "text": [
        "Anlass: Kunde hat Hund aus dem Tierheim uebernommen (Schaeferhund-Mischling, ca. 3 Jahre).\nWunsch: Absicherung fuer Schaeden durch den Hund.\nEmpfehlung: Einschluss Tierhalterbaustein in bestehende Privathaftpflicht (guenstiger als Einzelpolice). Hinweis auf Listenhunde-Regelung: nicht betroffen.\nEntscheid: Einschluss ab 01.03.2019, Zuschlag EUR 56,50 jaehrlich inkl. VersSt.\nKunde wuenscht Post per Brief, keine E-Mail.\nUnterschrift Kunde / Vermittler 12.02.2019"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-05",
      "datum": "2019-02-15",
      "art": "Dokument",
      "titel": "Nachtrag Nr. 2: Einschluss Tierhalterhaftpflicht, wirksam 01.03.2019",
      "gruppen": [
        "kunde"
      ],
      "senderGruppe": "kunde",
      "absender": "Pfefferminz Versicherung AG, Niederlassung Deutschland",
      "empfaenger": "Hans-Georg Pieper",
      "kennung": "DOK-00000801",
      "quelle": null,
      "text": [
        "Aenderungsgrund: Einschluss Baustein Tierhalterhaftpflicht (Hund)",
        "Baustein Tierhalter — bisher: nicht versichert; neu: eingeschlossen, 1 Hund (Schaeferhund-Mischling 'Rex', kein Listenhund)",
        "Deckungssumme Tierhalter — bisher: -; neu: innerhalb Deckungssumme EUR 5 Mio.",
        "Jahresbeitrag brutto — bisher: EUR 74,90; neu: EUR 131,40 (Zuschlag Hund EUR 56,50 inkl. Versicherungsteuer)",
        "Hinweis: In Sachsen besteht keine allgemeine Hundehalterhaftpflicht-Pflicht (vereinfachte Darstellung). Die uebrigen Bestimmungen bleiben unveraendert. Bedingungsgeneration HP-MODERN.",
        "Agentur Dresden, 15.02.2019"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-06",
      "datum": "2025-03-03",
      "art": "Tabellenereignis",
      "titel": "Migration nach MINT (Pilotwelle Privathaftpflicht Deutschland)",
      "gruppen": [
        "intern"
      ],
      "senderGruppe": "intern",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "Migrationslog",
      "text": [
        "Bausteincode Tierhalter (BST=01) wird beim Mapping nicht ins Zielschema übernommen, Feld bleibt leer. Warnung im Migrationslog: „Bausteincode BST=01 (Tierhalter) nicht ins Zielschema uebernommen, Feld leer; Baustein am 17.04.2025 manuell nachgetragen, nachmigriert 18.04.2025 (VF-2025-03)“"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-08",
      "datum": "2025-03-21",
      "art": "Tabellenereignis",
      "titel": "Erstreserve gebildet",
      "gruppen": [
        "schaden"
      ],
      "senderGruppe": "schaden",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "Schadenposition 01",
      "text": [
        "Reserve EUR 1500.00: Erstreserve automatisch"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-09",
      "datum": "2025-03-21",
      "art": "Dokument",
      "titel": "Notfallbehandlung des Geschädigten, Arztrechnung",
      "gruppen": [
        "kunde"
      ],
      "senderGruppe": "kunde",
      "absender": "Universitaetsklinikum Dresden, Notaufnahme",
      "empfaenger": "Radfahrer (Geschaedigter)",
      "kennung": "DOK-00000803",
      "quelle": null,
      "text": [
        "Patient: Herr M., Dresden. Behandlungsdatum 21.03.2025.\nDiagnose: Bissverletzung rechte Wade (S81.8), oberflaechlich, Wundreinigung, Tetanus-Auffrischung, Antibiotikaprophylaxe.",
        "Notfallpauschale                 EUR 210,00\nWundversorgung                    EUR 145,00\nImpfung und Medikamente           EUR 85,00\nGesamt                            EUR 440,00",
        "Zahlbar durch den Patienten; Weiterberechnung an den Tierhalter vorbehalten."
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-07",
      "datum": "2025-03-21T16:35",
      "art": "Telefonnotiz",
      "titel": "Schadenmeldung Hundebiss",
      "gruppen": [
        "kunde",
        "schaden"
      ],
      "senderGruppe": "kunde",
      "absender": "Hans-Georg Pieper",
      "empfaenger": "Contact Center Leipzig",
      "kennung": "INT-00000801",
      "quelle": null,
      "text": [
        "Tel. VN Pieper, Contact Center Leipzig (Aushilfe), 7 Min. Stichworte: Hund, Biss, Radfahrer, Leine ja, Wade, Notaufnahme Uniklinik, Hose kaputt. Geschaedigter: Herr M., Dresden, Kontaktdaten aufgenommen. VN sagt 'Hund ist doch bei euch versichert, seit 2019'. Erfasst in MINT als Schaden SCH-00000810, Kategorie Tierhalter."
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-10",
      "datum": "2025-03-24",
      "art": "Tabellenereignis",
      "titel": "Reserve aufgelöst, automatische Ablehnung",
      "gruppen": [
        "schaden"
      ],
      "senderGruppe": "schaden",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "Schadenposition 02",
      "text": [
        "Reserve auf EUR 0.00: Reserve aufgeloest: automatische Ablehnung 'kein Tierhalterbaustein' (MINT Triage v3)"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-11",
      "datum": "2025-03-24",
      "art": "Brief",
      "titel": "Ablehnung des Schadens (automatisch)",
      "gruppen": [
        "schaden",
        "kunde"
      ],
      "senderGruppe": "schaden",
      "absender": "Pfefferminzia Versicherung AG, Niederlassung Deutschland, Schaden Haftpflicht (maschinell erstellt, ohne Unterschrift)",
      "empfaenger": "Hans-Georg Pieper",
      "kennung": "INT-00000802",
      "quelle": null,
      "text": [
        "Sehr geehrter Herr Pieper,",
        "Sie haben uns einen Schaden vom 21.03.2025 gemeldet, den Ihr Hund verursacht hat. Nach Pruefung Ihres Vertrages VTR-00000801 muessen wir Ihnen mitteilen, dass Schaeden durch Tiere nur versichert sind, wenn der Baustein Tierhalterhaftpflicht eingeschlossen ist. Ihr Vertrag enthaelt diesen Baustein nicht. Wir koennen den Schaden daher nicht uebernehmen (AHB 2013 Ziffer 7.4 in Verbindung mit BBR 2015).",
        "Sollten Sie mit dieser Entscheidung nicht einverstanden sein, koennen Sie sich an den Versicherungsombudsmann e. V. wenden.",
        "Mit freundlichen Gruessen\nPfefferminzia Versicherung AG, Niederlassung Deutschland\nSchaden Haftpflicht",
        "Dieses Schreiben wurde maschinell erstellt und ist ohne Unterschrift gueltig."
      ],
      "wendepunkt": {
        "nr": 1,
        "bezeichnung": "Wendepunkt 1: Fehler wird wirksam"
      }
    },
    {
      "id": "EV-12",
      "datum": "2025-03-28",
      "art": "Brief",
      "titel": "Erste Beschwerde: Ablehnung unberechtigt",
      "gruppen": [
        "kunde",
        "schaden"
      ],
      "senderGruppe": "kunde",
      "absender": "Hans-Georg Pieper",
      "empfaenger": "Aylin Demirci, Teamleiterin Schaden Haftpflicht DE",
      "kennung": "INT-00000803",
      "quelle": null,
      "text": [
        "Dresden, den 28. Maerz 2025",
        "BESCHWERDE – SCHADEN NR. SCH-00000810 – ABLEHNUNG UNBERECHTIGT",
        "Sehr geehrte Damen und Herren,",
        "Ihr Schreiben vom 24.03.2025 habe ich erhalten. Sie behaupten, mein Vertrag enthalte keinen Tierhalterbaustein. DAS IST FALSCH. Ich habe den Baustein seit dem 1. Maerz 2019 in meinem Vertrag, damals bei Ihrer Agentur in Dresden abgeschlossen. Ich habe das Beratungsprotokoll und den Nachtrag Nr. 2 hier vor mir liegen, mit Unterschrift Ihres Vertreters. Seit 2019 bezahle ich dafuer jedes Jahr 56,50 Euro mehr.",
        "Es ist mein gutes Recht, dass Sie den Schaden meines Nachbarn bezahlen. Herr M. hat mir gesagt, er wartet noch bis Mitte April, dann geht er zum Anwalt.",
        "Ich fordere Sie auf, den Schaden binnen 14 Tagen zu regulieren und mir schriftlich zu erklaeren, wer diesen Brief geschrieben hat. Ein Computer kann mir nicht meinen Vertrag absprechen. Sollten Sie nicht reagieren, wende ich mich an die Saechsische Zeitung und an den Ombudsmann.",
        "Hochachtungsvoll\nH.-G. Pieper",
        "Anlagen: Kopie Nachtrag Nr. 2 vom 15.02.2019, Kopie Beratungsprotokoll"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-13",
      "datum": "2025-04-02T11:20",
      "art": "E-Mail",
      "titel": "Eingangsbestätigung der Beschwerde",
      "gruppen": [
        "schaden",
        "kunde"
      ],
      "senderGruppe": "schaden",
      "absender": "Pfefferminzia, Kundenservice Leipzig",
      "empfaenger": "Hans-Georg Pieper",
      "kennung": "INT-00000804",
      "quelle": null,
      "text": [
        "Sehr geehrter Herr Pieper,",
        "vielen Dank fuer Ihr Schreiben vom 28.03.2025. Ihr Anliegen wird geprueft. Wir melden uns innerhalb von 15 Arbeitstagen bei Ihnen.",
        "Mit freundlichen Gruessen\nKundenservice Leipzig"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-14",
      "datum": "2025-04-15",
      "art": "Brief",
      "titel": "Zweite Beschwerde: Ombudsmann und BaFin angekündigt",
      "gruppen": [
        "kunde",
        "intern"
      ],
      "senderGruppe": "kunde",
      "absender": "Hans-Georg Pieper",
      "empfaenger": "Miriam Steinbrecher, Compliance Officer DE und AI Compliance Officer Gruppe",
      "kennung": "INT-00000805",
      "quelle": null,
      "text": [
        "Dresden, den 15. April 2025",
        "ZWEITE BESCHWERDE – SCHADEN NR. SCH-00000810",
        "Sehr geehrte Damen und Herren,",
        "auf meine Beschwerde vom 28.03. habe ich eine Standardmail bekommen, in der steht, mein Anliegen werde geprueft. Seither: NICHTS. Herr M. war gestern bei mir und hat mir die Anwaltskarte gezeigt.",
        "Ich habe mich heute schriftlich an den Versicherungsombudsmann e. V. in Berlin gewandt (Kopie anbei). Ich werde mich ausserdem bei der Bundesanstalt fuer Finanzdienstleistungsaufsicht beschweren, weil Sie einen Vertrag, den ich seit sechs Jahren bezahle, per Computer fuer nicht existent erklaeren. Sie haben das schriftlich.",
        "Hochachtungsvoll\nH.-G. Pieper"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-15",
      "datum": "2025-04-16T09:05",
      "art": "E-Mail",
      "titel": "Interne Eskalation: automatische Ablehnung trotz Baustein",
      "gruppen": [
        "schaden",
        "intern"
      ],
      "senderGruppe": "schaden",
      "absender": "Aylin Demirci, Teamleiterin Schaden Haftpflicht DE",
      "empfaenger": "Jonas Pfister, ML Engineer und Lead MLOps, Miriam Steinbrecher, Compliance Officer DE und AI Compliance Officer Gruppe (Cc Martina Jost)",
      "kennung": "INT-00000806",
      "quelle": null,
      "text": [
        "An: Jonas Pfister (MLOps), Miriam Steinbrecher (Compliance DE); Cc: Martina Jost",
        "Hallo zusammen,",
        "wir haben ein Problem. Der Kunde Pieper (VTR-00000801) hat seit 2019 den Baustein Tierhalter, das sehe ich in HAPO (ZUSATZ1 = 'HUND', BST=01). In MINT ist das Feld coverages nach der Migration leer. Die Triage v3 hat den Schaden am 24.03. automatisch abgelehnt und das Ablehnungsschreiben ist rausgegangen, ohne dass jemand draufgeschaut hat. Der Kunde ist beim Ombudsmann und will zur BaFin.",
        "Ich reguliere heute. Aber: Wie viele Vertraege sind noch betroffen? Und warum konnte eine Ablehnung automatisch raus? Die Kompetenzordnung sagt, Ablehnungen nie automatisch.",
        "Aylin"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-16",
      "datum": "2025-04-16T14:40",
      "art": "E-Mail",
      "titel": "Ursache gefunden: Migrationsmapping und Vier-Augen-Lücke",
      "gruppen": [
        "intern",
        "schaden"
      ],
      "senderGruppe": "intern",
      "absender": "Jonas Pfister, ML Engineer und Lead MLOps",
      "empfaenger": "Aylin Demirci, Teamleiterin Schaden Haftpflicht DE",
      "kennung": "INT-00000807",
      "quelle": null,
      "text": [
        "Hi Aylin,",
        "ich habe es gefunden. Im Migrationsmapping der Pilotwelle HP-2025-PILOT (Privathaftpflicht DE, seit 03.03. in MINT) wurde der HAPO-Bausteincode BST=01 (Tierhalter) nicht auf coverages gemappt, weil in HAPO die Rasse im Freitext ZUSATZ1 steht und der Parser das Feld als Bemerkung behandelt hat. Betroffen: 214 Vertraege mit BST=01 in der Pilotwelle, davon 11 mit Schaden seit Maerz, alle 11 automatisch abgelehnt (Pieper eingeschlossen) (Regel 'Tierhalter ohne Baustein' = Ablehnung).",
        "Zur zweiten Frage: Die Regel war als 'Deckungspruefung negativ' konfiguriert und hat den Vier-Augen-Schritt nicht ausgeloest, weil sie als Konfigurationsregel und nicht als Modellentscheidung galt. Das habe ich im Review uebersehen. Heute Nachmittag: Regel deaktiviert, die 11 Faelle an dein Team, Nachmigration der 214 Vertraege bis Freitag. Das Mapping fuer die Hauptwelle am 15.05. korrigiere ich gleich mit.",
        "Jonas"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-17",
      "datum": "2025-04-17",
      "art": "Tabellenereignis",
      "titel": "Baustein Tierhalter manuell nachgetragen",
      "gruppen": [
        "intern"
      ],
      "senderGruppe": "intern",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "Migrationslog",
      "text": [
        "Baustein am 17.04.2025 manuell im Vertrag nachgetragen, nachmigriert am 18.04.2025."
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-18",
      "datum": "2025-04-17",
      "art": "Tabellenereignis",
      "titel": "Reserve wiedereröffnet",
      "gruppen": [
        "schaden"
      ],
      "senderGruppe": "schaden",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "Schadenposition 03",
      "text": [
        "Reserve EUR 1500.00: Wiedereroeffnung nach Beschwerde, Baustein in HAPO nachgewiesen"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-19",
      "datum": "2025-04-17",
      "art": "Tabellenereignis",
      "titel": "Regulierungszahlung an den Geschädigten",
      "gruppen": [
        "schaden"
      ],
      "senderGruppe": "schaden",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "Schadenposition 04",
      "text": [
        "Zahlung EUR 1240.00 an Radfahrer: Arztkosten 440, Schmerzensgeld 700, Radhose 100; ohne Selbstbehalt (Selbstbehalt EUR 150 der Hauptdeckung aus Kulanz erlassen)"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-20",
      "datum": "2025-04-17",
      "art": "Tabellenereignis",
      "titel": "Kulanzzahlung an den Versicherungsnehmer",
      "gruppen": [
        "schaden",
        "kunde"
      ],
      "senderGruppe": "schaden",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "Schadenposition 05",
      "text": [
        "Zahlung EUR 100.00 an Versicherungsnehmer: Kulanz fuer Aufwand und Verzoegerung"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-21",
      "datum": "2025-04-17",
      "art": "Brief",
      "titel": "Regulierung und Entschuldigung",
      "gruppen": [
        "schaden",
        "kunde"
      ],
      "senderGruppe": "schaden",
      "absender": "Aylin Demirci, Teamleiterin Schaden Haftpflicht DE",
      "empfaenger": "Hans-Georg Pieper",
      "kennung": "INT-00000808",
      "quelle": null,
      "text": [
        "Sehr geehrter Herr Pieper,",
        "Sie haben recht, und wir haben einen Fehler gemacht. Ihr Vertrag enthaelt seit dem 01.03.2019 den Baustein Tierhalterhaftpflicht. Bei der Uebernahme Ihres Vertrages in unser neues System im Maerz 2025 ist dieser Baustein nicht uebertragen worden. Unser Schadensystem hat deshalb Ihre Meldung automatisch abgelehnt. Das haette nicht passieren duerfen: Eine Ablehnung muss bei uns immer von einem Menschen geprueft werden.",
        "Wir haben den Schaden heute reguliert: EUR 1.240,00 wurden an Herrn M. ueberwiesen (Arztkosten, Schmerzensgeld und Hose). Den Selbstbehalt von EUR 150,00 aus Ihrem Vertrag ziehen wir nicht ab. Fuer Ihren Aufwand und die Verzoegerung ueberweisen wir Ihnen zusaetzlich EUR 100,00 auf das uns bekannte Konto.",
        "Ihr Vertrag ist korrigiert; der Baustein ist wieder im System sichtbar. Ich bitte Sie um Entschuldigung. Fuer Rueckfragen erreichen Sie mich direkt unter der unten stehenden Nummer.",
        "Mit freundlichen Gruessen\nAylin Demirci\nTeamleiterin Schaden Haftpflicht Deutschland"
      ],
      "wendepunkt": {
        "nr": 2,
        "bezeichnung": "Wendepunkt 2: Fehler korrigiert"
      }
    },
    {
      "id": "EV-22",
      "datum": "2025-04-18",
      "art": "Tabellenereignis",
      "titel": "Nachmigration der betroffenen Verträge",
      "gruppen": [
        "intern"
      ],
      "senderGruppe": "intern",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "Migrationslog",
      "text": [
        "Nachmigration der 214 von demselben Migrationsfehler betroffenen Verträge der Pilotwelle (unternehmensweit)."
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-23",
      "datum": "2025-04-24",
      "art": "Tabellenereignis",
      "titel": "Schaden geschlossen",
      "gruppen": [
        "schaden"
      ],
      "senderGruppe": "schaden",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "Schadenposition 06",
      "text": [
        "Reserve auf EUR 0.00, Schaden geschlossen."
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-24",
      "datum": "2025-04-24",
      "art": "Brief",
      "titel": "Anfrage des Versicherungsombudsmanns",
      "gruppen": [
        "ombudsmann",
        "intern"
      ],
      "senderGruppe": "ombudsmann",
      "absender": "Versicherungsombudsmann e. V., Referat Haftpflicht",
      "empfaenger": "Miriam Steinbrecher, Compliance Officer DE und AI Compliance Officer Gruppe, Beschwerdestelle Deutschland",
      "kennung": "INT-00000809",
      "quelle": null,
      "text": [
        "Sehr geehrte Damen und Herren,",
        "Herr Hans-Georg Pieper, Dresden, hat sich mit Schreiben vom 15.04.2025 an den Versicherungsombudsmann gewandt. Gegenstand ist die Ablehnung eines Haftpflichtschadens vom 21.03.2025 (Ihr Zeichen SCH-00000810) mit der Begruendung, der Vertrag enthalte keine Tierhalterdeckung, obwohl der Beschwerdefuehrer einen Nachtrag vom 15.02.2019 vorlegt.",
        "Wir bitten um Stellungnahme innerhalb von drei Wochen, insbesondere zu folgenden Punkten: (1) Vertragsstand zum Schadenzeitpunkt, (2) Zustandekommen der Ablehnung, (3) ob die Ablehnung automatisiert erfolgte und ob eine Ueberpruefung durch eine natuerliche Person stattgefunden hat, (4) zwischenzeitliche Regulierung.",
        "Mit freundlichen Gruessen\nVersicherungsombudsmann e. V., Referat Haftpflicht"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-25",
      "datum": "2025-05-06",
      "art": "Dokument",
      "titel": "Root-Cause-Analyse Vorfall VF-2025-03",
      "gruppen": [
        "intern"
      ],
      "senderGruppe": "intern",
      "absender": "Compliance DE (M. Steinbrecher), Data & AI Office (J. Pfister)",
      "empfaenger": "Geschaeftsleitung, Modellrisiko-Komitee",
      "kennung": "DOK-00000804",
      "quelle": null,
      "text": [
        "1. Sachverhalt\nZwischen 24.03. und 15.04.2025 hat das Schadensystem MINT (Triage v3) elf Haftpflichtschaeden mit Tierbezug automatisch abgelehnt, weil der Tierhalterbaustein im migrierten Vertragsstand fehlte. Ausloeser der Aufdeckung: Beschwerde des Kunden Pieper (SCH-00000810) mit Eskalation an den Versicherungsombudsmann und Ankuendigung einer BaFin-Beschwerde.",
        "2. Ursachen\na) Migrationsmapping der Pilotwelle HP-2025-PILOT (Privathaftpflicht DE, migriert am 03.03.2025): Der HAPO-Bausteincode BST=01 wurde nicht auf das Zielfeld coverages abgebildet, weil das Quellfeld ZUSATZ1 (Freitext, enthaelt Hunderasse) als Bemerkung klassifiziert wurde. Betroffen: 214 Vertraege. Das Mapping wurde vor der Hauptwelle Haftpflicht (15.05.2025) korrigiert.\nb) Konfiguration Triage v3: Die Regel 'Tierhalterschaden ohne Baustein' war als Deckungsregel mit Ergebnis 'Ablehnung' konfiguriert und umging den Vier-Augen-Schritt, der fuer Modellentscheidungen gilt. Der Review hat die Regel als reine Konfiguration behandelt.\nc) Prozess: Das Ablehnungsschreiben wurde ohne Sichtkontrolle versandt; die Eingangsbestaetigung der Beschwerde erfolgte fristgerecht, die inhaltliche Bearbeitung erst nach der zweiten Beschwerde, nach Ablauf der vom Kunden gesetzten Frist von 14 Tagen.",
        "3. Massnahmen\n- Regel deaktiviert (16.04.), Baustein im Vertrag Pieper manuell nachgetragen (17.04.), Nachmigration der 214 Vertraege (18.04.), elf Faelle wiedereroeffnet und reguliert (bis 25.04.).\n- Kompetenzordnung R08 Version 2.1: Jede ablehnende Entscheidung, gleich ob Modell oder Regel, erfordert eine Freigabe durch eine natuerliche Person; technisch erzwungen (Freigabe-Workflow).\n- Modellinventar: Eintrag Triage v3 mit Vorfall VF-2025-03, Konfigurationsregeln werden wie Modellentscheidungen behandelt.\n- Beschwerdeprozess: Beschwerden ueber automatisierte Entscheidungen werden mit Prioritaet 1 an die Beschwerdestelle geroutet.",
        "4. Bewertung\nKein Vermoegensschaden fuer Kunden nach Regulierung; Reputationsrisiko durch Ombudsmann- und Aufsichtskontakt; meldepflichtiger Vorfall im Sinne der KI-Governance-Richtlinie (Kategorie B). Bericht an das Technology & AI Committee erfolgt in der Sitzung vom 09.2025."
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-26",
      "datum": "2025-05-08",
      "art": "Brief",
      "titel": "Stellungnahme an den Ombudsmann",
      "gruppen": [
        "intern",
        "ombudsmann"
      ],
      "senderGruppe": "intern",
      "absender": "Miriam Steinbrecher, Compliance Officer DE und AI Compliance Officer Gruppe",
      "empfaenger": "Versicherungsombudsmann e. V., Referat Haftpflicht",
      "kennung": "INT-00000811",
      "quelle": null,
      "text": [
        "Sehr geehrte Damen und Herren,",
        "zu Ihrer Anfrage vom 24.04.2025 nehmen wir wie folgt Stellung:",
        "1. Vertragsstand: Der Vertrag VTR-00000801 (vormals 40.288.506-6) enthielt zum Schadenzeitpunkt den Baustein Tierhalterhaftpflicht (Nachtrag Nr. 2 vom 15.02.2019, wirksam 01.03.2019). Die Deckung bestand.\n2. Zustandekommen der Ablehnung: Bei der vorgezogenen Migration der Privathaftpflichtvertraege in unser neues Bestandssystem (Pilotwelle am 03.03.2025) wurde der Bausteincode aus dem Altsystem nicht uebernommen. Das Schadensystem prueft Deckungen gegen das neue Bestandssystem und kam deshalb zu einem falschen Ergebnis. Es handelt sich um einen Datenfehler, nicht um eine Ermessensentscheidung.\n3. Automatisierung: Die Ablehnung erfolgte automatisiert durch eine Konfigurationsregel unseres Schadensystems, ohne Ueberpruefung durch eine natuerliche Person. Das widerspricht unserer internen Kompetenzordnung, nach der ablehnende Entscheidungen stets durch Mitarbeitende zu treffen sind. Ursache war eine Fehlkonfiguration der Regel, die den vorgesehenen Vier-Augen-Schritt nicht ausloeste. Wir haben die Regel am 16.04.2025 deaktiviert, die Kompetenzordnung in Version 2.1 technisch abgesichert (Ablehnungen nur noch mit Freigabe) und alle 214 von demselben Migrationsfehler betroffenen Vertraege korrigiert. Zehn weitere Faelle mit gleicher Fehlablehnung wurden von Amts wegen wiedereroeffnet und reguliert.\n4. Regulierung: Der Schaden wurde am 17.04.2025 vollstaendig reguliert (EUR 1.240,00 an den Geschaedigten fuer Arztkosten, Schmerzensgeld und Kleidung), dem Beschwerdefuehrer wurde eine Kulanzzahlung von EUR 100,00 geleistet und eine schriftliche Entschuldigung uebermittelt.",
        "Wir bedauern den Vorfall und betrachten die Beschwerde als berechtigt.",
        "Mit freundlichen Gruessen\nMiriam Steinbrecher, Compliance Officer und Leiterin Beschwerdestelle Deutschland"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-27",
      "datum": "2025-05-20",
      "art": "Tabellenereignis",
      "titel": "Beschwerde bei der BaFin (nur erwähnt)",
      "gruppen": [
        "kunde",
        "aufsicht"
      ],
      "senderGruppe": "kunde",
      "absender": null,
      "empfaenger": null,
      "kennung": null,
      "quelle": "erwähnt in Dokument DOK-00000805",
      "text": [
        "Herr Pieper wendet sich schriftlich an die Bundesanstalt für Finanzdienstleistungsaufsicht. Das Schreiben selbst liegt der Fallakte nicht vor, nur die Erwähnung im Antwortschreiben der Aufsicht."
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-28",
      "datum": "2025-06-10",
      "art": "Dokument",
      "titel": "Anfrage der BaFin, Bitte um Stellungnahme",
      "gruppen": [
        "aufsicht",
        "intern"
      ],
      "senderGruppe": "aufsicht",
      "absender": "Bundesanstalt fuer Finanzdienstleistungsaufsicht (fiktive Darstellung)",
      "empfaenger": "Pfefferminzia Versicherung AG, Niederlassung Deutschland, Hauptbevollmaechtigte",
      "kennung": "DOK-00000805",
      "quelle": null,
      "text": [
        "Sehr geehrte Damen und Herren,",
        "Herr Hans-Georg Pieper, Dresden, hat sich mit Schreiben vom 20.05.2025 an uns gewandt und beanstandet, dass ein Haftpflichtschaden durch ein automatisiertes Verfahren abgelehnt worden sei, obwohl Versicherungsschutz bestand. Wir bitten um Stellungnahme innerhalb von vier Wochen, insbesondere zu den organisatorischen Vorkehrungen, die eine Ueberpruefung automatisierter Entscheidungen durch natuerliche Personen sicherstellen, sowie zu Anzahl und Behandlung gleichartiger Faelle.",
        "Dieses Schreiben ist eine vereinfachte, fiktive Darstellung fuer Lehrzwecke.",
        "Mit freundlichen Gruessen\nReferat Verbraucherschutz Versicherungen"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-29",
      "datum": "2025-07-07",
      "art": "Brief",
      "titel": "Bitte um schriftliche Zusicherung",
      "gruppen": [
        "kunde",
        "schaden"
      ],
      "senderGruppe": "kunde",
      "absender": "Hans-Georg Pieper",
      "empfaenger": "Aylin Demirci, Teamleiterin Schaden Haftpflicht DE",
      "kennung": "INT-00000823",
      "quelle": null,
      "text": [
        "Sehr geehrte Frau Demirci,",
        "Ihr Brief vom 17. April und das Geld sind angekommen, dafuer danke ich Ihnen. Ich bleibe bei Ihnen versichert. Aber ich moechte es schriftlich haben, dass kein Computer mehr ueber meine Schaeden entscheidet. Bitte bestaetigen Sie mir das.",
        "Hochachtungsvoll\nH.-G. Pieper"
      ],
      "wendepunkt": null
    },
    {
      "id": "EV-30",
      "datum": "2025-07-14",
      "art": "Brief",
      "titel": "Schriftliche Zusicherung: keine automatisierte Ablehnung mehr ohne Prüfung",
      "gruppen": [
        "schaden",
        "kunde"
      ],
      "senderGruppe": "schaden",
      "absender": "Aylin Demirci, Teamleiterin Schaden Haftpflicht DE",
      "empfaenger": "Hans-Georg Pieper",
      "kennung": "INT-00000824",
      "quelle": null,
      "text": [
        "Sehr geehrter Herr Pieper,",
        "gerne bestaetige ich Ihnen: Ablehnungen von Schaeden werden bei uns ausschliesslich von Mitarbeitenden entschieden und seit April zusaetzlich technisch durch eine zweite Freigabe abgesichert. Unser System darf Schaeden nur dann selbststaendig bearbeiten, wenn es sie bezahlt, und auch das nur bis EUR 5.000 bei eindeutiger Deckung. Jede Ablehnung, jede Kuerzung und jede Kulanzentscheidung trifft ein Mensch.",
        "Ich freue mich, dass Sie bei uns bleiben.",
        "Mit freundlichen Gruessen\nAylin Demirci"
      ],
      "wendepunkt": {
        "nr": 3,
        "bezeichnung": "Wendepunkt 3: Fall abgeschlossen"
      }
    }
  ],
  "faktencheck": {
    "regel": "Grün: Aussage ist in einer Tabelle, einem Dokument oder einer eindeutigen Nachrechnung belegt, und die dafür nötige Quelle liegt nicht nach dem Datum des Schreibens. Gelb: Aussage ist nur vermutet — etwa eine Zahl fürs ganze Unternehmen, die sich in unseren eigenen Tabellen (Datensatz Stufe S) nicht nachzählen lässt, oder eine Regel, die nur in einer späteren Fassung eines Regelwerks belegt ist. Rot: Aussage ist nicht belegt, oder die einzige verfügbare Quelle liegt nach dem Datum des Schreibens — auch wenn die Sache später zutraf.",
    "briefe": [
      {
        "id": "kunde",
        "titel": "Antwort an Herrn Pieper",
        "dateiname": "pieper-antwort-kunde.md",
        "datum": "2025-04-17",
        "meta": "Entwurf, Stand 17.04.2025, zur Freigabe durch Aylin Demirci, Teamleiterin Schaden Haftpflicht Deutschland",
        "betreff": "Ihre Schreiben vom 28. März 2025 und vom 15. April 2025 zu Ihrem Schaden SCH-00000810",
        "anrede": "Sehr geehrter Herr Pieper,",
        "absaetze": [
          "Sie haben recht, und wir haben einen Fehler gemacht. Ich beantworte Ihnen heute gemeinsam Ihr Schreiben vom 28. März 2025 und Ihr Schreiben vom 15. April 2025, denn beide betreffen denselben Vorgang: den Hundebiss vom 21. März 2025 und unsere Ablehnung vom 24. März 2025.",
          "Nach Ihrem ersten Schreiben haben Sie von uns nur die Standardmail vom 2. April 2025 erhalten und danach lange nichts mehr von uns gehört; das war nicht in Ordnung, und dafür entschuldige ich mich ausdrücklich.",
          "Zu Ihrer Frage, wer über Ihren Schaden entschieden hat: Es war kein Mensch, sondern ein Computerprogramm in unserem Schadensystem. Ihr Vertrag ist Anfang März 2025 in unser neues System übernommen worden; dabei wurde der Baustein Tierhalterhaftpflicht, den Sie seit dem 1. März 2019 eingeschlossen haben, versehentlich vergessen. Das Programm hat deshalb geprüft, ob eine Tierhalterdeckung besteht, keine gefunden und den Schaden automatisch abgelehnt, ohne dass zuvor eine Mitarbeiterin oder ein Mitarbeiter dies gesehen hat.",
          "Für diesen Fehler entschuldige ich mich ebenfalls, ebenso dafür, dass wir die Frist von 14 Tagen, die Sie uns in Ihrem Schreiben vom 28. März 2025 gesetzt hatten, nicht eingehalten haben: Diese Frist lief am 11. April 2025 ab, reguliert haben wir den Schaden erst heute, sechs Tage später.",
          "Wir haben den Baustein Tierhalterhaftpflicht heute wieder in Ihrem Vertrag eingetragen. Den Schaden haben wir noch heute abschließend bearbeitet: An Herrn M. sind EUR 1.240,00 für Arztkosten, Schmerzensgeld und die beschädigte Hose überwiesen worden, auf den vertraglichen Selbstbehalt von EUR 150,00 verzichten wir bei dieser Zahlung. Für den entstandenen Aufwand und die Wartezeit erhalten Sie von uns zusätzlich EUR 100,00, überwiesen auf Ihr uns bekanntes Konto.",
          "Ab sofort sieht bei jeder Ablehnung zuerst ein Mensch Ihren Fall an, bevor ein Brief an Sie geht.",
          "Ich bedaure diesen Vorfall sehr und möchte mich damit ausdrücklich bei Ihnen entschuldigen. Bei Fragen können Sie mich jederzeit unter der unten angegebenen Telefonnummer erreichen."
        ],
        "gruss": "Mit freundlichen Grüßen",
        "unterschrift": [
          "Aylin Demirci",
          "Teamleiterin Schaden Haftpflicht Deutschland",
          "[Telefon prüfen]"
        ],
        "zeilen": [
          {
            "aussage": "Sie haben recht, und wir haben einen Fehler gemacht.",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Beschwerderichtlinie R05, Anhang A, Textbaustein «Anerkennung»",
            "bemerkung": "Zulässiger Textbaustein, identisch mit dem historischen Schreiben INT-00000808 vom 17.04.2025 — Übernahme von Textbausteinen ist ausdrücklich erlaubt."
          },
          {
            "aussage": "Ihre Schreiben vom 28. März 2025 und vom 15. April 2025 zu Ihrem Schaden SCH-00000810",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000803 (Brief vom 28.03.2025), Interaktion INT-00000805 (Brief vom 15.04.2025), Schadentabelle SCH-00000810",
            "bemerkung": "Beide Quellen liegen vor dem Datum dieses Schreibens (17.04.2025)."
          },
          {
            "aussage": "den Hundebiss vom 21. März 2025",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Schadentabelle, Schaden SCH-00000810, Schadentag",
            "bemerkung": ""
          },
          {
            "aussage": "unsere Ablehnung vom 24. März 2025",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000802 (Brief vom 24.03.2025)",
            "bemerkung": ""
          },
          {
            "aussage": "die Standardmail vom 2. April 2025",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000804 (E-Mail vom 02.04.2025)",
            "bemerkung": ""
          },
          {
            "aussage": "danach lange nichts mehr von uns gehört",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Kontakttabelle: kein weiterer ausgehender Kontakt an Hans-Georg Pieper zwischen Interaktion INT-00000804 und diesem Schreiben",
            "bemerkung": "Geprüft durch Fehlen eines Gegenbelegs in der Kontakttabelle, nicht durch eine positive Erwähnung."
          },
          {
            "aussage": "Es war kein Mensch, sondern ein Computerprogramm in unserem Schadensystem",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000806 und INT-00000807 (interne E-Mails vom 16.04.2025)",
            "bemerkung": ""
          },
          {
            "aussage": "Ihr Vertrag ist Anfang März 2025 in unser neues System übernommen worden",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Vertragstabelle VTR-00000801, Feld migriert am (03.03.2025); Migrationslog",
            "bemerkung": ""
          },
          {
            "aussage": "der Baustein Tierhalterhaftpflicht, den Sie seit dem 1. März 2019 eingeschlossen haben",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Dokument DOK-00000801 (Nachtrag Nr. 2, wirksam 01.03.2019)",
            "bemerkung": ""
          },
          {
            "aussage": "versehentlich vergessen",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Migrationslog, Vertrag VTR-00000801 (Bausteincode Tierhalter nicht ins Zielschema übernommen)",
            "bemerkung": ""
          },
          {
            "aussage": "ohne dass zuvor eine Mitarbeiterin oder ein Mitarbeiter dies gesehen hat",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000806 vom 16.04.2025; Interaktion INT-00000802 selbst (maschinell erstellt, ohne Unterschrift)",
            "bemerkung": ""
          },
          {
            "aussage": "die Frist von 14 Tagen, die Sie uns in Ihrem Schreiben vom 28. März 2025 gesetzt hatten",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000803 (\"binnen 14 Tagen\")",
            "bemerkung": ""
          },
          {
            "aussage": "Diese Frist lief am 11. April 2025 ab",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Nachgerechnet: Interaktion INT-00000803 (28.03.2025) plus 14 Kalendertage",
            "bemerkung": "Zählweise Kalendertage."
          },
          {
            "aussage": "reguliert haben wir den Schaden erst heute, sechs Tage später",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Schadenposition SCH-00000810-04 (Zahlung 17.04.2025); nachgerechnet 17.04. minus 11.04. = 6 Tage",
            "bemerkung": ""
          },
          {
            "aussage": "Wir haben den Baustein Tierhalterhaftpflicht heute wieder in Ihrem Vertrag eingetragen",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Migrationslog, Vertrag VTR-00000801 (Baustein am 17.04.2025 manuell nachgetragen)",
            "bemerkung": "Nach der Korrektur (voriger Entwurf: „ist ab sofort wieder ... hinterlegt“, Ampel rot, weil die im Migrationslog vermerkte Nachmigration erst auf den 18.04.2025 datierte). Die jetzige Formulierung behauptet nur den manuellen Eintrag vom 17.04.2025 selbst, der belegt und taggleich ist; die spätere technische Nachmigration (18.04.2025) wird nicht mehr behauptet."
          },
          {
            "aussage": "An Herrn M. sind EUR 1.240,00 für Arztkosten, Schmerzensgeld und die beschädigte Hose überwiesen worden",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Schadenposition SCH-00000810-04 (17.04.2025)",
            "bemerkung": ""
          },
          {
            "aussage": "auf den vertraglichen Selbstbehalt von EUR 150,00 verzichten wir bei dieser Zahlung",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Schadenposition SCH-00000810-04; Deckungstabelle DEK-00000801-01 (Selbstbehalt EUR 150 fix)",
            "bemerkung": "Ursprünglich nahezu wortgleich mit dem historischen Schreiben INT-00000808 (\"Den Selbstbehalt von EUR 150,00 aus Ihrem Vertrag ziehen wir nicht ab.\"); im Zuge dieser Prüfung umformuliert."
          },
          {
            "aussage": "erhalten Sie von uns zusätzlich EUR 100,00",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Schadenposition SCH-00000810-05 (17.04.2025)",
            "bemerkung": "Ursprünglich wortgleich mit dem historischen Schreiben INT-00000808 (\"Fuer Ihren Aufwand und die Verzoegerung ueberweisen wir Ihnen zusaetzlich EUR 100,00 auf das uns bekannte Konto.\"); im Zuge dieser Prüfung umformuliert."
          },
          {
            "aussage": "Ab sofort sieht bei jeder Ablehnung zuerst ein Mensch Ihren Fall an, bevor ein Brief an Sie geht.",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Regelwerk RW-GRUPPE-R08-2025, Version 2.1, gültig ab 16.04.2025",
            "bemerkung": "Satz von der Teamleiterin wörtlich vorgegeben; inhaltlich geprüft und bestätigt."
          },
          {
            "aussage": "Bei Fragen können Sie mich jederzeit unter der unten angegebenen Telefonnummer erreichen.",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "kein Tatsachengehalt, Höflichkeitsfloskel",
            "bemerkung": "Ursprünglich wortgleich mit dem historischen Schreiben INT-00000808 (\"Fuer Rueckfragen erreichen Sie mich direkt unter der unten stehenden Nummer.\"); im Zuge dieser Prüfung umformuliert."
          }
        ],
        "vollstaendigkeit": [
          "Keine wesentliche inhaltliche Lücke gefunden.",
          "Einzige Auffälligkeit: Die Aussage «ist ab sofort wieder in Ihrem Vertrag hinterlegt» stützt sich auf den manuellen Eintrag vom 17.04.2025; die vollständige technische Nachmigration ist im Migrationslog erst für den 18.04.2025 vermerkt, einen Tag nach diesem Schreiben (siehe Zeile, Ampel rot)."
        ]
      },
      {
        "id": "ombudsmann",
        "titel": "Stellungnahme an den Versicherungsombudsmann",
        "dateiname": "pieper-stellungnahme-ombudsmann.md",
        "datum": "2025-05-08",
        "meta": "Entwurf, Stand 08.05.2025, zur Freigabe durch die Compliance-Abteilung Deutschland",
        "betreff": "Stellungnahme zur Beschwerde Pieper ./. Pfefferminzia, Ihr Zeichen O-2025-04-1187, unser Zeichen SCH-00000810",
        "anrede": "Sehr geehrte Damen und Herren,",
        "absaetze": [
          "wir beantworten Ihre Anfrage vom 24. April 2025 (Az. O-2025-04-1187) zu den vier von Ihnen genannten Punkten; die von Ihnen gesetzte Frist von drei Wochen läuft am 15. Mai 2025 ab, wir antworten Ihnen damit sieben Tage vor Fristablauf.",
          "1. Vertragsstand zum Schadenzeitpunkt: Der Baustein Tierhalterhaftpflicht war zum Zeitpunkt des Schadens am 21. März 2025 durchgehender Bestandteil des Vertrags VTR-00000801: Er wurde am 12. Februar 2019 beraten und mit Nachtrag Nr. 2 vom 15. Februar 2019 zum 1. März 2019 in den Vertrag aufgenommen. Die Deckung ist zu keinem späteren Zeitpunkt entfallen oder gekündigt worden.",
          "2. Zustandekommen der Ablehnung: Ursache ist ein Fehler bei der Datenübernahme. Am 3. März 2025 wurde der Vertrag im Rahmen einer vorgezogenen Migrationswelle für Privathaftpflichtverträge in Deutschland in unser neues Bestandssystem überführt. Der Code für den Baustein Tierhalterhaftpflicht ging bei dieser Überführung verloren und wurde im neuen System nicht angelegt, sodass der Vertragsdatensatz ab diesem Zeitpunkt fälschlich ohne Tierhalterdeckung geführt wurde. Als die Schadenmeldung vom 21. März 2025 einging, stützte sich die automatisierte Deckungsprüfung auf genau diesen unvollständigen Datensatz und verneinte die Deckung zu Unrecht. Ursächlich war damit ein technischer Übertragungsfehler bei der Migration, keine bewusste Prüfung des Einzelfalls.",
          "3. Automatisierung und Überprüfung: Ja, die Ablehnung kam ohne jede menschliche Beteiligung zustande. Das zugrunde liegende Regelwerk unseres Schadensystems war zum damaligen Zeitpunkt so eingerichtet, dass ein negatives Deckungsergebnis unmittelbar zum Versand eines Ablehnungsschreibens führte, statt vorher eine Mitarbeiterin oder einen Mitarbeiter einzuschalten. Bereits zum Zeitpunkt der Ablehnung galt bei uns intern der Grundsatz, dass über eine Ablehnung immer ein Mensch entscheidet; dieser Grundsatz wurde in diesem Fall nicht beachtet, weil die zuständige Regel technisch nicht als prüfpflichtige Entscheidung eingestuft war. Wir sehen darin ein eigenes Versäumnis in der Ausgestaltung unserer Kontrollen, nicht nur einen Softwarefehler.",
          "4. Zwischenzeitliche Regulierung: Die Zahlung an den Geschädigten in Höhe von EUR 1.240,00 für Arztkosten, Schmerzensgeld und die beschädigte Kleidung ist am 17. April 2025 erfolgt, den vertraglich vorgesehenen Selbstbehalt von EUR 150,00 haben wir dabei nicht in Abzug gebracht. Am selben Tag haben wir Herrn Pieper EUR 100,00 als Kulanz für seinen Aufwand und die Wartezeit ausgezahlt und uns schriftlich bei ihm entschuldigt.",
          "Versäumnisse bei der ersten Beschwerde: Auch bei der Bearbeitung der ersten Beschwerde von Herrn Pieper vom 28. März 2025 sind uns Versäumnisse unterlaufen. Wir haben den Eingang fristgerecht am 2. April 2025 bestätigt; eine inhaltliche Prüfung und Korrektur erfolgten jedoch nicht innerhalb der von Herrn Pieper gesetzten Frist von 14 Tagen, die am 11. April 2025 ablief. Reguliert haben wir erst am 17. April 2025, sechs Tage nach Ablauf dieser Frist und erst nach einer zweiten, deutlich schärferen Beschwerde vom 15. April 2025. Innerhalb unserer eigenen internen Bearbeitungsfrist von 15 Arbeitstagen lag die Regulierung noch, am 14. Arbeitstag nach der ersten Beschwerde; das genügt aus unserer Sicht dennoch nicht, denn die inhaltliche Klärung hätte nicht erst durch eine zweite Beschwerde ausgelöst werden dürfen.",
          "Bereits umgesetzte Maßnahmen: Die betroffene Regel unseres Schadensystems wurde am 16. April 2025 deaktiviert. Der Baustein wurde im Vertrag von Herrn Pieper am 17. April 2025 manuell nachgetragen. Nach unserer internen Auswertung vom 6. Mai 2025 waren insgesamt elf Schadenfälle von dieser automatisierten Fehlablehnung betroffen, darunter der Fall von Herrn Pieper; die übrigen zehn hat unser Haus aus eigener Initiative aufgegriffen und bis zum 25. April 2025 abschließend bearbeitet. Nach derselben internen Auswertung vom 6. Mai 2025 waren zudem 214 Verträge dieser Migrationswelle von demselben Migrationsfehler betroffen; sie wurden am 18. April 2025 nachträglich korrekt übertragen, und das fehlerhafte Zuordnungsschema wurde noch vor der bevorstehenden Hauptwelle der Migration Haftpflicht am 15. Mai 2025 korrigiert. Seit dem 16. April 2025 gilt in unserer Kompetenzordnung (R08, Fassung 2.1) zusätzlich eine technische Absicherung: Jede ablehnende, kürzende oder einschränkende Entscheidung, gleich ob durch ein Modell oder eine Konfigurationsregel, erzeugt zunächst eine Freigabeaufgabe für eine Mitarbeiterin oder einen Mitarbeiter und keinen Brief; ein Anteil der automatisierten Entscheidungen wird zusätzlich stichprobenweise nachgeprüft. Seit dem 1. Mai 2025 gilt zudem eine überarbeitete Beschwerderichtlinie (R05, Fassung 2025.2): Beschwerden über automatisierte Entscheidungen erhalten Priorität 1 und werden innerhalb von zwei Arbeitstagen darauf geprüft, ob bereits eine Überprüfung durch eine natürliche Person stattgefunden hat.",
          "Veranlasste, noch nicht abgeschlossene Maßnahmen: Die Meldung dieses Vorfalls an das unternehmensinterne Gremium für Modellrisiken ist veranlasst; die Befassung ist für eine Sitzung im September 2025 vorgesehen und hat zum jetzigen Zeitpunkt noch nicht stattgefunden. Ob die Korrektur des Zuordnungsschemas auch in der Praxis wirkt, zeigt sich endgültig erst mit der Hauptwelle am 15. Mai 2025, die nach dem Datum dieser Stellungnahme liegt.",
          "Wir sind zu dem Ergebnis gekommen, dass die Beschwerde von Herrn Pieper zu Recht erhoben wurde, und haben uns dafür ausdrücklich bei ihm entschuldigt. Für Rückfragen stehen wir gerne zur Verfügung."
        ],
        "gruss": "Mit freundlichen Grüßen",
        "unterschrift": [
          "Miriam Steinbrecher",
          "Compliance Officer Deutschland und Leiterin Beschwerdestelle Deutschland",
          "[Telefon prüfen]"
        ],
        "zeilen": [
          {
            "aussage": "Ihre Anfrage vom 24. April 2025 (Az. O-2025-04-1187)",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000809 (Brief vom 24.04.2025, Az. O-2025-04-1187)",
            "bemerkung": ""
          },
          {
            "aussage": "die von Ihnen gesetzte Frist von drei Wochen läuft am 15. Mai 2025 ab",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Nachgerechnet: Interaktion INT-00000809 (\"innerhalb von drei Wochen\") ab 24.04.2025 plus 21 Kalendertage",
            "bemerkung": ""
          },
          {
            "aussage": "wir antworten Ihnen damit sieben Tage vor Fristablauf",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Nachgerechnet: 15.05.2025 minus 08.05.2025 (Datum dieses Schreibens)",
            "bemerkung": ""
          },
          {
            "aussage": "Er wurde am 12. Februar 2019 beraten",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Dokument DOK-00000802 (Beratungsprotokoll, 12.02.2019)",
            "bemerkung": ""
          },
          {
            "aussage": "mit Nachtrag Nr. 2 vom 15. Februar 2019 zum 1. März 2019 in den Vertrag aufgenommen",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Dokument DOK-00000801 (Nachtrag Nr. 2, erstellt 15.02.2019, wirksam 01.03.2019)",
            "bemerkung": "Kernangaben (Vertrag, Baustein, Daten) sind zwangsläufig ähnlich wie im historischen Schreiben INT-00000811 formuliert, da es sich um dieselben Fakten handelt; Satzbau bewusst abweichend gehalten."
          },
          {
            "aussage": "Die Deckung ist zu keinem späteren Zeitpunkt entfallen oder gekündigt worden",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Deckungstabelle, Baustein BS-TIER-HUND zu Vertrag VTR-00000801 (kein Enddatum eingetragen)",
            "bemerkung": ""
          },
          {
            "aussage": "Am 3. März 2025 wurde der Vertrag im Rahmen einer vorgezogenen Migrationswelle für Privathaftpflichtverträge in Deutschland in unser neues Bestandssystem überführt",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Vertragstabelle VTR-00000801 (migriert am 03.03.2025); Migrationslog, Welle HP-2025-PILOT",
            "bemerkung": ""
          },
          {
            "aussage": "Der Code für den Baustein Tierhalterhaftpflicht ging bei dieser Überführung verloren und wurde im neuen System nicht angelegt",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Migrationslog, Vertrag VTR-00000801 (Bausteincode Tierhalter nicht ins Zielschema übernommen)",
            "bemerkung": ""
          },
          {
            "aussage": "Als die Schadenmeldung vom 21. März 2025 einging",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Schadentabelle, Schaden SCH-00000810, Schadentag",
            "bemerkung": ""
          },
          {
            "aussage": "Ja, die Ablehnung kam ohne jede menschliche Beteiligung zustande",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000806 und INT-00000807 (16.04.2025); Interaktion INT-00000802 (\"maschinell erstellt, ohne Unterschrift\")",
            "bemerkung": ""
          },
          {
            "aussage": "Bereits zum Zeitpunkt der Ablehnung galt bei uns intern der Grundsatz, dass über eine Ablehnung immer ein Mensch entscheidet",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Regelwerk RW-GRUPPE-R08-2025, Präambel (Grundsatz § 5 Nr. 2 galt schon in Version 2.0)",
            "bemerkung": "Beleg ist die rückblickende Aussage der Präambel von Version 2.1; der Wortlaut von Version 2.0 selbst liegt nicht vor."
          },
          {
            "aussage": "dieser Grundsatz wurde in diesem Fall nicht beachtet, weil die zuständige Regel technisch nicht als prüfpflichtige Entscheidung eingestuft war",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000807 vom 16.04.2025",
            "bemerkung": ""
          },
          {
            "aussage": "Die Zahlung an den Geschädigten in Höhe von EUR 1.240,00 für Arztkosten, Schmerzensgeld und die beschädigte Kleidung ist am 17. April 2025 erfolgt",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Schadenposition SCH-00000810-04",
            "bemerkung": ""
          },
          {
            "aussage": "den vertraglich vorgesehenen Selbstbehalt von EUR 150,00 haben wir dabei nicht in Abzug gebracht",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Schadenposition SCH-00000810-04; Deckungstabelle DEK-00000801-01",
            "bemerkung": ""
          },
          {
            "aussage": "Am selben Tag haben wir Herrn Pieper EUR 100,00 als Kulanz für seinen Aufwand und die Wartezeit ausgezahlt",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Schadenposition SCH-00000810-05 (17.04.2025)",
            "bemerkung": ""
          },
          {
            "aussage": "und uns schriftlich bei ihm entschuldigt",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000808 (Brief vom 17.04.2025)",
            "bemerkung": ""
          },
          {
            "aussage": "Wir haben den Eingang fristgerecht am 2. April 2025 bestätigt",
            "status": "vermutet",
            "ampel": "gelb",
            "quelle": "Interaktion INT-00000804 (E-Mail vom 02.04.2025); Beschwerderichtlinie R05 § 4 Nr. 1 (Eingangsbestätigung innert fünf Arbeitstagen)",
            "bemerkung": "Die Fünf-Arbeitstage-Regel ist nur in der ab 01.05.2025 gültigen Fassung 2025.2 dokumentiert; ob sie am 28.03./02.04.2025 in dieser Form bereits galt, ist nicht belegt."
          },
          {
            "aussage": "eine inhaltliche Prüfung und Korrektur erfolgten jedoch nicht innerhalb der von Herrn Pieper gesetzten Frist von 14 Tagen, die am 11. April 2025 ablief",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000803; nachgerechnet 28.03.2025 plus 14 Kalendertage",
            "bemerkung": ""
          },
          {
            "aussage": "Reguliert haben wir erst am 17. April 2025, sechs Tage nach Ablauf dieser Frist",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Schadenposition SCH-00000810-04; nachgerechnet",
            "bemerkung": ""
          },
          {
            "aussage": "erst nach einer zweiten, deutlich schärferen Beschwerde vom 15. April 2025",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000805",
            "bemerkung": ""
          },
          {
            "aussage": "Innerhalb unserer eigenen internen Bearbeitungsfrist von 15 Arbeitstagen lag die Regulierung noch, am 14. Arbeitstag nach der ersten Beschwerde",
            "status": "vermutet",
            "ampel": "gelb",
            "quelle": "Nachgerechnet: Arbeitstage 29.03.–17.04.2025, keine Feiertage in diesem Fenster (Karfreitag 18.04., Ostermontag 21.04. liegen danach); Beschwerderichtlinie R05 § 4 Nr. 2 (Antwort innert 15 Arbeitstagen)",
            "bemerkung": "Die Tageszählung selbst ist nachgerechnet und belegt; ob die 15-Arbeitstage-Regel am 28.03.2025 in dieser Form bereits galt, ist nicht belegt, nur vermutet."
          },
          {
            "aussage": "Die betroffene Regel unseres Schadensystems wurde am 16. April 2025 deaktiviert",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Interaktion INT-00000807 (16.04.2025)",
            "bemerkung": ""
          },
          {
            "aussage": "Der Baustein wurde im Vertrag von Herrn Pieper am 17. April 2025 manuell nachgetragen",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Migrationslog, Vertrag VTR-00000801",
            "bemerkung": ""
          },
          {
            "aussage": "Nach unserer internen Auswertung vom 6. Mai 2025 waren insgesamt elf Schadenfälle von dieser automatisierten Fehlablehnung betroffen",
            "status": "vermutet",
            "ampel": "gelb",
            "quelle": "Dokument DOK-00000804 (Root-Cause-Analyse, 06.05.2025)",
            "bemerkung": "Zahl fürs ganze Unternehmen; im Datensatz Stufe S liegt nur der Schadenfall SCH-00000810 vor, die Zahl elf lässt sich in unseren eigenen Tabellen nicht nachzählen. Die jetzige Formulierung nennt die Quelle (interne Auswertung vom 6. Mai 2025) immerhin transparent im Schreiben selbst; das ändert an der fehlenden eigenen Nachzählbarkeit nichts, bleibt deshalb gelb."
          },
          {
            "aussage": "die übrigen zehn hat unser Haus aus eigener Initiative aufgegriffen und bis zum 25. April 2025 abschließend bearbeitet",
            "status": "vermutet",
            "ampel": "gelb",
            "quelle": "Dokument DOK-00000804 (06.05.2025)",
            "bemerkung": "Unternehmensweite Zahl, nicht nachzählbar. Ursprünglich nahe an der Formulierung des historischen Schreibens INT-00000811 (\"wiedereröffnet und reguliert\"); umformuliert."
          },
          {
            "aussage": "Nach derselben internen Auswertung vom 6. Mai 2025 waren zudem 214 Verträge dieser Migrationswelle von demselben Migrationsfehler betroffen",
            "status": "vermutet",
            "ampel": "gelb",
            "quelle": "Dokument DOK-00000804 (06.05.2025: 214 Verträge)",
            "bemerkung": "Zahl fürs ganze Unternehmen, in Stufe S nicht nachzählbar; Quelle jetzt transparent im Schreiben genannt, bleibt aber gelb."
          },
          {
            "aussage": "sie wurden am 18. April 2025 nachträglich korrekt übertragen",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Migrationslog, Vertrag VTR-00000801 (nachmigriert 18.04.2025); Dokument DOK-00000804 (Nachmigration 18.04.) für die Gesamtzahl",
            "bemerkung": "Für Piepers eigenen Vertrag ist das Datum unmittelbar belegt; die Übertragung auf alle 214 Verträge stützt sich auf dieselbe unternehmensweite Auswertung wie oben."
          },
          {
            "aussage": "das fehlerhafte Zuordnungsschema wurde noch vor der bevorstehenden Hauptwelle der Migration Haftpflicht am 15. Mai 2025 korrigiert",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Dokument DOK-00000804 (06.05.2025: Mapping vor der Hauptwelle korrigiert)",
            "bemerkung": ""
          },
          {
            "aussage": "Seit dem 16. April 2025 gilt in unserer Kompetenzordnung (R08, Fassung 2.1) zusätzlich eine technische Absicherung",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Regelwerk RW-GRUPPE-R08-2025, Version 2.1, gültig ab 16.04.2025",
            "bemerkung": ""
          },
          {
            "aussage": "ein Anteil der automatisierten Entscheidungen wird zusätzlich stichprobenweise nachgeprüft",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Regelwerk RW-GRUPPE-R08-2025 § 5 Nr. 4 (zehn Prozent werden manuell nachgeprüft)",
            "bemerkung": ""
          },
          {
            "aussage": "Seit dem 1. Mai 2025 gilt zudem eine überarbeitete Beschwerderichtlinie (R05, Fassung 2025.2)",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Regelwerk RW-GRUPPE-R05-2025, Version 2025.2, gültig ab 01.05.2025",
            "bemerkung": ""
          },
          {
            "aussage": "Beschwerden über automatisierte Entscheidungen erhalten Priorität 1 und werden innerhalb von zwei Arbeitstagen darauf geprüft, ob bereits eine Überprüfung durch eine natürliche Person stattgefunden hat",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Regelwerk RW-GRUPPE-R05-2025 § 5 Nr. 3",
            "bemerkung": ""
          },
          {
            "aussage": "Die Meldung dieses Vorfalls an das unternehmensinterne Gremium für Modellrisiken ist veranlasst; die Befassung ist für eine Sitzung im September 2025 vorgesehen und hat zum jetzigen Zeitpunkt noch nicht stattgefunden",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Dokument DOK-00000804 (06.05.2025: Bericht an das Technology & AI Committee in der Sitzung 09/2025)",
            "bemerkung": "Korrekt als veranlasst/nicht erledigt gekennzeichnet, konsistent mit der Quelle."
          },
          {
            "aussage": "Wir sind zu dem Ergebnis gekommen, dass die Beschwerde von Herrn Pieper zu Recht erhoben wurde",
            "status": "belegt",
            "ampel": "gruen",
            "quelle": "Schadenfall insgesamt (Regulierung, interne E-Mails, Root-Cause-Analyse)",
            "bemerkung": "Ursprünglich nahe an der Formulierung des historischen Schreibens INT-00000811 (\"Wir bedauern den Vorfall und betrachten die Beschwerde als berechtigt.\"); umformuliert."
          }
        ],
        "vollstaendigkeit": [
          "Der Root-Cause-Analyse vom 06.05.2025 zufolge wurde der Vorfall zusätzlich im Modellinventar erfasst (Eintrag zu Vorfall VF-2025-03) und als meldepflichtiger Vorfall der KI-Governance-Richtlinie eingestuft; beides war am Datum dieser Stellungnahme bekannt, im Entwurf aber nicht erwähnt."
        ]
      }
    ]
  }
};
