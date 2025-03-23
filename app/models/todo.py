from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer

from . import db


class Todo(db.Model):
    __tablename__ = "todo"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(40), nullable=False)
    desc = mapped_column(String())

    def __repr__(self):
        return f"Todo({self.id}, {self.title}, {self.desc})"

    def to_dict(self):
        return {"id": self.id, "title": self.title, "desc": self.desc}
