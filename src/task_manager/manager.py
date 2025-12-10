import json
import os
from datetime import datetime, timedelta
from typing import Optional, List
from .models import Task

DATA_PATH = os.path.expanduser("/home/gio/Desktop/task-cli-manager/src/tasks.json")
PRIORITIES = {"LOW", "MEDIUM", "HIGH"}

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id: int = 1
        self._load()

    def _load(self):
        if not os.path.exists(DATA_PATH):
            os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
            self._save()
            return

        try:
            with open(DATA_PATH, "r") as f:
                raw = json.load(f)

            self.tasks = [Task.from_dict(t) for t in raw.get("tasks", [])]
            self.next_id = raw.get("next_id", 1)

        except json.JSONDecodeError:
            self.tasks = []
            self.next_id = 1
            self._save()

    def _save(self):
        data = {
            "tasks": [t.to_dict() for t in self.tasks],
            "next_id": self.next_id
        }
        with open(DATA_PATH, "w") as f:
            json.dump(data, f, indent=4)

    # ADD
    def add_task(
        self,
        title: str,
        due_date: Optional[datetime] = None,
        priority: str = "MEDIUM",
        tags: Optional[List[str]] = None,
        recurrence: Optional[str] = None
    ) -> Task:

        if priority not in PRIORITIES:
            raise ValueError(f"Priority must be one of {PRIORITIES}")

        task = Task(
            id=self.next_id,
            title=title,
            due_date=due_date,
            priority=priority,
            tags=tags or [],
            recurrence=recurrence
        )

        self.tasks.append(task)
        self.next_id += 1
        self._save()
        return task

    # LIST
    def list_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        if completed is None:
            return self.tasks
        return [t for t in self.tasks if t.completed == completed]

    # GET
    def get_task(self, task_id: int) -> Optional[Task]:
        return next((t for t in self.tasks if t.id == task_id), None)

    # COMPLETE
    def complete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False

        task.mark_as_completed()
        self._save()

        # RECURRENCE HANDLING
        if task.recurrence and task.due_date:
            if task.recurrence == "daily":
                new_due = task.due_date + timedelta(days=1)
            elif task.recurrence == "weekly":
                new_due = task.due_date + timedelta(weeks=1)
            elif task.recurrence == "monthly":
                new_due = task.due_date + timedelta(days=30)
            else:
                new_due = None

            if new_due:
                self.add_task(
                    title=task.title,
                    due_date=new_due,
                    priority=task.priority,
                    tags=task.tags,
                    recurrence=task.recurrence
                )

        return True

    # DELETE
    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False

        self.tasks.remove(task)
        self._save()
        return True
