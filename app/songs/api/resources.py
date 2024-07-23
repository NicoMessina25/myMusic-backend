from flask import request, Blueprint
from flask_restful import Api, Resource
import sqlite3

from .schemas import SongSchema
from app.songs.models import Song
from app.users.models import User
from app.common.error_handling import ObjectNotFound

songs_bp = Blueprint('songs_bp', __name__)

song_schema = SongSchema()
api = Api(songs_bp)

class SongListResource(Resource):
    def get(self):
        try:
            songs = Song.get_all()
            result = song_schema.dump(songs, many=True)
            return result
        except Exception as err:
            print(err)
            return {'msg': 'Error retrieving songs'}, 405
    
    def post(self):
        data = request.get_json()
        song_dict = song_schema.load(data)
        try:
            song = Song(
                title=song_dict['title'],
                length=song_dict['length'],
                year=song_dict['year'],
                director=song_dict['director']
            )
            for actor in song_dict['actors']:
                song.actors.append(User(name=actor['name']))
            song.save()
            resp = song_schema.dump(song)
            return resp, 201
        except Exception as err:
            print(err)
            return {'msg': 'Error creating song'}, 405
    
class SongResource(Resource):
    def get(self, song_id):
        song = Song.get_by_id(song_id)
        if song is None:
            raise ObjectNotFound('La canción no existe')
        resp = song_schema.dump(song)
        return resp

api.add_resource(SongListResource, '/api/songs/', endpoint='song_list_resource')
api.add_resource(SongResource, '/api/songs/<int:song_id>', endpoint='song_resource')
