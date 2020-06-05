#!/usr/bin/env python

from flask import Flask
from flask import redirect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from libs.db import db
from libs import config
from user.views import user_bp
from weibo.views import weibo_bp
from libs.utils import fake_sentence
from libs.utils import fake_word

# 初始化 App
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 初始化DB迁移模块
migrate = Migrate(app, db)

# 初始化命令行管理工具
manager = Manager(app)
manager.add_command('db', MigrateCommand)

app.register_blueprint(user_bp)
app.register_blueprint(weibo_bp)


@app.route('/')
def home():
    return redirect('/weibo/list')


@manager.command
def fake():
    import random
    from user.models import User
    from weibo.models import Weibo

    # 随机创建用户
    users = []
    for i in range(20):
        user = User(
            nickname=fake_word().title(),
            gender=random.choice(['male', 'female', 'unknow']),
            city=random.choice(['北京', '上海', '深圳', '太原', '福州', '南京']),
            avatar='/static/upload/default',
            birthday='1990-03-05',
            bio=fake_sentence(),
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

    # 随机创建微博
    weibo_list = []
    for i in range(1000):
        y = random.randint(2000, 2020)
        m = random.randint(1, 12)
        d = random.randint(1, 28)
        date = '%d-%02d-%02d' % (y, m, d)

        weibo = Weibo(
            uid=random.choice(users).id,
            content=fake_sentence(),
            created=date,
            updated=date,
        )
        weibo_list.append(weibo)

    db.session.add_all(weibo_list)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
