from flask import request, Blueprint
from flask_restful import Api, Resource
from app.playlists.models import Playlist, playlist_song
from app.songs.models import Song, Artist
from app.songs.api.schemas import SongSchema
from ....common.custom_response import CustomResponse
from ....auth.authManager import authenticate_user
from ....common.utils import retrieve_response_data
from sqlalchemy import func,or_,and_,select
from app.db import db

playlist_songs_bp = Blueprint('playlist_songs_bp', __name__)
api = Api(playlist_songs_bp)

song_schema = SongSchema()

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
        playlist_song_dict = retrieve_response_data(request)
        resp = CustomResponse(success=True)
        
        delete_query = playlist_song.delete().where(and_(
            playlist_song.c.playlistId == playlist_song_dict["playlistId"],
            playlist_song.c.songId == playlist_song_dict["songId"]
        ))
        
        db.session.execute(delete_query)
        db.session.commit()
        return resp.to_server_response(), 200

        
class PlaylistListSongsResource(Resource):
    def get(self):
        resp = CustomResponse(success=True)
        playlist_id = request.args.get('playlistId', type=int)
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offSet', default=0, type=int)
        filter_ =  request.args.get('filter', default="", type=str)
        
        if not playlist_id:
            resp.success = False
            resp.message = "Playlist ID is required."
            return resp.to_server_response(), 400
        
        query = Song.query
        if filter_:
            filter_ = filter_.strip()
            query = query.join(Song.artists).filter(
                or_(
                    func.lower(Song.title).ilike(f"%{filter_.lower()}%"),
                    func.lower(Artist.name).ilike(f"%{filter_.lower()}%")
                )
            )
        
        # Consulta para obtener las canciones de la playlist con offset y limit
        songs = query.join(playlist_song).filter(
            playlist_song.c.playlistId == playlist_id).order_by("title").offset(offset).limit(limit).all()
        
        resp.data = song_schema.dump(songs, many=True)
        return resp.to_server_response(),200
    
class PlaylistListToAddSongsResource(Resource):
    def get(self):
        resp = CustomResponse(success=True)
        playlist_id = request.args.get('playlistId', type=int)
        limit = request.args.get('limit', default=15, type=int)
        offset = request.args.get('offSet', default=0, type=int)
        filter_ =  request.args.get('filter', default="", type=str)
        
        if not playlist_id:
            resp.success = False
            resp.message = "Playlist ID is required."
            return resp.to_server_response(), 400
        
        query = Song.query
        if filter_:
            filter_ = filter_.strip()
            query = query.join(Song.artists).filter(
                or_(
                    func.lower(Song.title).ilike(f"%{filter_.lower()}%"),
                    func.lower(Artist.name).ilike(f"%{filter_.lower()}%")
                )
            )
        
        # Subconsulta para obtener los IDs de las canciones que ya están en la playlist
        songs_in_playlist_subquery = db.session.query(Song.songId).join(Song.playlists).filter_by(playlistId=playlist_id).subquery()

        # Consulta para obtener las canciones con el filtro, excluyendo las que ya están en la playlist
        songs_to_add = query.filter(
                ~Song.songId.in_(select(songs_in_playlist_subquery.c.songId))  # Excluir las canciones que ya están en la playlist
            ).order_by("title").offset(offset).limit(limit).all()
        # 
        
        resp.data = song_schema.dump(songs_to_add, many=True)
        return resp.to_server_response(),200


api.add_resource(PlaylistAddSongResource, '/api/playlist/addSong/', endpoint='playlist_add_song_resource')
api.add_resource(PlaylistDeleteSongResource, '/api/playlist/deleteSong/', endpoint='playlist_delete_song_resource')
api.add_resource(PlaylistListSongsResource, '/api/playlist/songs/', endpoint='playlist_songs_resource')
api.add_resource(PlaylistListToAddSongsResource, '/api/playlist/songsToAdd/', endpoint='playlist_songs_to_add_resource')
