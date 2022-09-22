from models.model import db

class UserRole():
    MEMBER = "MEMBER"
    ADMIN = "ADMIN"
    BANNED = "BANNED"
    SELLER = "SELLER"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    banned = db.Column(db.Boolean, nullable=True, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)


class HomeOwner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    house_address = db.Column(db.String(120), nullable=False)
    approved = db.Column(db.Boolean, nullable=True, default=False)
    banned = db.Column(db.Boolean, nullable=True, default=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
