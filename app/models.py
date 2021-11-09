from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

from app.extensions import db
from app.extensions import login
# flask db init
# flask db migrate -m "Adding column x."
# flask db upgrade


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # now email
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    models_allowed = db.Column(db.Integer, default=0)
    models_in_use = db.Column(db.Integer, default=0)

    def inc_models_allowed(self):
        self.models_allowed += 1

    def dec_models_allowed(self):
        self.models_allowed -= 1

    def inc_models_in_use(self):
        self.models_in_use += 1

    def dec_models_in_use(self):
        self.models_in_use -= 1

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class GPTModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer)
    name = db.Column(db.String(64))
    in_use = db.Column(db.Boolean)
    created = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    dataset_name = db.Column(db.String(64))

    # you pay and then get taken to a screen where you create a model dataset
    def init_model(self, owner_id, name, dataset_name):
        # when creating a model
        self.name = name
        self.owner = owner_id
        self.dataset_name = dataset_name
        # its in use but the time hasn't started yet start yet
        self.enable_model()

    def renew_model(self):
        # makes sure its true
        self.enable_model()

        self.created = datetime.now(timezone.utc).isoformat(timespec='seconds')
        self.end_date = self.created + datetime.timedelta(months=1)

    def disable_model(self):
        self.in_use = False

    def enable_model(self):
        self.in_use = True

    def rename_model(self, new_name):
        self.name = new_name

    def change_dataset(self, new_dataset):
        self.dataset_name = new_dataset
