from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.users.models import User

def authenticate_user():
    verify_jwt_in_request()
    return User.get_user_by_username(get_jwt_identity())