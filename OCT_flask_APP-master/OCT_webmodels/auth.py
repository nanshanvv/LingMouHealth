from exts import db
import shortuuid
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy_serializer import SerializerMixin




class UserModel(db.Model, SerializerMixin):
    #元组不加逗号会报错
    # serialize_rules = ("-_password", )
    serialize_only = ("id", "email", "username", "avatar", "signature", "join_time", "is_staff", "is_active")
    __tablename__ = "user"
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    #非明文密码
    _password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    join_time = db.Column(db.DateTime, default=datetime.now)
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    # role_id = db.Column(db.Integer, db.ForeignKey("role.id"))

#位置参数 (*args) 和关键字参数 (**kwargs)
    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")
        #已经吧password属性给pop了，所以再执行__init__就是初始化其他属性
        super(UserModel, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)
    def check_password(self, rawpwd):
        return check_password_hash(self.password, rawpwd)