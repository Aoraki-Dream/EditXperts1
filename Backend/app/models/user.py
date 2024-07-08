from ..extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """
    用户模型类，定义用户的基本信息和属性。

    属性:
        id (int): 用户ID，主键。
        username (str): 用户名，非空。
        email (str): 用户邮箱，唯一且非空。
        password (str): 用户密码，非空。
        nickname (str): 用户昵称，可为空。
        phone (str): 用户电话，可为空。
        birthday (date): 用户生日，可为空。
        avatar_url (str): 用户头像URL，可为空。
        address (str): 用户地址，可为空。
        created_at (datetime): 用户创建时间，默认当前时间。
        updated_at (datetime): 用户更新时间，默认当前时间，并在更新时自动更新。
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    birthday = db.Column(db.Date)
    avatar_url = db.Column(db.String(255))
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
