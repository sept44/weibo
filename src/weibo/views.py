import datetime
from math import ceil

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import session

from libs.db import db
from libs.config import PER_PAGE
from weibo.models import Weibo
from comment.models import Comment
from libs.utils import login_required


weibo_bp = Blueprint('weibo', import_name='weibo',
                     url_prefix='/weibo', template_folder='./templates')


@weibo_bp.route('/post', methods=('GET', 'POST'))
@login_required
def post_weibo():
    '''发布微博'''
    if request.method == "POST":
        content = request.form.get('content', '').strip()
        if not content:
            return render_template('post.html', error='微博内容不能为空')
        uid = session['uid']
        created = updated = datetime.datetime.now()  # 创建时间和修改时间相同
        weibo = Weibo(uid=uid, content=content, created=created, updated=updated)
        db.session.add(weibo)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return render_template('post.html', error='服务器内部错误')
        else:
            return redirect(f'/weibo/show?wid={weibo.id}')
    else:
        return render_template('post.html')


@weibo_bp.route('/edit', methods=('GET', 'POST'))
@login_required
def edit_weibo():
    '''编辑微博'''
    if request.method == 'POST':
        wid = request.form.get('wid')
        content = request.form.get('content')

        # 修改当前微博
        updated = datetime.datetime.now()
        Weibo.query.filter_by(id=wid).update({Weibo.content: content, Weibo.updated: updated})

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return render_template('edit.html', error='服务器内部错误')
        else:
            return redirect(f'/weibo/show?wid={wid}')

    else:
        wid = int(request.args.get('wid'))
        weibo = Weibo.query.get(wid)
        return render_template('edit.html', weibo=weibo)


@weibo_bp.route('/delete')
@login_required
def delete_weibo():
    '''删除微博'''
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    if weibo.uid != session['uid']:
        return redirect(f'/weibo/show?wid={wid}&error=您没有权限删除别人的微博')

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return redirect(f'/weibo/show?wid={wid}&error=服务器内部错误')
    else:
        return redirect('/')


@weibo_bp.route('/show')
def show_weibo():
    '''查看微博'''
    wid = int(request.args.get('wid'))
    error = request.args.get('error')
    weibo = Weibo.query.get(wid)  # 取出当前微博

    # 取出当前微博下所有的评论
    comments = Comment.query.filter_by(wid=wid).order_by(Comment.created.desc())

    return render_template('show.html', weibo=weibo, comments=comments, error=error)


@weibo_bp.route('/list')
def weibo_list():
    '''微博列表'''
    page = int(request.args.get('page', 1))  # 页码

    # 取出当前页需要显示的微博
    offset = (page - 1) * PER_PAGE  # 要跳过的微博

    # 将所有微博按 updated 的降序排列
    weibo_list = Weibo.query.order_by(Weibo.updated.desc()).limit(PER_PAGE).offset(offset)

    # 计算总页数：总页数 = math.ceil(总条数 / 30)
    total = Weibo.query.count()
    n_page = ceil(total / PER_PAGE)
    min_page = (page - 5) if page > 5 else 1
    max_page = min((page + 5), n_page)

    return render_template('index.html', weibo_list=weibo_list,
                           min_page=min_page, max_page=max_page, page=page)
