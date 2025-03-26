from flask import abort, g
from functools import wraps
import re


# decorator for checking if user is logged in
def login_required(handler):
    @wraps(handler)
    def endpoint_wrapper(**kwargs):
        if g.user is None:
            return abort(403, "Login is required to access this route")
        return handler(**kwargs)

    return endpoint_wrapper


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
