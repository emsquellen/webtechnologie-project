from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class SeriesAddForm(FlaskForm):

    name = StringField('Title')
    description = StringField('Description'))
    year = IntegerField('Year of release')
    genre = StringField('Genre')
    seasons = IntegerField('Amount of seasons')
    submit = SubmitField('Submit')

class RankingAddForm(FlaskForm):
    title = StringField('Title of your new rankinglist:')
    submit = SubmitField('Submit')