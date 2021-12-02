from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse

from app.extensions import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User, GPTModel, load_user


server_bp = Blueprint('main', __name__)


def get_user():
    """
    checks if a user is logged in
    if there is a user logged in return there username
    else return None
    """
    if current_user and current_user.is_authenticated:
        user = load_user(current_user.get_id())
        return user
    else:
        return None





@server_bp.route('/')
def index():
    """/account index page TODO make this profile?"""
    return render_template("index.html", title='Home Page')


@server_bp.route('/swipe/')
def swipe():
    """TODO Swipe functionality like tinder"""
    return render_template("swipe.html")


@server_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """login page TODO remove this and replace with just google sign in"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            error = 'Invalid username or password'
            return render_template('login.html', form=form, error=error)

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@server_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@server_bp.route('/register/', methods=['GET', 'POST'])
def register():
    """register a user but honestly I don't want to do this would rather have people just sign in with google"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.login'))

    return render_template('register.html', title='Register', form=form)

