from typing import List, Optional
from datetime import datetime
from .models import Task
from .storage import load_tasks, save_tasks

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = load_tasks()
        self.next_id = self._get_next_id()

    def _get_next_id(self):
        if not self.tasks:
            return 1
        return max(t.id for t in self.tasks) + 1

    def add_task(self, title: str, due_date: Optional[datetime] = None) -> Task:
        task = Task(id=self.next_id, title=title, due_date=due_date)
        self.tasks.append(task)
        self.next_id += 1
        save_tasks(self.tasks)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((t for t in self.tasks if t.id == task_id), None)

    def complete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            task.mark_as_completed()
            save_tasks(self.tasks)
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
            save_tasks(self.tasks)
            return True
        return False
