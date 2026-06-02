# NextStudy - Projektbeschreibung

## Kurzbeschreibung

NextStudy ist ein kleines Python-Programm für die Konsole. Es erstellt aus mehreren Lernthemen automatisch einen Lernplan. Man gibt ein Fach, die Themen, die Schwierigkeit, die verfügbaren Lerntage und die Lernzeit pro Tag ein.

Danach erzeugt das Programm für jeden Tag eine Aufgabe. Der Plan kann angezeigt, gespeichert, geladen und als Textdatei exportiert werden. Außerdem kann man Aufgaben abhaken und sich den Fortschritt anzeigen lassen.

## Ziel

Das Ziel war ein Programm, das nicht zu groß wird, aber trotzdem einen echten Nutzen hat. Es soll beim Lernen helfen, indem es aus vielen Themen einen einfachen Tagesplan macht.

Das Programm soll:

- Lernstoff ordnen,
- schwere Themen stärker gewichten,
- Aufgaben auf Lerntage verteilen,
- Wiederholung einplanen,
- Fortschritt anzeigen,
- den Plan speichern und wieder laden.

## Dateien der Abgabe

Die wichtigsten Dateien sind:

```text
index.py
DOKUMENTATION_index_neu.md
NextStudy_Notebook.ipynb
NextStudy_Portfolio.md
NextStudy_Portfolio.docx
start_nextstudy_windows.bat
start_nextstudy_macos.command
screenshots/nextstudy_terminal.png
```

`index.py` ist der lauffähige Quellcode. Die beiden Startdateien öffnen das Programm per Doppelklick im Terminal. Die anderen Dateien erklären das Projekt und zeigen die Umsetzung.

Die Startdateien funktionieren so:

- `start_nextstudy_windows.bat` startet NextStudy unter Windows.
- `start_nextstudy_macos.command` startet NextStudy unter macOS.

Beide Dateien wechseln zuerst in ihren eigenen Ordner und starten danach `index.py`. Dadurch funktioniert der Start auch dann, wenn man die Datei direkt aus dem Dateimanager öffnet.

## Funktionen

| Nr. | Funktion | Was sie macht |
|---:|---|---|
| 1 | Neues Lernprojekt erstellen | fragt Fach, Themen, Schwierigkeit, Tage und Lernzeit ab |
| 2 | Lernplan anzeigen | zeigt alle geplanten Lerneinheiten im Terminal |
| 3 | Aufgabe erledigen | markiert eine Aufgabe als abgeschlossen |
| 4 | Statistik anzeigen | zeigt Fortschritt, offene Aufgaben und Lernzeit |
| 5 | Tipp des Tages anzeigen | gibt einen zufälligen Lerntipp aus |
| 6 | Lernplan speichern | speichert den Plan als JSON-Datei |
| 7 | Lernplan laden | lädt einen gespeicherten Plan |
| 8 | TXT exportieren | schreibt den Plan in eine normale Textdatei |
| 9 | Beenden | beendet das Programm |

## Hauptmenü

```text
========================
       NEXTSTUDY
========================
1. Neues Lernprojekt erstellen
2. Lernplan anzeigen
3. Aufgabe als erledigt markieren
4. Statistik anzeigen
5. Tipp des Tages anzeigen
6. Lernplan speichern
7. Lernplan laden
8. Lernplan als TXT exportieren
9. Beenden
```

## Datenmodell

Das Programm arbeitet mit zwei eigenen Klassen:

| Klasse | Bedeutung |
|---|---|
| `Thema` | speichert ein Lernthema mit Schwierigkeit und Gewichtung |
| `Lerneinheit` | speichert eine Aufgabe für einen bestimmten Tag |

Der Lernplan ist am Ende eine Liste aus mehreren `Lerneinheit`-Objekten.

Der aktuelle Programmzustand wird in `main()` in einem Dictionary namens `daten` gespeichert. Dort stehen Fach, Themen, Tage, Lernzeit und Plan. Für die Menüauswahl gibt es zusätzlich das Dictionary `aktionen`. Das ordnet Eingaben wie `"1"` oder `"2"` direkt passenden Funktionen zu.

## Lernplan-Logik

Die Schwierigkeit wird in eine Zahl umgewandelt:

| Schwierigkeit | Gewichtung |
|---|---:|
| leicht | 1 |
| mittel | 2 |
| schwer | 3 |

Schwere Themen bekommen dadurch mehr Gewicht. Der letzte Tag wird immer für Wiederholung genutzt. Wenn mindestens vier Lerntage vorhanden sind, wird der vorletzte Tag als Prüfungsvorbereitung genutzt.

## Menülogik

Die alte Lösung wäre eine längere `if/elif/else`-Kette gewesen. In der aktuellen Version wird das Menü über eine Dispatch-Tabelle gesteuert:

```python
aktionen = {
    "1": neues_projekt,
    "2": lambda: plan_anzeigen(daten["fach"], daten["plan"]),
}
```

Im Dictionary steht jeweils eine Funktionsreferenz. Die Funktion wird also nicht sofort ausgeführt, sondern erst später mit `aktion()`. Dadurch bleibt das Menü kürzer und besser lesbar.

## Speicherung

Der Lernplan wird in `nextstudy_plan.json` gespeichert. Dort stehen Fach, Themen, Lerntage, Lernzeit und alle geplanten Aufgaben. Für eine lesbare Ausgabe gibt es zusätzlich `nextstudy_export.txt`.

## Sicherheits-Backup

Das Programm soll nicht direkt abstürzen, wenn etwas schiefgeht. Deshalb werden mehrere Fehler abgefangen:

- falsche Zahlen-Eingaben,
- leere Texteingaben,
- ungültige Menüauswahl,
- fehlende Speicherdatei,
- beschädigte JSON-Datei,
- Fehler beim Speichern oder Exportieren,
- unerwartete Fehler in einer Menüaktion.

Wenn so ein Fehler passiert, zeigt das Programm eine verständliche Meldung und kehrt danach zum Menü zurück. Bei `9` wird NextStudy beendet. Danach ist man wieder im normalen Terminal, deshalb gehört eine spätere Eingabe nicht mehr zum Programm.

## Was nicht eingebaut wurde

Ich habe bewusst keine grafische Oberfläche, keinen Login, keine Datenbank und keinen Kalender eingebaut. Das hätte das Projekt unnötig groß gemacht. Für diese Version reicht die Konsole, weil man daran die Python-Grundlagen gut zeigen kann.
