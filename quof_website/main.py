import json
import os

from .utils import generate_html

from flask import (Blueprint, Response, render_template,
                   url_for, send_file, abort, jsonify, request, redirect)
from flask_login import login_required, current_user


main = Blueprint("main", __name__)


@main.route("/")
def index() -> str:
    """ Shows the main page of the site. """

    name = "Anonymous"
    if hasattr(current_user, "name"):
        name = current_user.name

    email = "null"
    if hasattr(current_user, "email"):
        email = current_user.email

    return render_template(
        "index.html", name=name, email=email,
        avatar_path=url_for("static", filename="/images/user.png"),
        admin_email="quof.noreply@gmail.com"
    )


@main.route("/versions")
def versions_list() -> Response:
    """ Shows a json file with links to download the notepad. """

    with open(f"{main.root_path}\\static\\downloads\\versions.json", mode="r", encoding="utf-8") as file:
        versions = json.loads(file.read())

    output = {}
    for version, _ in versions.items():
        if version == "last_version":
            output[version] = (f"{request.headers['Host']}/download",
                               f"{request.headers['Host']}/api/<api_key>/download")
        else:
            output[version] = (f"{request.headers['Host']}/download/{version}",
                               f"{request.headers['Host']}/api/<api_key>/download/{version}")

    return jsonify(output)


@main.route("/download")
@login_required
def download() -> Response:
    """ Downloads the latest version of notepad (only if the user is logged in). """

    with open(f"{main.root_path}\\static\\downloads\\versions.json", mode="r", encoding="utf-8") as file:
        versions = json.loads(file.read())

    return send_file(versions["last_version"], as_attachment=True)


@main.route("/download/<version>")
@login_required
def download_version(version: str) -> Response:
    """ Downloads the selected version of notepad (only if the user is logged in). """

    with open(f"{main.root_path}\\static\\downloads\\versions.json", mode="r", encoding="utf-8") as file:
        versions = json.loads(file.read())

    if version in versions:
        return send_file(versions[version], as_attachment=True)
    else:
        return abort(404)


@main.route("/docs")
def docs() -> str:
    """ Shows a page with links to documentation. """

    with open(f"{main.root_path}\\static\\docs\\doc_list.json", mode="r", encoding="utf-8") as file:
        data = [(chunk["title"], chunk["brief"], f"docs/{chunk['url']}") for chunk in json.loads(file.read())]

    output = [data[data_index:data_index + 3] for data_index in range(0, len(data), 3)]

    return render_template("docs.html", documentations=output)


@main.route("/docs/<documentation>")
def docs_find(documentation: str) -> str:
    """ Shows the page with the selected documentation. """

    if os.path.exists(f"{main.root_path}\\templates\\docs\\{documentation}.html"):
        return render_template(f"docs/{documentation}.html")
    return abort(404)


@main.route("/create_doc")
def create_doc() -> str:
    """ Shows a page for creating documentation (only if the current user is an administrator). """

    if hasattr(current_user, "email") and current_user.email == "quof.noreply@gmail.com":
        return render_template("create_doc.html")
    return abort(404)


@main.route("/create_doc", methods=["POST"])
def create_doc_post() -> Response:
    """ Handles a request to create documentation. """

    if hasattr(current_user, "email") and current_user.email == "quof.noreply@gmail.com":
        title = request.form.get("title")
        brief = request.form.get("brief")
        url = request.form.get("url")
        markdown = request.form.get("markdown")

        with open(f"{main.root_path}\\static\\docs\\doc_list.json", mode="r", encoding="utf-8") as file:
            doc_list = json.loads(file.read())

        doc_list.append({"title": title, "brief": brief, "url": url})

        with open(f"{main.root_path}\\static\\docs\\doc_list.json", mode="w", encoding="utf-8") as file:
            file.write(json.dumps(doc_list, indent=2, ensure_ascii=False))

        with open(f"{main.root_path}\\templates\\docs\\{url}.html", mode="w", encoding="utf-8") as file:
            file.write(generate_html(title, markdown))

        return redirect(f"/docs/{url}")

    return abort(404)
