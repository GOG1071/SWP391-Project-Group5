
from models.user import UserRole, User
from models.model import db
from flask import Flask,redirect,url_for,json,render_template,request,session,flash

def register():
    pass

def login():

    user_name = request.form["user"]
    pass_word = request.form["pass"]

    query = User.query.filter(User.username == user_name , User.password == pass_word).first()
    if query:
        session['user'] = query.username
        return render_template("home.html")
    flash("Your account doesn't exist","info")
    render_template("login.html")


def logout():
    pass

def forgot_password():
    # nhan email tu form
    # kiem tra email
    # gen 1 password moi
    # luu password moi vao database
    # gui email cho user / goi toi stmp server
    pass

def register_seller():
    # nhan du lieu tu form
    # kiem tra du lieu
    # add thong bao cho admin
    # khi admin approve thi gui email cho seller
    pass