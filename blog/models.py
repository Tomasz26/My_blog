# blog/models.py

from . import db
import datetime

class Entry(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(80), nullable=False)
   body = db.Column(db.Text, nullable=False)
   pub_date = db.Column(db.DateTime, nullable=False,
       default=datetime.datetime.utcnow)
   is_published = db.Column(db.Boolean, default=False)

class Message(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name_surname = db.Column(db.String(120), nullable=False)
   contact_mail = db.Column(db.String(120), nullable=False)
   body = db.Column(db.Text, nullable=False)
   pub_date = db.Column(db.DateTime, nullable=False,
       default=datetime.datetime.utcnow)