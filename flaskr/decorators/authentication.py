from functools import wraps
from flask import request, jsonify, session
from models.user import UserRole

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" in session:
            if session['banned'] == False:
                return f(*args, **kwargs)
            else:
                return jsonify(error="You are banned"), 403
        else:
            return jsonify(error="Please login!"), 401
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        login_required(f)
        if session["role"] != UserRole.ADMIN:
            return jsonify(error="Admin access required"), 403
        return f(*args, **kwargs)
    return decorated_function

def seller_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        login_required(f)
        if session["role"] != UserRole.SELLER:
            return jsonify(error="Seller access required"), 403
        return f(*args, **kwargs)
    return decorated_function


