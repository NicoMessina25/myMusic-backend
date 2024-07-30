from app.db import db, BaseModelMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.profiles.models import EProfile

class User(db.Model, BaseModelMixin):
    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profileId = db.Column(db.Integer, db.ForeignKey('profile.profileId'), nullable=False, default=EProfile.PUBLIC.value)
    profile = db.relationship('Profile')
    
    def __init__(self, username, password, email, profileId = None):
        self.username = username
        self.set_password(password)
        self.email = email
        self.profileId = profileId 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    def to_dict(self):
        return {
            'userId': self.userId,
            'email': self.email,
            'username': self.username,
            'profile': self.profile.to_dict() if self.profile else None
            # Excluir 'password_hash' por razones de seguridad
        }
