from flask import Flask, request, jsonify
import os
from .models import db, Todo

basedir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.db")

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/api/todo")
def get_todos():
    todos = db.session.execute(db.select(Todo)).scalars().all()
    return [todo.to_dict() for todo in todos]


@app.route("/api/todo/<int:todo_id>")
def get_todo_by_id(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    return todo.to_dict()


@app.route("/api/todo", methods=["POST"])
def create_todo():
    todo_data = request.json

    todo = Todo(**todo_data)
    db.session.add(todo)
    db.session.commit()

    return todo.to_dict()


@app.route("/api/todo/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo_data = request.json

    todo = db.get_or_404(Todo, todo_id)

    todo.title = todo_data["title"]
    todo.desc = todo_data["desc"]

    db.session.commit()

    return todo.to_dict()


@app.route("/api/todo/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = db.get_or_404(Todo, todo_id)

    db.session.delete(todo)
    db.session.commit()

    return todo.to_dict()
