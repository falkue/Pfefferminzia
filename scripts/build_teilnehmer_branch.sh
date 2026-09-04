#!/usr/bin/env bash
# Erzeugt den Zweig "teilnehmer" ohne Loesungen aus dem aktuellen Stand von main und pusht ihn.
#
# Der Zweig ist ein Snapshot: gleicher Inhalt wie main, aber ohne data/truth (latente Wahrheit, Labels,
# DQ-Protokoll), ohne die Persona-Wahrheiten in den Akten-Quelltexten und ohne die Dozentendokumente.
# Teilnehmende klonen mit:  git clone -b teilnehmer https://github.com/falkue/Pfefferminzia
#
# Aufruf: scripts/build_teilnehmer_branch.sh [--no-push]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
BRANCH=teilnehmer
WT="$(mktemp -d)/wt"

git worktree add --detach "$WT" main >/dev/null
pushd "$WT" >/dev/null
git checkout -q --orphan "$BRANCH"

# Loesungen und Dozentenmaterial entfernen
git rm -rq --cached data/truth 2>/dev/null || true
rm -rf data/truth
git rm -rq --cached src/pfefferminzia/synth/akten_inhalte.py src/pfefferminzia/synth/akten_inhalte_2.py 2>/dev/null || true
rm -f src/pfefferminzia/synth/akten_inhalte.py src/pfefferminzia/synth/akten_inhalte_2.py
git rm -rq --cached docs/stammdaten 2>/dev/null || true
rm -rf docs/stammdaten
# Generator-Module, die Wahrheiten erzeugen, bleiben; ohne Akten-Quelltexte kann die Pipeline nicht laufen: Hinweis ablegen
cat > TEILNEHMER.md <<'EOF'
# Teilnehmer-Zweig

Dieser Zweig enthaelt den Datensatz ohne Loesungen: kein Ordner `data/truth`, keine Dozentenerlaeuterungen,
keine Quelltexte der Persona-Akten. Der Generator ist zur Ansicht enthalten, laeuft in diesem Zweig aber nicht
vollstaendig. Einstieg: `docs/START.md`.
EOF
git add -A
git -c user.name="Falk Uebernickel" -c user.email="uebernickel@gmail.com" commit -qm "Teilnehmer-Zweig ohne Loesungen (Snapshot von main $(git rev-parse --short main))"
if [[ "${1:-}" != "--no-push" ]]; then
  git push -qf origin "$BRANCH"
  echo "Zweig $BRANCH gepusht (Snapshot von main $(git rev-parse --short main))"
else
  echo "Zweig $BRANCH lokal erzeugt (kein Push)"
fi
popd >/dev/null
git worktree remove --force "$WT"
git branch -D "$BRANCH" >/dev/null 2>&1 || true
