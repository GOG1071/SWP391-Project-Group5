from models.user import UserRole, User
from models.model import db


def register():
    pass

def login():
    # session.push()
    # luu vao session object cua user hoac homeowner hoac admin
    db.Query.filter_by(User.username == username).first()
    # 'user'
    pass

def logout():
    pass

def forgot_password():
    # nhan email tu form
    # kiem tra email
    # gen 1 password moi
    # luu password moi vao database
    # gui email cho user / goi toi stmp server
    pass

def register_seller():
    # nhan du lieu tu form
    # kiem tra du lieu
    # add thong bao cho admin
    # khi admin approve thi gui email cho seller
    pass