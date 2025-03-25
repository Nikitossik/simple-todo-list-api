from flask import Flask, json
from werkzeug.exceptions import HTTPException
from .models import db
from .routes import register_routes
import os

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, "data.db"
    )
    app.config["SECRET_KEY"] = "my_secret_key"
    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps(
            {"code": e.code, "name": e.name, "description": e.description}
        )

        response.content_type = "application/json"
        return response

    return app
