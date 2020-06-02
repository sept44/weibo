from flask import Blueprint

from .models import User


user_bp = Blueprint('user',
                    import_name='user',
                    url_prefix='/user',
                    template_folder='./templates'
                    )


@user_bp.route('/login')
def login():
    return 'login'


@user_bp.route('/register')
def register():
    return 'register'
