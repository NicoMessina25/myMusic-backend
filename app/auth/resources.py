# app/auth/resources.py

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app import db
from app.users.models import User
from flask_jwt_extended import create_access_token, create_refresh_token

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            return {'msg': 'User already exists'}, 400

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return {'msg': 'User created successfully'}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        return {'msg': 'Invalid credentials'}, 401

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')