from libs.db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户 ID
    nickname = db.Column(db.String(32), unique=True)  # 昵称
    password = db.Column(db.String(128))  # 用户的安全密码
    gender = db.Column(db.String(16))  # 性别
    city = db.Column(db.String(16))  # 城市
    avatar = db.Column(db.String(128))  # 头像地址
    birthday = db.Column(db.Date, default='2000-01-01')  # 生日
    bio = db.Column(db.Text())  # 个人简介
