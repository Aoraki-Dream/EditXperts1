import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm.exc import NoResultFound
from ..models.verifycode import EmailVerification
from ..extensions import db

# 加载环境变量
load_dotenv()
QQ_APP_ID = os.getenv("QQ_APP_ID")
QQ_APP_KEY = os.getenv("QQ_APP_KEY")


def generate_verification_code(length=6):
    """
    生成一个指定长度的验证码，包含大写字母和数字。

    :param length: int 验证码长度，默认为6
    :return: str 生成的验证码
    """
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def send_verification_email(to_email, verification_code):
    """
    发送包含验证码的验证邮件。

    :param to_email: str 接收验证邮件的邮箱地址
    :param verification_code: str 生成的验证码
    """
    from_email = QQ_APP_ID
    from_password = QQ_APP_KEY

    subject = "Your Verification Code"
    body = f"Your verification code is: {verification_code} , please enter it in the verification page to complete the registration process in 5 minutes."

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        # 启用SMTP连接的调试输出
        server = smtplib.SMTP_SSL("smtp.qq.com")
        server.set_debuglevel(1)
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


def store_verification_code(email, code):
    """
    存储或更新邮箱的验证码记录。

    :param email: str 邮箱地址
    :param code: str 生成的验证码
    """
    try:
        record = EmailVerification.query.filter_by(email=email).one()
        record.code = code
        record.created_at = datetime.now()
        db.session.commit()
    except NoResultFound:
        new_record = EmailVerification(
            email=email, code=code, created_at=datetime.now()
        )
        db.session.add(new_record)
        db.session.commit()


def verify_code(email, code):
    """
    验证邮箱和验证码是否匹配，并检查验证码是否在有效期内。

    :param email: str 邮箱地址
    :param code: str 验证码
    :return: bool 验证成功返回True，失败返回False
    """
    try:
        record = EmailVerification.query.filter_by(email=email, code=code).one()
        created_at_utc = record.created_at.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) - created_at_utc > timedelta(minutes=5):
            return False
        db.session.delete(record)
        db.session.commit()
        return True
    except NoResultFound:
        return False
