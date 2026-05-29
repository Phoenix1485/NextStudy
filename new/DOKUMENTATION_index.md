# Dokumentation zu `index.py`

Diese Dokumentation beschreibt die Datei `index.py` aus dem Ordner `new` vollständig und möglichst genau. Das Programm heißt **NextStudy Lite** und ist ein Konsolenprogramm zur Erstellung, Anzeige, Speicherung und Auswertung eines persönlichen Lernplans.

## 1. Allgemeine Beschreibung

`index.py` ist ein Python-Programm, das über ein Textmenü im Terminal bedient wird. Der Benutzer kann:

- ein neues Lernprojekt erstellen,
- Themen mit Schwierigkeitsgrad eintragen,
- automatisch einen Lernplan erzeugen lassen,
- Aufgaben als erledigt markieren,
- eine Statistik anzeigen,
- einen zufälligen Lerntipp ausgeben,
- den Lernplan als JSON-Datei speichern,
- einen gespeicherten Lernplan laden,
- den Lernplan als TXT-Datei exportieren.

Das Programm arbeitet objektorientiert mit zwei Klassen:

- `Thema`: speichert ein einzelnes Lernthema.
- `Lerneinheit`: speichert eine Aufgabe an einem bestimmten Lerntag.

Zusätzlich gibt es viele Funktionen, die jeweils eine bestimmte Aufgabe übernehmen.

## 2. Verwendete Imports

### Zeile 1: `import json`

Das Modul `json` wird verwendet, um Daten in einer JSON-Datei zu speichern und wieder daraus zu laden.

JSON steht für "JavaScript Object Notation" und ist ein Textformat zur Speicherung strukturierter Daten. In diesem Programm wird es für die Datei `nextstudy_plan.json` verwendet.

Verwendete Funktionen aus `json`:

- `json.dump(...)`: schreibt Python-Daten in eine JSON-Datei.
- `json.load(...)`: liest JSON-Daten aus einer Datei zurück in Python.

### Zeile 2: `import random`

Das Modul `random` wird verwendet, um zufällig einen Lerntipp auszuwählen.

Verwendete Funktion:

- `random.choice(tipps)`: wählt ein zufälliges Element aus der Liste `tipps`.

### Zeile 3: `from pathlib import Path`

Aus dem Modul `pathlib` wird die Klasse `Path` importiert. Damit kann geprüft werden, ob eine Datei existiert.

Verwendete Methode:

- `pfad.exists()`: gibt `True` zurück, wenn die Datei existiert, sonst `False`.

## 3. Globale Konstanten

### Zeile 6: `SAVE_FILE = "nextstudy_plan.json"`

`SAVE_FILE` speichert den Dateinamen, in dem der Lernplan als JSON gespeichert wird.

Diese Konstante wird in folgenden Funktionen verwendet:

- `speichern(...)`
- `laden()`

Vorteil: Wenn der Dateiname geändert werden soll, muss man ihn nur an einer Stelle ändern.

### Zeile 7: `EXPORT_FILE = "nextstudy_export.txt"`

`EXPORT_FILE` speichert den Dateinamen für den TXT-Export.

Diese Konstante wird in der Funktion `exportieren(...)` verwendet.

## 4. Klasse `Thema`

Die Klasse `Thema` beschreibt ein einzelnes Thema, das gelernt werden soll.

Beispiel:

```python
Thema("Bruchrechnung", "schwer")
```

Dieses Objekt hätte:

- `name = "Bruchrechnung"`
- `schwierigkeit = "schwer"`
- `gewichtung = 3`

### Zeilen 10 bis 14: Konstruktor `__init__`

```python
class Thema:
    def __init__(self, name, schwierigkeit):
        self.name = name
        self.schwierigkeit = schwierigkeit
        self.gewichtung = self.berechne_gewichtung()
```

Der Konstruktor wird automatisch aufgerufen, wenn ein neues `Thema`-Objekt erstellt wird.

Parameter:

- `name`: Name des Themas, zum Beispiel `"Vokabeln"` oder `"Ableitungen"`.
- `schwierigkeit`: Schwierigkeitsgrad des Themas. Erlaubt sind `"leicht"`, `"mittel"` und `"schwer"`.

Attribute:

- `self.name`: speichert den Namen des Themas im Objekt.
- `self.schwierigkeit`: speichert die Schwierigkeit im Objekt.
- `self.gewichtung`: speichert eine Zahl, die von der Schwierigkeit abhängt.

Was bedeutet `self`?

`self` bezeichnet das aktuelle Objekt. Wenn also ein Thema erstellt wird, gehören `self.name`, `self.schwierigkeit` und `self.gewichtung` genau zu diesem einen Thema.

Warum gibt es `gewichtung`?

Die Gewichtung sorgt dafür, dass schwere Themen im Lernplan häufiger vorkommen als leichte Themen.

### Zeilen 16 bis 23: Methode `berechne_gewichtung`

```python
def berechne_gewichtung(self):
    if self.schwierigkeit == "leicht":
        return 1
    if self.schwierigkeit == "mittel":
        return 2
    if self.schwierigkeit == "schwer":
        return 3
    return 2
```

Diese Methode wandelt die Schwierigkeit in eine Zahl um.

Regeln:

- `"leicht"` wird zu `1`
- `"mittel"` wird zu `2`
- `"schwer"` wird zu `3`
- alle anderen Werte werden sicherheitshalber zu `2`

Der letzte `return 2` ist eine Art Standardwert. Eigentlich sollte er nicht gebraucht werden, weil die Eingabe vorher geprüft wird. Trotzdem macht er das Programm stabiler, falls irgendwann ein ungültiger Wert in ein `Thema` gelangt.

### Zeilen 25 bis 30: Methode `to_dict`

```python
def to_dict(self):
    return {
        "name": self.name,
        "schwierigkeit": self.schwierigkeit,
        "gewichtung": self.gewichtung
    }
```

Diese Methode wandelt ein `Thema`-Objekt in ein Dictionary um.

Warum ist das nötig?

Python-Objekte wie `Thema` können nicht direkt sauber als JSON gespeichert werden. Dictionaries können aber problemlos in JSON umgewandelt werden. Deshalb wird aus dem Objekt eine normale Datenstruktur gemacht.

Beispiel:

```python
Thema("Mathe", "schwer").to_dict()
```

Ergebnis:

```python
{
    "name": "Mathe",
    "schwierigkeit": "schwer",
    "gewichtung": 3
}
```

## 5. Klasse `Lerneinheit`

Die Klasse `Lerneinheit` beschreibt eine konkrete Aufgabe an einem Lerntag.

Beispiel:

```python
Lerneinheit(1, "Bruchrechnung", "Aufgaben üben", 45)
```

Dieses Objekt steht dann für eine Lerneinheit am Tag 1.

### Zeilen 33 bis 39: Konstruktor `__init__`

```python
class Lerneinheit:
    def __init__(self, tag, thema, aufgabe, dauer):
        self.tag = tag
        self.thema = thema
        self.aufgabe = aufgabe
        self.dauer = dauer
        self.status = "offen"
```

Parameter:

- `tag`: Nummer des Lerntages, zum Beispiel `1`, `2`, `3`.
- `thema`: Name des Themas oder Sonderthema wie `"Wiederholung"`.
- `aufgabe`: genaue Beschreibung, was gelernt werden soll.
- `dauer`: Lernzeit in Minuten.

Attribute:

- `self.tag`: speichert den Lerntag.
- `self.thema`: speichert das Thema der Einheit.
- `self.aufgabe`: speichert die konkrete Aufgabe.
- `self.dauer`: speichert die Dauer in Minuten.
- `self.status`: speichert, ob die Aufgabe noch offen oder schon abgeschlossen ist.

Der Status ist am Anfang immer `"offen"`, weil eine neue Aufgabe noch nicht erledigt wurde.

### Zeilen 41 bis 42: Methode `erledigen`

```python
def erledigen(self):
    self.status = "abgeschlossen"
```

Diese Methode markiert eine Aufgabe als erledigt.

Vorher:

```python
status = "offen"
```

Nach dem Aufruf:

```python
status = "abgeschlossen"
```

Sie wird in `aufgabe_erledigen(...)` verwendet.

### Zeilen 44 bis 51: Methode `to_dict`

```python
def to_dict(self):
    return {
        "tag": self.tag,
        "thema": self.thema,
        "aufgabe": self.aufgabe,
        "dauer": self.dauer,
        "status": self.status
    }
```

Diese Methode wandelt eine `Lerneinheit` in ein Dictionary um, damit sie später als JSON gespeichert werden kann.

## 6. Eingabefunktionen

Diese Funktionen sorgen dafür, dass Benutzereingaben geprüft werden. Dadurch wird verhindert, dass falsche oder leere Eingaben das Programm kaputt machen.

### Zeilen 54 bis 62: Funktion `zahl_eingeben`

```python
def zahl_eingeben(frage, minimum=1):
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

Diese Funktion fragt so lange nach einer Zahl, bis der Benutzer eine gültige ganze Zahl eingibt.

Parameter:

- `frage`: Text, der dem Benutzer angezeigt wird.
- `minimum`: kleinster erlaubter Wert. Standardwert ist `1`.

Wichtige Bestandteile:

- `while True`: Endlosschleife, die erst durch `return` verlassen wird.
- `input(frage)`: liest eine Eingabe vom Benutzer.
- `int(...)`: wandelt die Eingabe in eine ganze Zahl um.
- `try`: versucht, den Code auszuführen.
- `except ValueError`: fängt den Fehler ab, wenn die Eingabe keine ganze Zahl ist.
- `if wert >= minimum`: prüft, ob die Zahl groß genug ist.
- `return wert`: gibt die gültige Zahl zurück und beendet die Funktion.

Beispiel:

Wenn der Benutzer `"abc"` eingibt, kann Python daraus keine Zahl machen. Dann entsteht ein `ValueError`, und das Programm zeigt eine Fehlermeldung an statt abzustürzen.

### Zeilen 65 bis 70: Funktion `text_eingeben`

```python
def text_eingeben(frage):
    while True:
        text = input(frage).strip()
        if text:
            return text
        print("Die Eingabe darf nicht leer sein.")
```

Aufgabe:

Diese Funktion fragt so lange nach Text, bis der Benutzer wirklich etwas eingegeben hat.

Parameter:

- `frage`: Text, der dem Benutzer angezeigt wird.

Wichtige Methode:

- `.strip()`: entfernt Leerzeichen am Anfang und Ende der Eingabe.

Beispiel:

```python
"   Mathe   ".strip()
```

Ergebnis:

```python
"Mathe"
```

Warum ist `.strip()` wichtig?

Ohne `.strip()` könnte der Benutzer nur Leerzeichen eingeben, und das Programm würde das als Text akzeptieren. Durch `.strip()` wird daraus ein leerer String, und die Eingabe wird abgelehnt.

Die Bedingung `if text:` bedeutet: Wenn der String nicht leer ist, ist er gültig.

### Zeilen 73 bis 78: Funktion `schwierigkeit_eingeben`

```python
def schwierigkeit_eingeben(thema):
    while True:
        wert = input(f"Schwierigkeit für '{thema}' (leicht/mittel/schwer): ").lower().strip()
        if wert in ["leicht", "mittel", "schwer"]:
            return wert
        print("Bitte nur leicht, mittel oder schwer eingeben.")
```

Aufgabe:

Diese Funktion fragt den Schwierigkeitsgrad eines Themas ab.

Parameter:

- `thema`: Name des Themas, damit die Frage genauer angezeigt werden kann.

Wichtige Methoden:

- `.lower()`: wandelt die Eingabe in Kleinbuchstaben um.
- `.strip()`: entfernt Leerzeichen am Anfang und Ende.

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
if wert in ["leicht", "mittel", "schwer"]:
```

Diese Zeile prüft, ob der eingegebene Wert in der Liste der erlaubten Werte enthalten ist.

## 7. Lernprojekt erstellen

### Zeilen 81 bis 95: Funktion `projekt_erstellen`

```python
def projekt_erstellen():
    print("\n===== Neues Lernprojekt =====")
    fach = text_eingeben("Fach eingeben: ")
    anzahl = zahl_eingeben("Wie viele Themen möchtest du eintragen? ", 1)
    themen = []

    for nummer in range(1, anzahl + 1):
        name = text_eingeben(f"Thema {nummer}: ")
        schwierigkeit = schwierigkeit_eingeben(name)
        themen.append(Thema(name, schwierigkeit))
    tage = zahl_eingeben("Wie viele Lerntage hast du? ", 1)
    lernzeit = zahl_eingeben("Wie viele Minuten lernst du pro Tag? ", 1)
    plan = lernplan_erstellen(themen, tage, lernzeit)
    print("\nLernprojekt wurde erstellt.")
    return fach, themen, tage, lernzeit, plan
```

Aufgabe:

Diese Funktion erstellt ein komplett neues Lernprojekt.

Ablauf:

1. Überschrift ausgeben.
2. Fach abfragen.
3. Anzahl der Themen abfragen.
4. Für jedes Thema Name und Schwierigkeit abfragen.
5. Aus den Angaben `Thema`-Objekte erstellen.
6. Anzahl der Lerntage abfragen.
7. Lernzeit pro Tag abfragen.
8. Daraus einen Lernplan erzeugen.
9. Alle wichtigen Daten zurückgeben.

Wichtige Variable:

- `themen = []`: eine leere Liste, in der alle Themen gespeichert werden.

Wichtige Methode:

- `.append(...)`: fügt ein neues Element an das Ende einer Liste an.

Beispiel:

```python
themen.append(Thema(name, schwierigkeit))
```

Diese Zeile erstellt ein neues `Thema`-Objekt und fügt es der Liste `themen` hinzu.

Wichtige Schleife:

```python
for nummer in range(1, anzahl + 1):
```

Diese Schleife läuft von `1` bis `anzahl`.

Warum `anzahl + 1`?

Bei `range` ist der Endwert nicht enthalten. Wenn also `anzahl` den Wert `3` hat, erzeugt `range(1, 4)` die Werte `1`, `2`, `3`.

Rückgabe:

```python
return fach, themen, tage, lernzeit, plan
```

Die Funktion gibt fünf Werte zurück. In `main()` werden diese Werte wieder in Variablen gespeichert.

## 8. Lernplan erzeugen

### Zeilen 98 bis 119: Funktion `lernplan_erstellen`

```python
def lernplan_erstellen(themen, tage, lernzeit):
    plan = []
    sortierte_themen = sorted(themen, key=lambda t: t.gewichtung, reverse=True)
    lernliste = gewichtete_themenliste(sortierte_themen)

    if tage == 1:
        aufgabe = "Alle Themen kompakt wiederholen und einen Selbsttest machen"
        return [Lerneinheit(1, "Wiederholung", aufgabe, lernzeit)]

    for tag in range(1, tage + 1):
        if tag == tage:
            einheit = wiederholungstag_erstellen(tag, lernzeit)
        elif tag == tage - 1 and tage >= 4:
            einheit = pruefungsvorbereitung_erstellen(tag, lernzeit)
        else:
            thema = lernliste[(tag - 1) % len(lernliste)]
            aufgabe = aufgabe_fuer_thema(thema)
            einheit = Lerneinheit(tag, thema.name, aufgabe, lernzeit)

        plan.append(einheit)

    return plan
```

Aufgabe:

Diese Funktion erstellt aus den Themen, der Anzahl der Tage und der Lernzeit einen Lernplan.

Parameter:

- `themen`: Liste von `Thema`-Objekten.
- `tage`: Anzahl der Lerntage.
- `lernzeit`: Minuten pro Tag.

Wichtige Variable:

- `plan = []`: leere Liste, in die später alle `Lerneinheit`-Objekte kommen.

### Sortierung mit `sorted`

```python
sortierte_themen = sorted(themen, key=lambda t: t.gewichtung, reverse=True)
```

Diese Zeile sortiert die Themen nach ihrer Gewichtung.

Bestandteile:

- `sorted(themen, ...)`: sortiert die Liste `themen`.
- `key=lambda t: t.gewichtung`: sortiert nach dem Attribut `gewichtung`.
- `reverse=True`: sortiert absteigend, also höchste Gewichtung zuerst.

Was bedeutet `lambda t: t.gewichtung`?

Das ist eine kurze anonyme Funktion. Für jedes Thema `t` wird `t.gewichtung` als Sortierwert verwendet.

Beispiel:

- schwer: Gewichtung `3`
- mittel: Gewichtung `2`
- leicht: Gewichtung `1`

Durch `reverse=True` kommen schwere Themen zuerst.

### Gewichtete Themenliste

```python
lernliste = gewichtete_themenliste(sortierte_themen)
```

Hier wird aus den sortierten Themen eine neue Liste erstellt, in der schwere Themen mehrfach vorkommen.

Beispiel:

- Thema A ist schwer und hat Gewichtung 3.
- Thema B ist leicht und hat Gewichtung 1.

Dann wird daraus ungefähr:

```python
[A, A, A, B]
```

Dadurch wird Thema A häufiger im Lernplan ausgewählt.

### Sonderfall: Nur ein Lerntag

```python
if tage == 1:
    aufgabe = "Alle Themen kompakt wiederholen und einen Selbsttest machen"
    return [Lerneinheit(1, "Wiederholung", aufgabe, lernzeit)]
```

Wenn es nur einen Lerntag gibt, lohnt sich kein mehrtägiger Plan. Das Programm erstellt deshalb direkt eine einzige Wiederholungseinheit.

### Hauptschleife über alle Tage

```python
for tag in range(1, tage + 1):
```

Diese Schleife erzeugt für jeden Tag eine Lerneinheit.

### Letzter Tag ist Wiederholungstag

```python
if tag == tage:
    einheit = wiederholungstag_erstellen(tag, lernzeit)
```

Wenn der aktuelle Tag der letzte Tag ist, wird ein Wiederholungstag erstellt.

### Vorletzter Tag ist Prüfungsvorbereitung

```python
elif tag == tage - 1 and tage >= 4:
    einheit = pruefungsvorbereitung_erstellen(tag, lernzeit)
```

Wenn es mindestens 4 Lerntage gibt, wird der vorletzte Tag zur Prüfungsvorbereitung.

Warum `tage >= 4`?

Bei sehr kurzen Lernplänen würde sonst zu wenig Zeit für normale Themen bleiben.

### Normale Lerntage

```python
thema = lernliste[(tag - 1) % len(lernliste)]
aufgabe = aufgabe_fuer_thema(thema)
einheit = Lerneinheit(tag, thema.name, aufgabe, lernzeit)
```

Hier wird ein Thema aus der gewichteten Liste gewählt.

Wichtig ist diese Stelle:

```python
(tag - 1) % len(lernliste)
```

Das ist der Modulo-Operator `%`.

Er sorgt dafür, dass der Index wieder vorne beginnt, wenn das Ende der Liste erreicht ist.

Beispiel:

Wenn `lernliste` 3 Elemente hat, sind gültige Indizes:

```python
0, 1, 2
```

Durch Modulo entstehen bei mehreren Tagen:

```python
0, 1, 2, 0, 1, 2, ...
```

Dadurch kann das Programm beliebig viele Tage füllen, auch wenn es nur wenige Themen gibt.

## 9. Gewichtete Themenliste

### Zeilen 122 bis 129: Funktion `gewichtete_themenliste`

```python
def gewichtete_themenliste(themen):
    lernliste = []

    for thema in themen:
        for _ in range(thema.gewichtung):
            lernliste.append(thema)

    return lernliste
```

Aufgabe:

Diese Funktion erstellt eine Liste, in der Themen je nach Schwierigkeit mehrfach enthalten sind.

Parameter:

- `themen`: Liste von `Thema`-Objekten.

Ablauf:

- Für jedes Thema wird geprüft, welche Gewichtung es hat.
- Das Thema wird so oft in `lernliste` eingefügt, wie die Gewichtung vorgibt.

Beispiel:

```python
Thema("A", "leicht")  # Gewichtung 1
Thema("B", "schwer")  # Gewichtung 3
```

Ergebnis:

```python
[A, B, B, B]
```

Was bedeutet `_`?

```python
for _ in range(thema.gewichtung):
```

Der Unterstrich `_` wird als Variablenname benutzt, wenn der eigentliche Wert nicht gebraucht wird. Die Schleife soll nur eine bestimmte Anzahl an Wiederholungen machen.

## 10. Aufgabe passend zum Thema erstellen

### Zeilen 132 bis 137: Funktion `aufgabe_fuer_thema`

```python
def aufgabe_fuer_thema(thema):
    if thema.schwierigkeit == "leicht":
        return f"{thema.name} lernen, kurze Notizen machen und einmal wiederholen"
    if thema.schwierigkeit == "mittel":
        return f"{thema.name} lernen, Beispiele anschauen und Aufgaben lösen"
    return f"{thema.name} intensiv lernen, Aufgaben üben und Fehler notieren"
```

Aufgabe:

Diese Funktion erstellt einen passenden Aufgabentext abhängig von der Schwierigkeit.

Parameter:

- `thema`: ein `Thema`-Objekt.

Logik:

- leicht: einfache Aufgabe mit Notizen und Wiederholung.
- mittel: Beispiele anschauen und Aufgaben lösen.
- schwer: intensives Lernen, Üben und Fehler notieren.

Warum gibt es am Ende kein `if schwierigkeit == "schwer"`?

Der letzte `return` wird verwendet, wenn die Schwierigkeit nicht `"leicht"` oder `"mittel"` ist. Da die Eingabe vorher nur `"leicht"`, `"mittel"` oder `"schwer"` erlaubt, bedeutet das praktisch: Der letzte Fall ist `"schwer"`.

## 11. Sondertage erstellen

### Zeilen 140 bis 142: Funktion `wiederholungstag_erstellen`

```python
def wiederholungstag_erstellen(tag, lernzeit):
    aufgabe = "Alle Themen wiederholen, offene Fragen klären und Mini-Selbsttest machen"
    return Lerneinheit(tag, "Wiederholung", aufgabe, lernzeit)
```

Aufgabe:

Diese Funktion erstellt eine Lerneinheit für den Wiederholungstag.

Der Wiederholungstag ist immer der letzte Tag des Plans.

Rückgabe:

Ein neues `Lerneinheit`-Objekt mit:

- Thema: `"Wiederholung"`
- Aufgabe: Wiederholen, Fragen klären, Mini-Selbsttest
- Dauer: die normale Lernzeit pro Tag

### Zeilen 145 bis 147: Funktion `pruefungsvorbereitung_erstellen`

```python
def pruefungsvorbereitung_erstellen(tag, lernzeit):
    aufgabe = "Schwächen wiederholen, Zusammenfassung lesen und Beispielaufgaben lösen"
    return Lerneinheit(tag, "Prüfungsvorbereitung", aufgabe, lernzeit)
```

Aufgabe:

Diese Funktion erstellt eine Lerneinheit für die Prüfungsvorbereitung.

Sie wird im Lernplan am vorletzten Tag verwendet, aber nur wenn es mindestens 4 Lerntage gibt.

## 12. Lernplan anzeigen

### Zeilen 150 bis 162: Funktion `plan_anzeigen`

```python
def plan_anzeigen(fach, plan):
    if not plan:
        print("\nEs wurde noch kein Lernplan erstellt.")
        return

    print(f"\n===== Lernplan für {fach} =====")

    for index, einheit in enumerate(plan, start=1):
        print(f"\n[{index}] Tag {einheit.tag}")
        print(f"Thema:   {einheit.thema}")
        print(f"Aufgabe: {einheit.aufgabe}")
        print(f"Dauer:   {einheit.dauer} Minuten")
        print(f"Status:  {einheit.status}")
```

Aufgabe:

Diese Funktion gibt den aktuellen Lernplan im Terminal aus.

Parameter:

- `fach`: Name des Fachs.
- `plan`: Liste von `Lerneinheit`-Objekten.

Wichtige Prüfung:

```python
if not plan:
```

Diese Bedingung prüft, ob die Liste leer ist. Eine leere Liste gilt in Python als `False`.

Wenn kein Plan vorhanden ist, wird eine Meldung angezeigt und die Funktion mit `return` beendet.

### `enumerate`

```python
for index, einheit in enumerate(plan, start=1):
```

`enumerate` liefert gleichzeitig:

- den Zähler `index`
- das aktuelle Element `einheit`

Durch `start=1` beginnt die Anzeige bei 1 statt bei 0. Das ist benutzerfreundlicher, weil Menschen meistens ab 1 zählen.

## 13. Aufgabe als erledigt markieren

### Zeilen 165 bis 178: Funktion `aufgabe_erledigen`

```python
def aufgabe_erledigen(fach, plan):
    if not plan:
        print("\nEs gibt noch keinen Lernplan.")
        return

    plan_anzeigen(fach, plan)
    nummer = zahl_eingeben("\nWelche Aufgabe wurde erledigt? Nummer eingeben: ", 1)

    if nummer > len(plan):
        print("Diese Aufgabe existiert nicht.")
        return

    plan[nummer - 1].erledigen()
    print("Aufgabe wurde als abgeschlossen markiert.")
```

Aufgabe:

Diese Funktion lässt den Benutzer eine Aufgabe auswählen und markiert sie als abgeschlossen.

Ablauf:

1. Prüfen, ob ein Plan existiert.
2. Plan anzeigen.
3. Nummer der erledigten Aufgabe abfragen.
4. Prüfen, ob die Nummer im gültigen Bereich liegt.
5. Passende Lerneinheit auf `"abgeschlossen"` setzen.

Wichtige Stelle:

```python
plan[nummer - 1].erledigen()
```

Warum `nummer - 1`?

Listen beginnen in Python bei Index `0`. Der Benutzer sieht aber Nummern ab `1`.

Beispiel:

- Benutzer wählt `1`.
- Python braucht Index `0`.
- Deshalb wird `nummer - 1` gerechnet.

Dann wird auf dem passenden `Lerneinheit`-Objekt die Methode `.erledigen()` aufgerufen.

## 14. Statistik anzeigen

### Zeilen 181 bis 199: Funktion `statistik_anzeigen`

```python
def statistik_anzeigen(plan):
    if not plan:
        print("\nEs gibt noch keinen Lernplan.")
        return

    erledigt = sum(1 for einheit in plan if einheit.status == "abgeschlossen")
    offen = len(plan) - erledigt
    minuten_gesamt = sum(einheit.dauer for einheit in plan)
    minuten_erledigt = sum(einheit.dauer for einheit in plan if einheit.status == "abgeschlossen")
    prozent = round((erledigt / len(plan)) * 100)

    print("\n===== Statistik =====")
    print(f"Aufgaben gesamt:      {len(plan)}")
    print(f"Abgeschlossen:        {erledigt}")
    print(f"Offen:                {offen}")
    print(f"Lernzeit gesamt:      {minuten_gesamt} Minuten")
    print(f"Erledigte Lernzeit:   {minuten_erledigt} Minuten")
    print(f"Fortschritt:          {prozent} %")
    print(f"Hinweis:              {motivation(prozent)}")
```

Aufgabe:

Diese Funktion berechnet und zeigt den Lernfortschritt.

Berechnete Werte:

- Gesamtanzahl der Aufgaben.
- Anzahl abgeschlossener Aufgaben.
- Anzahl offener Aufgaben.
- gesamte Lernzeit.
- erledigte Lernzeit.
- Fortschritt in Prozent.
- Motivationstext abhängig vom Fortschritt.

### Abgeschlossene Aufgaben zählen

```python
erledigt = sum(1 for einheit in plan if einheit.status == "abgeschlossen")
```

Diese Zeile zählt alle Lerneinheiten, deren Status `"abgeschlossen"` ist.

Wichtig: Hier wird kein `.filter()` benutzt. Python verwendet hier einen Generator-Ausdruck mit einer `if`-Bedingung.

Erklärung:

- `for einheit in plan`: geht jede Lerneinheit durch.
- `if einheit.status == "abgeschlossen"`: nimmt nur abgeschlossene Einheiten.
- `1`: für jede passende Einheit wird eine `1` erzeugt.
- `sum(...)`: addiert alle Einsen.

Beispiel:

Wenn 3 Aufgaben abgeschlossen sind, entsteht ungefähr:

```python
sum([1, 1, 1])
```

Ergebnis:

```python
3
```

### Offene Aufgaben berechnen

```python
offen = len(plan) - erledigt
```

`len(plan)` gibt die Gesamtanzahl aller Aufgaben zurück. Davon werden die erledigten Aufgaben abgezogen.

### Gesamte Lernzeit berechnen

```python
minuten_gesamt = sum(einheit.dauer for einheit in plan)
```

Diese Zeile addiert die Dauer aller Lerneinheiten.

### Erledigte Lernzeit berechnen

```python
minuten_erledigt = sum(einheit.dauer for einheit in plan if einheit.status == "abgeschlossen")
```

Diese Zeile addiert nur die Dauer der erledigten Aufgaben.

Auch hier gibt es kein `.filter()`. Die Filterung passiert durch die `if`-Bedingung im Generator-Ausdruck.

### Prozent berechnen

```python
prozent = round((erledigt / len(plan)) * 100)
```

Diese Zeile berechnet den Fortschritt.

Formel:

```python
erledigte Aufgaben / alle Aufgaben * 100
```

`round(...)` rundet das Ergebnis auf eine ganze Zahl.

## 15. Motivationstext

### Zeilen 202 bis 219: Funktion `motivation`

```python
def motivation(prozent):
    texte = {
        0: "Starte mit der ersten Aufgabe. Danach wird es einfacher.",
        25: "Guter Anfang. Bleib dran.",
        50: "Die Hälfte ist geschafft.",
        75: "Fast fertig. Jetzt nicht nachlassen.",
        100: "Alles abgeschlossen. Gute Vorbereitung."
    }

    if prozent == 100:
        return texte[100]
    if prozent >= 75:
        return texte[75]
    if prozent >= 50:
        return texte[50]
    if prozent >= 25:
        return texte[25]
    return texte[0]
```

Aufgabe:

Diese Funktion gibt je nach Fortschritt einen passenden Motivationstext zurück.

Wichtige Datenstruktur:

```python
texte = {
    0: "...",
    25: "...",
    50: "...",
    75: "...",
    100: "..."
}
```

Das ist ein Dictionary. Es ordnet Zahlen bestimmten Texten zu.

Beispiel:

```python
texte[50]
```

liefert:

```python
"Die Hälfte ist geschafft."
```

Die Reihenfolge der `if`-Abfragen ist wichtig:

- Erst wird geprüft, ob 100 Prozent erreicht sind.
- Danach werden 75, 50 und 25 Prozent geprüft.
- Wenn nichts davon zutrifft, wird der Text für 0 Prozent zurückgegeben.

## 16. Tipp des Tages

### Zeilen 222 bis 231: Funktion `tages_tipp_anzeigen`

```python
def tages_tipp_anzeigen():
    tipps = [
        "Lerne lieber 45 Minuten konzentriert als 3 Stunden abgelenkt.",
        "Schreibe Fehler auf, damit du sie am Ende gezielt wiederholen kannst.",
        "Schwere Themen solltest du zuerst bearbeiten.",
        "Mache nach jeder Lerneinheit eine kurze Pause.",
        "Erkläre ein Thema laut, um zu prüfen, ob du es verstanden hast."
    ]
    print("\nTipp des Tages:")
    print(random.choice(tipps))
```

Aufgabe:

Diese Funktion zeigt einen zufälligen Lerntipp an.

Wichtige Bestandteile:

- `tipps`: Liste mit mehreren Tipp-Texten.
- `random.choice(tipps)`: wählt zufällig einen Tipp aus der Liste.
- `print(...)`: gibt den Tipp im Terminal aus.

## 17. Lernplan speichern

### Zeilen 234 bis 250: Funktion `speichern`

```python
def speichern(fach, themen, tage, lernzeit, plan):
    if not plan:
        print("\nEs gibt keinen Lernplan zum Speichern.")
        return

    daten = {
        "fach": fach,
        "tage": tage,
        "lernzeit": lernzeit,
        "themen": [thema.to_dict() for thema in themen],
        "plan": [einheit.to_dict() for einheit in plan]
    }

    with open(SAVE_FILE, "w", encoding="utf-8") as datei:
        json.dump(daten, datei, indent=4, ensure_ascii=False)

    print(f"Lernplan wurde in '{SAVE_FILE}' gespeichert.")
```

Aufgabe:

Diese Funktion speichert den aktuellen Lernplan in einer JSON-Datei.

Parameter:

- `fach`: Fachname.
- `themen`: Liste der Themen.
- `tage`: Anzahl der Lerntage.
- `lernzeit`: Lernzeit pro Tag.
- `plan`: Liste der Lerneinheiten.

### Prüfung auf vorhandenen Plan

```python
if not plan:
```

Wenn kein Lernplan existiert, wird nichts gespeichert.

### Dictionary `daten`

```python
daten = {
    "fach": fach,
    "tage": tage,
    "lernzeit": lernzeit,
    "themen": [thema.to_dict() for thema in themen],
    "plan": [einheit.to_dict() for einheit in plan]
}
```

Dieses Dictionary enthält alle Daten, die gespeichert werden müssen.

Die Zeilen:

```python
[thema.to_dict() for thema in themen]
[einheit.to_dict() for einheit in plan]
```

sind List Comprehensions. Sie wandeln jedes Objekt in ein Dictionary um.

Warum?

JSON kann einfache Datentypen wie Strings, Zahlen, Listen und Dictionaries speichern. Eigene Klassenobjekte müssen vorher umgewandelt werden.

### Datei öffnen

```python
with open(SAVE_FILE, "w", encoding="utf-8") as datei:
```

Erklärung:

- `open(...)`: öffnet eine Datei.
- `SAVE_FILE`: Name der Datei, also `nextstudy_plan.json`.
- `"w"`: write-Modus. Die Datei wird zum Schreiben geöffnet. Falls sie existiert, wird sie überschrieben.
- `encoding="utf-8"`: sorgt dafür, dass Umlaute wie ä, ö, ü korrekt gespeichert werden.
- `with`: sorgt dafür, dass die Datei automatisch wieder geschlossen wird.

### JSON schreiben

```python
json.dump(daten, datei, indent=4, ensure_ascii=False)
```

Erklärung:

- `daten`: die zu speichernden Daten.
- `datei`: die geöffnete Datei.
- `indent=4`: formatiert die JSON-Datei schön mit Einrückung.
- `ensure_ascii=False`: sorgt dafür, dass Umlaute lesbar bleiben und nicht als Unicode-Codes gespeichert werden.

## 18. Lernplan laden

### Zeilen 253 bis 275: Funktion `laden`

```python
def laden():
    pfad = Path(SAVE_FILE)

    if not pfad.exists():
        print("\nEs wurde keine Speicherdatei gefunden.")
        return "", [], 0, 0, []

    with open(SAVE_FILE, "r", encoding="utf-8") as datei:
        daten = json.load(datei)

    fach = daten["fach"]
    tage = daten["tage"]
    lernzeit = daten["lernzeit"]
    themen = [Thema(e["name"], e["schwierigkeit"]) for e in daten["themen"]]
    plan = []

    for eintrag in daten["plan"]:
        einheit = Lerneinheit(eintrag["tag"], eintrag["thema"], eintrag["aufgabe"], eintrag["dauer"])
        einheit.status = eintrag["status"]
        plan.append(einheit)

    print("Lernplan wurde geladen.")
    return fach, themen, tage, lernzeit, plan
```

Aufgabe:

Diese Funktion lädt einen gespeicherten Lernplan aus der Datei `nextstudy_plan.json`.

### Pfad erstellen

```python
pfad = Path(SAVE_FILE)
```

Hier wird aus dem Dateinamen ein `Path`-Objekt erstellt.

### Prüfen, ob die Datei existiert

```python
if not pfad.exists():
```

`.exists()` prüft, ob die Speicherdatei vorhanden ist.

Wenn die Datei nicht existiert, gibt die Funktion leere Standardwerte zurück:

```python
return "", [], 0, 0, []
```

Bedeutung:

- leeres Fach
- leere Themenliste
- `0` Tage
- `0` Lernzeit
- leerer Plan

### Datei lesen

```python
with open(SAVE_FILE, "r", encoding="utf-8") as datei:
    daten = json.load(datei)
```

Erklärung:

- `"r"` bedeutet read-Modus, also lesen.
- `json.load(datei)` liest die JSON-Datei und macht daraus wieder Python-Daten.

### Daten wiederherstellen

```python
fach = daten["fach"]
tage = daten["tage"]
lernzeit = daten["lernzeit"]
```

Hier werden einfache Werte aus dem Dictionary gelesen.

### Themen wiederherstellen

```python
themen = [Thema(e["name"], e["schwierigkeit"]) for e in daten["themen"]]
```

Diese List Comprehension erstellt aus den gespeicherten Dictionaries wieder echte `Thema`-Objekte.

### Plan wiederherstellen

```python
for eintrag in daten["plan"]:
    einheit = Lerneinheit(eintrag["tag"], eintrag["thema"], eintrag["aufgabe"], eintrag["dauer"])
    einheit.status = eintrag["status"]
    plan.append(einheit)
```

Für jeden gespeicherten Eintrag wird ein neues `Lerneinheit`-Objekt erstellt.

Wichtig:

```python
einheit.status = eintrag["status"]
```

Der Status wird extra gesetzt, weil der Konstruktor von `Lerneinheit` den Status immer zuerst auf `"offen"` setzt. Beim Laden soll aber der gespeicherte Status übernommen werden.

## 19. Lernplan exportieren

### Zeilen 278 bis 295: Funktion `exportieren`

```python
def exportieren(fach, plan):
    if not plan:
        print("\nEs gibt keinen Lernplan zum Exportieren.")
        return

    zeilen = [f"NextStudy Lite - Lernplan für {fach}", "=" * 40, ""]

    for einheit in plan:
        zeilen.append(f"Tag {einheit.tag}: {einheit.thema}")
        zeilen.append(f"Aufgabe: {einheit.aufgabe}")
        zeilen.append(f"Dauer: {einheit.dauer} Minuten")
        zeilen.append(f"Status: {einheit.status}")
        zeilen.append("")

    with open(EXPORT_FILE, "w", encoding="utf-8") as datei:
        datei.write("\n".join(zeilen))

    print(f"Lernplan wurde als '{EXPORT_FILE}' exportiert.")
```

Aufgabe:

Diese Funktion exportiert den Lernplan als normale Textdatei.

### Liste `zeilen`

```python
zeilen = [f"NextStudy Lite - Lernplan für {fach}", "=" * 40, ""]
```

Diese Liste enthält alle Zeilen, die später in die TXT-Datei geschrieben werden.

Wichtige Stelle:

```python
"=" * 40
```

Das erzeugt 40 Gleichheitszeichen als Trennlinie.

### Zeilen hinzufügen

```python
zeilen.append(...)
```

Mit `.append()` wird jede Textzeile an die Liste angehängt.

### Textdatei schreiben

```python
datei.write("\n".join(zeilen))
```

`.join(zeilen)` verbindet alle Elemente der Liste zu einem großen String.

`"\n"` bedeutet Zeilenumbruch.

Dadurch steht jede gespeicherte Zeile später in der Datei auf einer eigenen Zeile.

## 20. Menü anzeigen

### Zeilen 298 bis 310: Funktion `menue_anzeigen`

```python
def menue_anzeigen():
    print("\n========================")
    print("     NEXTSTUDY LITE")
    print("========================")
    print("1. Neues Lernprojekt erstellen")
    print("2. Lernplan anzeigen")
    print("3. Aufgabe als erledigt markieren")
    print("4. Statistik anzeigen")
    print("5. Tipp des Tages anzeigen")
    print("6. Lernplan speichern")
    print("7. Lernplan laden")
    print("8. Lernplan als TXT exportieren")
    print("9. Beenden")
```

Aufgabe:

Diese Funktion zeigt das Hauptmenü im Terminal an.

Sie enthält keine Berechnungen, sondern nur `print(...)`-Anweisungen.

## 21. Hauptfunktion `main`

### Zeilen 313 bis 344: Funktion `main`

```python
def main():
    fach = ""
    themen = []
    tage = 0
    lernzeit = 0
    plan = []

    while True:
        menue_anzeigen()
        auswahl = input("Auswahl: ").strip()

        if auswahl == "1":
            fach, themen, tage, lernzeit, plan = projekt_erstellen()
        elif auswahl == "2":
            plan_anzeigen(fach, plan)
        elif auswahl == "3":
            aufgabe_erledigen(fach, plan)
        elif auswahl == "4":
            statistik_anzeigen(plan)
        elif auswahl == "5":
            tages_tipp_anzeigen()
        elif auswahl == "6":
            speichern(fach, themen, tage, lernzeit, plan)
        elif auswahl == "7":
            fach, themen, tage, lernzeit, plan = laden()
        elif auswahl == "8":
            exportieren(fach, plan)
        elif auswahl == "9":
            print("NextStudy Lite wird beendet.")
            break
        else:
            print("Ungültige Auswahl.")
```

Aufgabe:

`main()` ist die zentrale Steuerfunktion des Programms.

Sie:

- legt Startwerte an,
- zeigt immer wieder das Menü,
- liest die Auswahl des Benutzers,
- ruft abhängig von der Auswahl die passende Funktion auf,
- beendet das Programm bei Auswahl `9`.

### Startwerte

```python
fach = ""
themen = []
tage = 0
lernzeit = 0
plan = []
```

Diese Variablen speichern den aktuellen Zustand des Programms.

Bedeutung:

- `fach`: Name des Fachs.
- `themen`: Liste aller Themen.
- `tage`: Anzahl der Lerntage.
- `lernzeit`: Minuten pro Tag.
- `plan`: Liste aller Lerneinheiten.

Am Anfang sind diese Werte leer oder `0`, weil noch kein Lernprojekt erstellt wurde.

### Endlosschleife

```python
while True:
```

Das Menü wird immer wieder angezeigt, bis der Benutzer das Programm beendet.

### Benutzerauswahl

```python
auswahl = input("Auswahl: ").strip()
```

Der Benutzer gibt eine Zahl als Text ein.

`.strip()` entfernt unnötige Leerzeichen.

Die Auswahl bleibt ein String, weil sie später mit `"1"`, `"2"` usw. verglichen wird.

### `if`, `elif`, `else`

Die Auswahl wird mit mehreren Bedingungen geprüft.

Beispiel:

```python
if auswahl == "1":
    fach, themen, tage, lernzeit, plan = projekt_erstellen()
```

Wenn der Benutzer `"1"` eingibt, wird ein neues Projekt erstellt.

Bei Auswahl `"9"`:

```python
break
```

`break` beendet die `while True`-Schleife. Dadurch endet das Programm.

## 22. Programmstart

### Zeilen 347 bis 348

```python
if __name__ == "__main__":
    main()
```

Diese Zeilen sorgen dafür, dass `main()` nur dann automatisch gestartet wird, wenn die Datei direkt ausgeführt wird.

Wenn man also im Terminal schreibt:

```bash
python3 index.py
```

dann ist `__name__` gleich `"__main__"` und `main()` wird gestartet.

Wenn die Datei aber von einer anderen Python-Datei importiert würde, dann würde `main()` nicht automatisch starten.

## 23. Wichtige Python-Methoden und Begriffe im Code

### `.strip()`

Entfernt Leerzeichen und Zeilenumbrüche am Anfang und Ende eines Strings.

Verwendet in:

- `text_eingeben`
- `schwierigkeit_eingeben`
- `main`

### `.lower()`

Wandelt einen String in Kleinbuchstaben um.

Verwendet in:

- `schwierigkeit_eingeben`

### `.append(...)`

Fügt ein Element an das Ende einer Liste an.

Verwendet in:

- `projekt_erstellen`
- `lernplan_erstellen`
- `gewichtete_themenliste`
- `laden`
- `exportieren`

### `.exists()`

Prüft, ob eine Datei oder ein Ordner existiert.

Verwendet in:

- `laden`

### `.to_dict()`

Eigene Methode in den Klassen `Thema` und `Lerneinheit`.

Sie wandelt Objekte in Dictionaries um, damit sie gespeichert werden können.

### Gibt es `.filter()` im Code?

Nein. In dieser Datei wird keine Methode oder Funktion `.filter()` verwendet.

Das Filtern passiert stattdessen über `if`-Bedingungen in Generator-Ausdrücken.

Beispiel:

```python
sum(1 for einheit in plan if einheit.status == "abgeschlossen")
```

Diese Zeile filtert gedanklich alle abgeschlossenen Lerneinheiten heraus, aber ohne eine `.filter()`-Funktion zu benutzen.

## 24. Datenfluss im Programm

Der typische Ablauf ist:

1. `main()` startet.
2. `menue_anzeigen()` zeigt das Menü.
3. Benutzer wählt `1`.
4. `projekt_erstellen()` fragt Fach, Themen, Tage und Lernzeit ab.
5. Für jedes Thema wird ein `Thema`-Objekt erstellt.
6. `lernplan_erstellen()` erstellt daraus mehrere `Lerneinheit`-Objekte.
7. Der Plan kann angezeigt, gespeichert, geladen oder exportiert werden.
8. Aufgaben können mit `aufgabe_erledigen()` abgeschlossen werden.
9. `statistik_anzeigen()` berechnet den Fortschritt.
10. Bei Auswahl `9` wird die Schleife beendet.

## 25. Warum das Programm sinnvoll strukturiert ist

Das Programm ist in viele kleine Funktionen aufgeteilt. Das hat Vorteile:

- Jede Funktion hat eine klare Aufgabe.
- Der Code ist leichter zu verstehen.
- Fehler lassen sich leichter finden.
- Funktionen können mehrfach verwendet werden.
- Klassen sorgen dafür, dass zusammengehörige Daten zusammen gespeichert werden.

Beispiele:

- Die Eingabeprüfung steht in eigenen Funktionen.
- Die Planerstellung steht getrennt von der Anzeige.
- Speichern und Laden sind eigene Funktionen.
- Themen und Lerneinheiten sind eigene Klassen.

## 26. Zusammenfassung der wichtigsten Funktionen

| Funktion | Aufgabe |
|---|---|
| `zahl_eingeben` | Fragt eine gültige ganze Zahl ab. |
| `text_eingeben` | Fragt nicht-leeren Text ab. |
| `schwierigkeit_eingeben` | Fragt `leicht`, `mittel` oder `schwer` ab. |
| `projekt_erstellen` | Erstellt ein neues Lernprojekt. |
| `lernplan_erstellen` | Erstellt den automatischen Lernplan. |
| `gewichtete_themenliste` | Lässt schwere Themen häufiger vorkommen. |
| `aufgabe_fuer_thema` | Erstellt passende Aufgaben je Schwierigkeit. |
| `wiederholungstag_erstellen` | Erstellt den letzten Wiederholungstag. |
| `pruefungsvorbereitung_erstellen` | Erstellt den Prüfungsvorbereitungstag. |
| `plan_anzeigen` | Gibt den Lernplan aus. |
| `aufgabe_erledigen` | Markiert eine Aufgabe als abgeschlossen. |
| `statistik_anzeigen` | Berechnet und zeigt den Fortschritt. |
| `motivation` | Gibt einen Motivationstext zurück. |
| `tages_tipp_anzeigen` | Zeigt einen zufälligen Lerntipp. |
| `speichern` | Speichert den Plan als JSON. |
| `laden` | Lädt den Plan aus JSON. |
| `exportieren` | Exportiert den Plan als TXT. |
| `menue_anzeigen` | Zeigt das Hauptmenü. |
| `main` | Steuert das gesamte Programm. |

## 27. Kurzes Fazit

`index.py` ist ein vollständiges Konsolenprogramm für Lernplanung. Es verwendet Klassen, Funktionen, Listen, Dictionaries, Schleifen, Bedingungen, Dateioperationen und Fehlerbehandlung. Die wichtigsten Konzepte sind:

- objektorientierte Programmierung mit `Thema` und `Lerneinheit`,
- Eingabevalidierung,
- automatische Planerstellung,
- gewichtete Auswahl schwerer Themen,
- Speichern und Laden mit JSON,
- Export als Textdatei,
- Fortschrittsberechnung.

