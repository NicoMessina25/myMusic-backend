from app.db import db, BaseModelMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, BaseModelMixin):
    userid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def __init__(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'userid': self.userid,
            'email': self.email,
            'username': self.username,
            # Excluir 'password_hash' por razones de seguridad
        }
