from flask import current_app
from flask_mail import Mail
import os

current_app.config['MAIL_SERVER'] = 'smtp.office365.com'
current_app.config['MAIL_PORT'] = 587
current_app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
current_app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
current_app.config['MAIL_USE_TLS'] = True

mail = Mail(current_app)