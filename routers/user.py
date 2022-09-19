import controllers.user
from decorators.authentication import login_required
from flask import Blueprint, jsonify, request, render_template, session


user_router = Blueprint('user_router', __name__)

@user_router.route("/", methods=["GET"])
def index():
    return "Hello World!"

@user_router.route("/register", methods=["POST", "GET"])
def register():
    if(request.method == "POST"):
        return controllers.user.register(request)
@user_router.route("/login", methods=["POST", "GET"])
def login():
    if request.method("POST"):
    if request.method == "POST":

        return controllers.user.login()
    return render_template("login.html")

@user_router.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    return controllers.user.logout()

@user_router.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():
    return controllers.user.forgot_password()

@user_router.route("/register_seller", methods=["POST", "GET"])
def register_seller():
    return controllers.user.register_seller()






