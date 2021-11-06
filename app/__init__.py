import dash
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required
from flask_bootstrap import Bootstrap

from config import BaseConfig
import dash_bootstrap_components as dbc


def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)

    bootstrap = Bootstrap(server)
    register_dashapps(server)
    register_extensions(server)
    register_blueprints(server)

    return server


def register_dashapps(app):
    from app.dashapp1.barapp import layout, register_callbacks, index_string
    from app.dashapp1.CustomDash import CustomDash

    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=yes"}

    dashapp1 = CustomDash(__name__,
                          server=app,
                          url_base_pathname='/',
                          assets_folder=get_root_path(__name__) + '/dashapp1/assets/',
                          meta_tags=[meta_viewport], external_stylesheets=[dbc.themes.LUX],
                          )

    print('HERE?:', get_root_path(__name__) + '/dashapp1/assets/')
    with app.app_context():
        dashapp1.title = 'Synthetic bars'
        dashapp1.layout = layout
        register_callbacks(dashapp1)

    # _protect_dashviews(dashapp1)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(
                dashapp.server.view_functions[view_func])


def register_extensions(server):
    from app.extensions import db
    from app.extensions import login
    from app.extensions import migrate

    db.init_app(server)
    login.init_app(server)
    login.login_view = 'main.login'
    migrate.init_app(server, db)


def register_blueprints(server):
    from app.google_signin import google_bp
    from app.webapp import server_bp
    from app.stripe_payment import stripe_bp, stripe_prefix

    server.register_blueprint(server_bp, url_prefix="/account")
    server.register_blueprint(google_bp, url_prefix="/google_login")
    server.register_blueprint(stripe_bp, url_prefix=stripe_prefix)
