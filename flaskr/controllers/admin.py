import random
import string

from models.user import Bookmark ,RoomRequest
from models.user import UserRole, User, HomeOwnerRequest
from models.model import db
from flask import Flask,redirect,url_for,json,render_template,request,session,flash
from flask_mail import Message
from controllers.mail_service import mail
from models.user import HomeOwnerRequest,User
from datetime import datetime

def view_request_register():

    request_register = HomeOwnerRequest.query.all()
    return render_template("admin/view_request_register.html",request_register = request_register)

def allow_access():
    id = request.args.get("id")
    request_register = HomeOwnerRequest.query.filter_by(id = id).first()
    request_register.status = True
    db.session.commit()
    return redirect(url_for('admin_router.view_request_register'))
