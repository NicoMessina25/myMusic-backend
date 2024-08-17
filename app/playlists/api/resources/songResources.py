from flask import request, Blueprint
from flask_restful import Api, Resource
from app.playlists.models import Playlist
from app.songs.models import Song
from ....common.custom_response import CustomResponse
from ....auth.authManager import authenticate_user
from ....common.utils import retrieve_response_data

playlist_songs_bp = Blueprint('playlist_songs_bp', __name__)
api = Api(playlist_songs_bp)

class PlaylistAddSongResource(Resource):
    def post(self):
        authenticate_user()
        playlist_song = retrieve_response_data(request)
        playlist = Playlist.get_by_id(playlist_song["playlistId"])
        
        resp = CustomResponse(success=True)
        if playlist is None:
            resp.success = False
            resp.message = "Playlist inexistente"
            return resp.to_server_response(), 200
        
        song = Song.get_by_id(playlist_song["songId"])
        playlist.songs.append(song)
        try:
            playlist.update()
        except Exception as err:
            print(err)
            resp.success = False
            resp.message = "Ya existe la canción en la playlist"
            return resp.to_server_response(), 200

        return resp.to_server_response(), 200
    
class PlaylistDeleteSongResource(Resource):
    def post(self):
        authenticate_user()
        playlist_song = retrieve_response_data(request)
        playlist = Playlist.get_by_id(playlist_song["playlistId"])
        
        resp = CustomResponse(success=True)
        if playlist is None:
            resp.success = False
            resp.message = "Playlist inexistente"
            return resp.to_server_response(), 200

        index = 0
        while index < len(playlist.songs) and playlist.songs[index].songId != playlist_song['songId']:
            index += 1
        if index < len(playlist.songs):
            playlist.songs.pop(index)
            playlist.update()
            return resp.to_server_response(), 200
        else:
            resp.success = False
            resp.message = "La cancion no existe en la playlist"
            return resp.to_server_response(), 200

api.add_resource(PlaylistAddSongResource, '/api/playlist/addSong/', endpoint='playlist_add_song_resource')
api.add_resource(PlaylistDeleteSongResource, '/api/playlist/deleteSong/', endpoint='playlist_delete_song_resource')