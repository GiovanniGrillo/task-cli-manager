from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

PRIORITIES = ("LOW", "MEDIUM", "HIGH")
RECURRENCES = ("daily", "weekly", "monthly")

@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None
    priority: str = "MEDIUM"
    tags: List[str] = field(default_factory=list)
    recurrence: Optional[str] = None  # daily, weekly, monthly

    def mark_as_completed(self):
        self.completed = True

    def is_overdue(self) -> bool:
        if self.due_date and not self.completed:
            return datetime.utcnow() > self.due_date
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "tags": self.tags,
            "recurrence": self.recurrence,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            id=data["id"],
            title=data["title"],
            completed=data.get("completed", False),
            created_at=datetime.fromisoformat(data.get("created_at")),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            priority=data.get("priority", "MEDIUM"),
            tags=data.get("tags", []),
            recurrence=data.get("recurrence"),
        )
