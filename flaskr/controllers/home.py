from datetime import datetime
from models.home import Home
from models.home import RoomDetail
from models.home import RoomImage
from models.model import db
from flask import Flask,redirect,url_for,json,render_template,request,session,flash
from flask_mail import Message
from controllers.mail_service import mail
import cloudinary.uploader 


def add_home():
    address = request.form["address"]
    des = request.form["des"]
    num_room = request.form["num_room"]
    room_not = request.form["room_no"]
    user_id = session["id"]
    timestamp = datetime.now()
    home = Home(address = address,description = des, total_rooms = num_room, available_rooms = room_not,timestamp = timestamp,user_id = user_id)
    db.session.add(home)
    db.session.commit()
    return render_template("add_home_for_owner.html")
