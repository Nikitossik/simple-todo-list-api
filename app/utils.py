from flask import abort, g
from functools import wraps
import re


# decorator for checking if user is logged in
def login_required(handler):
    @wraps(handler)
    def endpoint_wrapper(**kwargs):
        if g.user is None:
            return abort(401, "Login is required to access this route")
        return handler(**kwargs)

    return endpoint_wrapper


# decorator for checking if logged user is the owner of todo
def check_todo_user(todo):
    if g.user and g.user.id != todo.user_id:
        abort(403)


def validate_pagination(request):
    try:
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("pageSize", 10))
    except ValueError:
        page, page_size = 1, 10

    return page, page_size


def validate_sort(request):
    allowed_sort_fields = ["id", "title", "created_at", "updated_at"]

    sort_by = request.args.get("sort_by", "id")
    desc = request.args.get("desc", "false")

    if sort_by not in allowed_sort_fields:
        sort_by = "id"

    if desc not in ["true", "false"]:
        desc = "false"

    return sort_by, True if desc == "true" else False


def validate_credentials(data):
    user_email = data.get("email")
    user_password = data.get("password")

    if not user_email or not user_password:
        abort(400, "Missing credentials: email or password")

    user_email = validate_email(user_email)
    user_password = validate_password(user_password)

    return user_email, user_password


def validate_email(email):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, email):
        abort(400, "Invalid email")

    return email


def validate_password(password):
    if len(password) < 6:
        abort(400, "Password must containt at least 6 symbols")

    return password
