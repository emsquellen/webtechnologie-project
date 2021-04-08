from SB import db, app, login_manager
from flask import render_template, redirect, request, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user
from SB.models import User
from SB.login import LoginForm, RegistrationForm
blueprint = Blueprint(
    "secure", __name__, template_folder="templates", static_folder="static")


@app.context_processor
def secure():
    register_form = RegistrationForm()
    login_form = LoginForm()

    if register_form.validate_on_submit():
        user = User(email=register_form.email.data,
                    username=register_form.username.data,
                    password=register_form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Registered succesfully.', "success")
        redirect('/')
        return dict(login_form=login_form, register_form=register_form)

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user.check_password(login_form.password.data) and user is not None:
            login_user(user)
            print("success")
            flash(u'Logged in successfully.', "success")
            redirect('/profile')

            return dict(login_form=login_form, register_form=register_form)

    return dict(login_form=login_form, register_form=register_form)

@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!', "success")
    return redirect(url_for('base.index'))


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully.')
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('secure.profile')

            return redirect(next)
    return render_template('login.html', form=form)


@login_manager.unauthorized_handler
def unauthorized():
    flash(u'Please log in to view this page', 'warning')
    return redirect(url_for('secure.login', next=request.endpoint))