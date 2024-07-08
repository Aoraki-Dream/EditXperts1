from functools import wraps
from flask import request, jsonify, g
import jwt
from app.models import User
from flask import current_app

def token_required(f):
    """
    装饰器：验证请求中的JWT token，并将当前用户信息添加到全局对象中。

    :param f: function 被装饰的函数
    :return: function 包装后的函数
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        """
        验证请求头中的JWT token，如果验证成功，则继续执行被装饰的函数。

        :return: 被装饰函数的返回值，或包含错误信息的JSON响应
        """
        token = None

        # 从请求头中获取Authorization字段，并提取token
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        # 如果没有提供token，返回401错误
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # 解码token，获取用户信息
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            g.current_user = current_user
        except jwt.ExpiredSignatureError:
            # 如果token过期，返回401错误
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            # 如果token无效，返回401错误
            return jsonify({'message': 'Token is invalid!'}), 401

        # 执行被装饰的函数
        return f(*args, **kwargs)

    return decorated
