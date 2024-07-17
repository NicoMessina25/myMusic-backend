from flask import request, Blueprint
from flask_restful import Api, Resource
from ...common.custom_response import CustomResponse
import sqlite3

from .schemas import SongSchema
from ..models import Song, Artist
from ...common.error_handling import ObjectNotFound
from ...common.utils import retrieve_response_data

songs_bp = Blueprint('songs_bp', __name__)

song_schema = SongSchema()

api = Api(songs_bp)

class SongListResource(Resource):
    def get(self):
        resp = CustomResponse(success=True)
        try:
            songs = Song.get_all()
        except Exception as err:
            print(err)
            resp.success = False
            resp.message = "No se pudieron obtener las canciones"
            return resp, 405
        
        resp.data = song_schema.dump(songs, many=True)
        return resp.to_server_response()
    
    def post(self):
        try:
            song_dict = song_schema.load(retrieve_response_data(request))
            song = Song(title=song_dict['title'],
                        length=song_dict['length'],
                        releaseDate=song_dict['releaseDate']
            )
            for artist in song_dict['artists']:
                song.artists.append(Artist(artist['name']))
            song.save()
            resp = song_schema.dump(song)
            return resp, 201
        except Exception as err:
            print(err)
            return resp, 405
        
    def put(self):
        song_dict = song_schema.load(retrieve_response_data(request))
        try:
            song = Song.get_by_id(song_dict["songId"])
            song.title = song_dict["title"]
            song.releaseDate = song_dict["releaseDate"]
            song.length = song_dict["length"]
            
            song.artists.clear()
            for artist in song_dict['artists']:
                song.artists.append(Artist(artist['name']))
            song.update()
            resp = song_schema.dump(song)
            return resp, 200
        except Exception as err:
            print(err)
            return resp, 405
    
class SongResource(Resource):
    def get(self, song_id):
        try:
            resp = CustomResponse(success=True)
            song = Song.get_by_id(song_id)
            if song is None:
                resp.message = 'La canción no existe'
                resp.success = False
                
            resp.data = song_schema.dump(song)
            return resp.to_server_response(), 200
        except Exception as err:
                print(err)
                return resp.to_server_response(), 405
    
    def delete(self, song_id):
        resp = CustomResponse(success=True)
        try:
            song = Song.get_by_id(song_id)
            song.delete()
        except Exception as err:
            print(err)
            return resp, 405
        return resp.to_server_response(), 200

api.add_resource(SongListResource, '/api/songs/', endpoint='song_list_resource')
api.add_resource(SongResource, '/api/songs/<int:song_id>', endpoint='song_resource')