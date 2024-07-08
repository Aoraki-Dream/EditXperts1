from ..models.user import User
from ..extensions import db, bcrypt

def get_user_by_id(user_id):
    """
    根据用户ID获取用户信息。

    :param user_id: int 用户ID
    :return: User 对应的用户对象，如果不存在则返回None
    """
    return User.query.get(user_id)

def get_user_by_email(email):
    """
    根据用户邮箱获取用户信息。

    :param email: str 用户邮箱
    :return: User 对应的用户对象，如果不存在则返回None
    """
    return User.query.filter_by(email=email).first()

def create_user(username, email, password, nickname=None, phone=None, birthday=None, avatar_url=None, address=None):
    """
    创建新用户。

    :param username: str 用户名
    :param email: str 用户邮箱
    :param password: str 用户密码
    :param nickname: str 用户昵称，默认为None
    :param phone: str 用户电话，默认为None
    :param birthday: date 用户生日，默认为None
    :param avatar_url: str 用户头像URL，默认为None
    :param address: str 用户地址，默认为None
    :return: User 创建的用户对象
    """
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(
        username=username,
        email=email,
        password=hashed_password,
        nickname=nickname,
        phone=phone,
        birthday=birthday,
        avatar_url=avatar_url,
        address=address
    )
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user, data):
    """
    更新用户信息。

    :param user: User 需要更新的用户对象
    :param data: dict 包含更新数据的字典
    :return: User 更新后的用户对象
    """
    if 'email' in data:
        user.email = data['email']
    if 'nickname' in data:
        user.nickname = data['nickname']
    if 'phone' in data:
        user.phone = data['phone']
    if 'birthday' in data:
        user.birthday = data['birthday']
    if 'avatar_url' in data:
        user.avatar_url = data['avatar_url']
    if 'address' in data:
        user.address = data['address']
    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    db.session.commit()
    return user
