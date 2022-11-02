from flask import Flask, render_template, request
from dotenv import load_dotenv
from models.model import db
from pathlib import Path
import os
from controllers.mail_service import mail
from flask_mail import Mail
from routers.user import user_router
from routers.post import post_router
from routers.home import home_router
from routers.admin import admin_router
from routers.chat import chat_router
import cloudinary
from flask_wtf.csrf import CSRFProtect
from exceptions.handle import error_router

# load environment variables
env_path = Path('.') / '../.env'
load_dotenv(dotenv_path=env_path)

# start
app = Flask(__name__)

# database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True

app.secret_key = os.getenv('SECRET_KEY')

print(os.environ)
