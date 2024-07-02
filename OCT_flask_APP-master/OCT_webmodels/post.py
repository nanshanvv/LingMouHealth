# -*- coding: utf-8 -*-
"""
@Auth ： Wen,Shuchang
@File ：post.py
@IDE ：PyCharm

"""
from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class BoardModel (db.Model, SerializerMixin):
    serialize_only = ("id", "name", "priority","create_time")
    __tablename__ = "board"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)#自动增长
    name = db.Column(db.String(26), unique=True)
    priority = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)

class PostModel (db.Model, SerializerMixin):
    serialize_only = ('id', 'title', 'content', 'create_time', 'board', 'author')
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)#自动增长
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('user.id'))

    board = db.relationship("BoardModel", backref=db.backref("posts"))
    author = db.relationship("UserModel", backref=db.backref("posts"))

class BannerModel(db.Model, SerializerMixin):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)

class CommentModel(db.Model, SerializerMixin):

    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("user.id"), nullable=False)
#order_by用创建时间的反向排序; cascade级联删除（问答删除则下面评论全部删除）
    post = db.relationship("PostModel", backref=db.backref('comments', order_by="CommentModel.create_time.desc()",
                                                           cascade="delete, delete-orphan"))
    author = db.relationship("UserModel", backref='comments')