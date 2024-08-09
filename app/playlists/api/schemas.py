from marshmallow import fields
from app.ext import ma
from app.songs.api.schemas import SongSchema

class PlaylistSchema(ma.Schema):
    playlistId = fields.Integer()
    name = fields.String()
    description = fields.String()
    userId = fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    songs = fields.Nested('SongSchema', many=True)
