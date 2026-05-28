# NextStudy

NextStudy ist ein lokaler Lernplaner in Python mit moderner Desktop-Oberflaeche.
Das Programm nimmt ein Fach, mehrere Themen, deren Schwierigkeit, die
verfuegbaren Lerntage und die taegliche Lernzeit auf. Daraus entsteht ein
strukturierter Lernplan mit Wiederholung, Mini-Test, Fortschritt und
JSON-Speicherung.

## Installation und Start

Python 3.11 oder neuer muss installiert sein. Externe Pakete werden nicht
benoetigt.

```bash
python3 main.py
```

Die Konsolenversion bleibt weiterhin verfuegbar:

```bash
python3 -m nextstudy.cli
```

## Startskripte

Unter Windows:

```bat
start_nextstudy_windows.bat
```

Unter macOS:

```bash
chmod +x start_nextstudy_macos_tahoe.command
./start_nextstudy_macos_tahoe.command
```

Die Skripte erstellen automatisch eine lokale `.venv`, falls sie noch nicht
existiert, und starten die grafische Oberflaeche.

## Funktionen

- moderne Desktop-UI mit abgerundeten Panels und Buttons
- Fach und Themen erfassen
- Schwierigkeit pro Thema auswerten
- Lernplan automatisch erstellen
- schwere Themen staerker gewichten
- Wiederholungstag und Mini-Test einplanen
- Fortschritt pro Lerneinheit verwalten
- Statistik anzeigen
- Lernplan als JSON speichern und laden

## Projektstruktur

```text
nextstudy/
  gui.py       Moderne Desktop-Oberflaeche
  cli.py       Interaktive Konsolenoberflaeche
  models.py    Datenklassen und Validierung
  planner.py   Fachliche Planungslogik
  storage.py   JSON-Speicherung
tests/
  test_planner.py
  test_storage.py
main.py
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Die Anwendung verwendet nur die Python-Standardbibliothek. Dadurch laeuft sie
ohne Installation weiterer Pakete.
