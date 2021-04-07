from SB import db
from datetime import datetime
from base64 import b64encode

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
    img = db.Column(db.BLOB)
    description = db.Column(db.String(512))
    year = db.Column(db.Integer)
    genre = db.Column(db.String(16))
    seasons = db.Column(db.Integer)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, img, description, year, genre, seasons, added_by):
        self.name = name
        self.img = img
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
            data.imgloader(),
            data.description,
            data.year,
            data.genre,
            data.seasons,
            data.added_by,]

    @classmethod
    def get_index(cls):
        L = []
        data = cls.query.all()
        for item in data:
            itemlist = []
            itemlist.append(item.name)
            itemlist.append(item.description)
            itemlist.append(item.id)
            itemlist.append(item.imgloader())
            L.append(itemlist)
        return L

    def img_loader(self):
        img = "data:;base64," + base64.b64encode(self.img).decode('ascii') if self.img else None
