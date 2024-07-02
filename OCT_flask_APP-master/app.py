# -*- coding: utf-8 -*-
"""
@Auth ： Wen,Shuchang
@File ：apps.py
@IDE ：PyCharm

"""

from __future__ import division, print_function
# coding=utf-8
import os
import json
import matplotlib

import commands

matplotlib.use('agg')

import config
from exts import db, mail, cache, csrf, avatars,jwt,cors
from flask_migrate import Migrate
from OCT_webmodels import auth
from apps.front import front_bp
from apps.media import media_bp
from apps.cmsapi import cmsapi_bp
from model_use import model_predict
from oct_celery import make_celery



# Flask utils
from flask import Flask
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from flask import current_app



# Torch
import torch
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

# Define a flask app
app = Flask(__name__)

app.config.from_object(config)
# #database
#将ORM模型映射到数据库步骤
#0.migrate=Migrate(app.db)
#1.初始化：flask db init
#2.将orm模型生成迁移脚本：flask db migrate
#3.运行脚本：flask db upgrade
db.init_app(app)
mail.init_app(app)
cache.init_app(app)
csrf.init_app(app)
avatars.init_app(app)
jwt.init_app(app)
cors.init_app(app, supports_credentials=True)

#排除cmsapi除去csrf验证
csrf.exempt(cmsapi_bp)

migrate = Migrate(app,db)

# 在windows上使用celery，需要借助gevnet发邮件
# pip install gevent
# celery -A app.mycelery worker --loglevel=info -P gevent

mycelery = make_celery(app)

#注册蓝图
app.register_blueprint(front_bp)
app.register_blueprint(media_bp)
app.register_blueprint(cmsapi_bp)
#创建命令
app.cli.command("init_boards")(commands.init_boards)
app.cli.command("create_test_post")(commands.create_test_post)






if __name__ == '__main__':
    # Serve the app with gevent
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
    # app.run()
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
