from decorators.authentication import login_required,admin_required
from flask import Blueprint, jsonify, request, render_template, session,url_for,flash
from controllers import post
from models.post import Post
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
    return render_template("post/manage_posted.html")



@post_router.route('/update_post',methods=["POST", "GET"])
@login_required
def update_post():
    if request.method == "POST":
        return controllers.post.update_post()
    

@post_router.route('/report_post', methods=['POST','GET'])
@login_required
def report_post():
    if request.method == 'POST':
        return controllers.post.report_post()
    id = request.args.get("id")
    return render_template('report_post.html',id = id)


@post_router.route('/create_post',methods=["POST", "GET"])
@login_required
def create_post():
    if request.method == "POST":
        return controllers.post.create_post()
    return render_template("post/create_post.html")

@post_router.route('/post_detail',methods=["GET"])
@login_required
def post_detail():
    return controllers.post.post_detail(request.args.get("id"))

@post_router.route('/search_post',methods=["POST", "GET"]) 
# @login_required
def search_post():
    if request.method == "POST":
        return controllers.post.search_post()
    return render_template("post/searchPost.html")

@post_router.route("/post/<int:post_id>")
@login_required
def post(post_id):
    return controllers.post.post(post_id)

@post_router.route("/newsfeed")
@login_required
def newfeed():
    return controllers.post.newsfeed()

@post_router.route("/reportedPosts")
@admin_required
def reportedPosts():
    return controllers.post.reported_Posts()

@post_router.route('/delete_report',methods=["POST", "GET"])
@admin_required
def delete_report():
    if request.method == "POST":
        return controllers.post.delete_report()