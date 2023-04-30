from .api import api
from .auth import auth
from .block import block
from .main import main

from .models import db, User

from flask import Flask, render_template
from flask_login import LoginManager


def error_page(error: str) -> tuple[str, int]:
    """ Shows a custom error window. """

    return render_template("error.html"), int(str(error)[:3])


def create_app() -> Flask:
    """ Creates and configures the main Flask application. """

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "vgxZg2mrMe3IP46g7&0%SZJxeKYqZFcV!du"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.root_path}\\database\\database.sqlite"

    for error_code in [404, 403, 410, 500]:
        app.register_error_handler(error_code, error_page)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import models
    with app.app_context():
        db.create_all()

    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(block)
    app.register_blueprint(main)

    return app
