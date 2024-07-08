import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("SECRET_KEY:", os.getenv('SECRET_KEY'))
print("DATABASE_USER:", os.getenv('DATABASE_USER'))
print("DATABASE_PASSWORD:", os.getenv('DATABASE_PASSWORD'))
print("DATABASE_HOST:", os.getenv('DATABASE_HOST'))
print("DATABASE_PORT:", os.getenv('DATABASE_PORT'))
print("DATABASE_NAME:", os.getenv('DATABASE_NAME'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DATABASE_USER')}:"
        f"{os.getenv('DATABASE_PASSWORD')}@"
        f"{os.getenv('DATABASE_HOST')}:"
        f"{os.getenv('DATABASE_PORT')}/"
        f"{os.getenv('DATABASE_NAME')}?charset=utf8"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
# 打印配置以调试
print("SQLALCHEMY_DATABASE_URI:", Config.SQLALCHEMY_DATABASE_URI)