from flask import render_template, Blueprint, Markup, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from SB.models.series import Series
from flask_login import login_required, current_user
from SB import db

blueprint = Blueprint(
    "series", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/", methods=['GET', 'POST'])
@blueprint.route("/index", methods=['GET', 'POST'])
def index():
    titlelist = Series.get_index()
    return render_template('series_index.html', titlelist=titlelist)


@blueprint.route("/<int:series_id>", methods=['GET', 'POST'])
def info_page(series_id):
    id, name, description, year, genre, seasons, added_by = Series.get_data(
        id=series_id)

    return render_template('series.html',
                           id=id,
                           name=name,
                           description=description,
                           year=year,
                           genre=genre,
                           seasons=seasons,
                           added_by=added_by)


class SeriesAddForm(FlaskForm):

    name = StringField('Title')
    description = StringField('Description')
    year = IntegerField('Year of release')
    genre = StringField('Genre')
    seasons = IntegerField('Amount of seasons')
    submit = SubmitField('Submit')


@blueprint.route("/add", methods=['GET', 'POST'])
@login_required
def add():
    form = SeriesAddForm()

    if form.validate_on_submit():

        series_entry = Series(form.name.data, form.description.data, form.year.data,
                              form.genre.data, form.seasons.data, current_user.id)
        db.session.add(series_entry)
        db.session.commit()

        flash(f"Sucessfully added series {form.name.data}!")
        return render_template("add.html", form=form)

    return render_template("add.html", form=form)
