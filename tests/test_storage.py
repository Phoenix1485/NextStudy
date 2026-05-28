from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from nextstudy.models import Subject
from nextstudy.planner import StudyPlanner
from nextstudy.storage import JsonPlanStorage


class JsonPlanStorageTest(unittest.TestCase):
    def test_saves_and_loads_plan_without_losing_data(self) -> None:
        subject = Subject("Englisch")
        subject.add_topic("Tenses", "mittel")
        subject.add_topic("Essay Writing", "schwer")
        plan = StudyPlanner().create_plan(subject, days=3, minutes_per_day=50)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            storage = JsonPlanStorage()
            storage.save(plan, path)
            loaded_plan = storage.load(path)

        self.assertEqual(loaded_plan.subject.name, "Englisch")
        self.assertEqual(len(loaded_plan.subject.topics), 2)
        self.assertEqual(len(loaded_plan.units), len(plan.units))
        self.assertEqual(loaded_plan.to_dict(), plan.to_dict())


if __name__ == "__main__":
    unittest.main()

