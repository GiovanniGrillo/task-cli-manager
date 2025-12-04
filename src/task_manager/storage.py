import json
from pathlib import Path
from datetime import datetime
from typing import List
from .models import Task

STORAGE_FILE = Path(__file__).parent.parent.parent / "tasks.json"

def load_tasks() -> List[Task]:
    STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if not STORAGE_FILE.exists():
        return []

    with open(STORAGE_FILE, "r") as f:
        raw = json.load(f)

    tasks = []
    for t in raw:
        tasks.append(
            Task(
                id=t["id"],
                title=t["title"],
                completed=t["completed"],
                created_at=datetime.fromisoformat(t["created_at"]),
                due_date=datetime.fromisoformat(t["due_date"]) if t["due_date"] else None,
                priority=t.get("priority", "MEDIUM"),
            )
        )
    return tasks


def save_tasks(tasks: List[Task]) -> None:
    data = []
    for t in tasks:
        data.append({
            "id": t.id,
            "title": t.title,
            "completed": t.completed,
            "created_at": t.created_at.isoformat(),
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "priority": t.priority,
        })

    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)
