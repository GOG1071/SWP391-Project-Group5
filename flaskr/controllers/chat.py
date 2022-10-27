from models.user import User
from models.chat import Chat
from flask import render_template
from flask_mail import Message


def chat_all(userid):
    #get all the user with userid
    user = User.query.filter(User.id != userid).all()
    return render_template("chat/chat_all.html", list_user = user)

def message_user(userid):
    #get all the user with userid
    user = User.query.filter(User.id == userid).first()
    return render_template("chat/message_user.html", user = user)
def get_message(sender_id,receiver_id):
    list_messages = Message.query.filter((Message.sender_id == sender_id) & (Message.receiver_id == receiver_id)).all()
    return render_template("chat/message.html",messages=list_messages)
