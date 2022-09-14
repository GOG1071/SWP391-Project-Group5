from models.model import db

class UserRole():
    MEMBER = "MEMBER"
    ADMIN = "ADMIN"
    BANNED = "BANNED"
    SELLER = "SELLER"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)

