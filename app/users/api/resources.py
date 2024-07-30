from flask import request, Blueprint
from flask_restful import Api, Resource
from ...common.custom_response import CustomResponse
from sqlalchemy import func

from .schemas import UserSchema
from ..models import User
from app.profiles.models import EProfile
from ...common.error_handling import ObjectNotFound
from ...common.utils import retrieve_response_data
from ...auth.authManager import authenticate_user
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError

user_bp = Blueprint('user_bp', __name__)

user_schema = UserSchema()

api = Api(user_bp)

class UserListResource(Resource):
    def get(self):
        resp = CustomResponse(success=False)
        authenticate_user([EProfile.ADMIN])
        limit = request.args.get('limit', default=50, type=int)
        username_filter = request.args.get('filter', default='', type=str)
        
        query = User.query
        if username_filter:
            query = query.filter(func.lower(User.username).ilike(f"%{username_filter.lower()}%"))
        users = query.limit(limit).all()
        
        resp.data = user_schema.dump(users, many=True)
        resp.success = True
        return resp.to_server_response()
    
    def post(self):
        try:
            authenticate_user([EProfile.ADMIN])
            resp = CustomResponse(success=True)
            
            user_dict = user_schema.load(retrieve_response_data(request))        
            username = user_dict['username']

            if User.get_user_by_username(username):
                resp.success = False
                resp.message = "Ya existe un usuario con ese nombre"
                return resp.to_server_response(), 200
            
            if User.query.filter_by(email=user_dict["email"]).first():
                resp.success = False
                resp.message = "Ya existe un usuario con ese email"
                return resp.to_server_response(), 200

            user = User(
                username=username,
                email=user_dict['email'],
                password=user_dict['password'],
                profileId=user_dict['profile']["profileId"]
            )
            
            user.save()
            resp.message = "Usuario creado correctamente"
            return resp.to_server_response(), 201
        except PermissionError as err:
            resp.message = err            
            return resp.to_server_response(), 401
        except Exception as err:
            print(err)
            return resp, 405
        
    def put(self):
        resp = CustomResponse(success=True)
        user_dict = user_schema.load(retrieve_response_data(request))
        try:            
            authenticate_user([EProfile.ADMIN])
            user = User.get_by_id(user_dict["userId"])
            user.username = user_dict["username"]
            
            if "password" in user_dict:
                password = user_dict["password"].strip()
                if password != "":
                    user.set_password(password)
                
            user.email = user_dict["email"]
            user.profileId = user_dict["profile"]["profileId"]
            
            user.update()
            resp.data = user_schema.dump(user)
            return resp.to_server_response(), 200
        except PermissionError as err:
            resp.message = err            
            return resp.to_server_response(), 401
        except Exception as err:
            print(err)
            resp.success = False
            return resp.to_server_response(), 405
    
class UserResource(Resource):
    def get(self, user_id):
        try:
            authenticate_user([EProfile.ADMIN])
            resp = CustomResponse(success=True)
            user = User.get_by_id(user_id)
            if user is None:
                resp.message = 'El usuario no existe'
                resp.success = False
                
            resp.data = user_schema.dump(user)
            return resp.to_server_response(), 200
        except PermissionError as err:
            resp.message = err            
            return resp.to_server_response(), 401
        except Exception as err:
                print(err)
                return resp.to_server_response(), 405
    
    def delete(self, user_id):
        resp = CustomResponse(success=True)
        try:
            authenticate_user([EProfile.ADMIN])
            user = User.get_by_id(user_id)
            user.delete()
        except PermissionError as err:
            resp.success = False
            resp.message = err            
            return resp.to_server_response(), 401
        except Exception as err:
            print(err)
            return resp.to_server_response(), 405
        return resp.to_server_response(), 200

api.add_resource(UserListResource, '/api/users/', endpoint='user_list_resource')
api.add_resource(UserResource, '/api/users/<int:user_id>', endpoint='user_resource')