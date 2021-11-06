from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from oauthlib.oauth2 import TokenExpiredError

from app.models import User

from flask_dance.contrib.google import make_google_blueprint, google

#server_bp = Blueprint('main', __name__)
google_bp = make_google_blueprint(scope=["profile", "email"])



@google_bp.route("/")
def index():

    if not google.authorized:
        return redirect(url_for("google.login"))
    try:
        resp = google.get("/oauth2/v1/userinfo")
        assert resp.ok, resp.text
        user = User(username=resp.json()["email"])
        login_user(user)

    except TokenExpiredError as e:
        return redirect(url_for("google.login"))
    #print(resp.json())
    #{'id': 'xxx', 'email': 'mazzeogeorge@gmail.com', 'verified_email': True, 'name': 'George Mazzeo',

    return "You are {email} on Google".format(email=resp.json()["email"])
