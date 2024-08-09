from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from app.common.error_handling import ObjectNotFound, AppErrorBaseClass
from app.db import db
from app.jwt import jwt
from app.songs.api.resources.songResources import songs_bp
from app.songs.api.resources.artistResources import artist_bp
from app.playlists.api.resources.resources import playlist_bp
from app.songs.api.resources.songResources import songs_bp
from app.users.api.resources import user_bp
from app.common.custom_response import CustomResponse
from app.auth.resources import auth_bp
from app.profiles.api.resources import profile_bp
from app.playlists.api.resources.songResources import playlist_songs_bp
from .ext import ma, migrate
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError

def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    
    # Habilita el CORS
    CORS(app, supports_credentials=True)
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Inicializa las extensiones
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    # Captura todos los errores 404
    Api(app, catch_all_404s=True)

    # Deshabilita el modo estricto de acabado de una URL con /
    app.url_map.strict_slashes = False

    # Registra los blueprints
    app.register_blueprint(songs_bp)
    app.register_blueprint(artist_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(playlist_bp)
    app.register_blueprint(playlist_songs_bp)

    # Registra manejadores de errores personalizados
    register_error_handlers(app)

    return app

def register_error_handlers(app:Flask):
    
    def handle_invalid_signature_error(err):
        print(err)
        resp = CustomResponse(success=False)
        resp.message = "Credenciales inválidas"
        return resp.to_server_response(), 401
    
    def handle_expired_signature_error(err):
        print(err)
        resp = CustomResponse(success=False)
        resp.message = "Credenciales inválidas"
        return resp.to_server_response(), 401
    
    def handle_permission_error(err:PermissionError):
        resp = CustomResponse(success=False)
        resp.message = str(err)            
        return resp.to_server_response(), 403
    
    def handle_exception_error(e):
        print(e)
        return jsonify({'msg': 'Internal server error', 'error': str(e)}), 500

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed'}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'Not Found error'}), 404

    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({'msg': str(e)}), 500

    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({'msg': str(e)}), 404
    
    app.register_error_handler(InvalidSignatureError, handle_invalid_signature_error)
    app.register_error_handler(ExpiredSignatureError, handle_expired_signature_error)
    app.register_error_handler(PermissionError, handle_permission_error)
    app.register_error_handler(Exception, handle_exception_error)
    
