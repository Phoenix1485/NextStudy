"""JSON-Speicherung fuer NextStudy."""

from __future__ import annotations

import json
from pathlib import Path

from nextstudy.models import StudyPlan


DEFAULT_PLAN_PATH = Path("nextstudy_plan.json")


class JsonPlanStorage:
    """Speichert und laedt Lernplaene als gut lesbare JSON-Dateien."""

    def save(self, plan: StudyPlan, path: str | Path = DEFAULT_PLAN_PATH) -> Path:
        target = Path(path)
        if target.parent != Path("."):
            target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text(
            json.dumps(plan.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return target

    def load(self, path: str | Path = DEFAULT_PLAN_PATH) -> StudyPlan:
        source = Path(path)
        if not source.exists():
            raise FileNotFoundError(f"Die Datei '{source}' wurde nicht gefunden.")

        data = json.loads(source.read_text(encoding="utf-8"))
        return StudyPlan.from_dict(data)

