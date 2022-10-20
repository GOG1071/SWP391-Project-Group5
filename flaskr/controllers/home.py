from datetime import datetime
from email import message
from models.report import ReportHome
from models.home import Home
from models.home import RoomDetail
from models.home import RoomImage
from models.model import db
from flask import Flask,redirect,url_for,json,render_template,request,session,flash
from flask_mail import Message
from controllers.mail_service import mail
import cloudinary.uploader 


def add_home():
    name = request.form['name']
    address = request.form["address"]
    des = request.form["des"]
    num_room = request.form["num_room"]
    room_not = request.form["room_no"]
    user_id = session["id"]
    timestamp = datetime.now()
    home = Home(name = name, address = address,description = des, total_rooms = num_room, available_rooms = room_not,timestamp = timestamp,user_id = user_id)
    db.session.add(home)
    db.session.commit()
    return redirect( url_for('home_router.load_home'))


def load_home():
    user_id = session['id']
    list_home = Home.query.filter_by(user_id = user_id)
    return render_template("home/load_home.html",list_home = list_home)

def load_room():
    home_id = request.args.get("home_id")
    list_room = RoomDetail.query.filter_by(home_id = home_id)
    list_room_img = []
    for i in list_room:
        room_img = RoomImage.query.filter_by(room_id = i.id)
        list_room_img+=room_img
    if list_room_img:
        return render_template("home/load_room.html",list_room = list_room,list_room_img = list_room_img,home_id = home_id)
        
    return render_template("home/load_room.html",list_room = list_room,home_id = home_id)


def add_room():
    room_type = request.form['type_room']
    home_id = request.form['home_id']
    des = request.form['des']
    price = request.form['price']
    amount = request.form['num_room']
    image_link =  request.files.getlist('img')
    
    room_detail = RoomDetail(home_id = home_id,room_type = room_type,amount = amount,price = price,description = des)
    db.session.add(room_detail)
    db.session.commit()

    room_all = RoomDetail.query.all()
    room = room_all[len(room_all)-1]

    file_path = None
    list_file_path = []
    # lấy 1 list link img rồi đẩy hết lên cloudinary rồi lấy link sau khi đẩy add vào list_file_path
    if image_link:
        for img in image_link:
            
                response = cloudinary.uploader.upload(img)
                file_path = response['secure_url']
                list_file_path.append(file_path)
    
    for file in list_file_path:
        room_img = RoomImage(room_id = room.id, image_link = file)
        db.session.add(room_img)
        db.session.commit() 
    return redirect( url_for('home_router.load_room',home_id = home_id))

def info(id):
    home = Home.query.filter_by(id = id).first()
    return render_template("home/home_info.html",home = home)

def report_home(id, reason, reporter_id):
    home = Home.query.filter_by(id = id).first()
    home.reported = True
    report_home = ReportHome(\
        home_id = id, \
        user_id = reporter_id, \
        timestamp = datetime.now(), \
        reason = reason)
    db.session.add(report_home)
    db.session.commit()
    return redirect(url_for('home_router.info', message = "Reported successfully", id = id))

def list_home():
    list_home = Home.query.all()
    return render_template("home/list_home.html",list_home = list_home)
