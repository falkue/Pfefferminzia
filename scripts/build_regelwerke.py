"""Erzeugt Regelwerks-Dokumente unter ``docs/regelwerke/`` aus den Referenztabellen.

Aufruf: ``uv run python scripts/build_regelwerke.py``

Erzeugt: RW-LV-ARL-2025 (Annahmerichtlinie Leben, aus data/reference/lv/annahmerichtlinie_tabellen.yaml und
diagnose_bibliothek.csv), RW-GRUPPE-R08 (Kompetenzordnung, aus hp/vollmachtsstufen.csv und ARL-Kompetenzen).
Die Beschwerderichtlinie R05 ist handgeschrieben (docs/regelwerke/RW-GRUPPE-R05-2025.md) und wird hier nicht
ueberschrieben.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
ZIEL = ROOT / "docs" / "regelwerke"
DISCLAIMER = ("Pfefferminzia ist ein frei erfundenes Unternehmen für Lehrzwecke. Alle Personen, Firmen, Adressen, Verträge, Schäden, "
              "Kennzahlen und Ereignisse sind synthetisch erzeugt. Ähnlichkeiten mit real existierenden Personen, Unternehmen oder Marken, "
              "insbesondere mit gleichnamigen Medien oder Dienstleistern, sind unbeabsichtigt und nicht intendiert. Rechtliche und "
              "regulatorische Aussagen sind vereinfacht, Stand 2026, und ersetzen keine Rechtsberatung. Teile dieses Materials wurden mit "
              "Unterstützung von KI erzeugt.")


def frontmatter(dokument_id: str, titel: str, sparte: str, markt: str, version: str, gueltig_ab: str, absender: str,
                vertraulichkeit: str = "intern", gueltig_bis: str | None = None) -> str:
    return (f"---\ndokument_id: {dokument_id}\ntitel: {titel}\ntyp: regelwerk\nsparte: {sparte}\nmarkt: {markt}\nsprache: de-CH\n"
            f"version: \"{version}\"\ngueltig_ab: {gueltig_ab}\ngueltig_bis: {gueltig_bis or 'null'}\ntarifgeneration: null\nquelle_system: null\n"
            f"absender: {absender}\nvertraulichkeit: {vertraulichkeit}\nerzeugt_am: 2026-09-04\n---\n\n")


def tabelle(zeilen: list[list], kopf: list[str]) -> str:
    out = ["| " + " | ".join(kopf) + " |", "|" + "---|" * len(kopf)]
    out += ["| " + " | ".join("" if v is None else str(v) for v in z) + " |" for z in zeilen]
    return "\n".join(out)


def num(n) -> str:
    return f"{int(n):,}".replace(",", "'")


def _pct(v) -> str:
    return "Ablehnung" if v is None else f"+{v} %"


def arl_2025() -> str:
    a = yaml.safe_load((ROOT / "data/reference/lv/annahmerichtlinie_tabellen.yaml").read_text(encoding="utf-8"))
    dx = pd.read_csv(ROOT / "data/reference/lv/diagnose_bibliothek.csv")
    t = [frontmatter("RW-LV-ARL-2025", "Annahmerichtlinie Leben (ARL-2025)", "LV", "GRUPPE", "2025.1", "2025-01-01",
                     "Pfefferminzia Leben AG und Pfefferminzia Lebensversicherung Deutschland AG, Underwriting")]
    t.append("# Annahmerichtlinie Leben ARL-2025\n\nInterne Richtlinie für die Risikoprüfung der Produkte RisikoLeben, Vorsorge, RentePlus und "
             "des Zusatzbausteins Erwerbs- und Berufsunfähigkeit. Gültig für Anträge ab 1. Januar 2025 in der Schweiz und in Deutschland. "
             "Sie löst die Richtlinien ARL-2015 (Pfefferminz) und ARL-2020 (Minzia) ab und harmonisiert beide.\n")
    t.append("## § 1 Grundsätze\n\n1. Die Risikoprüfung dient dem Schutz der Versichertengemeinschaft vor Antiselektion. Sie behandelt alle Antragstellenden "
             "nach denselben Regeln.\n2. Unzulässige Merkmale: Nationalität, Herkunft, Wohnort als Proxy für Herkunft, Geschlecht bei Neugeschäft in Deutschland "
             "(Unisex seit 21. Dezember 2012). Frühere Richtlinien enthielten einen Tarifzonen-Zuschlag (bis 2019) und einen Nationalitätsfaktor (bis 2007); "
             "beide sind aufgehoben und dürfen bei Nachprüfungen nicht mehr angewendet werden.\n3. Genetische Untersuchungen: Ergebnisse dürfen nicht verlangt "
             f"und nicht verwendet werden. Gesetzliche Grenzen (vereinfacht): CH {num(a['pruefumfang']['gentest_verbot']['CH']['tod'])} Todesfallsumme, "
             f"DE {num(a['pruefumfang']['gentest_verbot']['DE']['tod'])}; die Gruppenrichtlinie ist strenger und untersagt jede Verwendung.\n4. Gesundheitsdaten sind "
             "besondere Kategorien personenbezogener Daten. Sie werden getrennt von Vertriebsdaten gespeichert und nie in Kundenschreiben genannt (§ 9).\n"
             )
    st = a["pruefumfang"]["stufen"]
    z = [[f"bis {num(s['bis_summe'])}" if s["bis_summe"] else "über 1'500'000", ", ".join(s["pruefung"])] for s in st]
    t.append("## § 2 Prüfumfang nach Versicherungssumme\n\nTodesfallsumme in CHF bzw. EUR (nominal gleich behandelt), Alter unter 50; ab Alter 50 gilt die "
             "nächst strengere Stufe.\n\n" + tabelle(z, ["Versicherungssumme", "Prüfung"]) +
             f"\n\nEU/BU-Rente über 2'500 je Monat: zusätzlich {', '.join(a['pruefumfang']['eu_bu_rente_monat_ab_2500'])}. "
             f"Laborumfang: {', '.join(a['pruefumfang']['labor_umfang'])}.\n")
    bmi = a["bmi"]
    z = [[f"{k['bmi_von']} bis {k['bmi_bis']}", *[_pct(v) for v in k["tod"]], *[_pct(v) for v in k["eu_bu"]], k.get("aktion", "")] for k in bmi["klassen"]]
    t.append("## § 3 Grösse und Gewicht (BMI)\n\nZuschläge in Prozent der Risikoprämie; Altersgruppen 18 bis 39, 40 bis 59, 60 und älter.\n\n" +
             tabelle(z, ["BMI", "Tod 18-39", "Tod 40-59", "Tod 60+", "EU/BU 18-39", "EU/BU 40-59", "EU/BU 60+", "Massnahme"]) +
             "\n\nHinweis Altbestand: ARL-2008 und ältere Richtlinien bewerteten BMI 30.0 bis 32.9 mit +50 Prozent. Bei Nachprüfungen von Verträgen "
             "dieser Generationen gilt die Tabelle dieser Richtlinie.\n")
    r = a["rauchen"]
    z = [[s["status"].replace("_", " "), s["tod"].replace("_", " "), s["eu_bu"].replace("_", " ")] for s in r["status"]]
    t.append(f"## § 4 Nikotin\n\nDefinition: {r['definition']}. Cotinin-Test ab Summe {num(r['cotinin_test_ab_summe'])}. Rauchertarif: Faktor {r['rauchertarif_faktor']} "
             "auf die Risikoprämie.\n\n" + tabelle(z, ["Status", "Todesfall", "EU/BU"]) + "\n")
    bg = a["berufsgruppen"]
    z = [[g["gruppe"], g["bezeichnung"], g["faktor"], ", ".join(g["beispiele"])] for g in bg["gruppen"]]
    t.append("## § 5 Berufsgruppen (Erwerbs- und Berufsunfähigkeit)\n\n" + tabelle(z, ["Gruppe", "Bezeichnung", "Faktor EU/BU", "Beispiele"]) +
             "\n\nSonderberufe:\n\n" + tabelle([[s["beruf"].replace("_", " "), s["tod"].replace("_", " "), s["eu_bu"].replace("_", " ")] for s in bg["sonderberufe"]],
                                                ["Beruf", "Todesfall", "EU/BU"]) + "\n")
    z = []
    for _, d in dx.sort_values(["icd10_kapitel", "diagnose_code"]).iterrows():
        tod = d["uw_wirkung_tod"] + (f" +{int(d['zuschlag_tod_pct'])} %" if pd.notna(d["zuschlag_tod_pct"]) and d["zuschlag_tod_pct"] > 0 else "")
        eu = d["uw_wirkung_eu_bu"] + (f" +{int(d['zuschlag_eu_bu_pct'])} %" if pd.notna(d["zuschlag_eu_bu_pct"]) and d["zuschlag_eu_bu_pct"] > 0 else "")
        z.append([d["icd10_gruppe"], d["bezeichnung_de"], tod, eu, int(d["zurueckstellung_monate"]) if pd.notna(d["zurueckstellung_monate"]) and d["zurueckstellung_monate"] > 0 else "",
                  d["nachweis"]])
    t.append("## § 6 Vorerkrankungen\n\nBewertung auf Ebene der ICD-10-Gruppen. Zuschläge in Prozent der Risikoprämie, Zurückstellung in Monaten ab Therapieende. "
             "Bei mehreren Diagnosen werden Prozentzuschläge addiert (§ 8).\n\n" + tabelle(z, ["ICD-10", "Diagnose", "Todesfall", "EU/BU", "Zurückstellung", "Nachweis"]) + "\n")
    z = [[f["risiko"].replace("_", " "), f["tod"], str(f["eu_bu"]).replace("_", " ")] for f in a["freizeitrisiken"]]
    t.append("## § 7 Freizeitrisiken\n\nZuschlag in Promille der Versicherungssumme je Jahr auf den Todesfall, oder Ausschluss.\n\n" + tabelle(z, ["Risiko", "Todesfall ‰", "EU/BU"]) + "\n")
    k = a["kombination"]
    z = [[c["klasse"], c["bezeichnung"].replace("_", " "), c["zuschlag_pct_von"], c["zuschlag_pct_bis"] if c["zuschlag_pct_bis"] is not None else "offen"] for c in k["risikoklassen"]]
    t.append(f"## § 8 Kombination und Risikoklassen\n\nMethode: {k['methode'].replace('_', ' ')}. Annehmbar bis {k['max_zuschlag_pct_annehmbar']} Prozent Gesamtzuschlag, "
             f"Referat ab {k['ab_zuschlag_pct_referat']} Prozent, Ablehnung ab {k['ab_zuschlag_pct_ablehnung']} Prozent.\n\n" +
             tabelle(z, ["Risikoklasse", "Bezeichnung", "Zuschlag von %", "Zuschlag bis %"]) + "\n")
    ko = a["kompetenzen"]
    t.append("## § 9 Entscheidungskompetenzen und Automatisierung\n\n"
             f"1. Automatische Annahme (MINT Underwriting-Engine v2, Modellinventar MI-03): nur Risikoklasse bis {ko['automat']['bis_risikoklasse']}, Todesfallsumme bis "
             f"{num(ko['automat']['bis_summe_tod']['ARL-2025'])}, EU/BU-Rente bis {num(ko['automat']['bis_rente_eu_bu_monat'])} je Monat. Ausschliesslich positive Entscheide. "
             f"Zuschläge, Ausschlüsse, Zurückstellungen und Ablehnungen werden nie automatisiert entschieden. Vollständige Protokollierung, manuelle Stichprobe "
             f"{ko['automat']['stichprobe_manuell_pct']} Prozent.\n"
             f"2. Sachbearbeitung: bis Risikoklasse {ko['sachbearbeiter']['bis_risikoklasse']}, Summe bis {num(ko['sachbearbeiter']['bis_summe_tod'])}.\n"
             f"3. Gesellschaftsarzt: bis Risikoklasse {ko['gesellschaftsarzt']['bis_risikoklasse']}, Summe bis {num(ko['gesellschaftsarzt']['bis_summe_tod'])}.\n"
             f"4. Rückversicherung: ab Summe {num(ko['rueckversicherer']['ab_summe_tod'])} oder ab Risikoklasse {ko['rueckversicherer']['ab_risikoklasse']}.\n"
             "5. Kommunikation: Kundenschreiben nennen Entscheid, Zuschlag und Nachprüfungsmöglichkeit, aber keine Diagnosen. Ärztliche Auskunft auf Wunsch an den "
             "behandelnden Arzt. Auf Verlangen wird der Entscheidungsweg einschliesslich der Rolle des Regelwerks erläutert.\n")
    z = [[g["code"], g["text"], g.get("kundentext", "")] for g in a["ablehnungsgruende"]["liste"]]
    t.append("## § 10 Ablehnungsgründe\n\n" + tabelle(z, ["Code", "Grund", "Kundentext"]) + "\n")
    t.append("## § 11 Übergangsbestimmungen\n\nAnträge mit Eingang vor dem 1. Januar 2025 werden nach der bei Eingang gültigen Richtlinie entschieden. Nachprüfungen "
             "bestehender Verträge erfolgen nach dieser Richtlinie; ein Zuschlag darf dabei nicht steigen, weil ein früher zulässiges Merkmal weggefallen ist.\n")
    t.append(f"\n---\n\n{DISCLAIMER}\n")
    return "\n".join(t)


def r08() -> str:
    v = pd.read_csv(ROOT / "data/reference/hp/vollmachtsstufen.csv")
    a = yaml.safe_load((ROOT / "data/reference/lv/annahmerichtlinie_tabellen.yaml").read_text(encoding="utf-8"))["kompetenzen"]
    t = [frontmatter("RW-GRUPPE-R08-2025", "Vollmachts- und Kompetenzordnung (R08), Version 2.1", "GRUPPE", "GRUPPE", "2.1", "2025-04-16",
                     "Pfefferminzia Holding AG, Geschäftsleitung", "intern")]
    t.append("# Vollmachts- und Kompetenzordnung R08\n\nVersion 2.1, in Kraft seit 16. April 2025. Version 2.1 ersetzt Version 2.0 vom 1. Januar 2025; "
             "geändert wurde § 5 nach dem Vorfall VF-2025-03 (automatisierte Fehlablehnungen nach der Migration Haftpflicht).\n")
    t.append("## § 1 Geltungsbereich\n\nDiese Ordnung regelt, wer in der Pfefferminzia-Gruppe welche Entscheidungen treffen darf: Zeichnung von Risiken, "
             "Regulierung von Schäden und Leistungsfällen, Kulanz, Finanzen, Verträge mit Vermittlern. Sie gilt für Mitarbeitende, Systeme und "
             "Modelle gleichermassen.\n")
    t.append("## § 2 Zeichnungsberechtigung\n\nRechtsverbindliche Unterschriften erfolgen kollektiv zu zweien (Schweiz) beziehungsweise durch Prokura "
             "nach Handelsregister (Deutschland). Elektronische Freigaben in MINT gelten als Unterschrift, wenn sie personenbezogen protokolliert sind.\n")
    z = [[r["stufe"], r["rolle"], r["uw_kompetenz"], r["tarifabweichung_max_pct"], r["risikoklasse_max"], r["zeichnungsstatus_max"]] for _, r in v.iterrows()]
    t.append("## § 3 Underwriting Haftpflicht\n\n" + tabelle(z, ["Stufe", "Rolle", "Kompetenz", "Tarifabweichung max. %", "Risikoklasse max.", "Zeichnungsstatus max."]) + "\n")
    t.append(f"## § 4 Underwriting Leben\n\nAutomatische Annahme nur bis Risikoklasse {a['automat']['bis_risikoklasse']} und Todesfallsumme "
             f"{num(a['automat']['bis_summe_tod']['ARL-2025'])}; Sachbearbeitung bis {num(a['sachbearbeiter']['bis_summe_tod'])}; Gesellschaftsarzt bis "
             f"{num(a['gesellschaftsarzt']['bis_summe_tod'])}; darüber Rückversicherung. Einzelheiten in der Annahmerichtlinie RW-LV-ARL-2025, § 9.\n")
    z = [[r["stufe"], r["rolle"], r["zahlung_max"], r["reserve_max"], r["vergleich_max"], r["kulanz_max"], r["vier_augen_ab"] if pd.notna(r["vier_augen_ab"]) else "",
          r["deckungsablehnung"]] for _, r in v.iterrows()]
    t.append("## § 5 Schaden und Leistung\n\nBeträge in CHF beziehungsweise EUR (nominal gleich).\n\n" +
             tabelle(z, ["Stufe", "Rolle", "Zahlung max.", "Reserve max.", "Vergleich max.", "Kulanz max.", "Vier-Augen ab", "Deckungsablehnung"]) +
             "\n\n**Entscheidungsgrenzen für Systeme und Modelle (Version 2.1):**\n\n1. Systeme und Modelle dürfen ausschliesslich positive Entscheide unterhalb der "
             "Stufe 0 selbständig ausführen: Annahme ohne Erschwerung, Zahlung bei eindeutiger Deckung bis 5'000 und Betrugsscore unter 0.3.\n2. Jede "
             "Ablehnung, Kürzung, Erschwerung, Kündigung und jede Kulanzentscheidung wird von einer natürlichen Person getroffen. Seit Version 2.1 ist dies "
             "technisch erzwungen: Ein ablehnendes Ergebnis, gleich ob aus Modell oder Konfigurationsregel, erzeugt eine Aufgabe zur Freigabe und kein Schreiben.\n"
             "3. Konfigurationsregeln in Schaden- und Underwriting-Systemen gelten als Modellentscheidungen im Sinne dieser Ordnung und der KI-Governance-Richtlinie.\n"
             "4. Jede automatische Entscheidung wird mit Regel oder Modell, Version und Eingangsdaten protokolliert; zehn Prozent werden manuell nachgeprüft.\n"
             "5. Kundinnen und Kunden haben das Recht, die Überprüfung einer automatisierten Entscheidung durch eine Person zu verlangen (Beschwerderichtlinie R05, § 5).\n")
    t.append("## § 6 Finanzen und Beschaffung\n\nInvestitionen bis 100'000 Bereichsleitung, bis 500'000 Geschäftsleitung, darüber Verwaltungsrat. KI-Projekte über "
             "500'000 zusätzlich über das Technology & AI Committee.\n")
    t.append("## § 7 Vermittlerverträge\n\nAgentur- und Maklerverträge zeichnet die Vertriebsleitung; Provisionsänderungen über fünf Prozent die Geschäftsleitung.\n")
    t.append("## § 8 Delegation und Stellvertretung\n\nKompetenzen können schriftlich an die nächsttiefere Stufe delegiert werden, nie an Systeme. Stellvertretungen "
             "sind im Kompetenzregister zu führen.\n")
    t.append(f"\n---\n\n{DISCLAIMER}\n")
    return "\n".join(t)


def r05() -> str:
    t = [frontmatter("RW-GRUPPE-R05-2025", "Beschwerdemanagement-Richtlinie (R05)", "GRUPPE", "GRUPPE", "2025.2", "2025-05-01",
                     "Pfefferminzia Holding AG, Legal und Compliance", "intern")]
    t.append("# Beschwerdemanagement-Richtlinie R05\n\nVersion 2025.2, in Kraft seit 1. Mai 2025. Ergänzt um § 5 Absatz 3 (Beschwerden über automatisierte "
             "Entscheidungen mit Priorität 1) nach dem Vorfall VF-2025-03.\n")
    t.append("## § 1 Begriff\n\nBeschwerde ist jede Äusserung von Unzufriedenheit einer Kundin, eines Kunden oder einer anspruchsberechtigten Person über "
             "eine Leistung, Entscheidung oder das Verhalten der Gruppe oder ihrer Vermittler, unabhängig von Form und Kanal. Anfragen und sachliche Einwände "
             "ohne Unzufriedenheitsäusserung sind keine Beschwerden; im Zweifel gilt die Äusserung als Beschwerde.\n")
    t.append("## § 2 Grundlagen\n\nDeutschland: Mindestanforderungen der BaFin an die Beschwerdebearbeitung, Leitlinien von EIOPA, Verfahren des Versicherungsombudsmanns e. V. "
             "Schweiz: Erwartung der FINMA an ein faires Beschwerdemanagement, Ombudsstelle der Privatversicherung. Alle Angaben vereinfacht.\n")
    t.append("## § 3 Organisation\n\nErstkontakt und einfache Fälle: Kundenservice (1st Level). Beschwerdestelle: zentral je Markt (Compliance CH, Compliance DE). "
             "Eskalation an Legal bei Ombudsfällen, Aufsichtskorrespondenz und Rechtsstreitigkeiten. Beschwerden über Vermittler an den Maklerservice mit Kopie an die "
             "Beschwerdestelle.\n")
    t.append("## § 4 Prozess und Fristen\n\n1. Eingangsbestätigung innert fünf Arbeitstagen.\n2. Antwort innert 15 Arbeitstagen; ist das nicht möglich, Zwischenbescheid "
             "mit Begründung und neuem Termin.\n3. Jede Beschwerde erhält eine Kategorie aus der Taxonomie (30 Kategorien) und eine Ursache.\n4. Berechtigte Beschwerden "
             "werden mit Entschuldigung, Korrektur und, wo angemessen, Kulanz beantwortet. Unberechtigte Beschwerden werden begründet abgelehnt, mit Hinweis auf die "
             "Ombudsstelle.\n")
    t.append("## § 5 Sonderfälle\n\n1. Beschwerden über Vermittler: Anhörung des Vermittlers, Antwort durch die Beschwerdestelle.\n2. Datenschutzbeschwerden: "
             "Weiterleitung an den Datenschutzbeauftragten innert eines Arbeitstags.\n3. Beschwerden über automatisierte Entscheidungen: Priorität 1. Die Beschwerdestelle "
             "prüft innert zwei Arbeitstagen, ob die Entscheidung von einer Person überprüft wurde; falls nicht, wird die Überprüfung sofort veranlasst. Die betroffene "
             "Person hat Anspruch auf eine Darstellung des Entscheidungswegs (Kompetenzordnung R08, § 5).\n")
    t.append("## § 6 Ursachenanalyse und Berichterstattung\n\nDie Beschwerdestelle erstellt quartalsweise eine Statistik nach Kategorie, Markt, Sparte und Ursache und "
             "meldet Häufungen an die Prozessverantwortlichen. Bei systematischen Ursachen (mehr als fünf gleichartige Beschwerden in einem Quartal oder ein "
             "Aufsichtskontakt) wird eine Ursachenanalyse mit Massnahmenplan erstellt. Die Beschwerdestatistik Deutschland wird jährlich der BaFin gemeldet.\n")
    t.append("## Anhang A Textbausteine\n\n**Eingangsbestätigung (de-DE):** «Vielen Dank für Ihr Schreiben vom …. Ihr Anliegen wird geprüft. Wir melden uns innerhalb "
             "von 15 Arbeitstagen bei Ihnen.»\n\n**Eingangsbestätigung (de-CH):** «Besten Dank für Ihr Schreiben vom …. Wir prüfen Ihr Anliegen und melden uns innert "
             "15 Arbeitstagen.»\n\n**Anerkennung:** «Sie haben recht, und wir haben einen Fehler gemacht. …»\n\n**Hinweis Ombudsstelle (DE):** «Sollten Sie mit unserer "
             "Entscheidung nicht einverstanden sein, können Sie sich an den Versicherungsombudsmann e. V., Postfach 08 06 32, 10006 Berlin, wenden.» "
             "**(CH):** «… an die Ombudsstelle der Privatversicherung und der SUVA, Zürich.»\n")
    t.append(f"\n---\n\n{DISCLAIMER}\n")
    return "\n".join(t)


def main() -> None:
    ZIEL.mkdir(parents=True, exist_ok=True)
    for name, inhalt in (("RW-LV-ARL-2025.md", arl_2025()), ("RW-GRUPPE-R08-2025.md", r08()), ("RW-GRUPPE-R05-2025.md", r05())):
        (ZIEL / name).write_text(inhalt, encoding="utf-8")
        print(ZIEL.relative_to(ROOT) / name, len(inhalt.splitlines()), "Zeilen")


if __name__ == "__main__":
    main()
