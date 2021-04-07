from flask import render_template, Blueprint, Markup, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, validators, SelectField, FileField
from SB.models.series import Series
from SB.models import User
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
    id = User.get_username(id)

    return render_template('series.html',
                           id=id,
                           name=name,
                           description=description,
                           year=year,
                           genre=genre,
                           seasons=seasons,
                           added_by=added_by)


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

        flash(f"Sucessfully added series {form.name.data}!")
        return render_template("add.html", form=form)

    return render_template("add.html", form=form)
