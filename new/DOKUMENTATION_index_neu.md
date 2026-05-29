# Dokumentation zu `index.py`

Diese Dokumentation beschreibt den aktuellen Code der Datei `index.py` im Ordner `new`. Sie erklärt den Aufbau, jede wichtige Funktion, die Klassen, Attribute, verwendete Python-Methoden und die Entscheidungen hinter der Umsetzung. Außerdem werden Verbesserungsmöglichkeiten genannt, damit man erklären kann, wie man das Programm auch anders hätte bauen können.

## 1. Ziel des Programms

Das Programm heißt **NextStudy**. Es ist ein Konsolenprogramm, mit dem ein Benutzer einen persönlichen Lernplan erstellen kann.

Der Benutzer kann:

- ein neues Lernprojekt erstellen,
- mehrere Themen mit Schwierigkeitsgrad eingeben,
- automatisch einen Lernplan erstellen lassen,
- den Lernplan anzeigen,
- Aufgaben als abgeschlossen markieren,
- eine Statistik zum Lernfortschritt sehen,
- einen zufälligen Lerntipp anzeigen,
- den Plan als JSON-Datei speichern,
- einen gespeicherten Plan laden,
- den Plan als Textdatei exportieren.

Das Programm läuft im Terminal und wird über ein Menü mit Zahlen bedient.

## 2. Grundidee des Codes

Der Code ist in mehrere Bereiche aufgeteilt:

- Imports und Konstanten
- Klassen für Datenobjekte
- Eingabe-Hilfsfunktionen
- Kernlogik zur Planerstellung
- Anzeige und Statistik
- Speichern, Laden und Exportieren
- Hauptprogramm mit Menü

Diese Struktur ist sinnvoll, weil nicht alles in einer großen Funktion steht. Jede Funktion hat eine bestimmte Aufgabe. Dadurch ist der Code übersichtlicher, leichter zu erklären und einfacher zu erweitern.

## 3. Imports

### Zeile 1: `import json, random`

```python
import json, random
```

Hier werden zwei Standardmodule importiert.

`json` wird zum Speichern und Laden des Lernplans benutzt. JSON ist ein Textformat, mit dem strukturierte Daten gespeichert werden können.

`random` wird benutzt, um einen zufälligen Lerntipp aus der Liste `TIPPS` auszuwählen.

Warum wurde das so gemacht?

Beide Module gehören zur Python-Standardbibliothek. Man muss also keine zusätzlichen Pakete installieren. Das macht das Programm einfacher lauffähig, besonders in der Schule.

Alternative:

Man könnte `import json` und `import random` in zwei getrennte Zeilen schreiben. Das wäre etwas lesbarer:

```python
import json
import random
```

Funktional ist beides gleich.

### Zeile 2: `from pathlib import Path`

```python
from pathlib import Path
```

`Path` wird für Dateioperationen verwendet. Damit kann das Programm prüfen, ob eine Datei existiert, und Dateien lesen oder schreiben.

Im Code wird `Path` verwendet bei:

- `Path(SAVE_FILE).write_text(...)`
- `Path(SAVE_FILE).read_text(...)`
- `Path(EXPORT_FILE).write_text(...)`
- `pfad.exists()`

Warum wurde `Path` verwendet?

`Path` ist moderner und oft kürzer als die ältere Schreibweise mit `open(...)`. Besonders bei einfachen Dateioperationen ist `write_text()` und `read_text()` übersichtlich.

Alternative:

Man könnte auch mit `open(...)` arbeiten:

```python
with open(SAVE_FILE, "w", encoding="utf-8") as datei:
    datei.write(text)
```

Die gewählte Variante mit `Path` ist kürzer.

## 4. Globale Konstanten

### Zeile 4: `SAVE_FILE`

```python
SAVE_FILE = "nextstudy_plan.json"
```

Diese Konstante speichert den Dateinamen für die JSON-Speicherdatei.

Sie wird in `speichern()` und `laden()` verwendet.

Warum als Konstante?

Der Dateiname steht dadurch nur an einer zentralen Stelle. Wenn man den Dateinamen später ändern möchte, muss man nicht im ganzen Code suchen.

### Zeile 5: `EXPORT_FILE`

```python
EXPORT_FILE = "nextstudy_export.txt"
```

Diese Konstante speichert den Dateinamen für den Export als Textdatei.

Sie wird in `exportieren()` verwendet.

Warum so gemacht?

Auch hier gilt: Der Dateiname ist zentral definiert und leicht änderbar.

### Zeile 7: `SCHWIERIGKEITEN`

```python
SCHWIERIGKEITEN = {"leicht": 1, "mittel": 2, "schwer": 3}
```

`SCHWIERIGKEITEN` ist ein Dictionary. Es ordnet jedem Schwierigkeitsgrad eine Zahl zu.

Bedeutung:

- `"leicht"` bekommt Gewichtung `1`
- `"mittel"` bekommt Gewichtung `2`
- `"schwer"` bekommt Gewichtung `3`

Diese Gewichtung wird später genutzt, damit schwere Themen im Lernplan häufiger vorkommen.

Warum ein Dictionary?

In der älteren Variante hätte man mehrere `if`-Abfragen schreiben können:

```python
if schwierigkeit == "leicht":
    gewichtung = 1
elif schwierigkeit == "mittel":
    gewichtung = 2
elif schwierigkeit == "schwer":
    gewichtung = 3
```

Das Dictionary ist kürzer und leichter zu erweitern. Wenn man später `"sehr schwer": 4` hinzufügen möchte, müsste man nur das Dictionary erweitern.

### Zeilen 9 bis 13: `AUFGABEN`

```python
AUFGABEN = {
    "leicht": "{} lernen, kurze Notizen machen und einmal wiederholen",
    "mittel": "{} lernen, Beispiele anschauen und Aufgaben lösen",
    "schwer": "{} intensiv lernen, Aufgaben üben und Fehler notieren"
}
```

`AUFGABEN` ist ebenfalls ein Dictionary. Es speichert für jede Schwierigkeit eine passende Aufgabenvorlage.

Das `{}` ist ein Platzhalter. Später wird mit `.format(thema.name)` der Name des Themas eingesetzt.

Beispiel:

```python
AUFGABEN["schwer"].format("Ableitungen")
```

Ergebnis:

```python
"Ableitungen intensiv lernen, Aufgaben üben und Fehler notieren"
```

Warum so gemacht?

Die Aufgabentexte stehen zentral an einer Stelle. Dadurch ist die Funktion `lernplan_erstellen()` kürzer, weil dort nicht mehr mehrere `if`-Abfragen für Aufgabentexte stehen müssen.

Alternative:

Man könnte eine eigene Funktion `aufgabe_fuer_thema(thema)` schreiben. Das wäre etwas ausführlicher, aber für Anfänger vielleicht leichter zu lesen. Die Dictionary-Lösung ist kompakter.

### Zeilen 15 bis 21: `TIPPS`

```python
TIPPS = [
    "Lerne lieber 45 Minuten konzentriert als 3 Stunden abgelenkt.",
    "Schreibe Fehler auf, damit du sie am Ende gezielt wiederholen kannst.",
    "Schwere Themen solltest du zuerst bearbeiten.",
    "Mache nach jeder Lerneinheit eine kurze Pause.",
    "Erkläre ein Thema laut, um zu prüfen, ob du es verstanden hast."
]
```

`TIPPS` ist eine Liste mit Lerntipps. Aus dieser Liste wird später zufällig ein Tipp ausgewählt.

Warum als globale Liste?

Die Tipps sind feste Programmdaten. Deshalb müssen sie nicht jedes Mal neu in einer Funktion erstellt werden. Außerdem sind sie oben im Code leicht zu finden und zu verändern.

Alternative:

Man könnte die Tipps in einer externen Textdatei speichern. Das wäre flexibler, aber für dieses Schulprojekt unnötig kompliziert.

## 5. Klasse `Thema`

### Zeilen 24 bis 31

```python
class Thema:
    def __init__(self, name, schwierigkeit):
        self.name = name
        self.schwierigkeit = schwierigkeit
        self.gewichtung = SCHWIERIGKEITEN.get(schwierigkeit, 2)

    def to_dict(self):
        return {"name": self.name, "schwierigkeit": self.schwierigkeit, "gewichtung": self.gewichtung}
```

Die Klasse `Thema` beschreibt ein einzelnes Lernthema.

Beispiel:

```python
Thema("Bruchrechnung", "schwer")
```

Dieses Objekt hat danach:

- `name = "Bruchrechnung"`
- `schwierigkeit = "schwer"`
- `gewichtung = 3`

### Konstruktor `__init__`

```python
def __init__(self, name, schwierigkeit):
```

Der Konstruktor wird automatisch aufgerufen, wenn ein neues `Thema`-Objekt erstellt wird.

Parameter:

- `name`: der Name des Themas
- `schwierigkeit`: der Schwierigkeitsgrad

### Attribut `self.name`

```python
self.name = name
```

Dieses Attribut speichert den Namen des Themas im Objekt.

### Attribut `self.schwierigkeit`

```python
self.schwierigkeit = schwierigkeit
```

Dieses Attribut speichert, ob das Thema leicht, mittel oder schwer ist.

### Attribut `self.gewichtung`

```python
self.gewichtung = SCHWIERIGKEITEN.get(schwierigkeit, 2)
```

Dieses Attribut speichert die Gewichtung des Themas.

Die Methode `.get(...)` wird auf dem Dictionary `SCHWIERIGKEITEN` aufgerufen.

```python
SCHWIERIGKEITEN.get(schwierigkeit, 2)
```

Bedeutung:

- Wenn `schwierigkeit` im Dictionary existiert, wird der passende Wert genommen.
- Wenn der Wert nicht existiert, wird `2` als Standardwert genommen.

Beispiel:

```python
SCHWIERIGKEITEN.get("schwer", 2)
```

Ergebnis:

```python
3
```

Beispiel mit ungültigem Wert:

```python
SCHWIERIGKEITEN.get("extrem", 2)
```

Ergebnis:

```python
2
```

Warum Standardwert `2`?

`2` entspricht `"mittel"`. Wenn aus irgendeinem Grund ein unbekannter Schwierigkeitsgrad auftaucht, wird das Thema neutral als mittel behandelt. Das verhindert Fehler.

### Methode `to_dict`

```python
def to_dict(self):
    return {"name": self.name, "schwierigkeit": self.schwierigkeit, "gewichtung": self.gewichtung}
```

Diese Methode wandelt ein `Thema`-Objekt in ein Dictionary um.

Warum ist das nötig?

JSON kann normale Dictionaries speichern, aber keine eigenen Python-Objekte wie `Thema`. Deshalb wird das Objekt vor dem Speichern umgewandelt.

## 6. Klasse `Lerneinheit`

### Zeilen 34 bis 44

```python
class Lerneinheit:
    def __init__(self, tag, thema, aufgabe, dauer):
        self.tag, self.thema, self.aufgabe, self.dauer = tag, thema, aufgabe, dauer
        self.status = "offen"

    def erledigen(self):
        self.status = "abgeschlossen"

    def to_dict(self):
        return {"tag": self.tag, "thema": self.thema, "aufgabe": self.aufgabe,
                "dauer": self.dauer, "status": self.status}
```

Die Klasse `Lerneinheit` beschreibt eine konkrete Aufgabe an einem bestimmten Lerntag.

Beispiel:

```python
Lerneinheit(1, "Mathe", "Mathe lernen und Aufgaben lösen", 45)
```

### Konstruktor `__init__`

```python
def __init__(self, tag, thema, aufgabe, dauer):
```

Parameter:

- `tag`: Nummer des Lerntages
- `thema`: Thema der Lerneinheit
- `aufgabe`: genaue Aufgabe
- `dauer`: Dauer in Minuten

### Mehrfachzuweisung

```python
self.tag, self.thema, self.aufgabe, self.dauer = tag, thema, aufgabe, dauer
```

Hier werden mehrere Attribute in einer Zeile gesetzt.

Das ist eine Kurzform für:

```python
self.tag = tag
self.thema = thema
self.aufgabe = aufgabe
self.dauer = dauer
```

Warum so gemacht?

Die Kurzform spart Platz und zeigt, dass diese vier Werte direkt zusammengehören.

Alternative:

Für Anfänger ist die ausführliche Schreibweise oft leichter verständlich. Die gewählte Variante ist kompakter.

### Attribut `status`

```python
self.status = "offen"
```

Jede neue Lerneinheit ist zuerst offen. Erst wenn der Benutzer sie erledigt, wird der Status auf `"abgeschlossen"` gesetzt.

### Methode `erledigen`

```python
def erledigen(self):
    self.status = "abgeschlossen"
```

Diese Methode markiert eine Lerneinheit als abgeschlossen.

Warum eine Methode?

Dadurch muss der restliche Code nicht direkt wissen, wie der Status intern geändert wird. Man ruft einfach `.erledigen()` auf.

### Methode `to_dict`

Diese Methode wandelt eine `Lerneinheit` in ein Dictionary um, damit sie in JSON gespeichert werden kann.

## 7. Eingabe-Hilfsfunktionen

Die Eingabe-Hilfsfunktionen stehen unter dem Kommentar:

```python
# ── Eingabe-Helpers ────────────────────────────────────────────────────────────
```

Diese Kommentare trennen Codebereiche optisch voneinander. Sie haben keine technische Funktion, helfen aber beim Lesen.

### Funktion `eingabe_zahl`

Zeilen 49 bis 57:

```python
def eingabe_zahl(frage, minimum=1):
    while True:
        try:
            wert = int(input(frage))
            if wert >= minimum:
                return wert
            print(f"Bitte eine Zahl ab {minimum} eingeben.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine ganze Zahl eingeben.")
```

Aufgabe:

Diese Funktion fragt eine ganze Zahl ab und prüft, ob sie mindestens einen bestimmten Wert hat.

Parameter:

- `frage`: Text, der dem Benutzer angezeigt wird
- `minimum`: kleinster erlaubter Wert, Standard ist `1`

Wichtige Bestandteile:

- `while True`: wiederholt die Eingabe so lange, bis sie gültig ist
- `input(frage)`: liest Benutzereingabe
- `int(...)`: wandelt die Eingabe in eine ganze Zahl um
- `try/except`: verhindert Absturz bei ungültiger Eingabe
- `return wert`: gibt die gültige Zahl zurück

Warum so gemacht?

Ohne diese Funktion müsste man die gleiche Eingabeprüfung an mehreren Stellen wiederholen. Durch die Funktion bleibt der Code sauberer.

Alternative:

Man könnte ungültige Eingaben nicht abfangen. Dann würde das Programm bei Eingabe von Text abstürzen. Die aktuelle Lösung ist benutzerfreundlicher.

### Funktion `eingabe_text`

Zeilen 60 bis 65:

```python
def eingabe_text(frage):
    while True:
        text = input(frage).strip()
        if text:
            return text
        print("Die Eingabe darf nicht leer sein.")
```

Aufgabe:

Diese Funktion fragt Text ab und verhindert leere Eingaben.

Wichtige Methode:

```python
.strip()
```

`.strip()` entfernt Leerzeichen am Anfang und Ende.

Beispiel:

```python
"   Mathe   ".strip()
```

Ergebnis:

```python
"Mathe"
```

Warum so gemacht?

Ohne `.strip()` könnte der Benutzer nur Leerzeichen eingeben, und das Programm würde das als gültiges Fach oder Thema akzeptieren.

### Funktion `eingabe_schwierigkeit`

Zeilen 68 bis 73:

```python
def eingabe_schwierigkeit(thema):
    while True:
        wert = input(f"Schwierigkeit für '{thema}' (leicht/mittel/schwer): ").lower().strip()
        if wert in SCHWIERIGKEITEN:
            return wert
        print("Bitte nur leicht, mittel oder schwer eingeben.")
```

Aufgabe:

Diese Funktion fragt den Schwierigkeitsgrad eines Themas ab.

Parameter:

- `thema`: Name des Themas, damit die Frage genauer formuliert werden kann

Wichtige Methoden:

- `.lower()`: macht aus Großbuchstaben Kleinbuchstaben
- `.strip()`: entfernt Leerzeichen

Beispiel:

```python
"  SCHWER ".lower().strip()
```

Ergebnis:

```python
"schwer"
```

Wichtige Bedingung:

```python
if wert in SCHWIERIGKEITEN:
```

Diese Zeile prüft, ob der eingegebene Wert als Schlüssel im Dictionary `SCHWIERIGKEITEN` existiert.

Warum so gemacht?

Weil dadurch nur gültige Schwierigkeitsgrade akzeptiert werden. Außerdem muss die Liste erlaubter Werte nur an einer Stelle gepflegt werden: im Dictionary `SCHWIERIGKEITEN`.

## 8. Projekt erstellen

### Funktion `projekt_erstellen`

Zeilen 78 bis 93:

```python
def projekt_erstellen():
    print("\n===== Neues Lernprojekt =====")
    fach = eingabe_text("Fach eingeben: ")
    anzahl = eingabe_zahl("Wie viele Themen möchtest du eintragen? ")
    themen = [Thema(eingabe_text(f"Thema {i}: "), eingabe_schwierigkeit(eingabe_text(f"Thema {i}: ")))
              for i in range(1, anzahl + 1)]
    # Sauberer: Namen einmal abfragen
    themen = []
    for i in range(1, anzahl + 1):
        name = eingabe_text(f"Thema {i}: ")
        themen.append(Thema(name, eingabe_schwierigkeit(name)))
    tage = eingabe_zahl("Wie viele Lerntage hast du? ")
    lernzeit = eingabe_zahl("Wie viele Minuten lernst du pro Tag? ")
    plan = lernplan_erstellen(themen, tage, lernzeit)
    print("\nLernprojekt wurde erstellt.")
    return fach, themen, tage, lernzeit, plan
```

Aufgabe:

Diese Funktion erstellt ein komplettes neues Lernprojekt.

Ablauf:

1. Überschrift ausgeben.
2. Fach abfragen.
3. Anzahl der Themen abfragen.
4. Themen und Schwierigkeitsgrade abfragen.
5. Anzahl der Lerntage abfragen.
6. Lernzeit pro Tag abfragen.
7. Lernplan erstellen.
8. Alle Daten zurückgeben.

### Wichtiger Hinweis zu Zeilen 82 bis 85

Im aktuellen Code steht zuerst diese List Comprehension:

```python
themen = [Thema(eingabe_text(f"Thema {i}: "), eingabe_schwierigkeit(eingabe_text(f"Thema {i}: ")))
          for i in range(1, anzahl + 1)]
```

Danach wird `themen` aber direkt wieder überschrieben:

```python
themen = []
```

Das bedeutet: Die erste List Comprehension wird zwar ausgeführt, aber ihr Ergebnis wird danach weggeworfen. Außerdem fragt sie den Themennamen doppelt ab. Deshalb ist der darunterstehende `for`-Block sauberer.

Der Kommentar im Code sagt das auch:

```python
# Sauberer: Namen einmal abfragen
```

Für die finale Version wäre es besser, Zeilen 82 und 83 zu entfernen und nur den `for`-Block zu behalten.

Warum ist der `for`-Block besser?

```python
for i in range(1, anzahl + 1):
    name = eingabe_text(f"Thema {i}: ")
    themen.append(Thema(name, eingabe_schwierigkeit(name)))
```

Hier wird der Name einmal gespeichert und dann für die Schwierigkeitsabfrage wiederverwendet. Das ist verständlicher und verhindert doppelte Eingaben.

### `range(1, anzahl + 1)`

```python
range(1, anzahl + 1)
```

Damit läuft die Schleife von `1` bis `anzahl`.

Warum `anzahl + 1`?

Bei `range` ist der Endwert nicht enthalten. Wenn `anzahl = 3` ist, erzeugt `range(1, 4)` die Werte `1`, `2`, `3`.

### `.append(...)`

```python
themen.append(Thema(name, eingabe_schwierigkeit(name)))
```

`.append()` fügt ein neues Element an eine Liste an.

Hier wird ein neues `Thema`-Objekt erstellt und in die Liste `themen` eingefügt.

### Rückgabe

```python
return fach, themen, tage, lernzeit, plan
```

Die Funktion gibt fünf Werte zurück. Diese Werte werden später in `main()` gespeichert.

## 9. Lernplan erstellen

### Funktion `lernplan_erstellen`

Zeilen 96 bis 115:

```python
def lernplan_erstellen(themen, tage, lernzeit):
    if tage == 1:
        return [Lerneinheit(1, "Wiederholung",
                            "Alle Themen kompakt wiederholen und einen Selbsttest machen", lernzeit)]

    lernliste = [t for t in sorted(themen, key=lambda x: x.gewichtung, reverse=True)
                 for _ in range(t.gewichtung)]
    plan = []
    for tag in range(1, tage + 1):
        if tag == tage:
            einheit = Lerneinheit(tag, "Wiederholung",
                                  "Alle Themen wiederholen, offene Fragen klären und Mini-Selbsttest machen", lernzeit)
        elif tag == tage - 1 and tage >= 4:
            einheit = Lerneinheit(tag, "Prüfungsvorbereitung",
                                  "Schwächen wiederholen, Zusammenfassung lesen und Beispielaufgaben lösen", lernzeit)
        else:
            thema = lernliste[(tag - 1) % len(lernliste)]
            einheit = Lerneinheit(tag, thema.name, AUFGABEN[thema.schwierigkeit].format(thema.name), lernzeit)
        plan.append(einheit)
    return plan
```

Aufgabe:

Diese Funktion erstellt aus den Themen, der Anzahl der Tage und der täglichen Lernzeit einen Lernplan.

Parameter:

- `themen`: Liste von `Thema`-Objekten
- `tage`: Anzahl der Lerntage
- `lernzeit`: Minuten pro Tag

### Sonderfall: Nur ein Tag

```python
if tage == 1:
    return [Lerneinheit(1, "Wiederholung",
                        "Alle Themen kompakt wiederholen und einen Selbsttest machen", lernzeit)]
```

Wenn es nur einen Lerntag gibt, wird kein normaler mehrtägiger Plan erstellt. Stattdessen gibt es eine einzige kompakte Wiederholung.

Warum so gemacht?

Bei nur einem Tag wäre es nicht sinnvoll, noch einen letzten Wiederholungstag und einen normalen Lerntag zu planen. Deshalb wird direkt ein Sonderfall behandelt.

### Gewichtete Lernliste

```python
lernliste = [t for t in sorted(themen, key=lambda x: x.gewichtung, reverse=True)
             for _ in range(t.gewichtung)]
```

Diese Zeile ist eine List Comprehension mit zwei `for`-Teilen.

Sie macht zwei Dinge:

1. Sie sortiert die Themen nach Gewichtung.
2. Sie fügt Themen mehrfach in die Liste ein, abhängig von ihrer Gewichtung.

### `sorted(...)`

```python
sorted(themen, key=lambda x: x.gewichtung, reverse=True)
```

`sorted(...)` sortiert die Themen.

Bestandteile:

- `themen`: die Liste, die sortiert wird
- `key=lambda x: x.gewichtung`: sortiert nach dem Attribut `gewichtung`
- `reverse=True`: sortiert absteigend, also schwere Themen zuerst

### `lambda x: x.gewichtung`

`lambda` ist eine kurze anonyme Funktion.

Diese Funktion bedeutet:

```python
Nimm ein Thema x und verwende x.gewichtung als Sortierwert.
```

Alternative:

Man könnte auch eine normale Funktion schreiben:

```python
def gewichtung_von_thema(thema):
    return thema.gewichtung
```

Dann:

```python
sorted(themen, key=gewichtung_von_thema, reverse=True)
```

Die Lambda-Variante ist kürzer.

### Mehrfaches Einfügen durch Gewichtung

```python
for _ in range(t.gewichtung)
```

Wenn ein Thema Gewichtung `3` hat, wird es dreimal in die `lernliste` aufgenommen.

Beispiel:

- Mathe schwer: Gewichtung 3
- Englisch leicht: Gewichtung 1

Dann entsteht ungefähr:

```python
[Mathe, Mathe, Mathe, Englisch]
```

Warum so gemacht?

Schwere Themen sollen häufiger im Lernplan auftauchen. Durch die mehrfache Aufnahme in die Liste passiert das automatisch.

### Bedeutung von `_`

Der Unterstrich `_` wird als Variablenname verwendet, wenn der Wert selbst nicht gebraucht wird. Hier zählt die Schleife nur, wie oft ein Thema eingefügt werden soll.

### Planliste

```python
plan = []
```

In dieser Liste werden alle Lerneinheiten gespeichert.

### Schleife über alle Tage

```python
for tag in range(1, tage + 1):
```

Diese Schleife erstellt für jeden Lerntag eine passende `Lerneinheit`.

### Letzter Tag: Wiederholung

```python
if tag == tage:
    einheit = Lerneinheit(tag, "Wiederholung",
                          "Alle Themen wiederholen, offene Fragen klären und Mini-Selbsttest machen", lernzeit)
```

Wenn der aktuelle Tag der letzte Tag ist, wird eine Wiederholungseinheit erstellt.

Warum so gemacht?

Ein Lernplan sollte am Ende nicht nur neue Inhalte enthalten, sondern auch eine Wiederholung. Das hilft bei der Prüfungsvorbereitung.

### Vorletzter Tag: Prüfungsvorbereitung

```python
elif tag == tage - 1 and tage >= 4:
```

Wenn der aktuelle Tag der vorletzte Tag ist und der Plan mindestens 4 Tage lang ist, wird eine Prüfungsvorbereitung erstellt.

Warum erst ab 4 Tagen?

Bei sehr kurzen Lernplänen würden sonst zu viele Sondertage entstehen. Bei 2 oder 3 Tagen wäre der Plan sonst fast nur Wiederholung und Prüfungsvorbereitung.

### Normale Lerntage

```python
thema = lernliste[(tag - 1) % len(lernliste)]
einheit = Lerneinheit(tag, thema.name, AUFGABEN[thema.schwierigkeit].format(thema.name), lernzeit)
```

Hier wird ein Thema aus der gewichteten Lernliste gewählt.

### Modulo-Operator `%`

```python
(tag - 1) % len(lernliste)
```

Der Modulo-Operator gibt den Rest einer Division zurück. Hier sorgt er dafür, dass der Index wieder vorne beginnt, wenn das Ende der Liste erreicht ist.

Beispiel:

Wenn die Liste 3 Elemente hat, sind gültige Indizes:

```python
0, 1, 2
```

Bei mehreren Tagen entstehen durch Modulo:

```python
0, 1, 2, 0, 1, 2
```

Warum so gemacht?

Der Plan kann dadurch mehr Tage haben als Themen vorhanden sind. Die Themen werden dann wiederholt.

### `.format(...)`

```python
AUFGABEN[thema.schwierigkeit].format(thema.name)
```

Hier wird die passende Aufgabenvorlage aus dem Dictionary `AUFGABEN` geholt und der Themenname eingesetzt.

Beispiel:

```python
AUFGABEN["mittel"].format("Grammatik")
```

Ergebnis:

```python
"Grammatik lernen, Beispiele anschauen und Aufgaben lösen"
```

## 10. Lernplan anzeigen

### Funktion `plan_anzeigen`

Zeilen 120 bis 126:

```python
def plan_anzeigen(fach, plan):
    if not plan:
        print("\nEs wurde noch kein Lernplan erstellt.")
        return
    print(f"\n===== Lernplan für {fach} =====")
    for i, e in enumerate(plan, 1):
        print(f"\n[{i}] Tag {e.tag}\nThema:   {e.thema}\nAufgabe: {e.aufgabe}\nDauer:   {e.dauer} Minuten\nStatus:  {e.status}")
```

Aufgabe:

Diese Funktion zeigt den aktuellen Lernplan im Terminal an.

### Prüfung `if not plan`

```python
if not plan:
```

Eine leere Liste gilt in Python als `False`. Wenn kein Plan existiert, wird eine Meldung ausgegeben und die Funktion beendet.

Warum so gemacht?

Ohne diese Prüfung würde das Programm versuchen, einen leeren Plan anzuzeigen. Das wäre für den Benutzer verwirrend.

### `enumerate(plan, 1)`

```python
for i, e in enumerate(plan, 1):
```

`enumerate` liefert gleichzeitig:

- eine Nummer `i`
- das aktuelle Element `e`

Die `1` bedeutet, dass die Nummerierung bei 1 beginnt.

Warum so gemacht?

Benutzer erwarten Aufgaben mit Nummer 1, 2, 3 und nicht mit 0, 1, 2.

### Mehrzeiliger f-String

Die Ausgabe enthält `\n`, also Zeilenumbrüche. Dadurch wird jede Lerneinheit übersichtlich angezeigt.

## 11. Statistik anzeigen

### Funktion `statistik_anzeigen`

Zeilen 129 bis 146:

```python
def statistik_anzeigen(plan):
    if not plan:
        print("\nEs gibt noch keinen Lernplan.")
        return
    erledigt = sum(1 for e in plan if e.status == "abgeschlossen")
    offen = len(plan) - erledigt
    min_ges = sum(e.dauer for e in plan)
    min_erl = sum(e.dauer for e in plan if e.status == "abgeschlossen")
    prozent = round(erledigt / len(plan) * 100)
    hinweis = next(t for s, t in [(100,"Alles abgeschlossen. Gute Vorbereitung."),
                                   (75,"Fast fertig. Jetzt nicht nachlassen."),
                                   (50,"Die Hälfte ist geschafft."),
                                   (25,"Guter Anfang. Bleib dran."),
                                   (0,"Starte mit der ersten Aufgabe. Danach wird es einfacher.")]
                   if prozent >= s)
    print(f"\n===== Statistik =====\nAufgaben gesamt:    {len(plan)}\nAbgeschlossen:      {erledigt}"
          f"\nOffen:              {offen}\nLernzeit gesamt:    {min_ges} Minuten"
          f"\nErledigte Lernzeit: {min_erl} Minuten\nFortschritt:        {prozent} %\nHinweis:            {hinweis}")
```

Aufgabe:

Diese Funktion berechnet und zeigt Statistiken zum Lernfortschritt.

### Erledigte Aufgaben zählen

```python
erledigt = sum(1 for e in plan if e.status == "abgeschlossen")
```

Diese Zeile zählt alle abgeschlossenen Aufgaben.

Erklärung:

- `for e in plan`: gehe jede Lerneinheit durch
- `if e.status == "abgeschlossen"`: berücksichtige nur erledigte Aufgaben
- `1`: für jede erledigte Aufgabe wird eine 1 erzeugt
- `sum(...)`: addiert alle Einsen

Wichtig:

Hier wird keine `.filter()`-Methode benutzt. Die Filterung passiert durch die `if`-Bedingung im Generator-Ausdruck.

### Offene Aufgaben

```python
offen = len(plan) - erledigt
```

Die offenen Aufgaben sind alle Aufgaben minus erledigte Aufgaben.

### Gesamte Lernzeit

```python
min_ges = sum(e.dauer for e in plan)
```

Diese Zeile addiert die Dauer aller Lerneinheiten.

### Erledigte Lernzeit

```python
min_erl = sum(e.dauer for e in plan if e.status == "abgeschlossen")
```

Diese Zeile addiert nur die Dauer der abgeschlossenen Lerneinheiten.

### Fortschritt in Prozent

```python
prozent = round(erledigt / len(plan) * 100)
```

Formel:

```python
erledigte Aufgaben / alle Aufgaben * 100
```

`round(...)` rundet auf eine ganze Zahl.

### Motivation mit `next(...)`

```python
hinweis = next(t for s, t in [(100,"Alles abgeschlossen. Gute Vorbereitung."),
                               (75,"Fast fertig. Jetzt nicht nachlassen."),
                               (50,"Die Hälfte ist geschafft."),
                               (25,"Guter Anfang. Bleib dran."),
                               (0,"Starte mit der ersten Aufgabe. Danach wird es einfacher.")]
               if prozent >= s)
```

Diese Zeile sucht den passenden Motivationstext.

Die Liste besteht aus Paaren:

- Schwelle
- Text

Beispiel:

```python
(75, "Fast fertig. Jetzt nicht nachlassen.")
```

`next(...)` nimmt den ersten passenden Text, bei dem `prozent >= s` gilt.

Warum funktioniert die Reihenfolge?

Die Liste beginnt bei 100 und geht nach unten bis 0. Dadurch wird immer der höchste passende Bereich gewählt.

Beispiel:

Wenn `prozent = 80` ist:

- 80 >= 100 ist falsch
- 80 >= 75 ist wahr
- also wird der 75-Prozent-Text genommen

Warum so gemacht?

Diese Lösung ist kompakt und vermeidet mehrere `if`-Abfragen.

Alternative:

Man könnte es auch einfacher, aber länger schreiben:

```python
if prozent == 100:
    hinweis = "Alles abgeschlossen..."
elif prozent >= 75:
    hinweis = "Fast fertig..."
elif prozent >= 50:
    hinweis = "Die Hälfte..."
elif prozent >= 25:
    hinweis = "Guter Anfang..."
else:
    hinweis = "Starte..."
```

Diese Alternative ist für Anfänger leichter lesbar. Die aktuelle Version ist kompakter.

## 12. Aufgabe erledigen

### Funktion `aufgabe_erledigen`

Zeilen 149 bis 159:

```python
def aufgabe_erledigen(fach, plan):
    if not plan:
        print("\nEs gibt noch keinen Lernplan.")
        return
    plan_anzeigen(fach, plan)
    nummer = eingabe_zahl("\nWelche Aufgabe wurde erledigt? Nummer eingeben: ")
    if nummer > len(plan):
        print("Diese Aufgabe existiert nicht.")
        return
    plan[nummer - 1].erledigen()
    print("Aufgabe wurde als abgeschlossen markiert.")
```

Aufgabe:

Diese Funktion markiert eine ausgewählte Lerneinheit als abgeschlossen.

Ablauf:

1. Prüfen, ob ein Plan existiert.
2. Plan anzeigen.
3. Nummer der erledigten Aufgabe abfragen.
4. Prüfen, ob die Nummer existiert.
5. Die passende Aufgabe auf abgeschlossen setzen.

### Warum `nummer - 1`?

```python
plan[nummer - 1].erledigen()
```

Python-Listen beginnen bei Index 0. Benutzer sehen aber Nummern ab 1.

Beispiel:

- Benutzer wählt `1`
- Python braucht Index `0`
- deshalb `nummer - 1`

### Methode `.erledigen()`

Die Methode `.erledigen()` gehört zur Klasse `Lerneinheit` und setzt den Status auf `"abgeschlossen"`.

## 13. Speichern

### Funktion `speichern`

Zeilen 164 bis 171:

```python
def speichern(fach, themen, tage, lernzeit, plan):
    if not plan:
        print("\nEs gibt keinen Lernplan zum Speichern.")
        return
    daten = {"fach": fach, "tage": tage, "lernzeit": lernzeit,
             "themen": [t.to_dict() for t in themen], "plan": [e.to_dict() for e in plan]}
    Path(SAVE_FILE).write_text(json.dumps(daten, indent=4, ensure_ascii=False), encoding="utf-8")
    print(f"Lernplan wurde in '{SAVE_FILE}' gespeichert.")
```

Aufgabe:

Diese Funktion speichert den aktuellen Lernplan in der Datei `nextstudy_plan.json`.

### Prüfung auf Plan

```python
if not plan:
```

Wenn kein Plan existiert, wird nichts gespeichert.

### Dictionary `daten`

```python
daten = {"fach": fach, "tage": tage, "lernzeit": lernzeit,
         "themen": [t.to_dict() for t in themen], "plan": [e.to_dict() for e in plan]}
```

Dieses Dictionary enthält alle Daten, die gespeichert werden müssen.

Bestandteile:

- `fach`: Fachname
- `tage`: Anzahl der Lerntage
- `lernzeit`: Lernzeit pro Tag
- `themen`: alle Themen als Dictionaries
- `plan`: alle Lerneinheiten als Dictionaries

### List Comprehensions

```python
[t.to_dict() for t in themen]
[e.to_dict() for e in plan]
```

Diese Ausdrücke wandeln alle Objekte in Dictionaries um.

Warum?

JSON kann keine eigenen Objekte speichern. Dictionaries kann JSON aber speichern.

### `json.dumps(...)`

```python
json.dumps(daten, indent=4, ensure_ascii=False)
```

`json.dumps` wandelt Python-Daten in einen JSON-String um.

Parameter:

- `daten`: die zu speichernden Daten
- `indent=4`: schöne Einrückung mit 4 Leerzeichen
- `ensure_ascii=False`: Umlaute bleiben lesbar

### `Path(...).write_text(...)`

```python
Path(SAVE_FILE).write_text(..., encoding="utf-8")
```

Diese Methode schreibt Text in eine Datei.

Warum `encoding="utf-8"`?

Damit Umlaute wie ä, ö, ü richtig gespeichert werden.

## 14. Laden

### Funktion `laden`

Zeilen 174 bis 187:

```python
def laden():
    pfad = Path(SAVE_FILE)
    if not pfad.exists():
        print("\nEs wurde keine Speicherdatei gefunden.")
        return "", [], 0, 0, []
    daten = json.loads(pfad.read_text(encoding="utf-8"))
    themen = [Thema(e["name"], e["schwierigkeit"]) for e in daten["themen"]]
    plan = []
    for e in daten["plan"]:
        einheit = Lerneinheit(e["tag"], e["thema"], e["aufgabe"], e["dauer"])
        einheit.status = e["status"]
        plan.append(einheit)
    print("Lernplan wurde geladen.")
    return daten["fach"], themen, daten["tage"], daten["lernzeit"], plan
```

Aufgabe:

Diese Funktion lädt den gespeicherten Lernplan aus der JSON-Datei.

### Datei prüfen

```python
pfad = Path(SAVE_FILE)
if not pfad.exists():
```

Hier wird geprüft, ob die Speicherdatei existiert.

Wenn nicht, gibt die Funktion leere Standardwerte zurück:

```python
return "", [], 0, 0, []
```

### Datei lesen

```python
daten = json.loads(pfad.read_text(encoding="utf-8"))
```

`pfad.read_text(...)` liest den Dateiinhalt als Text.

`json.loads(...)` wandelt den JSON-Text wieder in Python-Daten um.

Unterschied:

- `json.dumps(...)`: Python-Daten zu JSON-Text
- `json.loads(...)`: JSON-Text zu Python-Daten

### Themen rekonstruieren

```python
themen = [Thema(e["name"], e["schwierigkeit"]) for e in daten["themen"]]
```

Aus gespeicherten Dictionaries werden wieder echte `Thema`-Objekte erstellt.

### Plan rekonstruieren

```python
for e in daten["plan"]:
    einheit = Lerneinheit(e["tag"], e["thema"], e["aufgabe"], e["dauer"])
    einheit.status = e["status"]
    plan.append(einheit)
```

Hier wird jede gespeicherte Lerneinheit wieder als `Lerneinheit`-Objekt hergestellt.

Warum wird der Status extra gesetzt?

Der Konstruktor von `Lerneinheit` setzt den Status immer zuerst auf `"offen"`. Beim Laden soll aber der gespeicherte Status übernommen werden. Deshalb steht danach:

```python
einheit.status = e["status"]
```

## 15. Exportieren

### Funktion `exportieren`

Zeilen 190 bis 199:

```python
def exportieren(fach, plan):
    if not plan:
        print("\nEs gibt keinen Lernplan zum Exportieren.")
        return
    zeilen = [f"NextStudy - Lernplan für {fach}", "=" * 40, ""]
    for e in plan:
        zeilen += [f"Tag {e.tag}: {e.thema}", f"Aufgabe: {e.aufgabe}",
                   f"Dauer: {e.dauer} Minuten", f"Status: {e.status}", ""]
    Path(EXPORT_FILE).write_text("\n".join(zeilen), encoding="utf-8")
    print(f"Lernplan wurde als '{EXPORT_FILE}' exportiert.")
```

Aufgabe:

Diese Funktion exportiert den Lernplan als normale Textdatei.

### Liste `zeilen`

```python
zeilen = [f"NextStudy - Lernplan für {fach}", "=" * 40, ""]
```

Diese Liste sammelt alle Textzeilen für die Exportdatei.

### `"=" * 40`

Diese Schreibweise erzeugt 40 Gleichheitszeichen.

Das wird als Trennlinie benutzt.

### `zeilen += [...]`

```python
zeilen += [f"Tag {e.tag}: {e.thema}", ...]
```

Damit werden mehrere neue Elemente an die Liste angehängt.

Alternative:

Man könnte mehrmals `.append(...)` benutzen:

```python
zeilen.append(...)
```

Die aktuelle Variante ist kürzer, weil mehrere Zeilen auf einmal ergänzt werden.

### `"\n".join(zeilen)`

```python
"\n".join(zeilen)
```

Diese Methode verbindet alle Listenelemente zu einem Text. Zwischen den Elementen wird jeweils ein Zeilenumbruch eingefügt.

So entsteht eine gut lesbare Textdatei.

## 16. Menü anzeigen

### Funktion `menue_anzeigen`

Zeilen 204 bis 210:

```python
def menue_anzeigen():
    print("\n========================\n     NEXTSTUDY\n========================")
    for nr, text in enumerate(["Neues Lernprojekt erstellen", "Lernplan anzeigen",
                                "Aufgabe als erledigt markieren", "Statistik anzeigen",
                                "Tipp des Tages anzeigen", "Lernplan speichern",
                                "Lernplan laden", "Lernplan als TXT exportieren", "Beenden"], 1):
        print(f"{nr}. {text}")
```

Aufgabe:

Diese Funktion zeigt das Hauptmenü an.

### Warum eine Liste im Menü?

Die Menüpunkte stehen in einer Liste. Mit `enumerate(..., 1)` werden sie automatisch durchnummeriert.

Vorteil:

Man muss nicht jede Menüzeile einzeln schreiben:

```python
print("1. Neues Lernprojekt erstellen")
print("2. Lernplan anzeigen")
```

Die gewählte Lösung ist kürzer und leichter zu erweitern.

Alternative:

Für Anfänger ist die Variante mit einzelnen `print`-Zeilen leichter zu lesen. Die aktuelle Variante ist kompakter und professioneller.

## 17. Hauptprogramm

### Funktion `main`

Zeilen 213 bis 236:

```python
def main():
    fach, themen, tage, lernzeit, plan = "", [], 0, 0, []
    aktionen = {
        "1": lambda: projekt_erstellen(),
        "2": lambda: (plan_anzeigen(fach, plan), None)[:1],
        "3": lambda: (aufgabe_erledigen(fach, plan), None)[:1],
        "4": lambda: (statistik_anzeigen(plan), None)[:1],
        "5": lambda: (print("\nTipp des Tages:\n" + random.choice(TIPPS)), None)[:1],
        "6": lambda: (speichern(fach, themen, tage, lernzeit, plan), None)[:1],
        "7": lambda: laden(),
        "8": lambda: (exportieren(fach, plan), None)[:1],
    }
    while True:
        menue_anzeigen()
        auswahl = input("Auswahl: ").strip()
        if auswahl == "9":
            print("NextStudy wird beendet.")
            break
        if auswahl in aktionen:
            ergebnis = aktionen[auswahl]()
            if auswahl in ("1", "7") and ergebnis and len(ergebnis) == 5:
                fach, themen, tage, lernzeit, plan = ergebnis
        else:
            print("Ungültige Auswahl.")
```

Aufgabe:

`main()` steuert das gesamte Programm.

### Startwerte

```python
fach, themen, tage, lernzeit, plan = "", [], 0, 0, []
```

Hier werden mehrere Variablen gleichzeitig initialisiert.

Bedeutung:

- `fach`: Fachname
- `themen`: Liste der Themen
- `tage`: Anzahl der Lerntage
- `lernzeit`: Lernzeit pro Tag
- `plan`: Liste der Lerneinheiten

Warum so gemacht?

Die Werte müssen existieren, bevor der Benutzer im Menü zum Beispiel "Lernplan anzeigen" auswählt.

### Aktions-Dictionary

```python
aktionen = {
    "1": lambda: projekt_erstellen(),
    ...
}
```

`aktionen` ist ein Dictionary. Die Schlüssel sind Menüauswahlen als Strings. Die Werte sind Funktionen, die ausgeführt werden sollen.

Beispiel:

Wenn der Benutzer `"4"` eingibt, wird ausgeführt:

```python
statistik_anzeigen(plan)
```

Warum ein Dictionary?

Dadurch muss man nicht für jede Menüauswahl eine lange `if/elif`-Kette schreiben.

Alternative:

Man könnte das Menü so bauen:

```python
if auswahl == "1":
    ...
elif auswahl == "2":
    ...
elif auswahl == "3":
    ...
```

Diese Variante ist für Anfänger leichter zu verstehen. Das Dictionary ist kompakter und wirkt fortgeschrittener.

### `lambda`

`lambda` erstellt eine kleine Funktion ohne Namen.

Beispiel:

```python
"1": lambda: projekt_erstellen()
```

Bedeutung:

Wenn Aktion `"1"` aufgerufen wird, wird `projekt_erstellen()` ausgeführt.

Warum ist `lambda` hier nötig?

Ohne `lambda` würden die Funktionen teilweise sofort beim Erstellen des Dictionaries ausgeführt werden. Mit `lambda` werden sie erst ausgeführt, wenn der Benutzer die passende Auswahl trifft.

### Der Tuple-Trick bei Aktionen

Beispiel:

```python
"2": lambda: (plan_anzeigen(fach, plan), None)[:1]
```

Diese Schreibweise ruft `plan_anzeigen(fach, plan)` auf und gibt danach ein kleines Tuple zurück.

Technisch ist das etwas kompliziert. Der Zweck ist, dass die Aktion ausgeführt wird, ohne den Programmzustand wie bei Auswahl `"1"` oder `"7"` neu zu setzen.

Verbesserungsmöglichkeit:

Diese Schreibweise ist nicht sehr gut lesbar. Für ein Schulprojekt wäre eine einfache `if/elif`-Struktur oft verständlicher. Alternativ könnte man eigene kleine Funktionen schreiben.

### Endlosschleife

```python
while True:
```

Das Menü wird immer wieder angezeigt, bis der Benutzer `"9"` eingibt.

### Auswahl lesen

```python
auswahl = input("Auswahl: ").strip()
```

Die Eingabe wird als Text gelesen und mit `.strip()` bereinigt.

### Programm beenden

```python
if auswahl == "9":
    print("NextStudy wird beendet.")
    break
```

`break` beendet die Schleife und damit das Programm.

### Aktion ausführen

```python
if auswahl in aktionen:
    ergebnis = aktionen[auswahl]()
```

Wenn die Auswahl im Dictionary vorhanden ist, wird die passende Aktion ausgeführt.

### Rückgabewerte bei Auswahl 1 und 7

```python
if auswahl in ("1", "7") and ergebnis and len(ergebnis) == 5:
    fach, themen, tage, lernzeit, plan = ergebnis
```

Nur die Aktionen `"1"` und `"7"` geben einen kompletten neuen Programmzustand zurück:

- `"1"` erstellt ein neues Projekt
- `"7"` lädt ein gespeichertes Projekt

Deshalb werden nur bei diesen Auswahlen die Variablen `fach`, `themen`, `tage`, `lernzeit` und `plan` neu gesetzt.

## 18. Programmstart

### Zeilen 239 bis 240

```python
if __name__ == "__main__":
    main()
```

Diese Zeilen sorgen dafür, dass `main()` nur gestartet wird, wenn die Datei direkt ausgeführt wird.

Wenn man im Terminal startet:

```bash
python3 index.py
```

dann wird `main()` ausgeführt.

Wenn die Datei aber von einer anderen Datei importiert würde, würde `main()` nicht automatisch starten.

Warum so gemacht?

Das ist eine übliche Python-Struktur. Sie macht den Code sauberer und wiederverwendbarer.

## 19. Wichtige Python-Konzepte im Code

### Dictionary

Ein Dictionary speichert Schlüssel-Wert-Paare.

Im Code:

- `SCHWIERIGKEITEN`
- `AUFGABEN`
- `aktionen`
- gespeicherte JSON-Daten

### Liste

Listen speichern mehrere Elemente in einer Reihenfolge.

Im Code:

- `TIPPS`
- `themen`
- `plan`
- `zeilen`

### List Comprehension

Eine kompakte Schreibweise, um Listen zu erzeugen.

Beispiel:

```python
[t.to_dict() for t in themen]
```

### Generator-Ausdruck

Ähnlich wie List Comprehension, aber ohne sofort eine komplette Liste zu erzeugen.

Beispiel:

```python
sum(1 for e in plan if e.status == "abgeschlossen")
```

### `.get(...)`

Holt einen Wert aus einem Dictionary und liefert einen Standardwert, falls der Schlüssel nicht existiert.

Verwendet bei:

```python
SCHWIERIGKEITEN.get(schwierigkeit, 2)
```

### `.format(...)`

Setzt Werte in einen String ein.

Verwendet bei:

```python
AUFGABEN[thema.schwierigkeit].format(thema.name)
```

### `.strip()`

Entfernt Leerzeichen am Anfang und Ende eines Strings.

### `.lower()`

Wandelt Text in Kleinbuchstaben um.

### `.append(...)`

Fügt ein Element an eine Liste an.

### `.write_text(...)`

Schreibt Text in eine Datei.

### `.read_text(...)`

Liest Text aus einer Datei.

### `.exists()`

Prüft, ob eine Datei existiert.

### `next(...)`

Gibt das erste passende Element aus einem Generator zurück.

### `.filter()`

Eine Methode `.filter()` wird in diesem Code nicht verwendet.

Die Filterung passiert über `if`-Bedingungen in Generator-Ausdrücken:

```python
sum(e.dauer for e in plan if e.status == "abgeschlossen")
```

## 20. Warum der Code so aufgebaut wurde

Der Code wurde so aufgebaut, dass er kompakt ist und Wiederholungen reduziert.

Beispiele:

- Schwierigkeitswerte stehen in `SCHWIERIGKEITEN`, nicht in vielen `if`-Abfragen.
- Aufgabentexte stehen in `AUFGABEN`, nicht verstreut im Code.
- Tipps stehen in `TIPPS`, nicht direkt in der Menüaktion.
- Klassen speichern zusammengehörige Daten.
- `to_dict()` macht das Speichern in JSON möglich.
- `Path.write_text()` und `Path.read_text()` machen Dateioperationen kurz.
- Das Aktions-Dictionary ersetzt eine lange `if/elif`-Kette.

Der Code ist dadurch kürzer und fortgeschrittener als eine sehr einfache Anfänger-Version.

## 21. Warum nicht anders?

### Warum nicht alles in eine große Funktion?

Eine große Funktion wäre schwerer zu lesen und zu erklären. Mit mehreren Funktionen ist klarer, welcher Teil wofür zuständig ist.

### Warum Klassen?

Themen und Lerneinheiten haben mehrere zusammengehörige Eigenschaften. Klassen sind dafür passend, weil Name, Schwierigkeit, Gewichtung, Tag, Aufgabe, Dauer und Status sauber zusammengefasst werden.

### Warum JSON?

JSON ist lesbar, weit verbreitet und gut geeignet für strukturierte Daten. Außerdem unterstützt Python JSON direkt.

### Warum keine Datenbank?

Eine Datenbank wäre für dieses Projekt zu aufwendig. Das Programm speichert nur einen Lernplan, dafür reicht eine JSON-Datei völlig aus.

### Warum Terminal statt grafischer Oberfläche?

Ein Terminalprogramm ist leichter zu programmieren und für ein Schulprojekt gut erklärbar. Eine grafische Oberfläche würde viel zusätzlichen Code erfordern, ohne dass die eigentliche Lernplan-Logik besser wird.

### Warum Dictionaries für Schwierigkeitsgrade und Aufgaben?

Dictionaries vermeiden wiederholte `if`-Abfragen und machen den Code leichter erweiterbar.

## 22. Verbesserungsmöglichkeiten

### 1. Doppelte Themenabfrage entfernen

In `projekt_erstellen()` sollten die Zeilen mit der ersten List Comprehension entfernt werden, weil sie die Themen doppelt abfragen und danach überschrieben werden.

Besser:

```python
themen = []
for i in range(1, anzahl + 1):
    name = eingabe_text(f"Thema {i}: ")
    themen.append(Thema(name, eingabe_schwierigkeit(name)))
```

### 2. Aktions-Dictionary vereinfachen

Der Tuple-Trick mit `(funktion(), None)[:1]` ist schwer zu erklären. Eine `if/elif`-Kette wäre länger, aber für Anfänger verständlicher.

### 3. `dataclass` verwenden

Man könnte die Klassen mit `@dataclass` kürzer schreiben.

Beispiel:

```python
from dataclasses import dataclass
```

Das wäre moderner, aber für Anfänger vielleicht zusätzlicher Stoff.

### 4. Fehler beim Laden abfangen

Wenn die JSON-Datei beschädigt ist, könnte das Programm aktuell abstürzen. Man könnte `try/except` beim Laden einbauen.

### 5. Mehrere Lernpläne unterstützen

Aktuell gibt es nur eine Speicherdatei. Man könnte mehrere Projekte mit unterschiedlichen Dateinamen speichern.

### 6. Tests schreiben

Man könnte automatische Tests für Funktionen wie `lernplan_erstellen()` schreiben.

### 7. Code auf mehrere Dateien aufteilen

Bei größerem Umfang könnte man Klassen, Eingabe, Speicherung und Hauptprogramm in eigene Dateien verschieben.

Für dieses Projekt ist eine Datei aber noch in Ordnung.

## 23. Zusammenfassung der Funktionen

| Funktion | Aufgabe |
|---|---|
| `eingabe_zahl` | Fragt eine gültige ganze Zahl ab. |
| `eingabe_text` | Fragt nicht-leeren Text ab. |
| `eingabe_schwierigkeit` | Fragt `leicht`, `mittel` oder `schwer` ab. |
| `projekt_erstellen` | Erstellt ein neues Lernprojekt. |
| `lernplan_erstellen` | Erstellt automatisch den Lernplan. |
| `plan_anzeigen` | Zeigt den Lernplan im Terminal. |
| `statistik_anzeigen` | Berechnet und zeigt Fortschritt, Zeit und Hinweis. |
| `aufgabe_erledigen` | Markiert eine Aufgabe als abgeschlossen. |
| `speichern` | Speichert den Lernplan als JSON. |
| `laden` | Lädt den Lernplan aus JSON. |
| `exportieren` | Exportiert den Lernplan als TXT. |
| `menue_anzeigen` | Zeigt das Hauptmenü. |
| `main` | Steuert das komplette Programm. |

## 24. Gesamtfazit

`index.py` ist ein kompaktes, aber vollständiges Konsolenprogramm zur Lernplanung. Es nutzt wichtige Python-Grundlagen wie Funktionen, Klassen, Listen, Dictionaries, Schleifen, Bedingungen, Dateioperationen, JSON, Fehlerbehandlung und Generator-Ausdrücke.

Die wichtigste Idee ist, dass aus Themen und Schwierigkeitsgraden automatisch ein sinnvoller Lernplan erzeugt wird. Schwere Themen werden durch Gewichtung häufiger eingeplant. Am Ende gibt es Wiederholung und bei längeren Plänen eine Prüfungsvorbereitung.

Der Code ist an vielen Stellen bewusst kompakt geschrieben. Das zeigt fortgeschrittenere Python-Techniken, macht manche Stellen aber auch schwerer lesbar. Besonders das Aktions-Dictionary mit `lambda` und die aktuelle doppelte Themenabfrage sind Stellen, die man im Gespräch mit dem Lehrer gut als mögliche Verbesserung erklären kann.

