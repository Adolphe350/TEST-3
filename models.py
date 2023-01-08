from flask_login import UserMixin

from __init__ import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password


class Post(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thumbnail = db.Column(db.String(500))
    body = db.Column(db.String(5000))
