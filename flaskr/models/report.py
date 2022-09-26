from models.model import db

class ReportPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)
    reason = db.Column(db.String(1000), nullable = False)

class ReportHome(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)
    reason = db.Column(db.String(1000), nullable = False)

class ReportUser(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)
    reason = db.Column(db.String(1000), nullable = False)
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

