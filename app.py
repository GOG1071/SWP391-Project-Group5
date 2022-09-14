from flask import Flask, render_template, request
from dotenv import load_dotenv
from models.model import db
from pathlib import Path
import os

from routers.user import user_router

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.getenv('SECRET_KEY')

db.init_app(app)
db.create_all(app=app)

app.register_blueprint(user_router, url_prefix="/user")

app.run("0.0.0.0", port=os.environ["port"], debug=True)