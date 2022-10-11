import controllers.user
from decorators.authentication import login_required
from flask import Blueprint, jsonify, request, render_template, session
from models.user import UserRole, User
from models.post import  Post


user_router = Blueprint('user_router', __name__)

@user_router.route("/home", methods=["POST", "GET"])
def home():
    return controllers.user.home()

@user_router.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST" and request.form.get("password") == request.form.get("cf_password"):
        return controllers.user.register(request.form.get("username"), request.form.get("password"), request.form.get("email"))

    return render_template("register.html")

@user_router.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return controllers.user.login()
    return render_template("login.html")


@user_router.route("/logout", methods=["GET"])
# @login_required
def logout():
    return controllers.user.logout()

@user_router.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():
    if(request.method == "POST"):
        return controllers.user.forgot_password(request.form.get("email"))
    else:
        return render_template("forgot_password.html")

@user_router.route("/register_seller", methods=["POST", "GET"])
def register_seller():
    if(request.method == "POST"):
        return controllers.user.register_seller(request.form.get("username"), request.form.get("email"))
    else:
        return render_template("register_seller.html")

@user_router.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    return controllers.user.profile()

@user_router.route("/profile/edit", methods=["POST", "GET"])
@login_required
def edit_profile():
    if(request.method == "GET"):
        return render_template("editProfile.html")
    return controllers.user.edit_profile()


@user_router.route("/post/<string:username>")
@login_required
def user_posts(username):
    return controllers.user.user_posts(username)

@user_router.route("/bookmark")
@login_required
def bookmark():
    return controllers.user.bookmark()


