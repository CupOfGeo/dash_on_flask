import os


def get_sqlite_uri():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_name = os.environ['SQLITE_DATABASE_URL'].split('/')[-1]
    return f'sqlite:///{basedir}/{db_name}'

def get_postgress_uri():
    return os.environ['HEROKU_POSTGRESQL_RED_URL'].replace('postgres:','postgresql:')

class BaseConfig:
    # get_sqlite_uri()
    SQLALCHEMY_DATABASE_URI = get_postgress_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']
    # google auth
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
