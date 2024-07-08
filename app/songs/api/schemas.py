from marshmallow import fields

from app.ext import ma


class SongSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    length = fields.Integer()
    year = fields.Integer()
    director = fields.String()
    actors = fields.Nested('UserSchema', many=True)


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()