from .. import db
from datetime import datetime
from .series import Series
from SB.models import User

class Rankinglist(db.Model):
    __tablename__ = 'rankinglist'

    rankinglist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), unique=True, index=True)
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_added = db.Column(db.DateTime)
    contents = db.relationship('RankinglistItem', backref="ranklist")

    def __init__(self, title, creator):
        self.title = title
        self.creator = creator
        self.date_added = datetime.now()

    @classmethod
    def get_data(cls, rankinglist_id):
        data = cls.query.filter_by(rankinglist_id=rankinglist_id).first()
        return [
            data.title,
            data.creator,
            data.date_added,
            data.contents]

    @classmethod
    def autocomplete(cls):
        pass

    @classmethod
    def index_list(cls):
        data = cls.query.all()
        item_catalog = []
        for item in data:
            single = []
            single.append(item.rankinglist_id)
            single.append(item.title)
            single.append(User.query.filter_by(id=item.creator).first().username)
            item_catalog.append(single)
        return item_catalog


class RankinglistItem(db.Model):
    __tablename__ = 'rankinglist_item'

    rankinglist_id = db.Column(db.Integer, db.ForeignKey(
                           'rankinglist.rankinglist_id'), primary_key=True)
    series = db.Column(db.Integer, db.ForeignKey(
                       'series.id'), primary_key=True)
    index = db.Column(db.Integer)

    def __init__(self, rankinglist_id, series, index):
        self.rankinglist_id = rankinglist_id
        self.series = series
        self.index = index

    @classmethod
    def get_data(cls, rankinglist_id):
        L = []
        data = cls.query.filter_by(rankinglist_id=rankinglist_id).all()
        for item in data:
            itemlist = []
            itemlist.append(item.rankinglist_id)
            itemlist.append(item.series)
            itemlist.append(item.index)
            L.append(itemlist)
        return L
