from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Post body', validators=[DataRequired()])
    is_published = BooleanField('Is post published')