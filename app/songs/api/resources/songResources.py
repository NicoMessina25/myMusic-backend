from flask import request, Blueprint
from flask_restful import Api, Resource
from ....common.custom_response import CustomResponse
from sqlalchemy import func,or_
from ..schemas import SongSchema
from ...models import Song, Artist
from ....common.error_handling import ObjectNotFound
from ....common.utils import retrieve_response_data
from ....auth.authManager import authenticate_user
from app.profiles.models import EProfile

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
            limit = request.args.get('limit', default=50, type=int)
            offset = request.args.get('offSet', default=0, type=int)
            name_filter = request.args.get('filter', default='', type=str)
            
            query = Song.query
            if name_filter:
                name_filter = name_filter.strip()
                query = query.join(Song.artists).filter(
                    or_(
                        func.lower(Song.title).ilike(f"%{name_filter.lower()}%"),
                        func.lower(Artist.name).ilike(f"%{name_filter.lower()}%")
                    )
                )
            songs = query.order_by("title").offset(offset).limit(limit).all()
        except Exception as err:
            print(err)
            resp.success = False
            resp.message = "No se pudieron obtener las canciones"
            return resp.to_server_response(), 200
        
        resp.data = song_schema.dump(songs, many=True)
        return resp.to_server_response()
    
    def post(self):
        resp = CustomResponse(success=True)
        try:
            song_dict = song_schema.load(retrieve_response_data(request))
            song = Song(title=song_dict['title'],
                        length=song_dict['length'],
                        releaseDate=song_dict['releaseDate']
            )
            update_songs_artists(song_dict, song)
            song.save()
            resp.data = song_schema.dump(song)
            return resp.to_server_response(), 201
        except Exception as err:
            print(err)
            resp.data = str(err)
            resp.success = False
            return resp, 405
        
    def put(self):
        resp = CustomResponse(success=True)
        authenticate_user([EProfile.ADMINISTRATIVE,EProfile.ADMIN])
        song_dict = song_schema.load(retrieve_response_data(request))
        song = Song.get_by_id(song_dict["songId"])
        song.title = song_dict["title"]
        song.releaseDate = song_dict["releaseDate"]
        song.length = song_dict["length"]
        
        song.artists.clear()
        update_songs_artists(song_dict, song)
        song.update()
        resp.data = song_schema.dump(song)
        return resp.to_server_response(), 200
    
class SongResource(Resource):
    def get(self, song_id):
        authenticate_user([EProfile.ADMINISTRATIVE,EProfile.ADMIN])
        resp = CustomResponse(success=True)
        song = Song.get_by_id(song_id)
        if song is None:
            resp.message = 'La canción no existe'
            resp.success = False
            
        resp.data = song_schema.dump(song)
        return resp.to_server_response(), 200
    
    def delete(self, song_id):
        authenticate_user([EProfile.ADMINISTRATIVE,EProfile.ADMIN])
        resp = CustomResponse(success=True)
        song = Song.get_by_id(song_id)
        song.delete()
        return resp.to_server_response(), 200

api.add_resource(SongListResource, '/api/songs/', endpoint='song_list_resource')
api.add_resource(SongResource, '/api/songs/<int:song_id>', endpoint='song_resource')