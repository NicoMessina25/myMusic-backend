from marshmallow import fields

from app.ext import ma


class SongSchema(ma.Schema):
    songId = fields.Integer()
    title = fields.String()
    length = fields.Integer()
    releaseDate = fields.Date(allow_none=True)
    artists = fields.Nested('ArtistSchema', many=True)


class ArtistSchema(ma.Schema):
    artistId = fields.Integer()
    name = fields.String()
    
    