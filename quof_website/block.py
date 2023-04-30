from flask import Blueprint, abort
from flask_login import current_user


block = Blueprint("block", __name__)


@block.route("/static/api/api_keys.json")
def block_api_keys() -> None:
    """ Blocks access to the system file 'api_keys.json'. """

    return abort(404)


@block.route("/static/downloads/files/<file>")
def block_download_files() -> None:
    """ Blocks access to downloading the notepad (only if the user is not registered). """

    if not hasattr(current_user, "email"):
        return abort(404)
