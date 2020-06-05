import datetime

from flask import Blueprint
from flask import request
from flask import redirect
from flask import session
from flask import render_template

from .models import Comment
from libs.db import db
from libs.utils import login_required


comment_bp = Blueprint('comment', import_name='comment', url_prefix='/comment')


@comment_bp.route('/post', methods=('POST',))
@login_required
def post():
    uid = session['uid']
    wid = int(request.form.get('wid'))
    cid = int(request.form.get('cid', 0))
    content = request.form.get('content', '').strip()
    created = datetime.datetime.now()

    # 检查评论是否为空
    if not content:
        return redirect(f'/weibo/show?wid={wid}&error=评论内容不能为空')

    cmt = Comment(uid=uid, wid=wid, cid=cid, content=content, created=created)
    db.session.add(cmt)

    try:
        db.session.commit()  # 提交数据
    except Exception as e:
        print(e)
        db.session.rollback()
        return redirect(f'/weibo/show?wid={wid}&error=评论失败')
    else:
        return redirect(f'/weibo/show?wid={wid}')


@comment_bp.route('/delete')
@login_required
def delete():
    cid = int(request.args.get('cid'))
    cmt = Comment.query.get(cid)

    if cmt.uid == session['uid']:
        db.session.delete(cmt)
        Comment.query.filter_by(cid=cid).update({'cid': 0})  # 将本评论的回复指向微博本身
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        else:
            return redirect(f'/weibo/show?wid={cmt.wid}')
    else:
        return redirect(f'/weibo/show?wid={cmt.wid}&error=您没有权限删除别人的评论')
