from app.db import db, BaseModelMixin


playlist_song = db.Table(
    "playlist_song",
    db.Model.metadata,
    db.Column("playlistId", db.ForeignKey("song.songId"), primary_key=True),
    db.Column("songId", db.ForeignKey("playlist.playlistId"), primary_key=True),
    db.Column("addedAt", db.DateTime, nullable=False, default=db.func.current_timestamp())
)

class Playlist(db.Model, BaseModelMixin):
    __tablename__ = 'playlist'
    
    playlistId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    songs = db.relationship('Song', secondary= playlist_song, back_populates='playlists')

    def __init__(self, name, userId, description=None):
        self.name = name
        self.description = description
        self.userId = userId

    def __repr__(self):
        return f'Playlist({self.name})'

    def __str__(self):
        return f'{self.name}'