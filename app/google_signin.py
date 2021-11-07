from flask import redirect
from flask import url_for
from flask_login import login_user
from oauthlib.oauth2 import TokenExpiredError
from app.extensions import db
from app.models import User
from flask_dance.contrib.google import make_google_blueprint, google


google_bp = make_google_blueprint(scope=["profile", "email"])



@google_bp.route("/")
def index():

    if not google.authorized:
        return redirect(url_for("google.login"))
    try:
        resp = google.get("/oauth2/v1/userinfo")
        assert resp.ok, resp.text
        user = User.query.filter_by(username=resp.json()["email"]).first()
        if user == None:
            user = User(username=resp.json()["email"])
            db.session.add(user)
            db.session.commit()
        else:
            login_user(user)

    except TokenExpiredError as e:
        return redirect(url_for("google.login"))
    #print(resp.json())
    #{'id': 'xxx', 'email': 'mazzeogeorge@gmail.com', 'verified_email': True, 'name': 'George Mazzeo',

    return "You are {email} on Google".format(email=resp.json()["email"])

