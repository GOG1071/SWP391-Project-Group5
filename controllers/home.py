from datetime import datetime
from email import message
from models.report import ReportHome
from models.home import Home
from models.home import RoomDetail
from models.home import RoomImage
from models.user import User, Bookmark, RoomRequest
from models.model import db
from flask import Flask, redirect, url_for, json, render_template, request, session, flash
from flask_mail import Message
from controllers.mail_service import mail
import cloudinary.uploader


def add_home():
    name = request.form['home_name']
    address = request.form["address"]
    des = request.form["des"]
    num_room = request.form["num_room"]
    room_not = request.form["room_no"]
    user_id = session["id"]
    timestamp = datetime.now()
    home = Home(name=name, address=address, description=des, total_rooms=num_room,
                available_rooms=room_not, timestamp=timestamp, user_id=user_id)
    db.session.add(home)
    db.session.commit()
    if session.get('clear') != None:
        session.clear()
        return redirect(url_for('user_router.home'))
    return redirect(url_for('home_router.load_home'))


def load_home():
    user_id = session['id']
    list_home = Home.query.filter_by(user_id=user_id)
    return render_template("home/load_home.html", list_home=list_home)


def remove_home():
    home_id = request.args.get("home_id")
    home = Home.query.filter_by(id=home_id).first()
    if home:
        db.session.delete(home)
        db.session.commit()
    return redirect(url_for("home_router.load_home"))


def edit_home():
    if request.method == "GET":
        home_id = request.args.get("home_id")
        home = Home.query.filter_by(id=home_id).first()
        return render_template("home/edit_home.html", home=home, home_id=home_id)
    else:
        home_id = request.form.get("home_id")
        home = Home.query.filter_by(id=home_id).first()
        if home:
            home.name = request.form['home_name'] if request.form['home_name'] else home.name
            home.address = request.form["address"] if request.form["address"] else home.address
            home.description = request.form["des"] if request.form["des"] else home.description
            home.total_rooms = request.form["num_room"] if request.form["num_room"] else home.total_rooms
            home.available_rooms = request.form["room_no"] if request.form["room_no"] else home.available_rooms
            db.session.commit()
        return redirect(url_for("home_router.load_home"))


def load_room():
    home_id = request.args.get("home_id")
    list_room = RoomDetail.query.filter_by(home_id=home_id)
    home = Home.query.filter_by(id=home_id).first()
    list_room_img = []
    for i in list_room:
        room_img = RoomImage.query.filter_by(room_id=i.id)
        list_room_img += room_img
    if list_room_img:
        return render_template("home/load_room.html", list_room=list_room, list_room_img=list_room_img, home_id=home_id, total_room=home.total_rooms, room_home=list_room.count())
    return render_template("home/load_room.html", list_room=list_room, home_id=home_id, total_room=home.total_rooms, room_home=list_room.count())


def remove_room():
    room_id = request.args.get("room_id")
    room = RoomDetail.query.filter_by(id=room_id).first()
    home = Home.query.filter_by(id=room.home_id).first()
    if room:
        db.session.delete(room)
        db.session.commit()
    return redirect(url_for("home_router.load_room", home_id=home.id))


def add_room():
    room_type = request.form['type_room']
    home_id = request.form['home_id']
    des = request.form['des']
    price = request.form['price']
    amount = request.form['num_room']
    image_link = request.files.getlist('img')

    room_detail = RoomDetail(
        home_id=home_id, room_type=room_type, amount=amount, price=price, description=des)
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
        room_img = RoomImage(room_id=room.id, image_link=file)
        db.session.add(room_img)
        db.session.commit()
    return redirect(url_for('home_router.load_room', home_id=home_id))


def info(id):
    home = Home.query.filter_by(id=id).first()
    user = User.query.filter_by(id=home.user_id).first()
    list_room = RoomDetail.query.filter_by(home_id=id).all()
    for room in list_room:
        room.img = RoomImage.query.filter_by(room_id=room.id).all()
    return render_template("home/home_info.html", home=home, owner=user.username, list_room=list_room)


def report(home_id):
    home = Home.query.filter(Home.id == home_id).first()
    if home:
        user = User.query.filter(User.id == home.user_id).first()
        if user:
            return render_template("home/report.html", home_id=home_id)
        else:
            render_template("home/report.html", message="Home not found")
    else:
        return render_template("home/report.html", message="Home not found")


def do_report(reported_home_id, reporter_id, reason):
    home = Home.query.filter(Home.id == reported_home_id).first()
    if home:
        report = ReportHome(
            home_id=reported_home_id,
            user_id=reporter_id,
            timestamp=datetime.now(),
            reason=reason)
        db.session.add(report)
        db.session.commit()
        return render_template("home/report.html", message="Report successfully!")
    else:
        return render_template("home/report.html", message="Home not found")


def list_home():
    list_home = Home.query.all()
    return render_template("home/list_home.html", list_home=list_home)


def search(home_name):
    list_home = Home.query.filter(Home.name.like("%"+home_name+"%"))
    return render_template("home/search_home.html", list_home=list_home)


def home_detail(home_id):
    user = User.query.filter_by(username=session['username']).first()
    home = Home.query.filter_by(id=home_id).first()
    if home.user_id == user.id:
        username = user.username
    else:
        username = User.query.filter_by(id=home.user_id).first().username
    list_room = RoomDetail.query.filter_by(home_id=home_id).all()
    for room in list_room:
        room.image_link = RoomImage.query.filter_by(room_id=room.id).all()
    return render_template("home/home_detail.html", list_room=list_room, home_id=home_id, username=username)


def compare(home1, home2):
    home1 = Home.query.filter_by(id=home1).first()
    home2 = Home.query.filter_by(id=home2).first()
    list_room1 = RoomDetail.query.filter_by(home_id=home1.id).all()
    list_room2 = RoomDetail.query.filter_by(home_id=home2.id).all()
    for room in list_room1:
        room.image_link = RoomImage.query.filter_by(room_id=room.id).all()
    for room in list_room2:
        room.image_link = RoomImage.query.filter_by(room_id=room.id).all()
    return render_template("home/compare.html", home1=home1, home2=home2, list_room1=list_room1, list_room2=list_room2)


def home_compare(home_id):
    home_list = Home.query.all()
    for home in home_list:
        if home.id == int(home_id):
            home_list.remove(home)
    return render_template("home/home_compare.html", home_list=home_list, origin=home_id)


def new_room_request(room_id):
    room_id = request.form.get("id")
    name = request.form['name']
    phone = request.form['phone']
    timeVisit = request.form['timeVisit']
    facebook = request.form['facebook']
    user_id = session["id"]
    timestamp = datetime.now()
    room = RoomDetail.query.filter_by(id=room_id).first()
    owner = User.query.filter_by(id=room.home.user_id).first()
    room_reqest = RoomRequest(
        user_id=user_id, timestamp=timestamp, room_id=room_id, Seller_id=owner.id, name=name, phone=phone, facebook=facebook, content=timeVisit, readed=0)
    db.session.add(room_reqest)
    db.session.commit()
    return render_template("home/roomRequest.html", done=True, name=name, phone=phone, timeVisit=timeVisit, facebook=facebook, room=room)


def roomRequests():
    requests = RoomRequest.query.filter_by(Seller_id=session["id"]).all()
    user = User.query.all()
    return render_template("home/roomRequests.html", requests=requests, user=user)


def roomRequestDetail(id):
    request = RoomRequest.query.filter_by(id=id).first()
    user = User.query.filter_by(id=request.user_id).first()
    room = RoomDetail.query.filter_by(id=request.room_id).first()
    request.readed = 1
    session['noti'] = RoomRequest.query.filter_by(
        Seller_id=session['id'], readed=0).count()
    db.session.commit()
    return render_template("home/roomRequestDetail.html", request=request, user=user, room=room)


def refuseRoomRequest():
    requset_id = request.form.get("id")
    roomRequestDetail = RoomRequest.query.filter_by(id=requset_id).first()
    customer = User.query.filter_by(id=roomRequestDetail.user_id).first()
    homeOnwer = User.query.filter_by(id=roomRequestDetail.Seller_id).first()
    email = customer.email

    if roomRequestDetail:

        msg = Message('Your room request has been refused',
                      sender='sweethomehola@outlook.com', recipients=[email])
        msg.body = "Home owner has been refuse your room request, please contact to home owner for more information \r\n Home owner email: " + \
            homeOnwer.email + "\r\n Thank you for using our service"
        mail.send(msg)

        db.session.delete(roomRequestDetail)
        db.session.commit()

        requests = RoomRequest.query.filter_by(Seller_id=session["id"]).all()
        users = User.query.all()
        return render_template("home/roomRequests.html", requests=requests, user=users)
    requests = RoomRequest.query.filter_by(Seller_id=session["id"]).all()
    users = User.query.all()
    return render_template("home/roomRequests.html", requests=requests, user=users)


def acceptRoomRequest():
    requset_id = request.form.get("id")
    roomRequestDetail = RoomRequest.query.filter_by(id=requset_id).first()
    customer = User.query.filter_by(id=roomRequestDetail.user_id).first()
    homeOnwer = User.query.filter_by(id=roomRequestDetail.Seller_id).first()
    email = customer.email

    if roomRequestDetail:

        msg = Message('Your room request has been accpetd',
                      sender='sweethomehola@outlook.com', recipients=[email])
        msg.body = "Home owner has been accept your room request, please contact to home owner for more information \r\n Home owner email: " + \
            homeOnwer.email + "\r\n Thank you for using our service"
        mail.send(msg)

        db.session.delete(roomRequestDetail)
        db.session.commit()

        requests = RoomRequest.query.filter_by(Seller_id=session["id"]).all()
        users = User.query.all()
        return render_template("home/roomRequests.html", requests=requests, user=users)
    requests = RoomRequest.query.filter_by(Seller_id=session["id"]).all()
    users = User.query.all()
    return render_template("home/roomRequests.html", requests=requests, user=users)

def bookmark(id):
    user_id = session["id"]
    bookmark = Bookmark.query.filter_by(user_id=user_id, home_id =id).first()
    if not bookmark:
        bookmark = Bookmark(user_id=user_id, home_id=id)
        db.session.add(bookmark)
        db.session.commit()
        flash("Bookmark successfully", "bookmark")
        return redirect(url_for('home_router.list_home'))
    else:
        flash("You have bookmarked this home", "bookmark")
        return redirect(url_for('home_router.list_home'))

def unbookmark(id):
    user_id = session["id"]
    bookmark = Bookmark.query.filter_by(user_id=user_id, home_id =id).first()
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        flash("Unbookmark successfully", "bookmark")
        return redirect(url_for('home_router.list_home'))
    else:
        flash("You have not bookmarked this home", "bookmark")
        return redirect(url_for('home_router.list_home'))