
from decorators.authentication import login_required
from flask import Blueprint, request, render_template, flash
import controllers.post


post_router = Blueprint('post_router', __name__)

@post_router.route('/load_post',methods=["POST", "GET"])

@login_required

def load_post():

    return controllers.post.load_post()


@post_router.route('/delete_post',methods=["POST", "GET"])
@login_required

def delete_post():
    if request.method == "POST":
        return controllers.post.delete_post()



@post_router.route('/load_for_update',methods=["POST", "GET"])
@login_required
def load_for_update():
    if request.method == "POST":
        return controllers.post.load_for_update()
    flash("can't update","info")
    return render_template("manage_posted.html")



@post_router.route('/update_post',methods=["POST", "GET"])
@login_required

def update_post():
    if request.method == "POST":
        return controllers.post.update_post()

@post_router.route('/create_post',methods=["POST", "GET"])
@login_required
def create_post():
    if request.method == "POST":
        return controllers.post.create_post()
    return render_template("manage_posted.html")
@post_router.route('/post_detail',methods=["POST", "GET"])
@login_required
def post_detail():
    if request.method == "POST":
        return controllers.post.post_detail()
    return render_template("post_detail.html")
