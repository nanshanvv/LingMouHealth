# -*- coding: utf-8 -*-
"""
@Auth ： Wen,Shuchang
@File ：forms.py
@IDE ：PyCharm

"""
from flask_wtf.file import FileAllowed, FileSize
from wtforms.fields import FileField, StringField, IntegerField
from wtforms.validators import InputRequired

from apps.front.forms import BaseForm



class UploadImageForm(BaseForm):
    image = FileField(validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], message="图片不符合要求"),
        FileSize(max_size = 1024*1024*5, message = "图片最大5M")
    ])

class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='必须输入轮播图名称~')])
    image_url = StringField(validators=[InputRequired(message='必须输入轮播图链接~')])
    link_url = StringField(validators=[InputRequired(message='必须输入轮播图跳转链接~')])
    priority = IntegerField(validators=[InputRequired(message='必须输入轮播图优先级~')])

class EditBannerForm(AddBannerForm):
    id = IntegerField(validators=[InputRequired(message='必须输入轮播图id~')])