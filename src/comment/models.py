from libs.db import db
from user.models import User
from weibo.models import Weibo


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)

    uid = db.Column(db.Integer)  # 用户 ID
    wid = db.Column(db.Integer)  # 微博 ID
    cid = db.Column(db.Integer)  # 评论 ID

    content = db.Column(db.Text)      # 评论内容
    created = db.Column(db.DateTime)  # 评论时间

    @property
    def user(self):
        '''当前评论的作者'''
        if not hasattr(self, '_user'):
            self._user = User.query.get(self.uid)
        return self._user

    @property
    def weibo(self):
        '''当前评论的微博'''
        if not hasattr(self, '_weibo'):
            self._weibo = Weibo.query.get(self.wid)
        return self._weibo

    @property
    def reply_comment(self):
        '''当前回复的评论'''
        if self.cid == 0:
            return None

        elif not hasattr(self, '_reply_comment'):
            self._reply_comment = Comment.query.get(self.cid)

        return self._reply_comment
