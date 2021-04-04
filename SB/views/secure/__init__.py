from SB import db
from flask import render_template, redirect, request, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user
from SB.models import User
from SB.login import LoginForm, RegistrationForm
blueprint = Blueprint(
    "secure", __name__, template_folder="templates", static_folder="static")


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully.', "success")
            next = request.args.get('next')
            if next is None or not next[0] == '/':
                next = '/login'

            return redirect(next)
    return render_template('login.html', form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Dank voor de registratie. Er kan nu ingelogd worden! ', "success")
        return redirect('/')
    return render_template('register.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!', "success")
    return redirect(url_for('base.index'))


@blueprint.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
