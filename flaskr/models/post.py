from models.model import db
from models.user import User

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(1000), unique=False, nullable=False)
    image = db.Column(db.String(200), unique=False, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)