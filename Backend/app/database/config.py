import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DATABASE_NAME = os.getenv('MONGODB_DATABASE_NAME', 'your_database_name')

# print(MONGODB_URI,MONGODB_DATABASE_NAME)