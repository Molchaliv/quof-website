import json

from flask import Blueprint, Response, render_template, send_file, abort
from flask_login import current_user


api = Blueprint("api", __name__)


@api.route("/api")
def show_api_key() -> str:
    """ Shows a page with the api key of the current user. """

    email = ""
    if hasattr(current_user, "email"):
        email = current_user.email

    with open(f"{api.root_path}\\static\\api\\api_keys.json", mode="r", encoding="utf-8") as file:
        api_keys = json.loads(file.read())

    api_key = ""
    if email in api_keys:
        api_key = api_keys[email]

    return render_template("api.html", api_key=api_key)


@api.route("/api/<api_key>/download")
def download_api(api_key: str) -> Response:
    """ Download the latest version of notepad using api key. """

    with open(f"{api.root_path}\\static\\api\\api_keys.json", mode="r", encoding="utf-8") as file:
        api_keys = json.loads(file.read())

    with open(f"{api.root_path}\\static\\downloads\\versions.json", mode="r", encoding="utf-8") as file:
        versions = json.loads(file.read())

    if api_key in api_keys.values():
        return send_file(versions["last_version"])
    else:
        return abort(404)


@api.route("/api/<api_key>/download/<version>")
def download_version_api(api_key: str, version: str) -> Response:
    """ Downloads the selected version of notepad using an api key. """

    with open(f"{api.root_path}\\static\\api\\api_keys.json", mode="r", encoding="utf-8") as file:
        api_keys = json.loads(file.read())

    with open(f"{api.root_path}\\static\\downloads\\versions.json", mode="r", encoding="utf-8") as file:
        versions = json.loads(file.read())

    if api_key in api_keys.values():
        if version in versions:
            return send_file(versions["last_version"])
        else:
            return abort(404)
    else:
        return abort(404)
