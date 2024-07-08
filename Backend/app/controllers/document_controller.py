from flask import Blueprint, request, jsonify,g
from ..services.document_service import DocumentService
from ..middleware.authority import token_required
document_bp = Blueprint('document_bp', __name__)

@document_bp.route('/documents', methods=['POST'])
@token_required
def create_document():
    """
    创建一个新的HTML文档。
    
    :return: JSON 新文档的ID
    """
    # user_id = request.form.get('user_id')
    user_id = (str(g.current_user.id))
    filename = request.form.get('filename')
    content = request.form.get('content')
    
    if not filename or not content:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if DocumentService.get_document_by_filename_and_user(filename, user_id):
        return jsonify({'error': 'Document with this filename already exists for this user'}), 400
    if DocumentService.get_document_by_filename_and_user(filename, user_id):
        return jsonify({'error': 'Document with this filename already exists for this user'}), 400
    
    document_id = DocumentService.create_document(user_id, filename, content)
    return jsonify({'_id': str(document_id)}), 201

@document_bp.route('/<document_id>', methods=['GET'])
@token_required
def get_document(document_id):
    """
    获取文档内容并更新最后使用时间。
    
    :param document_id: str 文档ID
    :return: JSON 文档内容
    """
    document = DocumentService.get_document(document_id)
    if document:
        return jsonify(document), 200
    return jsonify({'error': 'Document not found'}), 404

@document_bp.route('/filename/<filename>', methods=['GET'])
@token_required
def get_document_by_filename_and_user( filename):
    """
    通过文件名和用户ID获取文档内容并更新最后使用时间。
    
    :param filename: str 文件名
    :return: JSON 文档内容
    """
    user_id = str(g.current_user.id)
    print("controller doc:",filename,user_id)
    document = list(DocumentService.get_document_by_filename_and_user(filename, user_id))
    if document:
        return jsonify(document), 200
    return jsonify({'error': 'Document not found'}), 404

@document_bp.route('/<document_id>', methods=['PUT'])
@token_required
def update_document(document_id):
    """
    更新已有文档内容并更新最后使用时间。
    
    :param document_id: str 文档ID
    :return: JSON 更新结果
    """
    content = request.form.get('content')
    result = DocumentService.update_document(document_id, content)
    if result.modified_count:
        return jsonify({'msg': 'Document updated'}), 200
    return jsonify({'error': 'Document not found or not modified'}), 404

@document_bp.route('/recent', methods=['GET'])
@token_required
def get_recent_documents():
    """
    获取最近使用的文档。
    
    :param user_id: str 用户ID
    :return: JSON 最近使用的文档列表
    """
    print("controller recent")
    user_id = str(g.current_user.id)
    limit = int(request.args.get('limit', 10))
    documents = list(DocumentService.get_recent_documents(user_id, limit))
    return jsonify({"documents":documents}), 200

@document_bp.route('/all', methods=['GET'])
@token_required
def get_all_documents():
    """
    获取用户的所有文档。
    
    :param user_id: str 用户ID
    :return: JSON 所有文档列表
    """
    user_id = str(g.current_user.id)
    documents = (DocumentService.get_all_documents(user_id))
    return jsonify({"documents":documents}), 200
