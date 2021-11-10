from flask_login import UserMixin
from flask_login import current_user
from sqlalchemy import and_

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


# Should this be here?
# def get_user():
#     return load_user(current_user.get_id())

def get_models():
    if current_user and current_user.is_authenticated:
        return GPTModel.query.filter_by(owner_id=current_user.get_id()).all()
    else:
        return []


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

    def delete_model(self, model_id):
        self.dec_models_in_use()
        GPTModel.query.filter(and_(GPTModel.id == model_id, GPTModel.owner_id == self.id)).delete()
        db.session.commit()

    def make_model(self, model_name, dataset_id):
        self.inc_models_in_use()
        new_model = GPTModel()
        new_model.init_model(self.id, model_name, dataset_id)
        db.session.add(new_model)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __str__(self):
        return self.username


class GPTModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    # User input
    name = db.Column(db.String(64))
    dataset_id = db.Column(db.String(64))

    # To set
    in_use = db.Column(db.Boolean)
    created = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    # Maybe just do a check on the form validation side
    # Model names must be unique to each user
    # db.UniqueConstraint(owner_id, name,),

    # you pay and then get taken to a screen where you create a model dataset
    def init_model(self, owner_id, name, dataset_id):
        # when creating a model
        self.name = name
        self.owner_id = owner_id
        self.dataset_id = dataset_id
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
