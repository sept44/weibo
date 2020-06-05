from libs.db import db

from user.models import User


class Weibo(db.Model):
    '''微博表'''
    __tablename__ = 'weibo'

    id = db.Column(db.Integer, primary_key=True)  # 微博ID
    uid = db.Column(db.Integer)                   # 对应的用户 ID
    content = db.Column(db.Text)                  # 微博内容
    created = db.Column(db.DateTime)              # 微博创建时间
    updated = db.Column(db.DateTime)              # 微博修改时间

    uid_list = '1,3,9,17'

    @property
    def user(self):
        '''当前微博作者'''
        if not hasattr(self, '_user'):
            self._user = User.query.get(self.uid)
        return self._user


class Like(db.Model):
    '''点赞表'''
    __tablename__ = 'like'

    uid = db.Column(db.Integer, primary_key=True)  # 对应的用户 ID
    wid = db.Column(db.Integer, primary_key=True)  # 对应的微博 ID
