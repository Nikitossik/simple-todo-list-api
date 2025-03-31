from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String, CheckConstraint, ForeignKey
from datetime import datetime, timezone
from . import Base
from .user import User


def current_datetime():
    return datetime.now(timezone.utc).isoformat()


class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    desc: Mapped[str | None]
    status: Mapped[str] = mapped_column(String(15), default="todo")
    created_at: Mapped[str] = mapped_column(String, default=current_datetime)
    updated_at: Mapped[str] = mapped_column(
        String, default=current_datetime, onupdate=current_datetime
    )

    CheckConstraint('status in ("todo", "in-progress", "done")', name="status_check")

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)
    user: Mapped[User] = relationship("User", back_populates="todos")

    def __repr__(self):
        return f"Todo({self.id}, {self.title}, {self.desc}, {self.completed})"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "desc": self.desc,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user_id": self.user_id,
        }
