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


class Follow(db.Model):
    '''关注表'''
    __tablename__ = 'follow'

    uid = db.Column(db.Integer, primary_key=True)  # 关注者的 UID
    fid = db.Column(db.Integer, primary_key=True)  # 被关注者的 UID

    @classmethod
    def is_followed(cls, uid, fid):
        '''检查是否关注过对方'''
        query_result = cls.query.filter_by(uid=uid, fid=fid).exists()
        return db.session.query(query_result).scalar()
