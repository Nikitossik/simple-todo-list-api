from .auth import auth_bp
from .todo import todo_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(todo_bp, url_prefix="/api")
