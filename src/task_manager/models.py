from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

PRIORITIES = ("LOW", "MEDIUM", "HIGH")

@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None
    priority: str = "MEDIUM"
    tags: List[str] = field(default_factory=list)

    def mark_as_completed(self):
        self.completed = True

    def is_overdue(self) -> bool:
        if self.due_date and not self.completed:
            return datetime.utcnow() > self.due_date
        return False

    def to_dict(self):
        """Convert the task to a JSON-serializable dict"""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "tags": self.tags,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        """Create a Task from its dictionary form"""
        return Task(
            id=data["id"],
            title=data["title"],
            completed=data["completed"],
            created_at=datetime.fromisoformat(data["created_at"]),
            due_date=datetime.fromisoformat(data["due_date"]) if data["due_date"] else None,
            priority=data.get("priority", "MEDIUM"),
            tags=data.get("tags", []),
        )
