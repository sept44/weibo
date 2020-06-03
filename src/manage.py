#!/usr/bin/env python

from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import render_template

from libs.db import db
from libs import config
from user.views import user_bp

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


@app.route('/')
def home():
    return render_template('base.html')


if __name__ == "__main__":
    manager.run()
