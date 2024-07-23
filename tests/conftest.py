import sys
import os
import pytest
from flask_jwt_extended import create_access_token

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

@pytest.fixture
def client():
    app = create_app('config.default')
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def auth_header(client):
    access_token = create_access_token(identity='testuser')
    return {'Authorization': f'Bearer {access_token}'}
