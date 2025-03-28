from flask import request, abort, Blueprint, session, g
from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import validate_credentials
from sqlalchemy import exc

auth_bp = Blueprint("/", __name__)


@auth_bp.route("/register", methods=["POST"])
def register_user():
    credentials = request.json or {}
    user_email, user_password = validate_credentials(credentials)

    try:
        new_user = User(
            email=user_email, password_hash=generate_password_hash(user_password)
        )
        db.session.add(new_user)
        db.session.flush()  # flushing changes to db to catch an error
    except exc.IntegrityError:
        abort(400, f"User with email {user_email} already exists")
    else:
        db.session.commit()
        return {"message": f"User {user_email} registered successfully"}, 201


@auth_bp.route("/login", methods=["POST"])
def login_user():
    credentials = request.json or {}
    user_email, user_password = validate_credentials(credentials)

    found_user = db.session.execute(
        db.select(User).filter_by(email=user_email)
    ).scalar()

    if not found_user or not check_password_hash(
        pwhash=found_user.password_hash, password=user_password
    ):
        abort(401, "Wrong email or password")

    session.clear()
    session["user_id"] = found_user.id

    return {"message": f"User {found_user.email} logged in successfully"}


@auth_bp.route("/logout")
def logout_user():
    session.clear()

    if g.user is None:
        return {"message": "Logout attempt. User was not logged in"}

    return {"message": f"User {g.user.email} logged out successfully"}


# loading user info in global context before every request
@auth_bp.before_app_request
def load_current_use():
    user_id = session.get("user_id")

    g.user = (
        db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
        if user_id
        else None
    )
