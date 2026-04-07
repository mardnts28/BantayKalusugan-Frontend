from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from functools import wraps
from flask import jsonify
from datetime import timedelta
from config import Config
from models import User

def generate_token(user_id):
    expires = timedelta(days=Config.JWT_EXPIRE_DAYS)
    return create_access_token(identity=str(user_id), expires_delta=expires)

def get_current_user():
    user_id = get_jwt_identity()
    return User.find_by_id(user_id)

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user = get_current_user()
            if not user or user.get('role') != 'admin':
                return jsonify({"message": "Admin access required"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
