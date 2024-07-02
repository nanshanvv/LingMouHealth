# -*- coding: utf-8 -*-
"""
@Auth ： Wen,Shuchang
@File ：views.py
@IDE ：PyCharm

"""
from flask import Blueprint, send_from_directory, current_app

bp = Blueprint("media",__name__, url_prefix="/media")

@bp.route("/avatar/<filename>")
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)
"""
这段代码允许客户端请求和下载存储在服务器上的头像文件。
例如，如果有一个文件名为 user123.jpg 的头像存储在配置的 'AVATARS_SAVE_PATH' 目录下，
客户端可以通过访问 URL /media/avatar/user123.jpg 来获取这个头像文件
"""

@bp.route("/post/<filename>")
def get_post_image(filename):
    return send_from_directory(current_app.config['POST_IMAGE_SAVE_PATH'], filename)

@bp.route("/banner/<filename>")
def get_banner_image(filename):
    return send_from_directory(current_app.config['BANNER_IMAGE_SAVE_PATH'], filename)