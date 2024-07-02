# -*- coding: utf-8 -*-
"""
@Auth ： Wen,Shuchang
@File ：views.py
@IDE ：PyCharm

"""
from datetime import datetime, timedelta
from idlelib import window

from flask import Blueprint, request, current_app, g, redirect

from exts import db
from utils import restful
from .forms import UploadImageForm, AddBannerForm, EditBannerForm
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from OCT_webmodels.auth import UserModel
from OCT_webmodels.post import BannerModel,PostModel, CommentModel, BoardModel
from sqlalchemy.sql import func

bp = Blueprint("cmsapi", __name__, url_prefix="/cmsapi")

@bp.before_request
#@jwt_required()
def cmsapi_before_request():
    '''if request.method == 'OPTIONS':
        return
    identity = get_jwt_identity()
    user = UserModel.query.filter_by(id=identity).first()
    if user:
        setattr(g, "user", user)'''
    pass



@bp.get("/")
#@jwt_required()
def mytest():
    # 这个identify是当初通过create_access_token传入的identity
    identity = get_jwt_identity()
    return restful.ok(message="success", data={"identity": identity})
#http://127.0.0.1:5000/cmsapi/banner/image/upload
@bp.post("/banner/image/upload")
def upload_banner_image():
    form = UploadImageForm(request.files)
    if form.validate():
        image = form.image.data
        print(image)
        filename = image.filename
        image_path = os.path.join(current_app.config['BANNER_IMAGE_SAVE_PATH'], filename)
        image.save(image_path)
        return restful.ok(data={"image_url": filename})
    else:
        message = form.image.errors[0]
        return restful.params_error(message=message)

@bp.get("/location")
def get_location():
    # 使用完整的URL进行重定向
    return redirect("http://localhost:8080")

#添加轮播图
@bp.post("/banner/add")
def add_banner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner_model = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner_model)
        db.session.commit()
        return restful.ok(data=banner_model.to_dict())
    else:
        return restful.params_error(message=form.messages[0])

@bp.get("/banner/list")
def banner_list():
    banners = BannerModel.query.order_by(BannerModel.create_time.desc()).all()
    banner_dicts = [banner.to_dict() for banner in banners]
    return restful.ok(data=banner_dicts)

@bp.post("/banner/delete")
def delete_banner():
    banner_id = request.form.get("id")
    if not banner_id:
        return restful.params_error(message='没有传入id')
    try:
        banner_model = BannerModel.query.get(banner_id)
    except Exception as e:
        return restful.params_error(message='轮播图不存在')
    db.session.delete(banner_model)
    db.session.commit()
    return restful.ok()

@bp.post("/banner/edit")
def edit_banner():
    form = EditBannerForm(request.form)
    if form.validate():
        banner_id = form.id.data
        try:
            banner_model = BannerModel.query.get(banner_id)
        except Exception as e:
            return restful.params_error(message='轮播图不存在')
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data

        banner_model.name = name
        banner_model.image_url = image_url
        banner_model.link_url = link_url
        banner_model.priority =priority
        db.session.commit()
        return restful.ok(data=banner_model.to_dict())
    else:
        return restful.params_error(message=form.messages[0])

@bp.get("/post/list")
def post_list():
    page = request.args.get("page",default=1, type=int)
    start = (page - 1)*current_app.config['PER_PAGE_COUNT']
    end = start + current_app.config['PER_PAGE_COUNT']
    query_boj = PostModel.query.order_by(PostModel.create_time.desc())
    total_count = query_boj.count()
    posts = query_boj.slice(start, end)
    post_list = [post.to_dict() for post in posts]
    return restful.ok(data={'post_list': post_list,"total_count":total_count,"page":page})

@bp.post("/post/delete")
def delete_post():
    post_id = request.form.get("id")
    try:
        print(post_id)
        post_model = PostModel.query.get(post_id)
    except Exception as e:
        return restful.params_error(message='帖子不存在')
    db.session.delete(post_model)
    db.session.commit()
    return restful.ok()

@bp.get("/comment/list")
def conmment_list():
    comments = CommentModel.query.order_by(CommentModel.create_time.desc()).all()
    comment_list = []
    for comment in comments:
        comment_dict = comment.to_dict()
        comment_list.append(comment_dict)
    return restful.ok(data=comment_list)

@bp.post("/comment/delete")
def delete_comment():
    comment_id = request.form.get('id')
    CommentModel.query.filter_by(id=comment_id).delete()
    return restful.ok()

@bp.get('/user/list')
def user_list():
    users = UserModel.query.order_by(UserModel.join_time.desc()).all()
    for user in users:
        user_dict_list = [user.to_dict() for user in users]
        return restful.ok(data=user_dict_list)

@bp.post('/user/active')
def user_active():
    is_active = request.form.get('is_active', type=int)
    user_id = request.form.get('id')
    user = UserModel.query.get(user_id)
    user.is_active = bool(is_active)
    db.session.commit()
    return restful.ok(data=user.to_dict())

@bp.get('/board/post/count')
def board_post_count():
    #获取板块下帖子数量
    board_post_count_list = db.session.query(BoardModel.name, func.count(BoardModel.name)).join(PostModel).group_by(BoardModel.name).all()
    # print (board_post_count_list)
    board_names = []
    post_counts = []
    for board_post_count in board_post_count_list:
        board_names.append(board_post_count[0])
        post_counts.append(board_post_count[1])
    return restful.ok(data={'board_names':board_names, 'post_counts':post_counts})

@bp.get('/day7/post/count')
def day7_post_count():
    # 日期，帖子数量
    now = datetime.now()
    seven_day_ago = now - timedelta(days=6, hours=now.hour, minutes=now.minute, seconds=now.second,
                                    microseconds=now.microsecond)
    day7_post_count_list = db.session.query(func.date_format(PostModel.create_time, "%Y-%m-%d"),
                                            func.count(PostModel.id)).group_by(
        func.date_format(PostModel.create_time, "%Y-%m-%d")).filter(PostModel.create_time >= seven_day_ago).all()
    day7_post_count_dict = dict(day7_post_count_list)
    for x in range(7):
        date = seven_day_ago + timedelta(days=x)
        date_str = date.strftime("%Y-%m-%d")
        if date_str not in day7_post_count_dict:
            day7_post_count_dict[date_str] = 0
    dates = sorted(list(day7_post_count_dict.keys()))
    counts = []
    for date in dates:
        counts.append(day7_post_count_dict[date])
    data = {"dates": dates, "counts": counts}
    return restful.ok(data=data)

