from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse

from app.extensions import db
from app.forms import LoginForm
from app.forms import RegistrationForm
# from app.forms import RegiserModel
from app.models import User
# load_user, Model

server_bp = Blueprint('main', __name__)

'''
checks if a user is logged in
if there is a user logged in return there username
else return None
'''
def is_logged_in():
    if current_user and current_user.is_authenticated:
        print('USER', current_user.username)
        return current_user.username
    else:
        return None


# def get_user():




@server_bp.route('/')
def index():
    return render_template("index.html", title='Home Page')


@server_bp.route('/swipe/')
def swipe():
    return render_template("swipe.html")

@server_bp.route('/login/', methods=['GET', 'POST'])
def login():
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


# @server_bp.route('/profile/')
# @login_required
# def profile():
#     user = load_user(current_user.get_id())
#     models = Model.query.filter_by(user_id=user.id).first()
#     form = RegiserModel()
#     if form.validate_on_submit():
#         form.username.data
#         if user is None or not user.check_password(form.password.data):
#             error = 'Invalid username or password'
#             return render_template('login.html', form=form, error=error)
#
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('main.index')
#         return redirect(next_page)



    return render_template('profile.html', models=models,
                           models_in_use=user.models_in_use, models_allowed=user.models_allowed,
                           form=form)

