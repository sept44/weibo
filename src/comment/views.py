from flask import Blueprint
from flask import request
from flask import redirect
from flask import render_template

from .models import Comment
from libs.utils import login_required


comment_bp = Blueprint('comment', import_name='comment', url_prefix='/comment')


@comment_bp.route('/post')
@login_required
def post():
    return render_template('')


@comment_bp.route('/delete')
@login_required
def delete():
    return render_template('')
