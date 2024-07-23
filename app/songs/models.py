from app.db import db, BaseModelMixin


class Song(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    length = db.Column(db.Integer)
    year = db.Column(db.Integer)
    director = db.Column(db.String)
    actors = db.relationship('User', backref='song', lazy=False, cascade='all, delete-orphan')

    def __init__(self, title, length, year, director, actors=[]):
        self.title = title
        self.length = length
        self.year = year
        self.director = director
        self.actors = actors

    def __repr__(self):
        return f'Song({self.title})'

    def __str__(self):
        return f'{self.title}'
