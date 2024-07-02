# -*- coding: utf-8 -*-
"""
@Auth ： Wen,Shuchang
@File ：forms.py
@IDE ：PyCharm

"""
from wtforms import Form, ValidationError, IntegerField
from wtforms.fields import StringField, FileField
from wtforms.validators import Email, Length, EqualTo, InputRequired
from flask_wtf.file import FileAllowed, FileSize
from OCT_webmodels.auth import UserModel
from exts import cache
from flask import request

class BaseForm(Form):
  @property
  def messages(self):
    message_list = []
    if self.errors:
      for errors in self.errors.values():
        message_list.extend(errors)
    return message_list

class RegisterForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱")])
    email_captcha = StringField(validators=[Length(6,6,message="请输入正确邮箱验证码")])
    username = StringField(validators=[Length(3,20,message="请输入规范用户名")])
    password = StringField(validators=[Length(6,20,message="请输入规范密码")])
    repeat_password = StringField(validators=[EqualTo("password",message="密码不一致！")])
    graph_captcha = StringField(validators=[Length(4,4,message="请输入正确的图形验证码")])

    #自定义的验证器form.validate()也会执行_
    def validate_email(self, field):
        email = field.data   # 通过 field.data 访问 email 字段的输入值
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise ValidationError(message="邮箱已经被注册！")

    def validate_email_captcha(self, field):
        email_captcha = field.data
        email = self.email.data #self is class RegisterForm
        cache_captcha = cache.get(email) # cache的验证码
        if not cache_captcha or email_captcha != cache_captcha:
            raise ValidationError(message="邮箱验证码错误！")

    def validate_graph_captcha(self, field):
        key = request.cookies.get("_graph_captcha_key")
        cache_captcha = cache.get(key)
        graph_captcha = field.data
        if not cache_captcha or graph_captcha.lower() != cache_captcha.lower():
            raise ValidationError(message="图形验证码错误！")

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱！")])
    password = StringField(validators=[Length(6, 20, message="请输入正确长度的密码！")])
    remember = IntegerField()

class UploadImageForm(BaseForm):
    image = FileField(validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], message="图片不符合要求"),
        FileSize(max_size = 1024*1024*5, message = "图片最大5M")
    ])

class PublicPostForm(BaseForm):
    title = StringField(validators=[Length(min=3, max=200, message="帖子标题必须在3-200之间")])
    content = StringField(validators=[InputRequired(message="请传入内容")])
    board_id = IntegerField(validators=[InputRequired(message="请传入板块的ID！")])

class PublicCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message= "请传入内容")])
    post_id = IntegerField(validators=[InputRequired(message="请传入帖子的ID！")])