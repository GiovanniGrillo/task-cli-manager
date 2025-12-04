from typing import List, Optional
from datetime import datetime
from .models import Task

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, due_date: Optional[datetime] = None) -> Task:
        task = Task(id=self.next_id, title=title, due_date=due_date)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def complete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            task.mark_as_completed()
            return True
        return False

    def list_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        if completed is None:
            return self.tasks
        return [task for task in self.tasks if task.completed == completed]

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
