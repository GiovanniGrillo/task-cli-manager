import json
from datetime import datetime
from typing import List
from .models import Task

FILE_PATH = "tasks.json"


def datetime_to_str(dt: datetime):
    return dt.isoformat() if dt else None


def datetime_from_str(s: str):
    return datetime.fromisoformat(s) if s else None


def save_tasks(tasks: List[Task]):
    data = []
    for t in tasks:
        data.append({
            "id": t.id,
            "title": t.title,
            "completed": t.completed,
            "created_at": datetime_to_str(t.created_at),
            "due_date": datetime_to_str(t.due_date),
        })
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=2)


def load_tasks() -> List[Task]:
    try:
        with open(FILE_PATH, "r") as f:
            raw = json.load(f)
    except FileNotFoundError:
        return []

    tasks = []
    for d in raw:
        task = Task(
            id=d["id"],
            title=d["title"],
            completed=d["completed"],
            created_at=datetime_from_str(d["created_at"]) if d["created_at"] is not None else datetime.now(),
            due_date=datetime_from_str(d["due_date"]),
        )
        tasks.append(task)
    return tasks
