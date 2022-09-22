from functools import wraps
from flask import request, jsonify, session
from models.user import UserRole

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user = session["user"]
            return f(*args, **kwargs)
        except:
            return jsonify(error="Please login"), 401
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["user"] == None:
            return jsonify(error="Please login"), 401
        if session["user"].role != UserRole.ADMIN:
            return jsonify(error="Admin access required"), 403
        return f(*args, **kwargs)
    return decorated_function

def seller_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["user"] == None:
            return jsonify(error="Please login"), 401
        if session["user"].role != UserRole.SELLER:
            return jsonify(error="Seller access required"), 403
        return f(*args, **kwargs)
    return decorated_function


