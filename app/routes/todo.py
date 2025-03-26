from flask import request, abort, Blueprint, g
from app.models import db, Todo
from app.utils import login_required, check_todo_user, validate_pagination

todo_bp = Blueprint("todo", __name__)


@todo_bp.route("/todo")
@login_required
def get_todos():
    page, page_size = validate_pagination(request)

    todos_page = db.paginate(db.select(Todo), page=page, per_page=page_size)

    return {
        "data": [todo.to_dict() for todo in todos_page.items],
        "page": todos_page.page,
        "pageSize": todos_page.per_page,
        "total": todos_page.total,
    }


@todo_bp.route("/todo/<int:todo_id>")
@login_required
def get_todo_by_id(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    return todo.to_dict()


@todo_bp.route("/todo/", methods=["POST"])
@login_required
def create_todo():
    todo_data = request.json or {}
    title = todo_data.get("title")
    desc = todo_data.get("desc")

    if not title:
        abort(400, "Missing required field: title")

    try:
        todo = Todo(title=title, desc=desc, user=g.user)
    except TypeError:
        abort(400, "Failed to create todo. Check your input.")
    else:
        db.session.add(todo)
        db.session.commit()

    return todo.to_dict(), 201


@todo_bp.route("/todo/<int:todo_id>", methods=["PUT"])
@login_required
def update_todo(todo_id):
    todo_data = request.json or {}

    if not todo_data.get("title"):
        abort(400, "Missing required field: title")

    todo = db.get_or_404(Todo, todo_id)

    check_todo_user(todo)

    todo.title = todo_data.get("title")
    todo.desc = todo_data.get("desc", "")
    todo.completed = todo_data.get("completed", False)

    db.session.commit()

    return todo.to_dict()


@todo_bp.route("/todo/<int:todo_id>", methods=["DELETE"])
@login_required
def delete_todo(todo_id):
    todo = db.get_or_404(Todo, todo_id)

    check_todo_user(todo)

    db.session.delete(todo)
    db.session.commit()

    return todo.to_dict()
