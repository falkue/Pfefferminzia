#!/usr/bin/env bash
# Erzeugt den Zweig "teilnehmer" ohne Loesungen aus dem aktuellen Stand von main und pusht ihn.
#
# Der Zweig ist ein Snapshot: gleicher Inhalt wie main, aber ohne Loesungen und Dozentenmaterial.
# Was genau entfernt wird, steht in scripts/teilnehmer_filter.py (data/truth, der ganze Generator src/ tests/
# scripts/ config/, docs/stammdaten, docs/planung, Datenschau mit latenter Wahrheit, Abschnitte «Rolle im Datensatz»
# und «Ground Truth» in den Persona-Steckbriefen, truth-Tabellen im Data Dictionary, Didaktik-Markierungen in den
# Referenzdaten). pyproject.toml wird zum reinen Abhaengigkeits-Projekt, uv.lock wird dazu neu erzeugt.
# main bleibt unveraendert: gefiltert wird nur in einem temporaeren Arbeitsbaum.
# Das Kursmaterial unter kurs/ bleibt im Zweig.
# Teilnehmende laden nur diesen Zweig:  git clone -b teilnehmer --single-branch https://github.com/falkue/Pfefferminzia
# (ohne --single-branch holt git auch main mit data/truth in den lokalen Klon)
#
# Aufruf: scripts/build_teilnehmer_branch.sh [--no-push]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
BRANCH=teilnehmer
TMP="$(mktemp -d)"
WT="$TMP/wt"
aufraeumen() {
  cd "$ROOT"
  git worktree remove --force "$WT" >/dev/null 2>&1 || true
  git branch -D "$BRANCH" >/dev/null 2>&1 || true
  rm -rf "$TMP"
}
trap aufraeumen EXIT

git branch -D "$BRANCH" >/dev/null 2>&1 || true
git worktree add --detach "$WT" main >/dev/null
pushd "$WT" >/dev/null
git checkout -q --orphan "$BRANCH"

# Loesungen und Dozentenmaterial entfernen (bricht ab, wenn danach noch Loesungsinhalte gefunden werden)
python3 scripts/teilnehmer_filter.py

cat > README.md <<'EOF'
# Pfefferminzia – Arbeitsstand für Teilnehmende

Pfefferminzia ist ein frei erfundener Versicherer für Lehrzwecke (Schweiz und Deutschland, Haftpflicht und Leben).
Dieser Zweig ist der Arbeitsstand für den Kurs: der fertige Datensatz, die Unterlagen des Unternehmens und das
Kursmaterial unter `kurs/`. Eigene Ergebnisse kommen nach `meine-ergebnisse/`. Lösungen, Dozentenmaterial und der
Generator gehören nicht dazu.

**Einstieg:** [docs/START.md](docs/START.md). Claude liest zusätzlich die Datei `CLAUDE.md`.

Laden ohne GitHub-Konto, nur diesen Zweig:

```bash
git clone -b teilnehmer --single-branch https://github.com/falkue/Pfefferminzia
```

Oder im Browser: Zweig `teilnehmer` wählen, «Code» → «Download ZIP», entpacken.

## Lizenz und Hinweis

Daten und Dokumente (`data/`, `docs/`, `kurs/`): CC BY 4.0, siehe [LICENSE-DATA.md](LICENSE-DATA.md).

Alle Personen, Firmen, Adressen, Verträge, Schäden, Kennzahlen und Ereignisse sind synthetisch erzeugt. Ähnlichkeiten
mit real existierenden Personen, Unternehmen oder Marken sind unbeabsichtigt. Rechtliche und regulatorische Aussagen
sind vereinfacht und ersetzen keine Rechtsberatung. Teile dieses Materials wurden mit Unterstützung von KI erzeugt.
EOF
rm -f TEILNEHMER.md
# Lockdatei zum Abhaengigkeits-Projekt ohne Paket neu erzeugen (Versionen bleiben, soweit moeglich, wie in main)
uv lock -q
git add -A
git -c user.name="Falk Uebernickel" -c user.email="uebernickel@gmail.com" commit -qm "Teilnehmer-Zweig ohne Loesungen (Snapshot von main $(git rev-parse --short main))"
echo "Zweig $BRANCH gebaut: $(git rev-parse --short HEAD) (Snapshot von main $(git rev-parse --short main))"
if [[ "${1:-}" != "--no-push" ]]; then
  git push -qf origin "$BRANCH"
  echo "Zweig $BRANCH gepusht"
else
  echo "Zweig $BRANCH lokal erzeugt (kein Push)"
fi
popd >/dev/null
