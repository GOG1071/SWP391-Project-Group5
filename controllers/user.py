
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
        return redirect(url_for("home"))
        
    flash("Your account doesn't exist","info")
    return render_template("login.html")

def logout():
    pass

def forgot_password():
    pass

def register_seller():
    pass