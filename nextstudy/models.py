"""Datenmodell fuer NextStudy.

Die Klassen in diesem Modul beschreiben nur den Zustand der Anwendung. Sie
enthalten bewusst keine Eingabelogik und keine Planungsregeln. Dadurch bleiben
die Objekte leicht testbar und koennen sauber als JSON gespeichert werden.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any


class Difficulty(str, Enum):
    """Schwierigkeit eines Themas mit fachlicher Gewichtung."""

    EASY = "leicht"
    MEDIUM = "mittel"
    HARD = "schwer"

    @property
    def weight(self) -> int:
        return {
            Difficulty.EASY: 1,
            Difficulty.MEDIUM: 2,
            Difficulty.HARD: 3,
        }[self]

    @classmethod
    def parse(cls, value: str | Difficulty) -> Difficulty:
        if isinstance(value, Difficulty):
            return value

        normalized = value.strip().lower()
        aliases = {
            "einfach": cls.EASY,
            "leicht": cls.EASY,
            "normal": cls.MEDIUM,
            "mittel": cls.MEDIUM,
            "schwierig": cls.HARD,
            "schwer": cls.HARD,
        }

        try:
            return aliases[normalized]
        except KeyError as exc:
            allowed = ", ".join(item.value for item in cls)
            raise ValueError(f"Ungueltige Schwierigkeit '{value}'. Erlaubt: {allowed}.") from exc


class Status(str, Enum):
    """Bearbeitungsstatus einer geplanten Lerneinheit."""

    OPEN = "offen"
    IN_PROGRESS = "in Bearbeitung"
    DONE = "abgeschlossen"

    @classmethod
    def parse(cls, value: str | Status) -> Status:
        if isinstance(value, Status):
            return value

        normalized = value.strip().lower()
        aliases = {
            "offen": cls.OPEN,
            "neu": cls.OPEN,
            "in arbeit": cls.IN_PROGRESS,
            "in bearbeitung": cls.IN_PROGRESS,
            "bearbeitung": cls.IN_PROGRESS,
            "abgeschlossen": cls.DONE,
            "fertig": cls.DONE,
            "erledigt": cls.DONE,
        }

        try:
            return aliases[normalized]
        except KeyError as exc:
            allowed = ", ".join(item.value for item in cls)
            raise ValueError(f"Ungueltiger Status '{value}'. Erlaubt: {allowed}.") from exc


@dataclass(slots=True)
class Topic:
    """Ein einzelnes Lernthema innerhalb eines Fachs."""

    name: str
    difficulty: Difficulty = Difficulty.MEDIUM

    def __post_init__(self) -> None:
        self.name = _clean_text(self.name, "Themenname")
        self.difficulty = Difficulty.parse(self.difficulty)

    @property
    def weight(self) -> int:
        return self.difficulty.weight

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "difficulty": self.difficulty.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Topic:
        return cls(
            name=str(data["name"]),
            difficulty=Difficulty.parse(str(data["difficulty"])),
        )


@dataclass(slots=True)
class Subject:
    """Ein Fach mit einer geordneten Sammlung von Themen."""

    name: str
    topics: list[Topic] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.name = _clean_text(self.name, "Fachname")
        self.topics = [topic if isinstance(topic, Topic) else Topic.from_dict(topic) for topic in self.topics]

    def add_topic(self, name: str, difficulty: str | Difficulty) -> None:
        self.topics.append(Topic(name=name, difficulty=Difficulty.parse(difficulty)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "topics": [topic.to_dict() for topic in self.topics],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Subject:
        return cls(
            name=str(data["name"]),
            topics=[Topic.from_dict(item) for item in data.get("topics", [])],
        )


@dataclass(slots=True)
class StudyUnit:
    """Eine konkrete Aufgabe an einem bestimmten Lerntag."""

    day: int
    topic: str
    task: str
    duration_minutes: int
    status: Status = Status.OPEN

    def __post_init__(self) -> None:
        if self.day < 1:
            raise ValueError("Der Tag muss mindestens 1 sein.")
        if self.duration_minutes < 1:
            raise ValueError("Eine Lerneinheit braucht mindestens eine Minute.")

        self.topic = _clean_text(self.topic, "Thema")
        self.task = _clean_text(self.task, "Aufgabe")
        self.status = Status.parse(self.status)

    def to_dict(self) -> dict[str, Any]:
        return {
            "day": self.day,
            "topic": self.topic,
            "task": self.task,
            "duration_minutes": self.duration_minutes,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StudyUnit:
        return cls(
            day=int(data["day"]),
            topic=str(data["topic"]),
            task=str(data["task"]),
            duration_minutes=int(data["duration_minutes"]),
            status=Status.parse(str(data.get("status", Status.OPEN.value))),
        )


@dataclass(slots=True)
class StudyPlan:
    """Der fertige Lernplan inklusive Fortschritt."""

    subject: Subject
    days: int
    minutes_per_day: int
    units: list[StudyUnit]
    exam_date: date | None = None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if self.days < 1:
            raise ValueError("Ein Lernplan braucht mindestens einen Tag.")
        if self.minutes_per_day < 1:
            raise ValueError("Die taegliche Lernzeit muss positiv sein.")

        if not isinstance(self.subject, Subject):
            self.subject = Subject.from_dict(self.subject)
        self.units = [unit if isinstance(unit, StudyUnit) else StudyUnit.from_dict(unit) for unit in self.units]

    def units_for_day(self, day: int) -> list[StudyUnit]:
        return [unit for unit in self.units if unit.day == day]

    def update_status(self, unit_number: int, status: str | Status) -> None:
        if unit_number < 1 or unit_number > len(self.units):
            raise IndexError("Diese Lerneinheit gibt es nicht.")
        self.units[unit_number - 1].status = Status.parse(status)

    def statistics(self) -> dict[str, int | float]:
        total = len(self.units)
        done = sum(1 for unit in self.units if unit.status == Status.DONE)
        in_progress = sum(1 for unit in self.units if unit.status == Status.IN_PROGRESS)
        open_units = total - done - in_progress
        progress = round((done / total) * 100, 1) if total else 0.0

        return {
            "total": total,
            "done": done,
            "in_progress": in_progress,
            "open": open_units,
            "progress": progress,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject": self.subject.to_dict(),
            "days": self.days,
            "minutes_per_day": self.minutes_per_day,
            "exam_date": self.exam_date.isoformat() if self.exam_date else None,
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "units": [unit.to_dict() for unit in self.units],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StudyPlan:
        exam_date = data.get("exam_date")
        created_at = data.get("created_at")

        return cls(
            subject=Subject.from_dict(data["subject"]),
            days=int(data["days"]),
            minutes_per_day=int(data["minutes_per_day"]),
            exam_date=date.fromisoformat(exam_date) if exam_date else None,
            created_at=datetime.fromisoformat(created_at) if created_at else datetime.now(),
            units=[StudyUnit.from_dict(item) for item in data.get("units", [])],
        )


def _clean_text(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} darf nicht leer sein.")
    return " ".join(cleaned.split())

