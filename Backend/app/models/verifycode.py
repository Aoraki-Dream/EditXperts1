from ..extensions import db
from flask_login import UserMixin

class EmailVerification(UserMixin, db.Model):
    """
    邮箱验证模型类，定义邮箱验证的基本信息和属性。

    属性:
        id (int): 验证记录的ID，主键，自增。
        email (str): 需要验证的邮箱地址，非空。
        code (str): 验证码，非空。
        created_at (datetime): 记录创建时间，默认当前时间。
        request_count (int): 验证码请求次数，默认为1。
        last_request (datetime): 最后一次请求时间，默认当前时间，并在更新时自动更新。
    """
    __tablename__ = 'email_verifications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    request_count = db.Column(db.Integer, default=1)
    last_request = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
