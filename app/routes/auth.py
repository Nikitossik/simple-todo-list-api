from flask import request, abort, Blueprint
from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import validate_credentials

auth_bp = Blueprint("/", __name__)


@auth_bp.route("/register", methods=["POST"])
def register_user():
    credentials = request.json or {}
    user_email, user_password = validate_credentials(credentials)

    found_user = db.session.execute(
        db.select(User).filter_by(email=user_email)
    ).scalar()

    if found_user:
        abort(400, "User with this email already exists")

    new_user = User(
        email=user_email, password_hash=generate_password_hash(user_password)
    )
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User registered successfully"}, 201


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

    return {"message": "User logged in successfully"}
