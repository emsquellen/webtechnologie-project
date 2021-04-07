from flask import render_template,  Blueprint
base = Blueprint(
    "base", __name__)


@base.route('/', methods=['GET', 'POST'])
@base.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
