# -*- coding: utf-8 -*-
"""
@Auth ： Wen,Shuchang
@File ：views.py
@IDE ：PyCharm

"""

import time
from hashlib import md5
from io import BytesIO

from flask import Blueprint, request, render_template, jsonify, make_response, session, redirect, g, url_for
from flask import current_app
from flask_mail import Message
from werkzeug.utils import secure_filename
from exts import mail, db
from exts import cache
from model_use import model_predict, model
import os
from app import *
import string, random
from utils import restful
from utils.captcha import Captcha
from .forms import RegisterForm, LoginForm, UploadImageForm, PublicPostForm, PublicCommentForm
from OCT_webmodels.auth import UserModel
from OCT_webmodels.post import *
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy.sql import func
from flask_jwt_extended import create_access_token
# 蓝图名字为front
bp = Blueprint("front", __name__, url_prefix="/")


@bp.route('/', methods=['GET'])
def index():
    # Main page
    sort = request.args.get('st', type=int, default=1)
    board_id = request.args.get('bd',type=int, default=None)
    boards = BoardModel.query.order_by(BoardModel.priority.desc()).all()
    post_query = None
    if sort == 1:
        post_query = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        #外连接帖子表和评论表
        post_query = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())

    page = request.args.get(get_page_parameter(), type=int, default=1)
    # 若一页10条则 page1:0-9，page2:10-19
    start = (page - 1) * current_app.config["PER_PAGE_COUNT"]
    end = start + current_app.config["PER_PAGE_COUNT"]
    #板块分类
    if board_id:
        # "mapped class CommentModel->comment" has no property "board_id"
        # CommentModel中寻找board_id，然后进行过滤
        # post_query = post_query.filter_by(board_id=board_id)
        post_query = post_query.filter(PostModel.board_id == board_id)
    total = post_query.count()
    posts = post_query.slice(start, end)
    pagination = Pagination(ba_version=3, page=page, total=total)

    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    context = {
        "boards": boards,
        "posts": posts,
        "pagination": pagination,
        "st": sort,
        "back_bd": board_id,
        "banners": banners
    }
    return render_template('front/index.html', **context)


# @bp.get('/email/captcha')
# def email_captcha():
#     # 传邮箱方式： email/captcha?email=xxx@example.com
#     """
#     request.args 是用于访问 URL 的查询字符串的参数。
#     查询字符串是 URL 中的一部分，位于问号 (?) 之后，用于传递额外的参数和值。
#     request.args.get('email') 用于获取名为 email 的查询参数的值。
#     """
#     email = request.args.get('email')
#     if not email:
#         return restful.params_error(message="Invalid email address")
#     # 六位数字验证码
#     source = list(string.digits)
#     captcha = "".join(random.sample(source, 6))
#     subject = '预诊断平台注册验证码'
#     body = "your code:%s" % captcha
#     current_app.celery.send_task("send_mail", (email, subject, body))
#     cache.set(email, captcha)
#     print(cache.get(email))
#     return restful.ok(message="邮件发送成功")

@bp.get('/email/captcha')
def email_captcha():
    # 传邮箱方式： email/captcha?email=xxx@example.com
    email = request.args.get('email')
    if not email:
        return restful.params_error(message="Invalid email address")

    # 六位数字验证码
    source = list(string.digits)
    captcha = "".join(random.sample(source, 6))

    subject = '预诊断平台注册验证码'
    body = f"""
    <h1>Welcome！欢迎注册灵眸健康平台</h1>
    <p>您的验证码是：<strong>{captcha}</strong></p>
    <p>灵眸健康平台专注于眼底疾病的预诊断，致力于为医生和科研人员提供便捷的沟通交流渠道。
    通过先进的技术和精准的诊断工具，灵眸健康平台不仅帮助患者及时发现眼底问题，还为医生提供高效的诊疗支持。
    科研人员也可以通过平台共享最新研究成果，促进医学进步，共同提升眼健康水平。</p>
    <p>Lingmou Health Platform focuses on the pre-diagnosis of fundus diseases and is dedicated to providing convenient communication channels for doctors and researchers. 
    Through advanced technology and precise diagnostic tools, Lingmou Health Platform not only helps patients detect fundus problems early but also provides doctors with efficient diagnostic support. 
    Researchers can also share the latest research findings through the platform, promoting medical advancements and collectively enhancing vision health.</p>
    <img src='cid:image1'>
    """

    current_app.celery.send_task("send_mail", (email, subject, body))
    cache.set(email, captcha)
    print(cache.get(email))
    return restful.ok(message="邮件发送成功")


@bp.route("/graph/capthca")
def graph_captcha():
    captcha, image = Captcha.gene_graph_captcha()
    # 将验证码存入缓存
    # key, value
    key = md5((captcha + str(time.time())).encode('utf-8')).hexdigest()
    cache.set(key, captcha)
    # 将image转成二进制从而让浏览器可以加载
    # with open("captcha.png", "wb") as fp:
    #     image.save(fp,"png")
    out = BytesIO()
    image.save(out, "png")
    # 把out指针指向最开始的位置，不然resp读的是个空
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = "image/png"
    resp.set_cookie("_graph_captcha_key", key, max_age=3600)
    return resp


@bp.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Ensure the 'uploads' directory exists in the root path of the application
        uploads_dir = os.path.join(current_app.root_path, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)  # Create 'uploads' directory if it does not exist

        # Save the file to the 'uploads' directory
        file_path = os.path.join(uploads_dir, secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        result, img_path, output_str = model_predict(file_path, model)
        print(result)
        print(output_str)
        # Return the result
        return jsonify({"result": result, "details": output_str})
    else:
        # Handle the case for non-POST requests or return a specific message
        return "Please use a POST request to upload the file."


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("front/login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            # 验证邮箱密码
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                return restful.params_error("邮箱或密码错误")
            if not user.check_password(password):
                return restful.params_error("邮箱或密码错误")
            session['user_id'] = user.id
            #如果是管理员才生成token
            token = ""
            if user.is_staff:
                token = create_access_token(identity=user.id)
            if remember == 1:
                # 默认关闭浏览器的话session过期
                session.permanent = True
                return restful.ok(data={'token': token, "user": user.to_dict()})
            else:
                session.permanent = False
                return restful.ok()
        else:
            return restful.params_error(message=form.messages[0])


@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("front/register.html")
    else:
        form = RegisterForm(request.form)

        if form.validate():
            email = form.email.data
            password = form.password.data
            uswename = form.username.data
            user = UserModel(email=email, password=password, username=uswename)
            db.session.add(user)
            db.session.commit()
            return restful.ok()
        else:
            message = form.messages[0]
            return restful.params_error(message=message)

        '''
        form.validate() 是 WTForms 库中的一个方法，用于检查表单数据是否符合定义的验证规则。
        每个字段（比如 email, username, password 等）都可以有一个或多个验证器（validator），
        验证器定义了数据应该满足的条件（例如，电子邮件字段可能需要通过电子邮件格式验证器）。
        当你调用 form.validate() 时，WTForms 将遍历表单中的每个字段，运行与之关联的所有验证器，
        以确保每个字段的数据都是有效的。如果所有字段都通过验证，form.validate() 将返回 True，表示表单数据是有效的。
        如果任何字段未通过验证，它将返回 False，并且可以通过 form.errors 访问具体的错误信息。
        '''


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# 钩子函数,在调用视图函数之前执行
@bp.before_request
def front_before_request():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)


# 上下文处理器
@bp.context_processor
def front_context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


# 请求 => 钩子函数 => 视图函数（返回模板）=> context_processor =>将context_processor返回的对象也添加到模板中


@bp.route('/setting')
@login_required  # 必须登陆后才能访问：装饰器
def setting():
    email_hash = md5(g.user.email.encode('utf-8')).hexdigest()
    return render_template('front/setting.html', email_hash=email_hash)


@bp.post('/avatar/upload')
@login_required
def upload_avatar():
    form = UploadImageForm(request.files)
    if form.validate():
        image = form.image.data
        filename = image.filename
        image_path = os.path.join(current_app.config['AVATARS_SAVE_PATH'], filename)
        image.save(image_path)
        g.user.avatar = filename
        db.session.commit()
        return restful.ok(data={"avatar": filename})
    else:
        message = form.image.errors[0]
        return restful.params_error(message=message)


@bp.route("/post/public", methods=["POST", "GET"])
def public_post():
    if request.method == "GET":
        boards = BoardModel.query.all()
        return render_template("front/public_post.html", boards=boards)
    else:
        form = PublicPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            try:
                board = BoardModel.query.get(board_id)
            except Exception as e:
                return restful.params_error(message="板块不存在")
            post_model = PostModel(title=title, content=content, board_id=board_id, author=g.user)
            db.session.add(post_model)
            db.session.commit()
            return restful.ok(data={'id':post_model.id})
        else:
            return restful.params_error(message=form.messages[0])


@bp.post('/post/image/upload')
@login_required
def upload_public_image():
    form = UploadImageForm(request.files)
    if form.validate():
        image = form.image.data
        filename = image.filename
        image_path = os.path.join(current_app.config['POST_IMAGE_SAVE_PATH'], filename)
        image.save(image_path)
        return jsonify({"errno": 0, "data": [{
            "url": url_for("media.get_post_image", filename=filename),
            "alt": filename,
            "href": ""
        }]})
    else:
        message = form.image.errors[0]
        return restful.params_error(message=message)

#帖子详情页没有数据传输，所以可以直接get（发评论是另外模块的功能了）
@bp.get('/post/detail/<int:post_id>')
def post_detail(post_id):
    try:
        post_model = PostModel.query.get(post_id)
    except:
        return "404"
    comment_count = CommentModel.query.filter_by(post_id=post_id).count()
    context = {
        "post": post_model,
        "comment_count": comment_count
    }
    return render_template("front/post_detail.html", **context)

@bp.post('/comment')
@login_required
def public_comment():
    form = PublicCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        try:
            post_model = PostModel.query.get(post_id)
        except Exception as e:
            return restful.params_error(message="帖子不存在")
        comment = CommentModel(content=content, post_id=post_id, author_id=g.user.id)
        db.session.add(comment)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message=form.messages[0])

@bp.get('/classification')
def classification():
    return render_template('front/classification.html')
