from flask import abort, g, Request
from functools import wraps
import re
from datetime import datetime
from .models import Todo
from typing import TypedDict, cast


class Filters(TypedDict, total=False):
    status: list[str]
    user: list[int]
    created_at_min: datetime | None
    created_at_max: datetime | None
    updated_at_min: datetime | None
    updated_at_max: datetime | None


def login_required(handler):
    """Checks if user is available in the session. Othervise aborts with 401 HTTPException"""

    @wraps(handler)
    def endpoint_wrapper(**kwargs):
        if g.user is None:
            return abort(401, "Login is required to access this route")
        return handler(**kwargs)

    return endpoint_wrapper


def check_todo_user(todo: Todo):
    """Checks if current user is the owner of todo"""
    if g.user and g.user.id != todo.user_id:
        abort(403)


def parse_pagination(request: Request) -> tuple[int, int]:
    """
    Parses pagination parameters - page and pageSize from a query string.
    If values are invalid, returns default: 1 and 10 for page and pageSize respectfully.
    """
    try:
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("pageSize", 10))
    except ValueError:
        page, page_size = 1, 10

    return page, page_size


def parse_sort(request: Request) -> tuple[str, str]:
    """
    Parses sorting parameters - sort_by and order from a query string.
    The default values for values are "id" and "asc"
    """
    allowed_sort_fields = ["id", "title", "created_at", "updated_at"]

    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")

    if sort_by not in allowed_sort_fields:
        sort_by = "id"

    if order not in ["asc", "desc"]:
        order = "asc"

    return sort_by, order


def build_filters(filters: Filters) -> list[bool]:
    """
    Compiles filters object to SQLAlchemy filters and returns
    """
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


def parse_filters(request: Request) -> Filters:
    """
    Parses filter params from a query string
    """
    filters: Filters = dict()

    # separated the logic of list type parsing

    filters["status"] = parse_str_list_values(request, "status")
    filters["user"] = parse_int_list_values(request, "user")
    filters["created_at_min"] = parse_date_value(request, "created_at_min")
    filters["created_at_max"] = parse_date_value(request, "created_at_max")
    filters["updated_at_min"] = parse_date_value(request, "updated_at_min")
    filters["updated_at_max"] = parse_date_value(request, "updated_at_max")

    return filters


def parse_date_value(request: Request, arg: str) -> datetime | None:
    """
    A helper function to parse a date in ISO format
    """
    argstring: str = request.args.get(arg, "").strip()

    try:
        return datetime.fromisoformat(argstring)
    except ValueError:
        return None


def parse_str_list_values(request: Request, arg: str) -> list[str]:
    """
    A helper function to parse multiple values str of the argument from a query string divided by "," into a list
    """
    argstring: str = request.args.get(arg, "").strip()
    values: list[str] = []

    if argstring:
        values = [val.strip() for val in argstring.split(",")]

    return values


def parse_int_list_values(request: Request, arg: str) -> list[int]:
    """
    A helper function to parse multiple int values of the argument from a query string divided by "," into a list
    """
    argstring: str = request.args.get(arg, "").strip()
    values: list[int] = []
    if argstring:
        str_values = [val.strip() for val in argstring.split(",")]
        values = [int(val) for val in str_values if val.isdigit()]

    return values


def validate_credentials(data: dict[str, str]) -> tuple[str, str]:
    """
    Parses login and register data: email and password
    """
    user_email = data.get("email")
    user_password = data.get("password")

    if not user_email or not user_password:
        abort(400, "Missing credentials: email or password")

    user_email = validate_email(user_email)
    user_password = validate_password(user_password)

    return user_email, user_password


def validate_email(email: str) -> str:
    """
    A helper function to validate email
    """
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, email):
        abort(400, "Invalid email")

    return email


def validate_password(password: str) -> str:
    """
    A helper function to validate password
    """
    if len(password) < 6:
        abort(400, "Password must containt at least 6 symbols")

    return password
