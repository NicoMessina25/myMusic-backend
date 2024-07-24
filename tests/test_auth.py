import pytest
from app import create_app, db
from app.users.models import User

@pytest.fixture
def client():
    app = create_app('config.default')
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_register(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    print(response.data)  # Imprimir los datos de respuesta para depuración
    assert response.status_code == 201
    assert response.json['msg'] == 'User created successfully'

def test_login(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    print(response.data)  # Imprimir los datos de respuesta para depuración
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json
