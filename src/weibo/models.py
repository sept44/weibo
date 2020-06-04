from libs.db import db


class Weibo(db.Model):
    '''微博表'''
    __tablename__ = 'weibo'

    id = db.Column(db.Integer, primary_key=True)  # 微博ID
    uid = db.Column(db.Integer)                   # 对应的用户 ID
    content = db.Column(db.Text)                  # 微博内容
    created = db.Column(db.DateTime)              # 微博创建时间
