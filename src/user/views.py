from flask import Blueprint
from flask import render_template
from flask import session
from flask import request
from flask import redirect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from .models import User
from .models import Follow
from libs.db import db
from libs import utils


user_bp = Blueprint('user',
                    import_name='user',
                    url_prefix='/user',
                    template_folder='./templates'
                    )


@user_bp.route('/register', methods=('GET', 'POST'))
def register():
    '''注册'''
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()
        gender = request.form.get('gender', 'unknow').strip()
        city = request.form.get('city', '上海').strip()
        avatar = request.files.get('avatar')
        birthday = request.form.get('birthday', '2000-01-01').strip()
        bio = request.form.get('bio', '').strip()

        if not (nickname and password):
            return render_template('register.html', error='昵称或密码不能为空')

        safe_password = utils.make_password(password)  # 安全处理密码
        avatar_url = utils.save_avatar(nickname, avatar)  # 保存头像，并返回头像网址

        user = User(nickname=nickname, password=safe_password, gender=gender,
                    city=city, avatar=avatar_url, birthday=birthday, bio=bio)

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  # 操作失败，进行事务回滚
            return render_template('register.html', error='昵称或密码不能为空')
        return redirect('/user/login')
    else:
        return render_template('register.html')


@user_bp.route('/login', methods=('POST', 'GET'))
def login():
    '''登录'''
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()

        if not (nickname and password):
            return render_template('login.html', error='昵称或密码不能为空')

        # 先根据昵称取到当前用户
        try:
            user = User.query.filter_by(nickname=nickname).one()
        except (NoResultFound, MultipleResultsFound):
            return render_template('login.html', error='昵称或密码输入错误')

        # 检查密码
        if utils.check_password(password, user.password):
            # 登录
            session['uid'] = user.id
            session['nickname'] = user.nickname
            return redirect('/user/info')
        else:
            return render_template('login.html', error='昵称或密码输入错误')
    else:
        return render_template('login.html')


@user_bp.route('/info')
def info():
    '''显示当前用户的信息'''
    uid = session['uid']
    other_uid = int(request.args.get('uid', 0))

    if other_uid:
        # 查看其他人的信息页
        user = User.query.get(other_uid)
        is_followed = Follow.is_followed(uid, other_uid)
    else:
        # 查看个人的信息页
        user = User.query.get(uid)
        is_followed = None

    return render_template('info.html', user=user, is_followed=is_followed)


@user_bp.route('/follow')
def follow():
    '''关注 / 取消关注'''
    fid = int(request.args.get('fid'))  # 从页面获取被关注者的 UID
    uid = session['uid']

    follow_relation = Follow(uid=uid, fid=fid)
    db.session.add(follow_relation)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # 发生冲突时，说明已经关注过此人，需要取消关注

        Follow.query.filter_by(uid=uid, fid=fid).delete()  # 取消关注，删除两人的关系
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    return redirect(f'/user/info?uid={fid}')
