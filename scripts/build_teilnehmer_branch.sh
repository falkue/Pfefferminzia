#!/usr/bin/env bash
# Erzeugt den Zweig "teilnehmer" ohne Loesungen aus dem aktuellen Stand von main und pusht ihn.
#
# Der Zweig ist ein Snapshot: gleicher Inhalt wie main, aber ohne Loesungen und Dozentenmaterial.
# Was genau entfernt wird, steht in scripts/teilnehmer_filter.py (data/truth, Akten-Quelltexte, docs/stammdaten,
# docs/planung, Datenschau mit latenter Wahrheit, Abschnitte «Rolle im Datensatz» und «Ground Truth» in den
# Persona-Steckbriefen, truth-Tabellen im Data Dictionary, Didaktik-Markierungen in den Referenzdaten).
# main bleibt unveraendert: gefiltert wird nur in einem temporaeren Arbeitsbaum.
# Das Kursmaterial unter kurs/ bleibt im Zweig.
# Teilnehmende laden mit:  git clone -b teilnehmer https://github.com/falkue/Pfefferminzia
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

cat > TEILNEHMER.md <<'EOF'
# Teilnehmer-Zweig

Dieser Zweig enthaelt den Datensatz ohne Loesungen: kein Ordner `data/truth`, keine Dozentenerlaeuterungen
und Planungsunterlagen, keine Quelltexte der Persona-Akten, keine Abschnitte zur Rolle der Personas im Datensatz.
Das Kursmaterial liegt unter `kurs/`, eigene Ergebnisse kommen nach `meine-ergebnisse/`.
Der Generator ist zur Ansicht enthalten, laeuft in diesem Zweig aber nicht vollstaendig. Einstieg: `docs/START.md`.
EOF
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
