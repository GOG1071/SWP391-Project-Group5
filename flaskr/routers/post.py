import controllers.post
from decorators.authentication import login_required
from flask import Blueprint, jsonify, request, render_template, session

post_router = Blueprint('post_router', __name__)

@post_router.route("/create", methods=["POST", "GET"])
def post():
    if request.method == "POST":
        return controllers.post.post()
    return render_template("create_post.html")
