import controllers.user
import controllers.admin
from decorators.authentication import login_required
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