from flask import request, abort, Blueprint
from app.models import db, Todo

todo_bp = Blueprint("todo", __name__)


@todo_bp.route("/todo")
def get_todos():
    todos = db.session.execute(db.select(Todo)).scalars().all()
    return [todo.to_dict() for todo in todos]


@todo_bp.route("/todo/<int:todo_id>")
def get_todo_by_id(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    return todo.to_dict()


@todo_bp.route("/todo/", methods=["POST"])
def create_todo():
    todo_data = request.json or {}

    if "title" not in todo_data.keys() or not todo_data["title"]:
        abort(400, "Missing required fields: title")

    try:
        todo = Todo(**todo_data)
    except TypeError as err:
        abort(400, "Failed to create todo. Check your input.")
    else:
        db.session.add(todo)
        db.session.commit()

    return todo.to_dict(), 201


@todo_bp.route("/todo/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo_data = request.json or {}

    if "title" not in todo_data.keys() or not todo_data["title"]:
        abort(400, "Missing required fields: title")

    todo = db.get_or_404(Todo, todo_id)

    todo.title = todo_data["title"]
    todo.desc = todo_data.get("desc", "")
    todo.completed = todo_data.get("completed", False)

    db.session.commit()

    return todo.to_dict()


@todo_bp.route("/todo/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = db.get_or_404(Todo, todo_id)

    db.session.delete(todo)
    db.session.commit()

    return todo.to_dict()
