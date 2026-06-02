#!/bin/zsh

# Startet NextStudy unter macOS per Doppelklick.
# Die Datei muss im gleichen Ordner wie index.py liegen.

cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 wurde nicht gefunden."
  echo "Bitte installiere Python 3 und starte diese Datei danach erneut."
  echo
  read -r "reply?Druecke Enter zum Beenden..." || true
  exit 1
fi

echo "Starte NextStudy..."
echo
python3 index.py

echo
echo "NextStudy wurde beendet. Dieses Fenster kann jetzt geschlossen werden."
read -r "reply?Druecke Enter zum Beenden..." || true
