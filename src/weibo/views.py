from flask import Blueprint

from weibo.models import Weibo


weibo_bp = Blueprint('weibo', import_name='weibo', url_prefix='/weibo', template_folder='./')


@weibo_bp.route('/post')
def post_weibo():
    '''发布微博'''


@weibo_bp.route('/edit')
def edit_weibo():
    '''编辑微博'''


@weibo_bp.route('/delete')
def delete_weibo():
    '''删除微博'''


@weibo_bp.route('/show')
def show_weibo():
    '''查看微博'''


@weibo_bp.route('/list')
def weibo_list():
    '''微博列表'''
