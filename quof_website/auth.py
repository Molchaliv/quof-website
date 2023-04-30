import json

from .models import db, User
from .utils import generate_api_key

from werkzeug.security import generate_password_hash, check_password_hash

from flask import Blueprint, Response, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required


auth = Blueprint("auth", __name__)


@auth.route("/login")
def login() -> str:
    """ Shows the login page. """

    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post() -> Response:
    """ Handles the login request and skips/doesn't skip the user. """

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=True)
    return redirect(url_for("main.index"))


@auth.route("/signup")
def signup() -> str:
    """ Shows the signup page. """

    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post() -> Response:
    """ Processes the registration request and registers/does not register the user. """

    email = request.form.get("email")
    name = request.form.get("username")
    password = request.form.get("password")

    if User.query.filter_by(email=email).first():
        flash("User with this email already exists!")
        return redirect(url_for("auth.signup"))

    db.session.add(
        User(email=email, name=name, password=generate_password_hash(password, method="sha256"))
    )
    db.session.commit()

    with open(f"{auth.root_path}\\static\\api\\api_keys.json", mode="r", encoding="utf-8") as file:
        api_keys = json.loads(file.read())

    api_keys = {email: generate_api_key(), **api_keys}
    
    with open(f"{auth.root_path}\\static\\api\\api_keys.json", mode="w", encoding="utf-8") as file:
        file.write(json.dumps(api_keys, indent=2, ensure_ascii=False))

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout() -> Response:
    """ Logs out. """

    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/delete")
@login_required
def delete() -> str:
    """ Shows a page to confirm deletion of the page. """

    return render_template("delete.html")


@auth.route("/immediate_delete")
@login_required
def immediate_delete() -> Response:
    """ Removes the current user immediately. """

    User.query.filter_by(email=current_user.email).delete()
    db.session.commit()

    return redirect(url_for("main.index"))
