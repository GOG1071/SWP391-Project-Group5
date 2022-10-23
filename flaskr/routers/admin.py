
import controllers.user
import controllers.admin
from decorators.authentication import login_required, admin_required
from flask import Blueprint, jsonify, request, render_template, session
from models.user import UserRole, User
from models.post import  Post

admin_router = Blueprint('admin_router',__name__)


@admin_router.route('/view_request_register',methods=['POST','GET'])
def view_request_register():
    return controllers.admin.view_request_register()

@admin_router.route('/allow_access',methods=["Post","get"])
def allow_access():
    return controllers.admin.allow_access()

@admin_router.route("/refuse_access",methods=['POST','GET'])
def refuse_access():
    return controllers.admin.refuse_access()

@admin_router.route("/reportedPosts")
def reportedPosts():
    return controllers.admin.reported_Posts()

@admin_router.route('/delete_report',methods=["POST", "GET"])
#@admin_required
def delete_report():
    if request.method == "POST":
        return controllers.admin.delete_report()
    
@admin_router.route('/accept_report',methods=["POST", "GET"])
#@admin_required
def accept_report():
    if request.method == "POST":
        return controllers.admin.accept_report()

@admin_router.route('/view_feedback', methods=["GET"])
@admin_required
def view_feedback():
    return controllers.admin.view_feedback()
