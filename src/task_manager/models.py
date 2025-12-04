from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None

    def mark_as_completed(self):
        self.completed = True

    def is_overdue(self) -> bool:
        if self.due_date and not self.completed:
            return datetime.utcnow() > self.due_date
        return False

