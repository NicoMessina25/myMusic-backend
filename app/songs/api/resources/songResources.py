from flask import request, Blueprint
from flask_restful import Api, Resource
from ....common.custom_response import CustomResponse
from sqlalchemy import func

from ..schemas import SongSchema
from ...models import Song, Artist
from ....common.error_handling import ObjectNotFound
from ....common.utils import retrieve_response_data
from ....auth.authManager import authenticate_user
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError

songs_bp = Blueprint('songs_bp', __name__)

song_schema = SongSchema()

api = Api(songs_bp)

def update_songs_artists(song_dict, song):
    for artist_dict in song_dict['artists']:
                artist = Artist.get_by_id(artist_dict["artistId"])
                
                if artist is None:                
                    song.artists.append(Artist(artist_dict['name']))
                else:
                    song.artists.append(artist)

class SongListResource(Resource):
    def get(self):
        resp = CustomResponse(success=True)
        try:
            authenticate_user()
            limit = request.args.get('limit', default=50, type=int)
            name_filter = request.args.get('filter', default='', type=str)
            
            query = Song.query
            if name_filter:
                query = query.filter(func.lower(Song.name).ilike(f"%{name_filter.lower()}%"))
            songs = query.limit(limit).all()
        except (InvalidSignatureError,ExpiredSignatureError) as err:
            print(err)
            resp.success = False
            resp.message = "Credenciales inválidas"
            return resp.to_server_response(), 401
        except Exception as err:
            print(err)
            resp.success = False
            resp.message = "No se pudieron obtener las canciones"
            return resp.to_server_response(), 404
        
        resp.data = song_schema.dump(songs, many=True)
        return resp.to_server_response()
    
    def post(self):
        try:
            song_dict = song_schema.load(retrieve_response_data(request))
            song = Song(title=song_dict['title'],
                        length=song_dict['length'],
                        releaseDate=song_dict['releaseDate']
            )
            update_songs_artists(song_dict, song)
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
            update_songs_artists(song_dict, song)
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