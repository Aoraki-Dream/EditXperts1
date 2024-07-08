from pymongo import ASCENDING
from ..database.mongodb import db
from bson.objectid import ObjectId


class TemplateModel:
    collection = db["templates"]

    @staticmethod
    def create_indexes():
        """
        创建必要的索引。
        """
        TemplateModel.collection.create_index([("filename", ASCENDING)], unique=True)

    @staticmethod
    def create(template):
        """
        创建一个新的模版。

        :param template: dict 包含模版数据，包括 filename, content, last_used_time
        :return: ObjectId 插入模版的ID
        """
        return TemplateModel.collection.insert_one(template).inserted_id

    @staticmethod
    def find_by_id(template_id):
        """
        通过ID查找模版。

        :param template_id: str 模版ID
        :return: dict 查找到的模版
        """
        template = TemplateModel.collection.find_one({"_id": ObjectId(template_id)})
        return TemplateModel._convert_id_to_str(template) if template else None

    @staticmethod
    def update(template_id, update_data):
        """
        更新模版。

        :param template_id: str 模版ID
        :param update_data: dict 更新的数据
        :return: UpdateResult 更新结果
        """
        return TemplateModel.collection.update_one(
            {"_id": ObjectId(template_id)}, {"$set": update_data}
        )

    @staticmethod
    def delete(template_id):
        """
        删除模版。

        :param template_id: str 模版ID
        :return: DeleteResult 删除结果
        """
        return TemplateModel.collection.delete_one({"_id": ObjectId(template_id)})

    @staticmethod
    def find_all_templates():
        """
        查找所有模版。

        :return: list 所有模版
        """
        templates = TemplateModel.collection.find()
        return [TemplateModel._convert_id_to_str(doc) for doc in templates]

    @staticmethod
    def _convert_id_to_str(template):
        """
        将模版中的 _id 字段转换为字符串。

        :param template: dict 模版
        :return: dict 转换后的模版
        """
        if template:
            template["_id"] = str(template["_id"])
        return template
