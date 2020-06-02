from libs.db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))
    bio = db.Column(db.Text())
    age = db.Column(db.Integer)
    gender = db.Column(db.String(16))
    avatar = db.Column(db.String(128))
