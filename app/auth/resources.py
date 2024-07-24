# app/auth/resources.py

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app import db
from app.users.models import User
from ..users.schemas import UserSchema
from ..common.utils import retrieve_response_data
from ..common.custom_response import CustomResponse
from flask_jwt_extended import create_access_token, create_refresh_token

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

user_schema = UserSchema()

class Register(Resource):
    def post(self):
        resp = CustomResponse(success=True)
            
        user_dict = user_schema.load(retrieve_response_data(request))        
        username = user_dict['username']

        if User.query.filter_by(username=username).first():
            resp.success = False
            resp.message = "User already exists"
            return resp.to_server_response(), 400

        user = User(
            username=username,
            email=user_dict['email'],
            password=user_dict['password']
        )
        
        user.save()
        resp.message = "User created successfully"
        return resp.to_server_response(), 201

class Login(Resource):
    def post(self):
        try:
            resp = CustomResponse(success=True)
            
            user_dict = user_schema.load(retrieve_response_data(request))     
            username = user_dict['username']
            password = user_dict['password']

            user = User.query.filter_by(username=username).first()
            if not user:
                resp.success = False
                resp.message = "User already exists"
                return resp.to_server_response(), 400
            
            if user.check_password(password):
                access_token = create_access_token(identity=username)
                refresh_token = create_refresh_token(identity=username)
                resp.data = {'access_token': access_token, 'refresh_token': refresh_token, 'user':user.to_dict()}
                return resp.to_server_response(), 200
            resp.message = "Invalid credentials"
            resp.success = False
            return resp.to_server_response(), 401
        except Exception as err:
            resp.message = err
            resp.success = False
            return resp.to_server_response(),401

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')