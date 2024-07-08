from pymongo import ASCENDING, DESCENDING
from ..database.mongodb import db
from bson.objectid import ObjectId
from datetime import datetime,timezone
from pymongo import DESCENDING

class DocumentModel:
    collection = db['documents']

    @staticmethod
    def create_indexes():
        """
        创建必要的索引。
        """
        DocumentModel.collection.create_index([('user_id', ASCENDING)])
        DocumentModel.collection.create_index([('filename', ASCENDING), ('user_id', ASCENDING)], unique=True)
        DocumentModel.collection.create_index([('updated_at', DESCENDING)])

    @staticmethod
    def create(document):
        """
        创建一个新的文档。

        :param document: dict 包含文档数据，包括 user_id, filename, content, last_used_time
        :return: ObjectId 插入文档的ID
        """
        document['created_at'] = datetime.now(timezone.utc)
        document['updated_at'] = datetime.now(timezone.utc)
        return DocumentModel.collection.insert_one(document).inserted_id

    @staticmethod
    def find_by_id(document_id):
        """
        通过ID查找文档。

        :param document_id: str 文档ID
        :return: dict 查找到的文档
        """
        return DocumentModel.collection.find_one({'_id': ObjectId(document_id)})

    @staticmethod
    def find_by_filename_and_user(filename, user_id):
        """
        通过文件名和用户ID查找文档。

        :param filename: str 文件名
        :param user_id: str 用户ID
        :return: dict 查找到的文档
        """
        print("model doc:",filename,user_id)
        return DocumentModel.collection.find_one({'filename': filename, 'user_id': (user_id)})

    @staticmethod
    def update(document_id, update_data):
        """
        更新文档。

        :param document_id: str 文档ID
        :param update_data: dict 更新的数据
        :return: UpdateResult 更新结果
        """
        update_data['updated_at'] = datetime.utcnow()
        return DocumentModel.collection.update_one({'_id': ObjectId(document_id)}, {'$set': update_data})

    @staticmethod
    def delete(document_id):
        """
        删除文档。

        :param document_id: str 文档ID
        :return: DeleteResult 删除结果
        """
        return DocumentModel.collection.delete_one({'_id': ObjectId(document_id)})

    @staticmethod
    def find_recent_documents(user_id, limit=10):
        """
        查找最近使用的文档。

        :param user_id: str 用户ID
        :param limit: int 返回文档的数量
        :return: list 最近使用的文档
        """
        documents = DocumentModel.collection.find({'user_id': (user_id)}).sort('updated_at', DESCENDING).limit(limit)
        return [DocumentModel._convert_id_to_str(doc) for doc in documents]

    @staticmethod
    def find_all_documents(user_id):
        """
        查找所有文档。

        :param user_id: str 用户ID
        :return: list 用户的所有文档
        """
        documents = DocumentModel.collection.find({'user_id': (user_id)}).sort('created_at', DESCENDING)
        return [DocumentModel._convert_id_to_str(doc) for doc in documents]

    @staticmethod
    def _convert_id_to_str(document):
        """
        将文档中的 _id 字段转换为字符串。

        :param document: dict 文档
        :return: dict 转换后的文档
        """
        document['_id'] = str(document['_id'])
        return document