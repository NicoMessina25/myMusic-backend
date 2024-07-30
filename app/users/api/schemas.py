from marshmallow import fields

from app.ext import ma
from app.profiles.api.schemas import ProfileSchema


class UserSchema(ma.Schema):
    userId = fields.Integer()
    username = fields.String()
    password = fields.String(load_only=True)
    email = fields.String()
    profile = fields.Nested(ProfileSchema)