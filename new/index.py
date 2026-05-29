import json
import random
from pathlib import Path


SAVE_FILE = "nextstudy_plan.json"
EXPORT_FILE = "nextstudy_export.txt"


class Thema:
    def __init__(self, name, schwierigkeit):
        self.name = name
        self.schwierigkeit = schwierigkeit
        self.gewichtung = self.berechne_gewichtung()

    def berechne_gewichtung(self):
        if self.schwierigkeit == "leicht":
            return 1
        if self.schwierigkeit == "mittel":
            return 2
        if self.schwierigkeit == "schwer":
            return 3
        return 2

    def to_dict(self):
        return {
            "name": self.name,
            "schwierigkeit": self.schwierigkeit,
            "gewichtung": self.gewichtung
        }


class Lerneinheit:
    def __init__(self, tag, thema, aufgabe, dauer):
        self.tag = tag
        self.thema = thema
        self.aufgabe = aufgabe
        self.dauer = dauer
        self.status = "offen"

    def erledigen(self):
        self.status = "abgeschlossen"

    def to_dict(self):
        return {
            "tag": self.tag,
            "thema": self.thema,
            "aufgabe": self.aufgabe,
            "dauer": self.dauer,
            "status": self.status
        }


def zahl_eingeben(frage, minimum=1):
    while True:
        try:
            wert = int(input(frage))
            if wert >= minimum:
                return wert
            print(f"Bitte eine Zahl ab {minimum} eingeben.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine ganze Zahl eingeben.")


def text_eingeben(frage):
    while True:
        text = input(frage).strip()
        if text:
            return text
        print("Die Eingabe darf nicht leer sein.")


def schwierigkeit_eingeben(thema):
    while True:
        wert = input(f"Schwierigkeit für '{thema}' (leicht/mittel/schwer): ").lower().strip()
        if wert in ["leicht", "mittel", "schwer"]:
            return wert
        print("Bitte nur leicht, mittel oder schwer eingeben.")


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


def gewichtete_themenliste(themen):
    lernliste = []

    for thema in themen:
        for _ in range(thema.gewichtung):
            lernliste.append(thema)

    return lernliste


def aufgabe_fuer_thema(thema):
    if thema.schwierigkeit == "leicht":
        return f"{thema.name} lernen, kurze Notizen machen und einmal wiederholen"
    if thema.schwierigkeit == "mittel":
        return f"{thema.name} lernen, Beispiele anschauen und Aufgaben lösen"
    return f"{thema.name} intensiv lernen, Aufgaben üben und Fehler notieren"


def wiederholungstag_erstellen(tag, lernzeit):
    aufgabe = "Alle Themen wiederholen, offene Fragen klären und Mini-Selbsttest machen"
    return Lerneinheit(tag, "Wiederholung", aufgabe, lernzeit)


def pruefungsvorbereitung_erstellen(tag, lernzeit):
    aufgabe = "Schwächen wiederholen, Zusammenfassung lesen und Beispielaufgaben lösen"
    return Lerneinheit(tag, "Prüfungsvorbereitung", aufgabe, lernzeit)


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


if __name__ == "__main__":
    main()
