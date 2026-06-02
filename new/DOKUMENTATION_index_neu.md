# Dokumentation zu `index.py`

## 1. Überblick

`index.py` ist die Hauptdatei von NextStudy. Das Programm läuft im Terminal und erstellt aus Lernthemen einen einfachen Lernplan. Man kann den Plan anzeigen, Aufgaben abhaken, eine Statistik ausgeben, den Plan speichern, laden und als Textdatei exportieren.

Die Datei ist bewusst als Einzeldatei aufgebaut. Das macht die Abgabe übersichtlich und man kann den Ablauf leichter erklären.

## 2. Start des Programms

Gestartet werden kann das Programm auf drei Arten.

Direkt über Python:

```bash
python3 new/index.py
```

Wenn man schon im Ordner `new` ist:

```bash
python3 index.py
```

Per Doppelklick im Dateimanager:

| Betriebssystem | Startdatei |
|---|---|
| Windows | `start_nextstudy_windows.bat` |
| macOS | `start_nextstudy_macos.command` |

Beide Startdateien liegen im gleichen Ordner wie `index.py`. Sie wechseln automatisch in diesen Ordner und starten dann das Programm in einem Terminalfenster. Die macOS-Datei ist ausführbar gemacht, damit sie im Finder per Doppelklick gestartet werden kann.

Nach dem Start erscheint das Menü:

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

Der Benutzer wählt immer eine Zahl aus. Dadurch bleibt die Bedienung einfach.

## 3. Aufbau der Datei

Die Datei ist in mehrere Bereiche eingeteilt:

1. Imports und Dateipfade
2. feste Werte wie Schwierigkeiten, Aufgaben und Tipps
3. Klasse `Thema`
4. Klasse `Lerneinheit`
5. Funktionen für Eingaben
6. Funktion zum Erstellen des Lernplans
7. Funktionen für Anzeige und Statistik
8. Funktionen zum Speichern, Laden und Exportieren
9. Hauptmenü mit `main()`

Diese Reihenfolge ist praktisch, weil zuerst die Daten und Klassen vorhanden sind und danach die Funktionen kommen, die damit arbeiten.

## 4. Imports und Dateipfade

```python
import json
import random
from pathlib import Path
```

`json` benutze ich zum Speichern und Laden. JSON ist dafür gut geeignet, weil man damit Listen und Dictionaries gut abspeichern kann.

`random` wird für den Tipp des Tages benutzt. Das Programm sucht damit einen zufälligen Satz aus der Liste `TIPPS` aus.

`Path` wird für Dateipfade verwendet. Damit kann man einfacher mit Dateien arbeiten als mit langen `open()`-Konstruktionen.

```python
BASE_DIR = Path(__file__).resolve().parent
SAVE_FILE = BASE_DIR / "nextstudy_plan.json"
EXPORT_FILE = BASE_DIR / "nextstudy_export.txt"
```

`BASE_DIR` ist der Ordner, in dem `index.py` liegt. Dadurch werden Speicherdatei und Exportdatei immer im gleichen Ordner erstellt. Das ist sinnvoll, weil die Dateien so nicht irgendwo anders auf dem Rechner landen.

## 5. Feste Programmdaten

```python
SCHWIERIGKEITEN = {"leicht": 1, "mittel": 2, "schwer": 3}
```

Hier wird die Schwierigkeit in eine Zahl umgewandelt. Diese Zahl heißt im Programm Gewichtung.

| Schwierigkeit | Gewichtung |
|---|---:|
| leicht | 1 |
| mittel | 2 |
| schwer | 3 |

Das habe ich mit einem Dictionary gelöst, weil man den passenden Wert direkt nachschlagen kann. Man braucht dadurch nicht mehrere `if`-Abfragen.

```python
AUFGABEN = {
    "leicht": "{} lernen, kurze Notizen machen und einmal wiederholen",
    "mittel": "{} lernen, Beispiele anschauen und Aufgaben lösen",
    "schwer": "{} intensiv lernen, Aufgaben üben und Fehler notieren",
}
```

In `AUFGABEN` stehen die Aufgabentexte für die drei Schwierigkeiten. Das `{}` ist ein Platzhalter für den Themennamen.

Beispiel:

```python
AUFGABEN["schwer"].format("Ableitungen")
```

Ergebnis:

```text
Ableitungen intensiv lernen, Aufgaben üben und Fehler notieren
```

```python
TIPPS = [...]
```

`TIPPS` ist eine Liste mit Lerntipps. Bei Menüpunkt 5 wird daraus ein zufälliger Tipp angezeigt.

## 6. Klasse `Thema`

```python
class Thema:
    def __init__(self, name, schwierigkeit):
        self.name = name
        self.schwierigkeit = schwierigkeit
        self.gewichtung = SCHWIERIGKEITEN.get(schwierigkeit, 2)
```

Ein `Thema` speichert ein einzelnes Lernthema. Es hat:

- `name`, zum Beispiel `"Ableitungen"`,
- `schwierigkeit`, also `"leicht"`, `"mittel"` oder `"schwer"`,
- `gewichtung`, also die passende Zahl für die Planung.

`SCHWIERIGKEITEN.get(schwierigkeit, 2)` nimmt die passende Gewichtung aus dem Dictionary. Falls aus irgendeinem Grund ein unbekannter Wert auftaucht, wird `2` genommen. Das entspricht mittel.

```python
def to_dict(self):
    return {"name": self.name, "schwierigkeit": self.schwierigkeit, "gewichtung": self.gewichtung}
```

`to_dict()` wird beim Speichern gebraucht. JSON kann keine eigenen Python-Objekte direkt speichern, aber Dictionaries funktionieren.

## 7. Klasse `Lerneinheit`

```python
class Lerneinheit:
    def __init__(self, tag, thema, aufgabe, dauer):
        self.tag = tag
        self.thema = thema
        self.aufgabe = aufgabe
        self.dauer = dauer
        self.status = "offen"
```

Eine `Lerneinheit` ist eine Aufgabe für einen bestimmten Tag.

| Attribut | Bedeutung |
|---|---|
| `tag` | Nummer des Lerntages |
| `thema` | Thema oder Sonderpunkt wie Wiederholung |
| `aufgabe` | genauer Aufgabentext |
| `dauer` | Lernzeit in Minuten |
| `status` | `offen` oder `abgeschlossen` |

Neue Aufgaben starten immer mit dem Status `offen`.

```python
def erledigen(self):
    self.status = "abgeschlossen"
```

Mit `erledigen()` wird eine Aufgabe abgehakt. Ich habe dafür eine eigene Methode benutzt, weil das klarer ist, als den Status überall direkt zu ändern.

Auch `Lerneinheit` hat eine `to_dict()`-Methode. Sie wird genauso wie bei `Thema` für das Speichern in JSON gebraucht.

## 8. Eingabefunktionen

### `eingabe_zahl(frage, minimum=1)`

Diese Funktion fragt eine ganze Zahl ab. Sie wird zum Beispiel für die Anzahl der Themen, die Lerntage, die Lernzeit und die Aufgabennummer benutzt.

Wichtig daran:

- `while True` wiederholt die Eingabe,
- `int(...)` wandelt den Text in eine Zahl um,
- `try/except` verhindert einen Absturz bei falscher Eingabe,
- `minimum` verhindert Zahlen wie `0` oder negative Werte.

Ohne diese Funktion müsste die gleiche Prüfung an mehreren Stellen im Code stehen.

### `eingabe_text(frage)`

Diese Funktion fragt Text ab und verhindert leere Eingaben. Mit `.strip()` werden Leerzeichen am Anfang und Ende entfernt.

### `eingabe_schwierigkeit(thema)`

Diese Funktion erlaubt nur `leicht`, `mittel` oder `schwer`. Die Eingabe wird vorher mit `.lower().strip()` angepasst. Dadurch funktioniert auch eine Eingabe wie ` Schwer `.

## 9. Neues Projekt erstellen

```python
def projekt_erstellen():
```

Diese Funktion sammelt alle Angaben für ein neues Lernprojekt:

1. Fach
2. Anzahl der Themen
3. Name und Schwierigkeit jedes Themas
4. Anzahl der Lerntage
5. Lernzeit pro Tag

Danach ruft sie `lernplan_erstellen()` auf und gibt alle wichtigen Werte zurück:

```python
return fach, themen, tage, lernzeit, plan
```

Diese Rückgabe ist wichtig, weil `main()` danach mit dem Plan weiterarbeiten muss.

## 10. Lernplan erstellen

```python
def lernplan_erstellen(themen, tage, lernzeit):
```

Das ist die zentrale Funktion des Programms.

Wenn es nur einen Lerntag gibt, erstellt das Programm direkt eine Wiederholung für alle Themen. Bei nur einem Tag wäre es nicht sinnvoll, nur ein einzelnes Thema auszuwählen.

Bei mehreren Tagen passiert Folgendes:

1. Die Themen werden nach Gewichtung sortiert.
2. Aus den Themen wird eine gewichtete Lernliste gebaut.
3. Für jeden Tag wird eine `Lerneinheit` erstellt.
4. Der letzte Tag wird als Wiederholung genutzt.
5. Bei mindestens vier Tagen wird der vorletzte Tag zur Prüfungsvorbereitung.

Die gewichtete Liste funktioniert so:

```python
for thema in sortierte_themen:
    lernliste.extend([thema] * thema.gewichtung)
```

Ein schweres Thema kommt also dreimal in die Liste, ein mittleres zweimal und ein leichtes einmal. Dadurch werden schwere Themen stärker eingeplant.

Mit dieser Zeile wird ein Thema aus der Liste gewählt:

```python
thema = lernliste[(tag - 1) % len(lernliste)]
```

Der Modulo-Operator `%` sorgt dafür, dass die Liste wieder von vorne beginnt, wenn es mehr Lerntage als Listeneinträge gibt.

## 11. Lernplan anzeigen

```python
def plan_anzeigen(fach, plan):
```

Diese Funktion gibt den fertigen Lernplan im Terminal aus. Angezeigt werden Nummer, Tag, Thema, Aufgabe, Dauer und Status.

Wenn noch kein Plan existiert, gibt die Funktion nur eine kurze Meldung aus und beendet sich mit `return`.

## 12. Statistik anzeigen

```python
def statistik_anzeigen(plan):
```

Die Statistik berechnet:

- wie viele Aufgaben es insgesamt gibt,
- wie viele abgeschlossen sind,
- wie viele noch offen sind,
- wie viel Lernzeit insgesamt geplant ist,
- wie viel Lernzeit schon erledigt wurde,
- den Fortschritt in Prozent.

Der Fortschritt wird so berechnet:

```python
prozent = round(erledigt / len(plan) * 100)
```

Danach gibt das Programm noch einen kurzen Hinweis aus, zum Beispiel ob man schon gut angefangen hat oder fast fertig ist.

## 13. Aufgabe erledigen

```python
def aufgabe_erledigen(fach, plan):
```

Zuerst wird der Plan angezeigt. Danach gibt der Benutzer die Nummer der Aufgabe ein, die erledigt wurde.

Diese Prüfung ist wichtig:

```python
if nummer > len(plan):
    print("Diese Aufgabe existiert nicht.")
    return
```

So kann keine Aufgabe abgehakt werden, die es gar nicht gibt.

## 14. Speichern

```python
def speichern(fach, themen, tage, lernzeit, plan):
```

Beim Speichern werden alle Daten in ein Dictionary gepackt. Im Code heißt dieses Dictionary `speicher_daten`. Die Themen und Lerneinheiten werden vorher mit `to_dict()` umgewandelt.

Gespeichert wird in:

```text
nextstudy_plan.json
```

Das Schreiben der Datei liegt in einem `try/except`-Block. Wenn das Speichern aus irgendeinem Grund nicht möglich ist, zum Beispiel wegen fehlender Rechte, stürzt das Programm nicht ab. Stattdessen wird eine Fehlermeldung angezeigt.

## 15. Laden

```python
def laden():
```

Beim Laden wird die JSON-Datei gelesen. Danach werden aus den gespeicherten Daten wieder `Thema`- und `Lerneinheit`-Objekte erstellt.

Die Funktion ist absichtlich vorsichtig gebaut. Sie benutzt `.get(...)`, Standardwerte und einen `try/except`-Block. Dadurch kann das Programm auch dann weiterlaufen, wenn die Speicherdatei fehlt, beschädigt ist oder einzelne Werte nicht so gespeichert wurden, wie erwartet.

## 16. Exportieren

```python
def exportieren(fach, plan):
```

Der Export schreibt den Plan als normale Textdatei:

```text
nextstudy_export.txt
```

JSON ist eher für das Programm gedacht. Die Textdatei ist eher für Menschen gedacht, zum Beispiel zum Ausdrucken oder schnellen Anschauen.

Auch der Export ist abgesichert. Falls die Textdatei nicht geschrieben werden kann, wird eine Meldung angezeigt und das Programm bleibt im Menü.

## 17. Hauptprogramm

```python
def menue_anzeigen():
```

Diese Funktion zeigt nur das Menü an.

```python
def main():
```

`main()` ist der Einstiegspunkt für die eigentliche Programmlogik. Dort wird zuerst der aktuelle Programmzustand angelegt:

```python
daten = {"fach": "", "themen": [], "tage": 0, "lernzeit": 0, "plan": []}
```

In diesem Dictionary liegen die aktuellen Daten des Programms. Dazu gehören Fach, Themen, Tage, Lernzeit und der fertige Plan. Ich habe das so gemacht, damit diese Werte nicht als viele einzelne Variablen im Menü herumliegen.

Danach werden kleine Funktionen für Aktionen angelegt, zum Beispiel `neues_projekt()`, `plan_laden()` und `tipp_anzeigen()`. Diese Funktionen greifen auf `daten` zu und ändern den Zustand, wenn zum Beispiel ein neues Projekt erstellt oder ein gespeicherter Plan geladen wird.

Die Menüauswahl läuft nicht mehr über eine lange `if/elif/else`-Kette. Stattdessen benutze ich eine Dispatch-Tabelle:

```python
aktionen = {
    "1": neues_projekt,
    "2": lambda: plan_anzeigen(daten["fach"], daten["plan"]),
    "3": lambda: aufgabe_erledigen(daten["fach"], daten["plan"]),
    "4": lambda: statistik_anzeigen(daten["plan"]),
    "5": tipp_anzeigen,
    "6": lambda: speichern(daten["fach"], daten["themen"], daten["tage"],
                           daten["lernzeit"], daten["plan"]),
    "7": plan_laden,
    "8": lambda: exportieren(daten["fach"], daten["plan"]),
}
```

Eine Dispatch-Tabelle ist hier ein Dictionary, das eine Eingabe wie `"1"` direkt einer Funktion zuordnet. Wichtig ist: Im Dictionary steht nicht das Ergebnis der Funktion, sondern die Funktion selbst. Das nennt man eine Funktionsreferenz. Erst später wird die gespeicherte Funktion wirklich ausgeführt:

```python
aktion = aktionen.get(auswahl)
if aktion:
    aktion()
```

Dadurch ist die Menülogik kürzer und übersichtlicher. Die Verzweigung passiert nicht mehr durch viele `elif`-Zeilen, sondern über den Dictionary-Zugriff.

Die `9` wird extra behandelt, weil sie das Programm beendet:

```python
if auswahl == "9":
    print("NextStudy wird beendet. Du bist jetzt wieder im Terminal.")
    break
```

Ganz unten steht der Main-Guard:

```python
if __name__ == "__main__":
    main()
```

Dadurch wird `main()` nur automatisch ausgeführt, wenn die Datei direkt gestartet wird. Wenn man die Datei später in einem Notebook oder Test importiert, startet das Menü nicht sofort.

## 18. Wichtige Begriffe zur Menülogik

| Begriff | Bedeutung in meinem Code |
|---|---|
| Kontrollstruktur | Die alte Lösung mit `if/elif/else` und die neue Steuerung über `aktionen` |
| Verzweigung | Auswahl zwischen mehreren Fällen, zum Beispiel Menüpunkt 1, 2 oder 3 |
| Dispatch-Tabelle | Das Dictionary `aktionen`, das Eingaben passenden Funktionen zuordnet |
| Funktionsreferenz | Im Dictionary steht die Funktion selbst, nicht direkt ihr Ergebnis |
| Funktionsaufruf | Die gespeicherte Funktion wird später mit `aktion()` ausgeführt |
| Zustandsverwaltung | Das Dictionary `daten` speichert den aktuellen Zustand des Programms |
| Programmzustand | Aktuelle Werte wie Fach, Themen, Tage, Lernzeit und Plan |
| Scope / Gültigkeitsbereich | Bereich, in dem eine Variable existiert |
| lokale Variable | Eine Variable, die nur innerhalb einer Funktion existiert |
| globale Variable | Eine Variable außerhalb von Funktionen; hier wäre das aber nicht die beste Lösung |
| falsche Blockstruktur | Ein Fehler, wenn Code falsch eingerückt ist und dadurch zur falschen Funktion gehört |
| Funktionskapselung | Die Menülogik liegt gesammelt in `main()` |
| Einstiegspunkt / Entry Point | Der Startpunkt des Programms, also `main()` |
| Main-Guard | `if __name__ == "__main__":`, damit das Programm nur beim direkten Start losläuft |
| NameError | Fehler, wenn Python einen Namen an der Stelle nicht kennt |
| statische Codeanalyse | Eine Prüfung vor dem Ausführen, zum Beispiel durch Pyright |

Kurz gesagt: Die ursprüngliche `if/elif`-Verzweigung wurde durch eine Dispatch-Tabelle ersetzt. Dabei werden Menüeingaben über ein Dictionary direkt passenden Funktionsreferenzen zugeordnet. Der aktuelle Programmzustand wird zentral in `daten` verwaltet. Außerdem liegt die Menülogik in `main()`, wodurch der Einstiegspunkt klarer ist und der Scope der Variablen besser passt.

## 19. Datenfluss

Der Ablauf sieht ungefähr so aus:

```text
Eingaben -> daten -> Thema-Objekte -> Lernplan -> Lerneinheit-Objekte -> Anzeige/Speichern/Export
```

Beim Speichern:

```text
Objekte -> Dictionaries -> JSON-Datei
```

Beim Laden:

```text
JSON-Datei -> Dictionaries -> Objekte
```

## 20. Fehlerbehandlung

Das Programm fängt mehrere typische Fehler ab:

- Text statt Zahl,
- leere Texteingaben,
- ungültige Schwierigkeit,
- zu kleine Zahlen,
- falsche Aufgabennummer,
- Speichern ohne vorhandenen Plan,
- Laden ohne Speicherdatei,
- kaputte oder unvollständige JSON-Datei,
- Fehler beim Speichern oder Exportieren,
- unerwartete Fehler in einer Menüaktion.

Zusätzlich gibt es im Hauptmenü ein Sicherheits-Backup. Wenn eine Aktion unerwartet einen Fehler auslöst, wird der Fehler angezeigt und danach wieder das Menü geöffnet:

```python
try:
    aktion()
except Exception as fehler:
    print(f"Unerwarteter Fehler: {fehler}")
    print("Das Sicherheits-Backup hat den Absturz verhindert. Das Menü wird neu angezeigt.")
```

Auch `Strg+C` oder ein Abbruch der Eingabe wird abgefangen. Dadurch kann man sich vertippen oder eine beschädigte Speicherdatei laden, ohne dass das Programm direkt abstürzt.

Wichtig ist aber: Wenn man im Menü `9` auswählt, ist NextStudy beendet. Danach ist man wieder im normalen Terminal. Eine Eingabe wie `h` gehört dann nicht mehr zu NextStudy, sondern wird von der Shell verarbeitet.

Die Startdateien halten das Terminalfenster nach dem Ende noch offen. Dadurch kann man die letzte Meldung lesen und das Fenster danach selbst schließen.

## 21. Warum ich es so umgesetzt habe

Ich habe das Programm eher einfach gehalten, damit man den Code nachvollziehen kann. Die Konsole reicht für die Funktion aus. Eine Datenbank oder Oberfläche hätte das Projekt unnötig größer gemacht.

Die Klassen waren trotzdem sinnvoll, weil ein Thema und eine Lerneinheit jeweils mehrere Werte haben. Die Dispatch-Tabelle habe ich eingebaut, weil das Menü dadurch aufgeräumter ist als mit einer langen `if/elif`-Kette. Die JSON-Speicherung macht das Programm praktischer, weil der Lernplan nicht nach jedem Beenden verloren geht.

## 22. Mögliche Erweiterungen

Später könnte man noch einbauen:

- mehrere Lernprojekte gleichzeitig,
- freie Tage,
- ein Prüfungsdatum statt nur Anzahl der Tage,
- Export als PDF,
- eine kleine Oberfläche,
- bessere Verteilung, damit schwere Themen nicht zu oft direkt hintereinander kommen.

## 23. Fazit

NextStudy ist ein überschaubares Python-Projekt, das trotzdem mehrere wichtige Grundlagen verbindet: Eingaben, Funktionen, Klassen, Listen, Dictionaries, Dateioperationen und einfache Logik. Am Ende entsteht kein reines Übungsprogramm, sondern ein Tool, das man wirklich für die eigene Lernplanung benutzen kann.
