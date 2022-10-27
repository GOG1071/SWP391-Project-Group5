import controllers.chat
from decorators.authentication import login_required
from flask import Blueprint, session

chat_router = Blueprint('chat_router', __name__)

@chat_router.route("/chat_all")
@login_required
def chat_all():
    return controllers.chat.chat_all(session['id'])

@chat_router.route("/message_user/<int:userid>")
@login_required
def message_user(userid):
    return controllers.chat.message_user(userid)
