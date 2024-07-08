from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# 使用初始化函数初始化扩展
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

print("Extensions initialized")
