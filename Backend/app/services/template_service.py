from ..models.template_model import TemplateModel

class TemplateService:

    @staticmethod
    def create_template(filename, content):
        """
        创建一个新的模版。
        :param filename: str 模版文件名
        :param content: str 模版内容
        :return: ObjectId 新模版的ID
        """
        template = {
            "filename": filename,
            "content": content
        }
        return TemplateModel.create(template)

    @staticmethod
    def get_template(template_id):
        """
        获取模版内容。
        :param template_id: str 模版ID
        :return: dict 模版内容
        """
        return TemplateModel.find_by_id(template_id)

    @staticmethod
    def delete_template(template_id):
        """
        删除模版。
        :param template_id: str 模版ID
        :return: DeleteResult 删除结果
        """
        return TemplateModel.delete(template_id)

    @staticmethod
    def get_all_templates():
        """
        获取所有模版。
        :return: list 所有模版
        """
        return TemplateModel.find_all_templates()

    @staticmethod
    def get_template_by_filename(filename):
        """
        通过文件名获取模版。
        :param filename: str 模版文件名
        :return: dict 模版内容
        """
        return TemplateModel.collection.find_one({"filename": filename})
