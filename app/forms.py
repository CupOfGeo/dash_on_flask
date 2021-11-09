from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired, Length, Regexp



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64, message='Exceeded max length 64')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class RegiserModel(FlaskForm):
    modelname = StringField('Model Name', validators=[DataRequired(), Regexp('^\w+$', message="Username must contain only letters numbers or underscore")])
    datasetname = StringField('Username', validators=[DataRequired(), Regexp('https:\/\/open\.spotify\.com\/playlist\/[0-9a-zA-Z]+', message="Not a spotify playlist link")])
    # https://open.spotify.com/playlist/1bsirFMYamoch1A5GyqDkA
    # https:\/\/open\.spotify\.com\/playlist\/[0-9a-zA-Z]+



'''
<div class="form-group has-success">
  <label class="form-label mt-4" for="inputValid">Valid input</label>
  <input type="text" value="correct value" class="form-control is-valid" id="inputValid">
  <div class="valid-feedback">Success! You've done it.</div>
</div>

<div class="form-group has-danger">
  <label class="form-label mt-4" for="inputInvalid">Invalid input</label>
  <input type="text" value="wrong value" class="form-control is-invalid" id="inputInvalid">
  <div class="invalid-feedback">Sorry, that username's taken. Try another?</div>
</div>

'''
