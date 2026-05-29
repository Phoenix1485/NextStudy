"""Planungslogik fuer NextStudy.

Der Planner arbeitet deterministisch: gleiche Eingaben erzeugen immer denselben
Plan. Das ist fuer ein Schulprojekt gut erklaerbar und fuer Tests deutlich
zuverlaessiger als zufaellige Verteilung.
"""

from __future__ import annotations

from collections import Counter
from datetime import date

from nextstudy.models import Difficulty, StudyPlan, StudyUnit, Subject, Topic


class StudyPlanner:
    """Erstellt aus Fach, Themen und verfuegbarer Zeit einen Lernplan."""

    def create_plan(
        self,
        subject: Subject,
        days: int,
        minutes_per_day: int,
        exam_date: date | None = None,
    ) -> StudyPlan:
        self._validate_input(subject, days, minutes_per_day)

        learning_days = self._learning_days(days)
        blocks_per_day = self._blocks_per_day(minutes_per_day)
        capacity = learning_days * blocks_per_day
        slots = self._build_topic_slots(subject.topics, max(1, capacity))
        daily_focus_minutes = minutes_per_day
        recap_minutes = 0

        if days == 1:
            recap_minutes = self._short_recap_minutes(minutes_per_day)
            daily_focus_minutes = minutes_per_day - recap_minutes

        units = self._build_learning_units(slots, learning_days, daily_focus_minutes)

        if days > learning_days:
            units.extend(self._build_final_review(days, subject.topics, minutes_per_day))
        elif days == 1:
            units.extend(self._build_short_recap(subject.topics, recap_minutes))

        return StudyPlan(
            subject=subject,
            days=days,
            minutes_per_day=minutes_per_day,
            exam_date=exam_date,
            units=units,
        )

    def _validate_input(self, subject: Subject, days: int, minutes_per_day: int) -> None:
        if not subject.topics:
            raise ValueError("Lege zuerst mindestens ein Thema an.")
        if days < 1:
            raise ValueError("Die Anzahl der Lerntage muss mindestens 1 sein.")
        if minutes_per_day < 15:
            raise ValueError("Plane mindestens 15 Minuten pro Tag ein.")

    def _learning_days(self, days: int) -> int:
        # Ab zwei Tagen bleibt der letzte Tag frei fuer Wiederholung und Testmodus.
        return max(1, days - 1) if days >= 2 else 1

    def _blocks_per_day(self, minutes_per_day: int) -> int:
        if minutes_per_day < 45:
            return 1
        if minutes_per_day < 90:
            return 2
        return 3

    def _build_topic_slots(self, topics: list[Topic], capacity: int) -> list[list[Topic]]:
        if len(topics) > capacity:
            return self._pack_topics_into_limited_capacity(topics, capacity)

        # Jedes Thema erscheint mindestens einmal. Zusaetzliche Slots gehen an
        # schwierigere Themen, ohne dass ein einzelnes Thema den Plan dominiert.
        target = min(sum(topic.weight for topic in topics), capacity)
        slots = [[topic] for topic in sorted(topics, key=self._topic_priority)]
        extra_count = max(0, target - len(slots))
        slots.extend([topic] for topic in self._smooth_weighted_topics(topics, extra_count))
        return self._interleave_slots(slots)

    def _pack_topics_into_limited_capacity(self, topics: list[Topic], capacity: int) -> list[list[Topic]]:
        slots: list[list[Topic]] = [[] for _ in range(capacity)]
        slot_weights = [0] * capacity

        for topic in sorted(topics, key=self._topic_priority):
            target_index = min(range(capacity), key=lambda index: (slot_weights[index], index))
            slots[target_index].append(topic)
            slot_weights[target_index] += topic.weight

        return [slot for slot in slots if slot]

    def _smooth_weighted_topics(self, topics: list[Topic], count: int) -> list[Topic]:
        if count <= 0:
            return []

        ordered_topics = sorted(topics, key=self._topic_priority)
        current_scores = {topic.name: 0 for topic in ordered_topics}
        total_weight = sum(topic.weight for topic in ordered_topics)
        result: list[Topic] = []

        for _ in range(count):
            for topic in ordered_topics:
                current_scores[topic.name] += topic.weight

            selected = max(ordered_topics, key=lambda topic: (current_scores[topic.name], topic.weight))
            current_scores[selected.name] -= total_weight
            result.append(selected)

        return result

    def _interleave_slots(self, slots: list[list[Topic]]) -> list[list[Topic]]:
        heavy = [slot for slot in slots if slot[0].difficulty == Difficulty.HARD]
        medium = [slot for slot in slots if slot[0].difficulty == Difficulty.MEDIUM]
        easy = [slot for slot in slots if slot[0].difficulty == Difficulty.EASY]

        result: list[list[Topic]] = []
        groups = [heavy, medium, easy]
        while any(groups):
            for group in groups:
                if group:
                    result.append(group.pop(0))
        return result

    def _build_learning_units(
        self,
        slots: list[list[Topic]],
        learning_days: int,
        minutes_per_day: int,
    ) -> list[StudyUnit]:
        units: list[StudyUnit] = []
        slot_groups = self._split_evenly(slots, learning_days)
        topic_counter: Counter[str] = Counter()

        for day, day_slots in enumerate(slot_groups, start=1):
            durations = self._split_minutes(minutes_per_day, len(day_slots))
            for slot, duration in zip(day_slots, durations, strict=True):
                topic_name = self._format_topic_slot(slot)
                task = self._task_for_slot(slot, topic_counter)
                units.append(
                    StudyUnit(
                        day=day,
                        topic=topic_name,
                        task=task,
                        duration_minutes=duration,
                    )
                )

                for topic in slot:
                    topic_counter[topic.name] += 1

        return units

    def _build_final_review(
        self,
        day: int,
        topics: list[Topic],
        minutes_per_day: int,
    ) -> list[StudyUnit]:
        hardest_topics = sorted(topics, key=self._topic_priority)[:3]
        focus = ", ".join(topic.name for topic in hardest_topics)

        if minutes_per_day < 45:
            return [
                StudyUnit(
                    day=day,
                    topic="Gesamtwiederholung",
                    task=f"Wichtige Inhalte wiederholen, besonders: {focus}",
                    duration_minutes=minutes_per_day,
                )
            ]

        review_minutes = round(minutes_per_day * 0.6)
        test_minutes = minutes_per_day - review_minutes
        return [
            StudyUnit(
                day=day,
                topic="Gesamtwiederholung",
                task=f"Zusammenfassungen pruefen und offene Fragen klaeren: {focus}",
                duration_minutes=review_minutes,
            ),
            StudyUnit(
                day=day,
                topic="Mini-Test",
                task="Pruefungsnahe Aufgaben ohne Unterlagen bearbeiten und Fehler auswerten",
                duration_minutes=test_minutes,
            ),
        ]

    def _build_short_recap(self, topics: list[Topic], minutes_per_day: int) -> list[StudyUnit]:
        focus = ", ".join(topic.name for topic in sorted(topics, key=self._topic_priority)[:3])
        return [
            StudyUnit(
                day=1,
                topic="Kurz-Wiederholung",
                task=f"Am Ende die wichtigsten Punkte aktiv abrufen: {focus}",
                duration_minutes=minutes_per_day,
            )
        ]

    def _short_recap_minutes(self, minutes_per_day: int) -> int:
        return max(5, round(minutes_per_day * 0.2))

    def _task_for_slot(self, slot: list[Topic], topic_counter: Counter[str]) -> str:
        if len(slot) > 1:
            return "Kernbegriffe ordnen, Gemeinsamkeiten vergleichen und offene Fragen notieren"

        topic = slot[0]
        previous_count = topic_counter[topic.name]
        if previous_count == 0:
            return self._first_task(topic)
        if previous_count == 1:
            return "Aufgaben ueben und typische Fehler in einer kurzen Fehlerliste sammeln"
        return "Gezielt wiederholen, Pruefungsfragen trainieren und Unsicherheiten schliessen"

    def _first_task(self, topic: Topic) -> str:
        if topic.difficulty == Difficulty.HARD:
            return "Grundlagen sauber aufarbeiten, Beispiele rechnen und schwierige Stellen markieren"
        if topic.difficulty == Difficulty.MEDIUM:
            return "Grundlagen verstehen, eigene Zusammenfassung schreiben und Beispiele pruefen"
        return "Kernaussagen lernen, kurze Notizen erstellen und ein Beispiel selbst erklaeren"

    def _format_topic_slot(self, slot: list[Topic]) -> str:
        return ", ".join(topic.name for topic in slot)

    def _split_evenly(self, slots: list[list[Topic]], days: int) -> list[list[list[Topic]]]:
        grouped: list[list[list[Topic]]] = []
        start = 0

        for day_index in range(days):
            remaining_slots = len(slots) - start
            remaining_days = days - day_index
            amount = max(1, -(-remaining_slots // remaining_days))
            grouped.append(slots[start : start + amount])
            start += amount

        return grouped

    def _split_minutes(self, total_minutes: int, parts: int) -> list[int]:
        if parts < 1:
            return []

        base = total_minutes // parts
        remainder = total_minutes % parts
        return [base + (1 if index < remainder else 0) for index in range(parts)]

    def _topic_priority(self, topic: Topic) -> tuple[int, str]:
        return (-topic.weight, topic.name.lower())
