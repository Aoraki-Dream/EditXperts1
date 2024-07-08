from flask import Blueprint, request, jsonify, g
from ..services.template_service import TemplateService
from ..middleware.authority import token_required

template_bp = Blueprint("template_bp", __name__)

@template_bp.route("/template", methods=["POST"])
def create_template():
    """
    创建一个新的模版。

    :return: JSON 新模版的ID
    """
    filename = request.form.get("filename")
    content = request.form.get("content")

    if not filename or not content:
        return jsonify({"error": "Missing required fields"}), 400

    if TemplateService.get_template_by_filename(filename):
        return jsonify({"error": "Template with this filename already exists"}), 400

    template_id = TemplateService.create_template(filename, content)
    return jsonify({"_id": str(template_id)}), 201


@template_bp.route("/<template_id>", methods=["GET"])
def get_template(template_id):
    """
    获取模版内容。

    :param template_id: str 模版ID
    :return: JSON 模版内容
    """
    template = TemplateService.get_template(template_id)
    if template:
        return jsonify(template), 200
    return jsonify({"error": "Template not found"}), 404


@template_bp.route("/<template_id>", methods=["DELETE"])
def delete_template(template_id):
    """
    删除模版。

    :param template_id: str 模版ID
    :return: JSON 删除结果
    """
    result = TemplateService.delete_template(template_id)
    if result.deleted_count:
        return jsonify({"msg": "Template deleted"}), 200
    return jsonify({"error": "Template not found"}), 404


@template_bp.route("/template", methods=["GET"])
def get_all_templates():
    """
    获取所有模版。

    :return: JSON 所有模版列表
    """
    templates = TemplateService.get_all_templates()
    return jsonify({"templates": templates}), 200
