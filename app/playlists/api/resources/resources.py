from flask import request, Blueprint
from flask_restful import Api, Resource
from ....common.custom_response import CustomResponse
from ...models import Playlist
from ....common.error_handling import ObjectNotFound
from ....common.utils import retrieve_response_data
from ....auth.authManager import authenticate_user
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
from ..schemas import PlaylistSchema, PlaylistSchemaWithSongs
from datetime import datetime, timezone
from sqlalchemy.orm import noload

playlist_bp = Blueprint('playlist_bp', __name__)
api = Api(playlist_bp)

playlist_schema = PlaylistSchema()

class PlaylistListResource(Resource):
    def get(self):
        resp = CustomResponse(success=True)
        user = authenticate_user()
        playlists = Playlist.query.options(noload(Playlist.songs)).filter_by(userId=user.userId).all()
        resp.data = playlist_schema.dump(playlists, many=True)
        return resp.to_server_response()

    def post(self):
        user = authenticate_user()
        resp = CustomResponse(success=True)
        playlist_dict = playlist_schema.load(retrieve_response_data(request))
        playlist_dict["userId"] = user.userId        
        print(playlist_dict)
        playlist = Playlist(name=playlist_dict["name"],
                            userId=playlist_dict["userId"],
                            description=playlist_dict["description"])
        playlist.save()
        resp.data = playlist_schema.dump(playlist)
        return resp.to_server_response(), 201
    
    def put(self):
        authenticate_user()
        resp = CustomResponse(success=True)
        playlist_dict = playlist_schema.load(retrieve_response_data(request))
        playlist = Playlist.get_by_id(playlist_dict["playlistId"])
        playlist.name = playlist_dict["name"]
        playlist.description = playlist_dict["description"]
        playlist.updated_at = datetime.now(timezone.utc)
        playlist.update()
        resp.data = playlist_schema.dump(playlist)
        return resp.to_server_response(), 200

class PlaylistResource(Resource):
    def get(self, playlistId):
        resp = CustomResponse(success=True)
        playlist = Playlist.get_by_id(playlistId)
        if playlist is None:
            resp.success = False
            resp.message = 'Playlist no encontrada'
            return resp.to_server_response(), 404
        resp.data = playlist_schema.dump(playlist)
        return resp.to_server_response()

    def delete(self, playlistId):
        authenticate_user()
        resp = CustomResponse(success=True)
        playlist = Playlist.get_by_id(playlistId)
        if playlist is None:
            resp.success = False
            resp.message = 'Playlist no encontrada'
            return resp.to_server_response(), 404
        playlist.delete()
        return resp.to_server_response(), 200

api.add_resource(PlaylistListResource, '/api/playlists/', endpoint='playlist_list_resource')
api.add_resource(PlaylistResource, '/api/playlists/<int:playlistId>', endpoint='playlist_resource')
