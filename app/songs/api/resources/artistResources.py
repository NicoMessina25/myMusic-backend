from flask import request, Blueprint
from flask_restful import Api, Resource
from ....common.custom_response import CustomResponse
import sqlite3

from ..schemas import ArtistSchema
from ...models import Song, Artist
from ....common.error_handling import ObjectNotFound
from ....common.utils import retrieve_response_data

artist_bp = Blueprint('artist_bp', __name__)

artist_schema = ArtistSchema()

api = Api(artist_bp)

class ArtistListResource(Resource):
    def get(self):
        resp = CustomResponse(success=True)
        try:
            artists = Artist.get_all()
        except Exception as err:
            print(err)
            resp.success = False
            resp.message = "No se pudieron obtener los artistas"
            return resp, 405
        
        resp.data = artist_schema.dump(artists, many=True)
        return resp.to_server_response()

api.add_resource(ArtistListResource, '/api/artists/', endpoint='song_list_resource')
#api.add_resource(ArtistResource, '/api/songs/<int:song_id>', endpoint='song_resource')