import random
from models.user import UserRole, User
from models.model import db
from flask import Flask,redirect,url_for,json,render_template,request,session,flash
from flask_mail import Message
from controllers.mail_service import mail


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
        session['user'] = query.username
        session['id'] = query.id
        
        return redirect(url_for("home"))
    flash("Your account doesn't exist","info")
    return render_template("login.html")


def logout():
    session.pop('user',None)
    return redirect(url_for('user_router.home'))

def forgot_password(email):
    # kiem tra email
    user = db.session.execute(db.select(User).where(User.email == email)).first()
    if user != None:
            # gen new password
            new_password = gen_new_password()
            # update password
            user[0].password = new_password
            # luu password moi vao database
            db.session.commit()
            #send email
            msg = Message('Your new password is: ' + new_password, sender = 'sweethomehola@outlook.com', recipients = [email])
            mail.send(msg)

            #thong bao toi front end
            flash("New password has been sent to your email.","info")
            return render_template("login.html")
    else:
        flash("Wrong email!","info")
        return render_template("forgot_password.html")

def register():
    # kiem tra du lieu
    user = User.query.filter(User.username == request.form["username"]).first()
    if user:
        flash("Username already exists!","info")
        return render_template("register.html")
    user = User.query.filter(User.email == request.form["email"]).first()
    if user:
        flash("Email already exists!","info")
        return render_template("register.html")
    # add vao database
    user = User(
        username=request.form["username"],
        password=request.form["password"],
        email=request.form["email"],
        banned=False)
    db.session.add(user)
    db.session.commit()
    # chuyen huong ve trang login
    return redirect(url_for('user_router.login'))

def register_seller(username, password, address, email):
    # nhan du lieu tu form
    
    # kiem tra du lieu
    # add thong bao cho admin (de approved = false)
    # khi admin approve thi gui email cho seller (xu li o admin)
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

def edit_profile():
    user = User.query.filter(User.id == session['id']).first()
    checkUsername = User.query.filter(User.username == request.form["username"]).first()
    if checkUsername:
        flash("Username already exists!","info")
        return render_template("editProfile.html",username=user.username,email=user.email)
    user.username = request.form["username"]
    checkEmail = User.query.filter(User.email == request.form["email"]).first()
    if checkEmail:
        flash("Email already exists!","info")
        return render_template("editProfile.html",username=user.username,email=user.email)
    user.email = request.form["email"]
    return render_template("editProfile.html",username=user.username,email=user.email)