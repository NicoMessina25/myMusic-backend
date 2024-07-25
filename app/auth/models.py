from app.db import db, BaseModelMixin
from datetime import datetime

class TokenBlockList(db.Model, BaseModelMixin):
    __tablename__ = 'tokenblocklist'

    tokenblocklistid = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(), nullable=False)
    create_at = db.Column(db.DateTime(), default = datetime.now)
    
    def __repr__(self):
        return f"<Token {self.jti}>"