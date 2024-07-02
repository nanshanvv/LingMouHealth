# -*- coding: utf-8 -*-
"""
@Auth ： Wen,Shuchang
@File ：commands.py
@IDE ：PyCharm

"""
import random

from OCT_webmodels.post import *
from OCT_webmodels.auth import *
from exts import db

def init_boards():
    board_names = ['眼科小知识', '医院推荐', 'OCT预诊', '关于我们']
    for index, board_name in enumerate(board_names):
        board = BoardModel(name=board_name, priority=len(board_names)-index)
        db.session.add(board)
    db.session.commit()
    print("success")

def create_test_post():
    boards = list(BoardModel.query.all())
    board_count = len(boards)
    for x in range(99):
        title = "分页测试%d"%x
        content = "我是内容%d"%x
        author = UserModel.query.first()
        index = random.randint(0, board_count-1)
        board = boards[index]
        post_model = PostModel(title=title, content=content, board=board, author=author)
        db.session.add(post_model)
    db.session.commit()
    print("测试添加成功")