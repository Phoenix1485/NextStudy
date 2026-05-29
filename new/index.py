import json, random
from pathlib import Path

SAVE_FILE = "nextstudy_plan.json"
EXPORT_FILE = "nextstudy_export.txt"

SCHWIERIGKEITEN = {"leicht": 1, "mittel": 2, "schwer": 3}

AUFGABEN = {
    "leicht": "{} lernen, kurze Notizen machen und einmal wiederholen",
    "mittel": "{} lernen, Beispiele anschauen und Aufgaben lösen",
    "schwer": "{} intensiv lernen, Aufgaben üben und Fehler notieren"
}

TIPPS = [
    "Lerne lieber 45 Minuten konzentriert als 3 Stunden abgelenkt.",
    "Schreibe Fehler auf, damit du sie am Ende gezielt wiederholen kannst.",
    "Schwere Themen solltest du zuerst bearbeiten.",
    "Mache nach jeder Lerneinheit eine kurze Pause.",
    "Erkläre ein Thema laut, um zu prüfen, ob du es verstanden hast."
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
        self.tag, self.thema, self.aufgabe, self.dauer = tag, thema, aufgabe, dauer
        self.status = "offen"

    def erledigen(self):
        self.status = "abgeschlossen"

    def to_dict(self):
        return {"tag": self.tag, "thema": self.thema, "aufgabe": self.aufgabe,
                "dauer": self.dauer, "status": self.status}


# ── Eingabe-Helpers ────────────────────────────────────────────────────────────

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
        wert = input(f"Schwierigkeit für '{thema}' (leicht/mittel/schwer): ").lower().strip()
        if wert in SCHWIERIGKEITEN:
            return wert
        print("Bitte nur leicht, mittel oder schwer eingeben.")


# ── Kernlogik ──────────────────────────────────────────────────────────────────

def projekt_erstellen():
    print("\n===== Neues Lernprojekt =====")
    fach = eingabe_text("Fach eingeben: ")
    anzahl = eingabe_zahl("Wie viele Themen möchtest du eintragen? ")
    themen = []
    for i in range(1, anzahl + 1):
        name = eingabe_text(f"Thema {i}: ")
        themen.append(Thema(name, eingabe_schwierigkeit(name)))
    tage = eingabe_zahl("Wie viele Lerntage hast du? ")
    lernzeit = eingabe_zahl("Wie viele Minuten lernst du pro Tag? ")
    plan = lernplan_erstellen(themen, tage, lernzeit)
    print("\nLernprojekt wurde erstellt.")
    return fach, themen, tage, lernzeit, plan

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


# ── Anzeige ────────────────────────────────────────────────────────────────────

def plan_anzeigen(fach, plan):
    if not plan:
        print("\nEs wurde noch kein Lernplan erstellt.")
        return
    print(f"\n===== Lernplan für {fach} =====")
    for i, e in enumerate(plan, 1):
        print(f"\n[{i}] Tag {e.tag}\nThema:   {e.thema}\nAufgabe: {e.aufgabe}\nDauer:   {e.dauer} Minuten\nStatus:  {e.status}")


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


# ── Persistenz ─────────────────────────────────────────────────────────────────

def speichern(fach, themen, tage, lernzeit, plan):
    if not plan:
        print("\nEs gibt keinen Lernplan zum Speichern.")
        return
    daten = {"fach": fach, "tage": tage, "lernzeit": lernzeit,
             "themen": [t.to_dict() for t in themen], "plan": [e.to_dict() for e in plan]}
    Path(SAVE_FILE).write_text(json.dumps(daten, indent=4, ensure_ascii=False), encoding="utf-8")
    print(f"Lernplan wurde in '{SAVE_FILE}' gespeichert.")


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


# ── Hauptprogramm ──────────────────────────────────────────────────────────────

def menue_anzeigen():
    print("\n========================\n     NEXTSTUDY\n========================")
    for nr, text in enumerate(["Neues Lernprojekt erstellen", "Lernplan anzeigen",
                                "Aufgabe als erledigt markieren", "Statistik anzeigen",
                                "Tipp des Tages anzeigen", "Lernplan speichern",
                                "Lernplan laden", "Lernplan als TXT exportieren", "Beenden"], 1):
        print(f"{nr}. {text}")


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


if __name__ == "__main__":
    main()