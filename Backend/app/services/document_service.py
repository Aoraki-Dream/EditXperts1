from ..models.document import DocumentModel
from datetime import datetime, timezone
from bson.objectid import ObjectId


class DocumentService:

    @staticmethod
    def create_document(user_id, filename, content):
        """
        创建新的HTML文档。

        :param user_id: str 用户ID
        :param filename: str 文件名
        :param content: str HTML内容
        :return: ObjectId 新文档的ID
        """
        document = {
            "user_id": (user_id),
            "filename": filename,
            "content": content,
            "last_used_time": datetime.now(timezone.utc),
        }
        return DocumentModel.create(document)

    @staticmethod
    def get_document(document_id):
        """
        获取文档内容并更新最后使用时间。

        :param document_id: str 文档ID
        :return: dict 文档内容
        """
        document = DocumentModel.find_by_id(document_id)
        if document:
            DocumentModel.update(
                document_id, {"last_used_time": datetime.now(timezone.utc)}
            )
        return document

    @staticmethod
    def get_document_by_filename_and_user(filename, user_id):
        """
        通过文件名和用户ID获取文档内容并更新最后使用时间。

        :param filename: str 文件名
        :param user_id: str 用户ID
        :return: dict 文档内容
        """
        document = DocumentModel.find_by_filename_and_user(filename, user_id)
        if document:
            DocumentModel.update(
                document["_id"], {"last_used_time": datetime.now(timezone.utc)}
            )
        return document

    @staticmethod
    def update_document(document_id, content):
        """
        更新已有文档内容并更新最后使用时间。

        :param document_id: str 文档ID
        :param content: str HTML内容
        :return: UpdateResult 更新结果
        """
        return DocumentModel.update(
            document_id,
            {"content": content, "last_used_time": datetime.now(timezone.utc)},
        )

    @staticmethod
    def get_recent_documents(user_id, limit=10):
        """
        获取最近使用的文档。

        :param user_id: str 用户ID
        :param limit: int 返回文档的数量
        :return: list 最近使用的文档
        """
        return DocumentModel.find_recent_documents(user_id, limit)

    @staticmethod
    def get_all_documents(user_id):
        """
        获取所有文档。

        :param user_id: str 用户ID
        :return: list 用户的所有文档
        """
        return DocumentModel.find_all_documents(user_id)
