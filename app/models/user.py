from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer
from . import db


class User(db.Model):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(100), unique=True, nullable=False)
    password_hash = mapped_column(String(256), nullable=False)

    todos = relationship("Todo", back_populates="user")

    def __repr__(self):
        return f"User({self.id}, {self.email})"
