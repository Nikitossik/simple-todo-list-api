from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .todo import Todo
from . import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)

    todos: Mapped[list["Todo"]] = relationship("Todo", back_populates="user")

    def __repr__(self):
        return f"User({self.id}, {self.email})"
