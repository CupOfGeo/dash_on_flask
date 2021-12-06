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
    from app.dashapp1.barapp import layout, register_callbacks
    from app.dashapp1.extratune import tune_layout, tune_register_callbacks
    from app.dashapp1.profile import profile_layout, profile_register_callbacks
    from app.dashapp1.voiceapp import voice_layout, voice_register_callbacks
    from app.dashapp1.helpers.CustomDash import CustomDash

    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=yes"}

    barapp = CustomDash(__name__,
                        server=app,
                        url_base_pathname='/demo/',
                        assets_folder=get_root_path(__name__) + '/dashapp1/assets/',
                        meta_tags=[meta_viewport], external_stylesheets=[dbc.themes.LUX],
                        )

    extratune = CustomDash(__name__,
                           server=app,
                           url_base_pathname='/tune/',
                           assets_folder=get_root_path(__name__) + '/dashapp1/assets/',
                           meta_tags=[meta_viewport], external_stylesheets=[dbc.themes.LUX],
                           )

    profile = CustomDash(__name__,
                         server=app,
                         url_base_pathname='/profile/',
                         assets_folder=get_root_path(__name__) + '/dashapp1/assets/',
                         meta_tags=[meta_viewport], external_stylesheets=[dbc.themes.LUX],
                         )

    voice = CustomDash(__name__,
                         server=app,
                         url_base_pathname='/',
                         assets_folder=get_root_path(__name__) + '/dashapp1/assets/',
                         meta_tags=[meta_viewport], external_stylesheets=[dbc.themes.LUX],
                         )

    with app.app_context():
        barapp.title = 'Synthetic bars'
        barapp.layout = layout
        register_callbacks(barapp)

        extratune.title = 'Tune'
        extratune.layout = tune_layout
        tune_register_callbacks(extratune)

        profile.title = 'USERNAME Profile'
        profile.layout = profile_layout
        profile_register_callbacks(profile)

        voice.title = 'RICK'
        voice.layout = voice_layout
        voice_register_callbacks(voice)

    # must be logged in to access
    _protect_dashviews(extratune)
    _protect_dashviews(profile)


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
