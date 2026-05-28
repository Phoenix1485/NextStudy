from __future__ import annotations

import unittest

from nextstudy.models import Status, Subject
from nextstudy.planner import StudyPlanner


class StudyPlannerTest(unittest.TestCase):
    def test_creates_weighted_plan_with_final_review(self) -> None:
        subject = Subject("LF5")
        subject.add_topic("Variablen", "leicht")
        subject.add_topic("Schleifen", "mittel")
        subject.add_topic("Klassen", "schwer")

        plan = StudyPlanner().create_plan(subject, days=4, minutes_per_day=60)

        self.assertEqual(plan.days, 4)
        self.assertEqual(sum(unit.duration_minutes for unit in plan.units_for_day(1)), 60)
        self.assertTrue(any(unit.topic == "Gesamtwiederholung" for unit in plan.units_for_day(4)))
        self.assertGreaterEqual(
            sum("Klassen" in unit.topic for unit in plan.units),
            sum("Variablen" in unit.topic for unit in plan.units),
        )

    def test_rejects_plan_without_topics(self) -> None:
        with self.assertRaises(ValueError):
            StudyPlanner().create_plan(Subject("Mathematik"), days=3, minutes_per_day=45)

    def test_updates_statistics_after_status_change(self) -> None:
        subject = Subject("Chemie")
        subject.add_topic("Redox", "schwer")

        plan = StudyPlanner().create_plan(subject, days=2, minutes_per_day=45)
        plan.update_status(1, Status.DONE)

        stats = plan.statistics()
        self.assertEqual(stats["done"], 1)
        self.assertGreater(stats["progress"], 0)

    def test_one_day_plan_keeps_daily_time_budget(self) -> None:
        subject = Subject("Mathematik")
        subject.add_topic("Funktionen", "schwer")
        subject.add_topic("Gleichungen", "mittel")

        plan = StudyPlanner().create_plan(subject, days=1, minutes_per_day=40)

        self.assertEqual(sum(unit.duration_minutes for unit in plan.units_for_day(1)), 40)


if __name__ == "__main__":
    unittest.main()
