
from asyncio.windows_events import NULL
import random
from models.user import UserRole, User
from models.model import db
from flask import Flask,redirect,url_for,json,render_template,request,session,flash

def home():
    if "user" in session:
        user = session['user']
        return render_template("home.html", username = user, isLogin = True)
    else:
        return render_template("home.html", stringName = "you are not login", isLogin = False)
        
        
def login():

    user_name = request.form["user"]
    pass_word = request.form["pass"]

    query = User.query.filter(User.username == user_name , User.password == pass_word).first()
    if query:
        session['id'] = query.id
        session['user'] = query.username
        return redirect(url_for('user_router.home'))
    flash("Your account doesn't exist","info")
    return render_template("login.html")


def logout():
    session.pop('user',None)
    return redirect(url_for('user_router.home'))

def forgot_password():
    # nhan email tu form
    email = request.form["email"]
    # kiem tra email
    query = User.query.filter(User.email == email).first()
    if query:
            User.password = gen_new_password()
    # luu password moi vao database
            db.session.commit()
            flash("New password has been sent to your email.","info")
            render_template("login.html")
    flash("Wrong email!","info")
    render_template("forgot_password.html")
    # gen 1 password moi

    # gui email cho user / goi toi stmp server

def register_seller():
    # nhan du lieu tu form
    # kiem tra du lieu
    # add thong bao cho admin
    # khi admin approve thi gui email cho seller
    pass
def gen_new_password():

    number = '0123456789'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    passwd = ''
    for i in range(0,8,2):
        passwd += random.choice(number)
        passwd += random.choice(alpha)
    return passwd

def profile():
    user = User.query.filter(User.id == session['id']).first()
    username = user.username
    email = user.email
    return render_template("userProfile.html",username=username,email=email)
