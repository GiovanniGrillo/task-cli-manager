from typing import List, Optional
from datetime import datetime
from .models import Task, PRIORITIES
from .storage import load_tasks, save_tasks

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = load_tasks()
        self.next_id = self._compute_next_id()

    def _compute_next_id(self) -> int:
        if not self.tasks:
            return 1
        return max(t.id for t in self.tasks) + 1

    def _save(self):
        save_tasks(self.tasks)

    def add_task(self, title: str, due_date: Optional[datetime] = None, priority: str = "MEDIUM") -> Task:
        if priority not in PRIORITIES:
            raise ValueError(f"Priority must be one of {PRIORITIES}")

        task = Task(id=self.next_id, title=title, due_date=due_date, priority=priority)
        self.tasks.append(task)
        self.next_id += 1
        self._save()
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((t for t in self.tasks if t.id == task_id), None)

    def complete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            task.completed = True
            self._save()
            return True
        return False

    def list_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        if completed is None:
            return self.tasks
        return [t for t in self.tasks if t.completed == completed]

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self._save()
            return True
        return False
