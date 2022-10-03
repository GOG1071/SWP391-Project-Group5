from models.model import db

class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    ad_detail = db.relationship("AdvertisementDetail")

class AdvertisementDetail(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    advertisement_id = db.Column(db.Integer, db.ForeignKey('advertisement.id'), nullable = False)
    price = db.Column(db.Float, nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)
    description = db.Column(db.String(1000), nullable = False)
    image_link = db.Column(db.String(200), unique = False, nullable = False)