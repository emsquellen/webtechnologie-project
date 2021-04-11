# Ex
from flask import render_template, Blueprint, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators
from flask_login import login_required, current_user
# Our own modules
from SB.models.ranking import Rankinglist, RankinglistItem
from SB.models.series import Series
from SB.models import User
from SB import db

blueprint = Blueprint(
    "rankinglists", __name__, template_folder="templates", static_folder="static")


class AddItem(FlaskForm):
    id = IntegerField('Series ID', validators=[
        validators.DataRequired("Title is required")])
    index = IntegerField('Index', validators=[
        validators.DataRequired("Index is required")])
    submit = SubmitField('Submit')


@blueprint.route("/<int:list_id>", methods=['GET', 'POST'])
@login_required
def rankinglist(list_id):
    form = AddItem()

    if form.validate_on_submit():
        new_entry = RankinglistItem(list_id, form.id.data, form.index.data)
        db.session.add(new_entry)
        db.session.commit()

        flash(u"Successfully added entry", 'success')
        return redirect(f'./{list_id}')

    title, creator, date_added, contents = Rankinglist.get_data(
        rankinglist_id=list_id)
    creator = User.get_username(creator)
    entries = RankinglistItem.get_data(list_id)
    index = [x[2] for x in entries]
    series = [Series.get_data(x[1]) for x in entries]
    length = len(series)
    return render_template('ranklist.html',
                           title=title,
                           rankinglist_id=list_id,
                           creator=creator,
                           date_added=date_added,
                           index=index,
                           series=series,
                           length=length,
                           form=form)


class RankingAddForm(FlaskForm):
    title = StringField('Title of your new rankinglist:', validators=[
        validators.DataRequired("Title is required")])
    submit = SubmitField('Submit')


@blueprint.route("/add", methods=['GET', 'POST'])
@login_required
def add():
    form = RankingAddForm()

    if form.validate_on_submit():
        new_entry = Rankinglist(form.title.data, current_user.id)
        db.session.add(new_entry)
        db.session.commit()

        flash(f"Successfully made rankinglist {form.title.data}!")
        return redirect(f'../rankinglist/{new_entry.rankinglist_id}')

    return render_template("add_rank.html", form=form)


@blueprint.route("/", methods=['GET', 'POST'])
@blueprint.route("/index", methods=['GET', 'POST'])
@login_required
def index():
    rankings = Rankinglist.index_list()

    return render_template('rindex.html', rankings=rankings)
