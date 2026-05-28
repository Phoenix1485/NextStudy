#!/bin/zsh

# Startet NextStudy unter macOS aus dem Projektordner heraus.
# Falls noch keine virtuelle Umgebung existiert, wird sie automatisch angelegt.

set -e

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 wurde nicht gefunden."
  echo "Installiere Python 3.11 oder neuer von https://www.python.org/downloads/macos/"
  read -r "reply?Druecke Enter zum Beenden..."
  exit 1
fi

if [ ! -x ".venv/bin/python" ]; then
  echo "Erstelle virtuelle Python-Umgebung..."
  python3 -m venv .venv
fi

source ".venv/bin/activate"

echo "Starte NextStudy..."
python main.py

echo
read -r "reply?Druecke Enter zum Beenden..."

