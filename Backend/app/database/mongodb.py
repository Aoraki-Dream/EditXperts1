from pymongo import MongoClient
from .config import MONGODB_URI, MONGODB_DATABASE_NAME

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE_NAME]
