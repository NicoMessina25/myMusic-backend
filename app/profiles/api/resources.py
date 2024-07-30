from flask import request, Blueprint
from flask_restful import Api, Resource
from ...common.custom_response import CustomResponse
from sqlalchemy import func

from .schemas import ProfileSchema
from ..models import Profile
from app.auth.authManager import authenticate_user
from app.profiles.models import EProfile

profile_bp = Blueprint('profile_bp', __name__)

profile_schema = ProfileSchema()

api = Api(profile_bp)

class ProfileListResource(Resource):
    def get(self):
        resp = CustomResponse(success=True)
        authenticate_user([EProfile.ADMIN])
        limit = request.args.get('limit', default=50, type=int)
        name_filter = request.args.get('filter', default='', type=str)
        
        query = Profile.query
        if name_filter:
            query = query.filter(func.lower(Profile.name).ilike(f"%{name_filter.lower()}%"))
        profiles = query.limit(limit).all()
        
        resp.data = profile_schema.dump(profiles, many=True)
        return resp.to_server_response()

api.add_resource(ProfileListResource, '/api/profiles/', endpoint='song_list_resource')