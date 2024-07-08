from flask import Blueprint, request, jsonify, current_app, g
from flask_login import  logout_user
from ..services.user_service import (
    get_user_by_email,
    create_user,
)
from ..extensions import db, bcrypt
from ..models.user import User
import jwt
from datetime import datetime, timedelta, timezone
from ..middleware.authority import token_required
from ..services.verifycode_service import (
    generate_verification_code,
    send_verification_email,
    store_verification_code,
    verify_code,
)

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/send_verification_code", methods=["POST"])
def send_verification_code_endpoint():
    """
    发送验证码到用户邮箱。

    接收用户的邮箱地址，生成一个验证码，将其存储起来，并通过电子邮件发送给用户。

    :return: JSON 包含操作结果的消息
    """
    email = request.form.get("email")
    if not email:
        return jsonify({"message": "Email is required"}), 400

    # 生成验证码并存储
    verification_code = generate_verification_code()
    store_verification_code(email, verification_code)
    send_verification_email(email, verification_code)

    return jsonify({"message": "Verification code sent"}), 200


@user_bp.route("/register", methods=["POST"])
def register():
    """
    用户注册接口，包含验证码验证。

    接收用户的注册信息，包括邮箱、验证码、用户名、密码，验证验证码的有效性后，创建用户账号。

    :return: JSON 包含操作结果的消息
    """
    data = request.form

    # 验证邮箱是否已经存在
    if get_user_by_email(data["email"]):
        return jsonify({"message": "Email already exists"}), 400

    # 验证验证码
    if not verify_code(data["email"], data["verification_code"]):
        return jsonify({"message": "Invalid or expired verification code"}), 400

    # 创建用户
    user = create_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        nickname=data.get("nickname"),
        phone=data.get("phone"),
        birthday=data.get("birthday"),
        avatar_url=data.get("avatar_url"),
        address=data.get("address"),
    )
    return jsonify({"message": "User created successfully"}), 201


# @user_bp.route("/register", methods=["POST"])
# def register():
#     """
#     注册新用户，无需验证码验证。

#     接收用户的注册信息，并创建新的用户账号，但不要求验证码验证。

#     :return: JSON 包含操作结果的消息和HTTP状态码。
#         - 成功时返回: `{'message': 'User created successfully'}`, 201
#         - 如果邮箱已存在，则返回: `{'message': 'Email already exists'}`, 400
#     """
#     data = request.form
#     if get_user_by_email(data["email"]):
#         return jsonify({"message": "Email already exists"}), 400
#     user = create_user(
#         username=data["username"],
#         email=data["email"],
#         password=data["password"],
#         nickname=data.get("nickname"),
#         phone=data.get("phone"),
#         birthday=data.get("birthday"),
#         avatar_url=data.get("avatar_url"),
#         address=data.get("address"),
#     )
#     return jsonify({"message": "User created successfully"}), 201


@user_bp.route("/login", methods=["POST"])
def login():
    """
    用户登录接口，通过邮箱和密码进行验证。

    接收用户的邮箱和密码，验证其有效性，并返回JWT令牌用于后续的身份验证。

    :param request.form: 包含用户登录信息的表单数据，包含'email'和'password'字段。
    :return: JSON 包含操作结果的消息和HTTP状态码。
        - 成功时返回: 包含JWT令牌的JSON对象，状态码200。
        - 凭证无效时返回: `{'message': 'Invalid credentials'}`, 状态码401。
    """
    data = request.form
    user = get_user_by_email(data["email"])
    # 获取当前UTC时间
    utc_now = datetime.now(timezone.utc)
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        token = jwt.encode(
            {"user_id": user.id, "exp": utc_now + timedelta(hours=24)},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@user_bp.route("/logout", methods=["POST"])
@token_required
def logout():
    """
    用户登出接口。

    :return: JSON 包含操作成功的消息和HTTP状态码200。
    """
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


@user_bp.route("/info", methods=["GET"])
@token_required
def get_user_info():
    """
    获取当前登录用户的个人信息。

    返回用户的个人信息。

    :return: JSON 包含用户信息的字典和HTTP状态码200。
    """
    user = g.current_user
    user_data = {
        "email": user.email,
        "username": user.username,
        "birthday": user.birthday,
        "phone": user.phone,
        "nickname": user.nickname,
        "avatar": user.avatar_url,
        "address": user.address,
    }
    return jsonify(user_data)


@user_bp.route("/update", methods=["POST"])
@token_required
def update_user():
    """
    更新当前登录用户的个人信息。

    :param request.form: 包含要更新的用户信息的表单数据。
    :return: JSON 包含操作结果的消息和HTTP状态码。
        - 成功时返回: `{'message': 'User updated successfully'}`, 200
        - 如果尝试更新的邮箱已存在且不等于当前用户的邮箱，则返回: `{'message': 'Email already exists'}`, 400
    """
    data = request.form
    user = g.current_user

    # 更新邮箱
    if "email" in data and data["email"]:
        if (
            User.query.filter_by(email=data["email"]).first()
            and data["email"] != user.email
        ):
            return jsonify({"message": "Email already exists"}), 400
        user.email = data["email"]

    # 更新其他信息
    if "password" in data and data["password"]:
        user.password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    if "nickname" in data and data["nickname"]:
        user.nickname = data["nickname"]

    if "phone" in data and data["phone"]:
        user.phone = data["phone"]

    if "birthday" in data and data["birthday"]:
        user.birthday = data["birthday"]

    if "avatar_url" in data and data["avatar_url"]:
        user.avatar_url = data["avatar_url"]

    if "address" in data and data["address"]:
        user.address = data["address"]

    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200
