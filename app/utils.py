from flask import abort
import re


def validate_credentials(data):
    user_email = data.get("email")
    user_password = data.get("password")

    if not user_email or not user_password:
        abort(400, "Missing credentials: email or password")

    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, user_email):
        abort(400, "Invalid email")

    return user_email, user_password
