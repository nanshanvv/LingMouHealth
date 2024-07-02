# -*- coding: utf-8 -*-
"""
@Auth ： Wen,Shuchang
@File ：oct_celery.py
@IDE ：PyCharm
"""

from flask_mail import Message
from exts import mail
from celery import Celery
from flask import current_app
import os


# 定义任务函数
def send_mail(recipient, subject, body):
    message = Message(subject=subject, recipients=[recipient], html=body)

    # 获取图片路径
    with current_app.app_context():
        image_path = os.path.join(current_app.root_path, 'static/front/images/logo.png')

    with open(image_path, 'rb') as f:
        image_data = f.read()

    # 添加图片附件
    message.attach("logo.png", "image/png", image_data, 'inline', headers=[['Content-ID', '<image1>']])

    try:
        mail.send(message)
        return {"status": "SUCCESS"}
    except Exception as e:
        print(e)
        return {"status": "FAILURE"}


# 创建celery对象工厂函数
def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    app.celery = celery

    # 添加任务
    celery.task(name="send_mail")(send_mail)

    return celery
