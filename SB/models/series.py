from SB import db
from datetime import datetime


# id
# name
# description
# year
# genre
# seasons
# added_by

class Series(db.Model):
    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(128))
    year = db.Column(db.Integer)
    genre = db.Column(db.String(16))
    seasons = db.Column(db.Integer)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, description, year, genre, seasons, added_by):
        self.name = name
        self.description = description
        self.year = year
        self.genre = genre
        self.seasons = seasons
        self.added_by = added_by

    # def __str__(self):
    #     return f'Title: {self.name}, Description: {self.description}, Year of release: {self.year}, Genre: {self.genre}, Amount of seasons: {self.seasons}. Added by: {self.added_by}'

    @classmethod
    def get_data(cls, id):
        data = cls.query.filter_by(id=id).first()
        return [
            data.id,
            data.name,
            data.description,
            data.year,
            data.genre,
            data.seasons,
            data.added_by,]
