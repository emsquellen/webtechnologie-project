from flask import render_template, Blueprint, Markup, flash, Response, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, validators, SelectField, FileField
from SB.models.series import Series
from SB.models import User
from SB.models.ranking import RankinglistItem
from flask_login import login_required, current_user
from SB import db

blueprint = Blueprint(
    "series", __name__, template_folder="templates", static_folder="static")


@blueprint.route("/", methods=['GET', 'POST'])
@blueprint.route("/index", methods=['GET', 'POST'])
def index():
    titlelist = Series.get_index()
    empty_state = True if len(titlelist) == 0 else False
    return render_template('series_index.html',
                           titlelist=titlelist, empty_state=empty_state)


class AddToRanglist(FlaskForm):
    rankinglist_id = IntegerField('Ranglist', validators=[
        validators.DataRequired("Please specify a ranglist")])
    index = IntegerField('Ranglist', validators=[
        validators.DataRequired("Please specify a index")])
    submit = SubmitField('Submit')


@blueprint.route("/<int:series_id>", methods=['GET', 'POST'])
def info_page(series_id):
    id, name, description, year, genre, seasons, added_by = Series.get_data(
        id=series_id)

    form = AddToRanglist()

    if form.validate_on_submit():
        if RankinglistItem.query.filter(
            RankinglistItem.rankinglist_id.like(form.rankinglist_id.data)
            ).filter(
            RankinglistItem.series.like(series_id)
        ).first() is None:

            new_entry = RankinglistItem(
                form.rankinglist_id.data, series_id, form.index.data)
            db.session.add(new_entry)
            db.session.commit()

            flash(Markup(
                f"Successfully added {name} to ranglist! <a href='/rankinglist/{{ new_entry.rankinglist_id }}'>Click here to view!</a>'"))
            return redirect(f'../rankinglist/{new_entry.rankinglist_id}')
        else:
            flash(
                f'Series already in ranglist {form.rankinglist_id.data}', 'warning')

    added_by = User.get_username(added_by)

    return render_template('series.html',
                           id=id,
                           name=name,
                           description=description,
                           year=year,
                           genre=genre,
                           seasons=seasons,
                           added_by=added_by,
                           form=form)


class SeriesAddForm(FlaskForm):

    name = StringField('Title', validators=[
                       validators.DataRequired("Title is required")])
    img = FileField('Image')
    description = TextAreaField('Description', validators=[
                                validators.DataRequired("Please provide a description")])
    year = IntegerField('Year of release', validators=[
                        validators.NumberRange(1800, 2023, "Pleas enter a year")])
    genre = SelectField(u'genre', choices=["action series",
                                           "adventure series",
                                           "animated series",
                                           "anthology series",
                                           "art",
                                           "cartoon series",
                                           "children's series",
                                           "comedy",
                                           "cooking show",
                                           "courtroom drama",
                                           "current affairs",
                                           "daytime television",
                                           "dark comedy",
                                           "detective fiction",
                                           "docudrama",
                                           "documentary",
                                           "dramality",
                                           "dramatic programming",
                                           "dramedy",
                                           "educational",
                                           "factual television",
                                           "fantasy",
                                           "game show",
                                           "infomercials",
                                           "instructional",
                                           "late night television",
                                           "legal drama",
                                           "medical drama",
                                           "mockumentary",
                                           "music television",
                                           "news show",
                                           "nsfw",
                                           "police procedural",
                                           "prime-time television",
                                           "reality",
                                           "religious",
                                           "romcom",
                                           "science fiction",
                                           "serial",
                                           "sitcom",
                                           "soap opera",
                                           "space western",
                                           "sports",
                                           "stand-up comedy",
                                           "tabloid television",
                                           "telenovela",
                                           "variety show",
                                           "western series"])
    seasons = IntegerField('Amount of seasons', validators=[
                           validators.NumberRange(1, 99, "You forgot to add amount of seasons")])
    submit = SubmitField('Submit')


@blueprint.route("/add", methods=['GET', 'POST'])
@login_required
def add():
    form = SeriesAddForm()

    if form.validate_on_submit():
        if form.img:
            pass

        series_entry = Series(form.name.data, form.description.data, form.year.data,
                              form.genre.data, form.seasons.data, current_user.id)
        db.session.add(series_entry)
        db.session.commit()

        flash(f"Successfully added series {form.name.data}!")
        return render_template("add.html", form=form)

    return render_template("add.html", form=form)


@blueprint.route('/delete/<int:series_id>', methods=['GET', 'POST'])
def delete(series_id):
    try:
        serie = Series.query.filter_by(id=series_id).first()
        db.session.delete(serie)
        db.session.commit()
        flash(u'Deletion submitted sucessfully', 'success')
        return Response(status=200, mimetype='application/json')
    except:
        return Response(status=500, mimetype='application/json')
