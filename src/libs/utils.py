import os
from hashlib import sha256
from functools import wraps

from flask import session
from flask import redirect


def make_password(password):
    '''将密码进行安全处理'''
    # 确保 password 是一个 bytes 类型
    if not isinstance(password, bytes):
        password = str(password).encode('utf-8')

    # 产生一个安全密码: 包含 32 个字符的随机数 和 sha256 的哈希值
    safe_password = os.urandom(16).hex() + sha256(password).hexdigest()
    return safe_password


def check_password(password, safe_password):
    '''检查用户输入的密码'''
    # 确保 password 是一个 bytes 类型
    if not isinstance(password, bytes):
        password = str(password).encode('utf-8')

    password_hash = sha256(password).hexdigest()
    return password_hash == safe_password[32:]


def save_avatar(nickname, avatar):
    '''将用户头像保存到硬盘'''
    base_dir = os.path.dirname(os.path.abspath(__name__))  # 项目文件夹绝对路径
    filepath = os.path.join(base_dir, 'static', 'upload', nickname)  # 头像绝对路径
    avatar.save(filepath)  # 保存文件
    avatar_url = f'/static/upload/{nickname}'
    return avatar_url


def login_required(view_func):
    '''登录验证装饰器'''
    @wraps(view_func)
    def wrapper(*args, **Kwargs):
        if isinstance(session.get('uid'), int):
            return view_func(*args, **Kwargs)
        else:
            return redirect('/user/login')
    return wrapper
