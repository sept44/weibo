from libs.db import db


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)

    uid = db.Column(db.Integer)  # 用户 ID
    wid = db.Column(db.Integer)  # 微博 ID
    cid = db.Column(db.Integer)  # 评论 ID

    content = db.Column(db.Text)      # 评论内容
    created = db.Column(db.DateTime)  # 评论时间
