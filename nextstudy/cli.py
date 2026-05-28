"""Interaktive Konsolenoberflaeche fuer NextStudy."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from nextstudy.models import Difficulty, Status, StudyPlan, Subject
from nextstudy.planner import StudyPlanner
from nextstudy.storage import DEFAULT_PLAN_PATH, JsonPlanStorage


class NextStudyApp:
    """Steuert den Dialog mit dem Nutzer und delegiert Fachlogik an Services."""

    def __init__(self) -> None:
        self.subject: Subject | None = None
        self.plan: StudyPlan | None = None
        self.planner = StudyPlanner()
        self.storage = JsonPlanStorage()

    def run(self) -> None:
        self._print_header()

        while True:
            self._print_menu()
            choice = input("Auswahl: ").strip()

            try:
                if choice == "1":
                    self._create_subject()
                elif choice == "2":
                    self._add_topics()
                elif choice == "3":
                    self._create_plan()
                elif choice == "4":
                    self._show_plan()
                elif choice == "5":
                    self._update_progress()
                elif choice == "6":
                    self._show_statistics()
                elif choice == "7":
                    self._save_plan()
                elif choice == "8":
                    self._load_plan()
                elif choice == "9":
                    print("NextStudy wird beendet.")
                    return
                else:
                    print("Bitte waehle eine Zahl von 1 bis 9.")
            except (ValueError, IndexError, FileNotFoundError) as error:
                print(f"Hinweis: {error}")

    def _print_header(self) -> None:
        print("=" * 32)
        print("          NEXTSTUDY")
        print("=" * 32)

    def _print_menu(self) -> None:
        print()
        print("1. Neues Fach anlegen")
        print("2. Themen hinzufuegen")
        print("3. Lernplan erstellen")
        print("4. Lernplan anzeigen")
        print("5. Fortschritt aktualisieren")
        print("6. Statistik anzeigen")
        print("7. Lernplan speichern")
        print("8. Lernplan laden")
        print("9. Programm beenden")

    def _create_subject(self) -> None:
        name = self._read_required("Fachname: ")
        self.subject = Subject(name=name)
        self.plan = None
        print(f"Fach '{self.subject.name}' wurde angelegt.")

        if self._confirm("Direkt Themen hinzufuegen?"):
            self._add_topics()

    def _add_topics(self) -> None:
        subject = self._require_subject()

        print("Gib pro Zeile ein Thema ein. Eine leere Eingabe beendet die Erfassung.")
        while True:
            name = input("Thema: ").strip()
            if not name:
                break

            difficulty = self._read_difficulty()
            subject.add_topic(name=name, difficulty=difficulty)
            print(f"'{name}' wurde hinzugefuegt.")

        self.plan = None
        print(f"Aktuelle Themenanzahl: {len(subject.topics)}")

    def _create_plan(self) -> None:
        subject = self._require_subject()
        days = self._read_int("Wie viele Lerntage stehen zur Verfuegung? ", minimum=1)
        minutes = self._read_int("Wie viele Minuten pro Tag moechtest du lernen? ", minimum=15)
        exam_date = self._read_optional_date("Pruefungstermin optional (JJJJ-MM-TT): ")

        self.plan = self.planner.create_plan(
            subject=subject,
            days=days,
            minutes_per_day=minutes,
            exam_date=exam_date,
        )
        print("Der Lernplan wurde erstellt.")
        self._show_plan()

    def _show_plan(self) -> None:
        plan = self._require_plan()

        print()
        print(f"Lernplan fuer {plan.subject.name}")
        if plan.exam_date:
            print(f"Pruefungstermin: {plan.exam_date.isoformat()}")
        print("-" * 32)

        unit_number = 1
        for day in range(1, plan.days + 1):
            print(f"Tag {day}:")
            for unit in plan.units_for_day(day):
                print(
                    f"  {unit_number}. {unit.topic} - {unit.task} "
                    f"({unit.duration_minutes} Min., {unit.status.value})"
                )
                unit_number += 1
            print()

    def _update_progress(self) -> None:
        plan = self._require_plan()
        self._show_plan()

        unit_number = self._read_int("Welche Lerneinheit soll aktualisiert werden? ", minimum=1)
        status = self._read_status()
        plan.update_status(unit_number, status)
        print("Der Fortschritt wurde aktualisiert.")

    def _show_statistics(self) -> None:
        plan = self._require_plan()
        stats = plan.statistics()

        print()
        print("Statistik")
        print("-" * 32)
        print(f"Lerneinheiten gesamt: {stats['total']}")
        print(f"Abgeschlossen: {stats['done']}")
        print(f"In Bearbeitung: {stats['in_progress']}")
        print(f"Offen: {stats['open']}")
        print(f"Fortschritt: {stats['progress']} %")

    def _save_plan(self) -> None:
        plan = self._require_plan()
        path = self._read_path("Speicherort", DEFAULT_PLAN_PATH)
        saved_path = self.storage.save(plan, path)
        print(f"Lernplan gespeichert unter: {saved_path}")

    def _load_plan(self) -> None:
        path = self._read_path("Datei laden", DEFAULT_PLAN_PATH)
        self.plan = self.storage.load(path)
        self.subject = self.plan.subject
        print(f"Lernplan fuer '{self.subject.name}' wurde geladen.")

    def _require_subject(self) -> Subject:
        if self.subject is None:
            raise ValueError("Lege zuerst ein Fach an.")
        return self.subject

    def _require_plan(self) -> StudyPlan:
        if self.plan is None:
            raise ValueError("Erstelle oder lade zuerst einen Lernplan.")
        return self.plan

    def _read_required(self, prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Die Eingabe darf nicht leer sein.")

    def _read_int(self, prompt: str, minimum: int) -> int:
        while True:
            raw_value = input(prompt).strip()
            try:
                value = int(raw_value)
            except ValueError:
                print("Bitte gib eine ganze Zahl ein.")
                continue

            if value >= minimum:
                return value
            print(f"Der Wert muss mindestens {minimum} sein.")

    def _read_difficulty(self) -> Difficulty:
        while True:
            raw_value = input("Schwierigkeit (leicht/mittel/schwer): ").strip()
            try:
                return Difficulty.parse(raw_value)
            except ValueError as error:
                print(error)

    def _read_status(self) -> Status:
        while True:
            raw_value = input("Status (offen/in Bearbeitung/abgeschlossen): ").strip()
            try:
                return Status.parse(raw_value)
            except ValueError as error:
                print(error)

    def _read_optional_date(self, prompt: str) -> date | None:
        raw_value = input(prompt).strip()
        if not raw_value:
            return None

        try:
            return date.fromisoformat(raw_value)
        except ValueError as exc:
            raise ValueError("Das Datum muss im Format JJJJ-MM-TT eingegeben werden.") from exc

    def _read_path(self, label: str, default: Path) -> Path:
        raw_value = input(f"{label} [{default}]: ").strip()
        return Path(raw_value) if raw_value else default

    def _confirm(self, question: str) -> bool:
        answer = input(f"{question} (ja/nein): ").strip().lower()
        return answer in {"ja", "j", "yes", "y"}


def main() -> None:
    NextStudyApp().run()


if __name__ == "__main__":
    main()
