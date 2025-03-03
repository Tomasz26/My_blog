from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from config import Config
from werkzeug.routing import ValidationError

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Post body', validators=[DataRequired()])
    is_published = BooleanField('Is post published')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate_username(self, field):
        if field.data == Config.ADMIN_USERNAME:
            return field.data
        else:
            raise ValidationError("Invalid username")

    def validate_password(self, field):
        if field.data == Config.ADMIN_PASSWORD:
            return field.data
        else:
            raise ValidationError("Invalid password")
    