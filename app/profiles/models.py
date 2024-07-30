from app.db import db, BaseModelMixin
from enum import Enum

class EProfile(Enum):
    ADMIN = 1
    ADMINISTRATIVE = 2
    PUBLIC = 3

class Profile(db.Model, BaseModelMixin):
    __tablename__ = 'profile'
    
    profileId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    def to_dict(self):
        return {
            'profileId': self.profileId,
            'name':self.name
        }
    