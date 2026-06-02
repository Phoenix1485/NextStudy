import json
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SAVE_FILE = BASE_DIR / "nextstudy_plan.json"
EXPORT_FILE = BASE_DIR / "nextstudy_export.txt"

SCHWIERIGKEITEN = {"leicht": 1, "mittel": 2, "schwer": 3}

AUFGABEN = {
    "leicht": "{} lernen, kurze Notizen machen und einmal wiederholen",
    "mittel": "{} lernen, Beispiele anschauen und Aufgaben lösen",
    "schwer": "{} intensiv lernen, Aufgaben üben und Fehler notieren",
}

TIPPS = [
    "Lerne lieber 45 Minuten konzentriert als 3 Stunden abgelenkt.",
    "Schreibe Fehler auf, damit du sie am Ende gezielt wiederholen kannst.",
    "Schwere Themen solltest du zuerst bearbeiten.",
    "Mache nach jeder Lerneinheit eine kurze Pause.",
    "Erkläre ein Thema laut, um zu prüfen, ob du es verstanden hast.",
]


class Thema:
    def __init__(self, name, schwierigkeit):
        self.name = name
        self.schwierigkeit = schwierigkeit
        self.gewichtung = SCHWIERIGKEITEN.get(schwierigkeit, 2)

    def to_dict(self):
        return {"name": self.name, "schwierigkeit": self.schwierigkeit, "gewichtung": self.gewichtung}


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
        return {"tag": self.tag, "thema": self.thema, "aufgabe": self.aufgabe,
                "dauer": self.dauer, "status": self.status}


# Eingaben
def eingabe_zahl(frage, minimum=1):
    while True:
        try:
            wert = int(input(frage))
            if wert >= minimum:
                return wert
            print(f"Bitte eine Zahl ab {minimum} eingeben.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine ganze Zahl eingeben.")


def eingabe_text(frage):
    while True:
        text = input(frage).strip()
        if text:
            return text
        print("Die Eingabe darf nicht leer sein.")


def eingabe_schwierigkeit(thema):
    while True:
        wert = input(f"Schwierigkeit für '{thema}' (leicht/mittel/schwer): ")
        wert = wert.lower().strip()
        if wert in SCHWIERIGKEITEN:
            return wert
        print("Bitte nur leicht, mittel oder schwer eingeben.")


# Lernplan
def projekt_erstellen():
    print("\n===== Neues Lernprojekt =====")
    fach = eingabe_text("Fach eingeben: ")
    anzahl = eingabe_zahl("Wie viele Themen möchtest du eintragen? ")

    themen = []
    for nummer in range(1, anzahl + 1):
        name = eingabe_text(f"Thema {nummer}: ")
        schwierigkeit = eingabe_schwierigkeit(name)
        themen.append(Thema(name, schwierigkeit))

    tage = eingabe_zahl("Wie viele Lerntage hast du? ")
    lernzeit = eingabe_zahl("Wie viele Minuten lernst du pro Tag? ")
    plan = lernplan_erstellen(themen, tage, lernzeit)

    print("\nLernprojekt wurde erstellt.")
    return fach, themen, tage, lernzeit, plan


def lernplan_erstellen(themen, tage, lernzeit):
    if tage == 1:
        return [Lerneinheit(1, "Wiederholung",
                            "Alle Themen kompakt wiederholen und einen Selbsttest machen", lernzeit)]

    sortierte_themen = sorted(themen, key=lambda thema: thema.gewichtung, reverse=True)
    lernliste = []
    for thema in sortierte_themen:
        lernliste.extend([thema] * thema.gewichtung)

    plan = []
    for tag in range(1, tage + 1):
        if tag == tage:
            einheit = Lerneinheit(tag, "Wiederholung",
                                  "Alle Themen wiederholen, offene Fragen klären und Mini-Selbsttest machen",
                                  lernzeit)
        elif tag == tage - 1 and tage >= 4:
            einheit = Lerneinheit(tag, "Prüfungsvorbereitung",
                                  "Schwächen wiederholen, Zusammenfassung lesen und Beispielaufgaben lösen",
                                  lernzeit)
        else:
            thema = lernliste[(tag - 1) % len(lernliste)]
            aufgabe = AUFGABEN[thema.schwierigkeit].format(thema.name)
            einheit = Lerneinheit(tag, thema.name, aufgabe, lernzeit)
        plan.append(einheit)

    return plan


# Ausgabe
def plan_anzeigen(fach, plan):
    if not plan:
        print("\nEs wurde noch kein Lernplan erstellt.")
        return

    print(f"\n===== Lernplan für {fach} =====")
    for nummer, einheit in enumerate(plan, 1):
        print(f"\n[{nummer}] Tag {einheit.tag}")
        print(f"Thema:   {einheit.thema}")
        print(f"Aufgabe: {einheit.aufgabe}")
        print(f"Dauer:   {einheit.dauer} Minuten")
        print(f"Status:  {einheit.status}")


def statistik_anzeigen(plan):
    if not plan:
        print("\nEs gibt noch keinen Lernplan.")
        return

    erledigt = sum(1 for einheit in plan if einheit.status == "abgeschlossen")
    offen = len(plan) - erledigt
    lernzeit_gesamt = sum(einheit.dauer for einheit in plan)
    lernzeit_erledigt = sum(einheit.dauer for einheit in plan if einheit.status == "abgeschlossen")
    prozent = round(erledigt / len(plan) * 100)

    if prozent == 100:
        hinweis = "Alles abgeschlossen. Gute Vorbereitung."
    elif prozent >= 75:
        hinweis = "Fast fertig. Jetzt nicht nachlassen."
    elif prozent >= 50:
        hinweis = "Die Hälfte ist geschafft."
    elif prozent >= 25:
        hinweis = "Guter Anfang. Bleib dran."
    else:
        hinweis = "Starte mit der ersten Aufgabe. Danach wird es einfacher."

    print(f"\n===== Statistik =====\nAufgaben gesamt:    {len(plan)}")
    print(f"Abgeschlossen:      {erledigt}\nOffen:              {offen}")
    print(f"Lernzeit gesamt:    {lernzeit_gesamt} Minuten")
    print(f"Erledigte Lernzeit: {lernzeit_erledigt} Minuten\nFortschritt:        {prozent} %")
    print(f"Hinweis:            {hinweis}")


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


# Dateien
def speichern(fach, themen, tage, lernzeit, plan):
    if not plan:
        print("\nEs gibt keinen Lernplan zum Speichern.")
        return

    speicher_daten = {
        "fach": fach,
        "tage": tage,
        "lernzeit": lernzeit,
        "themen": [thema.to_dict() for thema in themen],
        "plan": [einheit.to_dict() for einheit in plan],
    }

    try:
        SAVE_FILE.write_text(json.dumps(speicher_daten, indent=4, ensure_ascii=False), encoding="utf-8")
        print(f"Lernplan wurde in '{SAVE_FILE.name}' gespeichert.")
    except OSError as fehler:
        print(f"Speichern war nicht möglich: {fehler}")


def laden():
    if not SAVE_FILE.exists():
        print("\nEs wurde keine Speicherdatei gefunden.")
        return "", [], 0, 0, []

    try:
        gespeicherte_daten = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        themen = []
        for eintrag in gespeicherte_daten.get("themen", []):
            name = str(eintrag.get("name", "")).strip()
            schwierigkeit = str(eintrag.get("schwierigkeit", "mittel")).lower().strip()
            if name and schwierigkeit in SCHWIERIGKEITEN:
                themen.append(Thema(name, schwierigkeit))

        plan = []
        for eintrag in gespeicherte_daten.get("plan", []):
            einheit = Lerneinheit(
                int(eintrag.get("tag", len(plan) + 1)),
                str(eintrag.get("thema", "Unbekannt")),
                str(eintrag.get("aufgabe", "Keine Aufgabe gespeichert")),
                int(eintrag.get("dauer", 0)),
            )
            status = str(eintrag.get("status", "offen"))
            einheit.status = status if status in ("offen", "abgeschlossen") else "offen"
            plan.append(einheit)

        print("Lernplan wurde geladen.")
        return (
            str(gespeicherte_daten.get("fach", "")),
            themen,
            int(gespeicherte_daten.get("tage", 0)),
            int(gespeicherte_daten.get("lernzeit", 0)),
            plan,
        )
    except (json.JSONDecodeError, OSError, TypeError, ValueError, AttributeError) as fehler:
        print(f"Die Speicherdatei konnte nicht sicher geladen werden: {fehler}")
        print("Das Programm läuft ohne geladenen Plan weiter.")
        return "", [], 0, 0, []


def exportieren(fach, plan):
    if not plan:
        print("\nEs gibt keinen Lernplan zum Exportieren.")
        return

    zeilen = [f"NextStudy - Lernplan für {fach}", "=" * 40, ""]
    for einheit in plan:
        zeilen.append(f"Tag {einheit.tag}: {einheit.thema}")
        zeilen.append(f"Aufgabe: {einheit.aufgabe}")
        zeilen.append(f"Dauer: {einheit.dauer} Minuten")
        zeilen.append(f"Status: {einheit.status}")
        zeilen.append("")

    try:
        EXPORT_FILE.write_text("\n".join(zeilen), encoding="utf-8")
        print(f"Lernplan wurde als '{EXPORT_FILE.name}' exportiert.")
    except OSError as fehler:
        print(f"Export war nicht möglich: {fehler}")


# Hauptprogramm
def menue_anzeigen():
    punkte = [
        "Neues Lernprojekt erstellen",
        "Lernplan anzeigen",
        "Aufgabe als erledigt markieren",
        "Statistik anzeigen",
        "Tipp des Tages anzeigen",
        "Lernplan speichern",
        "Lernplan laden",
        "Lernplan als TXT exportieren",
        "Beenden",
    ]
    print("\n========================\n       NEXTSTUDY\n========================")
    for nummer, text in enumerate(punkte, 1):
        print(f"{nummer}. {text}")


def main():
    daten = {"fach": "", "themen": [], "tage": 0, "lernzeit": 0, "plan": []}

    def neues_projekt():
        fach, themen, tage, lernzeit, plan = projekt_erstellen()
        daten.update({"fach": fach, "themen": themen, "tage": tage,
                      "lernzeit": lernzeit, "plan": plan})

    def plan_laden():
        fach, themen, tage, lernzeit, plan = laden()
        daten.update({"fach": fach, "themen": themen, "tage": tage,
                      "lernzeit": lernzeit, "plan": plan})

    def tipp_anzeigen():
        print("\nTipp des Tages:")
        print(random.choice(TIPPS))

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

    while True:
        try:
            menue_anzeigen()
            auswahl = input("Auswahl: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nNextStudy wurde sicher beendet.")
            break

        if auswahl == "9":
            print("NextStudy wird beendet. Du bist jetzt wieder im Terminal.")
            break

        aktion = aktionen.get(auswahl)
        if aktion:
            try:
                aktion()
            except Exception as fehler:
                print(f"Unerwarteter Fehler: {fehler}")
                print("Das Sicherheits-Backup hat den Absturz verhindert. Das Menü wird neu angezeigt.")
        else:
            print("Ungültige Auswahl.")


if __name__ == "__main__":
    main()
