from marshmallow import fields

from app.ext import ma


class UserSchema(ma.Schema):
    userId = fields.Integer()
    username = fields.String()
    password = fields.String()
    email = fields.String()