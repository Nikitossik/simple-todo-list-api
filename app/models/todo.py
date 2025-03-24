from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, Boolean
from datetime import datetime, timezone
from . import db


def current_datetime():
    return datetime.now(timezone.utc).isoformat()


class Todo(db.Model):
    __tablename__ = "todo"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(100), nullable=False)
    desc = mapped_column(String())
    completed = mapped_column(Boolean, default=False)
    created_at = mapped_column(String, default=current_datetime)
    updated_at = mapped_column(
        String, default=current_datetime, onupdate=current_datetime
    )

    def __repr__(self):
        return f"Todo({self.id}, {self.title}, {self.desc}, {self.completed})"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "desc": self.desc,
            "completed": self.completed,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
