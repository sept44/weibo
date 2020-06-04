import datetime

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import session

from libs.db import db
from weibo.models import Weibo
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
        created = datetime.datetime.now()
        weibo = Weibo(uid=uid, content=content, created=created)
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
        Weibo.query.filter_by(id=wid).update({Weibo.content: content})

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
    Weibo.query.filter_by(id=wid).delete()

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
    weibo = Weibo.query.get(wid)
    return render_template('show.html', weibo=weibo)


@weibo_bp.route('/list')
def weibo_list():
    '''微博列表'''
