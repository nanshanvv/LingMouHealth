# -*- coding: utf-8 -*-
"""
@Auth ： Wen,Shuchang
@File ：apps.py
@IDE ：PyCharm

"""

import os
from datetime import timedelta

SECRET_KEY = "2001922"

#项目根路径
BASE_DIR = os.path.dirname(__file__)

DB_USERNAME = 'root'
DB_PASSWORD = '2001922'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'bishe'

# session.permanent=True的情况下的过期时间
PERMANENT_SESSION_LIFETIME = timedelta(days=7)




DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# lbdhhczhskawhaeb
# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件
# 发送者邮箱的服务器地址
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_USE_SSL = True
MAIL_USERNAME = "1585870861@qq.com"
MAIL_PASSWORD = "ayxwlricecqngbja"
MAIL_DEFAULT_SENDER = "1585870861@qq.com"

#celery的redis配置
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
#flask-chching
CACHE_TYPE = "RedisCache"
CACHE_DEFAULT_TIMEOUT = 300
CACHE_REDIS_HOST = "127.0.0.1"
CACHE_REDIS_POST = 6379

AVATARS_SAVE_PATH = os.path.join(BASE_DIR, "media", "avatars")

#帖子图片路径
POST_IMAGE_SAVE_PATH = os.path.join(BASE_DIR, "media", "post")

#每一页帖子数量
PER_PAGE_COUNT = 10

#JWT过期时间
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

#轮播图路径
BANNER_IMAGE_SAVE_PATH = os.path.join(BASE_DIR, "media", "banner")