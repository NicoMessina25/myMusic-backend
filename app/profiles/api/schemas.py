from marshmallow import fields

from app.ext import ma


class ProfileSchema(ma.Schema):
    profileId = fields.Integer()
    name = fields.String()