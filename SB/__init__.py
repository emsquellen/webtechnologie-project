from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = None
db = None
login_manager = LoginManager()


def create_app():
    global app
    app = Flask(__name__,
                template_folder="base/templates",
                static_folder="base/static")

    app.secret_key = "e79dce37365b401497eeaccb3b148b7b5416fab25e14ac26"

    global db
    basedir = os.path.abspath(os.path.dirname(__file__))
    db = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    Migrate(app, db)

    global login_manager
    login_manager.init_app(app)
    login_manager.login_view = "secure.login"

    from SB.views import base, secure, series, ranking

    @app.after_request
    def add_header(r):
        """ Adds headers to request """

        # No need for caching when debugging
        if app.debug:
            r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            r.headers["Pragma"] = "no-cache"
            r.headers["Expires"] = "0"
            r.headers['Cache-Control'] = 'public, max-age=0'
        return r

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    db.create_all()

    app.register_blueprint(base.base)
    app.register_blueprint(secure.blueprint)
    app.register_blueprint(series.blueprint, url_prefix="/series")
    app.register_blueprint(ranking.blueprint, url_prefix="/rankinglist")
    return app


def run():
    app = create_app()
    app.run(debug=True)
