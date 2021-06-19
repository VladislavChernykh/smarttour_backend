from flask import Blueprint, request

hello = Blueprint("hello", __name__)


@hello.route("/hey", methods=["GET"])
def hello_user():
    cfg = request.args
    username = cfg["username"]
    return f"Hello {username}!"
