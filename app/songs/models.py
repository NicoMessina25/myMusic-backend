from app.db import db, BaseModelMixin

song_artist = db.Table(
    "song_artist",
    db.Model.metadata,
    db.Column("songId", db.ForeignKey("song.songId"), primary_key=True),
    db.Column("artistId", db.ForeignKey("artist.artistId"), primary_key=True),
)


class Song(db.Model, BaseModelMixin):   
    __tablename__ = 'song'
     
    songId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    length = db.Column(db.Integer)
    releaseDate = db.Column(db.Date)
    artists = db.relationship(
        'Artist', secondary=song_artist, back_populates="songs"
    )

    def __init__(self, title, length, releaseDate, artists=None):
        self.title = title
        self.length = length
        self.releaseDate = releaseDate
        self.artists = artists if artists is not None else []

    def __repr__(self):
        return f'Song({self.title})'

    def __str__(self):
        return f'{self.title}'

class Artist(db.Model, BaseModelMixin):
    __tablename__ = 'artist'
    
    artistId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    songs = db.relationship(
        'Song', secondary=song_artist, back_populates="artists"
    )
    #song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)

    def __init__(self, name, songs=None):
        self.name = name
        self.songs = songs if songs is not None else []

    def __repr__(self):
        return f'Artist({self.name})'

    def __str__(self):
        return f'{self.name}'