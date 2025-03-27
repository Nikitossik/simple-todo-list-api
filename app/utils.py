from flask import abort, g
from functools import wraps
import re
from datetime import datetime
from .models import Todo


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


def parse_pagination(request):
    try:
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("pageSize", 10))
    except ValueError:
        page, page_size = 1, 10

    return page, page_size


def parse_sort(request):
    allowed_sort_fields = ["id", "title", "created_at", "updated_at"]

    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")

    if sort_by not in allowed_sort_fields:
        sort_by = "id"

    if order not in ["asc", "desc"]:
        order = "asc"

    return sort_by, order


def build_filters(filters):
    filters_map = {
        "status": lambda v: Todo.status.in_(v) if type(v) is list else Todo.status == v,
        "user": lambda v: Todo.user_id.in_(v) if type(v) is list else Todo.status == v,
        "created_at_min": lambda v: Todo.created_at >= v,
        "created_at_max": lambda v: Todo.created_at <= v,
        "updated_at_min": lambda v: Todo.updated_at >= v,
        "updated_at_max": lambda v: Todo.updated_at <= v,
    }

    conditions = []

    for k, v in filters.items():
        if k in filters_map.keys() and v:
            conditions.append(filters_map[k](v))

    return conditions


def parse_filters(request):
    filters = dict()

    filters["status"] = parse_list_values(request, "status")
    filters["user"] = parse_list_values(request, "user", argtype=int)
    filters["created_at_min"] = parse_date_value(request, "created_at_min")
    filters["created_at_max"] = parse_date_value(request, "created_at_max")
    filters["updated_at_min"] = parse_date_value(request, "updated_at_min")
    filters["updated_at_max"] = parse_date_value(request, "updated_at_max")

    print(filters)

    return filters


def parse_date_value(request, arg):
    argstring = request.args.get(arg, "").strip()
    date_value = ""
    print("date: ", type(argstring))

    try:
        date_value = datetime.fromisoformat(argstring)
    except ValueError:
        pass

    return date_value


def parse_list_values(request, arg, argtype=str):
    argstring = request.args.get(arg, "").strip()
    values = []

    if argstring:
        values = [val.strip() for val in argstring.split(",")]

    if argtype is int:
        values = [int(val) for val in values if val.isdigit()]

    return values


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
