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
import cloudinary
from flask_wtf.csrf import CSRFProtect


#load environment variables
env_path = Path('.') / '../.env'
load_dotenv(dotenv_path=env_path)

#start
app = Flask(__name__)
#cloudinary config
cloudinary.config( 
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.getenv('CLOUDINARY_API_KEY'), 
  api_secret = os.getenv('CLOUDINARY_API_SECRET') 
)
#database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True

app.secret_key = os.getenv('SECRET_KEY')

#start database
db.init_app(app)
db.create_all(app=app)

#start mail service
mail = Mail(app)

#start csrf
csrf = CSRFProtect(app)
csrf.init_app(app)

#register blueprint
app.register_blueprint(user_router, url_prefix="/user")
app.register_blueprint(post_router, url_prefix="/post")
app.register_blueprint(home_router,url_prefix="/home")

@app.route("/")
def index():
    return render_template("home.html", stringName = "You are not logged in",isLogin = False)
  
@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["HTTP-HEADER"] = "VALUE"
    return response

# @app.route("/test")
# def home():
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5)
#     return render_template('postTest.html', posts=posts)

app.run("0.0.0.0", port=os.environ["port"], debug=True)