# Portfolio: NextStudy

## Projektidee

Bei NextStudy geht es um ein Problem, das ich selber gut kenne: Man hat mehrere Themen für eine Arbeit oder Prüfung, aber am Anfang weiß man oft nicht, womit man anfangen soll. Dann schiebt man die Planung vor sich her und verliert Zeit, obwohl man eigentlich schon lernen könnte.

Deshalb habe ich ein kleines Python-Programm geschrieben, das aus ein paar Eingaben einen Lernplan macht. Man gibt das Fach ein, danach die Themen, die Schwierigkeit, die Anzahl der Lerntage und die Lernzeit pro Tag. Daraus erstellt das Programm für jeden Tag eine Aufgabe.

Mir war wichtig, dass schwere Themen nicht genauso behandelt werden wie leichte Themen. Deshalb bekommen sie im Programm eine höhere Gewichtung. Schwere Themen kommen dadurch früher oder öfter im Plan vor. Am Ende wird außerdem Wiederholung eingeplant, weil man kurz vor einer Prüfung nicht nur neue Themen lernen sollte.

## Planung

Ich habe mich bewusst für ein Konsolenprogramm entschieden. Eine Oberfläche mit Fenstern und Buttons wäre zwar schöner, aber für dieses Projekt wäre das zu viel gewesen. Ich wollte lieber zeigen, dass die eigentliche Logik funktioniert und dass der Code verständlich bleibt.

Geplant waren diese Funktionen:

- ein neues Lernprojekt erstellen,
- Themen und Schwierigkeiten eingeben,
- automatisch einen Lernplan erzeugen,
- den Plan anzeigen,
- Aufgaben als erledigt markieren,
- eine Statistik zum Fortschritt anzeigen,
- einen Lerntipp ausgeben,
- den Plan speichern und später wieder laden,
- den Plan als Textdatei exportieren.

Für die Struktur habe ich zwei Klassen benutzt. `Thema` speichert den Namen, die Schwierigkeit und die Gewichtung. `Lerneinheit` steht für eine konkrete Aufgabe an einem bestimmten Tag. So musste ich nicht alles in einzelnen Listen speichern, sondern konnte zusammengehörige Daten in Objekten bündeln.

## Umsetzung

Beim Start zeigt das Programm ein Menü im Terminal. Die Auswahl funktioniert über Zahlen. Wenn man ein neues Projekt erstellt, fragt das Programm Schritt für Schritt alle wichtigen Daten ab.

Damit man das Programm nicht immer über einen Terminalbefehl starten muss, habe ich zusätzlich zwei Startdateien angelegt. Unter Windows kann man `start_nextstudy_windows.bat` doppelklicken, unter macOS `start_nextstudy_macos.command`. Beide Dateien öffnen das Terminal und starten `index.py` aus dem richtigen Ordner.

Für die Menülogik habe ich nicht mehr nur eine lange `if/elif`-Kette benutzt. Stattdessen gibt es ein Dictionary `aktionen`. Darin wird zum Beispiel die Eingabe `"1"` direkt der passenden Funktion zugeordnet. So eine Struktur nennt man Dispatch-Tabelle. Das wirkt im ersten Moment etwas ungewohnt, macht das Menü aber aufgeräumter.

Den aktuellen Programmzustand speichere ich in einem Dictionary namens `daten`. Dort liegen Fach, Themen, Tage, Lernzeit und Plan. Dadurch sind diese Werte an einer Stelle gesammelt und die Menüfunktionen können damit weiterarbeiten.

Die wichtigste Stelle für den Lernplan ist die Funktion `lernplan_erstellen()`. Dort werden die Themen zuerst nach Schwierigkeit sortiert. Danach wird eine Liste gebaut, in der schwere Themen mehrfach vorkommen. Ein schweres Thema hat die Gewichtung `3`, ein mittleres Thema `2` und ein leichtes Thema `1`. Dadurch beeinflusst die Schwierigkeit direkt den Plan.

Zum Speichern benutze ich JSON. Das passt gut, weil man Listen und Dictionaries damit gut abspeichern kann. Eigene Python-Objekte können aber nicht direkt als JSON gespeichert werden. Deshalb haben die Klassen die Methode `to_dict()`. Damit werden die Objekte vor dem Speichern in normale Dictionaries umgewandelt.

## Herausforderungen und Lösungen

Eine Herausforderung war die Eingabeprüfung. Wenn jemand bei der Anzahl der Tage aus Versehen Text eingibt, darf das Programm nicht abstürzen. Dafür gibt es die Funktion `eingabe_zahl()`. Sie fragt so lange nach, bis wirklich eine gültige Zahl eingegeben wurde.

Auch die Verteilung der Themen war nicht ganz so einfach. Erst wollte ich die Themen nur der Reihe nach auf die Tage verteilen. Das wäre aber nicht besonders sinnvoll gewesen, weil ein schweres Thema dann genauso viel Platz bekommen hätte wie ein leichtes. Mit der Gewichtung ist die Lösung besser erklärbar und passt mehr zum echten Lernen.

Beim Speichern musste ich erst verstehen, dass JSON keine selbst erstellten Objekte speichern kann. Die Lösung war, die Objekte in Dictionaries umzuwandeln und beim Laden wieder neue Objekte daraus zu erstellen.

Bei der Menülogik war außerdem der Scope wichtig. Wenn eine Variable falsch eingerückt ist oder nur in einer Funktion existiert, kann Python sie an einer anderen Stelle nicht benutzen. Dann entsteht schnell ein `NameError`. Deshalb liegt `daten` jetzt direkt in `main()`, also in dem Bereich, in dem auch die Menüaktionen erstellt werden.

Ich habe außerdem ein Sicherheits-Backup eingebaut. Wenn beim Speichern, Laden, Exportieren oder bei einer Menüaktion ein unerwarteter Fehler passiert, soll das Programm nicht einfach abstürzen. Stattdessen wird eine Meldung angezeigt und das Menü läuft weiter. Besonders beim Laden ist das wichtig, weil eine JSON-Datei auch beschädigt oder unvollständig sein kann.

Bei der Beenden-Funktion habe ich die Meldung klarer gemacht. Wenn man `9` auswählt, sagt das Programm, dass man jetzt wieder im Terminal ist. Das ist wichtig, weil spätere Eingaben dann nicht mehr zum Programm gehören.

Eine weitere kleine Verbesserung war der feste Speicherort. Die Dateien `nextstudy_plan.json` und `nextstudy_export.txt` werden im gleichen Ordner wie `index.py` gespeichert. Dadurch landet nichts aus Versehen in einem anderen Ordner.

## Wie hilft das Tool?

NextStudy hilft vor allem dabei, den Lernstoff nicht nur als lange Liste zu sehen. Aus den Themen werden konkrete Tagesaufgaben. Man sieht also direkt, was man wann machen soll.

Das Tool hilft, weil es:

- schwierige Themen stärker berücksichtigt,
- jeden Lerntag mit einer Aufgabe füllt,
- am Ende Wiederholung einplant,
- erledigte Aufgaben speichert,
- den Fortschritt in Prozent anzeigt,
- den Plan auch nach dem Schließen wieder laden kann,
- sich per Doppelklick über eine Startdatei öffnen lässt.

## Screenshot des fertigen Programms

Der Screenshot liegt hier:

```text
screenshots/nextstudy_terminal.png
```

Auf dem Screenshot sieht man das Menü, einen Beispielplan und die Statistik. Da NextStudy ein Terminalprogramm ist, zeigt ein Terminal-Screenshot das fertige Ergebnis am besten.

## Reflexion

Bei dem Projekt habe ich gemerkt, wie wichtig eine klare Struktur im Code ist. Wenn man alles direkt in eine große Funktion schreibt, wird es schnell unübersichtlich. Mit mehreren kleineren Funktionen konnte ich die einzelnen Aufgaben besser trennen.

Ich habe außerdem besser verstanden, wofür Klassen praktisch sind. Ein Thema besteht nicht nur aus einem Namen, sondern auch aus Schwierigkeit und Gewichtung. Eine Lerneinheit hat Tag, Aufgabe, Dauer und Status. Mit Klassen kann man solche Daten sauber zusammenhalten.

Auch die Dispatch-Tabelle war ein wichtiger Punkt für mich. Vorher hätte ich das Menü einfach mit vielen `if`- und `elif`-Abfragen gelöst. Jetzt habe ich gesehen, dass man Funktionen auch in einem Dictionary speichern und später aufrufen kann.

Neu war für mich vor allem das Speichern mit JSON. Dadurch bleibt der Lernplan auch nach dem Beenden des Programms erhalten. Das macht das Programm deutlich nützlicher, weil man nicht jedes Mal alles neu eingeben muss.

Wenn ich das Projekt später erweitern würde, würde ich mehrere Lernprojekte gleichzeitig speichern. Außerdem wäre eine kleine grafische Oberfläche möglich. Für diese Version passt die Konsole aber gut, weil der Schwerpunkt auf der Python-Logik liegt.
